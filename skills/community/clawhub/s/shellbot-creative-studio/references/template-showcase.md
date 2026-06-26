# Template Showcase

Use this quick guide to choose the strongest starting point.

## `aida-classic-16x9`

- Path: `assets/remotion-product-template`
- Best for: General product explainers with direct AIDA mapping.
- Strength: Clean baseline for rapid customization.

## `cinematic-product-16x9`

- Path: `assets/templates/cinematic-product-16x9`
- Best for: Launch films, high-emotion reveals, premium positioning.
- Strength: Dramatic framing, bold typography, strong tonal transitions.

## `saas-metrics-16x9`

- Path: `assets/templates/saas-metrics-16x9`
- Best for: B2B/SaaS ads where operational outcomes matter.
- Strength: Dashboard-style visuals and animated metric storytelling.

## `mobile-ugc-9x16`

- Path: `assets/templates/mobile-ugc-9x16`
- Best for: Reels/TikTok/Shorts style creatives.
- Strength: Vertical pacing, caption-forward layout, thumb-stop rhythm.

## `blank-16x9`

- Path: `assets/templates/blank-16x9`
- Best for: Custom projects that don't fit a predefined narrative structure.
- Strength: Minimal starter — just a Root.tsx with a single empty composition. The "create-react-app" of Remotion.

## `explainer-16x9`

- Path: `assets/templates/explainer-16x9`
- Best for: How-it-works videos, tutorials, educational content, feature walkthroughs.
- Strength: 5-scene structure (Context > Problem > Mechanism > Benefits > Next Step) with typed ExplainerPlan props and stage-based color theming.

## Bootstrap commands

```bash
bash scripts/remotion_init.sh --list
bash scripts/remotion_init.sh --template cinematic-product-16x9 --name ProductLaunch --output ./my-video
bash scripts/remotion_init.sh --template blank-16x9 --output ./scratch-video
bash scripts/remotion_init.sh --template explainer-16x9 --name HowItWorks --output ./explainer
```
