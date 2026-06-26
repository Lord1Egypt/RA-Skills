# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

本仓库是 **Zopia AI 视频创作 Skill 包**，被 Claude Code / Gemini CLI / Codex / Cursor 等 Agent 通过 `npx skills add` 或 `npx clawhub install` 安装后调用。它本身不是后端服务，而是一组 Python 脚本 + 一份 `SKILL.md` 行为指引，封装对 Zopia 平台 HTTP API 的调用。

后端实现在姐妹仓库 `C:\code\jobCode\zipia\jaaz-cloud`（同 host 下的 `https://zopia.ai`），本仓库的脚本通过 HTTP 调用其接口。修改本项目时，若涉及接口字段、新模型 ID、新风格枚举等，对应能力须在 `jaaz-cloud` 已上线，否则脚本调用会报 400/404。

## 核心架构

```
SKILL.md            ← 行为契约：Agent 什么时候触发、如何组合脚本、典型场景、错误处理
README.md           ← 用户向：安装/配置/枚举值速查
scripts/_common.py  ← 唯一的共享层：urllib HTTP + Bearer 鉴权 + 业务级封装函数
scripts/*.py        ← 一脚本一动作，全是 argparse + _common 函数 + print_json 的薄壳
docs/               ← 维护者文档（如 publish-to-clawhub.md）
```

**只允许 Python 标准库**。`_common.py` 用 `urllib.request` 实现 HTTP，是有意为之——Skill 安装到用户机器后不能要求 `pip install`。新增脚本必须沿用这个约定，**不要引入 requests / httpx / pydantic 等第三方包**。

每个脚本的写法是固定的薄壳模式：

1. `sys.path.insert(0, os.path.dirname(__file__))` 后从 `_common` 导入
2. `argparse` 解析参数
3. 调用 `_common` 里的业务函数
4. `print_json(result)` 输出，由调用方（Agent）解析

新增 API 调用时，**先在 `_common.py` 加业务级封装函数**（参考 `create_project` / `send_message`），再写脚本壳。不要让脚本自己拼 URL 和 header。

## SKILL.md 是行为源

`SKILL.md` 是 Agent 的运行手册——它规定了 Agent 应该如何串联这些脚本（场景 1–5）、如何读 workspace 进度、什么时候该展示项目链接、不要替用户扩写需求等。**修改脚本参数或新增脚本时，必须同步更新 `SKILL.md` 的脚本速查表与场景示例**，否则 Agent 行为会与实际能力脱节。`README.md` 的枚举值表（风格、模型）也要同步。

## 常用命令

仓库无 lint、无测试、无构建。日常只有这些：

```bash
# 配置环境变量（脚本运行前提）
export ZOPIA_ACCESS_KEY="zopia-xxxxxxxxxxxx"
export ZOPIA_BASE_URL="https://zopia.ai"   # 可选，默认即此

# 直接跑脚本调试
python3 scripts/get_balance.py
python3 scripts/create_project.py "测试项目"
python3 scripts/query_session.py SESSION_ID --poll
```

调试本地 `jaaz-cloud` 时，把 `ZOPIA_BASE_URL` 改到本地端口（如 `http://localhost:3000`）即可。

## 发布流程

发布到 ClawHub 技能市场，详细步骤见 `docs/publish-to-clawhub.md`：

```bash
git push                              # 先推 GitHub
npx clawhub publish . --slug zopia-skill --version x.y.z --changelog "..."
npx clawhub inspect zopia-skill       # 验证 Latest 字段
```

版本号 semver：新增模型/功能 → minor +1；修 bug / 文档更新 → patch +1。

## 项目约定

- **Git commit message 用中文**，控制在 20 字以内（参考最近提交：`feat: 新增 Seedance 2.0 Fast 和 PixVerse C1 模型`）
- **不要 `git commit`**，除非用户明确要求
- 重构时不考虑兼容性，直接删除旧逻辑（除非用户明确要求保留）
- npm/npx 命令在 Windows 下用 cmd 执行
