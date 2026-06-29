# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-06-29

### Changed
- **版本号控制改为手动**：移除 workflow 中的 `--bump` 参数，版本号完全由 SKILL.md 控制
- **版本号跃升到 2.0.0**：标记 relay 模式核心功能修复完成

### Fixed
- **relay 模式 CSS 内联丢失**：`_draft_create_relay()` 和 `_draft_update_relay()` 现在正确传递 `<style>` 标签，`relay_client.py` 新增 `_inline_css()` 函数
- **relay 模式更新草稿失败（40007 invalid media_id）**：每次 update 强制生成新封面，`thumb_media_id` 正确传递
- **relay_client.py `update_draft` 函数签名**：新增 `thumb_media_id` 参数，支持直接使用已有封面 ID

---

## [1.5.1] - 2026-06-28

### Fixed
- **digest 长度修正**：120 → 128 字（与微信官方文档一致），按"字"混合计数（中文=1字，英文=0.5字）
- **author 长度修正**：新增 16 字上限截断（中文=1字，英文=0.5字混合计数）
- **title 长度修正**：新增 32 字上限截断（中文=1字，英文=0.5字混合计数）
- **封图生成失败不再静默跳过**：直接报错并提示解决方法，修复字体路径跨平台支持（Windows/macOS/Linux）
- **服务端 create_draft 增加 thumb_b64 空值校验**：清晰报错而非微信 API 神秘错误码

## [1.5.0] - 2026-06-27

### Added
- **HTTP 402 AI 付协议支持**：客户端支持标准 HTTP 402 AI 付协议（push_article → alipay-bot → finish_push）
- **Hybrid 混合模式**：direct 优先，IP 白名单失败自动切换 relay
- **Relay/Hybrid 模式支持**：为 7 个功能添加 relay/hybrid 模式支持
- **relay_client 增强**：添加 `_put` 函数，支持 PUT 方法

### Changed
- **统一命名风格**：`RELAY_SERVER` → `WECHAT_OA_SERVER` 统一命名
- **update_draft 改用 PUT 方法**：符合微信 API 规范
- **list_materials 移除 keyword 参数**：简化接口

### Fixed
- **digest 长度修复**：64 bytes 限制处理
- **draft_find 返回格式统一**：标准化返回数据结构

## [1.4.0] - 2026-04-15

### Added
- **正文配图自动生成**：`generate_infographic.py` 支持生成流程图、对比图、时间线、文字卡片、统计图
- **relay push 模式**：支持通过 relay 服务器推送文章
- 新增 `infographic` 命令到 SKILL.md

### Changed
- **自动去除外层容器卡片样式**：避免正文被大方框包围

### Fixed
- **图片URL替换Bug**：HTML源码中的双反斜杠路径（如 `C:\\Users\\...`）无法被替换为微信CDN地址，导致配图显示打叉。修复：上传前预处理，统一规范化所有路径格式

## [1.3.1] - 2026-04-14

### Fixed
- 自动去除外层容器卡片样式，避免正文被大方框包围

### Changed
- 配套公众号信息更新

## [1.3.0] - 2026-04-12

### Added
- **自动上传正文配图**：创建/更新草稿时，自动提取本地图片上传到微信素材库并替换 URL
- 支持 `.md` 文件直接创建草稿（自动解析 Markdown 语法）
- 集成 `premailer` 进行专业 CSS 内联转换
- 素材库管理增强：交互式删除 + 批量删除 + 关键词过滤
- `materialcount`：获取各类永久素材总数
- `materials <type> <count> [offset] [keyword]`：批量获取素材列表，支持关键词过滤
- `materialdel [media_id...]` 或交互式删除素材
- 更新测试报告，添加 Bug 修复记录

### Fixed
- `materialdel` 报错问题
- `materials` 命令中文乱码
- `parse_md_article` 保留图片语法而非过滤

## [1.2.0] - 2026-04-11

### Added
- `design.md` 公众号排版规范（容器宽度、字体、配色、布局、标题、内容结构、CSS/HTML/JS 限制）
- SKILL.md 增加排版说明章节（⚠️ 排版规范必读）
- 配套公众号信息（GitHub + 邮箱 + 公众号）

### Fixed
- `parse_html_article` 标题提取支持 h1/h2 多级兜底，修复无标题问题

## [1.1.1] - 2026-04-08

### Added
- 素材管理命令：`materialcount` / `materials` / `materialdel`
- 用户管理命令：`userinfo` / `userlist` / `userstat`
- 草稿搜索：`find <关键词>`
- 批量删除草稿：`batch-del <id1> [id2] ...`
- SKILL.md 触发词扩展

### Fixed
- 标题字数限制修正（64 bytes → 64 characters）
- 临时封面图 `cover_latest.png` 从版本控制移除

## [1.1.0] - 2026-04-08

### Fixed
- 中文乱码问题
- 封面图路径问题

## [1.0.2] - 2026-04-07

### Added
- 初始版本发布
- 草稿列表查看（`list`）
- 创建草稿（`create`）
- 更新草稿（`update`）
- 删除草稿（`delete`）
- 生成封面图（`cover`）
