# 🐐 GOAT AI Assistant

A powerful AI-powered assistant built with Llama 3.1 8B, featuring study plan generation, YouTube video analysis, PDF document Q&A, and general conversation capabilities. The application uses a FastAPI backend with LangChain chains and a beautiful Streamlit frontend.

## ✨ Features

- **📚 Study Plan Generator**: Create personalized study plans, learning roadmaps, and curated resource recommendations
- **🎥 YouTube Video Analysis**: Process YouTube videos with map-reduce summarization chains and RAG-powered Q&A
- **📄 PDF Document Q&A**: Upload PDF documents and ask intelligent questions using RAG retrieval
- **💬 General AI Chat**: Have natural conversations with conversation history memory
- **🔗 LangChain Integration**: Utilizes multiple specialized chains for different tasks (study plans, summarization)
- **🧠 Conversation Memory**: Maintains context across conversations with configurable history limits
- **🔍 RAG-Powered Responses**: Uses FAISS vector stores and semantic search for accurate, context-aware answers
- **⚡ GPU-Optimized**: Utilizes 4-bit quantization for efficient inference on GPU hardware

## 🏗️ Architecture

### Backend Stack
- **Framework**: FastAPI with asynchronous support
- **LLM**: Meta Llama 3.1 8B Instruct (4-bit quantized)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: FAISS for semantic similarity search
- **Orchestration**: LangChain with custom chains

### LangChain Chains Used

The application implements multiple specialized chains for different tasks:

#### 1. **Study Plan Generator Chains**
- **`study_plan_chain`**: Generates comprehensive study plans with weekly schedules, milestones, and daily routines
- **`roadmap_chain`**: Creates structured learning roadmaps divided into Foundation → Intermediate → Mastery phases
- **`resources_chain`**: Curates personalized learning resources (courses, books, practice platforms, communities)
- **Implementation**: `PromptTemplate | LLM | StrOutputParser` pattern
- **Token Limit**: 4096 tokens for detailed outputs

#### 2. **YouTube Summarization Chains** (Map-Reduce Pattern)
- **`youtube_summary_chain`**: Direct summarization for short videos (<10,000 words)
- **`youtube_chunk_chain`**: Processes individual video segments (Map phase)
- **`youtube_reduce_chain`**: Synthesizes segment summaries into final report (Reduce phase)
- **Usage**: Handles long videos by splitting into chunks and parallel processing
- **Implementation**: Conditional logic based on video length

#### 3. **RAG Chains for Q&A**
- **YouTube Q&A**: Retrieves relevant video segments using FAISS, then generates answers with context
- **PDF Q&A**: Retrieves relevant document chunks using FAISS, then generates answers with context
- **Implementation**: 
  ```python
  retriever.get_relevant_documents(query) 
  → context injection 
  → LLM response with retrieved context
  ```

### Conversation Memory

The application implements custom conversation history management:

- **`ConversationHistory` Class**: Custom implementation for maintaining context
- **Memory Limits**:
  - YouTube Q&A: 10 exchanges (20 messages)
  - PDF Q&A: 10 exchanges (20 messages)
  - General Chat: 15 exchanges (30 messages)
- **Context Window**: Last 3 exchanges (6 messages) included in prompts
- **Implementation**: Sliding window approach to prevent context overflow
- **Features**:
  - Automatic truncation of old messages
  - Formatted history injection into prompts
  - Per-feature isolation (separate memory for each feature)

### Frontend
- **Framework**: Streamlit with custom CSS
- **Design**: Modern, professional UI inspired by Claude/ChatGPT
- **Features**: Real-time updates, download buttons, responsive layout

## 📋 Prerequisites

- Python 3.10 or higher
- CUDA-capable GPU (recommended for optimal performance)
- HuggingFace account and API token
- ngrok account and auth token (for deployment)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/mazenmagdii/goat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend (Jupyter Notebook)

Open `goat.ipynb` in Jupyter Lab or Kaggle and run all cells. This will:
- Install all required packages
- Load the Llama 3.1 8B model with 4-bit quantization
- Log in to Hugging Face using your token
- Replace the NGROK_TOKEN with yours
- Start the FastAPI server
- Create an ngrok tunnel for public access

The notebook will display your public backend URL.

### 4. Run the Frontend

Update the `API_URL` in `app.py` with your ngrok URL from step 4, then:

```bash
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`


## 🔧 Configuration

### Backend Configuration

Key variables in `goat.ipynb`:

```python
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"  # LLM model
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Embedding model
PORT = 8000  # API server port
```

### Frontend Configuration

Update in `app.py`:

```python
API_URL = "your_ngrok_url_here"  # Backend URL
API_KEY = "secret1234"  # API authentication key
```

## 💡 Usage

### Study Plan Generator

1. Navigate to the "Study Plan" tab
2. Fill in the form:
   - **Subject**: What you want to learn (e.g., "Python Programming")
   - **Goal**: What you want to achieve (e.g., "Become a data scientist")
   - **Level**: Your current proficiency (Beginner/Intermediate/Advanced)
   - **Time Available**: Hours per week you can dedicate
   - **Timeline**: Desired learning duration (1 month, 3 months, 6 months, 1 year)
3. Choose what to generate:
   - **Study Plan**: Detailed weekly schedule with milestones and daily routines
   - **Roadmap**: Phase-based learning path (Foundation → Intermediate → Mastery)
   - **Resources**: Curated courses, books, practice platforms, and communities
   - **All Three**: Complete learning package
4. Click "Generate Plan" and wait for AI-powered recommendations
5. Download results as text files for offline reference

**Chains Used**: `study_plan_chain`, `roadmap_chain`, `resources_chain`

### YouTube Video Analysis

1. Navigate to the "YouTube" tab
2. Paste a YouTube URL
3. Click "Process Video" to extract and index the transcript
4. Click "Summarize Video" to get an AI-generated summary using map-reduce chains
5. Ask questions about the video content in the chat interface

**Chains Used**: `youtube_summary_chain` (short videos) or `youtube_chunk_chain` + `youtube_reduce_chain` (long videos)  
**RAG**: FAISS vector store for semantic search across video transcript  
**Memory**: 10 exchanges maintained for contextual follow-up questions

### PDF Document Q&A

1. Navigate to the "PDF Q&A" tab
2. Upload a PDF document
3. Click "Process PDF" to extract and index the content
4. Ask questions about the document in the chat interface
5. Receive accurate answers with relevant context from the document

**RAG**: FAISS vector store with RecursiveCharacterTextSplitter  
**Memory**: 10 exchanges maintained for contextual conversations  
**Chunk Size**: 1000 characters with 200 character overlap

### General Chat

1. Navigate to the "General Chat" tab
2. Start a conversation with the AI assistant
3. Ask questions about any topic
4. Enjoy contextual responses with conversation memory

**Memory**: 15 exchanges maintained for extended conversations  
**Context Window**: Last 3 exchanges included in each prompt

## 🛠️ Technical Details

### Model Quantization

The project uses 4-bit quantization via BitsAndBytes for efficient GPU memory usage:

```python
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)
```

**Benefits**:
- ~75% memory reduction (16GB → 4GB)
- Faster inference on consumer GPUs
- Minimal accuracy loss with NF4 quantization

### RAG Pipeline Implementation

#### Text Processing
- **Splitter**: `RecursiveCharacterTextSplitter`
  - Chunk size: 1000 characters
  - Overlap: 200 characters
  - Preserves context between chunks

#### Embedding & Retrieval
- **Model**: sentence-transformers/all-MiniLM-L6-v2
  - 384-dimensional embeddings
  - Fast inference (< 50ms per query)
- **Vector Store**: FAISS with L2 distance
  - Top-k retrieval (k=3 for Q&A)
  - Efficient similarity search

#### Context Injection
```python
# Retrieve relevant chunks
docs = vectordb.similarity_search(query, k=3)
context = "\n\n".join([doc.page_content for doc in docs])

# Inject into prompt
prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
```

### Chain Patterns

#### Simple Chain (Study Plans, Resources)
```python
chain = PromptTemplate | LLM | StrOutputParser()
result = chain.invoke({"subject": "...", "goal": "..."})
```

#### Map-Reduce Chain (Long YouTube Videos)
```python
# Map: Process chunks in parallel
chunk_summaries = [youtube_chunk_chain.invoke(chunk) for chunk in chunks]

# Reduce: Synthesize final summary
final = youtube_reduce_chain.invoke({"summaries": combined_summaries})
```

#### RAG Chain (Q&A)
```python
# Retrieve context
docs = vectordb.similarity_search(question)
context = format_docs(docs)

# Generate with context
answer = qa_chain.invoke({"context": context, "question": question})
```

### Memory Management

#### Conversation History Class
```python
class ConversationHistory:
    def __init__(self, max_history=10):
        self.max_history = max_history  # Max exchanges
        self.history = []  # List of {role, content} dicts
    
    def add_exchange(self, user_msg, assistant_msg):
        # Adds and auto-truncates
    
    def get_context_string(self):
        # Returns last 3 exchanges formatted for prompt
```

**Why Custom Memory?**
- Fine-grained control over context window
- Separate memory per feature (YouTube, PDF, Chat)
- Prevents token limit overflow
- Easy to clear/reset

### Generation Parameters

```python
pipeline(
    temperature=0.7,        # Balanced creativity
    top_p=0.9,             # Nucleus sampling
    repetition_penalty=1.1, # Reduce repetition
    max_new_tokens=1024,   # Standard responses
                           # 4096 for study plans
)
```

## 🔐 Security

- API key authentication for backend requests
- CORS middleware configuration for frontend-backend communication
- Secure token management for HuggingFace and ngrok

## ⚠️ Important Notes

1. **GPU Required**: This application requires a CUDA-capable GPU for optimal performance
2. **Model Download**: First run will download ~4.5GB of model weights
3. **Memory Usage**: Ensure at least 8GB of GPU memory is available
4. **ngrok Limits**: Free ngrok accounts have connection limits
5. **API Tokens**: Keep your HuggingFace and ngrok tokens secure

## 🐛 Troubleshooting

### Common Issues

**"CUDA out of memory"**
- Reduce batch size or switch to CPU mode (slower)
- Use a GPU with more memory

**"Model not found"**
- Verify your HuggingFace token has access to Llama models
- Accept the Llama license on HuggingFace

**"Connection refused"**
- Ensure backend is running and ngrok tunnel is active
- Update API_URL in frontend with correct ngrok URL

**"Slow inference"**
- This is normal on CPU; GPU is strongly recommended
- Consider using a smaller model if GPU is unavailable

## 📚 Dependencies

Major libraries used:

- **transformers**: HuggingFace transformers library
- **langchain**: LangChain framework for LLM applications
- **faiss-cpu**: Vector similarity search
- **streamlit**: Frontend web framework
- **fastapi**: Backend API framework
- **torch**: PyTorch deep learning framework
- **bitsandbytes**: Model quantization
- **youtube-transcript-api**: YouTube transcript fetching
- **pymupdf**: PDF processing

See `requirements.txt` for complete list.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- Meta AI for the Llama 3.1 model
- HuggingFace for model hosting and transformers library
- LangChain for the excellent framework
- Streamlit for the frontend framework

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Llama 3.1 8B • LangChain • Streamlit**
