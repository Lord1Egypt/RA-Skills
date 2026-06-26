# AI Task Router

Automatically routes prompts to the cheapest model that can handle them.

## How It Works

Pattern matching classifies tasks into tiers:

| Task Type | Example | Routed To | Cost |
|-----------|---------|-----------|------|
| Simple | "hi", "thanks", "what time is it" | Local (Ollama) | $0 |
| Moderate | "write an email", "analyze this" | Mid-tier (Sonnet) | $ |
| Complex | "debug this codebase", "write a chapter" | Premium (Opus) | $$$ |

## Usage

```javascript
const { TaskRouter } = require('./src/task-router');

const router = new TaskRouter({
  defaultModel: 'local',
  escalationModel: 'sonnet',
  heavyModel: 'opus'
});

const result = router.route('analyze the sales data from Q3');
// { model: 'sonnet', reason: 'Analysis task', confidence: 0.8 }
```

## Custom Rules

Add your own routing patterns:

```javascript
router.addRule({
  name: 'code-review',
  pattern: /\b(review|refactor|debug|optimize)\b.*\b(code|function|class)\b/i,
  model: 'opus',
  reason: 'Code review needs deep reasoning'
});
```

## Cost Savings

Typical usage pattern routes ~70% of tasks to free local models, ~25% to mid-tier, and ~5% to premium. With Opus at $15/M tokens vs Ollama at $0, this saves 60-80% on API costs.
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
