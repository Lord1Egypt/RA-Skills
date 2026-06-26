---
name: skill-vetter-guide
description: "第三方 OpenClaw Skill 安装前安全审查指南。适用场景：安装第三方 skill、审计已安装 skill、执行先审后装 SOP、定期安全巡检、在新 OpenClaw 实例上部署 Skill Vetter。触发词：安装 skill、审查 skill、skill 安全、巡检 skill、设置 skill vetter。"
---

# Skill Vetter 使用指南

第三方 OpenClaw Skill 安装前的安全优先审查协议。

**核心规则：未经审查，禁止安装任何 skill。**

## 安装 Skill Vetter

安装到用户全局 skills 目录，所有 agent 均可使用：

```
~/.agents/skills/skill-vetter/
```

来源：ClawHub 上的 `useai-pro/openclaw-skills-security@skill-vetter`，或对应的 GitHub 仓库。

安装后验证：
1. 确认 `~/.agents/skills/skill-vetter/SKILL.md` 存在且内容完整
2. 检查该 skill 出现在 agent 的可用 skills 列表中

## 审查 SOP

当被要求安装任何第三方 skill 时，按以下流程执行：

```
发现 skill → 获取源码 → 审查全部文件 → 风险分级 → 决定是否安装 → 安装并留档
```

### 1. 检查来源信息

- 来源（ClawHub / GitHub / 个人分享）
- 作者、最近更新时间、star/下载量、社区反馈
- 是否有明确的用途说明

### 2. 完整代码审查（强制）

审查 skill 中的**每一个文件**，不能只看 SKILL.md。检查以下红旗项：

| 红旗项 | 风险原因 |
|--------|---------|
| `curl`/`wget` 指向未知 URL | 数据外泄 |
| 向外部服务器发送数据 | 隐私泄露 |
| 请求 token/API key/凭证 | 凭证窃取 |
| 读取 `~/.ssh`、`~/.aws`、`~/.config` | 敏感目录访问 |
| 读取 `MEMORY.md`、`USER.md`、`SOUL.md`、`IDENTITY.md`、`TOOLS.md`、`openclaw.config.json` | OpenClaw 私有文件访问 |
| `base64` 解码不透明内容 | 代码混淆 |
| `eval()`/`exec()` 配合外部输入 | 代码注入 |
| 修改 workspace 之外的文件 | 系统篡改 |
| 安装未声明的依赖 | 供应链风险 |
| 使用 IP 地址直连（而非域名） | 绕过 DNS 控制 |
| 压缩/混淆的代码块 | 隐藏行为 |
| `sudo`/elevated 权限 | 权限提升 |
| 访问浏览器 cookie/session | 会话劫持 |

### 3. 评估权限范围

确定该 skill 会读取、写入、执行什么，是否需要联网。验证权限是否最小化，且与声明的功能匹配。

### 4. 风险分级

| 等级 | 含义 | 处理建议 |
|------|------|---------|
| 🟢 LOW（低） | 本地文本/格式化/天气类 | 审查后可安装 |
| 🟡 MEDIUM（中） | 文件操作、浏览器、第三方 API | 完整审查后谨慎安装 |
| 🔴 HIGH（高） | 涉及凭证、系统配置、自动外发 | **必须人工批准** |
| ⛔ EXTREME（极高） | root、安全策略修改、大范围敏感读取 | **禁止安装** |

### 5. 输出审查报告

使用标准报告格式。参见 [references/report-template.zh-CN.md](references/report-template.zh-CN.md)。

### 6. 安装后记录

安装后记录：日期、skill 名称、来源、风险等级、审查摘要、安装路径。
写入 `memory/YYYY-MM-DD.md` 或专门的 `security-audits/` 目录。

## 定期巡检

定期审计 `~/.agents/skills/` 下所有已安装的第三方 skill：
- 每 4 小时快速扫描（通过 cron 自动执行）
- 每周或每月完整复审（人工/半自动）

对每个 skill，检查是否有新增可疑文件、代码变更或新引入的红旗项。
输出每个 skill 的状态：✅ 正常 / ⚠️ 需关注 / ❌ 有问题。

结果写入带时间戳的文件：`security-audits/skills-audit-YYYY-MM-DD_HHMM.md`。
审计文件格式参见 [references/audit-template.zh-CN.md](references/audit-template.zh-CN.md)。

## AGENTS.md 强制规则

将以下规则加入 `AGENTS.md`，使审查成为所有 agent 的强制要求：

```markdown
## Skill 安装安全规则

所有第三方 Skills 安装前，必须先用 Skill Vetter 审查，通过后才能安装。无例外。

- 审查全部文件，不只看 SKILL.md
- 检查：外联、敏感文件访问、混淆代码、eval/exec、凭证请求、elevated 权限
- 输出标准化审查报告
- HIGH / EXTREME 风险必须等待人工批准
- 未通过审查的 skill 禁止安装
```

## 提示词模板

常用操作的即用提示词。参见 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。

## 多实例环境

管理多个 OpenClaw 实例时：
- 每台机器独立审查 skill
- 记录每台主机上已安装的版本
- 不要默认"在 A 机器安全，B 机器也一定安全"
- 跨主机同步或升级 skill 时留下审计痕迹
