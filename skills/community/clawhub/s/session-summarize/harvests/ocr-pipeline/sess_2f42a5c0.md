# sess_2f42a5c0 — 内证观察笔记 OCR→AI结构化→思源导入

> 项目: ocr-pipeline | 日期: 2026-06-28

## 项目总结

将492页扫描版内证观察笔记从OCR文本转换为结构化知识库（5编×30卷×章节层级+知识闪卡），导入思源笔记。

## 关键决策

1. PaddleOCR 2.8.1（非3.x，避免OneDNN bug）+ Python 3.12 → 中文OCR最佳方案
2. DeepSeek API逐章AI重构（¥0.06批量处理12万字，0失败）→ 替代规则脚本
3. 先拆章节再逐章处理 → 避免单次调用超长上下文
4. 最终组装后一次导入 → 避免反复创建多个版本文档

## 文件清单

| 路径 | 说明 | 状态 |
|------|------|:----:|
| 内证观察笔记_重构版.md(325KB) | 最终结构化Markdown | ✅ 保留 |
| 20260628193314-7pa44lb.sy(884KB) | 思源文档 | ✅ 已导入 |
| chapters/ (30文件) | 临时章节拆分 | 🗑️ 已清理 |
| chapters_restructured/ (30文件) | 临时AI重构输出 | 🗑️ 已清理 |
| *.py (脚本) | 提取/API/组装脚本 | 🗑️ 已清理 |

## 已知坑点

| 坑 | 原因 | 解决 |
|:---|:---|:---|
| PaddleOCR 3.x崩溃 | OneDNN bug | 锁定2.8.1+2.6.2 |
| createDocWithMd标题="未命名" | custom-sy-title-empty覆盖 | 事后renameDoc |
| removeDoc残留在recent-doc.json | API不清理状态文件 | 手动编辑recent-doc.json |
