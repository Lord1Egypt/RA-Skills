# wechat-control

## 简介

这个 Skill 用 **Python** 实现，利用 `itchat` 库登录本地微信客户端（Windows 桌面版），可以发送文本消息、获取最近的聊天列表以及读取未读消息数量。适用于单用户本地使用场景。

## 功能

- `login`：扫码登录（仅首次，需要手动在微信扫码）
- `send(to, text)`：向指定好友（昵称或微信号）发送文本消息
- `list_chats()`：返回最近 10 条聊天的 `nick`、`last_msg`、`unread_cnt`
- `unread_total()`：返回所有未读消息的总数

## 使用示例（Python REPL）

```python
>>> from wechat_control import WeChat
>>> wc = WeChat()
>>> wc.login()               # 首次扫码登录
>>> wc.send('小明', '你好，今天的天气不错哦')
>>> wc.list_chats()
[{'nick': '小明', 'last_msg': '好的', 'unread_cnt': 0}, ...]
>>> wc.unread_total()
3
```

## 注意事项

- 首次运行需要手动扫码登录一次，之后会保存登录状态（`itchat` 自动缓存 `loginInfo.pkl`），后续启动时会直接登录。
- 本 Skill 依赖 `itchat`（只能在 Windows 桌面版微信上运行）和 `pywin32`（用于获取窗口句柄、焦点等可选功能）。
- 请确保本机已安装 **Python 3.9+**，并在虚拟环境或全局环境中执行 `pip install -r requirements.txt` 安装依赖。
- 仅在本地机器上运行，**不要**将凭证或缓存文件同步到云端或与他人共享。

## 常见问题

- **登录失败**：检查是否已在同一台机器上打开微信，并确保网络通畅；删除 `itchat` 缓存文件 `loginInfo.pkl` 后重新扫码。
- **发送不到好友**：确认好友昵称或微信号拼写准确，或使用 `list_chats()` 获取实际 `nick`。
- **报错 `itchat` 找不到**：请先运行 `pip install itchat` 安装库。

---

## 依赖文件

```text
requirements.txt
```

```
itchat==1.3.10
pywin32==306
```

---

## 入口脚本

`main.py` 负责解析命令行参数并调用 `WeChat` 类的相应方法。使用方式如下：

```powershell
python main.py login
python main.py send "小明" "Hello!"
python main.py list
python main.py unread
```
