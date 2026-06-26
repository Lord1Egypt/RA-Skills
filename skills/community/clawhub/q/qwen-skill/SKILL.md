---
name: qwen-image
description: Generate and edit images with Qwen Image via DashScope API. This is a skill, not a callable tool. First use the read tool to open this SKILL.md, then run the script it specifies; never emit a tool call named qwen-image.
metadata: {"openclaw":{"emoji":"🖼️","requires":{"bins":["python3"],"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY"}}
---

# Qwen Image Skill

Use this skill for:
- text-to-image generation
- image-to-image editing (single image)
- multi-image fusion/editing (1 to 3 input images)
- never for file renaming by image understanding

## Runtime behavior (strict)

- `qwen-image` is a skill name, not a built-in tool name.
- Never emit a tool call named `qwen-image`.
- First use `read` on this `SKILL.md`, then execute the Python command below.
- Hard requirement: do not answer from imagination. You must execute the script first.
- Hard requirement: do not output markdown image syntax like `![](...)`.
- Hard requirement: do not output JSON object in final assistant reply.
- Hard requirement: do not describe image content unless the script actually ran successfully.
- Hard requirement: never output `MEDIA:` in tool-stage outputs; only output `MEDIA:` in the final assistant reply.
- Hard requirement: never transform `MEDIA:` lines into markdown image links.
- Hard requirement: do not use this skill for OCR, pure image understanding, or filename renaming tasks.
- If the user asks to rename files by image content, use `qwen-vision-rename` instead.
- Run the command directly; do not output pre-check/process narration.
- Do not read or print this `SKILL.md` or script source unless command fails.
- Do not output installation/config instructions unless the user explicitly asks for setup.
- Use script flag `--emit-media-ref`.
- On success:
  1) parse the last `MEDIA_REF:<path-or-url>` line from stdout (ignore preceding shell noise lines)
  2) final reply must be exactly one line: `MEDIA:<path-or-url>`
  3) if missing `MEDIA_REF:`, retry command once
- If command was not executed, do not send a final answer.
- On failure, output exactly 2 short Chinese sentences:
  1) failure reason
  2) actionable fix

## Setup

Install dependencies:

```bash
pip3 install -r {baseDir}/requirements.txt
```

Set API key:

```bash
export DASHSCOPE_API_KEY="your_api_key"
```

Optional region switch:

```bash
export DASHSCOPE_REGION="sg"  # sg or bj
```

Or use `.env` (auto-loaded from current directory, then `{baseDir}`):

```bash
cat > .env <<'EOF'
DASHSCOPE_API_KEY=your_api_key
DASHSCOPE_REGION=sg
OPENCLAW_MEDIA_OUTBOUND_DIR=~/.openclaw/media/outbound
OPENCLAW_MEDIA_BASE_URL=
EOF
```

Static URL mapping example (Nginx):

```nginx
location /gen/ {
  alias /home/huiya/.openclaw/media/outbound/;
  autoindex off;
}
```

## Commands

Text to image:

```bash
python3 {baseDir}/scripts/qwen_image.py text2img \
  --prompt "A futuristic tea shop in Shanghai at night, cinematic lighting" \
  --model qwen-image-2.0-pro \
  --size "1024*1024" \
  --n 1 \
  --emit-media-ref \
  --publish-dir ~/.openclaw/media/outbound \
  --out-dir {baseDir}/tmp/qwen-image
```

Image to image:

```bash
python3 {baseDir}/scripts/qwen_image.py img2img \
  --images ./input.png \
  --prompt "Keep composition, convert this to watercolor style" \
  --model qwen-image-2.0-pro \
  --n 1 \
  --emit-media-ref \
  --publish-dir ~/.openclaw/media/outbound \
  --out-dir {baseDir}/tmp/qwen-image
```

## Notes

- Recommended default: `qwen-image-2.0-pro` (quality first). `qwen-image-2.0` can be used for faster/cheaper runs.
- Input images can be local paths, public URLs, or `data:image/...;base64,...`.
- Returned image URLs are temporary. The script downloads images immediately to `--out-dir`.
- Published images are copied to `OPENCLAW_MEDIA_OUTBOUND_DIR` (default: `~/.openclaw/media/outbound`).
- The script also writes `.view.html` preview pages and uses those URLs in visible text to reduce markdown-image rewrites.
- `OPENCLAW_MEDIA_BASE_URL` is optional. Keep it empty for portable packaging; set it per deployment only when you need public links (e.g. `https://example.com/gen` or local `http://127.0.0.1:8090`).
- `--emit-media-ref` + final one-line `MEDIA:` reply is recommended for Feishu to avoid duplicate media sends.
- If you specifically need plain text URL in Control UI, use `--reply-format link`.
- Existing shell environment variables override `.env` values.
- If endpoint is not explicitly set, the script auto-retries once with the other region endpoint when receiving `InvalidApiKey`.
