---
name: westmoon-qrcode-login
description: >
  西之月账号扫码登录技能。当用户说“登录西之月”、“西之月扫码登录”、“获取西之月登录二维码”、
  “刷新西之月登录态”，或其他技能检测到缺少有效西之月 access_token 时，应立即触发此技能。
  执行完整登录流程：获取二维码 -> 向用户展示二维码 -> 轮询扫码状态 -> 保存 access_token、
  refresh_token 和用户信息到 ~/.westmoon-user-login/tokens.json，供其他西之月技能复用。
license: Complete terms in LICENSE.txt
---

# 西之月扫码登录 Skill

> 重要：先按本 skill 的流程执行，再调用具体业务接口。不要绕过这里的 token 校验和落盘逻辑。

这个 Skill 用于为西之月相关自动化提供稳定的用户登录态。它支持普通终端场景，也支持 OpenClaw 会话中的二维码展示。

## 何时使用

- 需要访问依赖西之月用户身份的接口
- 其他 Skill 提示缺少或检测到失效的 `Authorization: Bearer <token>`
- 需要重新获取二维码让用户扫码确认
- 需要校验本地保存的登录态是否还有效

## 工作流

```text
获取二维码 -> 解码 wxacode -> 展示给用户 -> 轮询 scan_token
    -> confirmed -> 保存 token -> 调用 /umc/user/user/info 验证
    -> invalid/expired -> 提示重新获取二维码
```

1. 调用生成接口获取 `scan_token` 和 `wxacode`
2. 将 `wxacode` 的 data URI 解码为 PNG 文件
3. 在普通终端打印图片路径和 data URI；在 OpenClaw 中额外输出可识别的文件标记
4. 阻塞模式下默认每 5 秒轮询一次 `/umc/miniprogram/qrcode/poll`
5. 状态为 `confirmed` 时保存：
   - `access_token`
   - `refresh_token`
   - `token_type`
   - `expires_in`
   - `expires_at`
   - `user_info`
6. 使用 `Authorization: Bearer <token>` 访问 `/umc/user/user/info`
7. 如果返回 HTTP 401，则认为本地登录态失效，需要重新登录

## 快速使用

### 命令行

```bash
# 获取二维码，默认非阻塞
python scripts/westmoon_login.py

# 显式阻塞等待扫码完成
python scripts/westmoon_login.py --blocking

# 继续上一次未完成的扫码轮询
python scripts/westmoon_login.py --continue

# 用指定 scan_token 继续轮询
python scripts/westmoon_login.py --poll <scan_token>

# 查看本地登录态摘要
python scripts/westmoon_login.py --status

# 校验当前 token 是否有效
python scripts/westmoon_login.py --check

# 读取用户信息
python scripts/westmoon_login.py --userinfo

# 清除本地登录态
python scripts/westmoon_login.py --logout
```

### Python API

```python
from scripts.westmoon_login import WestmoonLoginManager

manager = WestmoonLoginManager()
result = manager.login()

if result.success and result.scan_token:
    print(result.message)
    print(result.scan_token)
```

### 非阻塞默认行为与 OpenClaw 场景

- 默认行为是展示二维码后立即结束，并把待处理的 `scan_token` 存到 `~/.westmoon-user-login/pending_login.json`
- 用户扫码确认后，再让 agent 执行 `--continue` 或 `--poll <scan_token>` 完成登录
- 如果希望当前进程一直等到登录成功，使用 `--blocking`，此时会每 5 秒轮询一次
- OpenClaw 场景下，如果 `OPENCLAW_SESSION=1`，脚本会打印：
  - `[OPENCLAW_SEND_FILE]...[/OPENCLAW_SEND_FILE]`
  - `data:image/png;base64,...`

## 登录态存储

默认保存到：

```text
~/.westmoon-user-login/tokens.json
```

其他技能优先读取这个文件，或直接使用 `scripts/token_manager.py`。

## 关键脚本

- `scripts/westmoon_login.py`
  统一入口，负责编排二维码、轮询、持久化、用户信息验证
- `scripts/qr_code_client.py`
  负责调用生成接口、解析 `wxacode`、保存二维码文件
- `scripts/status_poller.py`
  负责轮询扫码状态
- `scripts/token_manager.py`
  负责登录态落盘、读取、过期判断
- `references/api_reference.md`
  西之月扫码登录接口速查
- `references/integration_guide.md`
  其他 Skill 如何复用登录态

## 集成建议

- 当业务 Skill 收到 401，先调用本 Skill 的 `--check`
- 若无效，再触发本 Skill 重新登录
- 只有在确认 token 有效后，才继续调用业务接口

详细接口和复用方式请按需读取：

- [references/api_reference.md](references/api_reference.md)
- [references/integration_guide.md](references/integration_guide.md)
