# Zotero 8.04 鏈湴 API 閰嶇疆鎸囧崡

**鐗堟湰锛?* Zotero 8.04  
**鏃ユ湡锛?* 2026 骞?3 鏈?26 鏃?
---

## 馃攳 闂鍒嗘瀽

Zotero 8.04 鏄渶鏂扮増鏈紝鏈湴 API 閰嶇疆鏂瑰紡鍙兘鏈夊彉鍖栵細

1. **绔彛鍙兘涓嶅悓** - 涓嶄竴瀹氭槸 23119
2. **API 璺緞鍙兘涓嶅悓** - 涓嶄竴瀹氭槸 `/api/3/items`
3. **璁よ瘉鏂瑰紡鍙兘涓嶅悓** - 鍙兘闇€瑕佹柊鐨勮璇佹柟寮?
---

## 馃洜锔?瑙ｅ喅鏂规

### 鏂规 1锛氭鏌?Zotero 8 璁剧疆

1. 鎵撳紑 **Zotero 8**
2. **缂栬緫** 鈫?**棣栭€夐」**
3. 鏌ユ壘浠ヤ笅鏍囩锛?   - **楂樼骇** 鈫?**鏈湴 API 鏈嶅姟**
   - **鍚屾** 鈫?**API 璁剧疆**
   - **缃戠粶鏈嶅姟** 鈫?**鏈湴鏈嶅姟**

4. 鏌ョ湅锛?   - 绔彛鍙锋槸澶氬皯锛?   - API 瀵嗛挜鍦ㄥ摢閲岋紵
   - 鏄惁闇€瑕佹墜鍔ㄥ惎鐢紵

---

### 鏂规 2锛氫娇鐢ㄨ繙绋?API锛堟帹鑽愶級

**鏈€绠€鍗曘€佹渶绋冲畾锛?*

1. 璁块棶锛歨ttps://www.zotero.org/settings/keys
2. 鐐瑰嚮 **"Create a new personal access token"**
3. 鍕鹃€夛細**Read Library**
4. 澶嶅埗 API Key
5. 淇濆瓨锛?   ```bash
   mkdir -p D:\Personal\OpenClaw\.config\zotero
   echo "浣犵殑 API Key" > D:\Personal\OpenClaw\.config\zotero\api_key
   ```
6. 娴嬭瘯锛?   ```bash
   python zotero_search.py -q "RTHS" -l 10
   ```

---

### 鏂规 3锛氭煡鎵?Zotero 8 閰嶇疆

杩愯 PowerShell 鍛戒护鏌ユ壘閰嶇疆锛?
```powershell
# 鏌ユ壘 Zotero 8 閰嶇疆鏂囦欢
Get-ChildItem -Path "$env:APPDATA\Zotero" -Recurse -Filter "*.json" | 
  Select-Object FullName

# 鏌ユ壘鍖呭惈 API 鐨勯厤缃?Get-ChildItem -Path "$env:APPDATA\Zotero" -Recurse -Filter "*config*" | 
  Select-Object FullName
```

---

### 鏂规 4锛氭鏌?Zotero 8 绔彛

```powershell
# 鏌ョ湅 Zotero 鍗犵敤鐨勭鍙?Get-NetTCPConnection -OwningProcess (Get-Process zotero).Id | 
  Select-Object LocalPort, State
```

---

## 馃摉 Zotero 8 鏂扮壒鎬?
Zotero 8 鍙兘浣跨敤浜嗘柊鐨?API 鏋舵瀯锛?
- **鍙兘鏄?GraphQL API** 鑰屼笉鏄?REST
- **鍙兘鏄?WebSocket** 鑰屼笉鏄?HTTP
- **绔彛鍙兘闅忔満鍒嗛厤**

---

## 馃幆 鎺ㄨ崘鏂规

**瀵逛簬 Zotero 8.04 鐢ㄦ埛锛?*

鉁?**浣跨敤杩滅▼ API**锛堟柟妗?2锛?
鍘熷洜锛?- Zotero 8 澶柊锛屾湰鍦?API 鏂囨。鍙兘涓嶅畬鏁?- 杩滅▼ API 绋冲畾銆佺畝鍗?- 鍔熻兘瀹屽叏涓€鏍?
---

## 馃摓 涓嬩竴姝?
**璇烽€夋嫨锛?*

1. **浣跨敤杩滅▼ API** 鈫?https://www.zotero.org/settings/keys
2. **缁х画鎺掓煡鏈湴 API** 鈫?鍛婅瘔鎴?Zotero 8 鐨勮缃晫闈㈡埅鍥?3. **绛夊緟鎶€鑳芥洿鏂?* 鈫?鎴戜細鐮旂┒ Zotero 8 鐨?API 瑙勮寖

---

**鎻愮ず锛?* Zotero 8 鏄?2026 骞寸殑鏂扮増鏈紝寰堝鎶€鑳藉彲鑳介渶瑕侀€傞厤锛?
