# 技能开发教程

这份文档是给**技术人员**看的，目标不是解释概念，而是让你拿到 `skill-template` 后，可以**一步一步开发出一个新的 skill**。

本文默认你开发的是当前最常见的一类业务 skill：

- 有明确的 `scripts/main.py` CLI 入口
- 可能需要读写本地 SQLite（例如任务日志 `task_logs`）
- 可能需要调用兄弟技能或外部 HTTP / RPA
- 业务逻辑主要放在 `scripts/service/`

发布、对账、代发、报表分析等场景都只是业务特例；模板提供通用骨架，复制后按领域补齐实现即可。

## 推荐 AI 开发工具

当前 skill 开发建议尽量配合 AI 编程工具使用。这样做不是为了替代技术人员，而是为了提升以下环节的效率：

- 搭建标准目录结构
- 生成样板代码
- 理解旧项目代码
- 批量补文档、注释和测试
- 辅助排查报错与重构代码

建议团队统一选择 1 到 2 个主力工具长期使用，避免每个人工具链差异太大，导致协作方式不一致。

下面先列国外主流工具，再列国内主流工具。链接优先使用官方站点、官方文档或官方安装入口。

### 国外主流工具

| 工具 | 类型 | 适合场景 | 官方入口 |
|------|------|----------|----------|
| Cursor | 独立 AI IDE | 代码编辑、Agent 开发、整仓理解 | <a href="https://www.cursor.com/" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://www.cursor.com/downloads" target="_blank" rel="noopener noreferrer">下载</a> |
| Windsurf | 独立 AI IDE | Agent 编程、项目生成、连续开发流 | <a href="https://docs.codeium.com/windsurf" target="_blank" rel="noopener noreferrer">文档</a> / <a href="https://windsurf.com/download" target="_blank" rel="noopener noreferrer">下载</a> |
| GitHub Copilot | IDE 插件 / 编程助手 | 日常补全、解释代码、生成函数、配合 VS Code 或 JetBrains 使用 | <a href="https://github.com/copilot" target="_blank" rel="noopener noreferrer">官网</a> |
| Claude Code | 终端 / IDE 编程代理 | 命令行开发、代码库分析、自动改代码、运行命令 | <a href="https://www.anthropic.com/claude-code" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://docs.anthropic.com/en/docs/claude-code/" target="_blank" rel="noopener noreferrer">文档</a> |
| Codex | 终端 / IDE / Web 编程代理 | OpenAI 官方编码代理，适合代码生成、理解、调试、评审 | <a href="https://developers.openai.com/codex/" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://developers.openai.com/codex/quickstart" target="_blank" rel="noopener noreferrer">快速开始</a> |
| Aider | 终端 AI 编程工具 | 已有代码仓库的增量开发、终端协作、快速提交 | <a href="https://www.aider.chat/" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://aider.chat/docs/" target="_blank" rel="noopener noreferrer">文档</a> |
| Cline | VS Code / JetBrains 插件 | 编辑器内 Agent 开发、命令执行、浏览器联动调试 | <a href="https://cline.bot/" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://docs.cline.bot/introduction/welcome" target="_blank" rel="noopener noreferrer">文档</a> / <a href="https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev" target="_blank" rel="noopener noreferrer">VS Code 插件</a> |

### 国内主流工具

| 工具 | 类型 | 适合场景 | 官方入口 |
|------|------|----------|----------|
| Trae | 独立 AI IDE | AI 辅助写代码、项目搭建、对话式开发 | <a href="https://www.trae.ai/home" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://www.trae.ai/download" target="_blank" rel="noopener noreferrer">下载</a> |
| 通义灵码 | 独立 IDE / IDE 插件 | 国内团队日常编码、问答、补全、代码生成 | <a href="https://tongyi.aliyun.com/lingma/?channel=yy_AiBot" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://tongyi.aliyun.com/lingma/download" target="_blank" rel="noopener noreferrer">下载</a> |
| CodeGeeX | IDE 插件 / 开源助手 | 代码补全、生成、注释、跨语言辅助 | <a href="https://github.com/zai-org/CodeGeeX" target="_blank" rel="noopener noreferrer">GitHub</a> / <a href="https://marketplace.visualstudio.com/items?itemName=aminer.codegeex" target="_blank" rel="noopener noreferrer">VS Code 插件</a> |
| 腾讯 CodeBuddy | IDE 插件 | 代码补全、测试生成、智能问答、腾讯云开发体系协作 | <a href="https://www.codebuddy.ai/" target="_blank" rel="noopener noreferrer">官网</a> / <a href="https://www.tencentcloud.com/document/product/1256" target="_blank" rel="noopener noreferrer">文档</a> / <a href="https://marketplace.visualstudio.com/items?itemName=Tencent-Cloud.coding-copilot" target="_blank" rel="noopener noreferrer">VS Code 插件</a> |
| 百度文心快码（Baidu Comate） | IDE 插件 | 国内研发团队辅助编码、解释、测试、优化 | <a href="https://comate.baidu.com/zh" target="_blank" rel="noopener noreferrer">官网</a> |

### 选型建议

如果你们团队主要做这类 Python skill 开发，我建议这样选：

- 想要一体化最强体验：优先试 `Cursor` 或 `Windsurf`
- 想要命令行深度协作：优先试 `Claude Code` 或 `Aider`
- 想继续基于 VS Code 插件体系：优先试 `GitHub Copilot`、`Cline`、`通义灵码`、`CodeBuddy`
- 想优先使用国内生态与中文支持：优先试 `Trae`、`通义灵码`、`CodeGeeX`、`CodeBuddy`、`文心快码`

### 团队落地建议

为了减少培训成本，建议内部至少统一一套主工具方案：

- 国外方案：`Cursor` + `Claude Code`
- 国内方案：`Trae` + `通义灵码`
- VS Code 插件方案：`GitHub Copilot` + `Cline`

不建议每位技术人员完全自由发挥，否则后续在：

- 提示词写法
- 代码修改习惯
- 调试方式
- 提交节奏

这些方面会越来越不统一。

## 1. 先理解模板的定位

`skill-template` 不是业务 skill，它只是一个**新 skill 仓库模板**。

你不应该直接在这个仓库里开发业务，而应该：

0. 按 [`NAMING.md`](NAMING.md) 确定 slug（`{verb}-{noun-phrase}-{platform}`）
1. **优先**用 [`tools/scaffold_skill.ps1`](../tools/scaffold_skill.ps1) 创建新目录（见 [`tools/README.md`](../tools/README.md)）
2. 在新目录内 `git init` 并绑定**本技能**远端（**不得**保留模板 `.git`）
3. 把占位内容替换掉
4. 再开始写业务逻辑

> **Git 红线**：禁止资源管理器整文件夹复制后保留模板 `.git`；`git remote -v` 必须指向新技能仓库，不能仍是 skill-template。

## 2. 新 skill 的标准目录结构

复制模板后，你应该保留下面这套结构：

```text
your-skill/
├─ .github/
├─ assets/
├─ development/
├─ evals/
├─ references/
├─ scripts/
│  ├─ cli/
│  ├─ db/
│  ├─ service/
│  └─ util/
├─ tests/
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ release.ps1
└─ SKILL.md
```

各目录职责如下：

- `assets/`：放示例输出、schema、静态说明资源
- `README.md`：面向用户的市场详情页说明
- `SKILL.md`：面向 LLM / 平台的技能入口
- `references/`：Agent 运行/编排/调用时渐进加载的补充上下文（如 CLI、SCHEMA）
- `development/`：面向开发者与 AI 编程代理的开发资料、需求、测试与技术规范
- `scripts/`：放真正的代码
- `tests/`：放自动化测试
- `evals/`：放人工验收材料、评估清单、示例场景

## 3. `scripts/` 内部如何分层

`scripts/` 不是乱放 Python 文件，而是按职责分层：

```text
scripts/
├─ main.py
├─ cli/
├─ db/
├─ service/
└─ util/
```

每层的职责要明确：

- `main.py`
  作用：唯一 CLI 入口
  只做启动、编码兼容、引入 `cli.app`

- `cli/`
  作用：参数解析、命令分发、用法说明
  不写具体业务逻辑

- `db/`
  作用：SQLite 连接、建表、repository
  不写页面操作和业务编排

- `service/`
  作用：核心业务逻辑
  比如任务编排、调用兄弟技能、外部 API、可选浏览器自动化

- `util/`
  作用：常量、日志、路径、时间工具、通用帮助函数

公共能力（config、logging、runtime_env、rpa、media_assets、video_session、runtime_diagnostics）从共享 runtime 的 `jiangchang-platform-kit>=1.0.17` import，**不得**在 `scripts/` 下保留 `jiangchang_skill_core/` 副本。

## 3.2 开发 RPA 类 skill

若 skill 需要浏览器/桌面/手机自动化，按以下顺序落地：

1. **先读三份标准**：`RPA.md`（三端范式与反反爬）、`CONFIG.md`（`.env` 落盘与读取）、`ADAPTER.md`（四档 adapter）。
2. **从 examples 选择性复制**（不要整包照搬 `examples/<mode>/`，见各 example README 的 copy map）：
   - 若是 **真实浏览器 RPA**（真实网站、登录态、验证码、滚动采集），**必须先读** `examples/real_browser_rpa/README.md`，再按需复制到 `scripts/service/`：
     - `examples/real_browser_rpa/scripts/service/browser_session.py`
     - `examples/real_browser_rpa/scripts/service/human_verification.py`
     - `examples/real_browser_rpa/scripts/service/task_rpa.py`
     - `examples/real_browser_rpa/scripts/service/account_client.py`
   - 若是 **仿真浏览器 RPA**（自有 sandbox、表单批量提交、可控 DOM），**必须先读** `examples/simulator_browser_rpa/README.md`，再按需复制到 `scripts/service/`：
     - `examples/simulator_browser_rpa/scripts/service/browser_session.py`（async）
     - `examples/simulator_browser_rpa/scripts/service/account_client.py`（subprocess，对齐 `real_browser_rpa`）
     - `examples/simulator_browser_rpa/scripts/service/simulator_playwright.py`（RPA 主流程，复制后改名为 `<platform>_playwright.py`）
     - `examples/simulator_browser_rpa/scripts/service/adapter/`（薄 `simulator_rpa` + mock）
     - `examples/simulator_browser_rpa/scripts/service/task_service.py`（async 编排）
     - `sandbox/demo_app.html` 仅留在 examples，不进入生产 skill
   - **禁止**：`rpa_helpers`、sync Playwright 用于完整技能 RPA 主路径、`task_service` 散落 account-manager subprocess
3. **只用共享库，不在 skill 里重写反反爬**：
   ```python
   from jiangchang_skill_core import config
   from jiangchang_skill_core.rpa import launch_persistent_browser, anti_detect, wait_for_captcha_pass
   ```
   上述 import 来自宿主共享 runtime 安装的 `jiangchang-platform-kit`，不是技能目录副本。
4. **mock 档必须离线可跑**（`OPENCLAW_TEST_TARGET=mock`）；sim_rpa / real_* 按需单独测。
5. **桌面/手机**：本期标准见 RPA.md 第 2/3 节，复用 `jiangchang_desktop_sdk` / `screencast`，**不要在新 skill 里重复造包**（尚待实战验证）。

---

### 3.1 `requirements.txt` 依赖规范

技能根目录的 `requirements.txt` 是**标准文件**，用于声明本技能**特有** Python 三方依赖。

- **公共依赖**（`jiangchang-platform-kit`、`playwright`、config、runtime diagnostics、RPA 公共能力等）由**宿主共享 runtime** 提供，**不要**写入技能 `requirements.txt`。
- `SKILL.md` 的 `metadata.openclaw.platform_kit_min_version`（当前 `1.0.17`）是运行契约/兼容性声明，供宿主安装与启用时校验，**不是** pip 依赖声明。
- 匠厂宿主安装/更新技能后，会将技能 `requirements.txt` 安装到共享 venv：`{JIANGCHANG_DATA_ROOT}/python-runtime/.venv`。
- **不要**在业务代码中 `subprocess` / `pip install`；缺依赖由 `health` 报错，由宿主负责安装。
- **版本约束尽量收窄**，降低多技能共享 venv 时的冲突风险。推荐范围写法：
  - `pkg>=1.2.0,<2`
- 对**原生扩展 / 高风险依赖**（如 `chromadb`、`onnxruntime`）建议 pin 或窄范围，避免无上限：
  - 不推荐：`chromadb>=0.5.0`
  - 推荐：`chromadb>=0.5.23,<0.6`
- **不要**把系统组件（VC++ Runtime、浏览器安装包等）写进 `requirements.txt`；这类前置条件写在 `health` / preflight 文档与错误提示中。
- 若技能无额外 Python 依赖，可保留空文件或仅含注释说明；**不要**为 platform-kit 或 playwright 保留占位行。
- 独立本地开发环境若缺少公共包，可手动安装；**生产/宿主运行**由共享 runtime 负责。

### 3.3 公共能力不要复制

以下模块由 platform-kit 提供，技能内**不要**重复实现或 vendored 拷贝：

| 能力 | 导入方式 |
|------|----------|
| config | `from jiangchang_skill_core import config` |
| logging | `from jiangchang_skill_core.unified_logging import ...` 或 `util.logging_config` 薄封装 |
| runtime_env | `from jiangchang_skill_core.runtime_env import ...` 或 `util.runtime_paths` 薄封装 |
| rpa | `from jiangchang_skill_core.rpa import ...` |
| media_assets | `from jiangchang_skill_core.media_assets import ...` |
| video_session | `from jiangchang_skill_core.rpa.video_session import RpaVideoSession` |
| runtime_diagnostics | `from jiangchang_skill_core import collect_runtime_diagnostics, format_runtime_health_lines` |

`health` 应委托 `collect_runtime_diagnostics`，不要在 `scripts/util/` 自建 `runtime_diagnostics.py`。

### 3.4 发布打包约束（PyArmor 与编码）

release workflow 会对 `scripts/` 下的 Python 源码做加密/打包。当前发布链路可能运行在 **PyArmor 免费/试用模式**，因此有两条**发布硬约束**：

**单文件行数（仅 `scripts/**/*.py`）**

- 每个 `scripts/` 下 Python 文件必须 **小于 1000 行**（`>= 1000` 可能在 CI 加密阶段失败）。
- 推荐单文件控制在 **900 行以内**；接近上限时应拆分模块。
- 不要把完整 RPA 主流程、DOM 选择器、数据库、CLI、日志全部堆进一个大文件。
- 正确做法是拆分到 `scripts/cli/`、`scripts/service/`、`scripts/db/`、`scripts/util/`。

`examples/` 里的 Python 示例也建议保持模块化，但**行数限制不作为 examples 的发布硬约束**；不要对 README、HTML、测试数据等文档/资源套用 PyArmor 行数规则。

**文本编码（UTF-8 without BOM）**

- 所有提交到 skill 的源码、文档、配置文本文件必须是 **UTF-8 without BOM**。
- Python 文件**绝对不能**带 UTF-8 BOM；否则 PyArmor/CI 可能报：`invalid non-printable character U+FEFF`。
- Windows 编辑器容易保存成 UTF-8 BOM，提交前须确认文件开头无 `U+FEFF`。
- 不要只写「UTF-8」，必须明确 **UTF-8 without BOM**。

本地可用 `python tests/run_tests.py release_packaging_constraints -v` 自检；默认必跑套件中的 `test_release_packaging_constraints.py` 会守护上述规则。

## 4. 开发一个新 skill 的标准步骤

下面这套顺序建议严格按步骤做，不要一上来就直接写 `service`。

### 第一步：复制模板并改目录名

例如你要开发 `disburse-payroll-icbc` 一类领域 skill（目录名 = slug）：

#### 推荐方式（首选）

在 **skill-template 仓库根目录**执行：

```powershell
.\tools\scaffold_skill.ps1 -Slug disburse-payroll-icbc -Destination D:\OpenClaw\client-gdcm\disburse-payroll-icbc
cd D:\OpenClaw\client-gdcm\disburse-payroll-icbc
git init
git remote add origin <你的新技能 Gitea/Git 仓库 URL>
git remote -v    # 确认 origin 不是 skill-template
```

跨平台可用 `python tools/scaffold_skill.py --slug ... --destination ...`（见 [`tools/README.md`](../tools/README.md)）。

脚手架会排除 `.git`、缓存与 `.env`，并删除 `.openclaw-skill-template` 标记；**不会**自动 `git init`。

#### 禁止方式

| 做法 | 后果 |
|------|------|
| ❌ 资源管理器整文件夹复制后不做 Git 清理 | 隐藏 `.git` 被带走，push 串到 template |
| ❌ 保留模板 `.git` 只改 `remote url` | 历史、分支、对象库仍属 template |
| ❌ 未删 `.git` 就 `git init` | 嵌套/混乱仓库，难以排查 |

#### 若已手工复制（补救）

```powershell
cd <新技能目录>
Remove-Item -Recurse -Force .git
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
Remove-Item -Force .openclaw-skill-template -ErrorAction SilentlyContinue
git init
git remote add origin <新技能仓库 URL>
git remote -v
```

#### AI / 编程代理复制红线

| 禁止 | 说明 |
|------|------|
| 保留模板 `.git` | 必须先 `Remove-Item -Recurse -Force .git` 再 `git init` |
| `origin` 仍指向 skill-template | 复制后必须 `git remote -v` 自检 |
| 保留 `.openclaw-skill-template` | 仅 template 源仓库可有；业务技能不得保留 |
| 复制 `.pytest_cache` / `__pycache__` | 用 scaffold 已排除；手工复制应删 |

目录名要和 skill slug 对齐，后面很多地方都依赖这个命名。

### 第二步：先改 4 个最关键的标识

复制后优先改下面这些地方：

1. `SKILL.md`
2. 根目录 `README.md`（用户市场说明）
3. `scripts/util/constants.py`
4. `references/` 与 `development/` 下的文案
5. `scripts/service/` 下的业务占位实现（优先改 `task_service.py`）

最先要统一的是：

- 技能中文名
- `slug`
- 平台中文名
- 平台内部键
- 日志 logger 名

此外，如果该技能发布后默认不公开（`access_scope = 0`），建议一开始就把 `SKILL.md` 中的 `metadata.openclaw.developer_ids` 配好。这样后续发布到平台时，开发者本人仍能在技能市场中看到并验证该技能。

## 5. 哪些占位内容必须替换

复制后，至少要全局检查并替换下面这些内容：

- `your-skill-slug`
- `your-platform-key`（若 skill 涉及外部平台对接，可能会用到这类占位）
- `技能开发模板（通用业务版）`
- `你的平台名`
- `openclaw.skill.your_skill_slug`

如果你的 skill 对外 CLI 需要自定义文案或别名（例如发布类对外仍叫 `publish`），通常还要替换：

- `run` 命令中的中文提示与别名策略（见 `../references/CLI.md`）
- `../references/CLI.md` 的命令示例
- `../README.md` 的用户话术
- `../references/SCHEMA.md` 的字段映射补充说明

如需浏览器自动化，不要在模板里保留空的 `platform_playwright.py`；请按业务新建 `xxx_playwright.py`（命名自定），并在 `task_service.py` 中按需引用。

## 6. `SKILL.md` 与根 `README.md` 应该怎么写

### `SKILL.md`（LLM / 平台入口）

`SKILL.md` 是给 LLM 与 OpenClaw 平台看的技能入口，**不是**用户市场详情页。

应该重点写：

- YAML frontmatter：`name`、`description`、`version`、`metadata.openclaw`（含 `slug`、`platform_kit_min_version`、`developer_ids` 等）
- 何时触发本技能、CLI 入口摘要、运行契约要点
- 指向 `references/`（Agent 调用）与 `development/`（开发规范）的分工说明

不要在 `SKILL.md` 里写大量用户市场文案或实现细节。

### 根 `README.md`（用户市场说明）

根 `README.md` 是技能市场详情页主来源（`metadata.readme_md`），面向普通用户。

应包含 YAML frontmatter 的 `description`（市场列表简介），正文用用户能理解的语言说明：

- 能做什么、适合什么场景、使用前准备什么
- 如何自然语言告诉 Agent
- 执行结果、注意事项、常见问题

不要在根 `README.md` 里写开发教程、目录规范、release、requirements 等技术细节。

实现细节放在：

- `development/`
- `references/`（CLI / SCHEMA）
- 代码注释与 `service/` 实现

### 关于 `metadata.openclaw.developer_ids`

这是一个平台发布元数据字段，用于解决下面这个问题：

- 技能发布后若平台记录中的 `access_scope = 0`，技能默认不公开
- 如果不额外授权，连开发者自己也可能在技能市场里看不到这个技能

因此可以在 `SKILL.md` 中声明：

```yaml
metadata:
  openclaw:
    slug: your-skill-slug
    category: 通用
    developer_ids:
      - 1032
      - 12428
```

约定如下：

- 只允许填写正整数用户 ID
- 推荐使用数组，即使当前只有 1 个开发者
- 发布时平台会把这些用户自动补写到 `skill_user_access`
- 第一个 ID 会同步到 `skills.developer_id`
- 一期只做“补授权”，不会因为你 later 修改数组而自动撤销旧授权

## 7. 文档目录分工

当前规范 skill 的文档按读者拆分：

**根 `README.md`**

- 用户市场详情页说明（含 frontmatter `description`）

**`SKILL.md`**

- LLM / OpenClaw 平台技能入口

**`references/`**（Agent 运行/编排/调用时渐进加载）

- `README.md` — Agent 参考索引（**不是**市场说明；不得含 YAML frontmatter 或 `description`）
- `CLI.md` — 命令、参数、默认值、兄弟技能调用方式
- `SCHEMA.md` — 数据库路径、核心表结构、日志表结构
- 可按需增加 `ERRORS.md`、`INTEGRATION.md` 等编排向补充

**`development/`**（开发者 / AI 编程代理）

- `REQUIREMENTS.md` — 需求与验收
- `DEVELOPMENT.md` — 开发教程（本文档）
- `TESTING.md` — 测试分层与隔离（详见 [`TESTING.md`](TESTING.md)）
- `ADAPTER.md`、`RPA.md`、`CONFIG.md`、`RUNTIME.md` — 技术规范

## 8. `assets/` 应该放什么

`assets/` 不放业务代码，只放辅助材料。

建议放：

- `examples/`
  比如 `version` 输出示例、`log-get` 输出示例

- `schemas/`
  比如日志记录、机读 JSON 的 schema

不要把正式研发文档放到 `assets/`。
用户说明进根 `README.md`；Agent 编排资料进 `references/`；开发规范进 `development/`。

## 9. `cli` 层怎么写

建议保持一个原则：

- `cli` 只负责解析参数和路由
- `service` 才负责干活

也就是说，`cli/app.py` 的职责是：

1. 打印帮助
2. 定义 `run / logs / log-get / health / version`
3. 把参数转交给 `service.task_service`

不要在 `cli/app.py` 里直接写：

- 浏览器自动化
- 子进程调用兄弟技能
- SQLite 逻辑

## 10. `service` 层怎么写

`service` 是核心层。

通常可以这样拆：

- `task_service.py`
  放命令编排、参数兜底、结果分流（例如 `cmd_run`）

- `sibling_bridge.py`
  放通用兄弟技能子进程工具（`call_sibling_json`）；**具体调用哪个 slug 由业务在 `task_service.py` 决定**，不要在本文件硬编码发布类专用 helper

- `xxx_playwright.py`（按需新建）
  浏览器后台自动化 **不在模板默认结构中**；若确有需要，按命名约定自建模块并在 `task_service.py` 引用

- `entitlement_service.py`
  放鉴权逻辑

### 一个很重要的原则

不要把所有逻辑都堆进一个文件。

推荐流向是：

`cli.app` -> `service.task_service` -> `service.sibling_bridge` / （可选）`service.xxx_playwright` -> `db`

## 11. `db` 层怎么写

如果你的 skill 需要记录日志或本地状态，建议：

- `db/connection.py`
  只做连接和建表

- `db/task_logs_repository.py`
  只做增删查改（模板默认表：`task_logs`）
- `db/display_metadata.py`
  创建 `_jiangchang_tables` / `_jiangchang_columns` 并幂等写入中文展示名（见 `references/SCHEMA.md`）
- `db/timestamp_columns.py`
  标准时间字段 trigger 与维护约定（`created_at` / `updated_at`，Unix 秒级）

不要在 `db` 层里：

- 调浏览器
- 打印用户提示
- 拼接业务流程

## 12. 如何接兄弟技能

如果 skill 要依赖兄弟 skill，不要在业务代码里写死绝对路径。

统一通过：

- `scripts/util/runtime_paths.py`
- `scripts/service/sibling_bridge.py`

来做调用。

调用哪些兄弟技能由具体业务决定；请在 `task_service.py` 中使用 `service.sibling_bridge.call_sibling_json(skill_slug, args)` 或 `get_sibling_main_path(skill_slug)`，不要在本模板仓库的 `sibling_bridge.py` 中堆积特定技能函数。

调用原则：

1. 通过 `get_skills_root()` 找到兄弟技能根目录
2. 再拼出对应 `scripts/main.py`
3. 用子进程调用
4. 机器可读输出优先 JSON

## 13. 如何开发一个新 skill

不管你开发的是发布类、采集类、分析类还是知识库类 skill，建议都先按下面这个顺序推进：

1. 先把目录结构搭完整
2. 先让 `health` / `version` 跑通
3. 再把核心 `service` 骨架跑通
4. 再接兄弟技能桥接、数据库或外部系统
5. 最后再补浏览器自动化、复杂流程编排或高风险集成

不要一开始就直接写页面选择器、复杂接口编排或深层业务逻辑。

推荐先确保这些基础能力正常：

- CLI 入口能跑通
- 基础命令输出稳定
- 关键依赖能取到
- 日志或本地状态能落下来
- 错误返回值格式定好了

如果你的 skill 属于外联型 / RPA 型，可以把上面的“核心 `service`”具体落成 `task_service.py`，再按需接 `sibling_bridge.py`、（可选）`*_playwright.py`。这只是示例路径组合，不代表模板绑定某一业务领域。

## 14. 本地开发的最小验证顺序

建议每次新 skill 开发时按下面顺序验证：

### 1. 验证入口

```bash
python scripts/main.py health
python scripts/main.py version
```

### 2. 验证 CLI 路由

```bash
python scripts/main.py -h
python scripts/main.py <your-command> -h
```

### 3. 验证本地日志与数据库

如果你的 skill 需要本地日志或数据库，再继续：

```bash
python scripts/main.py <your-log-command>
python scripts/main.py <your-detail-command> <id>
```

如果你沿用了模板中的通用任务日志骨架，那么这里可以具体对应成：

```bash
python scripts/main.py logs
python scripts/main.py log-get 1
```

### 4. 最后再验证真实业务

比如：

```bash
python scripts/main.py <your-command>
```

## 14.5 测试驱动的开发顺序

新 skill 不应该等所有业务做完才补测试。建议在每个开发阶段都先把对应测试跑一遍：

1. **目录搭建后**：跑 `python tests/run_tests.py -v`，确认全部默认测试套件通过。
   - 此时 `test_skill_metadata.py` 会校验 `SKILL.md` slug 与 `constants.SKILL_SLUG` 一致；如果你只改了一边，会立刻发现。
2. **改完 constants 后**：再跑一次必跑套件，确认未引入回归。
3. **写完 service 业务后**：从 `tests/samples/test_service_contract.py.sample` 复制一份做契约测试。
4. **接外部系统时**：写在 `tests/integration/`，并配合 `OPENCLAW_TEST_TARGET` 显式开启。

详见 `TESTING.md`。

## 15. 发布到正式环境验证

### release workflow 通道

`.github/workflows/release_skill.yaml` 默认引用：

```yaml
uses: client-jiangchang/jiangchang-platform-kit/.github/workflows/reusable-release-skill.yaml@main
```

约定如下：

- `jiangchang-platform-kit` 的 `main` 分支即稳定通道；kit 的开发、测试、验证须在合并 `main` 前完成。
- skill **不需要**锁定 workflow 版本（不要改为 `@v1`、`@v1.0.x` 等）。
- skill 运行时最低能力要求通过 `SKILL.md` 的 `metadata.openclaw.platform_kit_min_version` 声明。

在执行 `release.ps1` 之前，必须先在本地确认 `python tests/run_tests.py -v` 通过。测试不通过不得发起正式发布。

当本地开发、自测和联调完成后，还需要把 skill 发布到正式环境做一次完整验证。建议技术人员严格按下面顺序执行，不要跳步。

### 第一步：在 skill 根目录执行 `release.ps1`

在当前 skill 仓库根目录执行：

```powershell
.\release.ps1
```

如果你的技能使用了 `metadata.openclaw.developer_ids`，那么这一步触发的发布工作流除了同步 `skills` / `skill_versions` 外，还会在平台侧自动补开发者可见权限。测试非公开技能时，建议重点验证这部分是否生效。

这一步会自动完成标准发布动作，包括：

1. 检查当前仓库状态
2. 自动提交尚未提交的改动
3. 推送最新代码到远程仓库
4. 自动创建新的语义化版本 tag
5. 推送 tag，触发后续 CI 流程

如果你只是想先预览发布动作，可以先执行：

```powershell
.\release.ps1 -DryRun
```

### 第二步：到 Gitea 仓库查看工作流

发布命令执行完成后，远程仓库会自动触发 Gitea 工作流。此时应立即进入对应 skill 的仓库页面，切换到“工作流”页签查看执行状态。

重点确认：

- 是否已经出现最新一次发布记录
- 是否由最新提交触发
- 是否成功执行完 `release_skill.yaml`

下面这张图演示了在仓库页进入“工作流”的位置：

![Gitea 仓库工作流入口](../assets/screenshots/gitea-workflow-tab.png)

下面这张图演示了工作流成功后的状态页面：

![Gitea 工作流成功示例](../assets/screenshots/gitea-workflow-success.png)

### 第三步：确认工作流执行成功

只有当工作流状态为成功，才说明正式发布产物已经正确构建完成。

如果工作流失败，不要继续做平台验证，而应该先回到代码仓库排查，例如：

- 发布脚本是否正常推送
- `SKILL.md`、根 `README.md`、`scripts/`、`references/`、`development/` 是否齐全
- 工作流文件是否存在
- 发布包结构是否符合模板规范

### 第四步：进入匠厂平台下载安装包

当工作流成功后，就可以进入匠厂平台验证最终安装效果。

匠厂产品下载地址：

- [https://jc2009.com/product.html](https://jc2009.com/product.html)

打开页面后，下载并安装匠厂客户端。下面这张图演示了下载入口位置：

![匠厂客户端下载入口](../assets/screenshots/jc2009-download-page.png)

匠厂产品页可从这里进入：[产品下载 - 匠厂](https://jc2009.com/product.html)

### 第五步：安装匠厂后，在技能市场检查最新 skill

安装并启动匠厂后，进入左侧“技能市场”，搜索或查找刚刚发布的 skill，确认以下内容：

- 技能可以被正常检索到
- 技能名称、说明、版本信息正确
- 最新版本已经同步出来
- 可以正常安装或更新

下面这张图演示了在技能市场中查看已发布 skill 的位置：

![技能市场中的已发布技能](../assets/screenshots/market-installed-skill.png)

### 第六步：安装并实际启用该 skill

在技能市场中找到目标 skill 后，执行安装或更新操作，确保客户端本地已经拿到最新版本。

这一步建议至少确认：

- 安装按钮可以正常执行
- 安装后状态正常
- 不会出现缺文件、缺入口或安装失败的问题

### 第七步：在“新建任务”中实际使用该 skill

安装完成后，不要只停留在“已安装”状态，还需要进入“新建任务”页面，真正调用一次该 skill，完成最终验证。

建议至少验证：

- 新任务中可以正常选择或触发该 skill
- skill 能被正确唤起
- 主要命令或主流程可以运行
- 返回结果、日志和行为符合预期

下面这张图演示了安装后在任务界面中实际使用 skill 的场景：

![新建任务中使用技能](../assets/screenshots/new-task-usage.png)

## 16. 发布前检查清单

每个新 skill 发布前，建议技术人员逐条确认：

- [ ] 目录结构符合当前模板
- [ ] slug 符合 [`NAMING.md`](NAMING.md)（verb-noun-platform）
- [ ] 目录名、`SKILL.md` slug、`constants.SKILL_SLUG` 三者一致
- [ ] `SKILL.md` 中 slug、名称、描述都已替换
- [ ] `scripts/util/constants.py` 已修改
- [ ] `../references/CLI.md` 示例命令已改成真实命令
- [ ] `service` 下的核心业务文件（如 `task_service.py`）已按领域改名并实现
- [ ] 没有残留旧平台名
- [ ] `health` / `version` 可运行
- [ ] `.gitignore` 生效，没有把 `__pycache__` 提交进去
- [ ] `release.ps1` 存在
- [ ] `.github/workflows/release_skill.yaml` 存在
- [ ] `python tests/run_tests.py -v` 全部通过
- [ ] `scripts/**/*.py` 单文件 **< 1000 行**（PyArmor 试用/免费模式限制；推荐 < 900 行）
- [ ] 源码/文档/配置为 **UTF-8 without BOM**（Python 文件不得含 `U+FEFF`）
- [ ] 没有新增默认必跑测试访问真实网络或浏览器
- [ ] 如有 integration 测试需求，已写在 `tests/integration/` 下并保持 `.sample` 后缀
- [ ] 本仓库**不是** skill-template 的误复制（根目录**无** `.openclaw-skill-template`）
- [ ] `git remote -v` 指向**本技能**远端，URL 不含 skill-template 仓库名
- [ ] `git log` 首条提交属于本技能（非模板历史）

## 17. 常见错误

### 错误 1：只改了目录名，没改 slug

表现：

- 数据目录不对
- 版本输出不对
- 日志名不对

要检查：

- `SKILL.md`
- `scripts/util/constants.py`

### 错误 2：平台中文名改了，内部键没改

表现：

- 兄弟技能筛选账号失败
- `run` 命令走错平台或 task_type

要检查：

- `task_service.py`
- `sibling_bridge.py`
- `../references/CLI.md`

### 错误 3：把业务逻辑写进 CLI

表现：

- 文件越来越乱
- 不方便测
- 参数和业务耦合太重

要改回：

- `cli` 只做参数解析
- `service` 才做业务

### 错误 4：保留了旧模板结构

表现：

- 仓库同时存在 `docs/`、`optional/`、`skill_main.py`
- 技术人员不知道看哪一套

现在的新模板原则是：

- 不做旧结构兼容
- 用户说明在根 `README.md`，Agent 资料在 `references/`，开发规范在 `development/`
- 统一走 `scripts/main.py` 作为 CLI 入口

### 错误 5：平台放 slug 最前

表现：

- slug 形如 `erp-download-settlement-report`（平台段错误地放在最前）
- 语义校验或 `test_slug_naming` 失败

要改：

- 动词放首段，平台放末段，例如 `download-settlement-report-erp`
- 见 [`NAMING.md`](NAMING.md)

### 错误 6：noun 段过长导致超 48 字符

表现：

- slug 超过 48 字符
- 中间名词段堆砌过多

要改：

- 精简 noun-phrase，保留核心业务含义
- 见 [`NAMING.md`](NAMING.md) §3 硬约束

### 错误 7：只改目录名未改 slug

表现：

- 与「错误 1」相同，但目录已改名而 `SKILL.md` / `constants.py` 仍为占位

要检查：

- `SKILL.md` 的 `metadata.openclaw.slug`
- `scripts/util/constants.py` 的 `SKILL_SLUG`

### 错误 8：复制模板时带走了 `.git`

表现：

- `git remote -v` 仍显示 skill-template 的 origin
- push 到错误仓库，或 log 里全是模板历史
- 新技能目录里仍有 `.openclaw-skill-template`

修复：

```powershell
Remove-Item -Recurse -Force .git
Remove-Item -Force .openclaw-skill-template -ErrorAction SilentlyContinue
git init
git remote add origin <新技能仓库 URL>
```

以后复制请优先用 `tools/scaffold_skill.ps1`（见 [`tools/README.md`](../tools/README.md)）。

## 18. 推荐开发顺序总结

如果让一个新人照着做，我建议他按这个顺序：

1. 按 [`NAMING.md`](NAMING.md) 确定 slug，复制模板并改目录名
2. 改 `SKILL.md` 与根 `README.md`
3. 改 `scripts/util/constants.py`
4. 改 `references/` 与 `development/`
5. 改 `scripts/cli/app.py`
6. 改 `scripts/service/`
7. 跑 `python tests/run_tests.py -v`
8. 跑 `health` / `version`
9. 再做业务联调
10. 最后 release

## 19. 这份模板的底线要求

以后新建 skill，至少要满足这几点：

- 目录结构统一
- 入口统一为 `scripts/main.py`
- 用户说明在根 `README.md`，Agent 资料在 `references/`，开发规范在 `development/`
- 业务核心逻辑统一放 `scripts/service/`
- 不再使用旧模板历史结构

如果做不到这些，后面 skill 一多，就会越来越乱。
