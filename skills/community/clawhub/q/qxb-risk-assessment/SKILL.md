---
name: qxb-risk-assessment
description: 全面排查企业的经营风险情况，适用于供应商准入尽调、贷前风险筛查、合作伙伴背景调查等场景，全方位预警潜在经营风险，辅助决策者规避合作隐患。
license: MIT
metadata: { "openclaw": { "requires": { "env": ["QXBENT_API_TOKEN"], "bins": ["node", "npm"] }, "install": [ { "id": "npm-deps", "kind": "node", "package": "axios", "label": "Install Node.js dependencies" } ] } }
---

# 企业风险排查（综合）

## 概述

查询企业的空壳特征、合同违约、日常经营及存续情况等多维风险。空壳特征：识别空壳概率及异常特征；合同违约：统计5年内违约次数与规模；日常经营：分级展示高/中/低及关联风险的数量与最新详情（高/中/低风险每类最多返回最新10条）；存续情况：查询破产、解散及经营状态变化等潜在风险信息。

## 特性

- 空壳企业排查：识别空壳概率（低/中/高）及异常特征
- 合同违约情况：违约等级、5年内违约次数和规模
- 日常经营风险：自身风险（高/中/低分级）及关联风险统计，附最新明细
- 企业存续状态：破产风险、非正常解散、经营状态异常检测

## 快速上手

### 1. 获取 API Token

在 [启信宝会员中心-skill额度](https://www.qixin.com/app-center/home?route=skill-quota) 获取 API Token。

### 2. 配置 Token

设置环境变量 `QXBENT_API_TOKEN`：

**Windows：**
1. 按 `Win + R`，输入 `sysdm.cpl`，按回车
2. 点击"高级" -> "环境变量"
3. 在"用户变量"中点击"新建"
4. 变量名：`QXBENT_API_TOKEN`，变量值：粘贴你的 Token
5. 点击"确定"保存，重启 AI 应用

**Mac/Linux：**
```bash
echo 'export QXBENT_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 使用示例

```
帮我排查一下恒大地产集团有限公司的风险情况
```

```
查询深圳市某某科技有限公司是否有诉讼、失信、被执行等风险
```

```
这家公司是不是空壳公司？帮我查一下风险
```

## API 接口

| 接口名 | 描述 | 参数 |
|--------|------|------|
| getRiskAssessment | 查询企业风险排查（综合） | ename（企业名称）或 eid（企业ID） |

## 工具权限

- `Bash(node:*)`: 允许执行 Node.js/TypeScript 代码
- `Read`: 允许读取接口文档

## 运行时要求

**Bins**
- `node` (Node.js >= 16.x)
- `npm`

**Env**
- `QXBENT_API_TOKEN` (必需) - 启信宝 API 访问凭证

## 初始化

首次使用时需要安装依赖：

```bash
npm install
```

## 数据说明

- 支持通过企业名称（ename）或企业ID（eid）查询
- 企业名称支持模糊匹配，自动取最佳匹配结果
- 返回数据中包含 `ename` 字段，标识实际查询的企业
- 风险明细（highRiskItems/mediumRiskItems/lowRiskItems）各返回最新10条

## 参考文件

- 接口详细文档：读取 [references/getRiskAssessment.md](./references/getRiskAssessment.md)
