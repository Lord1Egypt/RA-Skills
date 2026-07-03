---
name: 文本转换工具
description: 一个提供文本转换、格式化和分析功能的MCP服务器，可直接集成到开发工作流中。
version: 1.0.0
---

# 文本转换工具

一个提供文本转换、格式化和分析功能的MCP服务器，可直接集成到开发工作流中。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Convert text to camelCase | `scripts.tools.case_to_camel` |
| Convert text to PascalCase | `scripts.tools.case_to_pascal` |
| Convert text to snake_case | `scripts.tools.case_to_snake` |
| Convert text to kebab-case | `scripts.tools.case_to_kebab` |
| Convert text to CONSTANT_CASE | `scripts.tools.case_to_constant` |
| Convert text to dot.case | `scripts.tools.case_to_dot` |
| Convert text to no case | `scripts.tools.case_to_no` |
| Convert text to Pascal_Snake_Case | `scripts.tools.case_to_pascal_snake` |
| Convert text to path/case | `scripts.tools.case_to_path` |
| Convert text to Sentence case | `scripts.tools.case_to_sentence` |
| Convert text to Train-Case | `scripts.tools.case_to_train` |
| Convert text to Capital Case | `scripts.tools.case_to_capital` |
| Encode text to Base64 | `scripts.tools.encode_base64` |
| Decode Base64 to text | `scripts.tools.decode_base64` |
| Encode text for URLs | `scripts.tools.encode_url` |
| Decode URL-encoded text | `scripts.tools.decode_url` |
| Encode HTML entities | `scripts.tools.encode_html` |
| Decode HTML entities | `scripts.tools.decode_html` |
| Format and beautify JSON | `scripts.tools.format_json` |
| Format and beautify XML | `scripts.tools.format_xml` |
| Format and beautify SQL | `scripts.tools.format_sql` |
| Format and beautify HTML | `scripts.tools.format_html` |
| Count characters in text | `scripts.tools.count_characters` |
| Count words in text | `scripts.tools.count_words` |
| Count lines in text | `scripts.tools.count_lines` |
| Calculate readability metrics | `scripts.tools.analyze_readability` |
| Trim whitespace from text | `scripts.tools.string_trim` |
| Extract a substring | `scripts.tools.string_substring` |
| Replace text | `scripts.tools.string_replace` |
| Split text into an array | `scripts.tools.string_split` |
| Join an array into text | `scripts.tools.string_join` |
| Generate a UUID | `scripts.tools.generate_uuid` |
| Validate a UUID | `scripts.tools.validate_uuid` |
| Generate MD5 hash | `scripts.tools.generate_md5` |
| Generate SHA-1 hash | `scripts.tools.generate_sha1` |
| Generate SHA-256 hash | `scripts.tools.generate_sha256` |
| Generate SHA-512 hash | `scripts.tools.generate_sha512` |
| Generate HMAC hash | `scripts.tools.generate_hmac` |
| Generate lorem ipsum text | `scripts.tools.generate_lorem_ipsum` |
| Test a regex pattern against text | `scripts.tools.regex_test` |
| Replace text using a regex pattern | `scripts.tools.regex_replace` |
| Extract matches using a regex pattern | `scripts.tools.regex_extract` |
| Split text using a regex pattern | `scripts.tools.regex_split` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.case_to_camel
工具描述：Convert text to camelCase
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to camelCase|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_pascal
工具描述：Convert text to PascalCase
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to PascalCase|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_snake
工具描述：Convert text to snake_case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to snake_case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_kebab
工具描述：Convert text to kebab-case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to kebab-case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_constant
工具描述：Convert text to CONSTANT_CASE
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to CONSTANT_CASE|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_dot
工具描述：Convert text to dot.case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to dot.case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_no
工具描述：Convert text to no case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to no case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_pascal_snake
工具描述：Convert text to Pascal_Snake_Case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to Pascal_Snake_Case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_path
工具描述：Convert text to path/case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to path/case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_sentence
工具描述：Convert text to Sentence case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to Sentence case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_train
工具描述：Convert text to Train-Case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to Train-Case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.case_to_capital
工具描述：Convert text to Capital Case
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to transform to Capital Case|
|delimiter|string|false| |The character to use between words (optional)|
|locale|null|false| |Locale for case conversion (optional)|
|mergeAmbiguousCharacters|boolean|false| |Whether to merge ambiguous characters (optional)|

---

## scripts.tools.encode_base64
工具描述：Encode text to Base64
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to encode or decode|

---

## scripts.tools.decode_base64
工具描述：Decode Base64 to text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to encode or decode|

---

## scripts.tools.encode_url
工具描述：Encode text for URLs
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to encode or decode|

---

## scripts.tools.decode_url
工具描述：Decode URL-encoded text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to encode or decode|

---

## scripts.tools.encode_html
工具描述：Encode HTML entities
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to encode or decode|

---

## scripts.tools.decode_html
工具描述：Decode HTML entities
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to encode or decode|

---

## scripts.tools.format_json
工具描述：Format and beautify JSON
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to format|
|indent_size|integer|false|2.0|Number of spaces for indentation (1-8)|

---

## scripts.tools.format_xml
工具描述：Format and beautify XML
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to format|
|indent_size|integer|false|2.0|Number of spaces for indentation (1-8)|

---

## scripts.tools.format_sql
工具描述：Format and beautify SQL
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to format|
|indent_size|integer|false|2.0|Number of spaces for indentation (1-8)|

---

## scripts.tools.format_html
工具描述：Format and beautify HTML
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to format|
|indent_size|integer|false|2.0|Number of spaces for indentation (1-8)|

---

## scripts.tools.count_characters
工具描述：Count characters in text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to analyze|

---

## scripts.tools.count_words
工具描述：Count words in text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to analyze|

---

## scripts.tools.count_lines
工具描述：Count lines in text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to analyze|

---

## scripts.tools.analyze_readability
工具描述：Calculate readability metrics
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to analyze|

---

## scripts.tools.string_trim
工具描述：Trim whitespace from text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to trim|
|trim_type|string|false|"both"|Type of trimming to perform|

---

## scripts.tools.string_substring
工具描述：Extract a substring
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to extract a substring from|
|start|integer|false|0.0|Starting index (inclusive)|
|end|integer|false| |Ending index (exclusive, optional)|

---

## scripts.tools.string_replace
工具描述：Replace text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to perform replacements on|
|search|string|true| |The string to search for|
|replace|string|true| |The string to replace with|
|replace_all|boolean|false|true|Whether to replace all occurrences|

---

## scripts.tools.string_split
工具描述：Split text into an array
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to split|
|delimiter|string|false|" "|The delimiter to split by|
|limit|integer|false| |Maximum number of splits (optional)|

---

## scripts.tools.string_join
工具描述：Join an array into text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|parts|array|true| |The array of strings to join|
|delimiter|string|false|""|The delimiter to join with|

---

## scripts.tools.generate_uuid
工具描述：Generate a UUID
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|version|string|false|"v4"|UUID version to generate|
|namespace|string|false| |Namespace for v5 UUID (required for v5)|
|name|string|false| |Name for v5 UUID (required for v5)|
|uppercase|boolean|false|false|Whether to return the UUID in uppercase|

---

## scripts.tools.validate_uuid
工具描述：Validate a UUID
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|uuid|string|true| |The UUID to validate|

---

## scripts.tools.generate_md5
工具描述：Generate MD5 hash
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to hash|

---

## scripts.tools.generate_sha1
工具描述：Generate SHA-1 hash
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to hash|

---

## scripts.tools.generate_sha256
工具描述：Generate SHA-256 hash
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to hash|

---

## scripts.tools.generate_sha512
工具描述：Generate SHA-512 hash
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to hash|

---

## scripts.tools.generate_hmac
工具描述：Generate HMAC hash
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to hash|
|key|string|true| |The secret key for HMAC|
|algorithm|string|false|"SHA256"|The hashing algorithm to use|

---

## scripts.tools.generate_lorem_ipsum
工具描述：Generate lorem ipsum text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|count|integer|false|5.0|Number of units to generate|
|units|string|false|"sentences"|Type of units to generate|
|paragraphLowerBound|integer|false|3.0|Minimum sentences per paragraph|
|paragraphUpperBound|integer|false|7.0|Maximum sentences per paragraph|
|sentenceLowerBound|integer|false|5.0|Minimum words per sentence|
|sentenceUpperBound|integer|false|15.0|Maximum words per sentence|
|format|string|false|"plain"|Output format|

---

## scripts.tools.regex_test
工具描述：Test a regex pattern against text
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to test against the pattern|
|pattern|string|true| |The regex pattern to test|
|flags|string|false|"g"|Regex flags (e.g., 'g', 'i', 'gi')|

---

## scripts.tools.regex_replace
工具描述：Replace text using a regex pattern
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to perform replacements on|
|pattern|string|true| |The regex pattern to match|
|replacement|string|true| |The replacement string|
|flags|string|false|"g"|Regex flags (e.g., 'g', 'i', 'gi')|

---

## scripts.tools.regex_extract
工具描述：Extract matches using a regex pattern
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to extract from|
|pattern|string|true| |The regex pattern with capture groups|
|flags|string|false|"g"|Regex flags (e.g., 'g', 'i', 'gi')|

---

## scripts.tools.regex_split
工具描述：Split text using a regex pattern
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|text|string|true| |The text to split|
|pattern|string|true| |The regex pattern to split by|
|flags|string|false|""|Regex flags (e.g., 'i')|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据