# ZLMediaKit Analyzer Skill

该 OpenClaw Skill 用于自动化跟踪开源流媒体项目 **ZLMediaKit** 的最新进展，并且帮助你进行源码分析。

## 核心功能

1. **自动拉取代码**：自动将 `https://github.com/ZLMediaKit/ZLMediaKit` 克隆或更新到本地工作区 (`D:\.openclaw\workspace\ZLMediaKit`)。
2. **抓取 Issue 和 PR**：调用 GitHub API 获取最近的讨论和更新，生成汇总报告。
3. **源码分析辅助**：准备好本地源码后，通过 OpenClaw 内置的 Search Agent 或 Grep 工具深度分析其 C++11 实现。

## 文件结构

- `SKILL.md`: OpenClaw 识别该 Skill 的元数据和工作流定义。
- `scripts/sync_and_analyze.py`: 一个 Python 辅助脚本，可直接运行来拉取代码并生成包含 Issue/PR 的报告 `zlmediakit_report.md`。
- `.trae/skills/zlmediakit-analyzer/SKILL.md`: 兼容 Trae IDE 格式的 Skill 描述文件。

## 如何使用

### 1. 手动运行脚本测试

如果想立即拉取代码并查看最新的 Issues/PRs，请在终端执行：
```powershell
python D:\.openclaw\workspace\skills\zlmediakit\scripts\sync_and_analyze.py
```
> **注意**：如果不配置 `GITHUB_TOKEN` 环境变量，可能会遇到 GitHub API 请求速率限制。
> 配置方法：
> ```powershell
> [System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_personal_access_token", "User")
> ```

### 2. 通过对话触发 Skill

你可以在对话中直接告诉 OpenClaw：
- "调用 zlmediakit-analyzer 查看最新的 PR"
- "分析 ZLMediaKit 中 TcpServer 的实现源码"
- "帮我运行 ZLMediaKit 的分析脚本并总结报告"

OpenClaw 将根据 `SKILL.md` 中定义的工作流，自动克隆代码、读取报告并回答你的问题。

### 3. 定期运行 (Cron)

如果你希望每天定期拉取，可以使用 Windows 任务计划程序配置每天运行一次上述的 Python 脚本。
