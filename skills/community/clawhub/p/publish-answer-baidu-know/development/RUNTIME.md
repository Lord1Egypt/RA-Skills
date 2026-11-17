# 运行时约定

## 共享 Python Runtime

**skill-template** 及复制出的新技能，公共能力均来自宿主匠厂安装的共享 Python Runtime（`jiangchang-platform-kit>=1.0.17` 及其传递依赖，含 `playwright`）。`jiangchang_skill_core` **不得**在技能仓库内 vendored，应由共享 venv 的 site-packages 提供。

技能根目录 `requirements.txt` **只声明技能特有依赖**；**不要**重复声明 `jiangchang-platform-kit` 或 `playwright`。`SKILL.md` 的 `platform_kit_min_version` 是运行契约，**不是** pip 依赖声明。

| 场景 | 推荐做法 |
|------|----------|
| 日常运行 | 由宿主匠厂触发技能 |
| 手工排查 / 测试机 | 使用共享 runtime 的 `python.exe` 执行 `scripts/main.py` |
| **不推荐** | 在技能目录内 `uv run python …` — 可能创建临时 venv，加载不到宿主共享 runtime |

占位命令（路径因环境而异，勿写死本机目录）：

```text
Windows:
  {JIANGCHANG_DATA_ROOT}\python-runtime\.venv\Scripts\python.exe {baseDir}\scripts\main.py health

通用:
  <shared-python> {baseDir}/scripts/main.py health
```

`<shared-python>` 通常位于 `{JIANGCHANG_DATA_ROOT}/python-runtime/.venv`。数据根由宿主注入；开发模式下也可能通过 `JIANGCHANG_DATA_ROOT` 解析（见 `jiangchang_skill_core.runtime_env`）。

## Runtime 诊断（platform-kit 1.0.17+）

`health` 命令通过 **`jiangchang_skill_core.collect_runtime_diagnostics`** 输出共享 runtime 诊断，**不在技能内重复实现**。典型字段：

- `skill_slug`、`python_executable`、`platform_kit_version`、`platform_kit_min_version`
- `jiangchang_skill_core_file` — 若从技能目录加载会输出 `runtime_issue[warning]`
- `JIANGCHANG_DATA_ROOT` / `resolved_data_root`
- `media_assets_root`、`ffmpeg_path`、`background_music_*`
- `record_video_enabled`、`runtime_issue[warning|error]`

`health` 是**只读诊断**，**不会**触发 media-assets 下载或修复。并补充 `env_path` / `env_exists` / `example_path` 配置路径字段。

## 配置 bootstrap

- 仓库内 `.env.example` 是配置模板（单一事实来源）。
- 用户实际 `.env`：`{JIANGCHANG_DATA_ROOT}/{JIANGCHANG_USER_ID}/{skill_slug}/.env`。
- `scripts/main.py` 与 `cli.app.main()` 启动时调用 `util.config_bootstrap.bootstrap_skill_config()`。
- 配置优先级：**进程环境变量** > **用户 `.env`** > **`.env.example` 默认值**。
- 公共 `config` / `merge_missing_env_keys` 来自共享 runtime 的 `jiangchang-platform-kit>=1.0.17`，**不得** vendored `scripts/jiangchang_skill_core/`。

## media-assets / ffmpeg / 背景音乐

背景音乐、ffmpeg 等共享资源由 platform-kit 统一解析，默认路径：

```text
{JIANGCHANG_DATA_ROOT}/shared/media-assets
```

（由宿主注入 `JIANGCHANG_DATA_ROOT`。）

RPA 录屏成片（`RpaVideoSession`）、ffmpeg 路径、背景音乐探测均由 platform-kit 提供；技能只 import，不重复实现。

## 目录结构

新技能建议采用以下根目录结构：

- `assets/`
- `development/`
- `references/`
- `scripts/`
- `tests/`
- `evals/`

**标准 `scripts/` 分层（不含 `jiangchang_skill_core/` 副本）：**

- `scripts/main.py`：唯一 CLI 入口
- `scripts/cli/`：参数解析与命令分发
- `scripts/db/`：SQLite 或本地持久化层（标准时间字段见 `references/SCHEMA.md`）
- `scripts/service/`：业务用例与外部交互
- `scripts/util/`：通用工具、常量、日志、路径薄封装

## 数据路径

推荐：

```text
{JIANGCHANG_DATA_ROOT}/{JIANGCHANG_USER_ID}/{skill_slug}/
```

数据库文件建议：

```text
{...}/{skill_slug}.db
```

- 业务表使用英文 snake_case；中文表名/字段名写入 `_jiangchang_tables` / `_jiangchang_columns`（见 `references/SCHEMA.md`）。
- 界面字段顺序由 `CREATE TABLE` 列定义顺序决定，**不要**维护 `display_order` 来调整顺序。

## 明确禁止

- **不得** vendored `scripts/jiangchang_skill_core/`
- **不得**在技能内本地重复实现 `RuntimeDiagnostics` / `collect_runtime_diagnostics`
- **不得**写死开发机绝对路径作为运行时约定

## 测试时的运行时隔离

本模板的 `tests/_support.IsolatedDataRoot` 会在测试期间设置：

- `JIANGCHANG_DATA_ROOT` → 临时 tempfile 目录
- `JIANGCHANG_USER_ID` → `_test`

退出时两个变量恢复，临时目录删除。所有 DB / 文件写入都被限制在临时目录内，不污染本机。

详见 `TESTING.md` 第 3 节。

## 编码与输出

- 所有提交到 skill 的源码、文档、配置文本文件必须是 **UTF-8 without BOM**（不要只写「UTF-8」）。
- Python 文件**绝对不能**带 UTF-8 BOM；否则 release CI 的 PyArmor 阶段可能报：`invalid non-printable character U+FEFF`。
- Windows 编辑器容易保存成 UTF-8 BOM；提交前确认文件开头无 `U+FEFF`。
- Windows 终端建议在 `scripts/main.py` 里做 UTF-8 stdout/stderr 包装
- 机读输出优先单行 JSON
- 错误前缀建议统一 `ERROR:`

## 发布打包约束（`scripts/**/*.py`）

release workflow 加密 `scripts/` 源码时，可能运行在 PyArmor 免费/试用模式：

- `scripts/**/*.py` 单文件必须 **< 1000 行**（`>= 1000` 可能在 CI 失败）；推荐 **< 900 行**。
- 接近上限时拆分到 `cli/`、`service/`、`db/`、`util/`，不要把 RPA 主流程、选择器、DB、CLI 堆进单文件。
- 此行数限制**仅适用于** `scripts/**/*.py`；不限制 README 等文档行数，也不把 examples 里的 HTML/README 纳入 PyArmor 行数约束。
