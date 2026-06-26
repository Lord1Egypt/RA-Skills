# 安装与配置

## 安装 CLI

```bash
npm install -g siluzan-cso-cli
```

环境要求：Node.js 18+

---

## 初始化 Skill 文件

```bash
siluzan-cso init -d /path/to-your/skills       # 写入自定义目录
```

使用 `init -d /path/to/skills`的方式，将skill复制到你的skill目录下

支持的 `--ai` 目标：
| 值 | 写入路径 |
|----|---------|
| `cursor` | `.cursor/skills/siluzan-cso/` |
| `claude` | `.claude/skills/siluzan-cso/` |
| `openclaw-workspace` | `skills/siluzan-cso/` |
| `openclaw-global` | `~/.openclaw/skills/siluzan-cso/` |
| `workbuddy-workspace` | `.workbuddy/skills/siluzan-cso/` |
| `workbuddy-global` | `~/.workbuddy/skills/siluzan-cso/` |
| `all` | 以上全部 |

---

## 首次登录 / 配置凭据

`siluzan-cso` 与 `siluzan-tso` **共用同一份凭据**，存储在 `~/.siluzan/config.json`，配置一次两个 CLI 均可使用。

```bash
siluzan-cso login                                    # 交互式登录，按提示创建 API Key 后粘贴
siluzan-cso login --api-key <YOUR_API_KEY>           # 直接设置 API Key（跳过交互）
siluzan-cso send-login-code --phone 138xxxx          # 两段式登录第 1 步：发送短信验证码
siluzan-cso login --phone 138xxxx --code 123456      # 两段式登录第 2 步：用验证码完成登录
siluzan-cso config set --api-key <Key>               # 或通过 config set 直接写入
siluzan-cso config set --token <Token>               # 备用：设置 JWT Token
```

> **⚠️ 不要使用 `config set --token <token>` 的方式。** 该方式会将 Token 明文写入 shell history（`~/.bash_history`、`~/.zsh_history`、PowerShell 历史），存在凭证泄露风险。推荐使用 `siluzan-cso login` 交互式输入。

API Key 获取入口：`https://www.siluzan.com/v3/foreign_trade/settings/apiKeyManagement`

### 通过手机号 + 验证码登录（对话式 AI 推荐）

**两段式调用**，专为 AI Agent 设计——任何一步都不会进入交互等待，绝不会卡住 stdout。
拆分后单一职责：第 1 步只发码；第 2 步只用 code 换 API Key。这样 Agent 不会因为"看到 stdout 卡住就重试"而触发短信轰炸。

| 步骤 | 命令                                                 | 说明                                                             |
| ---- | ---------------------------------------------------- | ---------------------------------------------------------------- |
| 1    | `siluzan-cso send-login-code --phone <手机号>`       | 仅向手机发送 6 位验证码，立即返回；**绝不创建 API Key**          |
| 2    | `siluzan-cso login --phone <手机号> --code <验证码>` | 用 code 完成登录并自动签发 API Key 写入 `~/.siluzan/config.json` |

```bash
# 第 1 步：让用户报出手机号后，立刻发码（命令立即返回，不会等待输入）
siluzan-cso send-login-code --phone 13800138000

# 第 2 步：让用户读出收到的 6 位验证码，再调登录命令
siluzan-cso login --phone 13800138000 --code 123456

# 自定义 API Key 名称 / 有效期 / 服务范围
siluzan-cso login --phone 13800138000 --code 123456 \
  --name "Cursor - my-mac - 2026" \
  --valid-days 30 \
  --services CSO,CUT
```

| 参数           | 命令           | 说明                                                                                                                               | 默认值                            |
| -------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `--phone`      | 两个命令都需要 | 中国大陆手机号，可带或不带 +86（如 `13800138000` / `+8613800138000`）；底层会自动补 `+86` 前缀；**手机号必须已在丝路赞网页端注册** | 必填                              |
| `--code`       | 仅 `login`     | 6 位短信验证码（来自第 1 步发码后的短信）；**login 命令必填**，未传会直接报错指引重新走两段式                                      | 必填（login 命令）                |
| `--name`       | 仅 `login`     | 自动创建的 API Key 显示名称                                                                                                        | `CLI - <hostname> - <yyyy-MM-dd>` |
| `--valid-days` | 仅 `login`     | API Key 有效期（天），与 `--expires-at` 二选一                                                                                     | `90`                              |
| `--expires-at` | 仅 `login`     | API Key 绝对过期时间（ISO 8601）                                                                                                   | 不传则用 `--valid-days`           |
| `--services`   | 仅 `login`     | 可访问的服务列表，逗号分隔；可选 `CSO`/`TSO`/`CUT`                                                                                 | `CSO,CUT`（内容发布 + 素材中心）  |
| `--verbose`    | 两个命令都支持 | 输出每次 HTTP 请求的 URL，便于排错                                                                                                 | 关闭                              |

> **未注册手机号**：`login` 第 2 步会返回 `❌ 登录失败：手机未注册` 并附带网页注册地址，引导用户先去网页注册再回来重试两段式。
>
> **验证码错误/过期**：返回明确提示，让用户重新跑 `send-login-code` 拿新验证码。
>
> **AI 助手用法**：先调 `send-login-code` 发码、立即返回继续对话；等用户报出收到的验证码后，再调 `login --phone xxx --code xxx` 完成登录。**永远不要在没拿到 `--code` 的情况下调用 `login --phone xxx`，那会直接报错。**

### 通过环境变量传入凭据（CI/CD 推荐）

无需写入 config.json，直接通过环境变量传入：

```bash
export SILUZAN_API_KEY=<YOUR_API_KEY>       # API Key（推荐）
# 或
export SILUZAN_AUTH_TOKEN=<YOUR_TOKEN>      # JWT Token
```

环境变量优先级高于 config.json，适合 CI/CD、Docker 容器、自动化脚本等场景。可通过 `siluzan-cso config show` 确认当前生效的凭据来源。

**凭据读取优先级（由高到低）：**

| 凭据类型  | 优先级                                                                           |
| --------- | -------------------------------------------------------------------------------- |
| API Key   | `SILUZAN_API_KEY` 环境变量 → `config.json` → `apiKey`                            |
| JWT Token | `--token` CLI 参数 → `SILUZAN_AUTH_TOKEN` 环境变量 → `config.json` → `authToken` |

> API Key 鉴权优先级高于 JWT Token，两者同时存在时使用 API Key。

> **若用户已配置过凭据，不要重复询问。** 先尝试直接运行命令；只有命令返回认证失败时，才引导用户重新执行 `siluzan-cso login`。

---

## 查看当前配置

```bash
siluzan-cso config show
```

输出示例：

```
  构建环境     : production
  apiBaseUrl   : https://api.siluzan.com
  csoBaseUrl   : https://cso.siluzan.com
  apiKey       : abcd****1234
```

---

## 更新

需要严格按照步骤执行

- 执行 `npm install -g siluzan-cso-cli@[beta|latest]` 根据当前使用的是beta版本还是正式版本更新对应的版本到最新版
- 执行 `siluzan-cso init -d /path/to/skills` 复制项目中最新的skill文件来更新你的skill

---

## 修改其他配置

```bash
siluzan-cso config set --api-base <url>    # 切换 CSO API 地址
siluzan-cso config clear                   # 清空所有凭据
```

---
