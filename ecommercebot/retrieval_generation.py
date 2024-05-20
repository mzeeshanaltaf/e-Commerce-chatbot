from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from ecommercebot.ingest import ingest_data


def generation(v_store):
    retriever = v_store.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    You are an Ecommerce chat bot and expert in product recommendations and customer queries.
    You analyzes product titles and reviews to provide accurate and helpful responses.
    Ensure your answers are relevant to the product context and refrain from straying off-topic.
    Your responses should be concise and informative.

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:

    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    llm = ChatOpenAI()

    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return chain


if __name__ == '__main__':
    vstore = ingest_data("done")
    llm_chain = generation(vstore)
    print(llm_chain.invoke("can you tell me the best bluetooth buds?"))