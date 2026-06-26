# 安装与配置

## 前置条件

| 依赖        | 版本             | 用途                            |
| ----------- | ---------------- | ------------------------------- |
| Node.js     | 18+              | CLI 运行时及 `node -e` 数据过滤 |
| npm 或 pnpm | npm 8+ / pnpm 8+ | 安装全局包                      |

## 安装 CLI

```bash
npm install -g siluzan-tso-cli
```

---

## 初始化 Skill 文件

```bash
siluzan-tso init -d /path/to-your/skills       # 写入自定义目录
```

使用 `init -d /path/to/skills`的方式，将skill复制到你的skill目录下

支持的 `--ai` 目标：
| 值 | 写入路径 |
|----|---------|
| `cursor` | `.cursor/skills/siluzan-tso/` |
| `claude` | `.claude/skills/siluzan-tso/` |
| `openclaw-workspace` | `skills/siluzan-tso/` |
| `openclaw-global` | `~/.openclaw/skills/siluzan-tso/` |
| `workbuddy-workspace` | `.workbuddy/skills/siluzan-tso/` |
| `workbuddy-global` | `~/.workbuddy/skills/siluzan-tso/` |
| `all` | 以上全部 |

---

## 首次登录 / 配置凭据

`siluzan-tso` 与 `siluzan-cso` **共用同一份凭据**，存储在 `~/.siluzan/config.json`，配置一次两个 CLI 均可使用。

> **登录方式优先级**
>
> 1. **首选**：**手机号 + 短信验证码**两段式（`send-login-code` → `login --phone --code`）——无 TTY 不卡死、不依赖浏览器里复制 API Key，**对话式 AI / OpenClaw / CI 日志旁路**均适用。

### 通过手机号 + 验证码登录（**首选**；对话式 AI / 无 TTY 与各 Agent 环境）

**两段式调用**，专为 AI Agent 设计——任何一步都不会进入交互等待，绝不会卡住 stdout。
拆分后单一职责：第 1 步只发码；第 2 步只用 code 换 API Key。这样 Agent 不会因为"看到 stdout 卡住就重试"而触发短信轰炸。

| 步骤 | 命令                                                 | 说明                                                             |
| ---- | ---------------------------------------------------- | ---------------------------------------------------------------- |
| 1    | `siluzan-tso send-login-code --phone <手机号>`       | 仅向手机发送 6 位验证码                                          |
| 2    | `siluzan-tso login --phone <手机号> --code <验证码>` | 用 code 完成登录并自动签发 API Key 写入 `~/.siluzan/config.json` |

## 其它登录方式（TTY 交互 / 已有 API Key / JWT）

```bash
siluzan-tso login                                    # 无参：TTY 下展开菜单 → 1 JWT / 2 API Key / 3 手机号（发码+输码）
siluzan-tso login --manual                           # 跳过菜单，直接粘贴 JWT（会清除已存 API Key 以启用 Bearer）
siluzan-tso login --api-key <YOUR_API_KEY>           # 直接设置 API Key（跳过交互）
siluzan-tso config set --api-key <Key>               # 或 config 直接写入
siluzan-tso config set --token <Token>               # 备用：设置 JWT Token
```

API Key 获取入口：`https://www.siluzan.com/v3/foreign_trade/settings/apiKeyManagement`

```bash
# 第 1 步：让用户报出手机号后，立刻发码（命令立即返回，不会等待输入）
siluzan-tso send-login-code --phone 13800138000

# 第 2 步：让用户读出收到的 6 位验证码，再调登录命令
siluzan-tso login --phone 13800138000 --code 123456

# 自定义 API Key 名称 / 有效期 / 服务范围
siluzan-tso login --phone 13800138000 --code 123456 \
  --name "Cursor - my-mac - 2026" \
  --valid-days 30 \
  --services TSO,CUT
```

| 参数           | 命令           | 说明                                                                                                                               | 默认值                            |
| -------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `--phone`      | 两个命令都需要 | 中国大陆手机号，可带或不带 +86（如 `13800138000` / `+8613800138000`）；底层会自动补 `+86` 前缀；**手机号必须已在丝路赞网页端注册** | 必填                              |
| `--code`       | 仅 `login`     | 6 位短信验证码（来自第 1 步发码后的短信）；**login 命令必填**，未传会直接报错指引重新走两段式                                      | 必填（login 命令）                |
| `--name`       | 仅 `login`     | 自动创建的 API Key 显示名称                                                                                                        | `CLI - <hostname> - <yyyy-MM-dd>` |
| `--valid-days` | 仅 `login`     | API Key 有效期（天），与 `--expires-at` 二选一                                                                                     | `90`                              |
| `--expires-at` | 仅 `login`     | API Key 绝对过期时间（ISO 8601）                                                                                                   | 不传则用 `--valid-days`           |
| `--services`   | 仅 `login`     | 可访问的服务列表，逗号分隔；可选 `CSO`/`TSO`/`CUT`                                                                                 | `TSO,CUT`（广告投放 + 素材中心）  |
| `--verbose`    | 两个命令都支持 | 输出每次 HTTP 请求的 URL，便于排错                                                                                                 | 关闭                              |

> **未注册手机号**：`login` 第 2 步会返回 `❌ 登录失败：手机未注册` 并附带网页注册地址，引导用户先去网页注册再回来重试两段式。
>
> **验证码错误/过期**：返回明确提示，让用户重新跑 `send-login-code` 拿新验证码。
>
> **AI 助手用法**：先调 `send-login-code` 发码、立即返回继续对话；等用户报出收到的验证码后，再调 `login --phone xxx --code xxx` 完成登录。**永远不要在没拿到 `--code` 的情况下调用 `login --phone xxx`，那会直接报错。**（人类在本地终端可直接运行无参 `siluzan-tso login` 选 3，由 CLI 发码并读验证码，无需先记 `send-login-code`。）

### 通过环境变量传入凭据（CI/CD 推荐）

无需写入 config.json，直接通过环境变量传入：

```bash
export SILUZAN_API_KEY=<YOUR_API_KEY>       # API Key（推荐）
# 或
export SILUZAN_AUTH_TOKEN=<YOUR_TOKEN>      # JWT Token
```

环境变量优先级高于 config.json，适合 CI/CD、Docker 容器、自动化脚本等场景。可通过 `siluzan-tso config show` 确认当前生效的凭据来源。

**凭据读取优先级（由高到低）：**

| 凭据类型  | 优先级                                                                           |
| --------- | -------------------------------------------------------------------------------- |
| API Key   | `SILUZAN_API_KEY` 环境变量 → `config.json` → `apiKey`                            |
| JWT Token | `--token` CLI 参数 → `SILUZAN_AUTH_TOKEN` 环境变量 → `config.json` → `authToken` |

> API Key 鉴权优先级高于 JWT Token，两者同时存在时使用 API Key。

---

## 查看当前配置

```bash
siluzan-tso config show
```

输出示例：

```
  构建环境     : production
  apiBaseUrl   : https://tso-api.siluzan.com
  googleApiUrl : https://googleapi.mysiluzan.com
  webUrl       : https://www.siluzan.com
  apiKey       : abcd****1234
```

`webUrl` 是网页基地址，引导用户打开平台页面时用此值拼接路径。

---

## 使用 webUrl 进行网页操作

- 涉及充值、账户激活、首页看板等**必须在网页完成**的操作时，应先通过 `siluzan-tso config show` 获取 `webUrl` 值，再按各业务文档提供的相对路径拼接完整链接，引导用户在浏览器中完成后续步骤。

## 更新

需要严格按照步骤执行

- 执行 npm install -g siluzan-tso-cli@[beta|latest]根据当前使用的是beta版本还是正式版本更新对应的版本到最新版
- 执行 siluzan-tso init -d /path/to/skills 复制项目中最新的skill文件来更新你的skill

---

## 修改其他配置

```bash
siluzan-tso config set --api-base <url>    # 切换 TSO API 地址
# Google API 地址从 TSO API 自动推导，如需覆盖可设置环境变量：
# export SILUZAN_GOOGLE_API=<url>
siluzan-tso config clear                   # 清空所有凭据
```

---
