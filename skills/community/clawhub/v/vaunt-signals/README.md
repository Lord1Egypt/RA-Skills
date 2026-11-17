Publishable copy of railway/src/agent/SKILL.md (the served route /agent/SKILL.md is the source of truth).
Sync before publishing: cp railway/src/agent/SKILL.md skills/vaunt-signals/SKILL.md
Publish: npx clawhub@latest login --no-browser   (device flow, approve in the browser once)
         npx clawhub@latest skill publish ./skills/vaunt-signals --slug vaunt-signals --categories trading --topics x402,hyperliquid,trading,signals
