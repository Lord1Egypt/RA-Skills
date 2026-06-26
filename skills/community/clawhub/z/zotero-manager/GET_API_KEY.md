# 鑾峰彇 Zotero 鏈湴 API 瀵嗛挜锛堟渶绠€鍗曟柟娉曪級

**鏃堕棿锛?* 2026 骞?3 鏈?26 鏃? 
**閫傜敤锛?* Zotero 7.x

---

## 馃攽 鏂规硶 1锛氫粠 Zotero 鐣岄潰鑾峰彇锛堟帹鑽愶級

### 姝ラ锛?
1. **鎵撳紑 Zotero 7**

2. **杩涘叆璁剧疆**
   - Windows: **缂栬緫** 鈫?**棣栭€夐」**
   - Mac: **Zotero** 鈫?**棣栭€夐」**

3. **鎵惧埌鏈湴 API 璁剧疆**
   - 鐐瑰嚮 **楂樼骇** 鏍囩
   - 鎵惧埌 **鏈湴 API 鏈嶅姟** 閮ㄥ垎

4. **鏌ョ湅/鐢熸垚瀵嗛挜**
   - 濡傛灉鐪嬪埌 **API 瀵嗛挜** 瀛楁锛岀洿鎺ュ鍒?   - 濡傛灉鏄剧ず"鏈敓鎴?锛岀偣鍑?**鐢熸垚鏂板瘑閽?* 鎸夐挳

5. **淇濆瓨瀵嗛挜**
   ```bash
   mkdir -p D:\Personal\OpenClaw\.config\zotero
   echo "澶嶅埗鐨勫瘑閽? > D:\Personal\OpenClaw\.config\zotero\local_api_key
   ```

---

## 馃攳 鏂规硶 2锛氭鏌?Zotero 鏄惁杩愯

```bash
# Windows 浠诲姟绠＄悊鍣ㄦ煡鐪?Get-Process | Where-Object {$_.Name -like "*zotero*"}
```

濡傛灉 Zotero 娌¤繍琛岋紝鍏堝惎鍔ㄥ畠锛?
---

## 馃搷 鏂规硶 3锛氭煡鎵鹃厤缃洰褰?
杩愯杩欎釜鍛戒护鎵惧埌 Zotero 鏁版嵁鐩綍锛?
```bash
# PowerShell
$env:APPDATA
```

鐒跺悗鎵嬪姩瀵艰埅鍒帮細
```
C:\Users\[USERNAME]\Roaming\Zotero\
```

鐪嬬湅鏈夋病鏈夎繖浜涙枃浠跺す锛?- `Zotero/`
- `prefs.js`
- `zotero.cfg`

---

## 馃洜锔?鏂规硶 4锛氫娇鐢ㄦ妧鑳借瘖鏂?
```bash
cd skills/zotero-manager
python zotero_diagnose.py
```

杩欎釜浼氭鏌ワ細
- Zotero 鏄惁鍦ㄨ繍琛?- 绔彛 23119 鏄惁寮€鏀?- API 鏄惁闇€瑕佽璇?
---

## 鈿狅笍 濡傛灉杩樻槸鎵句笉鍒?
**鍙兘鍘熷洜锛?*
1. Zotero 7 杩樻病寮€鍚湰鍦?API 鏈嶅姟
2. Zotero 鐗堟湰澶棫锛堥渶瑕?7.0+锛?3. 閰嶇疆鏂囦欢鍦ㄥ叾浠栦綅缃?
**瑙ｅ喅鏂规锛?*
1. 鎵撳紑 Zotero 7
2. 缂栬緫 鈫?棣栭€夐」 鈫?楂樼骇 鈫?鏈湴 API 鏈嶅姟
3. 鍕鹃€?鍏佽鍏朵粬搴旂敤绋嬪簭閫氳繃 HTTP 璁块棶 Zotero 鏁版嵁"
4. 鐐瑰嚮"鐢熸垚鏂板瘑閽?锛堝鏋滈渶瑕侊級
5. 澶嶅埗鏄剧ず鐨勫瘑閽?
---

## 馃摓 涓嬩竴姝?
**鑾峰彇瀵嗛挜鍚庯細**

1. 淇濆瓨鍒伴厤缃枃浠讹細
```bash
echo "浣犵殑瀵嗛挜" > D:\Personal\OpenClaw\.config\zotero\local_api_key
```

2. 娴嬭瘯鎼滅储锛?```bash
python zotero_search.py --local -q "RTHS" -l 5
```

---

**鎻愮ず锛?* 瀵嗛挜鏄竴涓插瓧姣嶆暟瀛楋紝绫讳技 `abc123def456ghi789...`

