# WeChat-OpenClaw-Gateway
> WeChat AI 接入网关
> 由 **wechatapi.net** 提供技术支持
> 支持 OpenClaw / Agent / AI 接入 WChat 私聊与群聊

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-WebHook-green)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Agent-orange)
![Status](https://img.shields.io/badge/Status-Running-success)

---

# 项目介绍

**WeChat OpenClaw Gateway** 是一个将 **OpenClaw AI 能力接入 WeChat 的网关程序**。

通过这个项目你可以快速实现：

* WeChat 私聊 AI
* WeChat 群机器人
* 图片识别
* 命令执行
* OpenClaw Agent 接入
* 私域 AI 助手

整个项目 **单文件运行，仅一个 main.py**。

---
<img width="628" height="576" alt="image" src="https://github.com/user-attachments/assets/4f61da82-0801-4106-953c-4c0b5b79e755" />

# 技术支持

本项目由 **wechatapi.net** 提供技术支持。

说明：

* wechatapi.net 为 **付费服务**
* 用于长期稳定接入 WChat
* 适合产品化部署

但同时提供：

**免费测试 Token**

用于：

* 功能验证
* 开发测试
* 项目体验

如果需要测试 Token，可以在官网申请。

---

# 功能特性

### 单文件运行

只需要：

`main.py`

即可运行整个系统。

---

### 自动初始化

首次运行自动进入初始化：

* `WX_API_TOKEN`
* `PUBLIC_URL`
* 群触发词
* 地区ID

并自动生成：

`config.ini`

---

### 支持消息类型

当前支持：

* 文本消息
* 图片消息

自动识别：

* 私聊
* 群聊
* 自己发送的消息

---

### 群触发机器人

群里使用：

`狗子 你在干什么`

即可触发 AI。

---

### 私聊白名单

默认私聊需要白名单。

用户发送：

`我是你的主人`

即可自动加入白名单。

---

### OpenClaw 接入

通过 CLI 调用：

`openclaw agent --session-id xxx --message "..."`

支持：

* 会话隔离
* 群共享上下文
* 群成员独立上下文

---

### 图片识别

收到图片后：

1. 保存图片
2. 生成 URL
3. 交给 OpenClaw 分析

---

### 命令转图片

命令例如：

`/models`
`/status`

执行结果自动转为图片发送。

---

### 多 worker 并发

架构特点：

* 同会话串行
* 多会话并行

提高吞吐能力。

---

# 项目结构

```text
.
├── main.py
├── config.ini
├── logs
└── images
```

---

# 安装依赖

```bash
pip install fastapi uvicorn requests pillow qrcode
```

---

# 运行程序

```bash
python3 main.py
```

---

# 初始化界面

运行后会出现：

```text
========================================================
              WChat OpenClaw Gateway
                    首次初始化
========================================================
  技术支持：wechatapi.net
  官网注册后可享受免费测试
```

---

# 回调地址

假设公网地址：

`http://your-domain:5000`

回调填写：

`http://your-domain:5000/wechat/callback`

---

# 使用示例

私聊：

`你在干什么`

群聊：

`狗子 你会什么`

图片：

发送图片即可识别。

命令：

`/models`

---

# 商业说明

wechatapi.net 为 **付费 API 服务**。

适用于：

* 商业项目
* 私域机器人
* AI 产品
* 客户部署

但支持：

**免费测试 Token**

用于开发者体验。

---

# 常见问题

### 私聊没有回复？

发送：

`我是你的主人`

加入白名单。

---

### 为什么回复慢？

当前版本使用：

`OpenClaw CLI`

每次调用会启动一次进程。

---

### 图片为什么有时识别不了？

部分回调只包含：

`缩略图`

而不是原图。

---

# 未来计划

计划扩展：

* 语音识别
* 文件识别
* 视频识别
* 原图下载
* Docker部署
* 一键安装

---

# License

本项目仅用于：

* 学习
* 测试
* 功能演示

请遵守相关平台规范。

---

# 联系

技术支持：

**wechatapi.net**

如果你需要：

* WChat API
* WChat AI 机器人
* OpenClaw 接入
* 私域 AI

欢迎注册体验。


---

## ClawHub 发布

本项目已整理为可发布的 OpenClaw Skill 目录，核心文件为 `SKILL.md`。
