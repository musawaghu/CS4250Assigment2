# -------------------------------------------------------------------------
# AUTHOR: Musa Waghu
# FILENAME: db_connection
# SPECIFICATION: inserting data into tables
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
# -----------------------------------------------------------*/

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to
# work here only with standard arrays

# importing some Python libraries
import psycopg2
from psycopg2.extras import RealDictCursor
import re


def connectDataBase():
    # Create a database connection object using psycopg2
    DB_NAME = "corpus"
    DB_USER = "postgres"
    DB_PASS = "123"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor,
                                )
        return conn

    except:
        print("Database not connected successfully")


def createCategory(cur, catId, catName):
    sql = "Insert into categories (id, name) Values (%s, %s)"
    recset = [catId, catName]
    cur.execute(sql, recset)


def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    sql = 'Select id from categories where name = %s'
    recset = [docCat]
    cur.execute(sql, recset)
    id = cur.fetchall()[0]["id"]

    sql = 'Select title from documents'
    recset = [docText]
    cur.execute(sql, recset)
    string = recset[0]
    cleaned_string = re.sub(r'[!.?\s]', '', string)
    num_chars = len(cleaned_string)
    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    sql = "Insert into documents (doc, text, title, num_chars, date, category_id) Values (%s, %s, %s, %s, %s, %s)"
    recset = [docId, docText, docTitle, num_chars, docDate, id]
    cur.execute(sql, recset)

    # 3 Update the potential new terms.
    cleaned_string2 = re.sub(r'[?!.]', '', string)
    term_identified = cleaned_string2.lower().split()
    sql = 'Select * from terms where term = %s'
    for i in term_identified:
        recset = [i]
        cur.execute(sql, recset)
        if (not cur.fetchall()):
            num_charTerm = len(i)
            sql2 = 'Insert into terms (term, num_chars) Values (%s, %s)'
            recset = [i, num_charTerm]
            cur.execute(sql2, recset)
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember
    # to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database --> add your Python code here

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    term_count = {}
    for word in term_identified:
        if word in term_count:
            term_count[word] += 1
        else:
            term_count[word] = 1

    for term, count in term_count.items():
        termToInsert = term
        countToInsert = count
        sql = 'Insert into index (doc, term, count) Values (%s, %s, %s)'
        recset = [docId, termToInsert, countToInsert]
        cur.execute(sql, recset)


def deleteDocument(cur, docId):
    sql = 'Select term from index where doc = %s'
    recset = [docId]
    cur.execute(sql, recset)
    test = cur.fetchall()
    for term in test:
        delete_term = (term["term"])
        sql2 = 'Delete from index where term = %s'
        recset = [delete_term]
        cur.execute(sql2, recset)
    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here

    # 2 Delete the document from the database
    sql = 'Delete from documents where doc = %(docId)s'
    cur.execute(sql, {'docId': docId})


def updateDocument(cur, docId, docText, docTitle, docDate, docCat):
    deleteDocument(cur, docId)
    # 1 Delete the document
    # --> add your Python code here

    # 2 Create the document with the same id
    createDocument(cur, docId, docText, docTitle, docDate, docCat)


def getIndex(cur):
    sql = 'select index.term, documents.title, count(*) as count from index inner join documents on index.doc = ' \
          'documents.doc group by term, title '
    cur.execute(sql)
    result = cur.fetchall()
    term_occur = {}
    for row in result:
        term = row['term']
        doc = row['title']
        count = row['count']
        if term in term_occur:
            term_occur[term] += f',{doc}:{count}'
        else:
            term_occur[term] = f'{doc}:{count}'

    for term, occurrences in term_occur.items():
        print(f"'{term}':'{occurrences}'")
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
