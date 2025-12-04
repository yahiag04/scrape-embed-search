import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

CSV_PATH = "books.csv"
VET_PATH = "vettorializzazione.npy"

def main():
    df = pd.read_csv(CSV_PATH)
    print("righe: ", len(df))

    df["title"]=df["title"].fillna("")
    df["category"]=df["category"].fillna("")

    df["search_text"] = df["title"] + " [CATEGORIA] " + df["category"]

    print("modello vettorializzazione: ")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts=df["search_text"].tolist()

    print("calcolo vettorializzazione: ")
    vettorializzazione = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
    )

    vettorializzazione = np.array(vettorializzazione)
    print("shape vettorializzazione: ", vettorializzazione.shape)

    np.save(VET_PATH, vettorializzazione)

if __name__ == "__main__":
    main()