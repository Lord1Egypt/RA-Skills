# Routing Policy (Draft)

Default model routing should be internal and based on:
- use_case
- quality_mode
- aspect_ratio
- count

## Default principle
- Do not force agents to pick raw models first.
- Prefer predictable outputs and low-friction execution.
- Allow optional advanced override only when necessary.

## quality_mode guidance
- fast: prioritize speed and lower cost
- balanced: default route for most agents
- high: prioritize output quality over speed/cost

## use_case guidance
- landing/ad: route toward stronger commercial visual quality
- product: route toward more stable product-like imagery
- blog/social: route toward faster and lower-friction defaults when appropriate
