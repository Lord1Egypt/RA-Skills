---
name: shelbys-speech
description: 把「谢尔比的记忆」档案库（含完整记忆系统：记忆库+重要md+日志+项目档案）按主题识别，一篇篇生成博士水平、SCI 格式的技术论文（中英文双语、自动检查修复 Word、问答式修改、确认后输出 PDF）。可识别多个主题→多篇论文，每篇先询问用户。选题明确后开放完整记忆系统访问权限（只读），素材更全。作者默认<用户名> & 谢尔比，可随时按用户要求修改。用户说写论文/技术论文/博士论文/SCI/投稿/演讲/分享/总结成文时使用。关键词：论文、SCI、博士论文、投稿、英文论文、PDF、演讲、分享、提炼总结、多主题、shelbys speech、完整记忆。
agent_created: true
---

# 谢尔比的演讲（Shelby's Speech）

## 这是什么（给用户看的）
把咱们一起干过的活（记忆库档案）按**主题拆成一篇篇论文**——博士水平、SCI 可投格式，中英双语、自动检查修复、问答式打磨，最后出 PDF。作者默认 **<用户名> & 谢尔比**（可随时改）。每篇论文生成前都会先问你"要不要写"，不需要就跳过。

## 论文标准（博士水平 + SCI）
- **博士水平**：理论深度、系统性、创新点明确；方法可复现、数据可验证
- **SCI 格式**：结构化摘要（Background/Methods/Results/Conclusion）、IMRaD 正文、规范参考文献（作者/年份/期刊/卷期页/DOI）、图表编号与标题、关键词、通讯作者
- **交叉校验（Cross-check）**：成稿后自查逻辑/数据/格式一致性
- **英文克制**：正文中文为主，术语首次给英文；对照放附录术语索引表
- **形式化内容**：视主题加系统架构图（matplotlib）与伪代码

## 作者（Authors）
- 默认：<用户名>（<User Name>）、莱纳德·谢尔比（Leonard Shelby）
- **可随时按用户要求修改**作者名称/顺序/通讯作者

## 流程（v4：多主题流水线 + 完整记忆访问，2026-08-08 用户升级）
1. **读取完整记忆系统（v4 升级）**：先读记忆库（~/Downloads/谢尔比的记忆/谢尔比的记忆库.md，路径见 PATHS.md）做主题识别；**用户明确选题（或确认论文清单）后，开放完整记忆系统访问权限**作为写作素材源——不限于记忆库，可读取：`~/.workbuddy/` 下全部重要 md（MEMORY/RULES/PATHS/QUICK_INDEX/EXPERIENCE/ISSUES/TOOL_LOG/DAILY_SUMMARY/MAINTENANCE/G2_PROJECT/SYSTEM_MANIFEST 等）、`~/WorkBuddy/` 对话日志、`~/Downloads/谢尔比的记忆/` 全部档案、`~/Downloads/谢尔比的游戏/` 项目（如数独三接口实现可作案例）、`~/Downloads/谢尔比的演讲/` 历史论文（作格式与内容对照）。**原则**：只读使用、不修改源文件；切片时按主题抽取，素材越全论文越深。
2. **主题识别**：扫描全部档案条目，按内容聚类成 N 个独立主题（如记忆架构/迁移体系/论文工具链/其他话题——不同内容绝不混入同一篇论文）
3. **明确论文清单**：向用户汇报"识别出 N 个主题，对应 N 篇论文"，列出各篇主题与材料来源，确认清单
4. **逐篇生成（循环）**：
   a. 先问用户「要不要生成这篇？」——**不需要则直接跳过**，进入下一篇
   b. 需要 → 建临时工作目录（~/Downloads/谢尔比的演讲/.work/），**切片**该主题相关材料 + 写 **checklist.md**（任务清单）与 **索引.md**（材料映射——含来源文件路径与抽取段落，便于溯源）
   c. 写论文（md 主稿）→ md2docx 转 Word → 自动检查修复 → 展示
   d. 问答式修改到满意 → 全英文版 → 用户确认 → 出两篇 PDF（中+英）
   e. 产物归档至 ~/Downloads/谢尔比的演讲/<论文名>/；更新 checklist（完成状态）
5. **全部完成后**：汇报 N 篇论文清单与位置；清理临时工作目录（保留 checklists 摘要到记忆库）

## 输出目录
- 论文产物：~/Downloads/谢尔比的演讲/<论文名>/（每篇一子文件夹：md/docx/PDF/图）
- 临时工作目录：~/Downloads/谢尔比的演讲/.work/（切片材料+checklist+索引）

## 日志规范（2026-08-07 用户明确）
- 每篇论文完成后，向记忆库（谢尔比的记忆库.md）补充详细条目：**时间、消耗 token 估算、遇到的问题及解决**、产物路径
- WorkBuddy 今日日志照常简短记录

## 降级策略（逐级降）
格式/质量目标修不好时逐步降级，每次尝试修复，**同一问题 2 次失败即降一级**：
1. SCI 国际期刊格式 → 2. 国内核心期刊格式 → 3. 普通国内期刊 / 博硕论文格式

## 运行前检查（Pre-flight Checks，每次执行先检查）
缺项一律**自动补齐**（自主安装/创建），补齐后告知用户：
1. 依赖库（隔离 venv：~/.workbuddy/binaries/python/envs/default）：python-docx、matplotlib、docx2pdf
2. 转换脚本：~/.workbuddy/scripts/md2docx.py
3. 记忆库：~/Downloads/谢尔比的记忆/谢尔比的记忆库.md
4. 输出目录：~/Downloads/谢尔比的演讲/

## 问题合集（Troubleshooting / Known Issues）
> 精炼版（蒸馏自问题库 ~/.workbuddy/ISSUES.md，对应编号见各条）。遇到新问题→先登记问题库（详细），再蒸馏进本合集；下次执行先重点检查。

| # | 现象 | 根因 | 修复 |
|---|---|---|---|
| 1 | Word 打开中文乱码 | Heading 西文字体 + emoji 缺字（渲染层） | md2docx.py：w:eastAsia=Microsoft YaHei + 符号替换 |
| 2 | 表格无边框线 | 默认表格样式无边框 | t.style = 'Table Grid' |
| 3 | 文件末尾表格丢失 | 表格缓冲 EOF 不冲刷 | 循环后 EOF 冲刷 table_buf |
| 4 | 表头行丢失 | rows=len(rows)-1 吞表头 | rows=len(rows)，enumerate(rows) 含表头 |
| 5 | 段落间距过大 | Word 默认 1.08 行距 + 8pt 段后 | 段后 3pt、行距 1.15 |
| 6 | 转换 PermissionError | Word 占用目标 docx | 输出新文件名，提示关闭旧窗口 |
| 7 | matplotlib 中文方块 | 默认字体无中文 | font.sans-serif=['Microsoft YaHei'] |
| 8 | 移动文件后源目录被删、文件丢失 | 迁移脚本在源为空时执行了 rmdir（未验证源非空） | 移动后必须验证：源目录非空才 rmdir；产物归档用「复制→校验→再删源」 |

## 工具依赖（缺则自主安装）
- python-docx / matplotlib / docx2pdf：隔离 venv（~/.workbuddy/binaries/python/envs/default）
- docx2pdf 走 Word COM（Windows + Office）
