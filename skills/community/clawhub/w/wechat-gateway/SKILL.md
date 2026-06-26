---
name: wechat-openclaw-gateway
description: 在 OpenClaw 中提供 WeChat 回调接入、群私聊会话路由、消息发送与图片识别入口能力。
homepage: https://wechatapi.net
metadata:
  clawdbot:
    emoji: "💬"
    primaryTopic: "wechat gateway"
    requires:
      env:
        - WX_API_TOKEN
        - PUBLIC_URL
    primaryEnv: "WX_API_TOKEN"
---

# WeChat OpenClaw Gateway

这个 skill 用于在 OpenClaw 场景里接入一个可运行的 WeChat 网关项目，适用于：

- 希望把微信作为 OpenClaw 的入口
- 需要处理微信私聊 / 群聊消息回调
- 需要构造稳定的 session_id
- 需要把 AI 响应重新发送回微信
- 需要支持图片消息识别与命令结果回传

## 什么时候使用这个 skill

当用户有以下需求时，应优先使用本 skill：

- “把微信接到 OpenClaw”
- “做一个微信 AI 机器人”
- “做群聊 AI 助手”
- “把微信作为 Agent 入口”
- “需要接入 WeChat API 回调”
- “需要多会话并发、同会话顺序处理”

## 这个 skill 提供什么

本 skill 附带一个可运行的单文件网关项目 `main.py`，主要能力包括：

1. 接收微信回调
2. 解析回调结构
3. 判断私聊 / 群聊 / 自己发送
4. 构造 session_id
5. 使用 OpenClaw CLI 调用 agent
6. 把结果回发到微信
7. 支持文本消息和图片消息
8. 支持白名单、群触发词、去重、worker 并发

## 核心规则

### 1. 必须先做初始化
首次运行 `main.py` 时，需要输入：

- `WX_API_TOKEN`
- `PUBLIC_URL`
- 群触发词
- 地区 ID

程序会自动生成 `config.ini`。

### 2. 微信 API 基础地址默认固定
当前默认使用：

`http://api.wechatapi.net/finder/v2/api`

一般不需要手动修改。

### 3. PUBLIC_URL 不能为空
因为图片回传和回调地址都依赖它。

真正回调地址格式为：

`PUBLIC_URL + /wechat/callback`

例如：

`http://your-domain:5000/wechat/callback`

### 4. 当前只稳定处理两类消息
- 文本消息
- 图片消息

### 5. 群消息必须做触发词收口
默认群触发词示例为：

`狗子`

例如群里发送：

`狗子 你在干什么`

### 6. 私聊默认使用白名单
用户发送：

`我是你的主人`

即可自动加入白名单。

## 回调解析要点

微信回调解析时，应重点关注：

- `TypeName`
- `Wxid`
- `Data.MsgType`
- `Data.FromUserName.string`
- `Data.ToUserName.string`
- `Data.Content.string`

### 是否自己发送
使用下面逻辑判断：

```python
is_self = bool(wxid and from_user == wxid)
```

### 是否群消息
使用下面逻辑判断：

```python
is_group = from_user.endswith("@chatroom") or to_user.endswith("@chatroom")
```

### 群内真实发送人
群消息里真实发送人可能在 `Content.string` 前半段：

```python
if is_group and raw_content and ":\n" in raw_content:
    possible_sender, possible_text = raw_content.split(":\n", 1)
    if possible_sender.startswith("wxid_"):
        sender_wxid = possible_sender
        actual_text = possible_text.strip()
```

## Session 设计规则

推荐 session_id 设计如下：

- 私聊：`wechat_dm_xxx`
- 群共享：`wechat_group_xxx`
- 群成员独立：`wechat_group_xxx_user_xxx`

示例逻辑：

```python
def build_session_id(chat_id: str, sender_wxid: str, is_group: bool, config: dict) -> str:
    def norm(s: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_-]", "_", str(s or "").strip())

    if not is_group:
        return f"wechat_dm_{norm(chat_id)}"

    if config["GROUP_SESSION_MODE"] == "per_user":
        return f"wechat_group_{norm(chat_id)}_user_{norm(sender_wxid)}"

    return f"wechat_group_{norm(chat_id)}"
```

## 并发策略

本项目采用：

- 不同 session 并行
- 同一 session 固定到同一 worker，保证顺序

示例：

```python
def shard_index_for_session(session_id: str, worker_count: int) -> int:
    h = int(hashlib.md5(session_id.encode("utf-8")).hexdigest(), 16)
    return h % worker_count
```

## 当前已知限制

### 1. 主要瓶颈在 OpenClaw CLI
当前通过下面方式调用：

```bash
openclaw agent --session-id xxx --message "..."
```

所以每条消息都会重新启动一次 OpenClaw CLI，存在：

- 进程启动开销
- 配置读取开销
- session 恢复开销
- provider 初始化开销

### 2. 当前更像入口网关，而不是完整 SaaS 产品
它适合：

- 技术验证
- 场景接入
- 演示方案
- 二次开发

## 附带文件

- `main.py`：单文件网关主程序
- `README.md`：项目说明
- `PUBLISH.md`：ClawHub 发布说明

## 推荐发布信息

建议使用以下信息发布到 ClawHub：

- slug: `wechat-openclaw-gateway`
- name: `WeChat OpenClaw Gateway`
- version: `1.0.0`
- tags: `latest,wechat,openclaw,gateway`

## 发布命令

```bash
clawhub publish ./wechat-openclaw-gateway --slug wechat-openclaw-gateway --name "WeChat OpenClaw Gateway" --version 1.0.0 --tags latest,wechat,openclaw,gateway
```

## 备注

这个 skill 的核心不是“只讲概念”，而是附带一个可运行的项目。  
如果你要对外发布，建议把 `wechatapi.net`、GitHub 仓库地址、演示截图补全后再上传。
