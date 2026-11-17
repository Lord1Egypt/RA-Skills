---
name: campus-madmodel
description: 清华大学 MAD **校内 LLM 服务**（madmodel.cs.tsinghua.edu.cn，DeepSeek-V4.1-Flash / qwen3.8-27b / DeepSeek-R1-W8A8），OpenAI 兼容。既是对话服务，也是**任意任务的模型后端**——对话、批量抽取、**跑需要 LLM 后端的评测/基准**（起本地 `/v1` 端点即可）。当用户需要"用清华的 Deepseek、校内大模型/LLM 服务、madmodel、DeepSeek-V4.1-Flash、qwen3.8-27b、DeepSeek-R1-W8A8、拿 MAD token、给评测/基准配模型后端、本地 OpenAI 代理"时使用。
metadata:
  openclaw:
    requires:
      env:
        - CAS_PASSWORD
    os:
      - windows
      - macos
      - linux
---

# 清华 MAD 大模型服务（madmodel）

> 独立子模块：只依赖 campus 底座（base-cas 浏览器/会话、creds 保险箱、shared.common），
> **不依赖任何外部中转服务**。token/ticket 只落本机 `campus/runtime/madmodel/`（`.gitignore` 已忽略）。

## 如果你是 AI，请阅读以下内容

### 铁律
- AI 运行所有脚本；**stdout 只输出 JSON**，进度写 `campus/runtime/logs/campus.log`
- **禁止**阻塞（无 `input()`；登录触发 2FA/验证码时如实返回 `needs_human`，由用户处理）
- 凭据读 campus 保险箱 `cas_username` / `cas_password`（禁止明文、禁止写进仓库）
- token/ticket 是**凭据**：只存 `campus/runtime/`，不进 git、不打印全文

### 机制（实测）
MAD 是校内服务，**校外必须经清华 WebVPN**。注意：**WebVPN 会直接放行 MAD 的 SPA 页面**（返回 200，不触发登录），
所以登录必须**先访问 webvpn 根**触发 CAS，再进 MAD 触发 app CAS，再用 ticket 换 JWT：

```
校园统一认证(账号+密码) → CAS 回跳 ?ticket= → GET /model-api/auth-login/check?ticket= → JWT(~6h)
调用：POST https://webvpn.tsinghua.edu.cn/https/<编码>/v1/chat/completions
      header Authorization: Bearer <JWT>   cookie wengine_vpn_ticket=<ticket>
```
- 用 base-cas 的**共享 CDP profile**（已受信指纹）→ 通常免短信 2FA。
- webvpn ticket 寿命短（~1h）；JWT ~6h。`token --force` 或 `token`（过期时）会重登。

### 使用（`scripts/madmodel.py`）
```bash
python scripts/madmodel.py models
python scripts/madmodel.py token            # 复用缓存；无/过期则登录
python scripts/madmodel.py token --force    # 强制重登
python scripts/madmodel.py status
python scripts/madmodel.py chat --prompt "用一句话介绍清华" --model DeepSeek-V4.1-Flash --effort high
python scripts/madmodel.py chat --prompt "数到3" --stream
python scripts/madmodel.py serve --port 18720   # 起本地 OpenAI 兼容代理（独立可用）
```

### 作为「通用 LLM 后端」（供其它任务 / 评测 / 基准）
本模块不只是聊天：它是**校内 OpenAI 兼容 LLM 服务**。任何需要模型后端的场景都可直接用：
```bash
python scripts/madmodel.py serve --port 18720     # 起本地端点
# 其它程序把 base_url 设为 http://127.0.0.1:18720/v1，api_key 随意（无需）
```
- 例：**跑需要 LLM 的评测（SWE-bench 之类的 agent/基准）** → 让评测的模型后端指向上面这个本地端点即可；
  评测真正缺的是**评测环境**（代码库/harness/Docker/数据），**模型后端由本模块提供**，两者不矛盾。
- 也可一次性调用：`madmodel.py chat --prompt ...`（脚本化）。

### 可用模型
| model | 思考开关 | 强度 reasoning_effort | 思考字段 | 视觉 | 上下文 |
|---|---|---|---|---|---|
| `DeepSeek-V4.1-Flash` | `chat_template_kwargs.thinking` | low/high/max | `reasoning_content` | ✗ | 1M |
| `qwen3.8-27b` | `chat_template_kwargs.enable_thinking` | low/medium/xhigh | `reasoning` | ✓ | 256k |
| `DeepSeek-R1-W8A8` | 无（默认思考） | low/medium/high | `content` | ✗ | — |

### 工作流（AI 执行）
1. 用户要"用清华 Deepseek 对话" → 先 `token`（必要时登录）→ 再 `chat`。
2. 需要给别的程序用 → `serve --port`，其 endpoint `http://127.0.0.1:<port>/v1` 即 OpenAI 兼容（无需 key）。
3. `token` 返回 `needs_human`（2FA/验证码）→ 提示用户完成，不要反复重试。

### 边界
- MAD 服务并发上限约 **3**；超额会被拒。端到端较慢（经 webvpn，首字节 ~1.5–2s）。
- 非流式响应里思考模型的 `content` 可能为 `null`，思考在 `reasoning_content`。
- 服务为校内共享实验服务，按合理频率自用；`serve` 仅绑 127.0.0.1。

## 如果你是用户，请阅读以下内容

你只要说一句话即可，例如：

- "用清华的 Deepseek 帮我写一段话"
- "MAD 有哪些模型？"
- "在本机起一个 MAD 的 OpenAI 代理（端口 18720）"

AI 会自动登录（用你已配置的校园账号，通常免短信）、取 token 并调用；token 只存本机、不会进仓库。
