# 学位论文评审 (Thesis Reviewer)

[English](README.md)

系统化评审各学科硕士和博士学位论文的 AI 编程助手技能。以导师视角提供全方位、结构化的评审反馈，帮助学生在提交前改进论文质量。

## 功能特点

| 功能 | 说明 |
|------|------|
| 全学科覆盖 | 7 个学科专项模块 + 通用评审框架，支持所有学科 |
| 硕博通用 | 支持硕士和博士学位论文，自动识别并适配评审标准 |
| 学术/专业学位 | 区分学术学位与专业学位的不同评审要求（依据 2025 学位法） |
| 五维评审 | 学术质量、写作质量、格式规范（GB/T 7713.1）、数据与结果、学术诚信 |
| 两阶段流程 | Phase 1 自动深度分析 → Phase 2 交互式精修 |
| 170+ 检查项 | 通用 149 项 + 学科专项 22-34 项 |
| 博士专项评审 | 原创贡献评价、独立研究能力、研究体系系统性、学术成果 |
| 盲审风险预警 | 模拟盲审评审维度（选题/创新性/学术性/规范性/写作），预判风险 |
| 结构化输出 | 正式评审意见书格式，可直接交给学生 |
| 严重程度标记 | 🔴 严重 / 🟡 需改进 / 🟢 良好，清晰的优先级 |
| 国家标准对齐 | 依据 GB/T 7713.1-2006、GB/T 7714-2015、GB 3100-3102-93 |

## 多平台支持

支持所有主流 AI 编程助手平台：

| 平台 | 状态 | 说明 |
|------|------|------|
| **Claude Code** | ✅ 完整支持 | 原生 SKILL.md 格式 |
| **OpenClaw / ClawHub** | ✅ 完整支持 | `metadata.openclaw` 命名空间，依赖检测 |
| **Hermes Agent** | ✅ 完整支持 | `metadata.hermes` 命名空间，标签，分类 |
| **OpenAI Codex** | ✅ 完整支持 | `agents/openai.yaml` 配套文件 |
| **OpenCode** | ✅ 完整支持 | SKILL.md 自动发现 |
| **Pi-Mono** | ✅ 完整支持 | `metadata.pimo` 命名空间，标签 |
| **SkillsMP** | ✅ 已收录 | GitHub topics 已配置 |

## 工作流程

```
输入 .docx 文件
    │
    ▼
[预处理] markitdown 转换 → Markdown → 识别章节结构
    │
    ▼
[Phase 1: 自动深度分析]
    ├─ Step 1: 整体扫描（结构完整性、研究问题、全局印象）
    ├─ Step 2: 逐章 + 全局分析（170+ 检查项）
    ├─ Step 2b: 跨章一致性检查
    └─ Step 3: 生成初版评审报告
    │
    ▼
[Phase 2: 交互式精修]
    ├─ 逐章讨论具体问题
    ├─ 追问、调整意见、补充遗漏
    └─ 用户说"完成精修"生成最终版
    │
    ▼
[最终输出] 合并修改 → 保存最终评审意见书
```

## 前置依赖

- `markitdown` MCP — 用于将 .docx 转换为 Markdown

## 技能安装

### Claude Code

```bash
# 全局安装
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.claude/skills/thesis-reviewer

# 项目级安装
git clone https://github.com/Agents365-ai/thesis-reviewer.git .claude/skills/thesis-reviewer
```

### OpenClaw / ClawHub

```bash
# 通过 ClawHub
clawhub install thesis-reviewer

# 手动安装
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.openclaw/skills/thesis-reviewer

# 项目级安装
git clone https://github.com/Agents365-ai/thesis-reviewer.git skills/thesis-reviewer
```

### Hermes Agent

```bash
# 安装到 research 分类
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.hermes/skills/research/thesis-reviewer
```

或在 `~/.hermes/config.yaml` 中添加外部目录：

```yaml
skills:
  external_dirs:
    - ~/myskills/thesis-reviewer
```

### OpenAI Codex

```bash
# 用户级安装
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.agents/skills/thesis-reviewer

# 项目级安装
git clone https://github.com/Agents365-ai/thesis-reviewer.git .agents/skills/thesis-reviewer
```

### OpenCode

```bash
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.opencode/skills/thesis-reviewer
```

### Pi-Mono

```bash
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.pimo/skills/thesis-reviewer
```

### SkillsMP

```bash
skills install thesis-reviewer
```

### 安装路径汇总

| 平台 | 全局路径 | 项目路径 |
|------|----------|----------|
| Claude Code | `~/.claude/skills/thesis-reviewer/` | `.claude/skills/thesis-reviewer/` |
| OpenClaw | `~/.openclaw/skills/thesis-reviewer/` | `skills/thesis-reviewer/` |
| Hermes Agent | `~/.hermes/skills/research/thesis-reviewer/` | 通过 `external_dirs` 配置 |
| OpenAI Codex | `~/.agents/skills/thesis-reviewer/` | `.agents/skills/thesis-reviewer/` |
| OpenCode | `~/.opencode/skills/thesis-reviewer/` | — |
| Pi-Mono | `~/.pimo/skills/thesis-reviewer/` | — |

## 使用方法

直接提供论文文件：

```
帮我评审这篇硕士论文：/path/to/thesis.docx
```

或英文：

```
Review this master's thesis: /path/to/thesis.docx
```

技能将自动转换、分析并生成结构化评审报告。

## 触发关键词

- 中文：论文评审、学位论文、审阅论文、论文修改意见、硕士论文、博士论文、毕业论文
- 英文：thesis review、dissertation review、thesis feedback、PhD thesis、doctoral thesis

## 输出文件

| 文件 | 说明 |
|------|------|
| `{filename}-converted.md` | 转换后的 Markdown 文本 |
| `{filename}-review-draft.md` | Phase 1 初版评审报告 |
| `{filename}-review-final.md` | 最终评审意见书 |

## 评审维度

### 1. 学术质量
摘要、绪论/文献综述、材料与方法、结果、讨论、结论、创新性 — 包含实验设计、样本量、对照组、生物学重复等学科特有检查。

### 2. 写作质量
章节间逻辑连贯性、论证严密性（论点-论据-论证）、学术语言规范、中英文摘要质量。

### 3. 格式规范
章节完整性、图表规范（编号、标题、分辨率、三线表）、参考文献格式一致性、缩略词、生物学命名规范（基因名斜体）。

### 4. 数据与结果
图表类型选择、误差线/置信区间、统计检验方法（参数/非参数）、p 值标注、多重比较校正、图表质量（坐标轴、图例、色盲友好）、可重复性。

### 5. 学术诚信
抄袭检测、图片不当处理、数据可疑、引用规范、独创性声明完整性。

### 学科专项模块

| 模块 | 覆盖内容 |
|------|----------|
| **生命科学** | 实验设计（对照、重复）、试剂/仪器记录、生物学命名（基因斜体）、数据提交（GEO/SRA）、Western blot/流式标准 |
| **医学** | 临床研究设计（CONSORT/STROBE）、伦理审批、临床试验注册、诊断试验指标、患者隐私 |
| **计算机/AI** | 算法形式化、baseline 对比、消融实验、数据泄露防范、代码可重复性、评估指标 |
| **工学** | 实验装置记录、仿真验证（网格无关性）、测量不确定度、行业标准（GB/ISO/ASTM） |
| **化学/材料** | 合成记录、表征数据（NMR/MS/XRD）、IUPAC 命名、CCDC 提交、安全规范 |
| **物理学** | 理论推导严谨性、实验误差分析、数值收敛验证、物理符号规范 |
| **人文社科** | 问卷信效度、抽样方法、内生性控制、定性编码透明度、价值-事实区分 |

### 博士论文附加维度
- **原创性贡献**：原创贡献 vs 增量改进、高水平期刊/会议发表水准
- **独立研究能力**：独立提出问题、设计研究、诊断问题的能力
- **研究体系系统性**：多章研究间的逻辑联系、层层递进的深度
- **文献综述深度**：对领域发展脉络的全局理解、经典与前沿文献覆盖、学术争议评述
- **学术成果与发表**：在读期间发表/接收论文情况、与论文内容的关联性

## 文件说明

- `SKILL.md` — 核心技能指令，所有平台加载
- `checklist.md` — 五大维度通用评审检查清单
- `output-template.md` — 评审意见书输出模板
- `disciplines/` — 学科专项检查模块（7 个学科）
- `agents/openai.yaml` — OpenAI Codex 专用配置
- `README.md` — 英文文档（GitHub 首页显示）
- `README_CN.md` — 本文件（中文文档）

## 已知限制

- **需要 markitdown MCP**：技能依赖 markitdown MCP 工具进行 .docx 转换。如未安装，需手动将论文转为 Markdown。
- **超长文档**：超过 8 万字的论文可能需要多轮读取。逐章分析的设计已缓解此问题。
- **格式检测**：部分格式问题（图片分辨率、页眉页脚）无法从 Markdown 转换中完全检测，需人工检查。
- **输出语言**：评审意见书使用简体中文输出，适用于中国高校学位论文评审场景。

## 许可证

MIT

## 支持作者

如果这个技能对你有帮助，欢迎支持作者：

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="微信支付">
      <br>
      <b>微信支付</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="支付宝">
      <br>
      <b>支付宝</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
  </tr>
</table>

## 作者

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
