---
name: verimor_sms
description: Verimor API üzerinden SMS gönder, bakiye sorgula, rapor al, başlıkları listele ve kara liste yönet.
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
      config:
        - VERIMOR_USERNAME
        - VERIMOR_PASSWORD
        - VERIMOR_SOURCE
---

# Verimor SMS Skill

Bu skill, Verimor SMS API (https://sms.verimor.com.tr/v2) üzerinden
SMS gönderimi ve yönetimi sağlar.

## Kimlik Bilgileri

Tüm komutlarda şu environment variable'ları kullan:
- `VERIMOR_USERNAME` → Verimor kullanıcı adı (905xxxxxxxxx formatında)
- `VERIMOR_PASSWORD` → Verimor API şifresi
- `VERIMOR_SOURCE`   → Varsayılan gönderici başlık (örn: FIRMAM), yoksa boş bırak

---

## 1. SMS Gönder (tek veya çoklu alıcı)

Kullanıcı "SMS gönder", "mesaj at", "bildirim gönder" gibi bir şey söylediğinde:
```bash
curl -s -X POST https://sms.verimor.com.tr/v2/send.json \
  -H "Content-Type: application/json" \
  -d '{
    "username": "'"$VERIMOR_USERNAME"'",
    "password": "'"$VERIMOR_PASSWORD"'",
    "source_addr": "'"$VERIMOR_SOURCE"'",
    "messages": [
      {
        "dest": "905XXXXXXXXX",
        "msg": "Mesaj metni buraya"
      }
    ]
  }'
```

Birden fazla alıcı için `dest` alanına virgülle ayırarak ekle:
`"dest": "905111111111,905222222222"`

İleri tarihli gönderim için `send_at` ekle:
`"send_at": "2025-06-01 10:00:00"`

Ticari mesaj için:
`"is_commercial": true, "iys_recipient_type": "BIREYSEL"`

Başarılı olursa API bir **Kampanya ID** döner (sayısal). Bunu kullanıcıya göster.

**Türkçe karakter notu:** Mesajda Ş ş Ğ ğ ç ı İ harfleri varsa
`"datacoding": 1` ekle. Yoksa `"datacoding": 0` kullan.

---

## 2. Bakiye Sorgula

Kullanıcı "bakiye", "kredi", "kaç SMS kaldı" dediğinde:
```bash
curl -s "https://sms.verimor.com.tr/v2/balance?username=$VERIMOR_USERNAME&password=$VERIMOR_PASSWORD"
```

Dönen sayı kalan SMS kredisidir. Kullanıcıya "X kredi kaldı" şeklinde göster.

---

## 3. Gönderim Raporu Sorgula

Kullanıcı kampanya ID vererek rapor istediğinde:
```bash
curl -s "https://sms.verimor.com.tr/v2/status?username=$VERIMOR_USERNAME&password=$VERIMOR_PASSWORD&id=KAMPANYA_ID" | jq '.'
```

Her mesaj için şu alanları göster:
- `dest` → Alıcı numara
- `status` → DELIVERED, NOT_DELIVERED, WAITING, EXPIRED vb.
- `done_at` → İşlem zamanı
- `credits` → Harcanan kredi

---

## 4. Tanımlı Başlıkları Listele

Kullanıcı "başlıklarım neler", "hangi başlıkları kullanabilirim" dediğinde:
```bash
curl -s "https://sms.verimor.com.tr/v2/headers?username=$VERIMOR_USERNAME&password=$VERIMOR_PASSWORD" | jq '.'
```

---

## 5. Kampanya İptal Et

Kullanıcı ileri tarihli bir kampanyayı iptal etmek istediğinde:
```bash
curl -s -X POST https://sms.verimor.com.tr/v2/cancel/KAMPANYA_ID \
  -H "Content-Type: application/json" \
  -d '{"username": "'"$VERIMOR_USERNAME"'", "password": "'"$VERIMOR_PASSWORD"'"}'
```

---

## 6. Kara Liste Sorgula
```bash
curl -s "https://sms.verimor.com.tr/v2/blacklists?username=$VERIMOR_USERNAME&password=$VERIMOR_PASSWORD" | jq '.'
```

---

## 7. Kara Listeye Numara Ekle
```bash
curl -s -X POST "https://sms.verimor.com.tr/v2/blacklists?username=$VERIMOR_USERNAME&password=$VERIMOR_PASSWORD&phones=905XXXXXXXXX"
```

---

## Hata Durumları

| HTTP Kodu | Anlam |
|---|---|
| 400 | Geçersiz istek (numara formatı, eksik alan) |
| 401 | Hatalı kullanıcı adı veya şifre |
| 403 | IP izinsiz veya yetkisiz erişim |
| 429 | Rate limit aşıldı (dakikada 240 istek) |

Hata alınırsa kullanıcıya hata mesajını ve HTTP kodunu göster.

## Numara Formatı

Tüm Türkiye numaraları `905XXXXXXXXX` formatında olmalı (başında 0 veya +90 değil).
Kullanıcı `05XX` veya `+905XX` formatında verirse otomatik düzelt.
