# 旺小美数据助手 (wxm-assistant)

> 让AI直接查询旺小美系统数据：录音、客户、接访/接诊记录，无需手动打开 App。

## 触发条件

当对话中出现以下关键词时，应自动触发此技能：

- **录音**：录音列表、录音详情、录音分析、录音搜索
- **客户**：客户列表、客户详情、客户搜索、意向客户
- **接访/接诊**：接访记录、来访详情、虚拟接访
- **旺小美**：旺小美、旺小美数据、旺小美系统
- **用户/租户/项目**：当前用户、租户列表、切换项目

## 快速开始

### 1. 首次授权

首次使用需要扫码授权，授权后 token 持久化保存在 `~/.wangke-auth-token`：

1. 告诉 AI 你想查询的数据（如"查看录音列表"）
2. AI 会打开授权页面，用旺小美 App 扫描二维码
3. App 自动获取 token 并返回
4. 授权完成，开始查询数据

### 2. 手动授权（备用方案）

如果扫码授权不可用，可以手动设置 token：

```bash
node ~/.claude/skills/wxm-assistant/scripts/manual-auth.js
```

### 3. 清除授权

```bash
rm ~/.wangke-auth-token
# 或
node ~/.claude/skills/wxm-assistant/scripts/auth-manager.js clear
```

## 功能清单

### 用户与租户

| 功能 | 说明 | 示例 |
|------|------|------|
| 当前用户 | 查看登录用户信息 | "查看当前登录的用户" |
| 租户列表 | 查看所有有权限的租户和项目 | "我有哪些租户" |
| 切换租户 | 切换到指定租户 | "切到利美康" |
| 切换项目 | 切换到指定项目 | "切到小美研发演示项目" |

### 录音查询

| 功能 | 说明 | 示例 |
|------|------|------|
| 录音列表 | 查看录音文件列表 | "显示最近10条录音" |
| 按日期查询 | 按日期范围筛选录音 | "查看今天的录音" |
| 录音详情 | 查看指定录音详情 | "查看录音ID为xxx的详情" |
| 录音NLP | 查看AI分析结果 | "查看录音的AI分析" |

**录音列表筛选参数**：
- `fromDate` / `toDate`：日期范围（格式 `YYYY-MM-DD HH:mm:ss`）
- `status`：录音状态
- `userList`：用户列表
- `hasValid`：有效性
- `hasAudio`：是否有录音

### 接访/接诊

| 功能 | 说明 | 示例 |
|------|------|------|
| 接访列表 | 查看接访/接诊记录 | "显示接访记录" |
| 按时间查询 | 按时间范围筛选 | "查看4月的接访记录" |
| 来访详情 | 查看指定来访详情 | "查看来访ID为xxx的详情" |

**接访列表筛选参数**：
- `startTime` / `endTime`：时间范围
- `page` / `size`：分页

### 客户管理

| 功能 | 说明 | 示例 |
|------|------|------|
| 客户列表 | 查看客户列表 | "显示客户列表" |
| 客户详情 | 查看指定客户详情 | "查看客户ID为xxx的信息" |
| 客户搜索 | 按关键词搜索 | "搜索姓张的客户" |

**客户列表筛选参数**：
- `teamId`：团队ID
- `startTime` / `endTime`：时间范围
- `guestTypes`：客户类型（新客/老客）
- `dealStatuses`：成交状态
- `guestPurposes`：来访目的
- `guestSources`：客户来源
- `guestLevels`：客户级别
- `customerIntentionLevels`：意向程度
- `customerValueLevels`：价值等级
- `evaluationGrades`：评估等级
- `hasAudio`：是否有录音
- `majorUserIds`：主用户ID列表
- `ownerConsultantIds`：所属顾问ID列表

## 技术架构

### 目录结构

```
wxm-assistant/
├── SKILL.md                    # 技能描述和触发说明
├── README.md                   # 本文档
├── evals/
│   └── evals.json              # 测试用例
├── references/
│   └── auth.html               # 授权页面
└── scripts/
    ├── api-client.js           # API 客户端（核心）
    ├── auth-manager.js         # 授权管理
    └── manual-auth.js          # 手动授权
```

### 核心模块

#### API 客户端 (`scripts/api-client.js`)

封装所有旺小美后端 API 调用，使用 Node.js 原生 `https` 模块，无外部依赖（除 `open` 包用于打开浏览器）。

```javascript
const ApiClient = require('./api-client')
const client = new ApiClient()

// 获取用户信息
const userInfo = await client.getUserInfo()

// 获取录音列表（支持日期筛选）
const audioList = await client.getAudioList({
  fromDate: '2026-04-21 00:00:00',
  toDate: '2026-04-27 23:59:59'
})

// 获取接访列表
const visitList = await client.getVisitList({
  page: 1, size: 20
})

// 切换租户
await client.switchTenant(tenantId)

// 切换项目
await client.switchProject(projectId)
```

#### 授权管理 (`scripts/auth-manager.js`)

通过远程授权服务器进行扫码授权，管理 token 的存储和验证。

#### 手动授权 (`scripts/manual-auth.js`)

备用方案，手动粘贴 token。

### API 端点

| 功能 | 方法 | 端点 |
|------|------|------|
| 用户信息 | GET | `/saas/v2/user/info` |
| 租户项目列表 | GET | `/saas/v2/estate/tenant-and-estate/by-user-id` |
| 切换租户 | POST | `/session/switch-tenant` |
| 切换项目 | POST | `/session/switch-project` |
| 录音列表 | POST | `/beautx-ai-voice/app/audio/page` |
| 录音详情 | GET | `/beautx-ai-voice/audio/detail/{audioId}` |
| 录音NLP | GET | `/beautx-ai-voice/app/audio/nlp-result/{audioId}` |
| 接访/接诊列表 | GET | `/beautx-ai-voice/visit` |
| 来访详情 | GET | `/app/visit/{visitId}` |
| 客户列表V2 | POST | `/beautx-ai-voice/app/customer/pageV2` |
| 客户详情V2 | GET | `/beautx-ai-voice/app/customer/detailV2` |
| 客户搜索 | POST | `/beautx-ai-voice/app/customer/page` |

所有请求使用以下认证头：
- `X-Auth-Token`: 用户 token
- `X-Platform-Client`: `iwangke`

基础域名：`wangkeapp.wangxiaobao.com`

## CLI 使用方式

API 客户端支持命令行直接调用：

```bash
# 用户信息
node scripts/api-client.js user-info

# 租户列表
node scripts/api-client.js tenant-list

# 切换租户
node scripts/api-client.js switch-tenant <tenantId>

# 切换项目
node scripts/api-client.js switch-project <projectId>

# 录音列表（分页）
node scripts/api-client.js audio 1 20

# 录音列表（按日期）
node scripts/api-client.js audio --fromDate "2026-04-27 00:00:00" --toDate "2026-04-27 23:59:59"

# 录音详情
node scripts/api-client.js audio-detail <audioId>

# 接访列表
node scripts/api-client.js visit

# 客户列表
node scripts/api-client.js customer

# 客户详情
node scripts/api-client.js customer-detail <customerId>
```

## 注意事项

1. **授权有效期**：token 持久化保存，直到手动清除
2. **数据安全**：token 存储在 `~/.wangke-auth-token`，权限 `0o600`（仅用户可读写）
3. **网络要求**：需要能访问 `wangkeapp.wangxiaobao.com` 和 `www.wangxiaobao.com`
4. **多租户**：每次切换租户/项目后，后续查询自动使用新上下文
5. **单账号**：不支持多账号同时使用，新授权会覆盖旧 token

## 常见问题

**Q: 授权失败怎么办？**
A: 确保 App 已登录，网络连接正常，重新扫描二维码。

**Q: Token 过期了怎么办？**
A: 删除 `~/.wangke-auth-token` 文件，重新授权。

**Q: 切换租户后查询不到数据？**
A: 部分数据按项目（estate）关联，切换租户后可能需要再切换到具体项目。

**Q: 如何知道当前在哪个租户/项目？**
A: 调用 `user-info` 或查看 API 返回数据中的 `tenantId`/`estateId` 字段。

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-04-27 | 初始版本：录音、客户、接访查询 |
| 1.1 | 2026-04-27 | 新增用户信息、租户列表、切换项目 |
| 1.2 | 2026-04-27 | 接访改名接访/接诊，添加时间范围筛选 |
| 1.3 | 2026-04-27 | 新增切换租户，更新客户列表完整参数 |
| 1.4 | 2026-04-27 | 录音列表参数对齐实际接口，更新 evals |
| 1.5 | 2026-04-27 | 修复无头环境 open() 崩溃问题，授权链接支持手动打开 |
