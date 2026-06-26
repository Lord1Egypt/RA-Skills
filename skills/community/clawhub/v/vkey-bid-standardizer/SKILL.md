---
name: vkey-bid-standardizer
description: 银行投标响应文档标准化工具（v1.0）。基于 Word 样式体系（Heading 1-5 + Normal），兼容 GB/T 9704 公文格式；统一入口 standardize.py，提供 7 条流水线（all/fix/renumber/auto-number/review/convert-md/validate-patterns）。
industry: 银行
region: 中国大陆
---

# vkey-bid-standardizer

银行投标响应文档标准化工具。基于 Word 内置样式体系（Heading 1-5 + Normal），把任意 docx 一键整理为符合银行投标规范的成品稿。

## 核心优势

- **章节统一**：5 级编号（1. / 1.1 / 1.1.1 / 1.1.1.1 / 1.1.1.1.1）由 Word 多级列表自动渲染，杜绝编号错位
- **手动编号自动转写**：12 种常见形式（一、/（一）/第 X 章/附录 X/1.1 等）→ 跑 `renumber` 一键转阿拉伯层级
- **公文格式兼容**：版心、行距、字号、首行缩进严格遵循 GB/T 9704
- **一键 3 步流水线**：`all` 子命令一气呵成——renumber → fix → auto-number
- **可审查**：每步输出报告，可 `dry-run` 预览改动
- **配置驱动**：22 条编号模式入 JSON 配置文件，新增模式不改代码

## 技能元信息

| 字段 | 值 |
|------|-----|
| 技能名称 | `vkey-bid-standardizer` |
| 行业 | 银行 |
| 配置文件 | `vkey_bid_standardizer/profiles/standard.json` |
| 流水线数 | 7（all / fix / renumber / auto-number / review / convert-md / validate-patterns） |
| 测试 | `pytest tests/` — 61 个 case |
| 依赖 | Python 3.7+ / python-docx 1.x / pytest |
| 适用文档 | 技术应答、商务标书、实施方案、应答偏离表、投标方案 |

---

## 1. 概述

### 1.1 编制目的

为统一银行业投标响应文档（技术应答、商务标书、实施方案等）的格式规范，**满足银行招标方评标专家对版面与编号的合规审查要求**，提升标书质量与中标率。

本规范遵循的基本原则（金融投标四原则）：

- **合规性**：与 GB/T 9704 公文格式、银行投标规范保持一致
- **可追溯性**：5 级编号由 Word 多级列表自动生成，便于专家引用（如"详见 3.2 节"）
- **专业性**：版心/字号/字体严格遵循公文标准，体现投标方严谨度
- **可操作性**：基于 Word 内置样式体系，专家可在 Word 中直接批注/修订

### 1.2 编制依据

| 序号 | 标准编号 | 标准名称 | 适用要点 |
|------|----------|----------|----------|
| 1 | GB/T 9704—2012 | 党政机关公文格式 | 版心/页边距/字号/行距 |
| 2 | GB/T 15834—2011 | 标点符号用法 | 标点符号全角半角 |
| 3 | GB/T 15835—2011 | 出版物上数字用法 | 数字/百分号/单位 |
| 4 | GB/T 9851—2008 | 印刷字体分类 | 字体别名识别 |
| 5 | JR/T 0067—2017 | 银行信息安全风险管理指引 | 银行业信息安全引用 |
| 6 | JR/T 0071—2014 | 金融行业网络安全等级保护实施指引 | 银行业网络安全引用 |

### 1.3 术语与定义

| 术语 | 定义 |
|------|------|
| 样式（Style） | Word 中预设的格式集合 |
| 标题样式 | Word 内置 Heading 1-9，标识文档层次 |
| 正文样式 | 菜单栏显示为"正文"的 Normal 样式 |
| 行距 | 段内行与行的垂直距离（倍数或固定值）|
| 段前/段后 | 段落上方/下方的空白距离 |
| 首行缩进 | 段落首行相对左页边距的内缩 |
| 多级列表 | Word 的多级自动编号功能（绑定 Heading 样式）|
| 段级覆盖 | 段落自身 pPr（spacing/ind/jc）覆盖样式定义 |

---

## 2. 适用范围

### 2.1 适用文档类型（银行投标场景）

- **技术应答文件**：系统设计方案、技术白皮书、架构图说明、接口规范、应答偏离表
- **商务标书**：投标函、报价表、商务偏离表、资质证明、业绩清单
- **实施方案**：实施计划、项目组织、质量保证、风险控制、培训方案
- **应答与澄清**：评标答疑、技术澄清、商务澄清、补充函
- **银行内部立项材料**：总行科技部立项评审、内部方案报备、系统变更说明

### 2.2 不适用情形

- 非正式的工作备忘、内部草稿、便签类文档
- 已经按客户特定模板要求编制的对外文档（直接套用客户模板，本工具不修改）
- 含有大量特殊排版元素（复杂公式、艺术字、流程图）的文档

---

## 3. 文档结构规范

### 3.1 章节层次体系

文档采用五级章节结构，编号**统一带点**：

| 层级 | 编号格式 | 样式 | 示例 |
|------|----------|------|------|
| 一级章节 | 1. | Heading 1 | 1. 概述 |
| 二级章节 | 1.1 | Heading 2 | 1.1 适用范围 |
| 三级章节 | 1.1.1 | Heading 3 | 1.1.1 子项说明 |
| 四级章节 | 1.1.1.1 | Heading 4 | 1.1.1.1 详细说明 |
| 五级章节 | 1.1.1.1.1 | Heading 5 | 1.1.1.1.1 极详细 |

**禁止**：使用 `一、` `（一）` `1 概述`（无点）等其他格式。

### 3.2 章节编号约定

- 标题必须用 Word 内置 Heading 样式（不能用普通段落加粗替代）
- 编号与标题文字之间使用**半角空格**分隔
- 数字编号采用阿拉伯数字，章节顺序 1, 2, 3（最多至 99）
- 跨章节引用用完整编号（如"详见 3.2 节"）
- 金融投标章节常超 9（GB/T 9704 章条编号支持到 999），编号可至 3 位

### 3.3 手动编号识别

技能支持 12 种常见手动编号形式（`一、`、`（一）`、`1.1`、第 X 章、附录 X 等）→ 跑 `standardize.py renumber` 自动转阿拉伯层级。详见 [附录 B](#附录-b-编号模式清单)。

---

## 4. 页面布局规范

### 4.1 页边距

| 边距 | 标准值 | 允许偏差 |
|------|--------|----------|
| 上 | 3.7 厘米 | ±0.1 厘米 |
| 下 | 3.5 厘米 | ±0.1 厘米 |
| 左 | 2.8 厘米 | ±0.1 厘米 |
| 右 | 2.6 厘米 | ±0.1 厘米 |

### 4.2 纸张与方向

- 纸张规格：A4（21 厘米 × 29.7 厘米）
- 页面方向：纵向
- 特殊场景：表格超宽时可用横向

---

## 5. 字体与字号规范

### 5.1 字体配置

| 元素 | 西文字体 | 中文字体 | 适用 |
|------|----------|----------|------|
| 标题 | Times New Roman | 黑体 | 标题 1-5 |
| 正文 | FangSong | 仿宋 | Normal 段落 |
| 表头 | Times New Roman | 黑体 | 表格首行 |
| 表内 | FangSong | 仿宋 | 表格数据 |

### 5.2 字号标准（GB/T 9704 公文格式）

| 元素 | 字号 | 磅数 | 标识 |
|------|------|------|------|
| 正文 | 四号 | 14pt | Normal |
| 一级标题 | 小二号 | 18pt | Heading 1 |
| 二级标题 | 三号 | 16pt | Heading 2 |
| 三级标题 | 小三号 | 15pt | Heading 3 |
| 四级标题 | 四号 | 14pt | Heading 4 |
| 五级标题 | 五号 | 10.5pt | Heading 5 |
| 表格表头 | 五号 | 10.5pt | — |
| 表格内容 | 五号 | 10.5pt | — |
| 页脚 | 五号 | 10.5pt | — |

### 5.3 颜色

- 标题与正文：黑色（`#000000`）
- 强调用粗体/下划线，避免颜色（除确有需要）
- 所有颜色保证黑白打印清晰

---

## 6. 段落与间距规范

### 6.1 行距

| 元素 | 类型 | 值 |
|------|------|-----|
| 正文 | 固定值 | 20 磅 |
| 标题 1-5 | 倍数 | 1.25 倍 |

### 6.2 段落间距

| 元素 | 段前 | 段后 |
|------|------|------|
| 一级标题 | 16 磅 | 0 磅 |
| 二级标题 | 14 磅 | 0 磅 |
| 三级标题 | 12 磅 | 0 磅 |
| 四级标题 | 10 磅 | 0 磅 |
| 五级标题 | 8 磅 | 0 磅 |
| 正文 | 0 磅 | 0 磅 |

### 6.3 缩进与对齐

- 首行缩进：正文段落 **2 字符 = 2 × 字号 = 28 磅**（4 号字 14pt × 2）
- 对齐：左对齐（避免两端对齐的字间距不均）

**OOXML `w:ind` 字段单位**（必须严格区分，否则 Word 显示与渲染不一致）：

| 字段 | 单位 | 2 字符示例 | 说明 |
|------|------|-----------|------|
| `w:firstLine` | 1/20 pt（twips） | `560` | 28pt = 560 twips；用于渲染 |
| `w:firstLineChars` | **1/100 字符** | `200` | **2 字符必须写 200，不是 2**；用于对话框"度量值"显示 |
| `w:left` | 1/20 pt（twips） | `0` | 段落左缩进 |
| `w:leftChars` | 1/100 字符 | `0` | 段落左缩进（字符单位）|
| `w:hanging` / `w:hangingChars` | 同上 | — | 悬挂缩进 |

> 常见陷阱：python-docx 设 `Pt(22.4)` 时**只写** `w:firstLine` 为 twips 值，**不写** `w:firstLineChars`；Word 对话框"度量值"读 `firstLineChars` 显示为字符数，缺省时显示 0/1 字符。**`apply_paragraph_format` 必须同时写两字段并保持换算一致**（`firstLineChars = first_line_chars × 100`）。
- 标题不缩进，左对齐于页边距

---

## 7. 表格规范

| 元素 | 字体 | 字号 | 对齐 |
|------|------|------|------|
| 表头 | 黑体 | 10.5pt | 居中 |
| 表内 | 仿宋 | 10.5pt | 左对齐 |

**边框**：外框 1.5 磅、内框 0.5 磅、黑色 `#000000`  
**表头底纹**：浅灰 `#D9D9D9`（仅首行）  
**列宽**：自动列宽，按内容比例分配

### 7.1 表格段落缩进（强制要求）

- 表格内段落**不得继承**正文 Normal 样式的首行缩进（GB/T 9704 公文规范不要求表格内容缩进）
- 必须在每个 `w:tc > w:p` 的段级 `w:pPr` **强制写入** `w:ind`，阻断样式继承链：

```xml
<w:pPr>
  <w:ind w:firstLine="0" w:firstLineChars="0"/>
</w:pPr>
```

> 陷阱：仅 `del` 现有 `w:firstLine` 属性无法阻断"无 w:ind 元素"的段落（会继承 Normal 样式）。**必须 `get_or_add_pPr()` + `get_or_add_w:ind()` 显式构造**——对应 `pipeline.py::_fix_tables` 中"强制段级 firstLine=0"逻辑。

---

## 8. 页脚规范

金融投标页脚**默认居中页码**，可按需扩展为「项目编号 + 页码」或「招标编号 + 页码 + 总页数」。

| 属性 | 标准值 |
|------|--------|
| 字体 | 仿宋 10.5 磅（五号）|
| 对齐 | 居中 |
| 位置 | 页底 |
| 起始页码 | 1 |
| 格式 | `页码`（默认）/ `项目编号 - 页码`（可配） |

> 模板与 `standard.json::footer.text` 字段联动。如需 `项目编号-页码` 格式，编辑 `footer.text` 为 `{project_code} - {page}`（v1.0 占位符占位，v1.1 将完整支持）。

---

## 9. 使用指南

### 9.1 推荐入口

v1.0 唯一 CLI 入口是顶层 `standardize.py`：

```bash
# 全流水线（推荐）
python standardize.py all input.docx -o output.docx

# 单步
python standardize.py fix input.docx
python standardize.py renumber input.docx
python standardize.py auto-number input.docx
python standardize.py review input.docx
python standardize.py convert-md input.md
python standardize.py validate-patterns
```

通用 flag：`--profile standard`（默认；`bid` 是别名）/ `--dry-run` / `--backup` / `-v` / `-o`

### 9.2 流水线总览

| # | 名称 | 命令 | 作用 |
|---|------|------|------|
| 1 | 全流水线 | `standardize.py all` | renumber → fix → auto-number 三步串行 |
| 2 | 修复样式 | `standardize.py fix` | 应用规范 + 清段级/run 级覆盖 |
| 3 | 重编号 | `standardize.py renumber` | 手动编号（一、/（一）/1.1）→ 阿拉伯层级 |
| 4 | 自动编号 | `standardize.py auto-number` | Heading 1-5 绑 Word 多级列表 |
| 5 | 审查 | `standardize.py review` | JSON 审计报告（段级覆盖、issues） |
| 6 | MD→docx | `standardize.py convert-md` | 从 Markdown 源生成 |
| 7 | 模式校验 | `standardize.py validate-patterns` | 22 条模式样本测试 |

### 9.3 典型应用场景

**场景一：技术应答文件标准化**

```bash
python standardize.py all 银行核心系统技术应答_v1.0.docx -o 银行核心系统技术应答_v1.0_标准化.docx
```

跑完 3 步：手动编号（一、/（一）/1.1）→ 阿拉伯层级 → 套用 GB/T 9704 公文样式 → 绑 Word 多级列表。

**场景二：先 dry-run 看会改什么，不写文件**

```bash
python standardize.py all 银行核心系统技术应答_v1.0.docx --dry-run
```

只输出计划（如 `renumber (62) | fix (1756) | auto-number (5)`），不写任何文件——评标前安全预览改动。

**场景三：投标合规审查**

```bash
python standardize.py review 银行核心系统技术应答_v1.0_标准化.docx
```

输出 JSON 报告：`overrides` 全为 0 + `issues: []` 即符合公文规范。

**场景四：备份原文件再修复（防止覆盖）**

```bash
python standardize.py all 银行核心系统技术应答_v1.0.docx -o 银行核心系统技术应答_v1.0_标准化.docx --backup
```

自动把原文件备份为 `银行核心系统技术应答_v1.0.docx.bak`。

**场景五：从 Markdown 起草金融投标稿**

```bash
python standardize.py convert-md 银行核心系统技术应答.md -o 银行核心系统技术应答_v1.0.docx
```

按附录 C 的 Markdown 规范写，5 级章节 + 表格 + 段落直接转成标准 docx。

---

## 10. 质量保证

### 10.1 审查清单

| 维度 | 通过标准 |
|------|----------|
| 样式使用 | 标题用 Heading 1-5，正文用 Normal |
| 字体 | 标题黑体，正文仿宋，色 `#000000` |
| 间距 | 行距 1.25 倍 / 固定 20 磅；段前段后符合规范 |
| 表格 | 表头黑体 10.5pt 灰底，表内仿宋 10.5pt |
| 页脚 | 仅页码数字 |
| 编号 | 标题具备 1./1.1/1.1.1 层级 |
| 段级覆盖 | 所有 Heading/Normal 段落无 pPr 覆盖（`overrides` 全为 0） |

### 10.2 合规判定

- **完全合规**：`issues` 空 + `overrides` 全 0
- **基本合规**：仅有模式 warning（需手动添加未识别编号）
- **不合规**：存在段级覆盖或样式错乱，跑 `standardize.py fix` 修复

---

## 11. 配置管理

### 11.1 配置文件

规范通过 `vkey_bid_standardizer/profiles/standard.json` 集中管理，含 9 个节：

| 节 | 作用 | 金融投标关注点 |
|----|------|----------------|
| `page` | 页面边距 | GB/T 9704 版心 156×225mm |
| `body` | 正文样式 | 三号仿宋 + 28 磅固定行距 |
| `headings` | 5 级标题样式 | 黑体 + 1.5 倍行距 |
| `tables` | 表格样式 + 边框 | 灰底表头 + 1.5/0.5 磅框 |
| `footer` | 页脚配置 | 居中页码 / 项目编号-页码 |
| `numbering` | Word 多级列表 | 1./1.1/1.1.1 层级 |
| `patterns` | 22 条手动编号识别 | 中文 / 第X章 / 附录 |
| `color` | 颜色（`#000000`） | 黑白打印兼容 |
| `metadata`（v1.1） | 项目元数据 | 招标编号 / 项目名称 / 投标类型 |

`bid.json` 是 `standard.json` 的别名（找不到时自动 fallback）。**调整规范**改 `standard.json` 而非源代码。

### 11.2 模板文件

| 模板 | 路径 | 用途 |
|------|------|------|
| 标书空白模板 | `templates/bid_blank.md` | Markdown 金融投标起草（`convert-md` 输入源） |

### 11.3 依赖

- Python 3.7+
- python-docx 1.x（`pip install python-docx`）
- Word 2016+ / WPS Office 2019+

---

## 12. 系统要求

| 组件 | 最低版本 | 备注 |
|------|---------|------|
| Python | 3.7+ | 推荐 3.10+ |
| python-docx | 1.0+ | `pip install python-docx` |
| pytest | 7.0+ | 仅运行测试时需要 |
| Microsoft Word | 2016+ | 需支持多级列表 |
| WPS Office | 2019+ | 兼容多级列表 |

**安装依赖**：

```bash
pip install python-docx pytest
```

---

## 13. 自定义模式教程

### 13.1 何时需要

如果客户 docx 用了**非标准编号形式**（不在 12 种内置模式里），`renumber` 会输出 warning：

```
[Heading 3] 未识别编号: §3.1 系统架构
```

### 13.2 添加步骤

**Step 1：分析样本**

从 docx 复制一段未识别的标题，如 `§3.1 系统架构`。

**Step 2：写正则，加到 `standard.json::patterns::h3`**

```json
{
  "name": "section_sign",
  "pattern": "^§(\\d+)\\.(\\d+)\\s+(.*)$"
}
```

`pattern` 规则：**第一个捕获组必须是编号**。

**Step 3：标注解析模式**

如果编号含中文数字，加 `"cn_to_int": true`：

```json
{
  "name": "part_cn",
  "pattern": "^第([一二三四五六七八九十百]+)部分\\s+(.*)$",
  "cn_to_int": true
}
```

或混合（中/阿）：`"mixed_cn_int": true`。

**Step 4：模式顺序**

**更具体的模式放前面**（避免被通用模式抢先匹配）。例如 `wps_label` 必须在 `single_arabic` 之前。

**Step 5：验证**

```bash
python standardize.py validate-patterns
```

如样本测试不通过，输出会指明问题。

### 13.3 字段参考

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✓ | 模式名（英文，warning 输出用）|
| `pattern` | ✓ | 正则，**第一个捕获组必须是编号** |
| `cn_to_int` |  | 第一组是中文数字（用 `parse_cn_num`） |
| `mixed_cn_int` |  | 第一组是混合数字（`1` 或 `三`） |

---

## 14. 修订历史

| 版本 | 日期 | 修订人 | 内容 |
|------|------|--------|------|
| V1.0 | 2026-06-03 | vkey-bid-standardizer | 首次独立发布；统一入口 `standardize.py`；7 条流水线；22 条编号模式；61 个 pytest case；单一真相源 `standard.json` |
| V1.0.1 | 2026-06-04 | vkey-bid-standardizer | 修复 3 项 OOXML 规范偏差：① `firstLineChars` 单位误用（改 `×100`）；② `firstLine` 增补 twips 兜底（28pt = 560）；③ 表格段落强制段级 `firstLine=0` 阻断 Normal 样式继承 |

---

## 附录 A 配置文件

`vkey_bid_standardizer/profiles/standard.json` 是规范的**唯一真相源**。

完整结构（请直接读源文件）：

```bash
# 查看完整 JSON
cat vkey_bid_standardizer/profiles/standard.json

# 关键字段速查
python -c "from vkey_bid_standardizer import load_profile; p = load_profile('standard'); print(p['headings'])"
```

> **不要在 SKILL.md 里复制完整 JSON**——配置可能演化，文档与代码脱钩后维护成本高。

## 附录 B 编号模式清单

`standard.json::patterns` 共 **22 条正则规则**，覆盖 **12 种**常见多级编号形式。

| 模式名 | 层级 | 形式 | 示例 |
|--------|------|------|------|
| `chinese_punct` | H1 | `一、` `二、` | `一、概述` |
| `chapter_cn` | H1 | 第X章（中文）| `第十章 总则` |
| `chapter_arabic` | H1 | 第N章 | `第3章 术语` |
| `appendix_cn` | H1 | 附录X | `附录A 数据` |
| `appendix_alpha` | H1 | Appendix X | `Appendix A Data` |
| `single_arabic` | H1-H5 | `1.` `2.` | `1. 总则` |
| `circle_num` | H1 | ①②③ | `① 条款` |
| `cn_paren_both` | H2 | `（一）` 或 `(一)` | `（一）适用范围` |
| `section_cn` | H2 | 第X节 | `第一节 概述` |
| `dot_arabic` | H2 | `1.1` | `1.1 范围` |
| `wps_label` | H2/H3 | `1. 标题 1` | `1. 标题 1` |
| `arabic_paren` | H3-H5 | `（1）` 或 `(1)` | `（1）数据采集` |
| `article_cn` | H3 | 第X条 | `第一条 范围` |
| `dot_triple` | H3 | `1.1.1` | `1.1.1 概述` |
| `dot_quad` | H4 | `1.1.1.1` | `1.1.1.1 详细` |
| `dot_quint` | H5 | `1.1.1.1.1` | `1.1.1.1.1 极详细` |

**模式顺序很重要**——更具体的模式放前面（避免被通用模式抢先匹配）。  
**失败降级**：未匹配段落原样保留 + warning。

> 正则源在 `standard.json::patterns`，**不要在 SKILL.md 里复制正则**——配置可能演化。

## 附录 C Markdown 编写规范

适用于 `standardize.py convert-md` 流水线的 Markdown 源文件。

**约定**：

- `# 文档标题` 仅用于**首行大标题**（居中加粗、黑体 18pt），独立成段，不进入目录
- `## 1. 章节名` 才是正文章节起点（对应 Heading 1）
- 不要省略文档标题——脚本按 Markdown 层级顺序解析

| Markdown 语法 | Word 样式 |
|---------------|----------|
| `# 文档标题` | Normal 段落（居中加粗，黑体 18pt）|
| `## 1. 章节名` | Heading 1 |
| `### 1.1 子章节` | Heading 2 |
| `#### 1.1.1 三级` | Heading 3 |
| `##### 1.1.1.1 四级子项` | Heading 4（独立成行）|
| `###### 1.1.1.1.1 五级子项` | Heading 5（独立成行）|
| `\| 表头 \|` | 表格（1.5pt 外框 + 0.5pt 内框）|

**要求**：标题独立成行 / 表格用标准 Markdown / 不使用代码块 / 列表项末尾加句号。
