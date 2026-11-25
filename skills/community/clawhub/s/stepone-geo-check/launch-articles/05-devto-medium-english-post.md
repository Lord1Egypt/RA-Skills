# I Built a Zero-Dependency GEO & AI Search Readiness Checker (28 Real Checks for ChatGPT, DeepSeek, Perplexity, Doubao & Bing)

> **Target Platforms**: Dev.to, Hashnode, Medium, Reddit (`r/SEO`, `r/webdev`, `r/LocalLLaMA`)  
> **Live Free Web Tool**: https://www.steponeai.com/geo-check  
> **GitHub Repository**: https://github.com/ustczz/stepone-geo-check  
> **ClawHub Skill**: https://clawhub.ai/ustczz/skills/stepone-geo-check  

---

A growing pattern I keep seeing across B2B websites in 2026:

A site ranks decently in traditional search engines, looks gorgeous in Chrome, and scores fine on classic SEO checklists—yet when buyers ask **ChatGPT, Perplexity, DeepSeek, Claude, Doubao, or Qwen** for vendor recommendations, the brand is completely invisible or hallucinated.

Why? Because **Generative Engine Optimization (GEO)** and AI search retrieval care about a different technical layer than classic SEO:

1. **AI Crawler Access (`robots.txt` & Headers)** — Many sites unintentionally block `OAI-SearchBot`, `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Bytespider`, or `DeepSeek`.
2. **Machine-Readable AI Manifests** — Missing `/llms.txt`, `/llms-full.txt`, or updated `/sitemap.xml`.
3. **No-JS SSR Content Density** — Client-side React/Vue SPAs frequently serve `<div id="root"></div>` with <100 visible characters to non-JS crawlers.
4. **Structured Entity & Comparison Grounding** — Missing `JSON-LD` (`Organization` + `sameAs`, `FAQPage`, `Product`) and rendering spec tables as screenshots instead of native HTML `<table>` markup.

Instead of burning LLM tokens for inconsistent "AI vibes" scores, I built **`stepone-geo-check`** — a **100% pure-code, zero-dependency Node.js audit engine** that runs **6 dimensions × 28 deterministic HTTP/HTML checks** in ~3 seconds and generates tailored fix snippets (`llms.txt`, `robots.txt`, and `JSON-LD`).

## What It Checks (6 Dimensions · 28 Checks)

| Dimension | Weight | Key Signals Audited |
| :--- | :---: | :--- |
| **1. AI Crawler Access** | 20 pts | `robots.txt` parsing across 10 major AI & search bots + `noindex/noai` directives |
| **2. AI Knowledge Manifests** | 20 pts | `/llms.txt`, `/llms-full.txt`, `/sitemap.xml` URL count, Markdown alternates |
| **3. SSR Readability & Speed** | 20 pts | Visible character count without JS, empty SPA shell detection, text-to-HTML ratio, TTFB, HTTPS |
| **4. Structured Schema & Tables** | 20 pts | `JSON-LD` blocks, `Organization + sameAs`, `FAQPage/Product`, native HTML `<table>`, OG & Canonical |
| **5. Semantic Citation Hierarchy** | 10 pts | Title, Meta Description, single `<h1>` + `<h2>/<h3>` outline, image `alt` coverage |
| **6. Authority & Trust Signals** | 10 pts | Legal entity grounding, FAQ blocks, contact/conversion anchors |

## Try It in 3 Seconds

### 1. Free Visual Web Tool (Radar Chart + 10-Bot Matrix)
👉 https://www.steponeai.com/geo-check

### 2. Run Locally via CLI (Node.js >= 18, Zero `npm install` Needed)
```bash
git clone https://github.com/ustczz/stepone-geo-check.git
cd stepone-geo-check
node bin/cli.js https://yourcompany.com --snippets
```

### 3. Install as an OpenClaw / Agent Skill (ClawHub)
```bash
npx clawhub install stepone-geo-check
```
Skill page: https://clawhub.ai/ustczz/skills/stepone-geo-check

### 4. Use as an MCP Server (Claude Desktop / Cursor)
```json
{
  "mcpServers": {
    "stepone-geo-check": {
      "command": "node",
      "args": ["/path/to/stepone-geo-check/mcp-server.js"]
    }
  }
}
```

## Security Note (SSRF-Safe by Design)
Because this engine powers our public web tool as well, every target URL and redirect hop resolves via `dns.lookup` and blocks loopback, RFC1918 private networks, link-local metadata IPs (`169.254.169.254`), and IPv6 ULA ranges before opening a socket.

Feedback, extra check ideas, and PRs are very welcome on GitHub: https://github.com/ustczz/stepone-geo-check
