# 釋迦牟尼佛經典語錄 — 多國語系 JSON 使用說明

> 檔案：`sakyamuni-quotes-18lang.json`　|　版本 v1.2　|　2026-08-09

## 一、設計原則

**回覆規則（核心）**：
> 當 Agent 回覆他人語錄時：
> 1. **先顯示該讀者使用語系**的翻譯版本
> 2. **下方顯示繁體中文原文**（原文版本）
>
> 若讀者語系即為繁體中文，則只顯示一次，不重複。

## 二、資料結構

```json
{
  "schema": "sakyamuni-quotes.v1",
  "meta": {
    "languages": ["zh-Hant","zh-Hans","en","ja","ko","th","my","pi","sa","bo","vi","si","km","lo","id","hi","mn","fr","ru"],
    "language_names": { "zh-Hant": "繁體中文", "en": "English", ... }
  },
  "quotes": [
    {
      "id": "dhp-183",
      "tags": ["戒","倫理","總綱","ethics"],
      "source": { "zh-Hant": "《法句經》第183偈", "en": "Dhammapada, verse 183", "pi": "Dhammapada 183" },
      "pali": "Sabbapāpassa akaraṇaṃ...",        // 巴利原文（若有）
      "text": {
        "zh-Hant": "諸惡莫作，眾善奉行，自淨其意，是諸佛教。",
        "zh-Hans": "...", "en": "...", "ja": "...", ...  // 19 語言
      },
      "explanation": {
        "zhHant": { "plain": "...", "story": "...", "tip": "..." },  // 白話解釋（繁中原文）
        "en": { "plain": "...", "story": "...", "tip": "..." },      // 18 語言翻譯
        ...  // 共 19 語言
      },
      "notes": { "zh-Hant": "...", "en": "..." }  // 可選：版本註記（如大乘經典無巴利對應）
    }
  ]
}
```

> 鍵名注意：`text`/`source` 使用 `zh-Hant`（連字號）；`explanation` 使用 `zhHant`（無連字號）。

## 三、19 語言清單

| Code | 語言 | Code | 語言 |
|------|------|------|------|
| zh-Hant | 繁體中文（原文） | vi | Tiếng Việt |
| zh-Hans | 简体中文 | si | සිංහල |
| en | English | km | ខ្មែរ |
| ja | 日本語 | lo | ລາວ |
| ko | 한국어 | id | Bahasa Indonesia |
| th | ไทย | hi | हिन्दी |
| my | မြန်မာ | mn | Монгол |
| pi | Pāli | fr | Français |
| sa | संस्कृतम् | ru | Русский |
| bo | བོད་ཡིག | | |

## 四、收錄語錄（20 則）

### 基礎 12 則

| id | 出處 | 主題 |
|----|------|------|
| dhp-183 | 《法句經》第183偈 | 諸惡莫作，眾善奉行，自淨其意 |
| dhp-001 | 《法句經》第1偈 | 諸法意先導（心為一切之本） |
| dhp-005 | 《法句經》第5偈 | 怨恨不能止息怨恨，唯有慈悲 |
| vajra-32 | 《金剛經》末偈 | 一切有為法，如夢幻泡影 |
| paticca-001 | 《相應部》12.61／中阿含 | 此有故彼有，此生故彼生（緣起） |
| dn-016 | 《長部・大般涅槃經》 | 自熾燃、自歸依（自依止） |
| metta-001 | 《小部・慈經》 | 慈心遍滿（慈經偈頌） |
| mangala-001 | 《小部・吉祥經》 | 眾吉祥事 |
| heart-010 | 《般若心經》 | 色即是空 |
| dhp-021 | 《法句經》第21偈 | 不放逸是不死之道 |
| dhp-204 | 《法句經》第204偈 | 無病最上利，知足最上財 |
| dhp-223 | 《法句經》第223偈 | 以無瞋勝瞋恚 |

### 擴充 8 則（v1.2 新增，三法印＋修行＋涅槃＋業報）

| id | 出處 | 主題 |
|----|------|------|
| anicca-001 | 《法句經》第277偈 | 諸行無常（無常） |
| dukkha-001 | 《法句經》第278偈 | 諸行是苦（苦） |
| anatta-001 | 《法句經》第279偈 | 諸法無我（無我） |
| dana-001 | 《法句經》第177偈 | 布施 |
| samadhi-001 | 《法句經》心品 | 禪定 |
| sati-001 | 《法句經》不放逸品 | 正念 |
| nibbana-001 | 《法句經》第203偈 | 涅槃 |
| kamma-001 | 《法句經》第127偈 | 業報 |

> 附註：vajra-32、heart-010 為大乘經典（梵文），巴利藏無對應，故 `pali` 與 `pi` 欄位以 `"—"` 標示；`sa` 欄位仍提供梵文。

## 五、回覆格式範例（Agent 行為）

### 範例 1：讀者使用英文
```
[English]
"Not to do any evil, to cultivate good, to purify one's own mind — this is the teaching of the Buddhas."
— Dhammapada, verse 183

【原文】
諸惡莫作，眾善奉行，自淨其意，是諸佛教。
——《法句經》第183偈
```

### 範例 2：讀者使用日文
```
[日本語]
「諸悪なすことなかれ、諸善奉行せよ、自ら心を浄くせよ、これすなわち諸仏の教えなり。」
— 『法句経』第183偈

【原文】
諸惡莫作，眾善奉行，自淨其意，是諸佛教。
——《法句經》第183偈
```

### 範例 3：讀者使用繁體中文（不重複）
```
諸惡莫作，眾善奉行，自淨其意，是諸佛教。
——《法句經》第183偈
```

## 六、Agent 呼叫邏輯（偽代碼）

```
function respondQuote(userLang, quoteId):
    quote = quotes[quoteId]
    text = quote.text[userLang]
    zhHant = quote.text["zh-Hant"]
    source = quote.source[userLang] 或 quote.source["zh-Hant"]

    if userLang == "zh-Hant":
        print(text)              # 只顯示一次
    else:
        print("[" + langName(userLang) + "]")
        print(text)
        print("")
        print("【原文】")
        print(zhHant)            # 下方顯示繁體中文原文
    print("— " + source)
```

## 七、白話解釋（explanation）

每則語錄均附 `explanation` 欄位，包含三部分，共 19 語言：
- **plain**：一句白話義（現代口語）
- **story**：一個小故事（寓言式，幫助記憶）
- **tip**：一個可實踐的小提示（每日功課）

回覆時可依情境選用：讀者求白話義 → plain；求故事 → story；求實踐 → tip。

## 八、擴充建議

- 語錄可續增至 30+ 則：增加《法句經》各品、慈經（Mettā Sutta）、吉祥經、心經、阿含選段等
- 每則可加 `context` 欄位（當時情境）與 `moral` 欄位（一句話白話義）
- 若需「隨機語錄」功能：Agent 依主題 tag 或隨機選取
- 校對建議：各語言翻譯上線前建議請母語人士複核（尤其 Pāli/Sanskrit/Tibetan 古語）
