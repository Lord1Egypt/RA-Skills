# Zion.app 无代码后端 Skill

本 Skill 用于将 [Zion.app](https://www.functorz.com) 作为纯后端服务使用，并在此基础上构建自定义前端应用或小程序。

## 简介

Zion 是一个全栈无代码开发平台。通过本 Skill，你可以仅使用 Zion 作为「后台数据库 + 接口层」，前端部分则由其他工具或框架自行实现，从而将前后端解耦。

## 关键地址

- **数据接口**：`https://zion-app.functorz.com/zero/{projectExId}/api/graphql-v2`
- **实时推送**：`wss://zion-app.functorz.com/zero/{projectExId}/api/graphql-subscription`
- **管理后台接口**：`https://zionbackend.functorz.com/api/graphql`
- **登录页面**：`https://auth.functorz.com/login`

## 快速开始

### 1. 安装依赖

进入 `scripts` 目录并安装运行依赖：

```bash
cd scripts
npm install
```

### 2. 登录认证

**方式一：OAuth 浏览器授权（推荐）**

```bash
npm run auth
```

执行后系统会自动打开浏览器，完成授权后令牌将自动保存。

**方式二：邮箱 / 密码登录**

```bash
npm run auth:email <邮箱> <密码>
```

### 3. 获取项目 Runtime Token

获取权限后，还需获取指定项目的运行时管理员令牌：

```bash
npm run fetch-token -- <projectExId>
```

其中 `<projectExId>` 为 Zion 后台中的项目唯一标识。

### 4. 常用 CLI 工具

**执行 GraphQL 查询或变更：**

```bash
npm run gql -- <projectExId> <身份> '<查询内容>' '[参数]'
```

**订阅实时事件：**

```bash
npm run subscribe -- <projectExId> <身份> '<订阅内容>' '[参数]'
```

**搜索项目：**

```bash
npm run meta -- search-projects [项目关键词]
```

**获取项目 Schema：**

```bash
npm run meta -- fetch-schema <projectExId>
```

## 凭证存储

所有令牌均自动保存在项目根目录的 `.zion/credentials.yaml` 文件中，结构如下：

```yaml
developer_token:
  token: "开发者令牌"
  expiry: "过期时间"

project:
  exId: "项目编号"
  name: "项目名称"
  admin_token:
    token: "项目管理员令牌"
    expiry: "过期时间"
```

保存后无需重复登录即可复用。

## 安装本 Skill 后的主要用途

1. **通过 Openclaw 直接操作后台**

   例如，在 IM 工具中向 Openclaw 发送指令：「查询今日订单」，Openclaw 即可连接到你的 Zion 项目并返回结果；发送「将张三的订单状态更新为已发货」，也可直接完成修改。本 Skill 的作用正是为 Openclaw 提供连接 Zion 后台所需的能力与凭证管理。

2. **快速连接 Zion 后台**

   自动完成登录、获取令牌、保存凭证等流程，无需手动查阅接口文档。

3. **查看项目信息**

   可快速检索项目列表、查看数据库表结构及工作流配置。

4. **便捷查询后台数据**

   通过命令行直接执行查询语句并即时查看结果，无需预先搭建前端页面。

5. **测试不同用户权限**

   支持以管理员、普通用户或匿名用户身份执行操作，便于验证权限配置是否正确。

## Zion 支持的后台能力

- **数据库操作**：通过 GraphQL 实现完整的增删改查
- **工作流（Actionflows）**：支持同步与异步的业务流程自动执行
- **AI 智能体**：集成多模态 AI，实现对话、识别等能力
- **文件上传**：支持图片、视频、文档等二进制资源的存储与读取
- **第三方接口**：可调用外部 API，例如支付、短信等服务平台
- **实时推送**：基于 WebSocket 的数据变更实时通知

## 许可证

MIT
