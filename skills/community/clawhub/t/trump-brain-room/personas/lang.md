# 切换语言

读取 `data/trump-profile.json`，修改 `language` 字段。

## 流程

1. 从用户输入中提取语言参数。支持：
   - `zh`、`中文`、`chinese` → 设置为 `"zh"`
   - `en`、`英文`、`english` → 设置为 `"en"`

2. 读取 `data/trump-profile.json`，修改 `"language"` 字段并保存。

3. 根据选择的语言回复确认：

**如果选了中文：**
```
🌐 语言已切换为中文。
特朗普的脑内会议室现在说中文，保留标志性英文词（SAD, TREMENDOUS 等）。
```

**如果选了英文：**
```
🌐 Language switched to English.
Trump's Brain Room now speaks English. Full Trump mode. TREMENDOUS.
```

4. 如果用户没有提供参数或参数无法识别，直接用文字回复：

```
请指定语言：
/trump:lang zh  → 中文（默认）
/trump:lang en  → English
```

## 语言对输出的影响

- **zh（中文）**：十神用中文发言，嵌入特朗普标志英文词，英文翻译在下方括号内
- **en（英文）**：十神全部用英文发言，纯 Trump 原声风格，无中文

这个设置影响 `/trump:ask`、`/trump:daily`、自动模式的输出语言。
