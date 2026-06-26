# Virtual Desktop Browser Skill (العربية)

تشغيل **Chromium بوضع غير headless** على **شاشة Xvfb افتراضية (ثابتة 1200x720x24)** مع أتمتة تشبه سلوك الإنسان باستخدام PyAutoGUI. مثالي لمواقع مضادة للبوت مثل Xiaohongshu و X/Twitter.

[中文](../README.md) | [English](en.md) | [Español](es.md)

---

## الميزات

| الميزة | الوصف |
|--------|-------|
| شاشة افتراضية | Xvfb خادم X مستقل، 1200x720x24 |
| متصفح غير headless | Chromium مع واجهة على الشاشة الافتراضية |
| محاكاة الماوس | تحريك، نقر (يسار/يمين/وسط/نقر مزدوج)، سحب |
| محاكاة لوحة المفاتيح | إدخال نص، اختصارات، مفاتيح مركبة |
| التمرير | تمرير عمودي وأفقي |
| لقطة شاشة | شاشة كاملة أو منطقة، PNG بـ Base64 |
| مطابقة الصور | البحث عن قوالب الصور على الشاشة (OpenCV) |
| لون البكسل | قراءة RGB في إحداثيات محددة |
| إدارة النوافذ | التركيز على النافذة حسب العنوان |
| تعيين DISPLAY تلقائي | تجنب تعدد الجلسات (:99 ~ :199) |
| إيقاف الطوارئ | نقل الماوس للزاوية السفلية اليمنى يوقف كل شيء |

---

## التثبيت

### تبعيات النظام (Ubuntu/Debian)

```bash
apt-get update
apt-get install -y xvfb chromium-browser \
  libnss3 libgconf-2-4 libxss1 libasound2 \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libgbm1 libgtk-3-0 libxshmfence1 x11-utils
```

### تبعيات بايثون

```bash
pip install -r requirements.txt
```

### تثبيت المهارة

```bash
npx skills add https://github.com/NHZallen/virtual-desktop-browser-skill
```

---

## مرجع الأدوات

### `browser_start(url=None, display=None)`

تشغيل Xvfb و Chromium.

| المعامل | النوع | الوصف |
|---------|------|-------|
| `url` | str (اختياري) | عنوان URL الافتراضي about:blank |
| `display` | str (اختياري) | عرض X، مثال `:99`. تلقائي إذا حُذف |

**النتيجة:**
```json
{
  "status": "started",
  "display": ":99",
  "xvfb_pid": 12345,
  "chrome_pid": 12346,
  "resolution": "1200x720x24"
}
```

---

### `browser_stop()`

إغلاق Chromium و Xvfb، تحرير الموارد.

**النتيجة:** `{ "status": "stopped" }`

---

### `browser_snapshot(region=None)`

التقاط الشاشة الافتراضية، إرجاع PNG بـ Base64.

| المعامل | النوع | الوصف |
|---------|------|-------|
| `region` | tuple (اختياري) | `(left, top, width, height)` |

**النتيجة:**
```json
{
  "image_base64": "iVBORw0KGgo...",
  "width": 1200,
  "height": 720
}
```

---

### `browser_click(x, y, button='left', clicks=1, duration=0.5)`

تحريك الماوس والنقر.

| المعامل | النوع | الافتراضي | الوصف |
|---------|------|-----------|-------|
| `x` | int | مطلوب | إحداثي X |
| `y` | int | مطلوب | إحداثي Y |
| `button` | str | `left` | `left` / `right` / `middle` |
| `clicks` | int | `1` | عدد النقرات |
| `duration` | float | `0.5` | وقت التحريك (ثانية) |

---

### `browser_type(text, interval=0.05, wpm=None)`

كتابة نص في العنصر النشط.

| المعامل | النوع | الافتراضي | الوصف |
|---------|------|-----------|-------|
| `text` | str | مطلوب | النص المراد كتابته |
| `interval` | float | `0.05` | الفاصل بين المفاتيح (ثانية) |
| `wpm` | int (اختياري) | — | كلمات في الدقيقة (سرعة إنسانية) |

---

### `browser_hotkey(keys, interval=0.05)`

الضغط على مفاتيح مركبة.

| المعامل | النوع | الوصف |
|---------|------|-------|
| `keys` | list[str] | أسماء المفاتيح، مثال `["ctrl", "c"]` |
| `interval` | float | الفاصل بين المفاتيح (ثانية) |

---

### `browser_scroll(clicks=1, direction='vertical', x=None, y=None)`

تمرير عجلة الماوس.

| المعامل | النوع | الافتراضي | الوصف |
|---------|------|-----------|-------|
| `clicks` | int | `1` | كمية التمرير (+أعلى/يسار، −أسفل/يمين) |
| `direction` | str | `vertical` | `vertical` أو `horizontal` |

---

### `browser_find_image(image_path, confidence=0.8)`

البحث عن صورة قالب على الشاشة.

**النتيجة:** `{ "found": true, "x": 100, "y": 200, "width": 50, "height": 50 }` أو `{ "found": false }`

---

### `browser_get_pixel_color(x, y)`

الحصول على لون RGB للبكسل.

**النتيجة:** `{ "r": 255, "g": 255, "b": 255 }`

---

### `browser_activate_window(title_substring)`

التركيز على النافذة حسب تطابق العنوان الجزئي.

---

## مثال: تصفح Xiaohongshu

```python
browser_start(url="https://www.xiaohongshu.com/explore")
time.sleep(3)
browser_scroll(clicks=-3)
browser_snapshot()
browser_stop()
```

---

## الأمان

- **Failsafe:** نقل الماوس للزاوية السفلية اليمنى (1199, 719) يوقف كل شيء

---

## استكشاف الأخطاء

| المشكلة | الحل |
|---------|------|
| `Missing: Xvfb` | `apt-get install -y xvfb` |
| `Missing: chromium-browser` | `apt-get install -y chromium-browser` |
| خطأ DISPLAY في PyAutoGUI | التأكد أن `browser_start()` تم استدعاؤه |
| فشل مطابقة الصور | استخدام صورة عالية التباين، خفض `confidence` |

---

## المؤلف

المنشئ: **Allen Niu**  
الرخصة: MIT-0
