---
name: qxb-listed-info
description: A 股 + 新三板 + H 股跨市场上市主体综合信息查询工具，一站式聚合两大资本市场的企业公开披露数据，标准化整合多维度字段，可快速完成单企业信息全景调取、多标的横向对比，高效解决跨市场上市企业信息零散、口径不一、查询繁琐的痛点，适配各类商业分析、投研研判、企业尽调等工作场景。
license: MIT
metadata: { "openclaw": { "requires": { "env": ["QXBENT_API_TOKEN"], "bins": ["node", "npm"] }, "install": [ { "id": "npm-deps", "kind": "node", "package": "axios", "label": "Install Node.js dependencies" } ] } }
---

# 上市信息综合查询

## 概述

查询上市企业的基本信息、股东信息、财务报表数据。

## 特性

- 跨市场覆盖：自动识别 A 股、新三板、H 股，符合条件的全部返回
- 基本行情：证券代码、上市日期、总市值、流通市值、市盈率、市净率等
- 股东结构：十大股东、十大流通股东（A股）、主要股东（H股）
- 财务报表：最新一期主要财务指标（收入/利润/资产/负债/现金流/各项比率）

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
查询贵州茅台的上市信息，包括市值和财务数据
```

```
帮我看看中国平安在A股和H股的上市情况
```

```
查询宁德时代的十大股东和最新财务报表
```

## API 接口

| 接口名 | 描述 | 参数 |
|--------|------|------|
| getListedInfo | 查询上市信息（综合） | ename（企业名称）或 eid（企业ID） |

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
- 一个企业可能同时有多种上市类型（A股+H股），符合条件的都会返回
- 财务报表返回最新一期数据
- A股和新三板的财务字段结构相同，H股为独立字段结构

## 参考文件

- 接口详细文档：读取 [references/getListedInfo.md](./references/getListedInfo.md)
