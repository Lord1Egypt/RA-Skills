---
name: qxb-gs-basic-info
description: 可快速验证企业真实性、经营状态，适用于商务合作前的背景核查、供应链准入审核、招投标资质验证，合同主体审查等场景，确保企业信息准确可靠。
license: MIT
metadata: { "openclaw": { "requires": { "env": ["QXBENT_API_TOKEN"], "bins": ["node", "npm"] }, "install": [ { "id": "npm-deps", "kind": "node", "package": "axios", "label": "Install Node.js dependencies" } ] } }
---

# 企业工商基本信息查询

## 概述

查询企业的基本信息，包括统一社会信用代码，法定代表人，成立日期，注册资本，经营状态，疑似实控人等。

## 特性

- 查询企业基本工商注册信息
- 支持企业名称模糊匹配，自动取最佳匹配结果
- 返回疑似实控人及持股比例
- 返回社保参保人数（反映企业实际经营规模）
- 返回纳税人资质信息

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
查询深圳市腾讯计算机系统有限公司的工商基本信息
```

```
帮我查一下华为技术有限公司的经营状态和注册资本
```

## API 接口

| 接口名 | 描述 | 参数 |
|--------|------|------|
| getGsBasicInfo | 查询企业工商基本信息 | ename（企业名称）或 eid（企业ID） |

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

## 参考文件

- 接口详细文档：读取 [references/getGsBasicInfo.md](./references/getGsBasicInfo.md)
