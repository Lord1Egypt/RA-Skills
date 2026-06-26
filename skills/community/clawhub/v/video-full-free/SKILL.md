---
name: short-video-ai
description: >
  بايبلاين إنتاج فيديو قصير (60-90 ثانية) بالكامل بالذكاء الاصطناعي.
  المستخدم يعطي فكرة أو عنوان → يولّد سكريبت مقسّم لمشاهد (كل مشهد 10 ثوانٍ) →
  يولّد فيديو كل مشهد بـ Wan2.6 → يولّد صوت كل مشهد بـ ElevenLabs →
  يدمج الكل بـ FFmpeg → يرسل الفيديو النهائي على Telegram.
  استخدم هذه المهارة عند أي طلب من نوع:
  "اعمل فيديو عن ...", "اعمل شورت عن ...", "اعمل ريلز عن ...",
  "short video ai", "فيديو ذكاء اصطناعي كامل", "wan2 + elevenlabs + telegram".
triggers:
  - "اعمل فيديو"
  - "اعمل شورت"
  - "اعمل ريلز"
  - "short video ai"
  - "wan2 elevenlabs"
  - "فيديو ذكاء اصطناعي"
  - "فيديو تلقائي"
compatibility:
  required_apis:
    - HuggingFace API (Wan2.6 أو Wan2.1)
    - ElevenLabs API
    - Telegram Bot API
  required_tools:
    - ffmpeg (مثبّت على الخادم أو VPS)
  optional:
    - fal.ai (بديل لـ HuggingFace)
---

# 🎬 Short-Video-AI Pipeline
## إنتاج فيديو قصير تلقائي بالكامل — من الفكرة إلى Telegram

---

## نظرة عامة على البايبلاين

```
المستخدم يعطي فكرة/عنوان
         ↓
[المرحلة 1] توليد السكريبت (LLM)
  → 6–9 مشاهد × 10 ثوانٍ
  → كل مشهد: وصف بصري + نص فويس أوفر (متوافقَين)
         ↓
[المرحلة 2] توليد فيديوهات المشاهد (Wan2.6 / HuggingFace)
  → لكل مشهد: scene_N.mp4
         ↓
[المرحلة 3] توليد صوت كل مشهد (ElevenLabs TTS)
  → لكل مشهد: vo_N.mp3
         ↓
[المرحلة 4] دمج الفيديو + الصوت لكل مشهد (FFmpeg)
  → merged_N.mp4
         ↓
[المرحلة 5] دمج كل المشاهد في فيديو واحد (FFmpeg concat)
  → final_video.mp4
         ↓
[المرحلة 6] إرسال على Telegram ✅
```

---

## الإعدادات المطلوبة

احفظ هذه القيم في بيئة العمل أو اطلبها من المستخدم قبل البدء:

```
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxx
ELEVENLABS_VOICE_ID=xxxxxx          ← ID الصوت المختار
TELEGRAM_BOT_TOKEN=xxxx:xxxxxxxx
TELEGRAM_CHAT_ID=xxxxxxxxx
```

---

## المتغيرات المطلوبة من المستخدم

| المتغير | الوصف | القيمة الافتراضية |
|---------|-------|-------------------|
| `TOPIC` | فكرة أو عنوان الفيديو | — (مطلوب) |
| `LANG` | لغة الفويس أوفر | `عربي` |
| `STYLE` | أسلوب المحتوى | `تعليمي` |
| `SCENES_COUNT` | عدد المشاهد (6–9) | `7` |
| `PROJECT_NAME` | اسم المجلد (بدون مسافات) | مشتق من TOPIC |

---

## المرحلة 1 — توليد السكريبت المتوافق

### 🔑 المبدأ الأساسي للتوافق
**الوصف البصري والفويس أوفر يجب أن يكونا وجهَين لنفس اللحظة.**
مثال صحيح:
- visual: `طائرة تشق السحاب الأبيض عند الغروب، ضوء ذهبي يملأ الأفق`
- voiceover: `"في رحلة طيران عادية، اكتشف الركاب شيئاً غريراً فوق الغيوم"`

مثال خاطئ (غير متوافق):
- visual: `طائرة في ليل مظلم` ← بينما الصوت: `"شمس الصحراء تحرق الأرض"`

---

### برومبت توليد السكريبت

أرسل هذا البرومبت للـ LLM (Claude أو GPT-4):

```
أنت كاتب سكريبت محترف متخصص في مقاطع الفيديو القصيرة.

اكتب سكريبت فيديو عن: [TOPIC]
الأسلوب: [STYLE]
اللغة: [LANG]
عدد المشاهد: [SCENES_COUNT]
مدة كل مشهد: 10 ثوانٍ بالضبط

قواعد صارمة:
1. كل مشهد له visual_description بالإنجليزية (للـ AI video generator)
2. كل مشهد له voiceover بلغة [LANG] (للنطق بـ TTS)
3. الـ visual_description يجب أن يصف نفس اللحظة التي يتحدث عنها الـ voiceover
4. الـ voiceover لكل مشهد = 2-3 جمل قصيرة تُنطق في 8-9 ثوانٍ
5. المشهد الأول (hook) يجب أن يكون صادماً أو مثيراً للفضول
6. المشهد الأخير يحتوي على call-to-action أو خلاصة

أعطني JSON فقط بدون أي نص خارجه:
{
  "project_title": "عنوان الفيديو",
  "total_duration": "XX ثانية",
  "style_notes": "ملاحظات الأسلوب البصري الموحّد",
  "scenes": [
    {
      "scene_number": 1,
      "duration_seconds": 10,
      "visual_description": "وصف بصري دقيق بالإنجليزية — cinematic, no text, no watermark, 9:16 vertical format",
      "visual_keywords": ["keyword1", "keyword2", "keyword3"],
      "voiceover": "النص المنطوق بالعربية هنا — 2-3 جمل",
      "voiceover_emotion": "محايد / متحمس / جدي / مفاجئ",
      "scene_purpose": "hook / معلومة / مثال / خلاصة / CTA",
      "consistency_note": "ملاحظة تشرح كيف يتوافق البصري مع الصوت"
    }
  ],
  "visual_style": "وصف الأسلوب البصري الموحّد للفيديو كله"
}
```

### استخراج ومعالجة النتيجة

```python
import json, re

# استخراج JSON من رد الـ LLM
def extract_script(llm_response):
    # إزالة markdown code blocks لو موجودة
    clean = re.sub(r'```json|```', '', llm_response).strip()
    script = json.loads(clean)
    
    # التحقق من التوافق لكل مشهد
    for scene in script['scenes']:
        assert 'visual_description' in scene, f"المشهد {scene['scene_number']} بدون وصف بصري"
        assert 'voiceover' in scene, f"المشهد {scene['scene_number']} بدون فويس أوفر"
    
    return script
```

---

## المرحلة 2 — توليد فيديوهات المشاهد (Wan2.6)

**API المستخدم:** HuggingFace Inference API أو Wan2.6 Space  
**النموذج:** `Wan-AI/Wan2.6-T2V-14B` (الأفضل جودةً)  
**البديل:** `Wan-AI/Wan2.1-T2V-14B` (أسرع)

> 📋 للتفاصيل الكاملة لـ Wan2.6 ومعاملاته راجع: `references/wan2-api.md`

### كود توليد فيديو مشهد واحد

```python
import requests, time, os

def generate_scene_video(scene, project_dir, hf_token):
    """يولّد فيديو مشهد واحد باستخدام Wan2.6"""
    
    # بناء الـ prompt مع الأسلوب الموحّد
    prompt = f"""
    {scene['visual_description']},
    cinematic quality, 9:16 vertical format, ultra-realistic,
    smooth motion, professional lighting, no text, no watermark,
    {', '.join(scene['visual_keywords'])}
    """
    
    # إرسال الطلب لـ HuggingFace
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt.strip(),
        "parameters": {
            "num_frames": 81,           # ~10 ثوانٍ عند 8fps
            "fps": 8,
            "width": 480,
            "height": 832,              # 9:16
            "num_inference_steps": 30,
            "guidance_scale": 5.0,
            "seed": 42
        }
    }
    
    # استخدام HuggingFace Inference API
    model_id = "Wan-AI/Wan2.6-T2V-14B"
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    response = requests.post(api_url, headers=headers, json=payload, timeout=300)
    
    if response.status_code == 200:
        # حفظ الفيديو
        output_path = os.path.join(project_dir, f"scene_{scene['scene_number']:02d}.mp4")
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ المشهد {scene['scene_number']} جاهز: {output_path}")
        return output_path
    else:
        raise Exception(f"❌ فشل المشهد {scene['scene_number']}: {response.status_code} — {response.text}")
```

### حلقة توليد جميع المشاهد

```python
import os

def generate_all_scenes(script, project_dir, hf_token):
    scene_videos = []
    
    for scene in script['scenes']:
        print(f"🎬 توليد المشهد {scene['scene_number']}/{len(script['scenes'])}...")
        print(f"   البصري: {scene['visual_description'][:60]}...")
        print(f"   الصوت:  {scene['voiceover'][:50]}...")
        
        video_path = generate_scene_video(scene, project_dir, hf_token)
        scene_videos.append(video_path)
        
        # انتظار بين الطلبات لتجنب rate limiting
        time.sleep(3)
    
    return scene_videos
```

---

## المرحلة 3 — توليد الصوت (ElevenLabs TTS)

### كود توليد فويس أوفر مشهد واحد

```python
import requests

def generate_voiceover(scene, project_dir, elevenlabs_key, voice_id):
    """يولّد الفويس أوفر لمشهد واحد بـ ElevenLabs"""
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "xi-api-key": elevenlabs_key,
        "Content-Type": "application/json"
    }
    
    # إعدادات الصوت حسب عاطفة المشهد
    emotion_settings = {
        "محايد":   {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0},
        "متحمس":   {"stability": 0.35, "similarity_boost": 0.8, "style": 0.4},
        "جدي":    {"stability": 0.7, "similarity_boost": 0.7, "style": 0.1},
        "مفاجئ":  {"stability": 0.3, "similarity_boost": 0.8, "style": 0.5},
    }
    
    emotion = scene.get('voiceover_emotion', 'محايد')
    settings = emotion_settings.get(emotion, emotion_settings['محايد'])
    
    payload = {
        "text": scene['voiceover'],
        "model_id": "eleven_multilingual_v2",   # يدعم العربية
        "voice_settings": {
            "stability": settings["stability"],
            "similarity_boost": settings["similarity_boost"],
            "style": settings["style"],
            "use_speaker_boost": True
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        output_path = os.path.join(project_dir, f"vo_{scene['scene_number']:02d}.mp3")
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ صوت المشهد {scene['scene_number']} جاهز: {output_path}")
        return output_path
    else:
        raise Exception(f"❌ فشل صوت المشهد {scene['scene_number']}: {response.status_code}")
```

### حلقة توليد جميع الأصوات

```python
def generate_all_voiceovers(script, project_dir, elevenlabs_key, voice_id):
    voiceovers = []
    
    for scene in script['scenes']:
        print(f"🎙️ توليد صوت المشهد {scene['scene_number']}...")
        vo_path = generate_voiceover(scene, project_dir, elevenlabs_key, voice_id)
        voiceovers.append(vo_path)
        time.sleep(1)
    
    return voiceovers
```

---

## المرحلة 4 — دمج الفيديو + الصوت لكل مشهد (FFmpeg)

```python
import subprocess

def merge_scene_av(scene_num, video_path, audio_path, project_dir):
    """يدمج فيديو المشهد مع صوته"""
    
    output_path = os.path.join(project_dir, f"merged_{scene_num:02d}.mp4")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,           # فيديو المشهد
        "-i", audio_path,           # صوت المشهد
        "-c:v", "copy",             # نسخ الفيديو بدون إعادة encoding
        "-c:a", "aac",              # تحويل الصوت لـ AAC
        "-b:a", "192k",
        "-shortest",                # ينتهي عند انتهاء أقصر المقطعَين
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg merge error: {result.stderr}")
    
    print(f"✅ دمج المشهد {scene_num} جاهز: {output_path}")
    return output_path
```

---

## المرحلة 5 — دمج كل المشاهد في فيديو واحد

```python
def concat_all_scenes(merged_videos, project_dir, project_name):
    """يدمج كل المشاهد في فيديو واحد بـ FFmpeg concat"""
    
    # إنشاء ملف قائمة المشاهد
    concat_file = os.path.join(project_dir, "concat_list.txt")
    with open(concat_file, 'w') as f:
        for video in merged_videos:
            f.write(f"file '{os.path.abspath(video)}'\n")
    
    final_path = os.path.join(project_dir, f"{project_name}_final.mp4")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264",          # إعادة encode للتوافق الكامل
        "-c:a", "aac",
        "-preset", "fast",
        "-crf", "23",
        "-movflags", "+faststart",  # تحسين للـ streaming
        final_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg concat error: {result.stderr}")
    
    # حذف ملف القائمة المؤقت
    os.remove(concat_file)
    
    print(f"🎉 الفيديو النهائي جاهز: {final_path}")
    return final_path
```

---

## المرحلة 6 — الإرسال على Telegram

```python
def send_to_telegram(video_path, script, bot_token, chat_id):
    """يرسل الفيديو النهائي مع caption على Telegram"""
    
    # بناء الـ caption
    caption = f"""🎬 *{script['project_title']}*

📋 *المشاهد:*
"""
    for scene in script['scenes']:
        caption += f"\n*{scene['scene_number']}* — {scene['voiceover'][:60]}..."
    
    caption += f"\n\n⏱️ المدة: {script['total_duration']}"
    caption += "\n\n🤖 _تم الإنتاج بالكامل بالذكاء الاصطناعي_"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    
    with open(video_path, 'rb') as video_file:
        response = requests.post(url, data={
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": "Markdown",
            "supports_streaming": True
        }, files={"video": video_file}, timeout=120)
    
    if response.status_code == 200:
        print("✅ تم الإرسال على Telegram بنجاح!")
        return response.json()
    else:
        raise Exception(f"❌ فشل إرسال Telegram: {response.status_code} — {response.text}")
```

---

## الكود الرئيسي — تشغيل البايبلاين كاملاً

```python
import json, os, time

def run_short_video_pipeline(
    topic,
    lang="عربي",
    style="تعليمي",
    scenes_count=7,
    project_name=None
):
    """
    البايبلاين الرئيسي — من الفكرة إلى Telegram
    """
    
    # =================== الإعدادات ===================
    HF_TOKEN = os.environ['HUGGINGFACE_API_TOKEN']
    EL_KEY   = os.environ['ELEVENLABS_API_KEY']
    EL_VOICE = os.environ['ELEVENLABS_VOICE_ID']
    TG_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
    TG_CHAT  = os.environ['TELEGRAM_CHAT_ID']
    
    if not project_name:
        project_name = topic[:20].replace(' ', '_').replace('/', '-')
    
    # إنشاء مجلد المشروع
    project_dir = f"/tmp/short_video/{project_name}"
    os.makedirs(project_dir, exist_ok=True)
    
    print(f"📁 مجلد المشروع: {project_dir}")
    print(f"🎯 الموضوع: {topic}")
    print(f"🎬 عدد المشاهد: {scenes_count} مشهد × 10 ثوانٍ")
    
    # =================== المرحلة 1: السكريبت ===================
    print("\n━━━ المرحلة 1: توليد السكريبت ━━━")
    
    script_prompt = build_script_prompt(topic, lang, style, scenes_count)
    llm_response  = call_llm(script_prompt)   # استخدم Claude أو GPT-4
    script        = extract_script(llm_response)
    
    # حفظ السكريبت
    with open(f"{project_dir}/script.json", 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    
    print(f"✅ السكريبت جاهز: {len(script['scenes'])} مشهد")
    
    # =================== المرحلة 2: الفيديوهات ===================
    print("\n━━━ المرحلة 2: توليد فيديوهات المشاهد (Wan2.6) ━━━")
    scene_videos = generate_all_scenes(script, project_dir, HF_TOKEN)
    
    # =================== المرحلة 3: الأصوات ===================
    print("\n━━━ المرحلة 3: توليد الفويس أوفر (ElevenLabs) ━━━")
    voiceovers = generate_all_voiceovers(script, project_dir, EL_KEY, EL_VOICE)
    
    # =================== المرحلة 4: دمج مشهد × صوت ===================
    print("\n━━━ المرحلة 4: دمج الفيديو والصوت لكل مشهد ━━━")
    merged_videos = []
    for i, (vid, aud) in enumerate(zip(scene_videos, voiceovers), 1):
        merged = merge_scene_av(i, vid, aud, project_dir)
        merged_videos.append(merged)
    
    # =================== المرحلة 5: الدمج النهائي ===================
    print("\n━━━ المرحلة 5: دمج كل المشاهد في فيديو واحد ━━━")
    final_video = concat_all_scenes(merged_videos, project_dir, project_name)
    
    # =================== المرحلة 6: Telegram ===================
    print("\n━━━ المرحلة 6: الإرسال على Telegram ━━━")
    send_to_telegram(final_video, script, TG_TOKEN, TG_CHAT)
    
    print(f"\n🎉 اكتمل البايبلاين بنجاح!")
    print(f"📂 الملفات في: {project_dir}")
    return final_video
```

---

## مثال عملي كامل

```python
# تشغيل مثال
result = run_short_video_pipeline(
    topic="أسرار الفيزياء النووية التي لا تعرفها",
    lang="عربي",
    style="تعليمي مثير",
    scenes_count=7,
    project_name="nuclear_secrets"
)
```

**مثال على سكريبت سيُنتَج:**

```
المشهد 1 (hook):
  visual:    "Extreme close-up of a uranium atom, electrons orbiting in 
              deep blue light, cinematic macro lens, 9:16 vertical"
  voiceover: "هل تعلم أن كيلو واحد من اليورانيوم يعادل 3 ملايين كيلو فحم؟"

المشهد 2:
  visual:    "Nuclear power plant control room with glowing displays,
              scientist in white coat monitoring screens, dramatic lighting"
  voiceover: "المفاعلات النووية لا تنفجر كالقنابل — الانشطار هناك محكوم بدقة متناهية"

...وهكذا لكل المشاهد
```

---

## التعامل مع الأخطاء

| الموقف | الإجراء |
|--------|---------|
| HuggingFace يُرجع 503 | أعد المحاولة بعد 30 ثانية (النموذج يُحمَّل) |
| ElevenLabs رصيد منتهي | أبلغ المستخدم — كل دقيقة صوت ≈ 1500 حرف |
| FFmpeg: audio/video out of sync | أضف `-async 1` للأمر |
| Telegram: file too large | ضغّط بـ `-crf 28` بدل `23` |
| Wan2.6 يرفض الـ prompt | احذف الكلمات الحساسة واستبدل بوصف أكثر حيادية |
| السكريبت غير متوافق | أعد توليده مع التأكيد الصريح في الـ prompt |

---

## نصائح الجودة

### لأفضل نتائج Wan2.6:
- دائماً أضف: `cinematic, 9:16 vertical, smooth motion, no text`
- تجنّب: مشاهد فيها نصوص أو وجوه بشرية كثيرة (التشويه يزيد)
- الأفضل: مشاهد طبيعة، تقنية، فضاء، مباني، بيانات تحريكية

### لأفضل صوت ElevenLabs بالعربية:
- استخدم `eleven_multilingual_v2` (يدعم العربية أفضل)
- أصوات مناسبة للعربية: `Adam`, `Antoni`, أو أضف صوتك المستنسخ
- اجعل جمل الفويس أوفر قصيرة (لا تتجاوز 150 حرف للمشهد)

### للتوافق البصري-الصوتي:
- راجع `consistency_note` في كل مشهد من السكريبت
- إذا بدا الوصف غير متوافق → أعد توليد السكريبت فقط (بدون إعادة الفيديو)

---

## هيكل مجلد المشروع

```
/tmp/short_video/[project_name]/
├── script.json              ← السكريبت الكامل
├── scene_01.mp4             ← فيديو المشهد 1 (Wan2.6)
├── scene_02.mp4
├── ...
├── vo_01.mp3               ← صوت المشهد 1 (ElevenLabs)
├── vo_02.mp3
├── ...
├── merged_01.mp4           ← مشهد 1 + صوته
├── merged_02.mp4
├── ...
└── [project_name]_final.mp4 ← الفيديو النهائي ✅
```

> 📋 للتفاصيل الكاملة لـ APIs راجع:
> - `references/wan2-api.md` — معاملات Wan2.6 والـ endpoints
> - `references/elevenlabs-arabic.md` — أفضل إعدادات الصوت العربي
> - `references/ffmpeg-recipes.md` — وصفات FFmpeg الجاهزة
