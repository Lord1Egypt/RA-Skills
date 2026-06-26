---
name: riskshield
description: RiskShield 案件审批自动化。使用 Playwright 浏览器自动化完成审批，支持 Pass/Refuse 两种操作。
---

# RiskShield 案件审批自动化 Skill

## 功能

- ✅ **浏览器模式**：使用 Playwright 控制无头浏览器完成审批
- ✅ 审批通过（PASS）- 填写 Credit Amount
- ✅ 审批拒绝（REFUSE）- 选择 Refuse Code
- ✅ 自动验证审批结果
- ✅ 后台运行，不影响工作

## 系统信息

| 项目 | 值 |
|------|-----|
| 系统 URL | `https://riskshield.dcsuat.com` |
| 账号 | `taskAccount` |
| 密码 | `ZIdongshenpi1.` |

## 使用方法

### 前提条件

```bash
# 确保 Playwright 已安装
cd ~/.openclaw/workspace/skills/riskshield/scripts
npm install playwright
npx playwright install chromium
```

### 运行审批

```bash
node ~/.openclaw/workspace/skills/riskshield/scripts/risk_approve.js <案件号> <操作> [拒绝码] [审批金额]
```

### 参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| 案件号 | ✅ | 要审批的案件编号 | - |
| 操作 | ✅ | `pass` 或 `refuse` | - |
| 拒绝码 | ❌ | 拒绝原因代码（仅 refuse 时使用） | `CA_TRUE_HIT` |
| 审批金额 | ❌ | 审批金额（仅 pass 时使用） | `100` |

### 示例

```bash
# 审批通过（默认金额 100）
node ~/.openclaw/workspace/skills/riskshield/scripts/risk_approve.js 2604151000000598528 pass

# 审批通过（指定金额 50000）
node ~/.openclaw/workspace/skills/riskshield/scripts/risk_approve.js 2604151000000598528 pass 100 50000

# 审批拒绝（使用默认拒绝码 CA_TRUE_HIT）
node ~/.openclaw/workspace/skills/riskshield/scripts/risk_approve.js 2604151000000598528 refuse

# 审批拒绝（指定拒绝码）
node ~/.openclaw/workspace/skills/riskshield/scripts/risk_approve.js 2604151000000598528 refuse REJ_POA_FAKE
```

## 审批流程

```
1. 登录系统
   ↓
2. 选择搜索类型: 案件编号 (No.)
   ↓
3. 输入案件号并搜索
   ↓
4. 验证案件状态（必须是 Pending/审理中）
   ↓
5. 获取审批页面 URL（从 Approval 链接）
   ↓
6. 打开审批详情页（新标签页）
   ↓
7. 点击 "Decision Information" 选项卡
   ↓
8. 填写审批表单:
   - PASS: ManualApprovalResult → Pass, Credit Amount → 金额
   - REFUSE: ManualApprovalResult → Refuse, Refuse Code → 拒绝码
   ↓
9. 点击 Submit 提交
   ↓
10. 验证案件状态变为 Closed/已结案
```

## 常用拒绝码

| 拒绝码 | 说明 |
|--------|------|
| `CA_TRUE_HIT` | CA真命中 |
| `REJ_POA_FAKE` | POA伪造 |
| `POA/POI` | POA/POI问题 |
| `GRAPHIC_EDITOR` | 图片编辑器检测 |
| `EXPIRATION_DATE` | 过期日期 |
| `WRONG_USER_REGION` | 用户区域错误 |
| `jumioH5Address_Check_<_100` | 地址检查失败 |

## 文件路径

| 文件 | 路径 |
|------|------|
| 主脚本 | `~/.openclaw/workspace/skills/riskshield/scripts/risk_approve.js` |
| 旧版脚本 | `~/.openclaw/workspace/skills/riskshield/scripts/browser_approve_v*.js` |
| Token 存储 | `~/.openclaw/workspace/skills/riskshield/token.json` |

## 注意事项

1. **已结案案件无法重复审批** - 脚本会检查案件状态
2. **后台运行** - 使用 headless 模式，不显示浏览器窗口
3. **自动验证** - 提交后会自动搜索案件确认状态变化
4. **审批链接时效性** - 每次打开详情页的 URL 不同，脚本会自动获取最新链接
