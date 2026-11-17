---
name: vocab-cards-lite
slug: vocab-cards-lite
version: 2.0.4
displayName: 英语词汇闪卡 Lite
author: 51comic
license: MIT-0
tags: [vocabulary, flashcards, english, education, print, python, image-generation]
compatibility: "OpenClaw 0.5+ / 通用技能运行时；需 Python 3.8+ 与系统字体 NotoSansCJK + DejaVu；仅 IPA 音标使用包内自带裁剪字体。"
description: |
  专业英语词汇闪卡生成器(精简版,包体仅68KB)。将「英文单词」批量生成「单词卡」「英文闪卡」「单词闪卡」:
  从 JSON 单词数据一键生成黑白打印优化的主卡/副卡/百度百科二维码 PNG。
  仅内置 IPA 音标裁剪字体,中英文使用系统字体(NotoSansCJK + DejaVu)。
  触发场景:当用户提到「单词卡」「英文单词」「英文闪卡」「单词闪卡」「闪卡」「词汇卡」「flashcard」「vocab cards」
  「背单词卡片」「打印单词卡」「批量生成单词卡」「英语卡片」「词卡 PNG」时使用。
  适用于把单词表(含音标/词性/释义/搭配/例句/文化背景)批量转成可打印卡片图片的场景。
  English: Generate printable black-and-white English vocabulary flashcard PNG images from JSON word lists, including main cards, optional side cards, and optional Baidu Baike QR-code cards, with a bundled IPA font plus system CJK and DejaVu fonts for clean multilingual rendering.
---

# Vocab Cards Lite — 专业英语词汇闪卡生成器(精简版)

从 JSON 单词数据生成黑白打印优化的专业英语闪卡 PNG。**主卡 + 副卡 + 百度百科二维码**三件套，包体仅 **68KB**（仅内置 IPA 音标裁剪字体，中英文使用系统字体）。

## 使用场景

- 需要把一批英文单词（音标/词性/释义/搭配/例句/文化背景）批量生成闪卡 PNG
- 生成面向**黑白打印**的简洁卡片（白底黑字灰线）
- 中英文混排，IPA 音标、CJK 中文、英文字体分别处理，根治"豆腐块"
- 需要**小体积分发**（完整版 vocab-cards-pro 内置完整 CJK 字体约 40MB，本版仅 68KB）

## 何时激活 / When to Activate

当用户表达以下意图时使用本技能（匹配 `description` 中的触发关键词）：

- 提到「单词卡」「英文单词」「英文闪卡」「单词闪卡」「闪卡」「词汇卡」「flashcard」「vocab cards」「背单词卡片」「打印单词卡」「批量生成单词卡」「英语卡片」「词卡 PNG」等
- 希望把单词表（含音标 / 词性 / 释义 / 搭配 / 例句 / 文化背景）**批量转成可打印图片**
- 需要生成**主卡 / 副卡 / 百度百科二维码 PNG** 三件套
- 需要**黑白打印优化**、小体积（68KB）分发的词汇卡片

## 何时不激活 / Anti-Triggers

以下情况不要使用本技能，改用更合适的工具：

- 用户只想要**文本释义 / 翻译**，不需要生成 PNG 图片 → 用词典 / 翻译工具
- 需要**彩色、设计感、复杂版式**的卡片 → 本技能仅做黑白打印优化
- 需要 **PDF 教材解析、OCR、全文排版** → 超出范围
- **系统缺少中文 / 英文系统字体**且无法安装（包体仅含 IPA 字体，生僻汉字依赖系统 CJK 字体）
- 不希望输出文件、仅要**纯文本结果**时

## 核心能力

- **主卡**：单词 + UK/US 音标 + 词性徽章 + 难度 + 中文释义 + 英文定义 + 固定搭配 + 丰富例句(含中文) + 文化背景
- **副卡**：相关信息 + 相关词汇 + 地道表达 + 文化背景 + 记忆提示
- **二维码**：右下角自动叠加 180px 百度百科二维码，标注 "Baidu Baike"，可开关
- **三字体策略**：IPA 音标 → 包内裁剪字体(68KB)，中文 → 系统 NotoSansCJK，英文/ASCII → 系统 DejaVu
- **分段渲染 + 基线对齐**：IPA/中文/英文混排不歪斜（v1.0.5 起）
- **智能换行**：英文单词不拆词、括号成对、标点黏连不居行首
- **动态画布**（v2.0）：内容多高卡片就多高，长词条不再被静默截断；超过 3200px 才告警截断
- **输入校验**（v2.0）：仅 `word` 必填，缺失字段自动补默认值并打印中文提示，不再 KeyError
- **黑白打印优化**：白底 #fff / 黑字 #000 / 灰阶 #374151、#6b7280、#d1d5db
- **文件命名**：按英文单词 slug 化（`new_zealand.png`）；纯中文词条自动 hash 命名（v2.0）

## 环境依赖

Python 库（`pillow` / `fonttools` / `qrcode[pil]`）需安装；**系统需有 NotoSansCJK（中文）和 DejaVu（英文）字体**。

### 一键安装依赖

```shell
bash scripts/setup.sh
```

自动：安装三个 Python 库（venv/系统 Python 自适应）→ 校验包内 IPA 字体 → 检测系统字体（缺失时给出中文安装指引）→ 验证可导入。

### 字体架构

| 字体 | 来源 | 用途 |
|------|------|------|
| DejaVuSans.ttf / DejaVuSans-Bold.ttf | **包内自带（68KB，裁剪版，仅 IPA 字符）** | IPA 音标 |
| NotoSansCJK (.ttc) | 系统字体（需自行安装） | 中文/CJK |
| DejaVuSans (.ttf) | 系统字体 | 英文/ASCII |

> 包体仅 68KB 的代价：中文/英文依赖系统字体。`setup.sh` 会检测并给出安装命令（如 `sudo apt install fonts-noto-cjk fonts-dejavu`）。如需开箱即用覆盖任意生僻汉字，改用完整版 `vocab-cards-pro`（约 40MB）。

## 输入 JSON 格式

顶层为数组；**只有 `word` 是必填的**，其余字段缺失时自动按空值处理并打印 `HINT` 提示。

```json
[
  {
    "word": "New Zealand",
    "ipa_uk": "njuː ˈziːlənd",
    "ipa_us": "nuː ˈziːlənd",
    "pos": "n.",
    "level": "C1",
    "cn": "新西兰",
    "en": "An island country in the southwestern Pacific Ocean.",
    "coll": ["New Zealanders", "North Island", "Maori culture"],
    "examples": [["I visited New Zealand last summer.", "我去年夏天去了新西兰。"]],
    "note": "位于南太平洋的岛国，毛利文化是其独特标识。",
    "baike_url": "https://baike.baidu.com/item/新西兰",
    "side": {
      "category": "Geography",
      "info": "毛利语 Aotearoa，意为「长白云之乡」。",
      "related": ["Auckland", "Wellington", "Kiwi"],
      "expressions": ["Kia ora — 毛利语问候"],
      "culture": "毛利文化与英式文化交融。",
      "tip": "aotearoa → 长白云之地，记住白云即新西兰。"
    }
  }
]
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `word` | ✅ | 单词本身（英文/词组） |
| `ipa_uk` / `ipa_us` | 可选 | 音标 |
| `pos` / `level` | 可选 | 词性徽章 / 难度等级 |
| `cn` / `en` | 可选 | 中文释义 / 英文定义 |
| `coll` | 可选 | 固定搭配数组 |
| `examples` | 可选 | `[[英文例句, 中文翻译], ...]` |
| `note` | 可选 | 文化背景 |
| `baike_url` | 可选 | 提供才生成 `_qr.png` 二维码卡 |
| `side` | 可选 | 提供才生成 `_side.png` 副卡；子字段全部可选 |

## 调用方式

```shell
python3 scripts/vocab_cards.py <input.json> [output_dir]
```

- `<input.json>`：必填，上述格式的单词批数据
- `[output_dir]`：输出目录，默认当前目录

**快速验证**（自带最小示例，可直接跑通）：

```shell
python3 scripts/vocab_cards.py examples/sample.json /tmp/vocab_demo
```

输出示例（`word="New Zealand"`）：
- `new_zealand.png` — 主卡
- `new_zealand_qr.png` — 主卡 + 百度百科二维码
- `new_zealand_side.png` — 副卡（仅当条目含 `side` 字段）

结束时打印汇总：`完成: 成功 X / 失败 Y / 跳过 Z`。

## 输出与退出码（v2.0 新增）

| 情况 | 行为 |
|------|------|
| 单条缺 `word` | 打印 `SKIP: ...` 跳过，不中断整批 |
| 单条生成异常 | 打印 `FAIL: ...`，不中断整批 |
| 全部失败/跳过 | 退出码 3（便于脚本链式判断） |
| 输入文件不存在/非法 JSON | 退出码 2 + 中文错误提示 |
| 内容超过 3200px | 打印 `WARN` 并截断（防爆图） |

## 注意事项

- 生僻字显示依赖系统字体；若遇生僻字显示方框，请安装系统字体 NotoSansCJK 或改用完整版 `vocab-cards-pro`
- 图片宽度固定 **1000px**，高度按内容动态扩展（最低 1700px，最高 3200px）
- 字体为**延迟加载**（v2.0）：仅查看帮助或 import 模块不会因缺字体崩溃；真正绘图时才校验字体
- 单个单词失败不中断整批（逐条 try/except）

## 领域知识 / Domain Knowledge

- **三字体策略**：IPA 音标 → 包内裁剪 DejaVu（68KB）；中文 → 系统 NotoSansCJK；英文 / ASCII → 系统 DejaVu。缺系统字体时中文 / 英文会显示方框。
- **画布尺寸**：宽度固定 1000px；高度按内容动态扩展，最低 1700px、上限 3200px，超出打印 `WARN` 并截断。
- **字体延迟加载**（v2.0）：仅真正绘图时校验字体；查看帮助或 `import` 模块不会因缺字体崩溃。
- **命名规则**：文件名按英文单词 slug 化（如 `new_zealand.png`）；纯中文 / 特殊字符自动 hash 命名（`word_<md5前8位>.png`）。
- **二维码 / 副卡条件**：仅当条目含 `baike_url` 才生成 `_qr.png`；仅当含 `side` 字段才生成 `_side.png`。
- **配色**：白底 `#fff` / 黑字 `#000` / 灰阶 `#374151`、`#6b7280`、`#d1d5db`，专为黑白打印校准。

## 参考文件 / References

| 文件 | 说明 |
|------|------|
| `README.md` | 快速上手、安装与使用说明 |
| `CHANGELOG.md` | 版本与变更记录 |
| `requirements.txt` | Python 依赖清单（pillow / fonttools / qrcode[pil]） |
| `scripts/vocab_cards.py` | 主生成脚本 |
| `scripts/setup.sh` | 依赖安装与字体校验一键脚本 |
| `examples/sample.json` | 内置最小验证示例（3 条） |
| `skill-card.md` | 技能卡片（发布元数据 / 风险评估） |
| `_meta.json` | 发布元数据（owner / slug / version） |
| `assets/fonts/` | 包内 IPA 裁剪字体（DejaVuSans.ttf / DejaVuSans-Bold.ttf，68KB） |
| `references/` | 参考与设计说明集 |

详见 [references/REFERENCES.md](references/REFERENCES.md)。

## 版本

- **v2.0.0**（2026-08-08）：达尔文全量优化——动态画布、输入校验、slug 兜底、字体延迟加载、setup.sh 重写、退出码规范、自带示例
- v1.0.5（2026-08-05）：分段渲染 + 基线对齐、纯黑白配色、三字体策略
- v1.0.0（2026-08-05）：首版发布到 ClawHub

详见 [CHANGELOG.md](CHANGELOG.md)。
