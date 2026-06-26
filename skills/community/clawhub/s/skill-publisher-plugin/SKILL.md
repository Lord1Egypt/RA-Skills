---
name: clawhub-publisher
description: 上传和发布技能到 ClawHub 市场。当用户说"发布skill"、"上传到clawhub"、"发布到市场"或需要将本地技能发布到 ClawHub 时触发。
---

# ClawHub 技能发布

将本地 Skill 上传到 ClawHub 市场。

## 前置检查

### 1. 检查登录状态

执行命令检查是否已登录：

```bash
cd ~ && npx clawhub whoami
```

- 如果显示用户名 → 已登录，继续下一步
- 如果未登录 → 执行 `npx clawhub login` 引导用户登录

### 2. 检查技能是否存在

查看目标技能是否已发布过：

```bash
cd ~ && npx clawhub inspect <slug>
```

- 如果存在 → 需要发布新版本（版本号 +0.0.1）
- 如果不存在 → 首次发布，使用 v1.0.0

## 发布流程

### 首次发布

```bash
cd ~ && npx clawhub publish <skill-path> --slug <slug> --name "<显示名称>" --version 1.0.0 --tags "<标签1,标签2>"
```

### 更新发布

```bash
cd ~ && npx clawhub publish <skill-path> --slug <slug> --version <新版本> --changelog "<更新说明>"
```

版本号规则：遵循语义化版本 (semver)
- 首次发布：1.0.0
- 小更新（bug修复）：1.0.x
- 新功能：1.x.0
- 重大更新：x.0.0

## CLI 命令参考

| 命令 | 说明 |
|------|------|
| `npx clawhub whoami` | 查看登录状态 |
| `npx clawhub login` | 登录 |
| `npx clawhub inspect <slug>` | 查看已发布技能信息 |
| `npx clawhub publish <path> [options]` | 发布技能 |
| `npx clawhub sync` | 同步本地技能到市场 |

### publish 选项

```
--slug <slug>       技能标识符（必填）
--name <name>       显示名称（必填，首次发布）
--version <version> 版本号（必填）
--changelog <text> 更新说明
--tags <tags>       标签，逗号分隔
```

## 输出格式

发布成功后，输出：
```
✅ <技能名> v<版本> 已发布到 ClawHub
🔗 https://clawhub.ai/<用户名>/<slug>
```

## 触发词

- "发布skill"
- "上传到clawhub"
- "发布到市场"
- "发布技能"
- "更新skill"
- "sync skills"

## 注意事项

1. skill 路径可以是绝对路径或 `~/.workbuddy/skills/<skill-name>`
2. slug 只能包含小写字母、数字和连字符
3. 版本号必须是有效的 semver 格式
4. 发布前确保 SKILL.md 格式正确
