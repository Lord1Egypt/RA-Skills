# WeChat Automation Skill for OpenClaw

基于 [pywechat127](https://pypi.org/project/pywechat127/) 的 OpenClaw 微信自动化技能，支持 Windows PC 微信的完整自动化操作。

## 功能列表

- 发送文本消息（单人/批量）
- 发送文件
- 读取聊天记录
- 获取通讯录（好友/群聊/企业微信）
- 朋友圈发图/爬取
- 自动回复（装饰器写法）
- 好友/群聊管理

## 环境要求

| 要求 | 版本 |
|------|------|
| 操作系统 | Windows 10 / Windows 11 |
| Python | 3.x |
| 微信版本 | 3.9.12.x / 4.0+ |

## 快速安装

```bash
pip install pywechat127 emoji pyautogui pywinauto pyperclip psutil pywin32
```

## 使用方式

安装依赖后，在 OpenClaw 中直接用自然语言描述需求，例如：

- "给文件传输助手发一条消息：测试"
- "读取张三的最近200条聊天记录"
- "查看我的所有群聊"
- "给标签为VIP的客户批量发送早安问候"

## 技术栈

- **UI 自动化**：pywinauto（Windows 原生 UI Automation API）
- **输入模拟**：pyautogui（剪贴板 + 键盘）
- **消息发送**：复制 → 粘贴（Ctrl+V） → 发送（Alt+S）

## 依赖说明

| 包 | 用途 |
|----|------|
| pywechat127 | 核心库 |
| pywinauto | Windows UI 自动化 |
| pyautogui | 键盘鼠标模拟 |
| pyperclip | 剪贴板操作 |
| psutil | 进程管理 |
| pywin32 | Windows API 调用 |
| emoji | 表情处理 |

## 项目结构

```
wechat-automation/
├── SKILL.md           # OpenClaw Skill 定义
├── README.md          # 本文件
└── scripts/
    └── check_env.py  # 环境检查脚本
```

## 参考资料

- pywechat PyPI：https://pypi.org/project/pywechat127/
- pywechat GitHub：https://github.com/Hello-Mr-Crab/pywechat
- 本地源码：`D:\code\pywechat3`
- ClawHub：https://clawhub.com/skill/zyq-wechat-automation

## 合规声明

本工具仅供个人学习和研究使用。请勿用于任何商业推广、垃圾信息发送或其他违反微信服务条款的行为。
