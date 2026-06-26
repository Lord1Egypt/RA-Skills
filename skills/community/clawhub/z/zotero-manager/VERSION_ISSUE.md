# Zotero 鏈湴 API 瀵嗛挜 - 鐗堟湰闂瑙ｅ喅鏂规

**闂锛?* Zotero 鐣岄潰娌℃壘鍒扮敓鎴?API 瀵嗛挜鐨勯〉闈?
---

## 馃攳 鍙兘鍘熷洜

### 1. Zotero 鐗堟湰澶棫

**鏈湴 API 鏈嶅姟鏄?Zotero 7 鐨勬柊鍔熻兘**

- Zotero 6.x 鈫?鉂?娌℃湁鏈湴 API
- Zotero 7.0+ 鈫?鉁?鏈夋湰鍦?API

### 2. 鏈湴 API 鏈嶅姟鏈惎鐢?
鍗充娇 Zotero 7锛屼篃闇€瑕佹墜鍔ㄥ紑鍚€?
---

## 鉁?瑙ｅ喅鏂规

### 鏂规 A锛氭鏌?Zotero 鐗堟湰

1. 鎵撳紑 Zotero
2. **甯姪** 鈫?**鍏充簬 Zotero**
3. 鏌ョ湅鐗堟湰鍙?
**濡傛灉鏄?6.x锛?*
- 闇€瑕佸崌绾у埌 Zotero 7
- 涓嬭浇鍦板潃锛歨ttps://www.zotero.org/download/

**濡傛灉鏄?7.0+锛?*
- 缁х画涓嬮潰鐨勬楠?
---

### 鏂规 B锛氫娇鐢ㄨ繙绋?API锛堟棤闇€鏈湴 API锛?
**濡傛灉鏈湴 API 鏈夐棶棰橈紝鍙互浣跨敤杩滅▼ API锛?*

1. 璁块棶锛歨ttps://www.zotero.org/settings/keys
2. 鐐瑰嚮 **"Create a new personal access token"**
3. 鍕鹃€夋潈闄愶細**Read Library**
4. 澶嶅埗 API Key
5. 淇濆瓨锛?   ```bash
   mkdir -p D:\Personal\OpenClaw\.config\zotero
   echo "浣犵殑 API Key" > D:\Personal\OpenClaw\.config\zotero\api_key
   ```
6. 娴嬭瘯锛?   ```bash
   python zotero_search.py -q "RTHS" -l 10
   ```

**浼樼偣锛?*
- 涓嶉渶瑕?Zotero 7
- 涓嶉渶瑕?Zotero 杩愯
- 鏇寸ǔ瀹?
**缂虹偣锛?*
- 闇€瑕佺綉缁?- 鏈?API 璋冪敤闄愬埗锛堟瘡鍒嗛挓绾?50 娆★級

---

### 鏂规 C锛氭墜鍔ㄦ煡鎵鹃厤缃紙楂樼骇锛?
濡傛灉纭畾鏄?Zotero 7锛屼絾鐣岄潰娌℃樉绀猴細

1. 鍏抽棴 Zotero
2. 鎵惧埌閰嶇疆鐩綍锛?   ```bash
   # 杩愯杩欎釜鍛戒护
   echo $env:APPDATA
   ```
3. 瀵艰埅鍒帮細`C:\Users\[USERNAME]\Roaming\Zotero\`
4. 鏌ユ壘鏂囦欢锛?   - `prefs.js`
   - `zotero.cfg`
5. 鐢ㄨ浜嬫湰鎵撳紑锛屾悳绱細
   - `api.key`
   - `httpServer.auth`

---

### 鏂规 D锛氫娇鐢?Web 搴擄紙鏈€绠€鍗曪級

**濡傛灉鍙槸鎯崇鐞嗘枃鐚紝涓嶉渶瑕佹湰鍦?API锛?*

1. 璁块棶锛歨ttps://www.zotero.org/
2. 鐧诲綍浣犵殑璐﹀彿
3. 鐩存帴浣跨敤 Web 鐗?Zotero
4. 鎶€鑳藉彲浠ラ€氳繃杩滅▼ API 璁块棶

---

## 馃洜锔?鎺ㄨ崘鏂规

**瀵逛簬澶у鏁扮敤鎴凤細**

鉁?**浣跨敤杩滅▼ API**锛堟柟妗?B锛?
鍘熷洜锛?- 绠€鍗曪紝涓嶉渶瑕侀厤缃湰鍦版湇鍔?- 绋冲畾锛屼笉鍙?Zotero 杩愯鐘舵€佸奖鍝?- 瀹夊叏锛屽彧鏈変綘鑳借闂嚜宸辩殑搴?
---

## 馃摓 涓嬩竴姝?
**璇烽€夋嫨锛?*

1. **浣跨敤杩滅▼ API** 鈫?鍘?https://www.zotero.org/settings/keys 鐢熸垚瀵嗛挜
2. **鍗囩骇 Zotero** 鈫?涓嬭浇 Zotero 7锛岀劧鍚庡紑鍚湰鍦?API
3. **缁х画鎺掓煡** 鈫?鍛婅瘔鎴戜綘鐨?Zotero 鐗堟湰鍙?
---

**鎻愮ず锛?* 杩滅▼ API 鍜屾湰鍦?API 鍙互鍏卞瓨锛屾妧鑳戒細鑷姩閫夋嫨鍙敤鐨勬柟寮忋€?
