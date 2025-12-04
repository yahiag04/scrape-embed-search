import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

CSV_PATH = "books.csv"
VET_PATH = "vettorializzazione.npy"


@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    return df


@st.cache_resource
def load_embeddings():
    embeddings = np.load(VET_PATH)
    return embeddings


@st.cache_resource
def load_model():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return model


def semantic_search(
    df,
    embeddings,
    query: str,
    model,
    k: int = 20,
    category: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    min_rating: int | None = None,
):

    mask = np.ones(len(df), dtype=bool)

    # filtri
    if category and category != "All":
        mask &= (df["category"].values == category)

    if price_min is not None:
        mask &= (df["price"].values >= price_min)

    if price_max is not None:
        mask &= (df["price"].values <= price_max)

    if min_rating is not None:
        mask &= (df["rating"].values >= min_rating)

    effective_indices = np.where(mask)[0]

    if len(effective_indices) == 0:
        return df.iloc[[]]

    if not query.strip():
        return df.iloc[effective_indices].head(k)

    query_emb = model.encode([query])
    sims = cosine_similarity(query_emb, embeddings)[0]

    sims_filtered = sims[effective_indices]

    # Ordine su similarità, discendente
    top_idx_local = np.argsort(-sims_filtered)[:k]
    top_indices = effective_indices[top_idx_local]

    results = df.iloc[top_indices].copy()
    results["similarity"] = sims[top_indices]

    return results


def main():
    st.title("Books Semantic Search Dashboard")

    df = load_data()
    embeddings = load_embeddings()
    model = load_model()

    st.write("Dataset size:", len(df))


    query = st.text_input("Cerca per contenuto (es: 'machine learning', 'travel stories')", value="")

    st.sidebar.header("Filtri")

    categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Categoria", categories)

    price_min_val = float(df["price"].min())
    price_max_val = float(df["price"].max())

    price_min, price_max = st.sidebar.slider(
        "Range prezzo",
        min_value=price_min_val,
        max_value=price_max_val,
        value=(price_min_val, price_max_val),
        step=0.5,
    )

    rating_min = st.sidebar.slider(
        "Rating minimo",
        min_value=0,
        max_value=5,
        value=0,
        step=1,
    )
    min_rating = rating_min if rating_min > 0 else None

    # Numero di risultati
    k = st.sidebar.slider("Numero di risultati", min_value=5, max_value=50, value=20, step=5)

    if st.button("Cerca") or query or selected_category != "All" or rating_min > 0 or (price_min > price_min_val) or (price_max < price_max_val):
        results = semantic_search(
            df,
            embeddings,
            query=query,
            model=model,
            k=k,
            category=selected_category,
            price_min=price_min,
            price_max=price_max,
            min_rating=min_rating,
        )

        st.write(f"Risultati trovati: {len(results)}")

        if len(results) == 0:
            st.warning("Nessun risultato con questi parametri.")
        else:
            # Mostra solo colonne utili
            cols = ["title", "category", "price", "rating", "product_page_url"]
            if "similarity" in results.columns:
                cols.append("similarity")

            st.dataframe(results[cols])
    else:
        st.info("Inserisci una query o modifica i filtri, poi premi 'Cerca'.")


if __name__ == "__main__":
    main()