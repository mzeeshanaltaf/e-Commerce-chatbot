from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from ecommercebot.data_converter import data_converter

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)


def ingest_data(status):
    v_store = AstraDBVectorStore(
        embedding=embedding,
        collection_name="chatbotecomm",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )

    storage = status

    if storage is None:
        docs = data_converter()
        ids = v_store.add_documents(docs)
    else:
        return v_store

    return v_store, ids


if __name__ == '__main__':
    vstore, inserted_ids = ingest_data(None)
    print(f"\nInserted {len(inserted_ids)} documents.")
    results = vstore.similarity_search("can you tell me the low budget sound bass head.")
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")