---
name: real-estate-report-workflow
description: 房地产市场调研报告撰写工作流。涵盖住宅/商业/办公/工业地产类型的专业市场调研报告撰写。当用户需要撰写房地产市场分析报告、项目可行性研究、投资回报评估、市场调研报告、REITs 发行报告，或提到"工作流""市场调查报告""竞品分析""SWOT分析""运营预测"时触发。5 步流程 + 14 条底线原则 + 56 条专项原则，经 3 个完整项目实战验证。
---

# 房地产市场调查报告撰写工作流

> 5 步精简流程 | 全局 14 条底线原则 | 6 章 56 条专项原则
> 适用：住宅/商业/办公/工业类型（含 REITs 专项）

---

## 环境自检（首次使用必执行）

使用本技能前，助手必须执行以下自检：

### 必要工具

| 工具 | 用途 | 检查方式 |
|------|------|---------|
| `web_search` | 联网搜索市场数据、政策、竞品信息 | 尝试搜索"深圳 2025 GDP" |
| `web_fetch` | 抓取具体网页内容 | 尝试抓取任一新闻页面 |
| `write` / `edit` | 保存报告 Part 文件 | 直接调用 |
| `exec` (python3) | 运行 L1/L2 检查脚本 | `python3 --version` |
| `exec` (node) | 生成 Word 文档 | `node --version` |

### 必要 Python 包

```bash
pip3 install python-docx  # Word 文档生成
```

### 自检脚本

```bash
# 运行此脚本确认环境就绪
python3 -c "import docx; print('python-docx OK')" && \
node -e "require('docx'); console.log('docx-js OK')" && \
echo "环境就绪，可以开始使用工作流"
```

### 自检失败处理

| 缺失项 | 处理方式 |
|--------|---------|
| `web_search` / `web_fetch` | 提醒用户：当前环境缺少搜索工具，报告中的市场数据将依赖用户提供或 AI 训练数据，无法实时验证 |
| `node` / `docx` 包 | 提醒用户：`npm install docx` 以支持 Word 导出 |
| `python3` / `python-docx` | 提醒用户：`pip3 install python-docx` 以支持文档样式清理 |

---

## 流程总览

```
用户需求
    ↓
Step 0  项目定义 ─── 7维度一次性确认
    ↓
Step 1  框架设计 ─── 主框架→二/三级标题→内容要求
    ↓
Step 2  报告撰写 ─── 边写边搜，内嵌检查点，卡死自检
    ↓
Step 3  质量审核 ─── L1+L2自动化，L3抽检
    ↓
Step 4  排版导出 ─── Markdown→Word
    ↓
Step 5  项目收尾 ─── 交付、复盘、归档
```

详细工作流见 `references/core_workflow.md`。

---

## 写作原则体系

```
全局 14 条（底线）  ←  所有章节必须满足
        +
章节专项 56 条（增量） ←  各章追加
        │
冲突时：专项优先
```

### 全局原则速查

| 类别 | # | 核心 |
|------|---|------|
| 数据 | 1-4 | 来源标注、缺失处理（区间>定性>标记）、用户数据优先、近5年时效 |
| 格式 | 5-8 | 单节300-800字、超1万字拆分、时序表格化、禁emoji |
| 文风 | 9-14 | 三段式论证、禁反问句、叙事连贯、句式多样、段落式叙述、深度分析 |

详细见 `references/writing_principles.md`。

### 章节专项原则

| 章 | 文件 | 项数 |
|----|------|------|
| 一 宏观背景分析 | `references/section_rules/01_宏观背景分析.md` | 10 |
| 二 中观市场分析 | `references/section_rules/02_中观市场分析.md` | 9 |
| 三 微观市场分析 | `references/section_rules/03_微观市场分析.md` | 10 |
| 四 竞品对比 | `references/section_rules/04_竞品对比.md` | 8 |
| 五 SWOT 分析 | `references/section_rules/05_SWOT分析.md` | 10 |
| 六 运营预测 | `references/section_rules/06_运营预测.md` | 10 |

> ⚠️ 撰写每章前必须用 `read` 工具显式读取对应章节专项原则文件。

---

## 快速启动

助手收到报告撰写需求后：

1. **读取完整工作流**：`references/core_workflow.md`
2. **执行环境自检**：运行上述自检脚本
3. **从 Step 0 开始**：确认项目 7 维度（物业类型/体量/阶段/基准日期 + 应用场景/立场/读者）
4. **严格按 Step 顺序执行**，不跳跃，每步结束等待确认

---

## 关键协议

- **执行护栏**：`references/protocol.md`
- **生成前强制回顾**：每章开始前回顾全部原则 + 读取对应 `section_rules/` 文件
- **内嵌检查点**：每章完成后自动对照 Step 1 框架验证标题和内容
- **卡死检测**：同一操作≥3次无进展 → 强制中断 → 报告用户
- **增量保存**：每三级标题后立即保存，禁止依赖对话历史

---

---

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/generate_report_docx.js` | Markdown → Word 排版导出 |
| `scripts/l1_check.py` | L1 基础层自动化检查 |
| `scripts/l2_check.py` | L2 逻辑层检查 |
