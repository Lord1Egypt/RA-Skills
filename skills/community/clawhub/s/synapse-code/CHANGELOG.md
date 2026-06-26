# CHANGELOG

All notable changes to Synapse Skills will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-04-10

### Added
- **Brain/Hands 架构** — synapse-code 作为 synapse-brain 的 Hand Agent 被调度执行
- **wiki 互操作** — Pipeline 完成后自动触发 synapse-wiki 知识沉淀
- **session 状态追踪** — 任务结果写入 Brain state.json，支持跨会话恢复
- **4 种运行模式** — standalone/lite/full/parallel（OpenClaw 原生子代理）
- **意图路由兼容** — 支持被 task_router.py 识别并路由

### Changed
- **架构升级** — 从外部 pipeline.py 依赖迁移到 OpenClaw 原生多 Agent 调度
- **默认模式** — standalone（独立模式）作为默认，降低新手门槛
- **legacy 兼容** — 保留 `--legacy` flag 兼容旧 pipeline.py 工作流
- **homepage** — 更新为 `https://github.com/ankechenlab-node/synapse-code`

### Why
- 消除新用户配置门槛，无需理解什么是 Pipeline
- 利用 OpenClaw 原生 subagents（max 8）实现灵活调度
- 通过 Brain 持久化状态，实现跨会话任务追踪
- synapse-code + synapse-wiki 互操作，开发过程自动沉淀知识

---

## [1.1.7] - 2026-04-09

### Fixed
- **P0 崩溃修复** — `run_pipeline.py` 4 个致命 bug（Colors 类未定义、log_progress 函数名不匹配、mode 变量未定义、重复 else 块）
- **--help 不工作** — `check_status.py` 和 `auto_log_trigger.py` 改用 argparse，支持标准 --help 参数
- **硬编码路径** — `init_project.py` 支持从 config.json 读取 Pipeline workspace 路径
- **auto_log fallback 路径** — knowledge_dirs 回退从 wiki 改为 .synapse（Synapse 标准目录）
- **无效参数传递** — `run_pipeline.py` 移除 pipeline.py 不支持的 `--mode lite/full` 参数
- **pipeline.py IndentationError** — 修复 line 907 空 try 块导致的 IndentationError

### Why
- 修复前 run_pipeline.py 任何模式都会 NameError 崩溃
- 修复后 5 个脚本可正常运行，5/5 基线测试通过
- 所有脚本支持标准 CLI 帮助和参数

---

## [1.1.6] - 2026-04-09

### Fixed
- **代码审计问题修复** — 修复 5 个 P1/P2 级别问题
- `run_pipeline.py` — 移除重复参数解析，使用 argparse 统一处理
- `query_memory.py` — 优化搜索性能，逐行读取避免大文件一次性加载

### Why
- 提高代码质量和健壮性
- 减少潜在崩溃风险

---

## [1.1.5] - 2026-04-09

### Added
- **program.md 模板** — 定义项目实验目标、约束条件和迭代日志
- **实验评估逻辑** — auto_log_trigger.py 自动评估测试结果（覆盖率、回归测试）
- **配置化阈值** — config.json 支持自定义测试覆盖率阈值

### Changed
- `auto_log_trigger.py` — 新增 `evaluate_experiment()` 和 `update_program_log()` 函数
- 实验评估结果仅供参考，不阻塞主流程（安全设计）

### Why
- 受 karpathy/autoresearch 的 program.md 启发，引入轻量级实验规范
- 帮助用户建立可迭代、可度量、可回溯的实验机制
- 评估逻辑作为"建议系统"，决策权仍归用户

---

## [1.1.4] - 2026-04-08

### Changed
- **IM 平台友好输出** — 移除所有 ANSI 颜色码，适配 Telegram/微信/飞书等 IM 平台
- `run_pipeline.py` — 替换进度条为阶段通知（`log_stage_start`、`log_stage_complete`）
- `auto_log_trigger.py` — 移除 ANSI 颜色码，使用纯文本输出
- `check_status.py` — 移除 ANSI 颜色码，树形结构纯文本
- 新增 IM 友好日志函数：`log_info`、`log_success`、`log_warning`、`log_error`
- 使用 emoji + 纯文本格式：`[INFO]`、`[✓]`、`[⚠]`、`[✗]`、`[⟳]`

### Why
- OpenClaw 的 `chat.send` 流式传输到 IM 平台时 ANSI 码被过滤
- 聊天消息不可变，`\r` 进度条动画无效
- 改为每阶段开始/完成时输出独立消息，用户可感知进度

---

## [1.1.1] - 2026-04-08

### Fixed
- **lint_wiki.py 递归扫描子目录漏检** — 从 `.glob()` 改为 `.rglob()` 递归扫描
- **summaries 目录链接检查** — 使用文件名而非 frontmatter title（匹配 wikilink 格式）
- **Node.js v25 与 tree-sitter 兼容性** — package.json 添加 engines 限制（`node >=18 <25`）

### Changed
- `install.sh` — 添加 Node.js 版本检测和友好错误提示
- 提供 3 种解决方案：降级 Node.js、更新 tree-sitter、跳过 npm

---

## [1.1.0] - 2026-04-08

### Added
- **测试覆盖** — 18/18 测试通过（基线 7/7 + 集成 11/11）
- **文档完善** — 新增 5 篇文档（AGENT_GUIDE、TROUBLESHOOTING、BEST_PRACTICES、TESTING、ITERATION_LOG）
- **配置验证** — 启动时验证 config.json 有效性
- **进度可视化** — Pipeline 运行时显示进度条和阶段状态
- **结构化日志** — 支持 JSON 格式日志输出
- **安装增强** — install.sh 添加前置检查、交互提示、后验证

### Changed
- `run_pipeline.py` — 增强错误处理、6 阶段进度显示、错误阶段解析
- `check_status.py` — 树形结构状态显示、建议操作列表
- `auto_log_trigger.py` — 结构化日志输出

### Fixed
- `lint_wiki.py` — 支持 summaries 目录链接检查

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

#### synapse-code (智能代码开发工作流引擎)
- **核心功能**:
  - `pipeline_init` — 初始化项目的 Synapse + Pipeline 环境
  - `pipeline_run` — 运行 Pipeline 交付代码
  - `synapse_log` — 手动触发 Synapse auto-log
  - `impact_check` — 检查代码变更影响范围（内建 GitNexus）
  - `status_check` — 检查项目状态
- **Scripts**:
  - `init_project.py` — 初始化项目环境
  - `run_pipeline.py` — 运行 Pipeline 并自动触发 auto-log
  - `auto_log.py` — Synapse 自动记录脚本（内置）
  - `auto_log_trigger.py` — 触发 auto-log
  - `check_status.py` — 检查项目状态
  - `infer_task_type.py` — 根据描述推断 task_type
  - `query_memory.py` — 查询记忆记录
- **Commands**: `init.sh`, `run.sh`, `log.sh`, `status.sh`, `query.sh`, `infer.sh`, `parallel.sh`
- **Tests**: 基线测试 3/3 通过

### Changed

- synapse-code 的 `run_pipeline.py` 和 `auto_log_trigger.py` 现在支持配置文件
- 移除了硬编码路径，使用 `config.json` 或 `config.template.json`
- `auto_log.py` 从外部依赖（synapse-core）改为内置脚本
- GitNexus 改为 npm 依赖，安装时自动集成
- SKILL.md 描述优化，突出用户价值而非技术实现

### Removed

- 移除了对 `~/.claude/skills/synapse-core/scripts/auto_log.py` 的硬依赖
- 移除了全局 GitNexus CLI 依赖（改为内建）

### Fixed

- 配置化路径，支持用户自定义 Pipeline workspace 位置
- 增强错误处理和友好错误提示
- 安装脚本支持 --dry-run 和 --uninstall

### Security

- 无

---

## [0.1.0] - 2026-04-08 (Initial Draft)

### Added

- 初始版本创建
- 基线测试框架
