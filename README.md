# Semantic Book Search
### End-to-End Scraping → Embeddings → Semantic Search Dashboard

## Overview
Semantic Book Search is a full end-to-end search system built entirely in Python.
It demonstrates the complete pipeline from **web scraping** to **semantic retrieval** and an interactive **Streamlit** UI.

## Features
- Scraping 1000+ books via **Playwright**
- Dataset creation (title, category, price, rating, URL)
- Text embeddings using **Sentence Transformers (SBERT)**
- **Cosine similarity**-based semantic search
- Category, price, and rating filters
- Streamlit dashboard for interactive exploration


## Architecture
```
Scraping (Playwright)
        ↓
Dataset (books.csv)
        ↓
Embeddings (SBERT → book_embeddings.npy)
        ↓
Semantic Search Engine (Cosine Similarity + Filters)
        ↓
Streamlit Dashboard (Interactive UI)
```

## Installation
```
pip install -r requirements.txt
playwright install
```

## Run Scraper
```
python scrape_books.py
```

## Build Embeddings
```
python build_embeddings.py
```

## Launch Dashboard
```
streamlit run app.py
```

## Project Structure
```
semantic-book-search/
│
├── scrape_books.py
├── build_embeddings.py
├── app.py
│
├── books.csv
├── book_embeddings.npy
│
└── README.md
```

## Technologies
- Python
- Playwright
- SBERT (Sentence Transformers)
- scikit-learn
- pandas / numpy
- Streamlit

## License
MIT License.
