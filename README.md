# AI-Powered Business Workflow Automation

A portfolio-ready starter project demonstrating how a business can receive customer requests, validate data, classify the request using an optional LLM, save it to a database, and expose the result to an automation platform such as n8n.

**Stack:** Python, FastAPI, Pydantic, REST API, JSON, SQLite, optional OpenAI-compatible LLM API, n8n, Docker, pytest.

## Features
- REST endpoint for incoming customer/business requests.
- Input validation, including email validation.
- Optional LLM classification with a local rule-based fallback.
- Categories: sales, support, billing, partnership, general.
- Priority detection and `needs_review` status for high-priority cases.
- Generated reply draft for a human to review.
- SQLite persistence and request listing.
- Importable n8n webhook workflow.
- Automated tests, Dockerfile, and Docker Compose configuration.
- No API key required for the default demo.

## Architecture
See [`docs/architecture.md`](docs/architecture.md).

## Run locally

### 1. Create environment
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start API
```bash
uvicorn app.main:app --reload
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### 4. Send a sample request
```bash
curl -X POST http://127.0.0.1:8000/process \
  -H "Content-Type: application/json" \
  --data @examples/sample_request.json
```

Expected response fields include `request_id`, `status`, `category`, `priority`, `summary`, `reply_draft`, `ai_mode`, and `created_at`. Exact classification depends on the message and whether an LLM is configured.

### 5. List saved requests
```bash
curl "http://127.0.0.1:8000/requests?limit=20"
```

## Enable LLM classification (optional)
Copy `.env.example` to `.env`, then add your provider's API key:
```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```
The API uses an OpenAI-compatible Chat Completions endpoint. Never commit `.env` or share API keys. If no key is configured or the provider call fails, the app falls back to rules-based classification.

## Import the n8n workflow
1. Start the API on port 8000.
2. In n8n, choose **Workflows → Import from File** and select [`n8n/workflow.json`](n8n/workflow.json).
3. Verify the HTTP Request node URL. For n8n running in Docker Desktop, `http://host.docker.internal:8000/process` may work. For other setups, use a reachable host/IP or service name.
4. Test the webhook node using its test URL. Send a POST request with `name`, `email`, `subject`, and `message`.
5. Review the API response. The included workflow does not automatically send email or write to Google Sheets; those can be added as follow-up nodes with your own credentials.

Example payload:
```json
{
  "name": "Avery Customer",
  "email": "avery@example.com",
  "subject": "Urgent issue with my order",
  "message": "I cannot access the order status page. Could someone help me as soon as possible?",
  "source": "website_form"
}
```

## Run tests
```bash
pytest -q
```

## Run with Docker
```bash
cp .env.example .env
docker compose up --build
```
On Windows, copy `.env.example` to `.env` using File Explorer or PowerShell.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service overview |
| GET | `/health` | Health check |
| POST | `/process` | Validate, classify, and store a request |
| GET | `/requests?limit=20` | List recent requests (demo endpoint) |

## Security and production limitations
This is a learning/portfolio project, not a production-ready customer support platform. Before deployment:
- Add API authentication and authorization.
- Protect `/requests` and any sensitive customer information.
- Add rate limiting, structured logging, monitoring, and alerting.
- Set data retention and deletion rules.
- Store secrets in a managed secret store.
- Review LLM privacy and data-processing terms before sending customer data to a provider.
- Add human approval before sending AI-generated replies.
- Configure CORS and TLS if accessed by a browser or public client.
- Add retries, idempotency, and dead-letter handling for reliable automation.

## Project status
Starter implementation with optional LLM support and a fallback classifier. Test locally before describing it as a completed deployment.
