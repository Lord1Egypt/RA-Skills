# thesis-docx-export

> 学术论文 Markdown → Word (.docx) 转换 + 格式校验工具集

## 这是什么

把符合学术规范（MBA / 南大 / GB/T 7714）的论文 Markdown 文件转换为 Word 文档，并在转换前后自动跑 Guardrails 校验。

**主要场景**：

1. **主 skill 配套**：`thesis-workflow-v2` 完成 Phase 1-5 后，Phase 5.2 自动调用本 skill 做 Word 转换
2. **独立使用**：用户手写完论文后，直接用本 skill 校验 + 转换

## 三步导出

```bash
# 1. 转换前：校验 Markdown 是否符合 10 项 Guardrails
python3 scripts/loop_self_check.py --file 论文_xxx.md

# 2. 转换：Markdown → Word
python3 scripts/md2docx_strict.py --input 论文_xxx.md --output 论文_xxx.docx

# 3. 转换后：校验生成的 docx 格式
python3 scripts/loop_self_check.py --file 论文_xxx.docx --verify-docx
```

## 安装

```bash
# 本 skill 是 thesis-workflow-v2 的子模块，已在仓库中。
# 软链接共享主 skill 的 Python 脚本，单一真实来源。
pip install python-docx pandoc
```

## 不做什么

- ❌ 不做内容生成（写、审、整合属于 `thesis-workflow-v2`）
- ❌ 不做 pandoc 直接转换（pandoc 不做三线表、不做 GB/T 7714）
- ❌ 不做引用文献自动抓取（用 `research_tools.py` 属于主 skill）

## 详细文档

- 格式规范清单：[references/checklist.md](references/checklist.md)
- 触发场景与边界：见 [SKILL.md](SKILL.md)
