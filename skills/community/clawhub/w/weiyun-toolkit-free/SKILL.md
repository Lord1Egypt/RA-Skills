---
slug: weiyun-toolkit-free
name: weiyun-toolkit-free
version: 1.0.0
displayName: 微云工具箱(免费版)
summary: 微云网盘文件管理免费版：目录浏览、文件下载与上传，内置一键脚本与基础错误码指南。
license: Proprietary
edition: free
description: 微云工具箱（免费版）面向个人用户与独立开发者，封装微云网盘的日常文件操作：目录浏览、文件下载、文件上传。通过 MCP工具协议与微云网盘交互，所有文件哈希计算在本地完成，避免敏感数据外泄。Use
  when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。
tags:
- 云存储
- 微云
- 文件管理
- MCP工具
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L2
pricing_model: per_use
suggested_price: 19.9
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# 微云工具箱（免费版）

## 概述

微云网盘是腾讯提供的个人云存储服务。本工具箱通过 MCP工具协议与微云网盘交互，把日常的"列目录、下载、上传"三件事封装成可直接复制的工作流。免费版聚焦于"能用、够用"，专业版补齐分享、删除、重命名、移动、分类查询等进阶操作。

所有文件哈希计算与分片逻辑均在本地完成，服务端只接收预计算好的哈希值，既保护隐私又降低服务端压力。

## 核心能力

| 能力 | 说明 | 免费版 |
|---|---|---|
| 目录列表 | `weiyun.list` 按目录浏览文件与子目录 | 是 |
| 文件下载 | `weiyun.download` 批量获取 HTTPS 下载链接 | 是 |
| 文件上传 | `weiyun.upload` 两阶段协议，支持秒传 | 是 |
| 一键上传脚本 | `upload_to_weiyun.py` 自动计算参数 | 是 |
| 按分类查询 | `weiyun.list_by_category` 文档/图片/视频 | 否（专业版） |
| 分享外链 | `weiyun.gen_share_link` 含密码设置 | 否（专业版） |
| 批量删除 | `weiyun.delete` 支持回收站 | 否（专业版） |
| 重命名 | `weiyun.rename_file/dir` | 否（专业版） |
| 创建/移动 | `weiyun.create_dir/move_file/move_dir` | 否（专业版） |
| 版本检查 | `check_skill_update` 自动更新 | 否（专业版） |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：微云网盘文件管理、免费版、目录浏览、文件下载与上传、内置一键脚本与基、础错误码指南、微云工具箱、面向个人用户与独、立开发者、封装微云网盘的日、常文件操作、文件下载、文件上传、MCP、工具协议与微云网、盘交互、所有文件哈希计算、在本地完成、避免敏感数据外泄、Use、when、需要数据分析、报表生成、统计洞察、数据可视化时使用、不适用于实时流数、据处理、适用于独立开发者、企业团队和自动化、工作流场景等。

## 使用场景

### 场景一：下载网盘中的文档到本地
用户说"把我微云里的会议纪要下载下来"。Agent 应先调用 `weiyun.list` 浏览目录定位文件，拿到 `file_id` 与顶层 `pdir_key`，再调用 `weiyun.download` 获取下载链接，最后用 `curl -b` 携带 cookie 下载。

### 场景二：上传本地文件到网盘备份
用户说"把这个项目压缩包传到微云"。Agent 应直接调用一键脚本 `upload_to_weiyun.py`，传入文件路径与目标目录 `pdir_key`，无需手动计算分片哈希。

### 场景三：浏览网盘结构
用户说"看看我微云根目录有哪些东西"。Agent 调用 `weiyun.list`，参数 `limit=50, get_type=0`，回显 `dir_list` 与 `file_list`。

## 快速开始

### 60 秒上手
1. 确认已通过微云授权获得 MCP工具 token（存于环境变量 `WEIYUN_MCP_TOKEN`）
2. 浏览目录：调用 `weiyun.list`
3. 下载文件：调用 `weiyun.download` 获取链接后用 curl 下载
4. 上传文件：直接运行一键脚本

### 一键上传脚本（推荐）

```bash
# Linux/macOS
python3 （请参考skill目录中的脚本文件） /path/to/file --token <mcp_token> --pdir_key <dir_key>
# ...
# Windows PowerShell（需先切换 UTF-8 编码）
chcp 65001 >nul && python scripts\upload_to_weiyun.py C:\path\to\file --pdir_key <dir_key>
```

脚本参数：

| 参数 | 必填 | 说明 |
|:-----|:-----|:-----|
| `file_path` | 是 | 本地文件路径（位置参数） |
| `--token` | 是 | MCP工具 token（或设 `WEIYUN_MCP_TOKEN` 环境变量） |
| `--pdir_key` | 否 | 上传目标目录 key（不填使用 token 绑定目录） |
| `--env_id` | 否 | 环境标识（如 `sit-0cd15bb3`） |
| `--mcp_url` | 否 | MCP server 地址（默认官方端点） |
| `--max_rounds` | 否 | 最大上传轮数（默认 50） |

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

## 示例

### 目录列表查询

```text
调用 weiyun.list，参数：
  limit = 50
  get_type = 0    # 0-所有，1-仅目录，2-仅文件
```

响应包含 `pdir_key`（顶层目录 key，后续操作必填）、`dir_list`、`file_list`、`finish_flag`。

### 下载文件

```text
调用 weiyun.download，参数：
  items = [{"file_id": "<file_id>", "pdir_key": "<顶层 pdir_key>"}]
```

返回每个文件的 `https_download_url` 与 `cookie`，下载时必须携带：

```bash
curl -s -L -o <本地文件名> -b "<cookie>" "<https_download_url>"
```

### 上传文件（手动方式）

```text
阶段一：预上传
  filename, file_size, file_sha, block_sha_list, check_sha
  → file_exist=true 秒传成功
  → file_exist=false 获取 upload_key + channel_list
# ...
阶段二：分片上传
  upload_key, channel_list, channel_id, ex, file_data, filename
  → status=1 继续下一片
  → status=2 上传完成
```

## 最佳实践

### 1. pdir_key 取值规则
所有需要 `pdir_key` 的操作都必须使用 `weiyun.list` 响应**顶层**的 `pdir_key`，**不要**使用文件条目自身的 `pdir_key` 字段（该字段常为空字符串）。这是最常见的错误来源。

### 2. 下载 cookie 携带
`weiyun.download` 返回的下载链接必须用 `curl -b` 携带 cookie，且加 `-L` 跟随重定向，否则会 403。

### 3. 上传优先用脚本
手动计算 `block_sha_list` 容易出错（微云使用流式 SHA1 内部状态，非标准独立分块 SHA1）。优先使用 `upload_to_weiyun.py`，它内置哈希计算与重试逻辑。

### 4. 服务繁忙重试
遇到 `retcode=50000` 时，等待 2-5 秒后重试，最多 3 次。一键脚本已内置此逻辑。

### 5. 安全披露
上传脚本会读取本地文件与 `WEIYUN_MCP_TOKEN` 环境变量，并向受信任的微云 MCP端点 发起 HTTPS 请求。调用前应向用户确认文件路径，禁止用通配符触发上传。

## 常见问题

### Q1：下载时 pdir_key 应该填什么？
A：使用 `weiyun.list` 响应中**顶层**的 `pdir_key`，不是文件自身的 `pdir_key` 字段（该字段可能为空字符串）。

### Q2：上传报 "Cannot upload to a directory that you do not own"？
A：必须指定 `--pdir_key` 参数。先调用 `weiyun.list` 获取响应顶层的 `pdir_key`。

### Q3：分片上传通道 len=0？
A：每轮上传完一片后，通道列表可能全部 len=0，需要重新预上传获取下一批通道。一键脚本已自动处理。

### Q4：SHA1 不匹配？
A：确保分块 SHA 值使用流式 SHA1 内部状态（小端序），而非独立分块 SHA1。直接用一键脚本可避免此问题。

### Q5：file_sha 被覆盖？
A：服务端用最后一个 block 的 SHA 覆盖 file_sha，两者必须相等。一键脚本会自动保证这一点。

### Q6：通道 ID 不匹配？
A：上传分片时 `channel_id` 必须与 `channel_list` 中某个条目匹配，否则报错。

### Q7：Windows 下中文乱码？
A：执行 Python 脚本或命令前必须先 `chcp 65001 >nul` 切换控制台为 UTF-8，且 Windows 下用 `python` 而非 `python3`。

## 错误处理

| 错误码 | 名称 | 处理建议 |
|---:|---:|---:|
| 1192 | 参数错误，目录名无效 | 删除目录时缺少 `dir_name`（专业版功能） |
| 50000 | 服务繁忙 | 等待 2-5 秒执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，最多 3 次 |
| 117401 | 每日配额耗尽 | 次日零点重置，或开通会员 |
| 117402 | MCP工具 token 无效 | 重新生成 token |
| 117403 | 必填参数为空 | 检查 file_list/dir_list 是否完整 |
| 117404 | 参数不合法 | 检查 file_id/pdir_key 格式 |
| 117405 | 权限不足 | 确认文件属于当前用户 |

## 已知限制

本免费体验版限制以下高级功能：
- 按分类查询文件（`weiyun.list_by_category`，文档/图片/视频分类）
- 生成分享外链（`weiyun.gen_share_link`，含密码设置）
- 批量删除（`weiyun.delete`，支持回收站与彻底删除）
- 重命名文件/目录（`weiyun.rename_file/rename_dir`）
- 创建文件夹与移动文件/目录（`weiyun.create_dir/move_file/move_dir`）
- 技能版本自动检查更新（`check_skill_update`）
- 高级错误恢复与重试策略

解锁全部功能请使用专业版：`weiyun-toolkit-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.8+（运行上传脚本）
- **网络**：可访问 `https://www.weiyun.com` 域名

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由 Agent 平台内置 LLM 提供 |
| mcporter | CLI 工具 | 必需 | 用于调用微云 MCP工具 |
| requests | Python 库 | 必需 | `pip install requests` |
| 微云 MCP工具 token | 凭证 | 必需 | 通过微云授权获取 |
| curl | CLI 工具 | 必需 | 系统自带或安装 |

### API Key 配置
- **微云 MCP工具 token**：通过微云授权流程获取，存于环境变量 `WEIYUN_MCP_TOKEN`
- **环境标识**：SIT 环境需额外设置 `WEIYUN_ENV_ID`
- **禁止**：在 SKILL.md 或脚本中硬编码 token
- **端点白名单**：脚本仅接受 `https://*.weiyun.com` / `*.qq.com` 的 MCP server 端点

### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务
- **模型路由建议**：免费版使用低成本模型（如 GPT-4o-mini / Claude Haiku）
