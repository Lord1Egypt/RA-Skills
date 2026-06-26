# Quick Team

在 OpenClaw 中快速创建新的 AI 团队成员。配置 openclaw.json，全程引导式。

---

## ⚠️ 权限说明

本 skill 需要以下操作，**所有变更展示 diff 后由用户确认，不会静默写入**：

| 操作 | 风险 | 缓解措施 |
|------|------|----------|
| 修改 `~/.qclaw/openclaw.json` | 修改运行时配置 | 展示 diff，确认后写入 |
| 在主控 workspace 创建文件 | 无风险 | 标准文件操作 |
| 执行 `openclaw gateway restart` | 中断当前所有会话 | 仅用户确认后执行 |

**关于 `allowAgents`**：默认建议最小白名单（仅新成员 ID），不推荐通配符 `["*"]`。

---

## 快速开始

```bash
# 安装
clawhub install quick-team

# 使用——直接对主控说：
# 「创建一个负责校对的成员，叫火眼」
# 「添加一个策略分析师」
```

## 创建流程（6步）

```
1. 确认需求（名称/职责/风格/禁止项）
2. 生成 Agent ID（中文拼音首字母）
3. 创建目录结构
4. 填充模板（SOUL/IDENTITY/TOOLS/HEARTBEAT/MEMORY）
5. 配置 openclaw.json
6. 验证激活
```

详细说明见 [SKILL.md](./SKILL.md)。

## 模板文件

| 文件 | 说明 |
|------|------|
| `SOUL.md` | 角色人格定义（核心，必须完整填写） |
| `IDENTITY.md` | 身份标识：名称/Emoji/氛围 |
| `TOOLS.md` | 常用工具备忘 |
| `HEARTBEAT.md` | 周期性任务（可为空） |
| `MEMORY.md` | 长期记忆 |

`templates/` 目录为空白模板，`examples/assistant/` 目录有完整示例。

---

## 版本

- **v1.1.2**（2026-04-24）— 权限声明强化：默认最小白名单（不推荐通配符），配置变更展示 diff 确认后再写入，metadata 新增 permissions 字段
