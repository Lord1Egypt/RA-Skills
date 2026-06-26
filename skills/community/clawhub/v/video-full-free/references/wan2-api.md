# Wan2.6 API Reference

## النماذج المتاحة

| النموذج | الجودة | السرعة | الاستخدام |
|---------|-------|--------|-----------|
| `Wan-AI/Wan2.6-T2V-14B` | ⭐⭐⭐⭐⭐ | بطيء | الإنتاج |
| `Wan-AI/Wan2.6-T2V-1.3B` | ⭐⭐⭐ | سريع | الاختبار |
| `Wan-AI/Wan2.1-T2V-14B` | ⭐⭐⭐⭐ | متوسط | بديل مستقر |

## HuggingFace Inference API

```python
import requests

HF_API_URL = "https://api-inference.huggingface.co/models/Wan-AI/Wan2.6-T2V-14B"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "inputs": "your prompt here",
    "parameters": {
        "num_frames": 81,       # 8fps × ~10s
        "fps": 8,
        "width": 480,
        "height": 832,          # 9:16
        "num_inference_steps": 30,
        "guidance_scale": 5.0,
        "seed": -1              # عشوائي
    }
}

response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=300)
# response.content = bytes (MP4 file)
```

## HuggingFace Serverless (Gradio)

```python
from gradio_client import Client

client = Client("Wan-AI/Wan2.6-T2V-14B", hf_token=HF_TOKEN)
result = client.predict(
    prompt="cinematic scene...",
    negative_prompt="text, watermark, blurry",
    num_frames=81,
    fps=8,
    api_name="/generate"
)
# result = path to local MP4 file
```

## إعدادات الجودة

### للفيديوهات القصيرة (10 ثوانٍ):
```python
params = {
    "num_frames": 81,           # 81 frame / 8fps = ~10.1 ثانية
    "fps": 8,
    "width": 480,
    "height": 832,
    "num_inference_steps": 30,
    "guidance_scale": 5.0
}
```

### للجودة الأعلى (أبطأ):
```python
params = {
    "num_frames": 81,
    "fps": 8,
    "width": 720,
    "height": 1280,
    "num_inference_steps": 50,
    "guidance_scale": 7.0
}
```

## نصائح الـ Prompts

### تنسيق المثالي:
```
[الوصف الرئيسي], [الأسلوب], [الكاميرا], [الإضاءة], [التنسيق]
```

### أمثلة ناجحة:
```
# طبيعة
"Aerial view of desert dunes at golden hour, smooth drone motion, warm orange light, 9:16 vertical, cinematic"

# تقنية
"Close-up of circuit board with glowing blue light pulses, slow zoom in, dark background, high-tech atmosphere"

# تعليمي
"Animated diagram showing atom structure with orbiting electrons, clean white background, educational style"
```

### كلمات تحسّن الجودة:
- `cinematic quality`
- `smooth camera motion`
- `professional lighting`
- `ultra-realistic`
- `9:16 vertical format`

### كلمات يجب تجنّبها:
- `text`, `watermark`, `logo`
- `face close-up` (تشويه عالٍ)
- `multiple people` (صعب الإدارة)
