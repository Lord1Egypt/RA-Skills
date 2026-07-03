# 触发方式与输出示例

## 触发规则

**唯一触发词**：`总结` 或 `summarize`，且必须作为独立词单独发送。

| ✅ 会触发 | ❌ 不会触发 |
|-----------|-------------|
| `总结`（单独发送） | "总结一下今天的工作"（在句中） |
| `summarize`（单独发送） | "帮我总结一下进度"（在句中） |
| `总结 统计`（独立词+参数） | 会话达到任意阈值（无自动提醒） |

> ⚠️ 无自动提醒、无定时触发、无其它激活路径。仅独立词触发。

## 输出示例（L0 正常，完整输出）

```
┌─ 📋 ZCodeProject — 完成 summarize 技能 WorkBuddy 发布适配
│
│  🎯 主任务
│    发布 summarize v6.6.2 到 WorkBuddy 技能市场
│    进度 ████████░░ 80%
│    > 完成: Frontmatter规范化、正文瘦身到~490行、输出格式重写
│    > 待办: 最终验证、Git push
│    > 阻塞: —
│
│  📌 次任务
│    跨平台适配完善  ██████████ 100%
│    > 5平台路径自动检测 + 写入目标变量化
│    文档拆分整理      ██████░░░░ 60%
│    > CHANGELOG/trigger-examples 等5个references文件已创建
│  ──────────────────────────────
│  📁 涉及文件(8)
│    ✏️ 修改: SKILL.md, README.md, VERSION, _self-stats.md
│    ➕ 新增: references/CHANGELOG.md, references/trigger-examples.md, references/installation.md
│    🗑️ 删除: —
│  ──────────────────────────────
│  ✅ 本轮完成(5)
│    - Frontmatter 字段规范化（删3非法字段 + 加 license/compatibility）
│    - description 重写为第三人称中英双语
│    - SKILL.md 从773行瘦身至约490行
│    - 输出格式重写（主/次任务分层 + 进度条）
│    - install 脚本移至 scripts/ 目录
│  ⏳ 待办(3)
│    - 验证所有 references 文件引用完整性
│    - Git commit + push to GitHub
│    - WorkBuddy 技能市场提交审核
│  ──────────────────────────────
│  💡 下一步
│    1. 验证 SKILL.md 行数 ≤500、frontmatter 字段合法
│    2. 运行 git add + commit + push
│    > 注意：push 前确认 VERSION 文件已更新为 6.6.2
│  ──────────────────────────────
│  📊 ~12轮 ｜ 压力 🟢(40%)
│
│  ⚠️ 错误(0): —
│  🛡️ 规则: 3/3 ✅ ｜ 0/3 ⚠️
│  💡 即时优化(0): —
│
│  ⚡ 成功经验(2):
│    ├ ⚡ 路径: 文档拆分→先写references再瘦身主文件，避免引用断裂
│    └ 🔬 效用: replace_in_file精确替换 > write_to_file重写（保留git历史）
│
│  📝 写入(2):
│    ├ → 全局级(1): ⚡路径: 文档拆分策略
│    └ → 项目级(1): 🏗️架构: summarize v6.6.2 目录结构
│
│  🪖 Headroom: 正常 (12,340 token) ｜ Kompress
└─────────────────────────────────────────
```

## 输出示例（L3 降级，仅进度+事实）

```
📋 ZCodeProject —— summarize 发布适配 | 🎯 WorkBuddy适配 80%
📁 文件(8): SKILL.md, README.md, VERSION, references/CHANGELOG.md, ...
💡 下一步: 验证引用完整性 → Git push
⚠️ 降级 L3 | 模块5仅内存 | 检查L0规则
```

## 输出示例（L4 极限降级，单行摘要）

```
📋 ZCodeProject —— summarize 发布适配 | 🎯 WorkBuddy适配 80% | 📁8 | ⚠️ L4降级
```
