# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-07

### Changed
- 更新 SKILL.md 为中文描述
- README.md 改为中文优先（原 README.zh-CN.md）
- 添加 README.en.md（英文版）
- 删除 README.zh-CN.md
- 添加 ClawHub 安装说明
- 统一分支为 master（删除 main 分支）

### Improved
- 中文用户体验优化
- 安装说明更清晰
- 语言切换更方便

## [1.0.0] - 2026-03-06

### Added
- Initial release of RSS to WeChat skill
- Article parsing from RSS feeds or direct URLs
- AI-assisted HTML generation with WeChat format compliance
- Configurable branding (name, slogan, color)
- Optional cover image generation integration
- Optional WeChat publishing script integration
- Configuration system with local overrides
- Complete documentation (README, SKILL.md, html-template.md)
- Configuration validation and dependency checking
- Support for custom RSS sources and filtering
- Keyword-based article filtering
- Example configuration file

### Features
- **Universal**: Works with any RSS source or URL
- **Configurable**: Brand, style, keywords fully customizable
- **Modular**: Data fetching, content generation, publishing separated
- **Flexible**: AI assistant can adjust structure based on content
- **Secure**: Local config not tracked by git

### Documentation
- Quick start guide
- Configuration options
- HTML format requirements
- Troubleshooting guide
- Advanced usage examples
