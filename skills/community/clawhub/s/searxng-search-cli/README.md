# SearXNG Search CLI

自托管 SearXNG 搜索引擎 CLI，聚合 200+ 搜索引擎（Google、Bing、Brave、GitHub 等），免费、可自部署。

## 功能

- 一键安装和部署 SearXNG 实例
- 多搜索引擎聚合查询
- 支持指定引擎、语言、时间范围
- 服务管理（启动、停止、重启、状态）
- 开机自启控制

## 适用场景

- 替代付费搜索 API 进行信息检索
- 为 AI Agent 提供搜索能力
- 自建私有搜索引擎实例

## 使用方式

本 skill 支持 Codex、Claude Code 和 OpenClaw，安装后可通过对话触发：

```
搜索一下 Python 异步编程
帮我查一下 GitHub 上的 xxx 项目
搜一下最近的 AI 新闻
```

首次使用需完成 [references/ONBOARDING.md](references/ONBOARDING.md) 配置。原生 Windows 可连接已有服务；本地部署命令面向 Linux/WSL。

## Codex 安装

```powershell
codex plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace.git
codex plugin add searxng-search-cli@kinema-skills-marketplace
```

安装后新开一个 Codex 对话。

## 命令列表

| 命令 | 说明 |
|------|------|
| `install` | 一键安装 SearXNG |
| `start / stop / restart` | 服务管理 |
| `status` | 查看服务状态 |
| `search <query>` | 搜索 |
| `enable / disable` | 开机自启 |

## 搜索参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--engine` | `-e` | 指定引擎 | `github`, `google` |
| `--lang` | `-l` | 语言 | `zh`, `en` |
| `--page` | `-p` | 分页 | `1`, `2` |
| `--time-range` | `-t` | 时间范围 | `day`, `week`, `month` |
| `--limit` | | 最大结果数 | `10` |

## 项目结构

```
searxng-search-cli/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── skills/searxng-search-cli/SKILL.md
├── SKILL.md
├── scripts/searxng_cli.py
└── references/ONBOARDING.md
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)
