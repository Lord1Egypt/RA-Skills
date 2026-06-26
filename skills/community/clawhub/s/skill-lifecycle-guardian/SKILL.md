---
name: skill-lifecycle-guardian
description: >
  Skill 全生命周期守护者。—— 每日自动扫描所有 workspace，检测新增/变更的 Skill。
  功能一：动态发现所有 agent workspace 下的 Skill，无需手动配置扫描范围。
  功能二：功能重叠检测（新增时），若发现相似/重复则发出提醒。
  功能三：新增/变更 Skill 自动生成或更新使用指南。
  功能四：更新总览 README.md。
  V2 升级：hash 变更检测 + 自动更新指南 + 静默退出 + 无 YAML frontmatter 兼容。
  V2.0.10：安全加固——cron 指令引用化（消除 Shadow Command）、guardian-check.sh 路径白名单校验。
  V2.0.11：通知策略优化——3h 扫描静默化（有变更通过 message 工具通知），每日 6:00 改为推送每日汇总；文档增加可调参数说明。
  V2.0.12：安全审查修复——添加文件写操作显式声明、手动触发限定管理员范围、消除触发意图歧义。
  手动触发：用户说"检查新技能"、"有没有重复的skill"、"生成使用指南"、"更新指南"、"更新 README"、"刷新技能列表"等。
---

# Skill Lifecycle Guardian — 技能全生命周期守护者 (V2)

> ⚠️ **安装后必做**：本 Skill 依赖定时 cron 驱动。`guardian-check.sh` 已包含在本 Skill 目录中，确认执行权限即可：
> ```bash
> chmod +x ~/.openclaw/workspace/skills/skill-lifecycle-guardian/guardian-check.sh
> ```
> 
> 然后创建两个 cron job（子 agent 会读取本 SKILL.md 公开文档中的工作流程执行）：
> 
> **① 每日 6:00 全量扫描**（兜底 + 每日汇总通知）：
> ```bash
> openclaw cron add --job '{
>   "name": "skill-guardian-daily-scan",
>   "schedule": {"kind":"cron","expr":"0 6 * * *","tz":"Asia/Shanghai"},
>   "sessionTarget": "isolated",
>   "payload": {"kind":"agentTurn","message":"请读取 ~/.openclaw/workspace/skills/skill-lifecycle-guardian/SKILL.md，严格按「工作流程」章节执行每日扫描。","timeoutSeconds":300},
>   "delivery": {"mode":"announce"}
> }'
> ```
> 
> **② 每 3 小时变更检测**（有变更即时通知，无变更静默）：
> ```bash
> openclaw cron add --job '{
>   "name": "guardian-change-detector",
>   "schedule": {"kind":"cron","expr":"0 */3 * * *","tz":"Asia/Shanghai"},
>   "sessionTarget": "isolated",
>   "payload": {"kind":"agentTurn","message":"请读取 ~/.openclaw/workspace/skills/skill-lifecycle-guardian/SKILL.md，严格按「工作流程」章节执行扫描。检测到变更时，使用 message 工具将结果发送给管理员。无变更则静默结束。","timeoutSeconds":600},
>   "delivery": {"mode":"none"}
> }'
> ```
> 
> **🔧 通知策略可调**（以上为推荐默认值，可按需修改）：
> - `delivery.mode`：`"announce"` 每次运行都推送 / `"none"` 仅变更时通过 message 工具推送
> - `delivery.channel` / `delivery.to`：按你使用的渠道修改（wecom、discord 等）
> - `schedule.expr`：扫描频率，不推荐短于每 3 小时或长于每天 1 次
> - 只需日报、不需要即时变更通知 → 只保留 cron ① 即可
> - 两个 cron 都关闭推送、纯靠手动触发 → 两个 delivery 均设为 `"none"`
> 
> **行为透明**：以上 cron 触发子 agent 后，子 agent 仅读取本 SKILL.md 公开文档中记录的工作流程执行。操作范围限于 skill registry、user-guides/ 目录和 README.md，不会执行本文档未声明的行为。
> 
> 不创建 cron 则本 Skill 只能手动触发，不会自动守护。

> ⚠️ **文件写操作声明**：本 Skill 运行时会修改以下持久化文件，安装即视为授权：
> - `memory/skill-registry.json` — 更新各 Skill 的 MD5 hash 记录
> - `skills/user-guides/*.md` — 生成或覆盖更新使用指南
> - `skills/user-guides/README.md` — 更新功能总览索引
> 
> 本 Skill 不会在声明范围外执行文件写操作。以上文件均位于安装者 workspace 内，不涉及系统目录。

守护 Skill 全生命周期：发现新建 → 检测变更 → 生成/更新指南 → 维护总览。

## 触发条件

本 Skill 的触发分为自动和手动两类。

### 自动触发（cron 驱动）
- **每日 6:00 全量扫描**：hash 对比检测新增和变更，有变更时执行完整流程
- **每 3 小时变更检测**：同上，有变更时通知到企微

### 手动触发（用户意图识别）

> ⚠️ **触发范围限定**：以下手动触发仅在管理员/安装者的对话中生效。普通用户说"检查新技能"不会被误解释为管理指令。AI 通过对话上下文判断发言者身份和真实意图，非简单关键词匹配。

| 用户意图 | 触发示例 | 执行操作 |
|----------|----------|----------|
| 安装后立即扫描 | "检查新技能"、"扫一下新 skill"、"新技能登记" | 全量扫描 + 重叠检测 + 生成指南 |
| 检查功能重复 | "有没有重复的 skill"、"检查重叠"、"这两个是不是冲突" | 重叠检测 |
| 生成/更新指南 | "生成使用指南"、"更新指南"、"给 XX 写个指南" | 生成/更新 user-guides/ |
| 刷新技能总览 | "更新 README"、"刷新技能列表"、"重新整理列表" | 更新总览 README |

### 修改事件触发（AI 行为约束）
当 Skill 的 SKILL.md 被修改后，AI 应在同一轮对话中触发守护者扫描。此行为依赖使用者在其 AI 助手中配置行为规则。未配置时由 3h cron 兜底。

## 数据存储

registry 文件路径：`~/.openclaw/workspace/memory/skill-registry.json`

```json
{
  "skills": {
    "<skill-name>": {
      "path": "/path/to/SKILL.md",
      "dirname": "dirname",
      "description": "...",
      "hash": "md5-of-skill.md-content"
    }
  },
  "lastScan": "ISO8601-timestamp"
}
```

**hash 计算方式**：读取 SKILL.md 全文，计算 MD5（`md5sum` 或等价方式）。用于变更检测。

## 工作流程

> **输出原则**：中文输出，禁止推理过程/中间步骤/英文 preamble。无变更时仅回复一句确认。有变更时简报 ≤3 行。

### 第零步：变更检测（每日扫描专属）

**仅在每日定时扫描时执行。手动触发跳过此步，直接进入第一步。**

1. 执行 `bash ~/.openclaw/workspace/skills/skill-lifecycle-guardian/guardian-check.sh` 进行确定性 hash 对比
2. 脚本输出 `NO_CHANGES` → 回复「🔍 技能守护者扫描完成，无变更。」，结束
3. 脚本输出 `CHANGES:...` → 继续以下流程：

4. 汇总变更结果：`检测到 N 个新 Skill、M 个变更 Skill`
5. 更新 registry：所有扫描到的 Skill 的 hash 写回 registry，更新 `lastScan`
6. 如果 N + M = 0 → 统一回复：「🔍 技能守护者扫描完成，无变更。」

### 第一步：发现新 Skill

确定目标 Skill 的 SKILL.md 路径和内容：

```bash
# 列出所有 skill 目录（三个来源合并扫描）
ls -d ~/.openclaw/workspace/skills/*/SKILL.md ~/.openclaw/plugin-skills/*/SKILL.md ~/.openclaw/skills/*/SKILL.md 2>/dev/null
```

**扫描范围**（动态发现，不再硬编码）：

守护者读取 `openclaw.json` 中所有 agent 的 `workspace` 字段，自动发现所有 `{workspace}/skills/` 目录：

```
openclaw.json → 遍历 agents.list[].workspace → 找 {workspace}/skills/
  ├─ /root/.openclaw/workspace/skills/        (main agent)
  ├─ /root/.openclaw/workspace-team/skills/    (team agent)
  ├─ /root/.openclaw/workspace-study/skills/   (study agent)
  └─ ... 以后新增的 workspace 自动加入
```

加上两个系统级目录：
- `~/.openclaw/plugin-skills/` — 插件市场安装的 Skill
- `~/.openclaw/skills/` — 系统级 Skill

所有目录合并后去重（以 `name` 字段为准），确保不遗漏任何 Skill。

读取新 Skill 的 `name`、`description` 和正文内容。

### 第二步：功能重叠检测

**仅对新 Skill 执行。变更的 Skill 跳过此步。**

对比新 Skill 与所有已有 Skill，判断是否功能重叠。

**检测方法**：

1. 读取每个已有 Skill 的 SKILL.md frontmatter（name + description）
2. 从新 Skill 的 description 和正文中提取核心功能关键词
3. 与每个已有 Skill 逐一对比，重点关注：
   - 目标用户群体是否相同
   - 核心操作是否重叠（如：都是管理待办、都是搜索）
   - 触发词是否冲突
4. 判定结果分三档：

| 重叠等级 | 判定标准 | 处理方式 |
|----------|----------|----------|
| 🔴 高度重复 | 核心功能几乎一致，触发词重叠 | **必须提醒**，建议合并而非新建 |
| 🟡 部分重叠 | 部分功能交集，但各有侧重 | **建议提醒**，说明重叠点和差异点 |
| 🟢 无重叠 | 功能独立，无冲突 | 正常通过 |

**输出格式**（仅在检测到重叠时输出）：

```
⚠️ 功能重叠提醒

新 Skill：{new-skill-name}
已有 Skill：{existing-skill-name}
重叠等级：🔴高度重复 / 🟡部分重叠

重叠点：{具体描述}
差异点：{具体描述}
建议：{合并/保留两者/调整触发词}
```

**已知的易混淆对**（铁律1延伸）：
- tencent-agent-storage（网盘）≠ tencent-cloud-cos（对象存储）
- wecom-edit-todo（企微待办）≠ personal-assistant（个人助理待办）
- wecom-doc-manager（企微文档）≠ tencent-docs（腾讯文档）

### 第三步：生成 / 更新用户使用指南

**新 Skill → 生成指南；变更的 Skill → 覆盖更新已有指南。**

**目标目录**：`~/.openclaw/workspace/skills/user-guides/`

**生成流程**：

1. 读取 Skill 的 SKILL.md 全文
2. 判断用户可见性（见下方规则）
3. 如果是内部工具 → 跳过指南生成
4. 如果是面向用户的 Skill：
   - 提取核心功能点
   - 为每个功能点编写自然语言示例
   - 生成指南文件

**文件命名**：按编号递增，格式 `{NN}-{中文名称}.md`
- 查询现有最大编号：`ls ~/.openclaw/workspace/skills/user-guides/ | grep -oP '^\d+' | sort -n | tail -1`
- **新 Skill**：新编号 = 最大编号 + 1
- **变更 Skill**：找到已有指南文件，就地覆盖更新（编号不变、文件名不变）

**指南格式**（严格遵循）：

```markdown
# {功能名称}使用指南

{emoji} **{一句话描述}**

## {主要操作1}
- 示例语句1
- 示例语句2

## {主要操作2}
- 示例语句1
- 示例语句2

💡 小提示：
- 提示1
- 提示2
```

**关键原则**：
- 每个操作配2-3个自然语言示例，让用户知道怎么说话
- 示例必须是**用户视角**的自然对话，不是命令行
- 小提示写用户容易忽略的注意事项
- 篇幅控制在15-30行，简洁为主

### 第四步：更新总览 README.md

更新 `skills/user-guides/README.md`：

1. 读取当前 README.md
2. 根据 Skill 的性质归类到对应分类（日常办公/文档与数据/信息获取/特色功能，或新增分类）
3. **新 Skill**：在对应分类表格中追加一行
4. **变更 Skill**：如果分类未变，更新对应条目；如果分类变了，移动条目
5. 编号重新排列确保连续

**如果 Skill 属于内部/开发者工具**：
- 不生成用户指南
- 在 README.md 的"未列入的内部工具"部分追加/更新条目

## 用户可见性判断

在生成指南前，先判断该 Skill 是否面向普通用户：

**面向用户**（生成指南）：
- 功能通过自然语言对话即可使用
- 不需要技术背景（编程、CLI、API）
- 触发词是日常用语

**内部工具**（不生成指南，仅列入内部列表）：
- 需要编程/CLI操作
- 是其他 Skill 的依赖或内部调用
- 仅管理员/开发者使用
- 功能高度技术化（如浏览器自动化、CI/CD）

## 边界情况

| 场景 | 处理 |
|------|------|
| 新 Skill 与已有 Skill 高度重复 | 提醒用户，不自动合并，等用户决策 |
| Skill 内容变更 | 重新生成对应指南、更新 README（如需要） |
| 已有 Skill 被删除 | 从 registry 移除、保留指南文件（不自动删除）、标注为"已移除" |
| 批量安装多个 Skill | 逐个检测，汇总输出 |
| 用户拒绝生成/更新指南 | 跳过第三、四步 |
| user-guides 目录不存在 | 自动创建 |
| 新 Skill 为内部工具 | 跳过指南生成，仅在 README 内部工具列表追加 |

## 变更通知格式

每日扫描完成后，仅在**有变更**时推送通知：

```
🔍 Skill 扫描报告（{日期}）

🆕 新增 Skill（{N}个）：
- {skill-name}：{简述}

📝 变更 Skill（{M}个）：
- {skill-name}：指南已更新

🔧 无需变更：
- 未发现功能重叠
- 总计追踪 {total} 个 Skill
```

如果 N + M = 0 → 统一回复：「🔍 技能守护者扫描完成，无变更。」。