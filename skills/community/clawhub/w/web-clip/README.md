# WebClip — Save & Summarize Web Pages

Fetch any web page, strip the junk, extract clean readable text, and optionally summarize it. Perfect for research tasks.

## Usage

```javascript
const { WebClip } = require('./src/web-clip');
const clip = new WebClip();

// Fetch and clean
const page = await clip.fetch('https://example.com/article');
console.log(page.title);
console.log(page.text);      // Clean text, no HTML
console.log(page.markdown);  // Formatted markdown

// Fetch and summarize
const summary = await clip.summarize('https://example.com/article', {
  maxLength: 200,
  model: 'llama3.1:8b'
});
```

## Features

- **HTML stripping** — removes scripts, styles, nav, ads, footers
- **Readability extraction** — finds main content automatically
- **Markdown conversion** — preserves headings, lists, links, code blocks
- **Batch fetching** — multiple URLs in parallel
- **Caching** — don't re-fetch pages you've already clipped
- **Offline archive** — save pages as local markdown files

## Output Formats

| Format | Use Case |
|--------|----------|
| `.text` | Raw clean text for agent context |
| `.markdown` | Formatted for reading or storage |
| `.summary` | Condensed version (requires model) |
| `.metadata` | Title, author, date, word count |

## Zero Dependencies

Uses only Node.js built-in `https` module. No Puppeteer, no headless browser.
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
