# 本地化 / Localization

本目录存放 skill 的**多语言版本**。默认（最前 / 首选）语言为中文（`zh-CN`），对应仓库根目录的 `SKILL.md` / `README.md` 及 `references/`。

This directory holds the **language localizations** of the skill. The default (first / preferred) language is Chinese (`zh-CN`), corresponding to the root `SKILL.md` / `README.md` and `references/`.

---

## 目录约定 / Directory Convention

```
网站测试安全规则/
├── SKILL.md              # 默认语言：中文（zh-CN），最前
├── README.md             # 默认语言：中文（zh-CN）
├── references/...        # 默认语言：中文（zh-CN）
└── locales/
    ├── README.md         # 本说明（双语）
    └── en/               # 英文版本（示例）
        ├── SKILL.md
        ├── README.md
        └── references/   # 英文版 references（与根 references 同构）
            ├── report_template.md
            ├── auth_notes.md
            ├── authorization_template.json
            ├── backup_notes.md
            └── authorized_pubkeys/README.md
```

新增语言时，复制 `locales/en/` 为 `locales/<语言代码>/` 并翻译。语言代码建议用 BCP 47（如 `en`、`ja`、`zh-TW`）。

To add a language, copy `locales/en/` to `locales/<lang-code>/` and translate. Use BCP 47 codes (e.g. `en`, `ja`, `zh-TW`).

---

## 语言选择 / Language Selection

默认语言为 **`zh-CN`**（根目录文件）。切换语言有两种方式：

The default language is **`zh-CN`** (root files). Switch language via either method:

1. **环境变量 / Environment variable**：设置 `MOWEN_LANG=<语言代码>`（如 `MOWEN_LANG=en`）。
2. **`lang` 文件 / `lang` file**：在项目或 skill 目录放置 `lang` 文件，内容为语言代码（如 `en`）。

> 无论哪种方式，落地的具体语言版本文件都在 `locales/<语言代码>/SKILL.md`。若对应语言不存在，回退到默认中文（`zh-CN`）。
> Either way, the concrete localized file lives at `locales/<lang-code>/SKILL.md`. If the language is missing, fall back to default Chinese (`zh-CN`).

### 在对话中切换 / Switching in conversation

- 中文（默认）：直接引用根目录 `SKILL.md` 的规则。
- English: tell the agent "use the English version" → it reads `locales/en/SKILL.md`.

---

## 维护说明 / Maintenance Notes

- 根目录（中文）始终是**权威源 / source of truth**。更新规则时，请同步更新所有 `locales/*` 下的对应文件，保持版本号（`version`）与内容一致。
- The root (Chinese) is always the **source of truth**. When updating rules, sync the corresponding files under every `locales/*`, keeping `version` and content consistent.
- 各语言版本 frontmatter 中标注 `lang` 字段（如 `lang: "en"`）以便识别。
- Each localized file carries a `lang` frontmatter field (e.g. `lang: "en"`) for identification.
