---
type: project
status: active
progress: 95
created: 2026-08-28
updated: 2026-10-14
docs:
  - path: docs/DESIGN.md
    desc: 设计文档（只读不修 + 渐进式依赖 + 双输出）
  - path: SKILL.md
    desc: 技能主体（5 类检查项 + 触发词 + 降级策略）
  - path: README.md / README.en.md
    desc: 中英双语 README
  - path: scripts/scan_workspace.py
    desc: 零依赖 Python 扫描脚本（纯标准库）
---

# xiaoyaoclaw-workspace-auditor（工作区体检）

> 🔁 2026-10-14工作区体检复核：状态保持 active（内容未变更，仅刷新审计时间）

## 目标 / 背景

五件套第五件——**健康（auditor）**：家（initializer）→ 内容（memory-distill）→ 状态（tracker）→ 知识（kb-retriever）→ **健康（auditor）**。工作区质检员，只读不修。

- 设计红线：只读不修（脚本永不修改/删除任何文件）+ 渐进式依赖（缺件套自动降级跳过）+ 零依赖 Python 标准库 + 双输出（MD/JSON）
- 检查项 5 类：目录合规（initializer 规范）/ 任务健康（tracker PROGRESS.md）/ 记忆健康（memory 日志空窗 + MEMORY.md）/ 知识库健康（data_structure.md 索引孤儿 + 类型 + 超大 + 散文件）/ 垃圾临时（tmp 超龄 + 大文件）
- 阈值：--days 默认 30（超龄）/ --max-file 默认 50MB（大文件）/ 记忆空窗 7 天 / kb 超大 20MB

## 当前状态

全流程完成（95%）：开发 + 15 类场景全覆盖测试（修复 3 bug）+ GitHub 发布 + 全局技能同步（哈希 MATCH）+ 五件套 README 互链 + ClawHub 已公开（指挥官自行处理，latest 1.0.2 精简版，MIT-0）。剩余：随生态演进维护。

## 进度日志

- 2026-08-28 15:49：立项——指挥官从 4 候选（audit/report-generator/web-clipper/release-checker）拍板 workspace-audit，命名 Auditor；砍发布健康检查、加知识库健康
- 2026-08-28 15:49-16:30：开发——scan_workspace.py（os.walk + 正则 + 路径匹配）；实测真实工作区 10 findings 全命中 + 降级场景 3 skipped 通过；发布 GitHub dtsola/xiaoyaoclaw-workspace-auditor（public/main/MIT/8 topics，commit df7c01b）+ ClawHub v1.0.0 提交 + 全局技能同步 + 五件套 8 个 README 互链
- 2026-08-28 16:40-16:43：全覆盖测试——15 类场景全命中无多余无缺失；**修复 3 bug**（data_structure.md 误报索引孤儿 / 命名检查缺失 / 类型检查被跳过）；真实工作区复测噪音归零（INTERNAL_DIR_NAMES 豁免 references/templates/raw 等）；GitHub push b961903
- 2026-08-28 16:28-16:40：README 格式对齐（定制区块改引流格式 + 姊妹项目列表格式）+ SKILL.md 微调（description 删五件套文字 / 依赖件套列改完整 slug / 触发词确认）
- 2026-08-28 17:00：ClawHub 公开确认——指挥官告知已自行发布，API 验证公开可见（versions 3，latest 1.0.2，MIT-0，文档/资产已精简导向 GitHub）
- 2026-09-07 12:00-12:05：**v1.1.0 优化——补检查盲区 root-extra-dir**（liliai 工作区体检暴露：chk-audit/chk-guide/chk-pub*/skills-test 等非标准目录零命中；根因=「根目录纯净」检查只拦非 *.md 文件、一级目录仅命名检查）。补丁：check_dirs() 在 root-nonmd 后新增「根目录多余目录」检查（标准/系统/隐藏目录之外的一级目录，聚合单条 yellow 提示，agent/sessions 等 SYSTEM_DIR_NAMES 豁免）；SKILL.md 检查项表同步；脚本 VERSION 1.0.0 → 1.1.0；合成测试验证通过（3 非标目录命中 + 系统目录豁免）；本地实测后按指挥官确认将 agent 级技能运行目录 skills 加入 SYSTEM_DIR_NAMES 豁免（commit b305543）；按指挥官确认新增 ROOT_FILE_EXEMPT 根目录配置文件豁免（distill-config.json，commit 8d3faed）

## 文档索引

| 文档 | 说明 | 更新 |
|------|------|------|
| docs/DESIGN.md | 设计文档（只读红线 + 渐进式依赖 + 双输出） | 2026-08-28 |
| SKILL.md | 技能主体（5 类检查项 + 触发词 + 降级） | 2026-09-07 (v1.1.0) |
| README.md / README.en.md | 中英双语 README（五件套同构） | 2026-08-28 |
| scripts/scan_workspace.py | 零依赖扫描脚本（纯标准库） | 2026-09-07 (v1.1.0) |

<!--
使用说明（agent 维护，用户可忽略）：
- status: active | paused | archived
- progress: 0-100，时刻维护（每次更新进度日志时同步调整）
- 进度日志只追加不删除
- 重要文档：移入 docs/ 或记录路径，追加到 docs 数组（机器可读）+ 本表格（人可读）
- 项目完结：status 改 archived + 关键结论记入 MEMORY.md（供 memory-distill 蒸馏）
-->
