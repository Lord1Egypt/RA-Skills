# TokenLab Cost Routing Skill

This skill helps coding agents choose TokenLab models with cost, quality, latency, and fallback constraints.

Install:

```bash
npx skills add https://github.com/hedging8563/tokenlab-skills --skill tokenlab-cost-routing -y
```

Use it when you want an agent to:

- Compare strong, balanced, fast, and lower-cost TokenLab model options.
- Read public pricing before recommending a model.
- Build a fallback chain for production requests.
- Avoid hardcoded stale model lists.

Canonical discovery endpoints:

- `https://api.tokenlab.sh/v1/models`
- `https://api.tokenlab.sh/v1/models?recommended_for=<scene>`
- `https://api.tokenlab.sh/v1/models/{model}`
- `https://api.tokenlab.sh/v1/models/{model}/pricing`
