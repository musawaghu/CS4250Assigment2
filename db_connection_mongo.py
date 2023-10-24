# -------------------------------------------------------------------------
# AUTHOR: Musa Waghu
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #2
# TIME SPENT: how long it took you to complete the assignment
# -----------------------------------------------------------*/
import pprint

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to
# work here only with standard arrays

# importing some Python libraries
from pymongo import MongoClient
import re


def connectDataBase():
    DB_NAME = "corpus"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")


def createDocument(col, docId, docText, docTitle, docDate, docCat):
    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    col = connectDataBase().get_collection("documents")
    term_count = {}
    text = docText
    num_char = re.sub(r'[!.?\s]', '', text)
    cleaned_text = re.sub(r'[?!.,]', '', text)
    term_identified = cleaned_text.lower().split()
    for term in term_identified:
        if term not in term_count:
            term_count[term] = 1
        else:
            term_count[term] += 1

    # create a list of dictionaries to include term objects.
    term_list = []
    for term, count in term_count.items():
        term_obj = {
            "term": term,
            "count": count,
            "num_chars": len(term)
        }
        term_list.append(term_obj)

    # Producing a final document as a dictionary including all the required document fields
    catName = docCat
    if catName == "Sports":
        catID = 1
    elif catName == "Seasons":
        catID = 2
    else:
        catID = random.randint(3, 100)
    document = {
        "id": docId,
        "title": docTitle,
        "text": docText,
        "num_chars": len(num_char),
        "date": docDate,
        "category": {
            "categoryid": catID,
            "name": docCat
        },
        "terms": term_list
    }

    # Insert the document
    col.insert_one(document)


def deleteDocument(col, docId):
    col = connectDataBase().get_collection("documents")
    col.delete_one({"id": docId})
    # Delete the document from the database
    # --> add your Python code here


def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Delete the document
    deleteDocument(col, docId)

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)


def getIndex(col):
    col = connectDataBase().get_collection("documents")
    result = {}

    # Retrieve all documents from the collection
    documents = col.find()

    # Iterate through the documents and update term counts
    for doc in documents:
        title = doc.get("title", "")
        text = doc.get("text", "").lower()
        cleaned_text = re.sub(r'[?!.,]', '', text)
        terms = cleaned_text.split()
        for term in terms:
            if term not in result:
                result[term] = {}
            if title in result[term]:
                result[term][title] += 1
            else:
                result[term][title] = 1

    # Iterate through the term counts and format the output
    formatted_result = {term: {doc: count for doc, count in doc_counts.items()} for term, doc_counts in result.items()}
    for term, doc_counts in formatted_result.items():
        print(f"'{term}': {', '.join([f'{doc}:{count}' for doc, count in doc_counts.items()])}")
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
