from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def load_documents():
    return [
        Document(page_content="Our pricing plans include Basic and Pro."),
        Document(page_content="Basic Plan costs $29/month with 10 videos and 720p resolution."),
        Document(page_content="Pro Plan costs $79/month with unlimited videos, 4K resolution, and AI captions."),
        Document(page_content="We offer two plans: Basic and Pro."),
        Document(page_content="No refunds after 7 days."),
        Document(page_content="24/7 support is available only on Pro plan.")
    ]
    return docs

def create_vector_store():
    docs = load_documents()
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(docs, embeddings)

def retrieve_docs(query, vectorstore, debug=False):
    results = vectorstore.similarity_search(query, k=4)

    if debug:
        print("\n [DEBUG] Retrieved Docs: ")
        for doc in results:
            print("-", doc.page_content)

    return [doc.page_content for doc in results]

def generate_rag_response(query, vectorstore, model):
    context_docs = retrieve_docs(query,vectorstore)
    context = "\n".join(context_docs)
    docs = retrieve_docs(query, vectorstore, debug=False)

    prompt = f"""
    You are a helpful assisstant.

    use the context below to answer the question.

    if the answer is partially available, answer as best as possible,
    only say "I don't know" if the context is completely irrelevant.

    Context:
    {context}

    Question:
    {query}
    """
    response = model.generate_content(prompt)
    return response.text.strip()
