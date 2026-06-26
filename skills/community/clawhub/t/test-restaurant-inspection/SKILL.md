---
name: test-restaurant-inspection
description: 餐厅AI巡检自动化。自动管理智能体（检测/创建）、设备抓图、AI分析，实现食品安全/卫生/合规性自动巡检。
metadata:
  openclaw:
    emoji: "🍽️"
    requires: 
      env: ["EZVIZ_APP_KEY", "EZVIZ_APP_SECRET", "EZVIZ_DEVICE_SERIAL"]
      pip: ["requests"]
    primaryEnv: "EZVIZ_APP_KEY"
    sideEffects:
      - "查询萤石智能体列表"
      - "自动创建餐厅专用智能体（模板ID: f4c255b2929e463d86e9）"
      - "设备抓拍图片"
      - "调用AI分析接口"
---

# Ezviz Restaurant Inspection (萤石餐厅巡检)

通过萤石设备抓图 + 智能体分析接口，实现对餐厅场景的 AI 自动巡检。

## 快速开始

### 安装依赖

```bash
pip install requests
```

### 设置环境变量

```bash
# 必需参数
export EZVIZ_APP_KEY="your_app_key"
export EZVIZ_APP_SECRET="your_app_secret"
export EZVIZ_DEVICE_SERIAL="dev1,dev2,dev3"

# 可选参数
export EZVIZ_CHANNEL_NO="1" # 通道号，默认 1
```

**注意**: 不需要设置 `EZVIZ_ACCESS_TOKEN` 或 `EZVIZ_AGENT_ID`！技能会自动获取 Token 并管理智能体。

### 运行

```bash
python3 {baseDir}/scripts/restaurant_inspection.py
```

命令行参数：
```bash
# 单个设备
python3 {baseDir}/scripts/restaurant_inspection.py appKey appSecret dev1 [channel_no]

# 多个设备（逗号分隔）
python3 {baseDir}/scripts/restaurant_inspection.py appKey appSecret "dev1,dev2,dev3" [channel_no]
```

## 工作流程

```
1. 获取 Token (appKey + appSecret → accessToken)
 ↓
2. 智能体管理 (检测是否存在餐厅智能体 → 不存在则创建)
 ↓
3. 设备抓图 (accessToken + deviceSerial → picUrl)
 ↓
4. AI 分析 (agentId + picUrl → 分析结果)
 ↓
5. 输出结果 (JSON + 控制台)
```

## 智能体自动管理说明

**你不需要手动配置 `EZVIZ_AGENT_ID`！**

技能会自动处理智能体的检测与创建：

```
每次运行:
 查询用户智能体列表 (appType=1)
 ↓
 检查是否存在名称包含"餐厅"或"餐饮"的智能体
 ↓
 如果存在 → 使用第一个匹配的智能体 appId
 如果不存在 → 从模板复制创建新智能体
   - templateId: f4c255b2929e463d86e9 (餐厅行业通用模板)
   - 返回新智能体的 appId
```

**智能体管理特性**:
- ✅ **自动检测**: 自动查找现有餐厅智能体
- ✅ **防重复创建**: 避免为同一用户重复创建相同智能体
- ✅ **模板复制**: 自动从标准模板创建专用智能体
- ✅ **无缝集成**: 用户无需手动管理智能体
- ⚠️ **注意**: 每次运行都会检查智能体状态

## 输出示例

```
======================================================================
Ezviz Restaurant Inspection Skill (萤石餐厅巡检)
======================================================================
[Time] 2026-03-16 22:35:00
[INFO] Target devices: 2
 - dev1 (Channel: 1)
 - dev2 (Channel: 1)

======================================================================
[Step 1] Getting access token...
[SUCCESS] Token obtained, expires: 2026-03-23 22:35:00

======================================================================
[Step 2] Managing intelligent agent...
[INFO] Found existing restaurant agent: appId_12345
[SUCCESS] Using existing agent: appId_12345

======================================================================
[Step 3] Capturing and analyzing images...
======================================================================

[Device] dev1 (Channel: 1)
[SUCCESS] Image captured: https://opencapture.ys7.com/...
[SUCCESS] Analysis completed!

[Analysis Result]
{
 "食品安全": "合格",
 "卫生状况": "良好",
 "人员着装": "规范",
 "违规行为": "未发现"
}

======================================================================
INSPECTION SUMMARY
======================================================================
 Total devices: 2
 Success: 2
 Failed: 0
 Agent ID: appId_12345
======================================================================
```

## 多设备格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 单设备 | `dev1` | 默认通道 1 |
| 多设备 | `dev1,dev2,dev3` | 全部使用默认通道 |
| 指定通道 | `dev1:1,dev2:2` | 每个设备独立通道 |
| 混合 | `dev1,dev2:2,dev3` | 部分指定通道 |

## API 接口

| 接口 | URL | 文档 |
|------|-----|------|
| 获取 Token | `POST /api/lapp/token/get` | https://open.ys7.com/help/81 |
| 设备抓图 | `POST /api/lapp/device/capture` | https://open.ys7.com/help/687 |
| 智能体列表 | `GET /api/service/open/intelligent/agent/app/list` | 内部接口 |
| 智能体复制 | `POST /api/service/open/intelligent/agent/template/copy` | 内部接口 |
| AI 分析 | `POST /api/service/open/intelligent/agent/engine/agent/anaylsis` | https://open.ys7.com/help/5006 |

## 网络端点

| 域名 | 用途 |
|------|------|
| `open.ys7.com` | 萤石开放平台 API（Token、抓图） |
| `aidialoggw.ys7.com` | 萤石 AI 智能体分析接口 |

## 格式代码

**返回字段**:
- `analysis` - AI 分析结果（依赖智能体配置）
- `pic_url` - 抓拍图片 URL（有效期 2 小时）

**错误码**:
- `200` - 操作成功
- `400` - 参数错误
- `500` - 服务异常
- `10002` - accessToken 过期
- `10028` - 频率限制触发

## Tips

- **多设备**: 逗号分隔 `dev1,dev2,dev3`
- **指定通道**: 冒号分隔 `dev1:1,dev2:2`
- **Token 有效期**: 7 天（每次运行自动获取）
- **图片有效期**: 2 小时
- **频率限制**: 设备间自动间隔 4 秒
- **分析超时**: 默认 60 秒
- **智能体模板**: 固定模板ID `f4c255b2929e463d86e9`

## 注意事项

⚠️ **频率限制**: 萤石抓图接口建议间隔 4 秒以上，频繁调用可能触发限流（错误码 10028）

⚠️ **智能体配额**: 每个用户可能有智能体创建数量限制，请确保配额充足

⚠️ **Token 安全**: Token 仅在内存中使用，不写入日志，不发送到非萤石端点

⚠️ **分析超时**: AI 分析可能耗时较长，默认超时 60 秒

## 数据流出说明

**本技能会向第三方服务发送数据**：

| 数据类型 | 发送到 | 用途 | 是否必需 |
|----------|--------|------|----------|
| 摄像头抓拍图片 | `open.ys7.com` (萤石) | AI 智能体分析 | ✅ 必需 |
| appKey/appSecret | `open.ys7.com` (萤石) | 获取访问 Token | ✅ 必需 |
| 设备序列号 | `open.ys7.com` (萤石) | 请求抓图 | ✅ 必需 |
| 智能体 ID | `aidialoggw.ys7.com` (萤石) | AI 分析请求 | ✅ 必需 |
| **EZVIZ_ACCESS_TOKEN** | **自动生成** | **每次运行自动获取** | **✅ 自动** |
| **智能体操作** | **萤石内部接口** | **智能体检测/创建** | **✅ 自动** |

**数据流出说明**:
- ✅ **萤石开放平台** (`open.ys7.com`): Token 请求、设备抓图 - 萤石官方 API
- ✅ **萤石 AI 智能体** (`aidialoggw.ys7.com`): 图片分析 - 萤石官方 API
- ✅ **萤石内部接口**: 智能体管理 - 萤石内部服务
- ❌ **无其他第三方**: 不会发送数据到其他服务

**凭证权限建议**:
- 使用**最小权限**的 appKey/appSecret
- 仅开通必要的 API 权限（设备抓图、AI 分析、智能体管理）
- 定期轮换凭证
- 不要使用主账号凭证

**本地处理**:
- ✅ Token 在内存中使用，不写入磁盘
- ✅ 不记录完整 API 响应
- ✅ 图片 URL 只显示前 50 字符
- ✅ 不跨运行缓存 Token（每次运行重新获取）
- ✅ 智能体操作仅在必要时执行

## 应用场景

| 场景 | 说明 |
|------|------|
| 🍽️ 食品安全巡检 | 自动检测食品存储、加工过程合规性 |
| 🧼 卫生状况监控 | 识别清洁状态、垃圾处理、消毒情况 |
| 👨‍🍳 员工规范检查 | 检查工作服、口罩、手套佩戴情况 |
| 📋 合规性审计 | 自动生成巡检报告，满足监管要求 |
| 🏢 连锁店管理 | 多门店统一标准，远程集中监控