# Image tools

Read this reference for image upscaling or background removal. Routing and polling rules remain in `SKILL.md`.

```bash
python3 scripts/showmeai.py pic upscale --image portrait.png --type face --scale-factor 2
python3 scripts/showmeai.py pic upscale --image product.png --type clean --scale-factor 4
python3 scripts/showmeai.py pic remove-bg --image person.jpg --type person --format png --crop
```

Upscale type is `clean` or `face`, with scale factor 1, 2, or 4. Background-removal type is `auto`, `person`, `object`, or `stamp`; output type and crop behavior are API-specific integer/boolean options. These are asynchronous by default, so the runtime journals, polls, and downloads results.
