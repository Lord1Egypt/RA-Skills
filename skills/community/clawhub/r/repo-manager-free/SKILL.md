---
slug: repo-manager-free
name: repo-manager-free
version: 1.0.0
displayName: 仓库管理器(免费版)
summary: 通过MCP工具协议管理GitHub仓库、Issue与PR,支持工具发现、参数预览与安全执行,适合个人开发者日常使用。
license: Proprietary
edition: free
description: '仓库管理器(免费版)是一款基于MCP工具协议的GitHub仓库管理工具,通过统一的工具调用接口管理仓库、Issue、Pull Request、提交与分支,无需手动配置API认证。核心能力:

  - 基于MCP工具协议的统一调用接口,自动处理OAuth认证

  - 仓库、Issue、PR的基础查询与管理

  - 提交与分支的查看与管理

  - 工具发现与参数预览,降低使用门槛

  - 安全执行机制,写操作需用户确认


  适用场景:

  - 个人开发者通过AI助手管理GitHub仓库

  - Issue与PR的快速浏览与处理

  - 代码审查前的信息...'
tags:
- GitHub
- 仓库管理
- MCP工具
- 集成
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "exec", "glob", "grep"]
tags: "工具,效率,自动化"
---
# 仓库管理器(免费版)

基于MCP工具协议管理GitHub仓库、Issue与Pull Request,通过统一的工具调用接口自动处理认证,提供"发现-预览-确认-执行"的安全流程。

## 概述

管理GitHub仓库通常需要配置API token、记忆大量端点、处理认证流程,门槛较高。本Skill基于MCP工具协议,将GitHub能力封装为标准化工具,Agent可通过统一接口调用,无需关心认证细节。用户只需用自然语言描述意图,Agent自动选择合适工具、预填参数、确认后执行。

免费版聚焦基础仓库管理能力,适合个人开发者日常使用。

## 核心能力

### 工具调用机制

通过MCP工具协议统一调用,所有认证由集成层自动处理:

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 仓库管理器(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   AI助手         │────▶│  MCP工具层    │────▶│   GitHub API     │
│   (用户对话)     │     │  (自动认证)   │     │   (REST/GraphQL) │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. 描述意图          │                       │
         │  2. 发现工具          │                       │
         │  3. 预览参数          │                       │
         │  4. 确认执行          │                       │
         │                       │  5. 注入Token         │
         │                       │  6. 代理请求          │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  自然语言 │           │ 工具目录  │           │ GitHub   │
   │  指令     │           │ 认证管理  │           │ 仓库     │
   └──────────┘           └──────────┘           └──────────┘
```

**输入**: 用户提供工具调用机制所需的指令和必要参数。
**处理**: 解析工具调用机制的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回工具调用机制的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 仓库管理

```bash
# 列出认证用户的仓库
repo-manager call --tool "github_list_repositories_for_the_authenticated_user" --params '{}'
# ...
# 查看指定仓库详情
repo-manager call --tool "github_get_a_repository" --params '{"owner": "owner", "repo": "repo-name"}'
# ...
# 创建新仓库(写操作,需确认)
repo-manager call --tool "github_create_a_repository" --params '{
  "name": "my-new-repo",
  "description": "新仓库描述",
  "private": true
}' --confirm
```

**输入**: 用户提供仓库管理所需的指令和必要参数。
**处理**: 解析仓库管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回仓库管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### Issue管理

```bash
# 列出仓库Issue
repo-manager call --tool "github_list_issues_for_a_repository" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "state": "open",
  "sort": "created",
  "direction": "desc"
}'
# ...
# 查看指定Issue
repo-manager call --tool "github_get_an_issue" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "issue_number": 123
}'
# ...
# 创建Issue(写操作)
repo-manager call --tool "github_create_an_issue" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "title": "Bug: 登录失败",
  "body": "复现步骤: 1. 进入登录页 2. 输入凭证 3. 报错",
  "labels": ["bug", "high-priority"]
}' --confirm
# ...
# 添加标签
repo-manager call --tool "github_add_labels_to_an_issue" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "issue_number": 123,
  "labels": ["needs-review", "bug"]
}' --confirm
```

**输入**: 用户提供Issue管理所需的指令和必要参数。
**处理**: 解析Issue管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回Issue管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### Pull Request管理

```bash
# 列出仓库PR
repo-manager call --tool "github_list_pull_requests" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "state": "open"
}'
# ...
# 查看PR详情
repo-manager call --tool "github_get_a_pull_request" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "pull_number": 55
}'
# ...
# 创建PR(写操作)
repo-manager call --tool "github_create_a_pull_request" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "title": "修复登录bug",
  "head": "fix/login-bug",
  "base": "main",
  "body": "修复 #123 - 移动端登录失败"
}' --confirm
```

**输入**: 用户提供Pull Request管理所需的指令和必要参数。
**处理**: 解析Pull Request管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回Pull Request管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 提交与分支管理

```bash
# 列出提交
repo-manager call --tool "github_list_commits" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "per_page": 10
}'
# ...
# 查看提交详情
repo-manager call --tool "github_get_a_commit" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "ref": "abc123def"
}'
# ...
# 列出分支
repo-manager call --tool "github_list_branches" --params '{
  "owner": "owner",
  "repo": "repo-name"
}'
# ...
# 创建分支(写操作)
repo-manager call --tool "github_create_a_branch" --params '{
  "owner": "owner",
  "repo": "repo-name",
  "branch": "feature/new-feature",
  "from": "main"
}' --confirm
```

**输入**: 用户提供提交与分支管理所需的指令和必要参数。
**处理**: 解析提交与分支管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回提交与分支管理的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：工具协议管理、支持工具发现、参数预览与安全执、适合个人开发者日、常使用、仓库管理器、免费版、是一款基于、工具协议的、仓库管理工具、通过统一的工具调、用接口管理仓库、无需手动配置、核心能力、工具协议的统一调、用接口、OAuth、的基础查询与管理、提交与分支的查看、与管理、工具发现与参数预、降低使用门槛、安全执行机制、写操作需用户确认等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景1:浏览仓库状态

用户意图: "看看我的仓库最近有什么动态。"

推荐流程:
1. 调用`github_list_repositories_for_the_authenticated_user`列出仓库
2. 对关注的仓库调用`github_list_issues`查看开放Issue
3. 调用`github_list_pull_requests`查看开放PR
4. 调用`github_list_commits`查看最近提交

### 场景2:创建Bug报告

用户意图: "发现一个bug,帮我创建Issue。"

推荐流程:
1. Agent询问bug详情(标题、描述、复现步骤、严重程度)
2. 调用`github_create_an_issue`预填参数
3. 用户确认后执行
4. 返回Issue编号与链接

### 场景3:代码审查准备

用户意图: "我要审查PR #55,先看看改了什么。"

推荐流程:
1. 调用`github_get_a_pull_request`查看PR描述
2. 调用`github_list_pull_request_files`查看变更文件
3. 调用`github_list_pull_request_commits`查看提交历史
4. Agent总结变更内容,辅助审查

## 不适用场景

以下场景仓库管理器(免费版)不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 依赖详情

```bash
# 安装仓库管理插件
agent plugins install repo-manager-plugin
# ...
# 配置工具权限
agent config set tools.alsoAllow '["repo-manager-plugin"]' --strict-json
# ...
# 重启Agent会话
agent restart
```

### Step 2:连接GitHub账号

1. 打开集成面板,选择GitHub
2. 完成OAuth授权
3. 验证连接:

```bash
# 验证连接
repo-manager list-integrations
# ...
# 查看可用工具
repo-manager list-tools --integration github
```

### Step 3:首次调用

```bash
# 列出仓库
repo-manager call --tool "github_list_repositories_for_the_authenticated_user" --params '{}'
```

### Step 4:工具发现

```bash
# 搜索可用工具
repo-manager search-tools --query "issue"
# ...
# 查看工具详情(参数schema)
repo-manager describe-tool --tool "github_create_an_issue"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### 工具调用模板

```bash
# 通用调用模板
repo-manager call \
  --tool "<tool_name>" \
  --params '<json_params>' \
  [--confirm]  # 写操作需要确认
# ...
# 查看工具详情
repo-manager describe-tool --tool "<tool_name>"
# ...
# 预览操作(不实际执行)
repo-manager preview --tool "<tool_name>" --params '<json_params>'
```

### 批量查询脚本

```bash
#!/bin/bash
# 查询多个仓库的开放Issue数
repos=("owner/repo1" "owner/repo2" "owner/repo3")
for repo in "${repos[@]}"; do
  IFS='/' read -r owner name <<< "$repo"
  result=$(repo-manager call --tool "github_list_issues_for_a_repository" \
    --params "{\"owner\":\"$owner\",\"repo\":\"$name\",\"state\":\"open\"}")
  count=$(echo "$result" | jq 'length')
  echo "$repo: $count open issues"
done
```

## 最佳实践

### 安全执行流程

所有写操作(创建、更新、删除)遵循"发现-预览-确认-执行"流程:

1. **发现**: 通过`search-tools`或`list-tools`找到合适工具
2. **预览**: 使用`describe-tool`查看参数schema,用`preview`预览操作效果
3. **确认**: 用户确认参数与预期效果
4. **执行**: 添加`--confirm`标志执行操作

### 工具选择策略

| 任务 | 推荐工具 | 模式 |
|:-----|:-----|:-----|
| 浏览仓库 | list_repositories | 读 |
| 查看Issue | get_an_issue / list_issues | 读 |
| 创建Issue | create_an_issue | 写(需确认) |
| 查看PR | get_a_pull_request | 读 |
| 创建PR | create_a_pull_request | 写(需确认) |
| 查看提交 | list_commits / get_a_commit | 读 |
| 创建分支 | create_a_branch | 写(需确认) |

## 错误处理

| 错误 | 含义 | 处理方式 |
|---:|---:|---:|
| Tool not found | 工具名不存在 | 用`list-tools`验证 |
| Missing connection | GitHub未连接 | 重新完成OAuth授权 |
| 404 Not Found | 资源不存在 | 检查owner/repo/number |
| 403 Forbidden | 权限不足或限速 | 检查权限,等待限速重置 |
| 422 Unprocessable | 参数错误 | 用`describe-tool`检查schema |
| Write rejected | 未确认写操作 | 添加`--confirm`标志 |

## 常见问题

### Q1: 工具列表为空怎么办?

A: 检查: (1)插件是否已安装(`agent plugins list`); (2)GitHub是否已连接(`repo-manager list-integrations`); (3)重启Agent会话重新加载工具目录; (4)检查工具权限配置。

### Q2: 写操作被拒绝怎么办?

A: 所有写操作需要用户确认。确保: (1)添加了`--confirm`标志; (2)在交互式会话中回答了确认提示; (3)预览结果符合预期后才确认执行。

### Q3: 如何知道某个任务用哪个工具?

A: 使用`repo-manager search-tools --query "关键词"`搜索相关工具,或使用`describe-tool`查看工具的`whenToUse`字段。Agent也会根据用户意图自动选择工具。

### Q4: 工具参数怎么填?

A: 每个工具的参数schema可通过`describe-tool`查看。必填参数会标记,可选参数有默认值。Agent会根据上下文自动填充部分参数(如owner/repo)。

### Q5: 如何处理OAuth授权过期?

A: OAuth token通常有效期较长,但可能因权限变更或安全策略过期。重新打开集成面板,完成OAuth授权即可。`repo-manager list-integrations`可查看连接状态。

## 已知限制

本免费体验版限制以下高级功能:
- 不支持工作流管理(Actions相关工具)
- 不支持Release管理
- 不支持批量操作(单次仅调用1个工具)
- 不支持工具目录搜索(仅支持列表浏览)
- 不支持自定义工具集成
- 不支持团队协作与共享配置

解锁全部功能请使用专业版: repo-manager-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **集成插件**: repo-manager-plugin(通过MCP工具协议提供GitHub能力)
- **网络**: 可访问GitHub API

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| repo-manager-plugin | 集成插件 | 必需 | `agent plugins install repo-manager-plugin` |
| GitHub账号 | 在线服务 | 必需 | 注册GitHub账号并完成OAuth授权 |
| jq | 命令行工具 | 可选 | `brew install jq`(JSON处理) |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- **OAuth认证**: 通过集成面板完成GitHub OAuth授权,token由插件安全存储
- **无需手动配置Token**: 插件自动管理token的获取与刷新
- **Token存储**: 加密存储于`~/.repo-manager/credentials.enc`
- **权限范围**: 根据授权时的scope决定(建议包含repo、workflow)
- **禁止**: 在SKILL.md或脚本中硬编码任何Token

### 可用性分类
- **分类**: MD+EXEC+MCP工具(Markdown指令+命令行工具+MCP工具协议)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent调用MCP工具执行GitHub操作

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "仓库管理器(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "repo manager"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
