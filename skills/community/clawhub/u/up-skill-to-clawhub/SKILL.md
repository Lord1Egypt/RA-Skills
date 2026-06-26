---
name: up-skill-to-clawhub
description: Package and publish OpenClaw skills to ClawHub registry. Use when user wants to upload, publish, or update a skill to ClawHub. Triggers on phrases like "upload skill", "publish skill", "push to clawhub", "update skill on clawhub".
---

# Up Skill to ClawHub / 上传技能到 ClawHub

**English**: A workflow guide for packaging and publishing OpenClaw skills to ClawHub registry.
**中文**: 打包并发布 OpenClaw 技能到 ClawHub 注册表的工作流程指南。

---

## Prerequisites / 前提条件

### English
1. ClawHub account and API token
2. Skill folder with valid SKILL.md
3. `npx clawhub@latest` CLI tool

### 中文
1. ClawHub 账户和 API Token
2. 包含有效 SKILL.md 的技能文件夹
3. `npx clawhub@latest` CLI 工具

---

## Quick Start / 快速开始

### English
```bash
# Login to ClawHub
npx clawhub@latest login --token YOUR_API_TOKEN --no-browser

# Publish skill
npx clawhub@latest publish /path/to/skill-folder --version 1.0.0
```

### 中文
```bash
# 登录 ClawHub
npx clawhub@latest login --token YOUR_API_TOKEN --no-browser

# 发布技能
npx clawhub@latest publish /path/to/skill-folder --version 1.0.0
```

---

## Workflow Steps / 工作流程

### Step 1: Prepare Skill / 步骤 1：准备技能

**English**: Ensure the skill folder contains required files:
- `SKILL.md` - Main skill documentation (required)
- `_meta.json` - Metadata with version info
- `scripts/` - Python/shell scripts
- `references/` - Config files, sample data

**中文**: 确保技能文件夹包含必要文件：
- `SKILL.md` - 主技能文档（必需）
- `_meta.json` - 包含版本信息的元数据
- `scripts/` - Python/shell 脚本
- `references/` - 配置文件、示例数据

**File Structure / 文件结构**:
```
skill-name/
├── SKILL.md          # Required / 必需
├── _meta.json        # Metadata / 元数据
├── scripts/
│   └── main.py       # Scripts / 脚本
└── references/
    └── config.json   # Configs / 配置
```

### Step 2: Update Version / 步骤 2：更新版本

**English**: Update `_meta.json` with new version:
```json
{
  "ownerId": "YOUR_OWNER_ID",
  "slug": "skill-name",
  "version": "1.0.1",
  "publishedAt": 1700000000000
}
```

**中文**: 更新 `_meta.json` 版本号：
```json
{
  "ownerId": "YOUR_OWNER_ID",
  "slug": "skill-name",
  "version": "1.0.1",
  "publishedAt": 1700000000000
}
```

### Step 3: Sanitize Sensitive Data / 步骤 3：清理敏感数据

**English**: ⚠️ IMPORTANT: Before publishing, remove or replace:
- Real MAC addresses → Use `AA:BB:CC:DD:EE:FF`
- Real IP addresses → Use `192.168.1.100`
- Real API keys → Use `YOUR_API_KEY` or `sk-xxx...`
- Real passwords → Use `YOUR_PASSWORD`
- Personal device names → Use `example-pc`, `my-device`
- Real phone numbers → Use `+1-555-123-4567`
- Real email addresses → Use `user@example.com`

**中文**: ⚠️ 重要：发布前必须移除或替换：
- 真实 MAC 地址 → 使用 `AA:BB:CC:DD:EE:FF`
- 真实 IP 地址 → 使用 `192.168.1.100`
- 真实 API 密钥 → 使用 `YOUR_API_KEY` 或 `sk-xxx...`
- 真实密码 → 使用 `YOUR_PASSWORD`
- 个人设备名称 → 使用 `example-pc`、`my-device`
- 真实电话号码 → 使用 `+1-555-123-4567`
- 真实邮箱地址 → 使用 `user@example.com`

### Step 4: Update Documentation / 步骤 4：更新文档

**English**: Update SKILL.md with:
- Version number in changelog
- New features/changes
- Bilingual (EN/CN) documentation

**中文**: 更新 SKILL.md：
- 更新日志中的版本号
- 新功能/变更说明
- 中英文双语文档

### Step 5: Login to ClawHub / 步骤 5：登录 ClawHub

**English**:
```bash
npx clawhub@latest login --token YOUR_API_TOKEN --no-browser
```

**中文**:
```bash
npx clawhub@latest login --token YOUR_API_TOKEN --no-browser
```

### Step 6: Publish / 步骤 6：发布

**English**:
```bash
npx clawhub@latest publish /path/to/skill-folder \
  --version 1.0.1 \
  --changelog "Added new feature. Fixed bug."
```

**中文**:
```bash
npx clawhub@latest publish /path/to/skill-folder \
  --version 1.0.1 \
  --changelog "添加新功能。修复问题。"
```

### Step 7: Verify & Restore / 步骤 7：验证并恢复

**English**:
1. Verify publication on clawhub.ai
2. Restore real configuration if needed for local use

**中文**:
1. 在 clawhub.ai 验证发布成功
2. 如需本地使用，恢复真实配置

---

## CLI Reference / CLI 命令参考

### Login / 登录
```bash
npx clawhub@latest login --token YOUR_API_TOKEN --no-browser
```

### Publish / 发布
```bash
npx clawhub@latest publish <path> [options]
```

| Option | Description | 说明 |
|--------|-------------|------|
| `--version <ver>` | Version (semver) | 版本号（语义化版本） |
| `--slug <slug>` | Skill slug | 技能标识符 |
| `--changelog <text>` | Changelog text | 更新日志 |
| `--tags <tags>` | Comma-separated tags | 逗号分隔的标签 |

### Check Login / 检查登录状态
```bash
npx clawhub@latest whoami
```

### Search / 搜索
```bash
npx clawhub@latest search <query>
```

### Install / 安装
```bash
npx clawhub@latest install <slug>
```

---

## Example Session / 示例会话

**User / 用户**: "Upload my skill to clawhub, version 1.0.1"

**Agent actions / Agent 操作**:
1. Check skill folder structure / 检查技能文件夹结构
2. Update `_meta.json` version / 更新版本号
3. Scan for sensitive data / 扫描敏感数据
4. Replace with generic values / 替换为通用值
5. Login to ClawHub / 登录 ClawHub
6. Publish with changelog / 发布并附带更新日志
7. Report success / 报告成功
8. Restore original config / 恢复原始配置

---

## Troubleshooting / 故障排除

### "Not logged in" / "未登录"
```bash
npx clawhub@latest login --token YOUR_API_TOKEN --no-browser
```

### "Path must be a folder" / "路径必须是文件夹"
- Ensure path points to a directory / 确保路径指向目录
- Check SKILL.md exists / 检查 SKILL.md 是否存在

### "Version must be valid semver" / "版本号必须是有效的语义化版本"
- Use format: `1.0.0`, `1.0.1`, `2.0.0` / 使用格式：`1.0.0`、`1.0.1`、`2.0.0`

### Publishing fails / 发布失败
1. Check internet connection / 检查网络连接
2. Verify API token is valid / 验证 API Token 有效
3. Ensure version is higher than existing / 确保版本号高于现有版本

---

## Security Checklist / 安全检查清单

Before publishing, verify / 发布前验证：

- [ ] No real MAC addresses / 无真实 MAC 地址
- [ ] No real IP addresses / 无真实 IP 地址
- [ ] No API keys or tokens / 无 API 密钥或令牌
- [ ] No passwords / 无密码
- [ ] No personal names or devices / 无个人姓名或设备名
- [ ] No phone numbers / 无电话号码
- [ ] No email addresses / 无邮箱地址
- [ ] No private URLs / 无私有 URL

---

## Skill Template / 技能模板

```
skill-name/
├── SKILL.md              # Main documentation / 主文档
├── _meta.json            # Metadata / 元数据
├── scripts/
│   └── main.py           # Main script / 主脚本
└── references/
    ├── config.json       # Config template / 配置模板
    └── README.md         # Reference docs / 参考文档
```

### SKILL.md Template / SKILL.md 模板

```markdown
---
name: skill-name
description: Brief description of what this skill does.
---

# Skill Name / 技能名称

**English**: Description in English.
**中文**: 中文描述。

## Quick Start / 快速开始

## Usage / 使用方法

## Configuration / 配置

## Troubleshooting / 故障排除
```

### _meta.json Template / _meta.json 模板

```json
{
  "ownerId": "YOUR_OWNER_ID",
  "slug": "skill-name",
  "version": "1.0.0",
  "publishedAt": 1700000000000
}
```
