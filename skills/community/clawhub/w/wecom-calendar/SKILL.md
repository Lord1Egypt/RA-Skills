# 📅 WeCom Calendar - 企业微信日历管理

企业微信日程管理完整工具，支持创建、查询、更新、删除日程，以及日历管理。

## ✅ 已验证功能

### 1. 日程管理

| 功能 | 状态 | API | 说明 |
|------|------|-----|------|
| 创建日程 | ✅ 已验证 | `/oa/schedule/add` | 支持一次性/重复/全天事件 |
| 获取日程详情 | ✅ 已验证 | `/oa/schedule/get` | 批量获取日程详细信息 |
| 获取日程列表 | ✅ 已验证 | `/oa/schedule/get_by_cal_id` | 按日历 ID 获取日程列表 |
| 更新日程 | ✅ 已验证 | `/oa/schedule/update` | 修改日程信息、添加参与者 |
| 取消日程 | ⚠️ 待测试 | `/oa/schedule/cancel` | 取消已创建的日程 |

### 2. 日历管理

| 功能 | 状态 | API | 说明 |
|------|------|-----|------|
| 创建日历 | ⚠️ 待测试 | `/oa/cal/add` | 创建共享日历 |
| 获取日历列表 | ⚠️ 待测试 | `/oa/cal/get` | 获取企业日历列表 |
| 更新日历 | ⚠️ 待测试 | `/oa/cal/update` | 修改日历信息 |
| 删除日历 | ⚠️ 待测试 | `/oa/cal/delete` | 删除日历 |

### 3. 高级功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 重复日程 | ✅ 已验证 | 支持每日/每周/每月/每年/工作日重复 |
| 提醒设置 | ✅ 已验证 | 支持多个提醒时间（提前 5 分钟/15 分钟/1 小时/1 天等） |
| 参与者管理 | ✅ 已验证 | 最多支持 1000 名参与者，可跟踪参与状态 |
| 管理员设置 | ⚠️ 待测试 | 最多 3 名管理员 |
| 时区支持 | ✅ 已验证 | 支持 UTC 偏移量设置 (-12 ~ +12) |
| 全天事件 | ⚠️ 待测试 | 支持全天日程标记 |

## 🔧 配置要求

### 1. 企业微信后台配置

**必须配置：**
- ✅ 应用凭证（corpId, agentId, agentSecret）
- ✅ 企业可信 IP（添加服务器 IP 到白名单）
- ✅ 日程管理 API 权限（协作 → 日程 → 可调用接口的应用）

**可选配置：**
- 📋 通讯录管理权限（读取成员列表）
- 📋 日历管理权限（管理共享日历）

### 2. 环境变量

```bash
WECOM_CORP_ID=ww6dddd750e5f1d37a          # 企业 ID
WECOM_AGENT_ID=1000004                     # 应用 ID
WECOM_AGENT_SECRET=xxx                     # 应用 Secret
```

## 📖 使用示例

### 创建一次性日程

```bash
node calendar.mjs add \
  --summary "项目启动会" \
  --description "讨论项目计划和分工" \
  --start 1741420800 \
  --end 1741424400 \
  --location "10 楼会议室"
```

### 创建重复日程（每周六）

```bash
node calendar.mjs add \
  --summary "王烙饼的英语课" \
  --start 1773462000 \
  --end 1773471600 \
  --repeat 1 \
  --repeat-type 1 \
  --repeat-day-of-week 6 \
  --repeat-until 1782835140 \
  --remind 1 \
  --remind-before 3600
```

### 获取日程列表

```bash
node calendar.mjs list \
  --cal_id "wcH5NrPwAAreot8LFnpjZyFZGJM1O5rA" \
  --offset 0 \
  --limit 100
```

### 更新日程（添加参与者）

```bash
node calendar.mjs update \
  --schedule_id "7424876b4743b9ef6dac5263e43378e2yvsdpisw" \
  --attendees "WangDong,WengWeng" \
  --summary "新标题"
```

### 取消日程

```bash
node calendar.mjs cancel \
  --schedule_id "7424876b4743b9ef6dac5263e43378e2yvsdpisw"
```

## 📊 参数说明

### 基本参数

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--summary` | 否 | 日程标题 | "会议" |
| `--description` | 否 | 日程描述 | "项目讨论" |
| `--start` | 是 | 开始时间戳 | 1773462000 |
| `--end` | 是 | 结束时间戳 | 1773471600 |
| `--location` | 否 | 地点 | "10 楼会议室" |
| `--attendees` | 否 | 参与者 (逗号分隔) | "user1,user2" |
| `--cal_id` | 否 | 日历 ID | "wcH5NrPwAA..." |

### 重复参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--repeat` | 0 | 是否重复 (0/1) |
| `--repeat-type` | 0 | 类型：0=每日，1=每周，2=每月，5=每年，7=工作日 |
| `--repeat-interval` | 1 | 重复间隔 |
| `--repeat-until` | 0 | 结束时间戳 (0=一直重复) |
| `--repeat-day-of-week` | - | 每周周几 (1-7，逗号分隔) |
| `--repeat-day-of-month` | - | 每月哪天 (1-31，逗号分隔) |
| `--timezone` | 8 | 时区 (-12 ~ +12) |

### 提醒参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--remind` | 0 | 是否提醒 (0/1) |
| `--remind-before` | 300 | 提前多少秒提醒 |
| `--remind-times` | - | 多个提醒时间 (逗号分隔) |

**支持的提醒时间：**
- `0` - 事件开始时
- `300` - 提前 5 分钟
- `900` - 提前 15 分钟
- `3600` - 提前 1 小时
- `86400` - 提前 1 天

## ⚠️ 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 40003 | 无效的企业 ID | 检查 corpId 配置 |
| 40014 | 无效的 access_token | 检查 agentSecret |
| 40058 | 参数错误 | 检查请求参数格式 |
| 48002 | API 无权限 | 在企业微信后台添加 API 权限 |
| 60111 | 成员不存在 | 检查 userid 是否正确 |
| 60205 | 日程不存在 | 检查 schedule_id |
| 60206 | 无权限操作 | 检查是否为日程管理员 |

## 🎯 实际案例

### 案例 1：创建团队周例会

```bash
node calendar.mjs add \
  --summary "团队周例会" \
  --description "每周团队工作同步" \
  --start 1773462000 \
  --end 1773471600 \
  --repeat 1 \
  --repeat-type 1 \
  --repeat-day-of-week 1 \
  --remind 1 \
  --remind-before 900 \
  --location "线上会议"
```

### 案例 2：创建月度汇报

```bash
node calendar.mjs add \
  --summary "月度工作汇报" \
  --start 1775376000 \
  --end 1775383200 \
  --repeat 1 \
  --repeat-type 2 \
  --repeat-day-of-month 1 \
  --repeat-until 1803916800 \
  --attendees "manager1,manager2"
```

### 案例 3：创建公司全员活动

```bash
# 1. 获取所有成员
curl -s "https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token=XXX&department_id=1&fetch_child=1"

# 2. 创建日程并添加所有成员
node calendar.mjs add \
  --summary "公司年会" \
  --start 1798704000 \
  --end 1798732800 \
  --attendees "user1,user2,user3,..." \
  --location "酒店宴会厅"
```

## 📝 注意事项

1. **时间戳** - 使用 Unix 时间戳（秒），北京时间需 +8 小时偏移
2. **参与者限制** - 最多 1000 人
3. **管理员限制** - 最多 3 人
4. **重复日程** - 时间跨度不能超过 1 年
5. **可信 IP** - 必须在企业微信后台配置服务器 IP
6. **权限配置** - 日程 API 需要单独授权（协作 → 日程 → 可调用接口的应用）

## 🔗 相关文档

- [企业微信日程 API 文档](https://developer.work.weixin.qq.com/document/path/93703)
- [企业微信日历 API 文档](https://developer.work.weixin.qq.com/document/path/93707)
- [GitHub 仓库](https://github.com/davinwang/wecom-calendar)

---

**版本**: 1.0.0  
**作者**: OpenClaw Workspace  
**许可**: MIT  
**最后更新**: 2026-03-07
