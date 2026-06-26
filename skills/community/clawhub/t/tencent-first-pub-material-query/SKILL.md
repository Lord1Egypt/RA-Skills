---
name: first-pub-material-query
description: "首发素材消耗批量查询。根据提供的账户ID列表，查询指定日期内的首发素材（图片+视频）消耗数据。首次使用时自动检查依赖环境（tencentads技能+API Key）。"
version: "1.2.0"
license: MIT
metadata:
  author: custom
  category: tencent-ads
---

# 首发素材消耗查询

根据账户ID列表，批量查询首发素材消耗数据。

## ⚠️ 首次使用自检流程

**Agent 在执行本技能前，必须先完成以下自检步骤：**

### Step 1：检查 tencentads-management 技能是否存在

```powershell
# 本 skill 的目录
$skillDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# 或者由 Agent 根据技能安装位置推断：$env:USERPROFILE\.openclaw\workspace\skills
Test-Path "$env:USERPROFILE\.openclaw\workspace\skills\tencentads-management\SKILL.md"
```

- ✅ 存在 → 继续 Step 2
- ❌ 不存在 → 提示用户安装：

> 缺少腾讯广告基础技能，请按以下步骤安装：
> 
> 在聊天窗口发送：`根据 http://skills.ad.qq.com/install/tencentads.md 安装腾讯营销投放技能`
> 
> 或手动访问 https://skills.ad.qq.com/ 查看安装指南

### Step 2：检查 tencentads-cli 是否已安装

```powershell
npm list tencentads-cli -g 2>$null
```

- ✅ 已安装 → 继续 Step 3
- ❌ 未安装 → 执行：

```powershell
npm install tencentads-cli@latest -g
```

### Step 3：检查 API Key 是否已配置

```powershell
Test-Path "$env:USERPROFILE\.tencent-ads\credentials.json"
```

- ✅ 存在 → 环境就绪，开始查询
- ❌ 不存在 → 提示用户：

> 请先配置腾讯广告 API Key。
> 
> 🔑 **获取 API Key**：https://skills.ad.qq.com/
> 
> 获取后请将 API Key 发给我，我会自动保存。

收到 API Key 后调用保存脚本：

```powershell
$authDir = "$env:USERPROFILE\.openclaw\workspace\skills\tencentads-auth"
Set-Location $authDir
node scripts/auth-save-apikey.mjs --api-key <用户提供的KEY>
```

### 自检完成后

三项检查全部通过后，开始执行查询流程。

---

## 查询流程

```
用户输入账户ID列表 + 日期范围
        │
        ▼
分批查询 IMAGE + VIDEO 维度数据（每批20个账户）
        │
        ▼
过滤首发素材（first_publication_status = FIRST_PUBLICATION_STATUS_FIRST_PUBLICATION）
        │
        ▼
按账户汇总输出：首发素材数、消耗、曝光、点击、转化
```

## 调用方式

### PowerShell

```powershell
$skillDir = "$env:USERPROFILE\.openclaw\workspace\skills\first-pub-material-query"
$json = @'
{"account_ids":["31079027","12345678"],"start_date":"2026-04-01","end_date":"2026-04-30"}
'@
$base64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($json))
node "$skillDir\scripts\query-first-pub.mjs" --base64 $base64
```

### Bash

```bash
node scripts/query-first-pub.mjs '{"account_ids":["31079027"],"start_date":"2026-04-01","end_date":"2026-04-30"}'
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `account_ids` | string[] | **是** | 账户ID数组 |
| `start_date` | string | **是** | 开始日期 YYYY-MM-DD |
| `end_date` | string | **是** | 结束日期 YYYY-MM-DD |

## 输出结构

```json
{
  "query": { "account_ids": [...], "start_date": "...", "end_date": "..." },
  "queried_accounts": 10,
  "active_accounts": 3,
  "results": [
    {
      "account_id": 31079027,
      "first_pub": {
        "total": { "material_count": 85, "cost": "35810.39", "views": 1296623, "clicks": 20996, "conversions": 27, "ctr": "1.62%", "conv_cost": "1326.31" },
        "image": { "first_pub_count": 53, "cost": "32591.88", ..., "details": [...] },
        "video": { "first_pub_count": 32, "cost": "3218.51", ..., "details": [...] }
      }
    }
  ]
}
```

## 依赖

- `tencentads-management` skill（报表查询）
- `tencentads-auth` skill（鉴权管理）
- `tencentads-cli` npm 包
- 腾讯广告 API Key

## 已知限制

- 每批查询20个账户，大量账户时耗时较长（每批约2-5分钟）
- 建议单次查询不超过100个账户

## Agent 使用指南

1. **首次使用必须执行自检流程**（见上方"首次使用自检流程"）
2. 自检通过后，用户提供账户ID + 日期范围即可查询
3. 脚本输出 JSON 后，Agent 整理为可读表格
4. 多账户时按消耗降序排列
5. 可选：导出为 Excel
