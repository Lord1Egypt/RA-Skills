# generate-image

用户请求画图时触发。

只做一次执行：先写英文 prompt，再调用脚本。

```bash
bash /home/node/.openclaw/workspace/tools/quick-generate.sh "<positive>" "<negative>"
```

Prompt 规则：
- positive: masterpiece, best quality, ultra-detailed, 8k, [主体], [风格], [场景], [光影]
- negative: lowres, bad anatomy, bad hands, blurry, worst quality, watermark, signature, text, ugly, deformed

风格词：
- anime style, cel shading, vibrant colors, anime screencap
- photorealistic, RAW photo, film grain, shallow depth of field
- showa era aesthetic, retro atmosphere, 1980s japan, vintage photography, neon signs
- cyberpunk, neon lights, rain, holographic, futuristic city
- watercolor painting, soft edges, color bleeding, artistic

高清版：
```bash
bash /home/node/.openclaw/workspace/tools/quick-generate.sh "<positive>" "<negative>" sdxl_hires.json
```

脚本会返回文件路径与 seed；用 message 工具发给用户（附简短中文标题+seed）。

规则：
- 单轮执行，不要多轮追问
- 不要手写 Python
- 不要手动 curl ComfyUI
- 不要额外检查（脚本已内置）
- 遵守系统与平台安全边界
