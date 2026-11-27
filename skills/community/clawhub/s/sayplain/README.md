# sayplain

[![skills.sh](https://skills.sh/b/shxuk/sayplain)](https://skills.sh/shxuk/sayplain)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-green.svg)](./scripts/style_check.py)

简体中文 | [English](./README.en.md)

中文技术书与文档的「去 AI 味」审校工作流（Agent Skill + 4 个零依赖 Python 脚本）。  
把充满套话、翻译腔和冗余总结的初稿洗成干净人话，同时保证数字、代码、路径和专有名词一字不丢。

## 上手

```bash
# 1) 装进 AI 助手（Claude Code / Cursor / Trae / Antigravity）
npx skills add shxuk/sayplain

# 2) 或直接跑本地质检脚本（仅用 Python 3 标准库，无需 pip install）
python scripts/format_check.py draft.md                      # 术语口径、标点与中英空格
python scripts/fact_anchor_check.py 01_原稿.md 02_二创稿.md   # 核对数字、代码、专名是否丢失或凭空新增
python scripts/style_check.py 02_二创稿.md                    # 扫描高频 AI 腔与高危文风
python scripts/consistency_check.py chapters/                # 跨章指代与标题一致性
```

> 脚本只读不写，命中只是信号，不是硬性违规；改不改结合上下文和 `references/` 规则定夺。

## 四道工序

工作稿按固定契约放在 `gongzuoliu/试跑/<日期_样本名>/` 下（输入 `01_原稿.md`，产出 `02_二创稿.md` 和 `复核报告.md`）：

0. **格式统一**：只改术语大小写、引号和错别字，不动语义（`references/风格手册.md`）。
1. **去 AI 味改写**：删翻译腔、理顺语病，面向零基础读者讲清逻辑（`references/改写规则.md`、`症状目录.md`、`保护边界.md`）。
2. **只删不添**：扫掉元叙述、假口语、重复升华和孤儿句，不新增原稿没有的观点或例子。
3. **复核修正**：跑完事实锚与文风脚本，按 `references/毛病词典.md`（21 条）通读定稿；仅在存在实质逻辑风险时写进 `复核报告.md`。

## 边界

- **不翻译，不从零写作**：只改已有中文初稿，不替作者重新立论或补造论据。
- **不破事实锚**：原稿里的数字、命令、文件名、代码块和真实引语逐字保留。
- **见凭证即停**：输入含疑似 API key、私钥或 cookie 时立刻中止。

<details>
<summary>仓库结构</summary>

```text
sayplain/
├── SKILL.md                  # 工序边界与文件契约
├── llms.txt                  # 机器可读摘要
├── references/               # 规则库（风格手册 / 改写规则 / 症状目录 / 毛病词典 / 保护边界 / 白名单等 9 份）
└── scripts/                  # 4 个纯标准库 Python 质检脚本
```

</details>

## License

[MIT](./LICENSE)
