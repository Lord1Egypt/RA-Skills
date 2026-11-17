---
name: wechat-miniprogram-cloudbase-scaffold
description: "从零快速搭建一个微信小程序（后端用微信云开发/CloudBase）的脚手架与方法论：单函数 REST 路由、幂等建号/幂等建集合、实时统计、订阅消息+定时触发器、全生命周期坑。Scaffold & methodology for building a WeChat Mini Program on WeChat CloudBase: single-function REST routing, idempotent user/collection seeding, real-time stats, subscribe messages + scheduled triggers, full-lifecycle pitfalls. Use when: 做一个云开发小程序 / 从零搭小程序 / 小程序 MVP / building a WeChat Mini Program MVP. Deployment details → wechat-miniprogram-cloudbase-deploy skill."
agent_created: true
---

# 微信小程序云开发脚手架（从零快速搭建）

把一个想法快速落成一个**可上线**的微信小程序，后端用微信云开发（CloudBase）：
云函数 + 云数据库，免服务器、免域名、免鉴权，个人主体也能发布。

本 skill 是从一个真实上线项目（「不刷短剧·打卡帮」）沉淀的完整方法论：
架构选型 → 脚手架 → 云函数模式 → 数据库 → 全生命周期坑 → 提审发布。

部署环节（`tcb` 部署、集合建索引、`miniprogram-ci` 上传、IP 白名单）在
**`wechat-miniprogram-cloudbase-deploy`** skill 里，本 skill 只引用、不重复。

## When to use

- 用户要「做一个小程序 / 小程序 MVP / 把某功能做成小程序」，且还没选后端。
- 个人/小团队、无服务器、想快速上线，后端数据量不大（云数据库单集合百万级以内）。
- 需要登录 + 数据读写 + 可选的消息推送（订阅消息）这类典型工具型小程序。

不适合用云开发的情况（改用自托管后端）：需要复杂事务/多表 join、超大并发、
对接自建数据库/第三方系统强耦合、或要严格控制成本（云开发按量计费）。

## 先收集 4 个前置信息（缺一不可）

| 项 | 从哪拿 | 用途 |
|---|---|---|
| 真实 **AppID** | mp.weixin.qq.com → 开发 → 开发管理 → 开发设置 | `touristappid` 不能用云开发 |
| **环境 ID** | 微信开发者工具 → 云开发 → 环境设置（形如 `xxx-4g1a2b3c`） | 云函数/数据库所在环境 |
| **上传私钥** `.key` | 开发设置 → 小程序代码上传密钥 → 下载 | `miniprogram-ci` 上传用，**只传文件路径，绝不贴内容** |
| **订阅消息模板 ID** | 功能 → 订阅消息 → 我的模板（如需推送才要） | 每日提醒推送用 |

主体类型（个人/企业）决定可选类目，个人主体可用类目很少（通常只有生活服务/工具/体育），
先确认主体类型再谈类目（见 references/pitfalls.md 的「提审」节）。

## 标准项目结构（本 skill 的模板即此结构）

```
your-miniprogram/
├── project.config.json          # AppID + miniprogramRoot + cloudfunctionRoot
├── cloudbaserc.json             # 云函数运行时/内存/超时/定时触发器
├── miniprogram/                 # 前端
│   ├── app.js                   # wx.cloud.init + login 时序（模板含）
│   ├── app.json                 # 页面 + tabBar（模板含，需按业务改）
│   ├── app.wxss                 # 全局样式（模板含）
│   ├── sitemap.json
│   ├── utils/
│   │   ├── config.js            # ENV_ID / APP_ID / SUBSCRIBE_TEMPLATE_ID 集中配置
│   │   └── request.js           # 统一 callFunction 封装（REST 风格）
│   └── pages/                   # 业务页面（第③层，模板不含，需按业务写 js/wxml/wxss）
├── cloudfunctions/              # 后端（每个目录一个云函数）
│   ├── api/                     # 核心：单函数 REST 路由
│   │   ├── index.js             # 路由分发
│   │   ├── db.js                # wx-server-sdk 初始化 + DYNAMIC_CURRENT_ENV
│   │   └── services/            # 业务逻辑（纯函数/数据访问分离）
│   ├── login/                   # OPENID 建号（幂等）
│   ├── seed/                    # 幂等建集合 + 种子数据
│   └── dailyPush/               # 定时触发器 + 订阅消息
# （部署脚本 deploy-cloud.sh / upload.js 不在此模板内，
#  统一放在 wechat-miniprogram-cloudbase-deploy 的 scripts/，见该 skill）
```

模板在 `assets/templates/`；部署脚本（deploy-cloud.sh/upload.js）在 deploy skill，不在本模板内。

### 模板三层：哪些通用、哪些要按业务替换

「打卡+群组」只是**占位演示域**，scaffold 真正沉淀的是下面的骨架与模式，
换任何需求（记账/任务清单/投票/预约/打卡…）都通用：

| 层 | 文件 | 换需求时 |
|---|---|---|
| ① 基础设施 | project.config.json / app.js / app.wxss / config.js / request.js / db.js / 各 package.json / login 的 openid 幂等建号 | 只改占位符（AppID/ENV_ID/模板ID），几乎零改 |
| ② 可复用模式 | 单函数 REST 路由、幂等建号、幂等建集合、订阅消息+定时触发器 | 模式不动，具体 handler 按业务写 |
| ③ 示例业务域 | api 的 createCheckin/listGroups 等 handler、streak.js/stats.js、「今天还没打卡」推送、seed 种子、app.json 的 tab、**pages/\*\* 页面（js/wxml/wxss）** | **整层重写** |

关键认知：**「改占位符」只覆盖第 ① 层；真正的工作量在第 ③ 层**——按你的业务写
handler + 数据模型。其余（路由骨架、鉴权、集合初始化、推送触发器、部署）都是
脚手架替你省掉的。

## 快速搭建工作流（按序执行）

0. **选型（默认云开发）**：**默认走云开发，不必每次问**。仅当需求命中
   「不适合用云开发」的红线（复杂事务/多表 join、超大并发、对接自建数据库/第三方系统
   强耦合、严格控制成本）时，才**停下来给用户选择**——说明「云开发可能不合适，理由 X」，
   给出「云开发 / 自托管后端」两个选项让用户拍板后再继续。

1. **复制模板骨架**：`cp -r assets/templates/* <项目目录>/`，替换 5 个占位符
   （`__APPID__`/`__ENV_ID__`/`__TEMPLATE_ID__`/`__APP_TITLE__`/`__PROJECT_NAME__`）：
   `project.config.json` 的 `appid`/`projectname`、`miniprogram/app.json` 的标题、
   `miniprogram/utils/config.js` 的 `ENV_ID`/`APP_ID`/`SUBSCRIBE_TEMPLATE_ID`、
   `cloudbaserc.json` 的 `envId`。
2. **写数据模型与集合清单**：先定集合，再写代码。原则见
   `references/architecture.md`。**集合清单必须与代码实际用到的集合一一核对**
   （这是本次踩过的最隐蔽的坑，见 pitfalls.md）。
3. **写云函数业务**：在 `api/services/` 写逻辑，在 `api/index.js` 加路由。
   `login`/`seed`/`dailyPush` 通常照模板改业务字段即可。
4. **部署云函数 + 上传前端**：见 `wechat-miniprogram-cloudbase-deploy` skill
   （含 `scripts/deploy-cloud.sh`、`scripts/upload.js` 与全部部署坑）。
5. **建集合 + 种子**：控制台建集合（或让 `seed` 幂等建），跑一次 seed。
6. **前端联调**：微信开发者工具打开 → 编译 → 模拟器跑通 → 真机/体验版。
7. **提审发布**：隐私指引 + 类目 + 版本描述（见 pitfalls.md），人工提交审核。

## 4 个关键设计模式（详见 references/architecture.md）

1. **单函数 REST 路由**：一个 `api` 云函数承载所有业务接口，前端
   `request.js` 统一走 `{path, method, body, query}`。好处：只维护一个函数、
   冷启动少、鉴权统一（OPENID 由平台注入，无需 token）。
2. **幂等建号**：`login` 和 `me` 都可能在对方之前被调用，所以 `me()` 查不到
   用户时**幂等补建号**（含自动加入公开数据），消除「用户不存在」时序竞争。
3. **幂等建集合 + 种子**：CLI 不能建集合（见 deploy skill 的 Pitfall 1），用
   `seed` 函数对每个集合 `.add` 占位再删，实现幂等建集合；种子数据只在空时插入。
4. **实时计算代替缓存集合**：统计类数据（连续天数等）直接从事实表实时算，
   **不要维护额外的缓存集合**——少一个集合就少一类「集合不存在」+「缓存不一致」的坑。

## 全生命周期坑（速查，详见 references/pitfalls.md）

- 集合清单漏一个 → `collection not exists`；用 seed 幂等建，别手工漏。
- `me` 页在 login 前请求 → 幂等补建号。
- 定时触发器写在 `cloudbaserc.json` 没用，必须写进函数自己的 `config.json`。
- 订阅消息模板 ID 与 AppID 强绑定，换 AppID 必须重新申请模板。
- 订阅消息 `data` 字段名（`thing1`/`time2`）必须与模板关键词顺序一致，否则静默失败。
- 换 AppID 后云环境要重新「使用已有环境」绑定（腾讯云账号先关联小程序）。
- 提审：类目别选「社交」；隐私指引在**提审时**勾；分享不用申请，但要备案+认证按钮才亮。

## 交付后必须提醒用户的两件事

1. 上传只产生**体验版**，真用户看不到；**审核 + 发布是纯人工步骤**。
2. 订阅消息的字段名要与模板关键词对齐，最好**实测一次推送**确认（否则静默失败）。
