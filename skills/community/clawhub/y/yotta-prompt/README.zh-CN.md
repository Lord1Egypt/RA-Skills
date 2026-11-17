<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-prompt banner" width="100%" />
</p>

<h1 align="center">yotta-prompt · 元引 (YuanYin)</h1>

<p align="center">YottaMeta 的 <b>意图澄清 + 生态入口</b> 技能：用户输入一句模糊的话 / 一个词时，识别意图、
给出 <b>2-4 个候选方向</b>、深挖（目标 / 范围 / 输出 / 约束），再串联到对应元阁技能，
输出<b>可直接运行的提示词</b>。</p>
<p align="center">触发场景：用户不知道怎么提问、不知道想要什么、输入模糊的一句话 / 一个词时 —
<b>每次新会话开始自动注入（always-load）</b>，接住「不会用 AI」的用户。</p>
<p align="center">零外部依赖（Python 3.8+ 标准库）；Windows + Linux + macOS；纯本地离线，不联网、不调外部服务。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-prompt"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-prompt" /></a>
  <a href="https://github.com/YottaMeta/yotta-prompt"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

很多人不会跟 AI 说话：打一句模糊的话、一个词，期待被帮助，却说不清自己到底想要什么。
元引是元阁技能家族的<b>门</b>——把「不知道怎么问」变成「能直接跑的任务」。

它走五步流程：**① 识别意图 → ② 给 2-4 个候选方向 → ③ 确认 → ④ 深挖（目标 / 范围 / 输出 / 约束）→
⑤ 串联到对应元阁技能，输出能直接运行的提示词。**

它不是 prompt 美化器。提示词润色是红海；元引只做「把模糊的话补全成可执行任务」这一件事。

## 核心价值

- **意图澄清，不做 prompt 美化**——把模糊词变成可执行任务，第一步绝不替用户下结论。
- **十个意图域**——开发 / 数据 / 计划 / 记忆 / 安全 / 日志 / 学习 / 写作 / 质量 / 通用，中文 + 英文关键词加权（纯本地）。行业无关：写周报、做表格、定计划、写演讲稿、翻译、会议纪要、审合同、头脑风暴、面试准备等都能接。
- **技能名锁定**——输入提到 `yotta-*` 或家族中文名（元忆 / 元安 / …）时，立即锁定到对应方向。
- **生态入口**——每个方向映射到对应元阁技能，带中文名、一句话说明与安装命令。
- **可跑提示词**——每个方向内置一条提示词模板，填上信息即可运行。
- **场景案例库**——18 个完整走查、覆盖任何行业（模糊输入 → 候选 → 深挖 → 串联），见 `references/scenarios.md`。

## 为什么用它

| 优势 | 说明 |
|---|---|
| **常驻注入** | `always-load: true`，会话开始即生效；接住「永远不会主动加载技能」的用户 |
| **零依赖** | Python 3.8+ 标准库；无守护进程 / 数据库 / 联网；Windows + Linux + macOS |
| **一个技能都没装也能用** | 提示词是自包含的行为描述；元阁技能是可选加速器，不是硬依赖 |
| **纯本地离线** | 意图分类与映射全部本地完成，不调外部服务 |
| **边界诚实** | 只澄清意图——不预设立场、不做安全评审；提示词不人为设限（不违规 / 不犯法 / 不越狱） |
| **生态分发** | GitHub + npm + ClawHub 三源同步；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 命令一览

| 命令 | 说明 |
|---|---|
| clarify | 一句话 / 一个词 → 2-4 个候选方向（各带中文说明） |
| clarify --json | 结构化候选，供程序消费 |
| clarify --top N | 控制候选数量（2-4，默认 4） |
| map | 方向 / 技能名 → 元阁技能 + 安装命令 + 可跑提示词 |
| map --json | 结构化映射结果 |
| scenarios | 列出内置场景案例 |
| --version | 显示版本 |

## 使用示例

Windows 用 python，Linux/macOS 用 python3。

```bash
# 意图澄清：一句话 / 一个词 → 2-4 个候选方向
python3 scripts/yotta_prompt.py clarify "帮我写一封邮件"

# JSON 输出（供程序消费）
python3 scripts/yotta_prompt.py clarify "记一下这个" --json

# 控制候选数量
python3 scripts/yotta_prompt.py clarify "怎么学 python" --top 3

# 方向 / 技能名 → 元阁技能 + 安装命令 + 可跑提示词
python3 scripts/yotta_prompt.py map 写作
python3 scripts/yotta_prompt.py map yotta-humanize --json

# 内置场景案例
python3 scripts/yotta_prompt.py scenarios
```

退出码：**0** = 成功；**1** = 未识别（已给引导）；**4** = 用法或读取错误。

示例输出：

```
元引 yotta-prompt v0.2.3 —— 意图澄清
输入：「帮我写一封邮件」

我猜你想做这几件事（回复数字选择，或直接说出你的选择）：

1. 写作与语言（writing）
   · 命中关键词：邮件
   · 可串联：元真 yotta-humanize
2. 通用与入门（general）
   · 还没想清楚，先从通用引导开始
```

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-prompt --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-prompt --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-prompt.git <智能体的技能目录>/yotta-prompt
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-prompt` 点 **Code → Download ZIP**，解压后把 `yotta-prompt` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 开发与校验

技能包自带测试脚本（随发布包一起分发）：

```bash
# 在技能目录内跑全量用例（41 个）
python scripts/test_yotta_prompt.py
```

场景走查见 `references/scenarios.md`。

## 参考文档

- references/faq.md

## 许可证

MIT © YottaMeta —— 见 [LICENSE](./LICENSE)。
