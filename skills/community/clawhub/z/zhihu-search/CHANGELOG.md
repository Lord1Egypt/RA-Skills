# Changelog

All notable changes to zhihu-search will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-06-17

### Added
- **2 个新 API 命令**:
  - `column-articles <c_id>` — 抓专栏内文章列表 (走 `/api/v4/columns/<c_id>/articles`)
  - `comments <aid>` — 抓答案的评论 (走 `/api/v4/answers/<aid>/comments`,绕开 comment_v5 反爬)
- `paths` 命令 — 在两个脚本中都能打印当前路径配置
- `paths.py` — 集中管理所有路径,支持环境变量覆盖 + 自包含部署
- `$SKILL/data/` 目录结构 (含 `.gitkeep`, 全部 git 排除)
- 完整 GitHub 发布文件: `README.md` / `CHANGELOG.md` / `LICENSE` / `CONTRIBUTING.md` / `.gitignore`
- 升级 SKILL.md frontmatter (含 `version` / `emoji` / `homepage` / `metadata.openclaw`)

### Changed
- **路径从 `/tmp/zhihu/` 迁到 `$SKILL/data/`** — 自包含,git clone 即可用
- 老的 `/tmp/zhihu/` 路径**完全向后兼容**(如果存在,自动用老的)
- 环境变量从 `ZHIHU_COOKIE` 改为 `ZHIHU_COOKIE_FILE` (跟 douyin-search 对齐)
- 落盘路径常量从 `DATA_DIR / "answers"` 改为 `ANSWERS_DIR` (清晰)
- SKILL.md 加入"端到端工作流"示例 + ⚠️ comment_v5 陷阱说明

### Removed
- 无 (完全向后兼容)

### Technical Highlights
- `column-articles` API 端点稳定, 131 篇文章测试通过
- `comments` API 走老 `/comments` 端点绕开 `comment_v5` 的 `data=[]` 反爬
- 全部命令在 60s 内可完成完整工作流
- 零新增依赖 (只用 python3 + curl)

### Engineering Lessons Captured
- 知乎有 2 套评论 API: `comment_v5` (部分账号 `data=[]` 反爬) vs `comments` (稳定返数据)
- `comment_v5` 路径: `/api/v4/comment_v5/answers/<aid>/root_comment` ← 不要用
- 老 `comments` 路径: `/api/v4/answers/<aid>/comments` ← 本 skill 用这个
- author 字段结构: `{"role": "normal", "member": {"name": "..."}}` 不是直接 `name`
- `/api/v4/topics/<t_id>/feeds*` 全部 10003 — 知乎已关话题 API

## [1.0.0] - 2026-06-17

### Added
- Initial release
- 8 个核心命令: `search` / `batch-search` / `quick` / `answers` / `extract` / `qa-batch` / `article` / `hotlist`
- 5 种搜索 type: `question` / `column` / `people` / `topic` / `zvideo`
- `quick` 一键主题摘要 (为 LLM agent 设计)
- 路径硬编码到 `/tmp/zhihu/`

[1.1.0]: https://github.com/excalibursssooo/zhihu-search/releases/tag/v1.1.0
[1.0.0]: https://github.com/excalibursssooo/zhihu-search/releases/tag/v1.0.0
