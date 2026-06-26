# Zotero 鏈湴 API 閰嶇疆鎸囧崡

**鍒涘缓鏃堕棿锛?* 2026 骞?3 鏈?26 鏃? 
**Zotero 鐗堟湰锛?* 7.x  

---

## 馃攳 璇婃柇缁撴灉

绔彛 `23119` 宸插紑鏀撅紝浣?API 璺緞杩斿洖 404銆?
**鍙兘鍘熷洜锛?*
1. Zotero 7 鐨勬湰鍦?API 璺緞涓嶆槸 `/api/2/items`
2. 闇€瑕佺壒瀹氱殑璇锋眰澶存垨鍙傛暟
3. Zotero 7 鏈湴 API 浣跨敤鐨勬槸涓嶅悓鐨勫崗璁?
---

## 馃敡 Zotero 7 鏈湴 API 璁剧疆

### 1. 寮€鍚湰鍦?API 鏈嶅姟

鍦?Zotero 7 涓細
1. 鐐瑰嚮 **缂栬緫** 鈫?**棣栭€夐」**锛圗dit 鈫?Preferences锛?2. 閫夋嫨 **楂樼骇**锛圓dvanced锛夋爣绛?3. 鎵惧埌 **鏈湴 API 鏈嶅姟**锛圠ocal API service锛?4. 鍕鹃€夛細
   - 鉁?鍏佽鍏朵粬搴旂敤绋嬪簭閫氳繃 HTTP 璁块棶 Zotero 鏁版嵁
   - 鉁?鍏佽璇诲啓璁块棶锛堝鏋滈渶瑕佸鍏ユ枃鐚級

### 2. 纭绔彛鍙?
榛樿绔彛锛歚23119`

濡傛灉绔彛琚崰鐢紝Zotero 浼氫娇鐢ㄤ笅涓€涓彲鐢ㄧ鍙ｏ紙23120, 23121...锛?
### 3. 娴嬭瘯 API 璁块棶

浣跨敤娴忚鍣ㄨ闂細
```
http://localhost:23119/api/2/items?limit=5
```

鎴栦娇鐢?curl锛?```bash
curl http://localhost:23119/api/2/items?limit=5
```

---

## 馃摉 Zotero 7 API 鏂囨。

瀹樻柟鏂囨。锛歨ttps://www.zotero.org/support/dev/web_api/v3/start

**娉ㄦ剰锛?* Zotero 7 鏈湴 API 浣跨敤鐨勬槸 **Web API v3**锛屼笉鏄?v2锛?
### 姝ｇ‘鐨?API 璺緞

```
http://localhost:23119/api/3/items?key=your_api_key
```

鎴栵紙鏈湴 API 鍙兘涓嶉渶瑕?key锛夛細
```
http://localhost:23119/api/3/items
```

### API 绔偣

| 绔偣 | 璇存槑 |
|------|------|
| `/api/3/items` | 鑾峰彇鏂囩尞鍒楄〃 |
| `/api/3/items/{itemKey}` | 鑾峰彇鍗曠瘒鏂囩尞 |
| `/api/3/collections` | 鑾峰彇鍒嗙被鍒楄〃 |
| `/api/3/tags` | 鑾峰彇鏍囩鍒楄〃 |

### 璇锋眰鍙傛暟

| 鍙傛暟 | 璇存槑 | 绀轰緥 |
|------|------|------|
| `limit` | 杩斿洖鏁伴噺闄愬埗 | `limit=10` |
| `q` | 鎼滅储鍏抽敭璇?| `q=RTHS` |
| `sort` | 鎺掑簭瀛楁 | `sort=title` |
| `direction` | 鎺掑簭鏂瑰悜 | `direction=asc` |
| `key` | API Key锛堟湰鍦?API 鍙兘涓嶉渶瑕侊級 | `key=xxx` |

---

## 馃洜锔?鎶€鑳介厤缃洿鏂?
### 浣跨敤鏈湴 API

```bash
cd skills/zotero-manager

# 浣跨敤 API v3
python zotero_search.py --local --api-url "http://localhost:23119/api/3" -q "RTHS"
```

### 浣跨敤杩滅▼ API

```bash
# 閰嶇疆 API Key
echo "your_api_key" > ~/.config/zotero/api_key

# 鎼滅储
python zotero_search.py -q "RTHS" -l 10
```

---

## 馃攳 璇婃柇宸ュ叿

杩愯璇婃柇鑴氭湰妫€鏌?API 杩炴帴锛?
```bash
cd skills/zotero-manager
python zotero_diagnose.py
```

璇婃柇鍐呭锛?- 妫€鏌ョ鍙?23119 鏄惁寮€鏀?- 妫€鏌?API 绔偣鏄惁鍙敤
- 杩斿洖姝ｇ‘鐨?API 鍩虹 URL

---

## 鈿狅笍 甯歌闂

### Q1: 杩炴帴琚嫆缁?**A:** Zotero 鏈惎鍔ㄦ垨鏈湴 API 鏈嶅姟鏈紑鍚?
### Q2: 404 閿欒
**A:** API 璺緞閿欒锛屼娇鐢?`/api/3/` 鑰屼笉鏄?`/api/2/`

### Q3: 杩斿洖绌虹粨鏋?**A:** 鏂囩尞搴撲腑娌℃湁鍖归厤鐨勬枃鐚紝鎴栨悳绱㈠叧閿瘝涓嶅

### Q4: 闇€瑕?API Key 鍚楋紵
**A:** 鏈湴 API锛坙ocalhost锛夐€氬父涓嶉渶瑕侊紝杩滅▼ API 闇€瑕?
---

## 馃摓 涓嬩竴姝?
1. **纭 Zotero 7 宸插惎鍔?*
2. **寮€鍚湰鍦?API 鏈嶅姟**锛堢紪杈戔啋棣栭€夐」鈫掗珮绾э級
3. **杩愯璇婃柇宸ュ叿**锛歚python zotero_diagnose.py`
4. **娴嬭瘯鎼滅储**锛歚python zotero_search.py --local -q "RTHS"`

---

**澶囨敞锛?* Zotero 7 鏈湴 API 鏂囨。鍙兘涓嶅畬鏁达紝濡傞亣闂璇峰弬鑰冨畼鏂硅鍧涙垨 GitHub銆?
