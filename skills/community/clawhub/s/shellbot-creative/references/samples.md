# Samples

## Slash command samples

```text
/shellbot-creative plan product-marketing --brief "Create a 30s launch video for a new meal planner app"
/shellbot-creative asset nano-banana-2 --prompt "Colorful kitchen scene with app on phone" --aspect_ratio 9:16
/shellbot-creative edit freepik --model seedream-v4-5-edit --prompt "Replace background with modern home kitchen"
/shellbot-creative video freepik --model kling-v3-omni-pro --prompt "Slow cinematic pan over product"
/shellbot-creative voice freepik --text "Plan your meals in minutes, not hours"
/shellbot-creative pipeline explainer --duration 60 --aspect_ratio 16:9
```

## Local script samples

```bash
python3 scripts/creative_provider_router.py --goal image --priority quality --needs-consistency true
python3 scripts/creative_provider_router.py --goal video --priority speed
python3 scripts/creative_brief_to_storyboard.py --brief "Explain API monitoring alerts" --format explainer --duration 60
python3 scripts/run_full_dry_run.py --brief "Create a 45s product marketing video for a fintech app"
./scripts/package_skill.sh
./scripts/install_skill.sh --target "$HOME/.openclaw/skills"
```

## Remotion composition starter

Use the generated manifest plus the template component:

```bash
cp assets/remotion/ProductMarketingTemplate.tsx ./src/ProductMarketingTemplate.tsx
cp assets/remotion/Root.tsx ./src/Root.tsx
```
