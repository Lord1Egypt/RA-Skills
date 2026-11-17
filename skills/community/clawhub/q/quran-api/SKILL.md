# Quran API Skill

البحث في القرآن الكريم باستخدام API alquran.cloud.

## الاستخدام

### الحصول على سورة كاملة
```bash
bash scripts/quran_search.sh surah_by_number 10
```

### الحصول على آية محددة
```bash
bash scripts/quran_search.sh ayah 10:27
```
(سورة:آية)

### الحصول على صفحة
```bash
bash scripts/quran_search.sh page 212
```

### الحصول على جزء
```bash
bash scripts/quran_search.sh juz 11
```

## المخرجات

- نص الآية بالعربية مع التشكيل (من مصحف المدينة المبسط)
- معلومات السورة (الاسم، عدد الآيات، نوع النزول)
- معلومات الآية (رقمها، الصفحة، الجزء، الركوع، السجدة)

## API

Base URL: `https://api.alquran.cloud/v1/`

## التجربة

تم التحقق من العمل:
- سورة يونس آية ٢٧ ✅
- سورة يونس كاملة ✅
- الصفحة ٢١٢ ✅
