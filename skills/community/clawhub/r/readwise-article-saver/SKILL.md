---
name: readwise_article_saver
description: >
  Save article links to Readwise Reader with automatic content-based tagging.
  Specialized handling for WeChat Official Account (微信公众号) articles.
  Use this skill whenever the user sends a URL, shares an article link, says
  "save this", "save to Readwise", "存一下", "保存到 Readwise", "帮我收藏",
  or pastes any http/https link — especially mp.weixin.qq.com links.
  Also use when the user asks to batch-save multiple links.
  Do NOT use for general web browsing, search, or non-article URLs.
metadata:
  openclaw:
    requires:
      bins: ["python3", "curl"]
      config: ["READWISE_TOKEN", "OPENROUTER_API_KEY"]
---

# Readwise Article Saver

Save articles to Readwise Reader with LLM-powered tagging from a controlled
taxonomy. WeChat articles are fetched server-side to avoid Readwise's parsing
failures.

## Workflow

When the user sends a message containing one or more URLs, execute these steps
**immediately without asking for confirmation**.

### Step 1 — Fetch and save the article

Use `exec` to run the bundled Python script. The script handles:
- WeChat detection and server-side fetching with MicroMessenger UA
- HTML content validation (empty-page detection)
- Title and author extraction
- Calling the Readwise Save API

```bash
python3 ~/.openclaw/workspace/skills/readwise_article_saver/save_article.py "THE_URL"
```

The script outputs JSON to stdout:

```json
{
  "status": "ok",
  "title": "Article Title",
  "author": "Author Name",
  "domain": "mp.weixin.qq.com",
  "text_preview": "First 8000 characters of article body text...",
  "is_wechat": true,
  "fetch_method": "server_fetch",
  "readwise_status": 201
}
```

Or on failure:

```json
{
  "status": "error",
  "error": "Description of what went wrong",
  "fallback_saved": true
}
```

If `status` is `"error"` and `fallback_saved` is `false`, inform the user
that manual saving is needed (open in WeChat → share to Readwise).

### Step 2 — Generate tags with llm-task

If Step 1 returned `status: "ok"` and includes a `text_preview`, use the
`llm-task` tool to classify the article. Pass the full taxonomy as the prompt
and the article metadata as input.

Call `llm-task` with:

```json
{
  "prompt": "You are a document classifier. Read the document and return 2-5 tags as a JSON array of strings. PREFER tags from the taxonomy. If the content's central subject is not covered, create a new specific tag (1-3 words, same specificity as existing tags). Never create broad tags like 'Technology' or 'Finance'. Never assign 'favorite' or 'shortlist'.\n\nTAXONOMY:\n- AI agent: AI agents, autonomous systems, agentic workflows, tool-use architectures\n- Chips: semiconductors, chip design, GPU/TPU, NVIDIA/AMD/TSMC, export controls\n- AI 上下文: context windows, RAG, prompt engineering, foundation models, broader AI landscape\n- VC: venture capital, fund mechanics, early-stage investments, seed/pre-A/series-A\n- PE: private equity, series-B/C/D, buyouts, LBO mechanics\n- Fundraising: LP/GP dynamics, new LP allocation trends\n- Private Credit: direct lending, BDCs, unitranche, mezzanine, private debt\n- Equity: public equities, stock analysis, earnings, equity research, trading ideas\n- M&A: mergers, acquisitions, deal-making, corporate restructuring\n- Market: broad market conditions, macro outlook, cross-asset dynamics\n- Family Office: family office structures, ultra-HNW wealth management\n- Launching Fund: starting a fund, emerging manager playbooks, GP fundraising\n- Politics: domestic politics, elections, government policy (single country; NOT cross-border)\n- IR: international relations, foreign policy, diplomacy, geopolitics, great-power competition\n- Economics: macroeconomics, monetary/fiscal policy, trade economics\n- infra: infrastructure investment, physical/digital infrastructure\n- Consumer: consumer markets, retail, CPG, consumption-driven analysis\n- Startup Growth: startup scaling, growth strategies, go-to-market, PMF\n- Founder: founder-centric advice, founder stories, lessons from building\n- China, US, Europe, Middle East: apply when region is primary focus\n- Ray Dalio, Paul Graham, Howard Marks, 黄铮, Trump: apply ONLY if person is central subject (>50% content)\n- YC, XVC, Space X, Anthropic, Cursor: apply ONLY if company is primary subject\n- Career: career strategy, job transitions, professional development\n- Personal Development: mindset, self-improvement, habits, mental models\n- Mindset: psychological frameworks, resilience, cognitive biases\n- Guide: practical how-to, tutorials, step-by-step guides\n\nRULES:\n1. Always separate Politics from IR.\n2. For finance, choose the most specific tag. Never use generic 'Finance'.\n3. Key Thinker/Company tags only if central subject, not passing mention.\n4. Geographic tags only when region is primary focus.\n5. Return a JSON array of 2-5 strings. Nothing else.",
  "input": {
    "title": "<title from Step 1>",
    "author": "<author from Step 1>",
    "domain": "<domain from Step 1>",
    "text": "<text_preview from Step 1>"
  },
  "schema": {
    "type": "array",
    "items": { "type": "string" },
    "minItems": 1,
    "maxItems": 5
  }
}
```

The `llm-task` tool returns a JSON array of tag strings, e.g. `["AI agent", "China", "Guide"]`.

### Step 3 — Apply tags to the saved article

Use `exec` to call the Readwise API to update the article's tags:

```bash
python3 ~/.openclaw/workspace/skills/readwise_article_saver/update_tags.py "THE_URL" "tag1" "tag2" "tag3"
```

### Step 4 — Report to user

Combine the results and report concisely:

- ✅ **Success**: `✅ 「Article Title」已保存到 Readwise Reader。标签: tag1, tag2, tag3`
- ⚠️ **Partial**: `⚠️ 文章已保存但标签生成失败。标签: openclaw`
- ❌ **Failure**: `❌ 无法保存此文章。建议在微信中打开后手动保存。`

Do NOT add unnecessary commentary. Report the result and move on.

## Handling multiple URLs

If the user sends multiple URLs in one message, process each URL through
Steps 1-3 sequentially, then present a summary table of all results.

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `READWISE_TOKEN not set` | Env var missing | Set in `openclaw.json` under `skills.entries` |
| `Readwise API 401` | Token expired | Regenerate at readwise.io/access_token |
| `Server fetch failed` (WeChat) | Link expired or anti-bot | User should save manually from WeChat |
| `llm-task` returns error | LLM provider issue | Article is still saved; tags fallback to "openclaw" |
