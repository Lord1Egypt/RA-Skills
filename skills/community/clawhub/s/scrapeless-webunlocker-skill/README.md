
[<img width="1200" height="629" alt="20260318-100141" src="https://github.com/user-attachments/assets/3a0f7070-d6ad-4ebe-ab5e-07de5356a46a" />](https://www.scrapeless.com/en/product/universal-scraping-api)

</p>

<p align="center">
  <strong>OpenClaw skill of Scrapeless Web Unlocker for Web Scraping, Cloudflare Solving, and AI Data Collection.</strong><br/>
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

# 🤖 Scrapeless Openclaw WebUnlocker Skill

A skill for the Scrapeless platform that enables you to solve website blocks and scrape web content using the Scrapeless Universal Scraping API. It supports JavaScript rendering, CAPTCHA solving, IP rotation, and intelligent request retries.

## Overview

The **Web Unlocker Skill** allows developers and AI agents to **access and extract data from websites that normally block automated traffic**.
Built on top of the **Scrapeless Universal Scraping API**, this skill automatically handles common bot protections such as **Cloudflare, CAPTCHA challenges, IP blocking, and JavaScript rendering**, making it easy to retrieve clean web data from difficult targets.
Instead of managing proxy pools, headless browsers, and bypass logic yourself, Web Unlocker provides a **simple API interface to reliably fetch web pages at scale**.
This makes it ideal for **web scraping, data pipelines, AI training datasets, market intelligence, and automation workflows**.

## ❓ Why Use Web Unlocker

Modern websites deploy increasingly sophisticated bot detection systems such as:

- Cloudflare protection  
- CAPTCHA challenges  
- Browser fingerprint detection  
- IP reputation blocking  
- JavaScript-rendered content  

Traditional scraping tools or headless browsers often fail against these protections.

**Web Unlocker solves this by combining:**

- Stealth browser infrastructure  
- Proxy rotation  
- CAPTCHA solving  
- Intelligent retry mechanisms  

👉 Developers only need to send a request — the platform handles the rest.

---

## ✨ Key Features

**🤖 Automatic CAPTCHA Solving**
- Supports reCAPTCHA, Cloudflare Turnstile and Cloudflare challenge pages. 

**🌐 JavaScript Rendering**
- Execute full browser rendering for modern frameworks such as **React, Next.js, and Vue**.

**🌍 Global Proxy Infrastructure**
- Built-in proxy rotation and country selection for higher success rates and geo-targeted scraping.

**📦 Multiple Response Formats**
- Retrieve data in various formats:

  - HTML  
  - Plain text  
  - Markdown  
  - Screenshots (PNG / JPEG)  
  - Network requests  
  - Structured extracted content  

**🔁 Intelligent Retry System**
- Automatically retries failed requests using optimized routing.

---

## 🧩 Use Cases

**📊 Web Scraping & Data Extraction**
- Collect structured data from e-commerce, search engines, directories, and public websites.  

**🤖 AI Training Data Collection**
- Gather high-quality datasets for LLM training, AI evaluation, or synthetic data generation.  

**📈 Market Intelligence**
- Monitor competitors, pricing data, product catalogs, and industry signals. 

**🔍 SEO & AI Search Monitoring**
- Track how websites appear across search engines and AI-powered search platforms. 

**⚙️ Automation & AI Agents**
- Integrate web data directly into **AI agents, workflows, or automation platforms.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/scrapeless-ai/webunlocker-skill.git
```

2. Install dependencies for WebUnlocker:

```bash
cd webunlocker-skill
pip install -r requirements.txt
```

## ⚙️ Environment Configuration

1. **Manual installation**: Place the skill in OpenClaw’s `.openclaw/skills` directory.
  
2. Create a `.env` file in the root directory based on the `.env.example` file:

```bash
cp .env.example .env
```

3. Add your Scrapeless API token to the `.env` file:

```
X_API_TOKEN=your_api_token_here
```

You can obtain an API token from the [Scrapeless website](https://www.scrapeless.com).

## Usage Examples

```bash
# Scrape HTML content
python3 scripts/webunlocker.py --url "https://httpbin.io/get"

# Scrape as Markdown
python3 scripts/webunlocker.py --url "https://example.com" --response-type markdown

# Take a screenshot
python3 scripts/webunlocker.py --url "https://example.com" --response-type png

# Extract specific content types
python3 scripts/webunlocker.py --url "https://example.com" --response-type content --content-types emails,links,images

# Use a US proxy
python3 scripts/webunlocker.py --url "https://example.com" --country US

# Use POST method
python3 scripts/webunlocker.py --url "https://httpbin.org/post" --method POST --data '{"key": "value"}'

# Add custom headers
python3 scripts/webunlocker.py --url "https://example.com" --headers '{"User-Agent": "Mozilla/5.0"}'

# Use custom proxy
python3 scripts/webunlocker.py --url "https://example.com" --proxy-url "http://your-proxy-url:port"

# Enable JavaScript rendering
python3 scripts/webunlocker.py --url "https://example.com" --js-render

# Bypass Cloudflare Turnstile challenge
python3 scripts/webunlocker.py --url "https://2captcha.com/demo/cloudflare-turnstile-challenge" --js-render --headless --response-type markdown
```

## Output Structure
Web Unlocker supports multiple response formats depending on your needs.

| Response Type | Description |
|--------------|------------|
| HTML | Full rendered page HTML |
| Plaintext | Clean text without HTML tags |
| Markdown | Structured Markdown content |
| PNG / JPEG | Page screenshots |
| Network | All network requests during page load |
| Content | Extract specific data types such as emails, links, or images |

## Common Issues

### Rate Limits
If you encounter 429 errors, you've exceeded the rate limit. Reduce request frequency or upgrade your Scrapeless plan.

### Timeouts
- Page load timeout: 30 seconds
- Global execution timeout: 180 seconds

### CAPTCHA Solving
WebUnlocker automatically handles reCaptcha V2, Cloudflare Turnstile, and Cloudflare Challenge, but complex CAPTCHAs may occasionally fail.

### Billing
- Charges are applied on a per-request basis
- Only successful requests will be billed

## 🔗 Related resources

- [Scrapeless LLM Scraper](https://docs.scrapeless.com/en/llm-chat-scraper/quickstart/introduction/)
- [Scrapeless Universal Scraping API](https://docs.scrapeless.com/en/universal-scraping-api/)

## 📬 Contact Us
For questions, suggestions, or collaboration inquiries, feel free to contact us via:
- Email/Slack: market@scrapeless.com
- Official Website: https://www.scrapeless.com
- Community Forum: [Browser Labs Discord](https://discord.com/invite/xBcTfGPjCQ)
