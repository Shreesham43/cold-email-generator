import pandas as pd
import uuid
import chromadb


class Portfolio:
    def __init__(self):
        self.df = pd.read_csv("./resources/portfolios.csv")
        self.client = chromadb.PersistentClient("portfolio")
        self.collection = self.client.get_or_create_collection(name = "portfolios")

    def load_portfolios(self):
        if not self.collection.count():
            for _, row in self.df.iterrows():
                self.collection.add(documents=row["Programming Skills"],
                            metadatas={"links": row["Portfolio URL"]},
                            ids=[str(uuid.uuid4())]
                            )
    def get_portfolio_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get("metadatas", []) 