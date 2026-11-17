---
name: "企业微信"
version: "2.0.0"
description: "企业微信群机器人工具与服务端 API 指南。Use for: (1) 用附带的零依赖 CLI 向企微群发通知——文本/markdown/图片/文件, (2) CI/监控/日报自动化推送, (3) 企业微信服务端 API（通讯录/应用消息/客户联系）开发指导。WeCom (WeChat Work) group-robot CLI (zero-dependency: text/markdown/image/file) plus server-side API development guide."
tags: ["wework", "wecom", "wechat-work", "bot", "webhook", "cli"]
author: "ClawSkills Team"
category: "enterprise"
---

# 企业微信 Skill

附带零依赖 CLI（`scripts/wecombot.py`，仅 Python 标准库），agent 可
直接向企微群发通知，比钉钉机器人多两个实用能力：**直接发图片**
（图表截图秒达）和**直接发文件**（日志、报表附件）。

## 快速开始

```bash
# 群右键 → 添加群机器人 → 复制 webhook URL 里的 key= 部分
export WECOM_WEBHOOK_KEY=693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa

python3 scripts/wecombot.py text "部署完成 ✅" @all
python3 scripts/wecombot.py markdown report.md
python3 scripts/wecombot.py image chart.png
python3 scripts/wecombot.py file error.log
```

脚本行为声明：仅请求 `qyapi.weixin.qq.com`；image/file/markdown 命令
读取指定的本地文件，不写本地文件。

## 命令手册

| 命令 | 作用 | 限制 |
|------|------|------|
| `text <内容> [@userid,userid\|@all]` | 文本消息 | 2048 字节 |
| `markdown <md文件或内容>` | markdown 消息 | 4096 字节，支持`<font color>`不支持表格 |
| `image <图片文件>` | 发图片（自动 base64+md5） | ≤2MB，jpg/png |
| `file <文件路径>` | 先传临时素材再发送 | ≤20MB |

## Agent 典型用法

1. **图表直达**：数据分析生成 PNG → `image` 直接发群里，
   不用先传图床（钉钉机器人做不到这点）
2. **附件送达**：异常日志、Excel 报表 → `file` 直接给到群
3. **CI/监控/日报**：与钉钉场景相同，`text`/`markdown` 推送
4. **@ 提醒**：text 的 mentioned_list 用企微 userid；只知道手机号时
   可用 `mentioned_mobile_list`（本脚本 @ 参数传 userid）

## 实战要点与错误码（实测）

| errcode | 含义 | 处理 |
|---------|------|------|
| 93000 | webhook key 无效 | key 拼错或机器人被移除（报错信息会带查询链接） |
| 45009 | 接口超限 | 每机器人 **20 条/分钟**，超限丢弃 |
| 40008 | 消息类型不支持 | 检查 msgtype 拼写 |

- 群机器人**免认证免审批**——不需要管理员开发权限，是企微自动化
  阻力最小的入口；服务端 API 则需要管理后台配置
- markdown 与钉钉一样不支持表格；企微独有 `<font color="warning">`
  三色高亮（info 绿/comment 灰/warning 橙），做告警分级很好用
- 机器人只能发群消息，**不能单聊、不能读消息**；要读写单聊用
  服务端 API 的应用消息

## 服务端 API 速查（超出机器人能力时）

- token：`GET /cgi-bin/gettoken?corpid=&corpsecret=`，7200 秒，中心化缓存；
  **不同 secret 权限不同**（应用/通讯录/客户联系各一把）
- 应用消息（可单聊）：`POST /cgi-bin/message/send`，需 agentid，
  用户须在应用可见范围内
- 客户联系（外部联系人/客户群/朋友圈）是企微对微信生态的独有打通，
  也是 SCRM 系统的地基
- 回调验证：URL 验证用 AES 解密 echostr，消息体加解密用
  官方 WXBizMsgCrypt 库，别手写
- 参数以 developer.work.weixin.qq.com 文档为准

## 与钉钉/飞书机器人对比

| 能力 | 企微机器人 | 钉钉机器人（见 `dingding` skill） |
|------|-----------|----------------------------------|
| 文本/markdown | ✅ | ✅（多 link 卡片） |
| 直接发图片 | ✅ base64 | ❌ 只能 markdown 引外链图 |
| 直接发文件 | ✅ ≤20MB | ❌ |
| 安全机制 | key 即凭证 | 关键词/加签/IP 三选一 |
| 频控 | 20 条/分钟 | 20 条/分钟 |

## 本 skill 不做什么

- 不含个人微信自动化；企微侧自动化也应使用官方 API 而非协议逆向
- 群发与 @all 打扰面大，agent 使用前应向用户确认
- 第三方服务商应用（代开发/应用市场）的授权流程未展开，以官方文档为准
