# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-04-15

### Added

- 新增 `get_latest_email` MCP Tool 和客户端方法，支持直接获取指定邮箱最近收到的一封邮件（含完整内容）
- 新增 OpenAPI 端点定义 `GET /v1/emails/latest`
- 新增 `get_latest_email` 工具参数定义（`tool_definition.json`）
- SKILL.md 新增「获取最新邮件」使用示例及推荐的轮询验证工作流

## [1.0.0] - 2026-03-18

### Added

- MCP Server 支持（基于 FastMCP），提供 `get_domains`、`list_emails`、`get_email_content` 三个 Tool
- Python 客户端封装（`TemporamClient`），支持域名查询、邮件列表、邮件详情、随机邮箱生成
- OpenAPI 3.0 接口定义
- Tool 参数定义（`tool_definition.json`）
- API 参考文档
