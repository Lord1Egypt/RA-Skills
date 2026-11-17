# <目录名 / Directory name>

## Purpose
<这个目录是干什么的、什么时候应该被检索 / What this folder holds and when it should be searched>

## Files
- <子目录/ subdir>/ — <该子目录放什么，指向其 data_structure.md / what it holds; points to its own data_structure.md>
- <file1.pdf> — <内容说明，时间/版本范围 / what it contains, time or version range>
- <file2.xlsx> — <表结构摘要，关键列 / sheet summary, key columns>

## Coverage
<时间范围、版本、来源，帮助 agent 判断优先级 / time range, version, provenance — helps the agent rank sources>

> **模板说明（可见备注，复制到知识库后可删除本段）**：每个含内容的目录放一个 `data_structure.md`，形成分层索引树；
> 可用 `scripts/build_index.py` 自动生成骨架：`python build_index.py <知识库根目录>`；
> 段落标题（Purpose / Files / Coverage）保持英文，正文语言可自由选择（中文 / 英文 / 其它）。
