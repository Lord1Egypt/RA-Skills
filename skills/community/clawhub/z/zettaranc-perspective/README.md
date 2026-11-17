# zettaranc-perspective

Z 哥（zettaranc / 万千）思维框架与表达方式的独立 Skill 包。纯文档，不包含数据代码；需要真实行情时，通过外部 `zt` CLI 取数。

> 仓库：https://github.com/lululu811/zettaranc-perspective

## 安装

把本目录链接或复制到宿主的 skills 目录：

```bash
# Claude Code（推荐 symlink，便于跟随本目录更新）
ln -s /path/to/zettaranc-perspective ~/.claude/skills/zettaranc-perspective

# 或直接复制
cp -R /path/to/zettaranc-perspective ~/.claude/skills/
```

宿主加载 `SKILL.md` 即可，`knowledge/` 与 `references/` 按 `SKILL.md` 的资源索引按需读取。

新电脑的完整安装步骤（含 Windows、数据源配置、验收清单、常见问题）见 [INSTALL.md](INSTALL.md)。

## 两种运行状态

| 状态 | 判定 | 能力 |
|---|---|---|
| 数据在线 | `command -v zt` 成功 | 行情、指标、战法、回测、选股 |
| 数据离线 | 无 `zt` | 纯框架问答、历史案例、职业/人生/商业判断 |

数据工具来自另一个项目 `zettaranc-skill`：

```bash
# 安装方式以 zettaranc-skill 仓库 README 为准，例如：
git clone https://github.com/lululu811/zettaranc-skill.git
cd zettaranc-skill
pip install -r requirements.txt && pip install -e .   # 提供 zt / zt-web

zt sync status                                         # 查看本地数据状态
zt analyze 600519.SH --json                            # 一次真实分析
```

Skill 与代码之间的唯一契约是 `zt <cmd> --json`。本目录不 import `modules.*`，也不依赖代码仓库的目录结构。

## 目录

```
SKILL.md                 # 唯一入口：数据契约、路由、资源索引、工具契约、角色协议、工作流
knowledge/               # 32 个知识文件（战法、指标、卖出、仓位、宏观、人生/职业/商业等）
references/research/     # 调研来源（不参与运行时加载）
test-prompts.json        # 验收用例
skill.json               # 发布元数据
LICENSE                  # MIT
```

## 版本

- 独立发行版版本号写在 `SKILL.md` 正文与 `skill.json`，两处必须一致。
- 内容基线：`zettaranc-skill` v4.13.1。代码项目有自己的版本节奏，不再与 Skill 强制同步。

## 边界

本 Skill 是分析框架，不是交易执行系统；所有输出均不构成投资建议。投资有风险，入市需谨慎。

## License

MIT
