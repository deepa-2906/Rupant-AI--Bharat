# AWS Infrastructure Setup

## 1. Amazon S3 (Data Lake)
- Stored NCERT Science Laboratory Manuals (Classes 6-10) in PDF format.
- Serves as the "Source of Truth" for the RAG engine.

## 2. Knowledge Bases for Amazon Bedrock
- **Embedding Model:** Titan Text Embeddings v2.
- **Vector Store:** Managed OpenSearch Serverless.
- **Chunking Strategy:** Fixed-size chunking (512 tokens) with 20% overlap to maintain scientific context.

## 3. Foundation Model
- **Model:** Amazon Nova Pro.
- Chosen for its high reasoning capabilities and excellent support for Indian regional languages.
