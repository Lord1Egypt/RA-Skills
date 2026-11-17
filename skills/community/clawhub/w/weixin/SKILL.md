---
name: "微信公众平台开发"
version: "2.0.0"
description: "微信公众号/小程序 API 工具与实战避坑手册。Use for: (1) 用附带的零依赖 CLI 直接调公众号 API——取 token、传素材、建草稿、发布文章，(2) 排查 40164/45009 等真实高频错误，(3) 公众号接入/OAuth/JSSDK/支付 V3 开发指导。WeChat Official Account API CLI (zero-dependency) plus a battle-tested pitfall guide for token, media, draft and publishing workflows."
tags: ["wechat", "weixin", "official-account", "miniprogram", "api", "cli"]
author: "ClawSkills Team"
category: "social"
---

# 微信公众平台开发 Skill

不止讲"微信开发是什么"——本 skill 附带一个**零依赖命令行工具**
（`scripts/wxoa.py`，仅 Python 标准库），让 agent 直接替用户完成
公众号内容发布全链路：取 token → 传封面 → 建草稿 → 发布 → 查发表记录。
另附一份**真实生产环境踩坑清单**（每一条都来自实际运营公众号的事故复盘）。

## 快速开始

```bash
export WX_APPID=wx开头的AppID
export WX_SECRET=公众号AppSecret

python3 scripts/wxoa.py token                        # 验证凭证
python3 scripts/wxoa.py call /cgi-bin/get_api_domain_ip   # 冒烟测试
```

脚本行为声明：仅请求 `api.weixin.qq.com`；本地只写一个 token 缓存文件
（系统临时目录，7000 秒过期），不读写其他文件。

## 命令手册

| 命令 | 作用 |
|------|------|
| `token` | 取 access_token（本地缓存，避免重复刷新挤掉线上服务的 token） |
| `call <path> [json]` | 通用调用：任何官方接口，无 body 为 GET，有 body 为 POST |
| `upload-image <file>` | 上传正文内图片（uploadimg，返回 url，不占素材库） |
| `upload-thumb <file>` | 上传永久图片素材（返回 media_id，作草稿封面） |
| `draft-add <标题> <html文件> <thumb_media_id> [作者] [摘要]` | 新建图文草稿 |
| `drafts [offset] [count]` | 列草稿箱 |
| `publish <media_id>` | 发布草稿（freepublish/submit） |
| `published [offset] [count]` | 列已发表记录 |

### 发一篇文章的完整流程

```bash
python3 scripts/wxoa.py upload-thumb cover.jpg
# → {"media_id": "MEDIA_ID", "url": "..."}
python3 scripts/wxoa.py draft-add "文章标题" article.html MEDIA_ID "作者名" "摘要"
# → {"media_id": "DRAFT_MEDIA_ID"}
python3 scripts/wxoa.py publish DRAFT_MEDIA_ID
# → {"publish_id": "..."}（异步，稍后用 published 查结果）
```

`call` 兜底示例（脚本未封装的接口都能调）：

```bash
python3 scripts/wxoa.py call /cgi-bin/menu/get
python3 scripts/wxoa.py call /cgi-bin/user/get
python3 scripts/wxoa.py call /cgi-bin/message/template/send '{"touser":"OPENID","template_id":"...","data":{}}'
```

## 实战踩坑清单（生产事故复盘）

1. **40164 = IP 不在白名单**。公众号后台"IP白名单"只认配置过的服务器
   出口 IP。本地开发机直接调 token 必挂——要么把出口 IP 加白名单，
   要么经已加白的服务器中转。
2. **45009 = 接口日配额耗尽**。draft/freepublish 等接口有每日调用上限，
   耗尽后当天无解，次日 0 点重置。批量操作前先估算次数，脚本里
   **不要**对 45009 做无脑重试。
3. **access_token 全局唯一**。任何一端刷新 token 会使旧 token 失效——
   本脚本做了本地缓存，但若线上服务也在刷 token，两边会互相挤掉线。
   生产环境必须中心化缓存（Redis 等），临时脚本操作尽量复用线上缓存。
4. **发表记录里的标题会被截断**。用标题反查已发表文章时必须做
   **子串匹配**，完整标题 == 匹配会漏。freepublish/batchget 也只能
   拉最近的记录，历史全量要自己本地存档。
5. **推草稿前先去重**。同名文章已在草稿箱或已发表时重复 push 会造成
   重复群发风险，push 前先查 drafts + published 双向子串匹配。
6. **author 字段为空时部分第三方工具会跳过署名**，导致历史旧笔名残留。
   建草稿时显式传作者名。
7. **平台会判定"低创作度内容"**。纯 AI 生成、排比堆砌、无真实锚点的
   文章可能被限流。发布前自查：有无真实数据/引用/具体案例。
8. **封面必须独立生成**。公众号封面比例 900×383，从 16:9 头图硬裁
   必丢内容。

## 开发知识速查

### 服务器接入验证

```python
# GET 回调: sha1(sorted([token, timestamp, nonce])) == signature 则原样返回 echostr
tmp = ''.join(sorted([token, timestamp, nonce]))
ok = hashlib.sha1(tmp.encode()).hexdigest() == signature
```

### 网页授权 OAuth2.0（三步）

1. 跳 `open.weixin.qq.com/connect/oauth2/authorize`（scope=snsapi_base
   静默拿 openid / snsapi_userinfo 弹窗拿资料）
2. code 换 token：`/sns/oauth2/access_token`
3. 拉用户信息：`/sns/userinfo`（此 token 与全局 access_token 是两回事）

### 小程序登录

`wx.login()` 取 code → 服务端 `/sns/jscode2session` 换 openid+session_key
→ 生成自定义登录态。**session_key 绝不下发前端。**

### JSSDK 签名

`sha1("jsapi_ticket=T&noncestr=N&timestamp=TS&url=U")`，url 取 `#` 前部分。
jsapi_ticket 用全局 access_token 换取，同样需要中心化缓存。

### 支付 V3 要点

- 域名 `api.mch.weixin.qq.com`，JSON + SHA256withRSA 商户私钥签名
- 回调必须验签 + AES-256-GCM 解密 + **幂等处理**（微信会重复通知）
- 商户私钥/APIv3 密钥绝不进版本库

### API 域名速查

| 用途 | 域名 |
|------|------|
| 公众号/小程序 API | api.weixin.qq.com |
| 微信支付 | api.mch.weixin.qq.com |
| 网页授权入口 | open.weixin.qq.com |
| 企业微信 | qyapi.weixin.qq.com |

## 本 skill 不做什么

- 不提供绕过微信审核、风控或反自动化机制的方法
- 不含个人微信号（非公众平台）自动化——那是封号高危区
- 群发、模板消息等触达用户的写操作，agent 必须先向用户确认再执行
- 企业微信深度集成建议用专门的 `wework` skill
