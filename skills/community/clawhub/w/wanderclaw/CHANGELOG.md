# 虾游 Changelog

## v3.2.4 (2026-04-20)

### Cron 注册最终一致性 — 解决 gateway busy 时 cron add 批量失败

**根因**：OpenClaw `cron add` CLI 通过 WebSocket 调 gateway；在主 agent 刚跑完 setup.sh + 冷启动三连时 gateway 正忙，CLI 等不到响应就超时 → 6 个注册任务成功率不稳定（实测一次仅 1/6 成功）。

**修复思路**：把"一次性注册"变成"最终一致性注册"——失败了不算结束，下次激活时自动补。

- `scripts/schedule-cron.sh` 重写：
  - 每条 `cron add` 内置 3 次重试（0s → 3s → 8s 指数退避）
  - 不同任务之间固定 2s 间隔，避免集中打爆 gateway
  - 重试仍失败的任务，以可执行 `.cmd` 文件形式写入 `wanderclaw/pending-cron/` 队列
  - 脚本开头自动 drain 这个队列，成功的移除，失败的保留
  - 新增 `--drain-only` 标志：只补 pending，不新增（幂等可多次调用）

- `SKILL.md` 激活规则新增"静默副任务"：每次被触发时，如发现 `pending-cron/` 有待办，后台调用 `schedule-cron.sh --drain-only`，不打扰用户。队列彻底清空时可顺口报告一下。

- 对用户的承诺：cron 注册变成"最终会成功"而不是"要么成要么失败"。用户不再需要手动 ssh 上去重跑脚本。

---

## v3.2.3 (2026-04-20)

### DORMANT 模型 + 一次性安装提示
新用户完整体验测试（see docs/user-journey-test-2026-04-20.md）发现：用户刚装 skill 说"嗨？"时 agent 不触发虾游，用户也不知道要说"虾游"才行——UX 可发现性盲点。

按项目定位（虾游是主 agent 的一个**角色/工具**，不抢主 identity），改动：
- **SKILL.md frontmatter 重写**：删 `MANDATORY FIRST ACTIONS (on EVERY user message)`，改为 `ACTIVATION KEYWORDS` 显式列表（虾游/探索/明信片/深潜/收藏/黑名单/cron）+ `DORMANT 行为` 明确"没触发就不介入"
- **SKILL.md body "⚡ 首次激活" 章节**：对齐 dormant 模型，开头就告知"用户说不含关键词的消息时，本 skill 不介入，主 agent 按自己节奏回"
- **setup.sh 尾部**：向当日 `memory/YYYY-MM-DD.md` 追加一段一次性 onboarding 提示（附 `<!-- wanderclaw-install-nudge -->` 标记防重复）。主 agent 按 AGENTS.md 规范启动时会读当日 memory → 下次对话时自然地提一句"顺便说，你装了虾游，想试试说'虾游'"→ 提完自行删除该段落。完全不创建 workspace 根目录的新文件，不改 AGENTS.md/SOUL.md/USER.md。

### v3.2.2 合并内容
- 反幻觉硬性规则（声称必须有 tool 输出证据 / 不凭记忆猜兴趣 / 不手写替代 setup.sh / 脚本输出必须转述）
- Step 2/3/4 改命令式

---

## v3.2.2 (2026-04-20)

### 行为层修复 — 阻止幻觉与虚报
真实环境测试（远端 OpenClaw 实例）暴露出 skill 描述性 TRIGGER RULES 被 agent 当作背景信息忽略的问题，导致：
- Agent 收到 "嗨，虾游？" 后只回随意问候，不检查 state.json、不走 onboarding
- 显式请求 onboarding 时 agent 从记忆幻觉用户兴趣（没问用户），自己 mkdir+cp 建 state.json 漏 5 个字段
- 声称 "✅ 5个定时任务已注册"，实际 `openclaw cron list` 为空

本版本改动：
- **SKILL.md frontmatter** — TRIGGER RULES 改为 MANDATORY FIRST ACTIONS（命令式 + 必须 Bash 跑 `ls state.json`）+ ANTI-FABRICATION RULES 三条
- **SKILL.md 首次激活区** — 新增"⛔ 反幻觉硬性规则"章节，禁止：声称未执行的事 / 推测用户兴趣 / 替换 setup.sh / 不转述脚本输出
- **Step 2** — 明确"必须问，不准猜"，禁止从 memory/USER.md/prior session 推断兴趣
- **Step 3** — 要求通过 Bash 工具一字不差执行 `exec bash setup.sh`，禁止手写 mkdir+cp 替代（手写会漏字段）；脚本 stdout 必须转述给用户
- **Step 4** — 要求把 schedule-cron.sh 的成败统计行原文贴给用户；openclaw cron add 部分失败时必须如实告知

### v3.2.1 合并内容
- state.json 模板补全 direction_blacklist / favorites / exploration_stats
- schedule-cron.sh 真实统计成败（openclaw 缺失时 exit 1）
- SKILL.md Step 3 改为 exec bash setup.sh（单一初始化入口）
- CHECKLIST 补字数校验、删 fix-null-cards.py / rebuild-index.py 死引用

---

## v3.2.0 (2026-04-20)

### 冷启动可靠性修复
- **修复冷启动三连探索不触发的问题**
  - 根因：OpenClaw `--at` 一次性定时器注册后 state 为空，从未触发
  - 方案：冷启动不再依赖 at cron，改为 onboarding 流程中在当前 session 直接执行
- schedule-cron.sh 删除冷启动 cron 注册部分
- SKILL.md Step 4/5 重写：注册日常 cron → 直接执行三连探索
- 断点续做：cold_start_progress < 3 时，下次触发自动补完剩余探索

---

## v3.1.0 (2026-04-19)

### 最终版
- README 新增真实明信片示例（#003 多 Agent 协作、#033 含羞草计数）
- 新增参赛说明 PITCH.md
- 修复 cron message 语法错误
- 清除所有硬编码路径
- 部署服务器安装测试通过 ✅

---

## v3.0.0 (2026-04-19)

### 精简发布

经过 41 轮自动迭代后的精简版本——保留有价值的改进，去掉过度工程化的部分。

**精简：**
- EXPLORER.md: 421→301 行（删除冗余 checklist、归一化映射表、Python GATE 代码块）
- state.json 模板: 35→14 行（只保留核心字段）
- postcard-format.md: 146→69 行（去重、简化字数规则）
- 删除迭代产物文件

**保留的有价值改进（来自 41 轮迭代）：**
- 搜索失败处理与 fallback 重试链
- POST-EXPLORATION CHECKLIST（精简为 5 项）
- character_card 必填规则
- 收藏模式（收藏/取消/查看列表）
- 探索方向黑名单
- 来源多样性规则
- sources.yaml 新增 ScienceDaily 等源
- explorer-templates.md 格式模板拆分

---

## v2.3.0 (2026-04-19)

- 周度总结 cron（周日 10:00）
- 深潜模式（周六 22:00，深度源，450-600字，≥8分门槛）
- 明信片关联索引 postcard-index.json
- 冷启动提速（第1次从 30s→15s）
- 移除 outbox.json（Skill 版无需）
- 初始化统一（setup.sh 为唯一入口）

---

## v2.1.0 (2026-04-13)

- Skill 版发布，支持 clawhub install
- 三层水域信息源架构
- 冷启动三连探索 + 日常 4 次定时探索
- 兴趣图谱自动演化
- 圆桌奇遇模式 + 人物卡系统
- 反馈机制（👍/👎 权重调整）
