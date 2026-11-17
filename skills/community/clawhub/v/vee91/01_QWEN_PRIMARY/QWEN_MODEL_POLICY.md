# Qwen Primary Model Policy

## Routing defaults
1. General reasoning / planning / agent orchestration: qwen3.8-max.
2. Coding / repository engineering: strongest verified Qwen Coder model available; prefer qwen3-coder-next or newer successor when benchmarked.
3. Native multimodal agent tasks: strongest verified Qwen Omni model available; prefer qwen3.8-omni-flash or newer successor.
4. Image generation/editing: strongest verified Qwen Image model available; prefer Qwen-Image-2.1 or newer successor.
5. Small/local tasks: route to an appropriate smaller Qwen/open-weight model when benchmark quality is sufficient.

## Latest-model rule
Never assume a hard-coded model name is permanently latest. At startup and on a scheduled refresh, query the configured model registry, collect capability metadata, run a representative benchmark suite, and update the preferred alias only after regression and safety gates pass.

## Failure policy
If Qwen primary is unavailable, use a configured local/open-weight fallback or another authorized provider. Do not bypass authentication, quotas, billing, licensing, or access controls.
