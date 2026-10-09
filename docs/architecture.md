# Architecture

```text
Website / Form / n8n webhook
          |
          v
POST /process (FastAPI + Pydantic validation)
          |
          v
Optional LLM classification ---- no key / API failure ----> Rule-based fallback
          |                                                   |
          +-------------------------+-------------------------+
                                    v
                            SQLite persistence
                                    |
                                    v
                JSON result: category, priority, summary,
                      reply draft, request ID, status
```

## Components
- **FastAPI** exposes `/health`, `/process`, and `/requests`.
- **Pydantic** validates incoming fields and email addresses.
- **LLM adapter** uses an OpenAI-compatible chat-completions endpoint when configured.
- **Rule fallback** keeps the demo usable without paid API credentials.
- **SQLite** persists requests for local demonstration.
- **n8n workflow** receives a webhook, sends the payload to the API, and returns the API response.

## Important notes
- The included workflow is a starter template; adjust the HTTP URL for your n8n deployment.
- `host.docker.internal` works in many Docker Desktop setups. For Linux or hosted n8n, use the API's reachable hostname.
- This demo drafts replies but does not send email automatically.
- Add authentication, rate limiting, retention policies, and secrets management before exposing the API publicly.
