---
name: swipenode
description: Give your agent the superpower to read the modern web without getting blocked by Cloudflare. Extracts clean JSON, saves 98% of LLM tokens, and executes zero malicious JS.
author: sirToby99
version: 1.6.3
repository: https://github.com/sirToby99/swipenode
---

# ⚡ SwipeNode: The Ultimate Web Extractor for Agents

Is your OpenClaw agent constantly hitting **403 Forbidden** errors when trying to read websites? Or are headless browser skills eating up your RAM and exposing your machine to malicious JavaScript?

**SwipeNode fixes all of this.**

It is a lightning-fast, highly optimized Go binary that fetches websites and extracts structured data (`__NEXT_DATA__`, Nuxt, JSON-LD) *without* rendering the page.

### 🔒 Security & Transparency (For Reviewers & Users)
To address security validations:
* **Fully Open Source:** The source code is completely public and auditable at [github.com/sirToby99/swipenode](https://github.com/sirToby99/swipenode).
* **How the WAF Bypass works:** SwipeNode does NOT use exploits. It simply uses the open-source `bogdanfinn/tls-client` Go library to mimic the TLS handshake signature of a standard Chrome/Safari browser.
* **Safer than Browsers:** Because SwipeNode does not use a headless browser engine, it *cannot* execute malicious JavaScript payloads from target websites. It only parses static HTML/JSON, making it inherently safer for autonomous agents.
* **Provenance:** The `install.sh` script explicitly uses `go install` with a pinned version tag to pull the public code directly from GitHub safely.

### 🔥 Why your Agent needs this:
* 🥷 **Bypasses Cloudflare & WAFs:** Native TLS-fingerprint spoofing.
* 💰 **Saves 98% of LLM Tokens:** Prunes tracking pixels, base64 data, and boilerplate UI noise.
* 🛡️ **Zero-JS Execution:** Immune to browser-based prompt injections.

---

## 🤖 Instructions for the AI Agent

**When to use this skill:**
Whenever the user asks you to read a webpage, summarize an article, check the news, or extract data from a URL. You should generally prefer this tool over standard HTTP clients (`curl`, `wget`) because it handles structured data efficiently.

**Ethical & Operational Guidelines:**
* Ensure your usage respects the target website's Terms of Service and legal constraints.
* Do not use this tool to aggressively scrape, spam, or overwhelm target servers. 
* Act responsibly as a user-driven autonomous agent.

**How to use it:**
Execute the following command in the terminal:
`swipenode extract --url "<TARGET_URL>"`

*Pro Tip:* If a high-security site actively blocks the default request, spoof the TLS fingerprint by appending `--impersonate safari` or `--impersonate firefox`.

**Understanding the Output:**
The tool will output a JSON object to stdout. 
1. If you see keys like `"nextjs"`, `"json_ld"`, or `"nuxtjs_raw"`, parse this structured data to answer the user's request.
2. If it's a legacy site, look for the `"text"` key, which contains the clean, readable content.
3. If it contains `"error"`, report the network issue to the user.

---

### Legal & Credits
This product includes software developed by Bogdan Finn (bogdanfinn/tls-client).
