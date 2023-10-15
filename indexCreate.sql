-- Table: public.index

-- DROP TABLE IF EXISTS public.index;

CREATE TABLE IF NOT EXISTS public.index
(
    doc integer NOT NULL,
    term character varying COLLATE pg_catalog."default" NOT NULL,
    count integer,
    CONSTRAINT index_pkey PRIMARY KEY (doc, term),
    CONSTRAINT index_doc_fkey FOREIGN KEY (doc)
        REFERENCES public.documents (doc) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT index_term_fkey FOREIGN KEY (term)
        REFERENCES public.terms (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.index
    OWNER to postgres;