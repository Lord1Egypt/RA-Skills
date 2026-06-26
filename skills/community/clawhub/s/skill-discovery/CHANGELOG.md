# Changelog

本项目的所有重要变更都会记录在此文件中。

## [2.2.1] - 2026-03-31

### 增强

- SKILL.md 声明 `install.type: bundled` + `entrypoint: index.js`，消除 OpenClaw "No install spec declared" 提示
- SKILL.md 补充 `sanitize()` 脱敏策略文档（遮蔽字段名/值模式、日志路径），消除 OpenClaw 截断审查提示

## [2.2.0] - 2026-03-31

### 安全增强（解决 OpenClaw Suspicious 标记）

- **默认推荐模式**: `autoDiscover()` 默认 `dryRun: true`，不再自动安装，仅返回推荐结果
- **OpenClaw hook 推荐模式**: `onUserInput()` 使用 `dryRun: true`，返回推荐信息和安装命令供用户确认
- **安装需显式确认**: `skillsAdd()` 默认 `global: false, yes: false`，调用方需显式传入才会执行全局/非交互安装
- **SKILL.md 更新**: 描述从"自动安装"改为"推荐并由用户确认安装"，新增安全说明块

## [2.1.2] - 2026-03-31

### 增强

- ClawHub 搜索自动过滤被安全标记（flagged/suspicious）的 skill（`nonSuspiciousOnly=true`）

## [2.1.1] - 2026-03-31

### 修复

- 新增 `.clawhubignore` 排除 `package-lock.json` 等非必要文件，消除 ClawHub 安全扫描的 `install_untrusted_source` 标记
- SKILL.md 声明 `requires.bins` (`npx`) 和 `anyBins` (`clawhub`)，消除 LLM 扫描的元数据不一致警告

## [2.1.0] - 2026-03-31

### 新增

- **ClawHub 搜索源**: 新增 ClawHub (`clawhub.ai`) 作为 skill 搜索源，与 skills.sh 并行搜索
- `clawhubSearch()`: 通过 ClawHub 公共 API (`/api/v1/search`) 进行向量语义搜索
- `clawhubAdd()`: 支持通过 `clawhub install` 安装 ClawHub 来源的 skill
- `deduplicateResults()`: 合并去重两个源的搜索结果，skills.sh 优先
- `skillsFind()` 现使用 `Promise.allSettled` 并行搜索两个源，ClawHub 故障不影响 skills.sh 结果
- `CLAWHUB_CONFIG`: 集中管理 ClawHub API 配置（基址、端点、超时、数量限制）
- `openclaw` 加入 `trustedOwners` 可信来源列表
- `resolveInstall()` 根据 skill 来源自动选择安装命令（`npx skills add` 或 `clawhub install`）

## [2.0.0] - 2026-03-31

基于 GPT、Opus、GLM、Kimi、MiniMax、Qwen 六份独立评审结果的全面重构。

### 重构

- **常量统一**: 新建 `constants.js`，消除 MAGIC/CONFIG 跨文件重复定义
- **错误码标准化**: 新增 `ERROR_CODES` 枚举（11 种错误类型），所有返回结构统一为 `{ success, stage, outcome, errorCode, skill, candidates, message }`
- **sanitize() 修正**: 重命名 `SANITIZE_SAFE_FIELDS` → `SANITIZE_REDACT_KEY_PATTERNS`，业务字段（installs/confidence/domain）不再被误脱敏
- **autoDiscover 拆分**: 从单一大函数拆为 `searchSkills()` → `filterAndSelect()` → `resolveInstall()` 管道
- **导出清理**: 收紧公共 API，内部工具函数不再暴露

### 增强

- **parseFindOutput() 强化**: JSON 优先解析 + 文本降级，双正则模式（支持 emoji 前缀），新增 M 后缀支持
- **CLI 正式化**: 支持 `--dry-run`、`--json`、`--verbose`、`--help` 参数
- **ESLint + Prettier**: 配置代码检查和格式化（ESLint v10 flat config）

### 测试

- 测试用例从 21 个增加到 **80 个**
- 新增 `openclaw-hook.test.js`（onUserInput、generatePrompt、safeRemove、cleanTrash）
- 补充 shellEscape、withRetry、extractJson、validateParams、buildLogEntry、sanitize 测试

### 文档

- README 和 SKILL.md 全部中文化
- README 视角从"开发者"调整为"OpenClaw 用户"
- 删除未实现功能的描述（config.js、pre-audit、ratings），移至"规划中"章节
- 修正 cleanTrash 注释（"30 分钟" → "1 小时"）

### 修复

- `sanitize()` 不再遮蔽业务字段，日志恢复排查价值
- OAUTH 正则从宽泛的 `===+.*===+` 改为精确的 `===+\s*[A-Za-z]+\s*===+`

## [1.0.0] - 2026-03-30

### 新增

- 首次发布
- 基于用户意图的自动 skill 发现
- 中英文双语输入支持
- 质量验证（安装量、可信来源）
- 自动安装 + 白名单机制
- 安全特性：Shell 转义、日志脱敏、卸载备份
- OpenClaw 集成钩子
- CLI 和编程 API
- 单元测试和集成测试（21 个用例）
