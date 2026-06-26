
[<img width="1200" height="629" alt="img_v3_02vs_05ae6cc6-fae6-4a1e-956f-f2cdc12b043g" src="https://github.com/user-attachments/assets/47d09e83-911d-4c15-b339-8ac635b68936" />](https://docs.scrapeless.com/en/llm-chat-scraper/scrapers/chatgpt/)
</p>

<p align="center">
  <strong>Scrapeless OpenClaw skill for scraping ChatGPT, Gemini, Perplexity, and Grok responses.</strong><br/>
</p>

  <p align="center">
    <a href="https://www.youtube.com/@Scrapeless" target="_blank">
      <img src="https://img.shields.io/badge/Follow%20on%20YouTuBe-FF0033?style=for-the-badge&logo=youtube&logoColor=white" alt="Follow on YouTuBe" />
    </a>
    <a href="https://discord.com/invite/xBcTfGPjCQ" target="_blank">
      <img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Join our Discord" />
    </a>
    <a href="https://x.com/Scrapelessteam" target="_blank">
      <img src="https://img.shields.io/badge/Follow%20us%20on%20X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow us on X" />
    </a>
    <a href="https://www.reddit.com/r/Scrapeless" target="_blank">
      <img src="https://img.shields.io/badge/Join%20us%20on%20Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white" alt="Join us on Reddit" />
    </a> 
    <a href="https://app.scrapeless.com/passport/register?utm_source=official&utm_term=githubopen" target="_blank">
      <img src="https://img.shields.io/badge/Official%20Website-12A594?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Official Website"/>
    </a>
  </p>

---


# 🤖 Scrapeless LLM Scraper OpenClaw Skill

A skill for the Scrapeless platform that allows you to scrape AI chat conversations from various LLM models via the Scrapeless API. It supports ChatGPT, Gemini, Perplexity, Copilot, Google AI Mode, and Grok.

## 🚀 Overview

This OpenClaw skill integrates [Scrapeless LLM Scrapers](https://docs.scrapeless.com/en/llm-chat-scraper/quickstart/introduction/) into any OpenClaw-compatible AI agent or LLM pipeline. It collects structured AI chat responses from Gemini, Perplexity, Google AI Mode, ChatGPT, Grok and Copilot.

Built for **GEO / AI SEO, AI search monitoring, LLM benchmarking, brand & market intelligence, AI content platforms, and automation agents, this skill helps developers, AI labs, and enterprise teams gather high-quality structured LLM outputs** for research, analytics, or workflow automation.

⭐ If you find this project useful, please give it a star!

## Features
- **Major LLM support**: ChatGPT, Gemini, Perplexity, Copilot, Google AI Mode, and Grok.

- **High concurrency & reliability:** Supports hundreds of concurrent tasks with error rates <10%.

- **Adaptive scraping:** Automatically adjusts strategies to minimize blocking and maximize success.

- **Seamless workflow integration:** Works with OpenClaw, Cursor, Trae and other AI agent platforms.

- **Structured output:** JSON responses with model info, citations, links, and optional web search enrichment.

- **Trial-ready:** Works with Scrapeless API; X_API_TOKEN(get it from https://www.scrapeless.com/) required for authentication. 

- **Real-time scraping**

- **Support for web search enrichment**

- **Country-based proxy selection**

## Use Cases

This OpenClaw skill is designed for teams working on:

| Use Case | Description |
|------|-----|
| AI SEO/GEO (Generative Engine Optimization)  | Monitor how brands appear in AI-generated answers.  |
| AI Search Monitoring | Track responses from ChatGPT / Perplexity / Gemini.  |
| LLM Response Analysis | Analyze answer structure, citations and model behavior.  |
| Competitive Intelligence  | Compare how different LLM platforms respond to the same query.  |


## Installation

1. Clone the repository:

```bash
git clone https://github.com/scrapeless-ai/llm-chat-scraper-skill.git
```

2. Install dependencies for the LLM Chat Scraper:

```bash
cd llm-chat-scraper-skill
pip install -r requirements.txt
```

## Environment Configuration

1. Manual installation: Place the skill in OpenClaw’s `.openclaw/skills` directory.

2. Create a `.env` file in the root directory based on the `.env.example` file:

```bash
cp .env.example .env
```

3. Add your Scrapeless API token to the `.env` file:

```
X_API_TOKEN=your_api_token_here
```

You can obtain an API token from the [Scrapeless website](https://www.scrapeless.com).

## Supported Models

**ChatGPT**
- Returns markdown responses with model info, web search results, links, and citations
- Supports web search enrichment

**Gemini**
- Returns markdown responses with citations
- Note: Japan (JP) and Taiwan (TW) are not supported

**Perplexity**
- Returns markdown responses with related prompts, web results, and media items
- Supports web search enrichment

**Copilot**
- Returns markdown responses with mode information, links, and citations
- Supports different modes: search, smart, chat, reasoning, study
- Note: Japan (JP) and Taiwan (TW) are not supported

**Google AI Mode**
- Returns answer body in multiple formats with citations
- Note: Japan (JP) and Taiwan (TW) are not supported

**Grok**
- Returns full responses with model info, follow-up suggestions, and web search results
- Supports different modes: FAST, EXPERT, AUTO
- Note: Japan (JP) and Taiwan (TW) are not supported

## Usage Examples

```bash
# Scrape ChatGPT with web search
python3 scripts/llm_chat_scraper.py chatgpt --query "AI trends in 2024" --web-search

# Scrape Gemini with UK proxy
python3 scripts/llm_chat_scraper.py gemini --query "Best restaurants in London" --country GB

# Scrape Perplexity
python3 scripts/llm_chat_scraper.py perplexity --query "Latest tech news"

# Scrape Copilot in reasoning mode
python3 scripts/llm_chat_scraper.py copilot --query "Explain quantum computing" --mode reasoning

# Scrape Google AI Mode
python3 scripts/llm_chat_scraper.py aimode --query "Climate change solutions"

# Scrape Grok in expert mode
python3 scripts/llm_chat_scraper.py grok --query "What's happening in AI" --mode MODEL_MODE_EXPERT
```
⚙️ Optional Parameters

- `country`
- `web-search`
- `mode`

## Output Structure

| Model          | Key Fields                | Description            |
| -------------- | ------------------------- | ---------------------- |
| ChatGPT        | `result_text`, `model`, `web_search`, `links`, `citations` | Returns markdown responses with model info, web search results, links, and citations.   |
| Gemini         | `result_text`, `citations`    | Returns markdown responses with integrated citations.      |
| Perplexity     | `result_text`, `related_prompt`, `web_results`, `media_items`  | Enriched responses with related prompts, web results, and media items.       |
| Copilot        | `result_text`, `mode`, `links`, `citations`               | Supports search/chat/reasoning/study modes with links and citations.     |
| Google AI Mode | `result_text`, `result_md`, `result_html`, `citations`, `raw_url`    | Returns full structured answer body in multiple formats with citations. |
| Grok | `full_response`, `user_model`, `follow_up_suggestions`, `web_search_results`    | Full responses for Expert/FAST/AUTO modes with follow-up suggestions and search results. |

## Common Issues

**Rate Limits**
If you encounter 429 errors, you've exceeded the rate limit. Reduce request frequency or upgrade your Scrapeless plan.

**Regional Restrictions**
Some LLM models (Gemini, Copilot, Google AI Mode, Grok) do not support Japan (JP) and Taiwan (TW).

**Result Expiry**
Task results are available for 12 hours.

## Related resources

- [Scrapeless LLM Scraper](https://docs.scrapeless.com/en/llm-chat-scraper/quickstart/introduction/)
- [Scrapeless Universal Scraping API](https://docs.scrapeless.com/en/universal-scraping-api/)

## Contact Us
For questions, suggestions, or collaboration inquiries, feel free to contact us via:
- Email/Slack: market@scrapeless.com
- Official Website: https://www.scrapeless.com
- Community Forum: [Browser Labs Discord](https://discord.com/invite/xBcTfGPjCQ)
