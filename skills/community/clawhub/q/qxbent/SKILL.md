---
name: qxbent
description: 启信宝企业信息查询工具，提供企业工商信息、股东信息、主要人员、变更记录等查询功能。支持通过企业名称查询，返回标准化的企业数据。
license: MIT
metadata: { "openclaw": { "requires": { "env": ["QXBENT_API_TOKEN"], "bins": ["node", "npm"] }, "install": [ { "id": "npm-deps", "kind": "node", "package": "axios", "label": "Install Node.js dependencies" } ] } }
---
# 启信宝企业信息查询

## 概述

启信宝（QiXinBao）企业信息查询 Skill，提供全面的企业数据查询服务。本 Skill 基于启信宝 API，支持通过企业名称查询工商信息、股东信息、主要人员、变更记录等数据。

## 特性

- 🏢 **企业工商信息** - 查询企业注册信息、经营状态等基础数据
- 👥 **股东信息** - 获取企业股东持股情况
- 👤 **主要人员** - 查询企业高管、董事等关键人员信息
- 📋 **变更记录** - 追踪企业工商变更历史
- 🔍 **智能识别** - 支持通过企业名称自动查询

## 快速上手

### 1. 获取 API Token

首先需要获取启信宝 API Token。Token 格式类似：`ent_xxx_xxxxxxxxxx`

如果没有，请联系启信宝平台管理员获取。

### 2. 配置 Token

**⚠️ 安全提示**：Token 是敏感凭证，请妥善保管。**必须使用环境变量配置**，不要在对话中提供 token。

设置环境变量 `QXBENT_API_TOKEN`：

**Windows 永久配置：**
1. 按 `Win + R`，输入 `sysdm.cpl`，按回车
2. 点击"高级" → "环境变量"
3. 在"用户变量"中点击"新建"
4. 变量名：`QXBENT_API_TOKEN`
5. 变量值：粘贴你的 Token
6. 点击"确定"保存
7. 重启 AI 应用

**Mac/Linux 永久配置：**
```bash
# 如果使用 bash
echo 'export QXBENT_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc

# 如果使用 zsh (Mac 默认)
echo 'export QXBENT_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

配置成功后，AI 会自动从环境变量中读取 token，无需在对话中提供。

### 3. 使用示例

在支持的 AI 智能体中加载此 Skill 后，可以用自然语言进行查询：

**查询企业工商信息**：
```
查询上海合合信息科技发展有限公司的工商信息
```

**查询企业股东**：
```
帮我查一下恒大地产集团有限公司的股东信息
```

**查询主要人员**：
```
查询上海合合信息科技发展有限公司的主要人员
```

**查询变更记录**：
```
查看上海合合信息科技发展有限公司最近的变更记录
```

## API 接口列表

| 接口名 | 描述 | 参数 |
|--------|------|------|
| getEnterpriseInformation | 查询企业工商信息 | ename（企业名称） |
| getPartnerListV3 | 查询企业股东信息 | ename（企业名称） |
| getEmployeesListV4 | 查询企业主要人员 | ename（企业名称） |
| getPagingEntBasicInfo | 查询企业变更记录 | ename（企业名称） |

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

首次使用时，如果遇到模块未找到错误，需要先安装依赖：

```bash
# 在 skill 根目录执行
npm install
```

AI 助手会在必要时自动检测并执行此命令。

## 数据说明

- 所有接口都支持通过企业名称（ename）查询
- 企业名称会自动转换为企业 ID 进行查询
- 股东信息、主要人员默认返回前 10 条记录
- 变更记录默认返回最近 10 条记录

### 企业名称匹配说明

当使用不完整或简称查询时，可能会遇到以下情况：

**情况 1: 精确匹配**
- 输入：`上海合合信息科技发展有限公司`
- 结果：直接返回企业信息

**情况 2: 多个候选企业**
- 输入：`胜宏科技`
- 结果：返回 `MultipleMatchError` 错误，包含候选企业列表
- AI 处理：展示候选企业列表，请用户选择或提供更完整的企业名称

示例候选列表：
```
找到多个匹配的企业，请选择：
1. 胜宏科技（惠州）股份有限公司
2. 惠州市胜宏科技研究院有限公司
3. 南通胜宏科技有限公司
4. 武汉市胜宏科技有限公司
5. 北京胜宏科技有限公司
```

**情况 3: 企业未找到**
- 输入：`不存在的企业名称`
- 结果：返回 `EnterpriseNotFoundError` 错误

### AI 交互流程建议

1. 用户使用简称查询 → 捕获 `MultipleMatchError`
2. AI 展示候选企业列表
3. 用户选择具体企业
4. AI 使用完整企业名称重新查询

## 注意事项

### 安全性

- ⚠️ **Token 安全**：API Token 是敏感凭证，切勿在对话中提供或分享给他人
- ✅ **推荐配置**：必须通过环境变量 `QXBENT_API_TOKEN` 配置，该变量仅存储在本地系统
- 🔒 **访问范围**：Token 仅用于访问 `https://external-api.qixin.com/skill/ent/public` API 端点
- 📊 **权限控制**：建议向 API 提供商申请权限受限的 token（如限制每日配额）

### 使用条款

本 Skill 仅供学习和研究使用，请勿用于商业用途。使用时请遵守启信宝 API 的使用条款和访问限制。
