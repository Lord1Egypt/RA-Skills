---
name: wechat-automation
description: 微信RPA自动化技能。基于pywechat3（pip install pywechat127）实现Windows PC微信自动化操作，包括发消息、批量群发、读取聊天记录、获取通讯录、自动回复、朋友圈管理等。当用户需要操作微信（发消息、查记录、自动回复等）时激活。
---

# WeChat Automation Skill

## 环境要求

- **操作系统**：Windows 10/11
- **微信版本**：PC微信 3.9.12.x / 4.0+
- **Python**：3.x
- **依赖**：`pip install pywechat127 emoji pyautogui pywinauto pyperclip psutil pywin32`

## 一键安装

在 OpenClaw 终端执行一次：

```bash
pip install pywechat127 emoji pyautogui pywinauto pyperclip psutil pywin32
```

**注意**：OpenClaw 运行在沙箱时需要微信安装在标准路径，且与 OpenClaw 同桌面会话。首次使用前先运行环境检查：

```bash
python "C:\Users\HUAWEI\.openclaw\workspace\skills\wechat-automation\scripts\check_env.py"
```

---

## 核心功能（直接调用，无需生成脚本）

### 发送消息

```python
import sys
sys.path.insert(0, r'D:\code\pywechat3')
from pywechat.WechatAuto import Messages

# 单人单条
Messages.send_message_to_friend(
    friend="好友备注",
    message="消息内容",
    close_wechat=True
)

# 单人多条
Messages.send_messages_to_friend(
    friend="好友备注",
    messages=["消息1", "消息2"],
    delay=0.4
)
```

### 批量发送（给不同好友发不同消息）

```python
from pywechat.WechatAuto import Messages

Messages.send_messages_to_friends(
    friends=["好友1", "好友2"],
    messages=[["消息A"], ["消息B"]],
    delay=0.4
)
```

### 发送文件

```python
from pywechat.WechatAuto import Files

Files.send_file_to_friend(
    friend="好友备注",
    file_path=r"C:\path\to\file.pdf"
)
```

### 读取聊天记录

```python
from pywechat.WechatTools import Tools

contents, senders, types = Tools.pull_messages(
    friend="好友备注",
    number=200
)
```

### 获取通讯录

```python
from pywechat.WechatAuto import Contacts

# 好友列表
friends = Contacts.get_friends_info()

# 群聊列表
groups = Contacts.get_groups_info()
```

### 监听新消息

```python
from pywechat.WechatAuto import Messages

new_messages = Messages.check_new_message(
    duration="5min",
    save_file=True
)
```

### 自动回复（装饰器）

```python
from pywechat.utils import auto_reply_to_friend_decorator

@auto_reply_to_friend_decorator(duration="30min", friend="好友备注")
def reply_func(newMessage):
    if "在吗" in newMessage:
        return "你好，我暂时不在"
    return "收到"

reply_func()
```

---

## 技术原理

- **UI 自动化**：`pywinauto`（Windows 原生 UI Automation API）
- **输入模拟**：`pyautogui`（剪贴板复制 → Ctrl+V 粘贴 → Alt+S 发送）
- **发消息**：复制内容到剪贴板 → 粘贴到微信输入框 → 发送快捷键
- **无 Hook / 无内存读取**：纯物理 UI 模拟，微信无法检测

## 错误处理

| 错误 | 原因 | 解决 |
|------|------|------|
| `WeChatNotStartError` | 微信未启动 | 先手动打开微信 |
| `ElementNotFoundError` | 微信版本不兼容 | 更新 pywechat 或检查 UI 元素 |
| `NotInstalledError` | 未找到微信注册表 | 确认微信 3.9+ 已安装 |
| `NoSuchFriendError` | 好友备注不匹配 | 检查精确备注名 |

## 参考

- PyPI：https://pypi.org/project/pywechat127/
- 源码：https://github.com/Hello-Mr-Crab/pywechat
- 本地源码：`D:\code\pywechat3`
