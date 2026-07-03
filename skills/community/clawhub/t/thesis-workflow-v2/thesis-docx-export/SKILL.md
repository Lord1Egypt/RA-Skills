---
name: thesis-docx-export
description: "Convert academic thesis markdown (.md) into a Word (.docx) document that meets the MBA / 南大 / GB/T 7714 formatting spec, and run the 10-item Guardrails check before and after export. Triggers: 导出 Word / 转换为 docx / 论文格式校验 / Guardrails 校验 / md2docx / 三线表 / 分页符 / GB/T 7714 参考文献格式. Required by `thesis-workflow-v2` Phase 5.2; can also be invoked standalone after manual writing."
platforms: [linux, macos, windows]
metadata:
  clawdbot:
    emoji: "📄"
    version: "1.0.0"   # 单一真实来源；主 skill thesis-workflow-v2 仅在 Phase 5.2 阶段引用本 skill
    requires: {}
    os: ["linux", "darwin", "win32"]
---

# Thesis DOCX Export

把学术论文 Markdown 转换为符合学术规范的 Word 文档，并在导出前后自动跑 Guardrails 校验。

本 skill 是 `thesis-workflow-v2`（主 skill）Phase 5.2 阶段的"出口工序"——主 skill 完成 Phase 1-5 内容生产后，调用本 skill 做 Word 转换和最终格式校验。本 skill **也可以独立调用**：用户手写完论文后，直接用本 skill 做导出。

> **核心原则**：本 skill 不做内容生成（写、审、整合都是主 skill 的事）。本 skill 只做"格式合规"：校验 → 转换 → 再校验。

## ⚠️ 调用矩阵

| 触发场景 | 选择 |
|---------|------|
| 主 skill `thesis-workflow-v2` 跑到 Phase 5.2 | ✅ 本 skill（自动调用，无需用户手动触发） |
| 用户手写论文后想导出 docx | ✅ 本 skill（standalone 调用） |
| 用户只想校验 Markdown 是否符合学术规范 | ✅ `python3 scripts/loop_self_check.py --file 论文.md`（只校验、不导出） |
| 用户想用 pandoc / python-docx 直接生成 Word | ❌ 本 skill（pandoc 不做三线表、不做 GB/T 7714 排序） |

**反模式：** 不要把本 skill 用于"内容生成"——主 skill 的 Phase 2 写作、Phase 3 审核、Phase 4 整合都由 `thesis-workflow-v2` 负责。本 skill 只接受已完成的 Markdown 输入。

## 核心能力

### 1. Guardrails 10 项自动校验

`scripts/loop_self_check.py` 在转换前后各跑一次：

```bash
# 转换前校验 Markdown 内容（10 项 Guardrails）
python3 scripts/loop_self_check.py --file 论文_xxx.md

# 转换后再校验生成的 docx（Word 格式校验）
python3 scripts/loop_self_check.py --file 论文_xxx.docx --verify-docx
```

**10 项校验项详见 [references/checklist.md §六](references/checklist.md)**。

### 2. Word 格式转换

`scripts/md2docx_strict.py` 把符合 Guardrails 的 Markdown 转为 docx，应用以下格式：

| 维度        | 规则                                                     |
|-------------|----------------------------------------------------------|
| 正文加粗过滤 | 正文段落内的 `**text**` 全部转为普通文字（无强调术语）   |
| 表格加粗过滤 | 表格单元格内的 `**` 同步清除                             |
| 三线表      | 顶线 1.5 磅 / 表头底线 0.75 磅 / 底线 0.5 磅，无竖线     |
| 分页符      | 每章标题前插入分页符（首章跳过），附录/致谢前分页         |
| 字体         | 中文宋体 / 英文 Times New Roman / 标题黑体                |
| 行距         | 正文 20 磅                                               |

**反模式：** 不要用 `pandoc 论文.md -o 论文.docx` 走捷径——pandoc 不做加粗过滤、不做三线表、不做 GB/T 7714 排序；出来的 docx 必须经 `loop_self_check.py --verify-docx` 二次校验才能交付。

## 入口与依赖

### 入口

```bash
# 校验 + 转换 + 再校验 一条龙
python3 scripts/loop_self_check.py --file 论文_xxx.md
python3 scripts/md2docx_strict.py --input 论文_xxx.md --output 论文_xxx.docx
python3 scripts/loop_self_check.py --file 论文_xxx.docx --verify-docx
```

### 依赖

- `python-docx`（Word 写入）
- `pandoc`（Markdown 预处理）
- 标准 Python 3.9+ 库

### 反向依赖

本 skill **被** `thesis-workflow-v2`（主 skill）Phase 5.2 引用。如果本 skill 不可用，主 skill 的 Phase 5.2 步骤会失败。

## 文件结构

```
thesis-docx-export/
├── SKILL.md                    ← 本文件
├── README.md                   ← 用户使用说明
├── CHANGELOG.md                ← 版本日志
├── scripts/
│   ├── md2docx_strict.py       ← Word 转换器（软链接 → ../../scripts/md2docx_strict.py）
│   └── loop_self_check.py      ← Guardrails + Word 校验（软链接 → ../../scripts/loop_self_check.py）
└── references/
    └── checklist.md            ← 18 项格式规范 + 10 项 Guardrails 校验项 + Phase 退出门禁
```

> **单一真实来源原则**：`md2docx_strict.py` 和 `loop_self_check.py` 的真身在主 skill `scripts/` 目录，本目录用软链接共享——避免代码 drift。

## 18 项格式规范（人工对照清单）

完整清单在 [references/checklist.md](references/checklist.md)，核心维度：

- **格式维度（18 项）**：封面 / 原创性声明 / 中英文摘要 / 目录 / 章节标题层级 / 段落 / 图号图题 / 表号表题 / 表格 / 图表编号 / 注释 / 参考文献 / 页码 / 附录 / 致谢 / 写作语法
- **大纲维度（2 项）**：章节范围 + 章节结构
- **内容准确性（2 项）**：引用标注 + 数据自洽
- **查重风险（1 项）**：30 字以上连续重合
- **学术规范（6 项）**：引用完整率 + 术语缩写 + 中英文格式

## 违规等级

| 等级    | 标记 | 处理                                       |
|---------|------|--------------------------------------------|
| 🔴 P0   | 致命 | **必须修复**（章节缺失、参考文献缺失、合并残留） |
| 🟡 P1   | 严重 | **必须修复**（标题层级错误、加粗残留、字数不足） |
| ⚠️ P2   | 一般 | 建议修复（引用缺失、图表编号不规范）         |
| 💡 建议 | 优化 | 可选（措辞、过渡句式）                      |

## 维护与支持

- 维护者：`thesis-workflow-v2` 同 owner
- 主 skill 引用：本 skill 在 `thesis-workflow-v2/SKILL.md` 的 Phase 5.2 段被引用
- Bug 报告：在 GitHub `mba-thesis-workflow` 仓库的 issue 列表提，标签 `thesis-docx-export`
