# 寰俊鍏紬鍙疯嚜鍔ㄥ彂甯冩妧鑳?
馃摑 **涓€閿彂甯?Markdown/HTML 鏂囩珷鍒板井淇″叕浼楀彿鑽夌绠?*

---

## 蹇€熷紑濮?
### 1. 瀹夎鎶€鑳?
鎶€鑳藉凡瀹夎鍒帮細
```
C:\Users\JMO\.openclaw\workspace\skills\wechat-publisher-pro/
```

### 2. 閰嶇疆鍏紬鍙?
**鑾峰彇 APPID 鍜?APPSECRET:**
```
1. 鐧诲綍 https://mp.weixin.qq.com
2. 璁剧疆涓庡紑鍙?鈫?鍩烘湰閰嶇疆
3. 澶嶅埗 APPID 鍜?APPSECRET
```

**閰嶇疆 IP 鐧藉悕鍗?**
```
1. 璁剧疆涓庡紑鍙?鈫?鍩烘湰閰嶇疆 鈫?IP 鐧藉悕鍗?2. 娣诲姞浣犵殑鍏綉 IP
3. 绛夊緟 5 鍒嗛挓鐢熸晥
```

### 3. 璁剧疆鐜鍙橀噺

```bash
cd C:\Users\JMO\.openclaw\workspace\skills\wechat-publisher-pro
copy .env.example .env
```

缂栬緫 `.env` 鏂囦欢锛屽～鍏ヤ綘鐨勯厤缃細
```
WECHAT_APPID=浣犵殑 APPID
WECHAT_APPSECRET=浣犵殑 APPSECRET
```

---

## 浣跨敤鏂规硶

### 鏂瑰紡 1: 鍛戒护琛?
```bash
cd C:\Users\JMO\.openclaw\workspace\skills\wechat-publisher-pro

# 鍙戝竷鏂囩珷
python scripts/wechat_publish.py \
  --article "C:/path/to/article.md" \
  --cover "C:/path/to/cover.jpg" \
  --title "鏂囩珷鏍囬" \
  --beautify
```

### 鏂瑰紡 2: 鍦?OpenClaw 涓?
```
甯垜鍙戝竷杩欑瘒鏂囩珷鍒板井淇″叕浼楀彿锛?鏂囩珷锛歮emory/content/articles/openclaw-ecosystem-review.md
灏侀潰锛欴ownloads/wechat-cover-ai-AI 浠ｇ爜.jpg
鏍囬锛歄penClaw 鐢熸€侊細14 涓?AI 椤圭洰妯瘎
```

### 鏂瑰紡 3: Python 浠ｇ爜

```python
from scripts.wechat_publish import WeChatPublisher

publisher = WeChatPublisher(
    appid="你的 APPID",
    appsecret="你的 APPSECRET"
)

result = publisher.publish(
    article_path="article.md",
    cover_path="cover.jpg",
    title="鏂囩珷鏍囬",
    beautify=True
)

print(f"鑽夌 ID: {result}")
```

---

## 鍔熻兘鐗规€?
鉁?**鏍稿績鍔熻兘**
- 涓€閿彂甯冨埌鑽夌绠?- Markdown/HTML 鑷姩杞崲
- 涓枃缂栫爜淇锛圲TF-8锛?- 鑷姩涓婁紶灏侀潰鍥?- 缇庡寲鎺掔増鏍峰紡

鉁?**缇庡寲鐗规€?*
- 娓愬彉瀵艰妗?- 鏍囬鏍峰紡浼樺寲
- 鍒楄〃鏍煎紡缇庡寲
- 娈佃惤闂磋窛浼樺寲
- 搴曢儴淇℃伅鏍?
鉁?**鎶€鏈紭鍔?*
- 瑙ｅ喅 Unicode 杞箟闂
- 瑙ｅ喅涓枃涔辩爜闂
- 鏀寔闀挎枃绔狅紙50000 瀛椾互鍐咃級
- 鑷姩鍥剧墖鍘嬬缉

---

## 鍙傛暟璇存槑

```bash
python scripts/wechat_publish.py \
  --article "鏂囩珷璺緞" \          # 蹇呴渶锛?md 鎴?.html 鏂囦欢
  --cover "灏侀潰鍥捐矾寰? \          # 蹇呴渶锛欽PG/PNG 鍥剧墖
  --title "鏂囩珷鏍囬" \            # 蹇呴渶锛氭枃绔犳爣棰?  --digest "鎽樿" \               # 鍙€夛細鏂囩珷鎽樿
  --appid "APPID" \               # 鍙€夛細榛樿浠庣幆澧冨彉閲忚鍙?  --appsecret "APPSECRET" \       # 鍙€夛細榛樿浠庣幆澧冨彉閲忚鍙?  --beautify                      # 鍙€夛細鍚敤缇庡寲鎺掔増
  --dry-run                       # 鍙€夛細娴嬭瘯妯″紡锛屼笉瀹為檯鍙戝竷
```

---

## 绀轰緥

### 绀轰緥 1: 鍙戝竷鎶€鏈枃绔?
```bash
python scripts/wechat_publish.py \
  --article "memory/content/articles/openclaw-ecosystem-review.md" \
  --cover "Downloads/wechat-cover-ai-AI 浠ｇ爜.jpg" \
  --title "OpenClaw 鐢熸€侊細14 涓?AI 椤圭洰妯瘎" \
  --digest "浠?56 涓囪浠ｇ爜浼樺寲鍒?888KB锛孫penClaw 濡備綍寮曠垎 AI Agent 鐢熸€侊紵" \
  --beautify
```

### 绀轰緥 2: 娴嬭瘯妯″紡

```bash
python scripts/wechat_publish.py \
  --article "article.md" \
  --cover "cover.jpg" \
  --title "娴嬭瘯鏂囩珷" \
  --dry-run
```

### 绀轰緥 3: 涓嶅惎鐢ㄧ編鍖?
```bash
python scripts/wechat_publish.py \
  --article "article.md" \
  --cover "cover.jpg" \
  --title "绠€鍗曟枃绔?
```

---

## 鏂囦欢缁撴瀯

```
wechat-publisher-pro/
鈹溾攢鈹€ SKILL.md                 # 鎶€鑳借鏄?鈹溾攢鈹€ README.md                # 鏈枃妗?鈹溾攢鈹€ .env.example             # 鐜鍙橀噺绀轰緥
鈹溾攢鈹€ scripts/
鈹?  鈹溾攢鈹€ wechat_publish.py    # 涓诲彂甯冭剼鏈?鈹?  鈹溾攢鈹€ beautify_html.py     # 缇庡寲鑴氭湰
鈹?  鈹斺攢鈹€ test_api.py          # API 娴嬭瘯鑴氭湰
鈹溾攢鈹€ templates/
鈹?  鈹斺攢鈹€ article_template.html # 鏂囩珷妯℃澘
鈹斺攢鈹€ examples/
    鈹溾攢鈹€ article.md           # 绀轰緥鏂囩珷
    鈹斺攢鈹€ cover.jpg            # 绀轰緥灏侀潰
```

---

## 甯歌闂

### Q1: Token 鑾峰彇澶辫触

**閿欒淇℃伅:**
```
{'errcode': 40164, 'errmsg': 'invalid ip ...'}
```

**瑙ｅ喅鏂规硶:**
```
1. 鐧诲綍 mp.weixin.qq.com
2. 璁剧疆涓庡紑鍙?鈫?鍩烘湰閰嶇疆 鈫?IP 鐧藉悕鍗?3. 娣诲姞浣犵殑鍏綉 IP锛堣繍琛?curl https://ifconfig.me/ip 鏌ョ湅锛?4. 绛夊緟 5-10 鍒嗛挓鐢熸晥
5. 閲嶈瘯
```

### Q2: 涓枃涔辩爜

**鐜拌薄:** 鑽夌绠辨樉绀?`\u751f\u6001` 鑰屼笉鏄?`鐢熸€乣

**鍘熷洜:** JSON 缂栫爜闂

**瑙ｅ喅:** 鑴氭湰宸茶嚜鍔ㄤ慨澶嶏紝纭繚浣跨敤 `ensure_ascii=False`

### Q3: 鍥剧墖涓婁紶澶辫触

**閿欒淇℃伅:**
```
{'errcode': 45001, 'errmsg': 'file size exceed'}
```

**瑙ｅ喅:**
```
- 鍥剧墖澶у皬锛?10MB
- 鏍煎紡锛欽PG/PNG
- 灏哄锛氬缓璁?1200x630px
```

### Q4: 鎵句笉鍒拌崏绋?
**瑙ｅ喅:**
```
1. 纭鍏紬鍙锋槸鍚︽纭?2. 鏌ョ湅鑽夌绠憋紙涓嶆槸宸插彂琛級
3. 鍒锋柊椤甸潰
4. 妫€鏌?API 杩斿洖鐨?media_id
```

---

## 鏈€浣冲疄璺?
### 1. 鏂囩珷鏍煎紡

```markdown
# 鏍囬

> 瀵艰锛堜細鏄剧ず鍦ㄦ憳瑕佷腑锛?
## 灏忔爣棰?1

鍐呭...

- 鍒楄〃椤?1
- 鍒楄〃椤?2

## 灏忔爣棰?2

鍐呭...
```

### 2. 灏侀潰鍥捐鏍?
- **灏哄:** 1200x630px (2.35:1)
- **鏍煎紡:** JPG/PNG
- **澶у皬:** <10MB
- **鍐呭:** 涓庢枃绔犱富棰樼浉鍏?
### 3. 鍙戝竷鏃堕棿

**鏈€浣虫椂闂?**
- 宸ヤ綔鏃ワ細20:00-22:00
- 鍛ㄦ湯锛?0:00-12:00

### 4. 鍙戝竷娴佺▼

```
1. 鍑嗗鏂囩珷 (.md 鎴?.html)
2. 鍑嗗灏侀潰鍥?3. 杩愯鍙戝竷鑴氭湰
4. 妫€鏌ヨ崏绋跨
5. 鎵嬫満棰勮
6. 纭鍙戝竷
```

---

## 鏇存柊鏃ュ織

### v1.0.0 (2026-03-11)
- 鉁?鍩虹鍙戝竷鍔熻兘
- 鉁?Markdown 杞?HTML
- 鉁?涓枃缂栫爜淇
- 鉁?鑷姩涓婁紶鍥剧墖
- 鉁?缇庡寲鎺掔増

### v1.1.0 (璁″垝)
- 馃搮 鎵归噺鍙戝竷
- 馃搮 瀹氭椂鍙戝竷
- 馃搮 鏁版嵁鍒嗘瀽
- 馃搮 澶氳处鍙锋敮鎸?
---

## 鎶€鏈敮鎸?
**鏂囨。:** 鏌ョ湅鏈洰褰?README.md

**绀轰緥:** `examples/` 鐩綍

**闂鍙嶉:** 鑱旂郴鎶€鑳戒綔鑰?
---

*鏈€鍚庢洿鏂帮細2026-03-11*  
*鐗堟湰锛歷1.0.0*  
*浣滆€咃細Robotqu*

