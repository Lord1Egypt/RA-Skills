---
name: wechat-public-auto
description: "微信公众号自动发文一站式技能。组合 内容策划 + 人性化润色 + 自动创建草稿，一条龙生成公众号文章保存到草稿箱。Use when user needs to write 公众号文章、微信公众号、create wechat public account article, auto save to draft。"
---

# 微信公众号自动发文一站式技能

整合了 **内容运营专家 + humanizer 人性化润色 + 微信公众号草稿箱** 三个能力，一站式完成从选题到存草稿。

## 工作流程

1. **接收用户需求** - 用户给出文章主题
2. **内容策划** - 按照 `operations-expert` 内容策略确定受众、价值、目标、结构
3. **写作初稿** - 根据策划写出完整文章，markdown 格式，段落之间空行
4. **人性化润色** - 调用 `humanizer` 去除 AI 写作痕迹，让文字更自然
5. **自动创建草稿** - 自动生成/复用封面，创建草稿保存到微信公众号后台
6. **返回结果** - 告诉用户 Media ID 和成功信息，用户登录公众号就能发布

## 格式要求

- markdown 写作，每个大段落之间必须空一行
- 标题用 `#`、`##` 标记
- 写完润色保证：
  - 去除 AI 套话（"pivotal role", "evolving landscape" 这类）
  - 变化句子长度，避免单调
  - 去掉三连排比、虚假平行结构
  - 去掉emoji、过度加粗
  - 段落之间保证空行，HTML 输出每个块加 `<br>` 保证显示有空行

## 依赖

- 需要环境变量 `WECHAT_APPID` `WECHAT_APPSECRET` 已配置
- 需要 IP 白名单已经添加正确
- 需要 `requests` `pillow` Python 依赖已安装

## 购买卡密

| 类型 | 价格 | 链接 |
|------|------|------|
| 日卡 | 9.9元 | https://www.zhufaka.cn/item/tgcsid |
| 月卡 | 399元 | https://www.zhufaka.cn/item/i6wfue |
| 年卡 | 3500元 | https://www.zhufaka.cn/item/x8ancz |
| 定制 | 联系 | 微信 CChenJ_ |

## 卡密（授权）

本技能采用**联网验证**模式，连接授权服务器校验卡密有效性。

1. **客户端激活**（首次运行）：

   ```text
   cd "<本技能文件夹>"
   py .\scripts\run_wechat_channel_ops.py --card-key "你的卡密"
   ```

2. **校验入口**：

   ```text
   py .\scripts\run_wechat_channel_ops.py --card-key "你的卡密"
   py .\scripts\run_wechat_channel_ops.py --show-machine-id
   py .\scripts\run_wechat_channel_ops.py --license-status
   ```

3. **授权服务器**：默认连接 `http://120.27.202.105:8000`，可通过环境变量 `TMO_LICENSE_SERVER` 覆盖。

## 作者

组合技能 by OpenClaw session, 2026-03-17
