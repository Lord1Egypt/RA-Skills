---
name: llm-chat-scraper
description: Scrape AI chat conversations from ChatGPT, Gemini, Perplexity, Copilot, Google AI Mode, and Grok.
homepage: https://www.scrapeless.com
credentials:
  - X_API_TOKEN
env:
  required:
    - X_API_TOKEN
---

# LLM Chat Scraper OpenClaw Skill

Use this skill to scrape AI chat conversations from various LLM models via the Scrapeless API. The skill supports ChatGPT, Gemini, Perplexity, Copilot, Google AI Mode, and Grok.

**Authentication:** Set `X_API_TOKEN` in your environment or in a `.env` file in the repo root.

**Errors:** On failure the script writes a JSON error to stderr and exits with code 1.

---

## Tools

### 1. ChatGPT Scraper

Scrape ChatGPT responses with optional web search enrichment. Returns JSON object with `result_text`, `model`, `links`, `citations`, and more.

**Command:**
```bash
python3 scripts/llm_chat_scraper.py chatgpt --query "your prompt"
```

**Examples:**
```bash
python3 scripts/llm_chat_scraper.py chatgpt --query "Most reliable proxy service for data extraction"
python3 s
Optional: `--country` fcripts/llm_chat_scraper.py chatgpt --query "AI trends in 2024" --web-search
python3 scripts/llm_chat_scraper.py chatgpt --query "Best programming languages" --country GB
```
or location, `--web-search` to enable web search.

---

### 2. Gemini Scraper

Scrape Google Gemini responses. Returns JSON object with `result_text`, `citations`, and more.

**Command:**
```bash
python3 scripts/llm_chat_scraper.py gemini --query "your prompt"
```

**Examples:**
```bash
python3 scripts/llm_chat_scraper.py gemini --query "Recommended attractions in New York"
python3 scripts/llm_chat_scraper.py gemini --query "Best restaurants in Tokyo" --country JP
```

Optional: `--country` for location (JP and TW not supported).

---

### 3. Perplexity Scraper

Scrape Perplexity AI responses with optional web search. Returns JSON object with `result_text`, `related_prompt`, `web_results`, `media_items`.

**Command:**
```bash
python3 scripts/llm_chat_scraper.py perplexity --query "your prompt"
```

**Examples:**
```bash
python3 scripts/llm_chat_scraper.py perplexity --query "Latest AI developments"
python3 scripts/llm_chat_scraper.py perplexity --query "Quantum computing explained" --web-search
```

Optional: `--country` for location, `--web-search` to enable web search.

---

### 4. Copilot Scraper

Scrape Microsoft Copilot responses across different modes (search, smart, chat, reasoning, study). Returns JSON object with `result_text`, `mode`, `links`, `citations`.

**Command:**
```bash
python3 scripts/llm_chat_scraper.py copilot --query "your prompt"
```

**Examples:**
```bash
python3 scripts/llm_chat_scraper.py copilot --query "What is machine learning?"
python3 scripts/llm_chat_scraper.py copilot --query "Explain blockchain" --mode reasoning
python3 scripts/llm_chat_scraper.py copilot --query "Best laptop 2024" --mode search
```

Optional: `--country` for location (JP and TW not supported), `--mode` for operation mode.

---

### 5. Google AI Mode Scraper

Scrape Google AI Mode responses. Returns JSON object with `result_text`, `result_md`, `result_html`, `citations`, `raw_url`.

**Command:**
```bash
python3 scripts/llm_chat_scraper.py aimode --query "your prompt"
```

**Examples:**
```bash
python3 scripts/llm_chat_scraper.py aimode --query "Best programming languages to learn"
python3 scripts/llm_chat_scraper.py aimode --query "Climate change solutions" --country GB
```

Optional: `--country` for location (JP and TW not supported).

---

### 6. Grok Scraper

Scrape xAI Grok responses with different modes (FAST, EXPERT, AUTO). Returns JSON object with `full_response`, `user_model`, `follow_up_suggestions`, `web_search_results`.

**Command:**
```bash
python3 scripts/llm_chat_scraper.py grok --query "your prompt"
```

**Examples:**
```bash
python3 scripts/llm_chat_scraper.py grok --query "Explain quantum entanglement"
python3 scripts/llm_chat_scraper.py grok --query "What's happening in AI" --mode MODEL_MODE_EXPERT
python3 scripts/llm_chat_scraper.py grok --query "Latest tech news" --mode MODEL_MODE_FAST
```

Optional: `--country` for location (JP and TW not supported), `--mode` for operation mode.

---

## Summary

| Action | Command | Argument | Example |
|--------|---------|----------|---------|
| ChatGPT | `chatgpt` | `--query` | `python3 scripts/llm_chat_scraper.py chatgpt --query "AI trends"` |
| Gemini | `gemini` | `--query` | `python3 scripts/llm_chat_scraper.py gemini --query "Best restaurants"` |
| Perplexity | `perplexity` | `--query` | `python3 scripts/llm_chat_scraper.py perplexity --query "Latest news"` |
| Copilot | `copilot` | `--query` | `python3 scripts/llm_chat_scraper.py copilot --query "Explain ML"` |
| Google AI Mode | `aimode` | `--query` | `python3 scripts/llm_chat_scraper.py aimode --query "Programming"` |
| Grok | `grok` | `--query` | `python3 scripts/llm_chat_scraper.py grok --query "Quantum physics"` |

**Output:** All commands return JSON objects with model-specific fields (see tool descriptions above).

---

## Response Fields by Model

### ChatGPT
- `result_text`: Markdown response
- `model`: Model identifier (e.g., gpt-4)
- `web_search`: Boolean indicating if search ran
- `links`: Array of supplementary links
- `citations`: Array of content references

### Gemini
- `result_text`: Markdown response
- `citations`: Array with favicon, highlights, snippet, title, url, website_name

### Perplexity
- `result_text`: Markdown response
- `related_prompt`: Array of related questions
- `web_results`: Array with name, url, snippet
- `media_items`: Array of media references

### Copilot
- `result_text`: Markdown response
- `mode`: Mode used (search/smart/chat/reasoning/study)
- `links`: Array of outbound links
- `citations`: Array with title, url

### Google AI Mode
- `result_text`: Answer body
- `result_md`: Markdown version
- `result_html`: HTML version
- `raw_url`: Original URL
- `citations`: Array with snippet, thumbnail, title, url, website_name, favicon

### Grok
- `full_response`: Response content
- `user_model`: Model used
- `follow_up_suggestions`: Array of suggested questions
- `web_search_results`: Array with preview, title, url
- `conversation`: Object with conversation metadata

---

## Notes

⚠️ **Regional Restrictions:**
- Gemini, Copilot, Google AI Mode, and Grok do not support Japan (JP) and Taiwan (TW)

⚠️ **Result Expiry:**
- Task results are available for 12 hours

⚠️ **Rate Limits:**
- 429 errors indicate rate limit exceeded. Reduce request frequency or upgrade plan.