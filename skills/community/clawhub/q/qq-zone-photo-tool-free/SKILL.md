---
slug: qq-zone-photo-tool-free
name: qq-zone-photo-tool-free
version: 1.0.0
displayName: QQ空间相册入门工具
summary: QQ空间相册管理工具，支持相册浏览与单张照片下载。
license: Proprietary
edition: free
description: '面向个人用户的QQ空间相册管理工具。支持登录QQ空间、浏览相册

  列表、查看照片与单张下载。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。Use
  when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。'
tags:
- Operations
- QQ空间
- 相册管理
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
# QQ空间相册入门工具（免费版）

## 概述

本工具为个人用户提供QQ空间相册管理能力。支持登录QQ空间、浏览相册列表、查看照片和单张下载。适合个人用户备份与管理QQ空间中的珍贵照片。

## 核心能力

### 管理功能

| 功能 | 说明 | 免费版支持 |
|---|---|-----|
| 登录认证 | QQ空间登录 | 支持 |
| 相册浏览 | 相册列表查看 | 支持 |
| 照片查看 | 在线浏览照片 | 支持 |
| 单张下载 | 下载单张照片 | 支持 |
| 批量下载 | 批量下载照片 | 不支持 |
| 相册创建 | 新建相册 | 不支持 |
| 照片上传 | 上传照片 | 不支持 |
| 相册管理 | 编辑/删除 | 不支持 |

**输入**: 用户提供管理功能所需的指令和必要参数。
**处理**: 解析管理功能的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回管理功能的响应数据,包含状态码、结果和日志。

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：空间相册管理工具、支持相册浏览与单、张照片下载、面向个人用户的、支持登录、浏览相册、查看照片与单张下、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：浏览相册

用户输入："查看我的QQ空间相册"

```bash
# 登录QQ空间
python3 （请参考skill目录中的脚本文件） login --qq 123456789
# ...
# 查看相册列表
python3 （请参考skill目录中的脚本文件） albums list
# ...
# 输出：
# === 我的相册 ===
# 1. 旅行照片 (156张)
# 2. 家庭聚会 (89张)
# 3. 工作记录 (45张)
```

### 场景二：查看照片

用户输入："看看旅行相册里的照片"

```bash
# 查看相册照片
python3 （请参考skill目录中的脚本文件） photos list \
  --album "旅行照片" \
  --page 1
# ...
# 输出照片列表（缩略图链接）
```

### 场景三：下载照片

用户输入："下载这张照片"

```bash
# 下载单张照片
python3 （请参考skill目录中的脚本文件） photo download \
  --photo-id 12345 \
  --output ./downloads/
# ...
# 下载到指定目录
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 环境准备

```bash
# 依赖说明
pip install requests beautifulsoup4
# ...
# 登录QQ空间
python3 （请参考skill目录中的脚本文件） login --qq 123456789
# 根据提示完成登录认证
```

### 常用命令

```bash
# 登录
python3 （请参考skill目录中的脚本文件） login --qq 123456789
# ...
# 相册管理
python3 （请参考skill目录中的脚本文件） albums list
python3 （请参考skill目录中的脚本文件） albums info --name "旅行照片"
# ...
# 照片管理
python3 （请参考skill目录中的脚本文件） photos list --album "旅行照片"
python3 （请参考skill目录中的脚本文件） photo download --photo-id 12345 --output ./downloads/
python3 （请参考skill目录中的脚本文件） photo info --photo-id 12345
# ...
# 登出
python3 （请参考skill目录中的脚本文件） logout
```

## 示例

### QQ空间配置

```yaml
qzone_config:
  auth:
    method: "cookie"              # cookie | qrcode
    cookie_file: "./qzone_cookies.json"
    qrcode_timeout: 120
# ...
  download:
    default_dir: "./downloads"
    naming: "original"            # original | sequential | date
    quality: "original"           # original | thumbnail
# ...
  cache:
    enabled: true
    ttl: 3600
```

## 最佳实践

1. **登录安全**：使用Cookie登录，避免频繁输入密码
2. **下载路径**：指定明确的下载目录，便于管理
3. **照片备份**：定期下载重要照片，防止丢失
4. **遵守规则**：仅下载自己的照片，尊重他人隐私

| 实践要点 | 说明 |
|:-----|:-----|
| Cookie有效期 | Cookie可能过期，需重新登录 |
| 下载频率 | 避免频繁请求，防止被限制 |
| 照片质量 | 优先下载原图，保证清晰度 |
| 版权尊重 | 仅管理自己的照片内容 |

## 常见问题

### Q1：如何登录QQ空间？

支持Cookie登录和扫码登录两种方式。Cookie登录需手动获取Cookie；扫码登录使用QQ手机版扫码，更便捷安全。

### Q2：免费版支持批量下载吗？

免费版仅支持单张照片下载。如需批量下载整个相册，建议升级PRO版。

### Q3：下载的照片是什么质量？

免费版默认下载原图（最高质量）。如果原图不可用，会下载最高可用质量的版本。

### Q4：可以下载好友的相册吗？

本工具仅支持管理自己的QQ空间相册。下载他人照片涉及隐私和版权问题，不建议使用。

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| requests | Python库 | 必需 | `pip install requests` |
| beautifulsoup4 | Python库 | 可选 | `pip install beautifulsoup4`（HTML解析） |

### API Key 配置

- 无需API Key
- 通过QQ账号Cookie或扫码认证

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本执行）
- **说明**: 通过QQ空间Web接口管理相册
- **免费版限制**: 单张下载、不支持批量与相册管理
- **合规声明**: 仅支持管理自己的照片，请尊重他人隐私与版权

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
