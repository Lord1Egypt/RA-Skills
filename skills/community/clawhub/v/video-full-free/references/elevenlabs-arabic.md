# ElevenLabs — إعدادات الصوت العربي

## النماذج المدعومة للعربية

| النموذج | العربية | الجودة | السرعة |
|---------|---------|-------|--------|
| `eleven_multilingual_v2` | ✅ ممتاز | ⭐⭐⭐⭐⭐ | متوسط |
| `eleven_turbo_v2_5` | ✅ جيد | ⭐⭐⭐⭐ | سريع |
| `eleven_flash_v2_5` | ✅ مقبول | ⭐⭐⭐ | سريع جداً |

**الموصى به للفيديوهات:** `eleven_multilingual_v2`

## API Call كامل

```python
import requests

def tts_arabic(text, voice_id, api_key, emotion="محايد"):
    
    emotion_map = {
        "محايد":  {"stability": 0.50, "similarity_boost": 0.75, "style": 0.00},
        "متحمس": {"stability": 0.35, "similarity_boost": 0.80, "style": 0.40},
        "جدي":   {"stability": 0.70, "similarity_boost": 0.70, "style": 0.10},
        "مفاجئ": {"stability": 0.30, "similarity_boost": 0.80, "style": 0.50},
        "هادئ":  {"stability": 0.80, "similarity_boost": 0.65, "style": 0.00},
    }
    
    settings = emotion_map.get(emotion, emotion_map["محايد"])
    
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": settings["stability"],
                "similarity_boost": settings["similarity_boost"],
                "style": settings["style"],
                "use_speaker_boost": True
            }
        },
        timeout=60
    )
    
    return response.content  # bytes (MP3)
```

## أصوات عربية مناسبة

### أصوات افتراضية تعمل مع العربية:
- `Adam` (ID: `pNInz6obpgDQGcFmaJgB`) — ذكر، رسمي
- `Antoni` (ID: `ErXwobaYiN019PkySvjV`) — ذكر، ودود  
- `Rachel` (ID: `21m00Tcm4TlvDq8ikWAM`) — أنثى، محايدة

### للحصول على أفضل نتيجة:
1. اذهب إلى VoiceLab على ElevenLabs
2. أنشئ صوتاً من تسجيل عربي (Voice Cloning)
3. استخدم الـ ID الناتج

## حساب التكلفة

```python
# ElevenLabs: يحسب بالحروف
def estimate_cost(scenes):
    total_chars = sum(len(s['voiceover']) for s in scenes)
    
    # Creator plan: $22/شهر = 100,000 حرف
    cost_per_char = 22 / 100000
    estimated_cost = total_chars * cost_per_char
    
    print(f"إجمالي الحروف: {total_chars}")
    print(f"التكلفة التقديرية: ${estimated_cost:.4f}")
    
    return estimated_cost

# مثال: 7 مشاهد × 100 حرف = 700 حرف ≈ $0.0015 للفيديو
```

## نصائح كتابة الفويس أوفر العربي

1. **الجمل القصيرة أفضل** — لا تتجاوز 3 جمل للمشهد
2. **تجنّب الحروف الغريبة** — لا emoji، لا أرقام (اكتبها حروفاً)
3. **الفواصل مهمة** — تساعد النموذج على التنفس الطبيعي
4. **مثال جيد:**
   ```
   "الفيزياء النووية ليست صعبة كما تظن. كل شيء يبدأ بالذرة. دعنا نستكشف سرها معاً."
   ```
5. **مثال سيء:**
   ```
   "الفيزياء النووية (Nuclear Physics) هي علم يدرس atoms⚛️ & molecules في 3 خطوات رئيسية:"
   ```
