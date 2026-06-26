# Setup And Run

## Preferred Install Path

Use the manual repo setup by default:

```bash
git clone https://github.com/stockvaluation-io/stockvaluation_io.git
cd stockvaluation_io
cp .env.example .env
```

Then edit `.env`, fill the required values, and start the stack:

```bash
docker compose -f docker-compose.local.yml up -d --build
```

## Optional Installer Path

If the user explicitly wants the installer, recommend inspecting it first after cloning the repo:

```bash
git clone https://github.com/stockvaluation-io/stockvaluation_io.git
cd stockvaluation_io
sed -n '1,240p' install.sh
bash install.sh
```

Do not recommend `curl | bash` as the default path.

## Manual Docker Flow

Prerequisites:

- Docker with Compose
- Required local env vars in `.env`: `CURRENCY_API_KEY`, `POSTGRES_PASSWORD`, `DEFAULT_PASSWORD`, `YFINANCE_SECRET_KEY`, `VALUATION_AGENT_SECRET_KEY`, `BULLBEARGPT_SECRET_KEY`, and `VALUATION_SERVICE_JWT_SECRET`
- At least one provider API key if the user wants research or narrative features

Then edit `.env` and fill required values. The main required secrets are usually:

- `CURRENCY_API_KEY`
- `POSTGRES_PASSWORD`
- `DEFAULT_PASSWORD`
- `YFINANCE_SECRET_KEY`
- `VALUATION_AGENT_SECRET_KEY`
- `BULLBEARGPT_SECRET_KEY`
- `VALUATION_SERVICE_JWT_SECRET`

Optional env vars for fuller workflows:

- One provider key that matches the chosen model backend: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY`, or `OPENROUTER_API_KEY`
- `TAVILY_API_KEY` for live research
- `DUMP_PROMPTS` and `PROMPT_DUMP_DIR` only when intentionally writing prompt dumps to disk for inspection

## Verify The Stack

Useful checks:

```bash
docker compose -f docker-compose.local.yml ps
curl http://localhost:5001/health
curl http://localhost:5002/health
```

If the frontend is running, open:

```text
http://localhost:4200
```

## Run A Valuation

Via UI:

- Open `http://localhost:4200`
- Enter a ticker such as `AAPL`, `MSFT`, `TSLA`, `SAP.DE`, or `7203.T`

Via API:

```bash
curl -X POST http://localhost:8081/api-s/valuate \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL"}'
```

## When The Repo Is Present

Inspect these first:

- `README.md` for the local architecture and main entrypoints
- `.env.example` for required environment variables
- `docker-compose.local.yml` for service names, ports, and dependencies
