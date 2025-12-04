# Semantic Book Search -- Scraping + Vettorializzazione + Dashboard

## Descrizione

Il progetto implementa un sistema completo di ricerca semantica a
partire da dati reali raccolti via web scraping.

Pipeline end-to-end:

1.  **Scraping** del sito pubblico di demo Books to Scrape tramite
    **Playwright**.\
2.  Costruzione di un **dataset strutturato** con ≥ 1000 libri.\
3.  **Vettorializzazione** del contenuto testuale con **Sentence
    Transformers**.\
4.  Implementazione di un **motore di ricerca semantico + filtri
    strutturati**.\
5.  **Dashboard interattiva** sviluppata con **Streamlit**.

------------------------------------------------------------------------

## Tecnologie utilizzate

-   Python\
-   Playwright\
-   Pandas, NumPy\
-   Sentence Transformers\
-   Scikit-learn\
-   Streamlit

------------------------------------------------------------------------

## Struttura del progetto

    project-root/
    │
    ├─ scrape_books.py          
    ├─ build_embeddings.py      
    ├─ app.py                   
    │
    ├─ books.csv                
    ├─ book_embeddings.npy      

------------------------------------------------------------------------

## Dataset

Ogni libro include:

-   `title`\
-   `category`\
-   `price`\
-   `rating`\
-   `product_page_url`

Dimensione: **\~1000 righe**

------------------------------------------------------------------------

## Embeddings

La stringa vettorializzata è:

    search_text = title + " [CATEGORY] " + category

Modello utilizzato: `all-MiniLM-L6-v2`\
Output: matrice `N x 384`

------------------------------------------------------------------------

## Motore di ricerca

### Ricerca semantica:

-   embedding della query\
-   cosine similarity con tutti i libri\
-   ordinamento per rilevanza

### Filtri strutturati:

-   categoria\
-   prezzo min/max\
-   rating minimo

------------------------------------------------------------------------

## Dashboard

Avvio della dashboard:

    streamlit run app.py

Funzionalità: - barra ricerca semantica\
- filtri categoria/prezzo/rating\
- tabella risultati

------------------------------------------------------------------------

## Setup

    pip install -r requirements.txt
    playwright install
    python scrape_books.py
    python build_embeddings.py
    streamlit run app.py

------------------------------------------------------------------------

## Cosa dimostra il progetto

-   Web scraping avanzato\
-   Data engineering\
-   Modelli di embeddings\
-   Motore di ricerca ibrido (semantico + strutturato)\
-   UI completa con Streamlit
