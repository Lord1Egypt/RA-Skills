# Publish Checklist

## Pre-publish
- [x] SKILL.md exists
- [x] README.md tightened for publish
- [x] SCHEMA.md exists
- [x] IMPLEMENTATION.md exists
- [x] package.json exists
- [x] example happy path exists
- [x] runtime supports mock mode
- [x] runtime supports live mode hooks
- [x] polling support exists
- [x] live-mode error handling exists

## Recommended final preflight
- [ ] Review title / slug one last time
- [ ] Confirm whether to publish as 0.1.0 or 0.1.1
- [ ] Decide whether to soft-launch or broadly promote
- [ ] Optionally test with a real RYNJER_ACCESS_TOKEN
- [ ] Confirm ClawHub account auth (`clawhub login`)
- [ ] Run `clawhub whoami`

## Suggested publish command
```bash
cd /root/.openclaw/workspace
clawhub publish ./skills/rynjer-image-generation \
  --slug rynjer-image-generation \
  --name "Rynjer Image Generation for Agents" \
  --version 0.1.0 \
  --changelog "Initial release: agent-first image generation skill with prompt rewrite, cost estimate, live-mode hooks, and polling support"
```

## Suggested rollout
- Start with soft launch
- Watch install → invoke → generate → paid usage
- Tighten onboarding copy if installs are high but invokes are low
- Tighten monetization boundary if invokes are high but paid usage is weak
