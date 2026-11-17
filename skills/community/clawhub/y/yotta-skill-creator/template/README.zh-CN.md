<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<h1 align="center">{{skill_name}} · {{zh_name}}</h1>

<p align="center">{{summary}}</p>
<p align="center">{{description}}</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/{{skill_name}}"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/{{skill_name}}" /></a>
  <a href="https://github.com/YottaMeta/{{skill_name}}"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/{{skill_name}}" /></a>
  <a href="https://github.com/YottaMeta/{{skill_name}}/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/{{skill_name}}" /></a>
</p>

## 这是什么

填写：描述这个技能做什么、什么时候触发、输出什么。

## 何时使用

- 填写：触发场景一。
- 填写：触发场景二。

**Do NOT trigger**：填写边界。

## 快速使用

```bash
# 填写：替换为本技能真实命令
python3 scripts/{{skill_name}}.py --help
```

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/{{skill_name}} --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/{{skill_name}} --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/{{skill_name}}.git <智能体的技能目录>/{{skill_name}}
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/{{skill_name}}` 点 **Code → Download ZIP**，解压后把
`{{skill_name}}` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。

## 开发与校验

```bash
# 填写：跑本技能自带测试
python scripts/test_{{skill_name}}.py
```

## 许可证

MIT © YottaMeta —— 见 [LICENSE](./LICENSE)。
