# AI Workspace Self-Repair System

Automated self-healing for AI automation setups. Detects failures and fixes them without human intervention.

## What It Monitors & Fixes

| Problem | Detection | Auto-Fix |
|---------|-----------|----------|
| Ollama crashed | HTTP health check | Restart Ollama service |
| Config file corrupted | JSON parse test | Restore from defaults |
| Required files missing | Filesystem check | Restore from backup |
| Service unresponsive | Timeout detection | Kill and restart |

## Usage

```javascript
const { SelfRepair } = require('./src/self-repair');

const repair = new SelfRepair({
  workspacePath: process.cwd(),
  backupPaths: ['/path/to/backup'],
  requiredFiles: ['config.json', 'data/important.db'],
  requiredDirs: ['logs', 'data']
});

// Run full health check + auto-repair
const report = await repair.fullRepairCycle();
console.log('Status:', report.status);
console.log('Repairs made:', report.repairs);
```

## Hub Mode (Full Orchestration)

Combine with the task router and scheduled routines:

```javascript
const { AutomationHub } = require('./src/hub');

const hub = new AutomationHub({
  workspacePath: process.cwd(),
  defaultModel: 'llama3.1:8b',
  healthCheckInterval: 5 * 60 * 1000 // every 5 min
});

await hub.start(); // Boots all systems, runs initial health check
```

## Custom Health Checks

Add your own monitoring:

```javascript
repair.addCheck('my-database', async () => {
  return await db.ping(); // return true/false
});
```

## Logging

All repairs are logged to a JSON file with timestamps. Keeps last 200 entries with automatic rotation.
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
