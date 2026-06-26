# 西之月扫码登录集成指南

## 登录态存储位置

```text
~/.westmoon-user-login/tokens.json
```

保存结构示例：

```json
{
  "access_token": "xxx",
  "refresh_token": "xxx",
  "token_type": "Bearer",
  "expires_in": 604800,
  "expires_at": 1776244244.0,
  "created_at": 1775639444.0,
  "user_info": {
    "id": "85844",
    "name": "xxx"
  }
}
```

## 其他 Skill 如何复用

### 方式 1：直接读取本地文件

```python
import json
from pathlib import Path

token_file = Path.home() / ".westmoon-user-login" / "tokens.json"
data = json.loads(token_file.read_text(encoding="utf-8"))
authorization = f"{data['token_type']} {data['access_token']}"
```

### 方式 2：使用 TokenManager

```python
from scripts.token_manager import TokenManager

manager = TokenManager()
token = manager.get_token()
if token:
    authorization = token.authorization_header
```

## 推荐接入策略

1. 业务 Skill 发请求前先读取本地 token
2. 如果本地没有 token，直接触发本 Skill
3. 如果业务接口返回 401，调用：

```bash
python scripts/westmoon_login.py --check
```

4. 如果仍无效，再重新发起扫码登录

## OpenClaw 集成

OpenClaw 会话中建议设置：

```bash
OPENCLAW_SESSION=1
```

脚本会输出：

- `[OPENCLAW_SEND_FILE]二维码文件路径[/OPENCLAW_SEND_FILE]`
- 原始 `data:image/png;base64,...`

这样 OpenClaw 可以直接展示二维码，同时外部系统也能继续复用原始 data URI。
