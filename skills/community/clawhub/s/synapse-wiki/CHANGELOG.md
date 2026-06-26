# CHANGELOG

All notable changes to Synapse Skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-04-10

### Added
- **Brain/Hands 架构** — synapse-wiki 作为 synapse-brain 的 Hand Agent 被调度执行
- **code 互操作** — 接收 synapse-code Pipeline 完成后的自动知识沉淀
- **知识沉淀内容** — 技术决策、代码模式、Bug 修复、API 变更
- **意图路由兼容** — 支持被 task_router.py 识别（ingest/query/lint 意图）

### Changed
- **homepage** — 更新为 `https://github.com/ankechenlab-node/synapse-wiki`
- **tags** — 新增 `brain-compatible` 标记

### Why
- 让知识管理成为开发流程的自然延伸，而非独立操作
- 通过 Brain 统一入口，降低用户学习成本
- synapse-code 开发过程自动沉淀知识到 wiki

---

## [1.1.7] - 2026-04-09

### Fixed
- **脚本 --help 支持** — 所有 4 个脚本改用 argparse，支持标准 --help 参数

---

## [1.1.6] - 2026-04-09

### Fixed
- **代码审计问题修复** — 修复 3 个 P1/P2 级别问题
- `ingest.py` — 修复 YAML sources 格式错误（从字符串改为列表格式）
- `ingest.py` — 添加路径穿越保护（检查 source 是否在 wiki root 内）
- `query.py` — 修复 `or not pages` 逻辑反转问题
- `baseline_test.py` — 修复 lint 测试过于宽松的问题

### Why
- 提高代码质量和健壮性
- 减少潜在崩溃风险

---

## [1.1.5] - 2026-04-09

### Changed
- **版本号同步** — 与 synapse-code 保持版本对齐（无实际代码变更）

---

## [1.1.4] - 2026-04-08

### Changed
- **CHANGELOG 对齐** — 补充 v1.1.x 版本历史记录，与 synapse-code 一致

---

## [1.1.3] - 2026-04-08

### Changed
- **SKILL.md 用户体验改进** — 添加决策树和命令速查卡片
- 添加 `user-invocable: true` 支持 slash command 直接触发
- 决策树：快速选择命令（init/ingest/query/lint）
- 命令速查：4 个核心命令 + 使用示例

---

## [1.1.2] - 2026-04-08

### Changed
- 同步变更：删除 `.skillhub.json`，与 GitHub 仓库一致

---

## [1.1.1] - 2026-04-08

### Fixed
- **lint_wiki.py 递归扫描子目录漏检** — 从 `.glob()` 改为 `.rglob()` 递归扫描
- **summaries 目录链接检查** — 使用文件名而非 frontmatter title（匹配 wikilink 格式）

---

## [1.1.0] - 2026-04-08

### Added
- **测试覆盖** — 9/9 测试通过（基线 4/4 + 集成 5/5）
- **文档完善** — 新增 5 篇文档（AGENT_GUIDE、TROUBLESHOOTING、BEST_PRACTICES、TESTING、ITERATION_LOG）

### Changed
- `install.sh` — 添加前置检查、交互提示

---

## [1.0.0] - 2026-04-08

### Added

#### synapse-wiki (智能知识库管理系统)
- **核心功能**:
  - `wiki_init` — 初始化新的 Wiki 知识库
  - `wiki_ingest` — 摄取源文件创建 Wiki 页面
  - `wiki_query` — 查询知识并综合答案
  - `wiki_lint` — 健康检查（死链接、孤立页面等）
- **Scripts**:
  - `scaffold.py` — 引导新的 Wiki 目录树
  - `ingest.py` — 摄取新资料，编译为 Wiki 页面
  - `query.py` — 查询 Wiki，综合答案
  - `lint_wiki.py` — 健康检查（死链接/孤立页/矛盾）
- **Commands**: `init.sh`, `ingest.sh`, `query.sh`, `lint.sh`
- **Tests**: 基线测试 4/4 通过

### Changed

- SKILL.md 描述优化，突出"越用越聪明"的核心价值
- 移除技术术语（LLM Wiki、RAG 对比），改用用户友好语言
- 安装脚本支持 --dry-run 和 --uninstall

### Fixed

- 目录结构统一，所有元数据文件位于根目录
- 配置文件支持 config.template.json → config.json 自动创建

### Security

- 无

---

## [0.1.0] - 2026-04-08 (Initial Draft)

### Added

- 初始版本创建
- 基线测试框架
