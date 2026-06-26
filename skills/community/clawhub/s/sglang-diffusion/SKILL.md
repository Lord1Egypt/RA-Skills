---
name: sglang-diffusion
description: "Generate images using a local SGLang-Diffusion server (FLUX, Stable Diffusion, Qwen-Image, etc.). Use when: user asks to generate, create, draw, or render an image with a locally running SGLang-Diffusion instance. NOT for: cloud-hosted image APIs (use openai-image-gen or nano-banana-pro instead). Requires a running SGLang-Diffusion server."
homepage: https://github.com/sgl-project/sglang
metadata:
 {
   "openclaw":
     {
       "emoji": "🎨",
       "requires": { "bins": ["python3"] },
     },
 }
---


# SGLang-Diffusion Image Generation


Generate images via a local SGLang-Diffusion server's OpenAI-compatible API.


## Prerequisites


- SGLang-Diffusion server running (default: `http://127.0.0.1:30000`)
- If the server was started with `--api-key`, set `SGLANG_DIFFUSION_API_KEY` env var


## Generate an image


```bash
python3 {baseDir}/scripts/generate.py --prompt "a futuristic cityscape at sunset"
```


## Useful flags


```bash
python3 {baseDir}/scripts/generate.py --prompt "portrait of a cat" --size 512x512
python3 {baseDir}/scripts/generate.py --prompt "abstract art" --negative-prompt "blurry, low quality"
python3 {baseDir}/scripts/generate.py --prompt "landscape" --steps 30 --guidance-scale 7.5 --seed 42
python3 {baseDir}/scripts/generate.py --prompt "photo" --server http://192.168.1.100:30000 --out ./my-image.png
```


## API key (optional)


Only needed if the SGLang-Diffusion server was started with `--api-key`.
Set `SGLANG_DIFFUSION_API_KEY`, or pass `--api-key` directly:


```bash
python3 {baseDir}/scripts/generate.py --prompt "hello" --api-key sk-my-key
```


Or configure in `~/.openclaw/openclaw.json`:


```json5
{
 skills: {
   "sglang-diffusion": {
     env: { SGLANG_DIFFUSION_API_KEY: "sk-my-key" },
   },
 },
}
```


## Notes


- The script prints a `MEDIA:` line for OpenClaw to auto-attach on supported chat providers.
- Output defaults to timestamped PNG in `/tmp/`.
- Do not read the image back; report the saved path only.