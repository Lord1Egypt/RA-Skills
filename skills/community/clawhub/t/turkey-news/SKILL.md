---
name: turkey-news
version: 1.0.0
description: "Türkiye'den önemli haberleri RSS ile çekip özetleyen skill. Cron ile otomatik bildirim yapar."
author: dias
tags: [news, turkey, rss, turkish]
---

# 🇹🇷 Turkey News

Türkiye'deki önemli haberleri takip eder ve özetler.

## Kaynaklar (RSS)

- NTV: https://www.ntv.com.tr/son-dakika.rss
- CNN Türk: https://www.cnnturk.com/feed/rss/all/news
- TRT Haber: https://www.trthaber.com/sondakika.rss
- Sözcü: https://www.sozcu.com.tr/rss/all.xml
- Milliyet: https://www.milliyet.com.tr/rss/rssnew/gundemrss.xml
- Habertürk: https://www.haberturk.com/rss
- Hürriyet: https://www.hurriyet.com.tr/rss/anasayfa
- Sabah: https://www.sabah.com.tr/rss/anasayfa.xml
- Anadolu Ajansı: https://www.aa.com.tr/tr/rss/default?cat=guncel

## Kullanım

### Manuel
Agent'a "Türkiye haberleri ver" veya "son haberler ne" de.

### Otomatik (Cron)
Günde 2-3 kez cron job ile çalıştır. Agent haberleri çeker, filtreler ve önemli olanları Telegram'dan bildirir.

### Script
```bash
node scripts/fetch-news.js
```
JSON çıktı verir, agent yorumlar.

## Agent Talimatları

1. `scripts/fetch-news.js` çalıştır
2. Çıktıdan son 3 saatteki haberleri filtrele
3. En önemli 5-7 haberi seç
4. Kısa Türkçe özet yaz (başlık + 1 cümle)
5. Telegram'dan Usta'ya bildir
