
# wechat-public-auto

微信公众号自动发文一站式技能

## 功能

整合 **内容运营专家 + humanizer 人性化润色 + 微信公众号草稿箱** 三个能力，一站式完成从选题到存草稿。

- 用户给主题 → 自动策划 → 写作 → 润色 → 排版 → 创建草稿 → 完成
- 自动去除 AI 写作痕迹，文章更自然
- 自动处理段落空格，微信显示美观
- 自动封面上传，开箱即用

## 工作流程

1. 用户给出文章主题
2. 按照内容运营策略确定受众、价值、结构
3. 写作初稿
4. humanizer 润色去除 AI 痕迹
5. 正确排版（段落空行）
6. 自动创建草稿保存到微信公众号后台
7. 用户登录公众号直接发布

## 要求

- 已经配置环境变量 `WECHAT_APPID` `WECHAT_APPSECRET`
- 微信公众号后台已经添加 IP 白名单
- Python 依赖 `requests` `pillow` 已安装

## 卡密

- 使用 `scripts/license_gate.py` + `scripts/run_wechat_channel_ops.py`，与淘宝商家技能相同的 `TMO1` 卡密与 `TMO_MASTER_SECRET`。
- 发卡请使用你已有的 `cardkey_issuer.py`（勿随客户包分发）。
- 详见 `SKILL.md` 中「卡密（授权）」一节。

## 作者

Created by: [你的名字] - 2026-03-17

## 许可证

MIT
