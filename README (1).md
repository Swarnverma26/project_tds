# 🎓 TDS Virtual Teaching Assistant

A fully automated AI-powered Virtual Teaching Assistant for the IIT Madras Data Science course. This system scrapes discourse forum data, creates embeddings for semantic search, and provides intelligent Q&A capabilities with optional image OCR support.

## ✨ Features

- **🔍 Discourse Scraping**: Automated scraping of IIT Madras discourse forum with authentication
- **🧠 Semantic Search**: OpenAI-compatible embedding API integration with `text-embedding-3-small`
- **💬 Intelligent Q&A**: FastAPI-based question answering with source attribution
- **📸 Image OCR**: Support for image-based questions using Tesseract and GPT-4 Vision
- **🚀 Easy Deployment**: Ready for Vercel, Render, and Fly.io deployment
- **📊 Evaluation**: Automated promptfoo evaluation configuration

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Discourse     │───▶│   Data Processing │───▶│   Vector Store  │
│   Scraping      │    │   & Chunking     │    │   (JSON)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────┴───────┐
│   Frontend      │◀───│   FastAPI        │◀───│   Semantic      │
│   Interface     │    │   Server         │    │   Search        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                      ┌───────┴────────┐
                      │   OCR Service   │
                      │ (Tesseract +    │
                      │  GPT-4 Vision)  │
                      └────────────────┘
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd tds-virtual-ta

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your credentials:

```env
# Required: At least one embedding API key
AIPIPE_API_KEY=your_aipipe_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Required: Discourse authentication
DISCOURSE_SESSION_COOKIE=your_session_cookie_here
DISCOURSE_T_TOKEN=your_t_token_here

# Optional: Custom Tesseract path
TESSERACT_CMD=/usr/bin/tesseract
```

### 3. Run Complete Setup

```bash
# Automated setup (scrape + embed + run)
python scripts/setup.py setup --start-date 2025-01-01 --end-date 2025-04-14

# Or step by step:
python scripts/setup.py scrape --start-date 2025-01-01 --end-date 2025-04-14
python scripts/setup.py embed
```

### 4. Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` to access the interface!

## 📚 Usage

### Discourse Scraping

```bash
# Scrape IIT Madras TDS forum
python scripts/setup.py scrape \
  --start-date 2025-01-01 \
  --end-date 2025-04-14 \
  --category-id 34

# Scrape any Discourse forum
python scripts/discourse_scraper.py \
  --url https://discourse.example.com \
  --session-cookie "cookie_value" \
  --t-token "token_value" \
  --start-date 2025-01-01 \
  --end-date 2025-04-14 \
  --category-id 5
```

### API Usage

```python
import httpx

# Text question
response = httpx.post("http://localhost:8000/api/", 
    data={"question": "What is machine learning?"})

# Question with image
files = {"image": open("screenshot.png", "rb")}
response = httpx.post("http://localhost:8000/api/", 
    data={"question": "Explain this code"}, files=files)

print(response.json())
```

### API Response Format

```json
{
  "question": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "sources": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/topic/123",
      "title": "Introduction to Machine Learning",
      "preview": "Machine learning involves algorithms that learn...",
      "similarity_score": 0.95
    }
  ],
  "confidence": 0.87,
  "timestamp": "2025-06-05T11:13:00"
}
```

## 🔧 Configuration

Key configuration options in `app/utils/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `chunk_size` | 500 | Text chunk size for embeddings |
| `chunk_overlap` | 50 | Overlap between chunks |
| `top_k_results` | 5 | Number of results to return |
| `similarity_threshold` | 0.7 | Minimum similarity for results |
| `embedding_model` | text-embedding-3-small | OpenAI embedding model |

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Set environment variables in Vercel dashboard
```

### Render

1. Connect your GitHub repository
2. Use the provided `render.yaml` configuration
3. Set environment variables in Render dashboard

### Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly deploy
```

### Docker

```bash
# Build and run locally
docker build -t tds-virtual-ta .
docker run -p 8000:8000 --env-file .env tds-virtual-ta

# Or use Docker Compose
docker-compose up -d
```

## 🧪 Testing & Evaluation

### Run Tests

```bash
pytest tests/ -v
```

### Promptfoo Evaluation

The system includes automated evaluation using promptfoo:

```bash
# Install promptfoo
npm install -g promptfoo

# Run evaluation
promptfoo eval project-tds-virtual-ta-promptfoo.yaml

# View results
promptfoo view
```

## 📁 Project Structure

```
tds-virtual-ta/
├── app/
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   ├── utils/           # Utilities and config
│   └── routers/         # API routes (future)
├── scripts/             # Setup and utility scripts
├── frontend/            # Web interface
├── data/               # Data storage
├── tests/              # Test files
├── main.py             # FastAPI application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── vercel.json        # Vercel deployment config
└── README.md          # This file
```

## 🔑 Environment Variables

### Required

- `AIPIPE_API_KEY` or `OPENAI_API_KEY`: For embeddings API
- `DISCOURSE_SESSION_COOKIE`: Session cookie for discourse authentication
- `DISCOURSE_T_TOKEN`: CSRF token for discourse authentication

### Optional

- `TESSERACT_CMD`: Custom path to Tesseract executable
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (default: false)
- `LOG_LEVEL`: Logging level (default: INFO)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Format code: `black .`
6. Commit changes: `git commit -am 'Add feature'`
7. Push to branch: `git push origin feature-name`
8. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**1. Tesseract not found**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**2. Discourse authentication fails**
- Ensure session cookie and t-token are current
- Check that you have access to the category
- Verify the discourse URL is correct

**3. Embedding API errors**
- Verify API key is valid
- Check API endpoint URL
- Ensure you have sufficient credits/quota

**4. Memory issues during embedding creation**
- Reduce `chunk_size` in configuration
- Process in smaller batches
- Use a machine with more RAM

### Getting Help

- 📖 [API Documentation](http://localhost:8000/docs) (when server is running)
- 🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

## 🙏 Acknowledgments

- IIT Madras for the excellent Data Science program
- OpenAI for the embedding models
- The FastAPI and Python community
- Contributors and testers

---

**Ready to deploy?** Submit your project to: https://exam.sanand.workers.dev/tds-project-virtual-ta
