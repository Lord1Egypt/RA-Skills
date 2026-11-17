--
name: domain-kit
description: "Access department domain knowledge - PLC models, coding standards, code templates, device parameters"
tags: [domain-specific, data, file-based, memory-based, cli]
version: "1.0.0"
---

# Domain-Knowledge Toolkit

閮ㄩ棬棰嗗煙鐭ヨ瘑寤烘ā + LLM 涓婁笅鏂囧寮哄伐鍏枫€傚皢璁惧鎵嬪唽銆佷唬鐮佹ā鏉裤€佺紪鐮佽鑼冪瓑鐭ヨ瘑缁撴瀯鍖栧瓨鍌紝锟?agent 鎵ц浠诲姟鏃剁簿鍑嗘绱㈠苟娉ㄥ叆鐩稿叧涓婁笅鏂囷拷?
## 浣跨敤鍦烘櫙

褰撻渶瑕佷互涓嬩换鍔℃椂锛岃皟鐢ㄦ skill锟?- 鐢熸垚璁惧鎺у埗浠ｇ爜锛圥LC/ST/LD/FBD锟?- 杩涜璁惧閫夊瀷锛圥LC/I/O 妯″潡/WCS 璁惧/瑙嗚纭欢锟?- 鏌ヨ鎶€鏈鑼冿紙缂栫爜瑙勮寖/绾︽潫瑙勫垯/閫氫俊鍗忚锟?- 鍙傝€冨巻鍙叉渶浣冲疄锟?
## 璋冪敤鏂瑰紡

### 鏌ヨ鐭ヨ瘑

```bash
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\domain-kit\cli.py query "AM600 杈撻€佸甫鎺у埗浠ｇ爜鐢熸垚"
```

杩斿洖 Markdown 鏍煎紡锛屽寘鍚細
- 璁惧绾︽潫锛圕onstraints锟?- 浠ｇ爜妯℃澘锛圕odeTemplate锟?- 鏈€浣冲疄璺碉紙BestPractice锟?- 鍏宠仈瀹炰綋锛堥€氳繃 relations 杩芥函锟?
### 鐭ヨ瘑缁熻

```bash
python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\domain-kit\cli.py stats
```

### 鐭ヨ瘑褰曞叆

```bash
# 浠庢枃妗ｆ彁锟?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\domain-kit\cli.py extract --file docs/AM600_manual.pdf --type doc

# 浠庝唬鐮佹彁锟?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\domain-kit\cli.py extract --file templates/conveyor.st --type code

# 浠庤〃鏍兼彁锟?python D:\Users\yindb2\AppData\Roaming\mx\openclaw-home\yindb2\.openclaw\workspace\skills\domain-kit\cli.py extract --file io_config.xlsx --type table
```

## 鐭ヨ瘑鏉ユ簮

- 璁惧鎶€鏈墜鍐岋紙PDF/Markdown锟?- 鍘嗗彶浠ｇ爜妯℃澘锛坰t 鏂囦欢锟?- 鍥㈤槦瑙勮寖鏂囨。
- I/O 閰嶇疆琛紙Excel/CSV锟?
## 娉ㄦ剰浜嬮」

- 鏌ヨ缁撴灉鎸夌疆淇″害锛坈onfidence锛夐檷搴忔帓锟?- 浠呮敞锟?confidence 锟?0.7 鐨勭煡锟?- 鐭ヨ瘑鐗堟湰鏇存柊鍚庯紝鏃х増鏈繚鐣欙紝鏌ヨ鏃跺彇鏈€鏂扮増
- 涓庣幇锟?ontology 绯荤粺鍏卞瓨锛歰ntology 瀛橀」锟?浜哄憳锛堝姩鎬侊級锛宒omain-kit 瀛橀鍩熺煡璇嗭紙闈欐€侊級

## 涓変釜涓氬姟鏂瑰悜

1. **鑷姩鍖栬锟?*锛坅utomation锛夛細PLC 鍨嬪彿鐗规€с€佺紪鐮佽鑼冦€佷唬鐮佹ā鏉裤€両/O 閰嶇疆
2. **鐗╂祦 WCS**锛坵cs锛夛細璁惧绫诲瀷銆佹帴鍙ｅ崗璁€佽皟搴﹁鍒欍€佸巻鍙叉柟锟?3. **宸ヤ笟瑙嗚**锛坴ision锛夛細缂洪櫡绫诲瀷銆佺畻娉曟ā鍨嬨€佺‖浠堕厤缃€佹娴嬫爣锟?