# 🐉 青龙面板 OpenClaw / Claude Code 技能

通过 OpenClaw 或 Claude Code 控制 [青龙面板](https://github.com/whyour/qinglong) 的定时任务、环境变量、脚本、依赖、日志等。

## 功能一览

| 模块 | 支持操作 |
|------|----------|
| **定时任务** | 列表、创建、编辑、删除、运行、停止、启用/禁用、置顶/取消置顶、查看日志 |
| **环境变量** | 列表、创建、编辑、删除、启用/禁用、排序、置顶 |
| **脚本管理** | 列表、查看、保存、运行、停止、删除 |
| **依赖管理** | 列表、安装、重装、取消、删除（Node/Linux/Python3） |
| **订阅管理** | 列表、运行、停止、启用/禁用、删除、查看日志 |
| **日志查看** | 列表、查看、删除 |
| **系统管理** | 系统信息、配置、检查更新、更新系统、重启、执行命令、重置密码 |
| **配置文件** | 列表、查看、保存 |

## 前置条件

- 系统安装了 `curl` 和 `jq`
- 青龙面板已开启 Open API

## 获取青龙 API 凭证

1. 打开青龙面板 Web 界面
2. 进入 **配置** → **应用**
3. 点击 **创建应用**
4. 勾选需要的权限范围（如：crons、envs、scripts、logs、system）
5. 复制生成的 **Client ID** 和 **Client Secret**

## 环境变量

| 变量名 | 说明 | 是否必填 |
|--------|------|----------|
| `QINGLONG_URL` | 面板地址，如 `http://192.168.1.100:5700` | ✅ |
| `QINGLONG_CLIENT_ID` | 应用 Client ID | ✅ |
| `QINGLONG_CLIENT_SECRET` | 应用 Client Secret | ✅ |

---

## 方式一：在 OpenClaw 中使用

### 安装技能

**方式 A：通过 ClawHub 安装（推荐）**

```bash
clawhub install qinglong-skills
```

**方式 B：通过 npx 安装**

```bash
npx skills add NNNNzs/qinglong-skills
```

**方式 C：使用 `extraDirs`（推荐用于开发）**

在 `~/.openclaw/openclaw.json` 中添加：

```json5
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/qinglong-skills"]
    }
  }
}
```

**方式 D：复制到 workspace skills 目录**

```bash
cp -r qinglong-skills ~/.openclaw/workspace/skills/qinglong
```

### 在 `openclaw.json` 中配置环境变量

打开 `~/.openclaw/openclaw.json`，找到或创建 `skills.entries.qinglong` 对象：

```json5
{
  "skills": {
    "entries": {
      "qinglong": {
        "enabled": true,
        "env": {
          "QINGLONG_URL": "https://ql.yourdomain.com",
          "QINGLONG_CLIENT_ID": "你的Client ID",
          "QINGLONG_CLIENT_SECRET": "你的Client Secret"
        }
      }
    }
  }
}
```

**完整路径：** `skills.entries.qinglong.env.QINGLONG_URL` / `QINGLONG_CLIENT_ID` / `QINGLONG_CLIENT_SECRET`

> ⚠️ 注意：Gateway UI **不会**为 `skills.entries.*.env` 渲染输入表单。你需要直接编辑 `openclaw.json`，或者在 Gateway UI 中使用 Raw JSON 编辑器。

编辑完成后重启网关：

```bash
openclaw gateway restart
```

验证技能已加载：

```bash
openclaw skills list
```

你应该看到 `🐉 qinglong` 状态为 `✓ ready`。

### 通过 OpenClaw 智能体使用

智能体在你询问青龙相关操作时会自动使用该技能。

---

## 方式二：在 Claude Code CLI 中使用

本技能**不依赖 OpenClaw**。Claude Code（或任何能执行 shell 命令的 AI agent）都可以直接使用。

### 设置

1. 克隆仓库：

```bash
git clone git@github.com:NNNNzs/qinglong-skills.git
cd qinglong-skills
```

2. 设置系统环境变量（添加到 `~/.bashrc` 或 `~/.zshrc`）：

```bash
export QINGLONG_URL="https://ql.yourdomain.com"
export QINGLONG_CLIENT_ID="你的Client ID"
export QINGLONG_CLIENT_SECRET="你的Client Secret"
```

然后重新加载：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

3. 测试脚本：

```bash
./scripts/ql.sh cron list
```

### 通过 Claude Code 使用

有几种方式让 Claude Code 使用这个技能：

**方法 1：传递 SKILL.md 作为上下文**

```bash
claude-code --context SKILL.md "帮我查看青龙面板有哪些定时任务"
```

**方法 2：在提示词中说明**

告诉 Claude Code：

> 你是一个青龙面板管理助手。使用 `scripts/ql.sh` 脚本操作青龙面板。
> 参考 SKILL.md 了解可用命令。
> 环境变量已配置好，直接调用脚本即可。

**方法 3：使用 CLAUDE.md 项目文件（推荐）**

在项目根目录创建 `CLAUDE.md`：

```markdown
# 青龙面板管理

使用 `scripts/ql.sh` 管理青龙面板。

常用命令：
- `scripts/ql.sh cron list` — 查看所有定时任务
- `scripts/ql.sh env list` — 查看环境变量
- `scripts/ql.sh system info` — 查看系统信息

完整参考：见本目录下的 SKILL.md。
```

然后运行：

```bash
claude-code "帮我查看青龙面板的定时任务"
```

Claude Code 会读取 `CLAUDE.md` 并知道如何使用脚本。

---

## CLI 命令参考

### 定时任务

```bash
scripts/ql.sh cron list                                    # 查看所有定时任务
scripts/ql.sh cron get <id>                                # 查看指定任务详情
scripts/ql.sh cron create --command "task x.js" --schedule "0 0 * * *" --name "任务名"
scripts/ql.sh cron update <id> --name "新名称"             # 编辑任务
scripts/ql.sh cron delete <id>                             # 删除（支持多个 ID）
scripts/ql.sh cron run <id>                                # 立即运行
scripts/ql.sh cron stop <id>                               # 停止运行
scripts/ql.sh cron enable <id>                             # 启用
scripts/ql.sh cron disable <id>                            # 禁用
scripts/ql.sh cron pin <id> / unpin <id>                   # 置顶 / 取消置顶
scripts/ql.sh cron log <id>                                # 查看日志
```

### 环境变量

```bash
scripts/ql.sh env list                                     # 查看所有
scripts/ql.sh env list "JD"                                # 搜索
scripts/ql.sh env create --name "KEY" --value "VALUE" --remarks "备注"
scripts/ql.sh env update --id <id> --name "KEY" --value "新值"
scripts/ql.sh env delete <id>
scripts/ql.sh env enable <id> / disable <id>
```

### 脚本管理

```bash
scripts/ql.sh script list                                  # 查看所有脚本
scripts/ql.sh script get --file "test.js"                  # 查看内容
scripts/ql.sh script save --file "test.js" --content "console.log('hello')"
scripts/ql.sh script run --file "test.js"                  # 运行
scripts/ql.sh script stop --file "test.js"                 # 停止
scripts/ql.sh script delete --file "test.js"               # 删除
```

### 依赖管理

```bash
scripts/ql.sh dep list                                     # 查看所有
scripts/ql.sh dep install --name "axios" --type 0          # 0=Node, 1=Linux, 2=Python3
scripts/ql.sh dep reinstall <id>
scripts/ql.sh dep delete <id>
```

### 订阅管理

```bash
scripts/ql.sh sub list / run <id> / stop <id> / enable <id> / disable <id> / delete <id>
```

### 系统管理

```bash
scripts/ql.sh system info                                  # 系统信息
scripts/ql.sh system config                                # 系统配置
scripts/ql.sh system check-update                          # 检查更新
scripts/ql.sh system reload                                # 重启系统
scripts/ql.sh system command-run --command "task test.js"  # 执行命令
scripts/ql.sh system auth-reset --username admin --password newpass
```

### Token 管理

```bash
scripts/ql.sh token refresh                                # 强制刷新 Token
scripts/ql.sh token show                                   # 查看缓存的 Token
scripts/ql.sh token clear                                  # 清除 Token 缓存
```

---

## 常见问题

### 401 未授权

检查 `QINGLONG_CLIENT_ID` 和 `QINGLONG_CLIENT_SECRET` 是否正确。

### 连接被拒绝

确认 `QINGLONG_URL` 地址可从当前机器访问。

### 权限不足

确保在青龙面板创建应用时勾选了所需的权限范围（Scopes）。

### Token 过期

脚本会自动刷新 Token，无需手动处理。如遇问题可执行：
```bash
scripts/ql.sh token clear
scripts/ql.sh token refresh
```

## 项目结构

```
qinglong-skills/
├── SKILL.md              # 技能定义文档
├── README.md             # 英文说明文档
├── README_zh-CN.md       # 中文说明文档（本文件）
├── scripts/
│   └── ql.sh             # 核心 CLI 脚本
└── references/
    └── api.md            # 完整 API 参考文档
```

## 相关链接

- [青龙面板 GitHub](https://github.com/whyour/qinglong)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.com)
