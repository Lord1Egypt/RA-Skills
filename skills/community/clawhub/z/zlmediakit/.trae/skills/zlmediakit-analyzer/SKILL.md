---
name: "zlmediakit-analyzer"
description: "定期拉取 ZLMediaKit 仓库，查看最新的 Issue、Pull Request，并提供源码深度分析功能。当用户要求查看 ZLMediaKit 动态、Issue、PR 或分析其源码时触发调用。"
metadata: { "openclaw": { "requires": { "tools": ["git", "gh", "curl", "grep"] } } }
---

# ZLMediaKit Analyzer

该 Skill 用于定期跟踪和分析开源流媒体框架 [ZLMediaKit](https://github.com/ZLMediaKit/ZLMediaKit) 的最新动态，包括 Issue、Pull Request，并支持对其 C++11 源码进行深度分析。

## 环境要求

- 已安装 `git` (用于克隆和拉取代码)
- 已安装 GitHub CLI `gh` (用于获取 Issue 和 PR 列表)
- 可选：配置 `GITHUB_TOKEN` 环境变量以避免 API 速率限制

## Workflow 工作流

当用户触发此 Skill 时，Agent 应按照以下步骤执行：

### 1. 检查并拉取最新代码 (Sync Code)

检查本地是否存在 ZLMediaKit 代码库（默认路径：`D:\.openclaw\workspace\ZLMediaKit`）。
- **如果不存在**，使用 `RunCommand` 工具执行克隆：
  ```powershell
  git clone https://github.com/ZLMediaKit/ZLMediaKit.git D:\.openclaw\workspace\ZLMediaKit
  ```
- **如果已存在**，则进入目录并拉取最新代码：
  ```powershell
  cd D:\.openclaw\workspace\ZLMediaKit
  git pull origin master
  ```

### 2. 获取最新动态 (Fetch Issues & PRs)

使用 `RunCommand` 工具调用 `gh` CLI 获取最新的 5 个 Issue 和 Pull Request：
- **查看最近的 Issues**：
  ```powershell
  gh issue list -R ZLMediaKit/ZLMediaKit --limit 5 --state all
  ```
- **查看最近的 Pull Requests**：
  ```powershell
  gh pr list -R ZLMediaKit/ZLMediaKit --limit 5 --state all
  ```
*(注：如果没有 `gh` CLI，可以使用 `curl -s https://api.github.com/repos/ZLMediaKit/ZLMediaKit/issues?per_page=5` 替代)*

### 3. 源码深度分析 (Code Analysis)

当用户要求分析特定模块或源码（如 RTSP/RTMP、WebRTC、网络 IO 模型等）时：
- 优先建议使用内置的 **search agent** (`default_api:search`) 或 **SearchCodebase** 工具，在 `D:\.openclaw\workspace\ZLMediaKit` 目录下搜索相关实现。
- 结合 ZLMediaKit 项目的特点进行解读：
  - 基于 **C++11** 开发，无裸指针，采用智能指针管理内存。
  - 使用 **多路复用/多线程/异步网络 IO 模式**。
  - 支持多种协议互转 (RTSP/RTMP/HLS/WebRTC 等)。
- 对关键的类（如 `TcpServer`, `EventPoller`, `Session` 等）或请求处理流程进行追踪，生成函数调用栈或架构解析。

### 4. 生成报告 (Generate Report)

根据用户需求，综合社区动态（最新的 Issue/PR 讨论）与源码分析结果，输出结构化、排版清晰的 Markdown 报告。报告中应包含代码文件的具体路径（如 `src/Network/TcpServer.cpp`）及核心逻辑解释。

## 计划任务 / 定期拉取说明

如需**定期**执行，可通过 OpenClaw 或系统级定时任务（如 Windows 任务计划程序、Cron）调用该 Skill 对应的执行脚本，自动触发 "拉取代码 -> 检查 PR -> 生成简报" 的工作流。
