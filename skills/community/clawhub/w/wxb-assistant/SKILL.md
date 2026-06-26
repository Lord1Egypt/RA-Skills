---
name: wxb-assistant
description: 查询旺小宝系统的录音、接访、客户、盘客等数据。当你需要查看客户画像、盘客分析、录音详情时，使用此技能。适用于销售顾问、经理需要快速查询旺小宝数据的场景。当用户提到"录音"、"接访"、"客户画像"、"盘客"、"旺小宝"、"工牌接访"等相关术语时，或需要查询销售分析、客户数据时，应该触发此技能。
---

# 旺小宝数据助手

这是一个让AI能够查询旺小宝系统数据的技能。通过扫码授权后，你可以让AI帮你查询录音、客户、盘客等各类数据。

## 首次使用 - 授权流程

在使用此技能查询数据之前，需要先完成授权：

1. **发起授权**：告诉我你想查询的数据（如"查看客户列表"）
2. **扫码授权**：我会生成一个二维码，你用旺小宝 App 扫描它
3. **自动完成**：App 会自动获取当前登录的 token 并返回
4. **开始使用**：授权完成后，我就可以帮你查询数据了

授权信息会保存在 `~/.wxb-auth-token` 文件中，下次使用时无需重新授权。

## 可以查询的数据

### 录音查询

- **录音详情** - 获取单条录音的基础信息
- **录音文本** - 获取录音的转写文本内容
- **录音摘要** - 获取录音的AI摘要和问答
- **录音扩展** - 获取录音的扩展信息
- **录音评论** - 查看录音的评论列表
- **录音修改** - 修改录音显示名称
- **重新分析** - 重新进行语音识别(ASR)

**使用示例**：

- "查看录音 xxx 的详情"
- "查看录音 xxx 的文本内容"
- "查看录音 xxx 的摘要"
- "查看录音 xxx 的评论"

### 客户相关

- **客户列表** - 查看客户列表，支持多维度筛选
- **客户详情** - 查看指定客户的详细信息
- **客户画像** - 查看客户画像预测结果
- **客户旅程** - 查看客户综合来访跟进轨迹
- **关注点/抗性点** - 查看客户的关注点和抗性点

**使用示例**：

- "显示客户列表"
- "查看客户 xxx 的画像"
- "查看客户 xxx 的关注点"
- "查看客户的来访轨迹"

### 工牌接访

- **接访列表** - 查看工牌接访记录列表，支持分页和时间筛选
- **接访详情** - 查看指定工牌接访的详细信息
- **客户列表** - 查看工牌客户列表
- **搜索功能** - 搜索来访、客户、录音
- **看板数据** - 查看团队数据统计
- **接待管理** - 开始/结束接待、查询WiFi状态等

**使用示例**：
- "显示工牌接访列表"
- "查看工牌接访详情"
- "搜索工牌客户"

### 客户中心

- **客户管理** - 客户列表、详情、搜索
- **客户画像** - 查看画像预测结果、重新预测
- **客户轨迹** - 查看客户综合来访跟进轨迹
- **关注点/抗性点** - 查看客户的关注点和抗性点
- **虚拟接访** - 虚拟接访列表、详情、绑定录音等

**使用示例**：
- "显示客户中心列表"
- "查看虚拟接访记录"

### 盘客分析

- **盘客列表** - 分页查询盘客记录，支持筛选
- **盘客详情** - 查看盘客详情（含画像、买点、风控、关注点）
- **收集表** - 查看/提交/编辑盘客收集表
- **AI辅助回想** - 获取AI辅助回想内容
- **金句内容** - 根据录音ID查询金句内容
- **金句认可** - 金句内容认可操作
- **分析任务** - 创建金句分析任务
- **销售意向** - 获取/更新销售意向级别
- **事件查询** - 通过客户ID获取事件ID
- **评论** - 查看/新增盘客评论

**使用示例**：
- "显示盘客列表"
- "查看盘客详情"
- "查看盘客画像"
- "查看盘客金句"

### 用户与项目

- **当前用户** - 查看当前登录用户的详细信息
- **租户项目列表** - 查看当前用户有权限的所有租户和项目
- **切换项目** - 切换到指定的项目

## 技术实现

此技能使用以下技术实现：

1. **授权管理** (`scripts/auth-manager.js`)
   - 启动本地 HTTP 服务器接收授权回调
   - 生成授权二维码
   - 管理 token 的存储和验证

2. **API 客户端** (`scripts/api-client.js`)
   - 主入口文件，提供统一访问接口
   - 自动处理认证头（`X-Auth-Token`, `X-Platform-Client`）
   - 统一的错误处理

3. **模块化 API** (`scripts/api/`)
   - `visit-api.js` - 工牌接访相关接口
   - `customer-api.js` - 客户中心相关接口
   - `audio-api.js` - 录音查询相关接口
   - `panke-api.js` - 盘客相关接口
   - `other-api.js` - 其他功能（今日代办等）

## API 端点

技能使用以下旺小宝后端 API：

### 录音查询

| 功能         | 方法 | 端点                                              |
| ------------ | ---- | ------------------------------------------------- |
| 录音列表     | POST | `/ai-voice/app/audio/page`                       |
| 录音详情     | GET  | `/ai-voice/audio/detail/{audioId}`               |
| 录音视频     | GET  | `/ai-voice/audio/video/{audioId}`                |
| 录音分析     | GET  | `/ai-voice/app/audio/nlp-result/{audioId}`       |
| 录音文本搜索 | POST | `/ai-voice/app/visit/audio-split-text`           |
| 编辑录音     | POST | `/ai-voice/audio/edit/valid`                     |
| 绑定接访     | POST | `/ai-voice/audio/bind-visit`                     |
| 解绑录音     | POST | `/ai-voice/visit/unbind-audios`                  |
| 基础信息     | GET  | `/audio/app/v2/audio/base/{id}`                  |
| 录音文本     | GET  | `/audio/app/v2/audio/base/text/{id}`             |
| 录音评论     | GET  | `/audio/app/v2/audio/commentary/{id}`            |
| 评论文本     | GET  | `/audio/app/v2/commentary/text/{audioId}`        |
| 摘要问答     | GET  | `/audio/app/v2/audio/agi/summary/dialogue/{id}`  |
| 录音扩展     | GET  | `/audio/app/v2/audio/expand/{id}`                |
| 录音卡片     | GET  | `/audio/app/v2/audio/base/card/{id}`             |
| 音频分享     | POST | `/audio/app/v2/audio/share`                      |

### 客户中心

| 功能     | 方法 | 端点                                          |
| -------- | ---- | --------------------------------------------- |
| 客户列表 | POST | `/customer/customer/list`                    |
| 单个客户 | GET  | `/customer/customer/list/one`                |
| 搜索客户 | GET  | `/customer/customer/search`                  |
| 客户详情 | GET  | `/customer/customer/detail/{wangId}`         |
| 客户轨迹 | GET  | `/customer/customer/trajectory`              |
| 关注点   | GET  | `/customer/customer/focus/wang/list`         |
| 抗性点   | GET  | `/customer/customer/point/wang/list`         |
| 画像预测 | GET  | `/customer/predict/can-view`                 |
| 重新预测 | POST | `/customer/predict/re-predict/{wangId}`      |

### 工牌接访

| 功能           | 方法 | 端点                                   |
| -------------- | ---- | -------------------------------------- |
| 接访列表       | POST | `/ai-voice/app/visit/page`             |
| 客户列表       | POST | `/ai-voice/app/customer/page`          |
| 接访详情       | GET  | `/ai-voice/app/visit/{id}`             |
| 搜索来访       | GET  | `/ai-voice/app/search/visit/page`      |
| 搜索客户       | GET  | `/ai-voice/app/search/customer/page`   |
| 搜索录音       | GET  | `/ai-voice/app/search/audio/page`      |
| 看板来访列表   | POST | `/ai-voice/board/visit:page`           |
| 团队用户统计   | POST | `/ai-voice/board/user:stat`            |
| 团队统计       | POST | `/ai-voice/board/team:stat`            |
| WiFi状态       | GET  | `/ai-voice/app/visit/manager/wifi-status` |
| 开始接待       | POST | `/ai-voice/app/visit/manager/start`    |
| 结束接访       | POST | `/ai-voice/app/visit/manager/end`      |
| 开始录音       | GET  | `/ai-voice/app/visit/manager/start-visit-audio` |
| 结束录音       | GET  | `/ai-voice/app/visit/manager/stop-visit-audio` |

### 盘客

| 功能           | 方法 | 端点                                              |
| -------------- | ---- | ------------------------------------------------- |
| 盘客列表       | POST | `/panke/app/panke/page`                          |
| 盘客进度率     | POST | `/panke/app/panke/page/score`                    |
| 盘客筛选条件   | GET  | `/panke/common/searchCondition`                  |
| 盘客权限       | GET  | `/panke/permission`                              |
| 盘客详情       | GET  | `/panke/app/panke/detail`                        |
| 盘客详情V2     | GET  | `/panke/app/panke/v2/detail`                     |
| 客户中心盘客详情 | GET  | `/panke/app/panke/wang/v2/detail`              |
| 盘客画像       | GET  | `/panke/app/panke/complete-table`                |
| 盘客画像V2     | GET  | `/panke/app/panke/v2/complete-table`             |
| 盘客买点       | GET  | `/panke/app/panke/customer/selling-point-reach`  |
| 盘客风控       | GET  | `/panke/risk/list`                               |
| 盘客关注点     | GET  | `/panke/focus/list`                              |
| 客户来访信息   | POST | `/panke/app/panke/tableCusVisitInfo`             |
| 收集表         | GET  | `/panke/app/panke/table`                         |
| 提交收集表     | POST | `/panke/app/panke/table`                         |
| 编辑收集表字段 | POST | `/panke/app/panke/table/field`                   |
| 收集表校验     | GET  | `/panke/app/panke/check-table`                   |
| 标记特殊来访   | POST | `/panke/app/panke/mark-special-visits`           |
| AI辅助回想     | GET  | `/panke/app/panke/ai-assisted-recall`            |
| 金句内容       | POST | `/panke/panke/new/sop/getGoldenContentByAudioId` |
| 金句认可       | POST | `/panke/panke/new/sop/goldenContentAccept`       |
| 创建分析任务   | POST | `/panke/panke/sop/createGoldenAnalysisTask`      |
| 销售意向级别   | GET  | `/panke/panke/sop/v1/options/salesPitchIntent`   |
| 更新销售意向   | POST | `/panke/panke/sop/v1/options/salesPitchIntent/update` |
| SOP2阶段状态   | GET  | `/panke/panke/new/sop/two/stage/result/status`   |
| SOP2阶段概览   | GET  | `/panke/panke/new/sop/two/stage/sketch`          |
| 评论列表       | GET  | `/panke/comment/list`                            |
| 新增评论       | POST | `/panke/comment/add`                             |
| 获取事件ID     | GET  | `/panke/app/panke/wang/event/detail`             |
| 获取盘客ID     | GET  | `/panke/app/panke/get-pankeId-by-visitId`        |

### 今日代办

| 功能       | 方法 | 端点                                                   |
| ---------- | ---- | ------------------------------------------------------ |
| 待办统计   | GET  | `/ai-voice/app/virtually/visit/virtually-today-todo:count` |
| 待办列表   | GET  | `/ai-voice/app/virtually/visit/virtually-today-todo:all`   |
| 待办详情   | GET  | `/ai-voice/app/virtually/visit/virtually-today-todo/{id}`  |

### 用户与项目

| 功能         | 方法 | 端点                                           |
| ------------ | ---- | ---------------------------------------------- |
| 用户信息     | GET  | `/saas/v2/user/info`                           |
| 租户项目列表 | GET  | `/saas/v2/estate/tenant-and-estate/by-user-id` |
| 切换项目     | POST | `/session/switch-project`                      |
| 切换租户     | POST | `/session/switch-tenant`                       |

## 注意事项

1. **授权有效期**：授权 token 会持久化保存，直到手动清除
2. **数据安全**：token 存储在本地文件中，权限设为仅用户可读写
3. **网络要求**：需要能够访问 `wangkeapp.wangxiaobao.com` 和 `www.wangxiaobao.com`
4. **App 版本**：需要旺小宝 App 支持扫码授权功能
5. **模块化调用**：支持传统调用方式和模块化调用方式两种

## 清除授权

如果需要重新授权或更换账号，可以删除授权文件：

```bash
rm ~/.wxb-auth-token
```

或告诉我"清除授权"，我会帮你处理。

## 常见问题

**Q: 授权失败怎么办？**
A: 确保 App 已登录，网络连接正常，重新扫描二维码即可。

**Q: Token 过期了怎么办？**
A: 删除 `~/.wxb-auth-token` 文件，重新进行授权即可。

**Q: 如何使用模块化 API？**
A: 可以直接调用 `api-client.js` 中对应的模块，如 `visit.getVisitPage()`、`customer.getCustomerPage()` 等。

**Q: 可以同时使用多个账号吗？**
A: 目前不支持，每次授权会覆盖之前的 token。
