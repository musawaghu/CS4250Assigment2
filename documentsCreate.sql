-- Table: public.documents

-- DROP TABLE IF EXISTS public.documents;

CREATE TABLE IF NOT EXISTS public.documents
(
    doc integer NOT NULL,
    text character varying COLLATE pg_catalog."default",
    title character varying COLLATE pg_catalog."default",
    num_chars integer,
    date character varying COLLATE pg_catalog."default",
    category_id integer,
    CONSTRAINT documents_pkey PRIMARY KEY (doc),
    CONSTRAINT documents_category_id_fkey FOREIGN KEY (category_id)
        REFERENCES public.categories (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to postgres;