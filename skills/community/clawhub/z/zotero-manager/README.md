# Zotero Manager 鎶€鑳?
**鐗堟湰锛?* v0.2  
**鍒涘缓鏃堕棿锛?* 2026 骞?3 鏈?26 鏃? 
**鐘舵€侊細** 馃攧 寮€鍙戜腑

---

## 馃摎 鍔熻兘

- 鉁?鏂囩尞鎼滅储锛堟寜鍏抽敭璇?鍒嗙被锛?- 鉁?鏂囩尞瀵煎叆锛圖OI锛?- 鉁?鏈湴 API 鏀寔锛圸otero 7锛?- 鈴?鍒嗙被绠＄悊
- 鈴?鍙傝€冩枃鐚鍑?
---

## 馃殌 蹇€熷紑濮?
### 鏂瑰紡 1锛氫娇鐢?Zotero 7 鏈湴 API锛堟帹鑽愶級

**鍓嶆彁锛?* Zotero 7 宸插畨瑁呭苟杩愯

1. 寮€鍚湰鍦?API 鏈嶅姟锛?   - 缂栬緫 鈫?棣栭€夐」 鈫?楂樼骇 鈫?鏈湴 API 鏈嶅姟
   - 鍕鹃€?鍏佽鍏朵粬搴旂敤绋嬪簭閫氳繃 HTTP 璁块棶 Zotero 鏁版嵁"

2. 娴嬭瘯杩炴帴锛?```bash
cd skills/zotero-manager
python zotero_diagnose.py
```

3. 鎼滅储鏂囩尞锛?```bash
python zotero_search.py --local --api-url "http://localhost:23119/api/3" -q "RTHS" -l 10
```

### 鏂瑰紡 2锛氫娇鐢ㄨ繙绋?API

**鍓嶆彁锛?* 闇€瑕?Zotero API Key

1. 鑾峰彇 API Key: https://www.zotero.org/settings/keys
2. 鐐瑰嚮 "Create a new personal access token"
3. 鍕鹃€夋潈闄愶細**Read Library**
4. 閰嶇疆 API Key锛?```bash
mkdir -p D:\Personal\OpenClaw\.config\zotero
echo "浣犵殑 API Key" > D:\Personal\OpenClaw\.config\zotero\api_key
```

5. 鎼滅储鏂囩尞锛?```bash
python zotero_search.py -q "RTHS" -l 10
```

---

## 馃摉 浣跨敤绀轰緥

### 鎼滅储鏂囩尞

```bash
# 鍏抽敭璇嶆悳绱?python zotero_search.py -q "鎸姩鍙版帶鍒? -l 10

# 鍒嗙被鎼滅储
python zotero_search.py -c "02-RTHS" -l 5

# JSON 杈撳嚭
python zotero_search.py -q "NTMD" --json
```

### 瀵煎叆鏂囩尞

```bash
# 鍗曠瘒 DOI 瀵煎叆
python zotero_import.py --doi "10.1016/j.engstruct.2024.117123"

# 鎵归噺瀵煎叆
python zotero_import.py --doi-list dois.txt -c "01-ShakeTable"
```

---

## 馃搧 鏂囦欢缁撴瀯

```
skills/zotero-manager/
鈹溾攢鈹€ SKILL.md                 # 鎶€鑳藉畾涔?鈹溾攢鈹€ README.md                # 浣跨敤璇存槑锛堟湰鏂囦欢锛?鈹溾攢鈹€ zotero_search.py         # 鏂囩尞鎼滅储
鈹溾攢鈹€ zotero_import.py         # 鏂囩尞瀵煎叆
鈹溾攢鈹€ zotero_collections.py    # 鍒嗙被绠＄悊锛堝緟寮€鍙戯級
鈹斺攢鈹€ zotero_export.py         # 鍙傝€冩枃鐚鍑猴紙寰呭紑鍙戯級
```

---

## 馃敡 寰呭紑鍙戝姛鑳?
- [ ] `zotero_collections.py` - 鍒嗙被绠＄悊
  - 鍒涘缓鍒嗙被
  - 鍒楀嚭鎵€鏈夊垎绫?  - 鍒嗙被閲嶅懡鍚?
- [ ] `zotero_export.py` - 鍙傝€冩枃鐚鍑?  - 瀵煎嚭 BibTeX
  - 瀵煎嚭 EndNote
  - 瀵煎嚭绾枃鏈?
- [ ] 閰嶇疆浼樺寲
  - 鑷姩鑾峰彇 UserID
  - 閰嶇疆鏂囦欢璺緞鑷畾涔?
---

## 馃搳 鐮旂┒鏂瑰悜鍒嗙被

| 缂栧彿 | 鐮旂┒鏂瑰悜 | Zotero 鍒嗙被鍚?|
|------|----------|--------------|
| 01 | 鎸姩鍙版帶鍒舵妧鏈?| 01-ShakeTable |
| 02 | RTHS 瀛愮粨鏋勮瘯楠?| 02-RTHS |
| 03 | 鏂囩墿闅旈渿 | 03-Heritage |
| 04 | 绮夋湯闃诲凹 | 04-Powder |
| 05 | 瓒呮潗鏂欓殧闇?| 05-Metamaterial |
| 06 | NTMD 鍑忔尟 | 06-NTMD |
| 07 | 鍦伴渿棰勬祴 | 07-Prediction |
| 08 | 鐖嗙牬妯℃嫙鍦伴渿 | 08-Blasting |
| 09 | 瀹為獙瀹ょ鐞?| 09-Lab |
| 10 | 鐮旂┒鐢熷煿鍏?| 10-Training |

---

## 馃攼 瀹夊叏璇存槑

- API Key 浠呭彂閫佸埌 `api.zotero.org`
- 涓嶈褰曘€佷笉瀛樺偍鍑瘉
- 鍙鏉冮檺锛屼笉淇敼鏂囩尞

---

## 馃摓 闂鍙嶉

閬囧埌闂璇锋鏌ワ細
1. API Key 鏄惁姝ｇ‘
2. 缃戠粶杩炴帴鏄惁姝ｅ父
3. Zotero 搴撴槸鍚﹀彲璁块棶

---

**涓嬩竴姝ワ細** 寮€鍙?obsidian-manager 鎶€鑳?
