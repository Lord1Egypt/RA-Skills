# Zotero 鏈湴 API 蹇€熼厤缃?
**鐘舵€侊細** 鈿狅笍 闇€瑕佽璇?
---

## 馃攳 娴嬭瘯缁撴灉

```
http://localhost:23119/api/ 鈫?403 Forbidden
```

**璇存槑锛?* Zotero 鏈湴 API 闇€瑕佽璇侊紝鍗充娇鏄湰鍦拌闂€?
---

## 馃攽 鑾峰彇鏈湴 API 瀵嗛挜

### 鏂规硶 1锛氫粠 Zotero 璁剧疆涓幏鍙?
1. 鎵撳紑 Zotero 7
2. **缂栬緫** 鈫?**棣栭€夐」** 鈫?**楂樼骇** 鈫?**鏈湴 API 鏈嶅姟**
3. 鏌ョ湅 **API 瀵嗛挜** 瀛楁
4. 澶嶅埗瀵嗛挜锛堜竴涓插瓧姣嶆暟瀛楋級

### 鏂规硶 2锛氭煡鐪?Zotero 閰嶇疆鏂囦欢

瀵嗛挜瀛樺偍鍦細
```
%APPDATA%\Zotero\Zotero\prefs.js
```

鏌ユ壘锛?```javascript
user_pref("extensions.zotero.httpServer.auth.token", "浣犵殑瀵嗛挜");
```

---

## 鈿欙笍 閰嶇疆鎶€鑳?
### 淇濆瓨瀵嗛挜

```bash
mkdir -p D:\Personal\OpenClaw\.config\zotero
echo "浣犵殑鏈湴 API 瀵嗛挜" > D:\Personal\OpenClaw\.config\zotero\local_api_key
```

### 娴嬭瘯杩炴帴

```bash
cd skills/zotero-manager
python zotero_search.py --local -q "RTHS" -l 5
```

鎶€鑳戒細鑷姩锛?1. 璇诲彇鏈湴 API 瀵嗛挜
2. 娣诲姞鍒拌姹傚ご
3. 杩斿洖鎼滅储缁撴灉

---

## 馃敡 鏇存柊鍚庣殑鎶€鑳?
`zotero_search.py` 宸叉洿鏂帮紝鏀寔锛?- 鉁?鑷姩璇诲彇鏈湴 API 瀵嗛挜
- 鉁?娣诲姞鍒?`Authorization` 璇锋眰澶?- 鉁?浣跨敤 API v3 绔偣

---

## 馃摉 API 绔偣鍙傝€?
| 绔偣 | 璇存槑 |
|------|------|
| `/api/3/items` | 鏂囩尞鍒楄〃 |
| `/api/3/items/{key}` | 鍗曠瘒鏂囩尞 |
| `/api/3/collections` | 鍒嗙被鍒楄〃 |
| `/api/3/tags` | 鏍囩鍒楄〃 |

---

## 馃挕 涓嬩竴姝?
1. **浠?Zotero 鑾峰彇 API 瀵嗛挜**
2. **淇濆瓨鍒伴厤缃枃浠?*
3. **杩愯鎼滅储娴嬭瘯**

---

**鎻愮ず锛?* 鏈湴 API 瀵嗛挜涓庤繙绋?API 瀵嗛挜涓嶅悓锛屼笉瑕佹贩娣嗭紒

