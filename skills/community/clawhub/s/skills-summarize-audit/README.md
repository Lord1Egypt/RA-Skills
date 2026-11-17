# Skills-Summarize-Audit v9.2.2

面向中文用户的技能生态证据审查与优化建议。三项核心能力：技能库翻译精炼、项目画像、技能/插件推荐操作。默认只读，不负责安装、更新、发布、配置、迁移或历史清理。

## 核心能力

| 能力 | 输入 | 输出 |
|---|---|---|
| 技能说明翻译精炼 | 侧栏与命令栏完整可见 ID 集合 | 保留英文名称的中文 `short_description` 候选、质量和来源门禁 |
| 项目画像 | 当前或指定项目目录 | 技术栈、项目类型、扫描覆盖和技能推荐 |
| 技能/插件推荐操作 | 项目画像、真实来源、使用/版本/MCP/Agent/安全证据 | 保留/升级/替换/引入/共存/归档建议与完整执行交接 |

## 触发

- `技能审查`：审查已安装技能/插件问题、版本、画像匹配、评分、冲突/互补，并按请求组合翻译、画像和推荐。
- `技能问题审查` / `插件问题审查`：运行本地只读问题检测，输出证据、严重度和处理方案。
- `技能翻译精炼` 或 `技能审查 精炼`：只生成翻译候选。
- `项目画像`：只生成当前项目的事实画像。
- `技能推荐` 或 `插件推荐`：只输出建议。

支持自然语言请求；旧审查触发词进入第三项内部证据采集。详细规则见 [SKILL.md](SKILL.md)。

## 边界

- 不写入 Codex UI、插件缓存、系统技能、配置或项目文件。
- 不负责安装、更新、卸载、发布、CI/CD、回滚、桌面迁移、环境修复或历史清理；只输出可执行处理建议。
- 报告发现这类后续工作时，只建议用户直接调用对应 Agent，并说明所需输入与确认边界。
- 外部搜索需要用户明确同意；无证据时输出 `unavailable`。

## 验证

```powershell
python tests/validate.py --strict
python -m pytest tests/ -v
```

## 环境依赖

- `scripts/analyze_project_profile.py` 需要 PyYAML：`pip install -r requirements.txt`。缺失时脚本不再直接崩溃，而是以退出码 2 输出 `unavailable` 降级信息，相关测试与 validate 的项目画像门禁自动跳过。
- `scripts/collect_codex_display_candidates.py` 与 `scripts/audit_skill_plugin_issues.py` 仅需标准库 + `tomllib`（要求 Python ≥ 3.11）；PyYAML 对 collect 脚本为可选依赖，缺失时自动降级。

## 脚本参数

扫描脚本默认只读；测试依赖用 `python -m pip install -r requirements-dev.txt` 安装在隔离环境。完整参数用 `--help` 查看。

**`scripts/analyze_project_profile.py`**（项目画像，需 PyYAML）

| 参数 | 说明 |
|---|---|
| `project`（位置参数） | 待扫描项目目录 |
| `--max-files`（默认 2000） | 扫描文件数上限 |
| `--max-depth`（默认 10） | 目录遍历深度上限 |
| `--json` | 输出 JSON 画像 |

**`scripts/collect_codex_display_candidates.py`**（Codex 展示候选采集）

| 参数 | 说明 |
|---|---|
| `--root` / `--catalog-dir` / `--runtime-dir` / `--user-skill-dir` | 各来源目录覆盖（root 默认 `$CODEX_HOME` 或 `~/.codex`） |
| `--scope`（visible/installed/catalog/all） | 采集范围，默认 visible |
| `--visible-id`（可重复） | 当前 UI 可见技能 ID |
| `--expect-visible-count` / `--provided-visible-count` | 可见数量门禁 |
| `--batch-size` / `--offset` | 分批精炼输出（零基偏移） |
| `--require-chinese` / `--require-ready` / `--fail-on-source-conflict` / `--check-unchanged` | 质量与一致性门禁 |
| `--json` | 输出 JSON |

**`scripts/audit_skill_plugin_issues.py`**（技能/插件问题审查）

| 参数 | 说明 |
|---|---|
| `--root` / `--catalog-dir` / `--runtime-dir` / `--staging-dir` / `--user-skill-dir` | 各来源目录覆盖 |
| `--profile` | 用户画像文件；缺失时 profile_alignment=unavailable |
| `--scope`（installed/visible/all/ecosystem） | 审查范围，默认 installed；ecosystem 是推荐内部取证模式 |
| `--signals-path` / `--market-path` | 显式输入使用/市场证据；缺失值不补零、不推荐隐藏卸载 |
| `--scan-mode auto/full/incremental` / `--baseline` | 首次全景、有效基线增量；所有来源重新发现和比对 |
| `--output <new-file>` | 用户明确要求时才导出；不覆盖已有文件，JSON 含 baseline |
| `--visible-id`（可重复） | 用户提供的可见技能 ID |
| `--fail-on`（none/info/warning/critical） | 严重度门禁 |
| `--detail` / `--json` | 逐项明细 / JSON 输出 |

## DeepSeek Harness 插件市场

本仓库同时是 DeepSeek Harness（dsh）技能包插件，可通过 dsh 插件系统安装：

```bash
dsh plugin --profile web add github:gtbwpkwjnb-alt/skills-summarize-audit-skill
```

安装后重启 dsh web，技能出现在 Settings → Plugins，按需懒加载（渐进式披露）。技能包由本仓库根目录的 `SKILL.md` 提供，`cordis.patch.yml` + `index.js` 为插件外壳（只读 skill provider，无工具、无凭据、无网络请求）。

- 测试兼容版本：dsh v0.1.1-rc.2（2026-08-22）。预览期版本迭代快，若 API 变更请以官方文档为准。
- 技能格式：kebab-case 名称 + `name`/`description` frontmatter，与 dsh 技能契约一致。
- 插件外壳无 npm 依赖，可从 GitHub 直装。
