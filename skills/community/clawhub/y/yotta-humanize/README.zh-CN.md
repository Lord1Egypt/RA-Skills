<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>


<p align="center">
  <img src="assets/banner.png" alt="yotta-humanize banner" width="100%" />
</p>

<h1 align="center">yotta-humanize · 元真</h1>

<p align="center"><b>粘贴一段中文草稿，先看 AI 味评分，再改掉像机器写的句子。</b></p>
<p align="center">元真用 <b>24 类规则 + 统计突发性</b>检查空泛升华、套话、AI 黑话、同义堆叠、机械排比、聊天残渣和标点滥用。</p>
<p align="center">Python 3.8+ 标准库本地运行，不调用模型、不上传文本、不依赖外部服务。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-humanize"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-humanize" /></a>
  <a href="https://github.com/YottaMeta/yotta-humanize"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-humanize" /></a>
  <a href="https://github.com/YottaMeta/yotta-humanize/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-humanize" /></a>
  <a href="https://github.com/YottaMeta/yotta-humanize"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 两条真实案例

> 以下均为 0.2.4 `rewrite` 的实际输出；分数是引擎的 0-100 AI 味评分。

**1. 替换 AI 黑话**

改写前：

```text
赋能业务增长，打造闭环生态，提升用户体验，实现价值最大化。
```

改写后：

```text
支持业务增长，打造流程生态，提升用户体验，实现价值最大化。
```

`46 -> 0`；修正：赋能 -> 支持，闭环 -> 流程。

**2. 清理套话与聊天残渣**

改写前：

```text
感谢你的提问。赋能业务增长，打造闭环生态，沉淀方法论，提升颗粒度。如果你有任何问题，随时告诉我。
```

改写后：

```text
支持业务增长，打造流程生态，积累方法，提升细致程度。
```

`52 -> 0`；共修正 8 处：AI 黑话 ×5、奉承 ×1、聊天残渣 ×2。

## 这是什么

AI 生成的中文文本有一眼可辨的「AI 腔」：空泛升华（标志着 / 彰显了）、套话（众所周知 / 综上所述 / 未来可期）、黑话（赋能 / 闭环 / 抓手 / 颗粒度）、机械列举（首先 / 其次 / 再次）、聊天残渣（希望对你有所帮助）……元真把这些特征做成**确定性检测器引擎**：24 类规则（词表 + 句式正则）+ 中文统计突发性（句长均匀度 / 词汇多样性），输出 0-100 的 AI 腔评分，并给出**确定性改写**（词表替换、套话删除、聊天残渣清理、标点限流）。

它不是某个平台的专属功能，而是一份与智能体无关的工具包：装进任何支持 Agent Skills 的智能体即可按需调用。全程零依赖、不调模型；需要判断的改写以建议形式给出，不强行自动改。

## 核心价值

- **24 类检测规则**：内容（空泛升华 / 套话开头结尾 / 模糊归因 / 绝对化）/ 语言（AI 黑话 / 同义堆叠 / 名词化堆砌 / 「我们」滥用）/ 句式（排比三连 / 机械列举 / 反问堆叠 / 标点滥用）/ 沟通（聊天残渣 / 奉承讨好 / 免责回避）/ 废话（填充 / 转折 / 重复声明）。
- **统计突发性**：句长均匀度（CV）、突发性、双字词汇多样性（TTR）、逗号密度——补规则检测不到的节奏问题。
- **确定性改写**：无歧义机械变换直接改（赋能→支持、抓手→切入点、众所周知 / 综上所述 删除、希望对你有所帮助 清理、破折号 / 感叹号限流），输出修复清单与前后评分。
- **机器可读**：--json 输出纯净 JSON；score --gate 接入 CI / 发布前检查。
- **中文优先**：词表、句式、改写映射全部针对中文语料自研整理，与英文 humanizer 类技能无共享代码。

## 核心优势

| 优势 | 说明 |
|---|---|
| **零依赖** | Python 3.8+ 标准库，无模型、无数据库、无外部服务；Windows + Linux + macOS 通用 |
| **确定性** | 规则判定可复现、可解释；改写是确定性变换，不依赖模型概率 |
| **中文优先** | 针对中文 AI 腔（黑话 / 套话 / 排比 / 聊天残渣）自研词表与句式，非英文规则直译 |
| **检测 + 改写一体** | score / analyze / report / suggest / rewrite 全流程，一条命令从检测到改写 |
| **可复核** | 改写输出修复清单与前后评分，人工可逐条核对 |
| **生态分发** | GitHub + npm + ClawHub 三源同步发布；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 功能体系

| 能力 | 说明 |
|---|---|
| score | 输出 AI 腔评分（0-100），--gate 可做 CI 拦截（退出码 1） |
| analyze | 详细检测报告（文本 / --json），含命中规则、上下文片段、建议 |
| report | Markdown 检测报告（统计表 + 命中规则） |
| suggest | 按优先级分组的改写建议 |
| rewrite | 确定性改写：替换 / 删除 AI 腔，输出修复清单 + 改写后文本 + 前后评分 |
| version | 打印版本 |

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 评分（0-100，越高越像 AI 写的）
python3 scripts/yotta_humanize.py score -f article.md

# 详细检测报告
python3 scripts/yotta_humanize.py analyze -f article.md

# Markdown 报告
python3 scripts/yotta_humanize.py report -f article.md > report.md

# 按优先级分组的改写建议
python3 scripts/yotta_humanize.py suggest -f article.md

# 确定性改写（输出改写后文本 + 修复清单）
python3 scripts/yotta_humanize.py rewrite -f article.md

# 管道输入
cat article.md | python3 scripts/yotta_humanize.py score --stdin

# CI 拦截：评分 >= 阈值时退出码 1
python3 scripts/yotta_humanize.py score -f article.md --gate --threshold 45
```

退出码语义（与元安 / 元审 / 元盾家族一致）：0 = 成功；1 = score --gate 且评分达到阈值；4 = 用法错误 / 致命异常。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-humanize --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-humanize --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-humanize.git <智能体的技能目录>/yotta-humanize
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-humanize` 点 **Code → Download ZIP**，解压后把 `yotta-humanize` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 使用示例（AI 智能体）

1. 将本仓库的 SKILL.md 接入任意 AI 智能体的技能/规则系统（见上方安装）。
2. 收到一段 AI 味很重的文稿时，先跑一次检测：
   ```bash
   python3 scripts/yotta_humanize.py analyze -f draft.md
   ```
   看评分与命中规则（空泛升华 / 黑话 / 套话 / 聊天残渣等）。
3. 无歧义的部分直接机械改写：
   ```bash
   python3 scripts/yotta_humanize.py rewrite -f draft.md
   ```
   对照修复清单确认，把改写后文本落回稿件。
4. 需要判断的部分（排比拆句、模糊归因补来源、绝对化软化）按 suggest 的建议手工润色。
5. 改写完再 score 一次，确认评分下降、原意未破坏。

## 改写输出

`rewrite` 会返回改写后文本、带规则编号的修复清单，以及改写前后评分。`--json` 返回 `{ text, fixes, before, after }`。上方案例都是当前引擎的确定性输出；需要判断的润色只给建议，不会自动强改。

## 错误处理

- 退出码：**0** = 成功；**1** = `--gate` 命中（CI 拦截）；**4** = 输入错误（文件不存在、无输入等）。
- 文件不存在 / 不是 UTF-8 编码 / 无读取权限时，会给出**中文修复建议**，不再抛一堆英文堆栈。
- 常见问题与避坑详见 [references/faq.md](references/faq.md)。

## 常见问题 FAQ（速查）

| 问题 | 答案（详见 references/faq.md） |
|---|---|
| 怎么传文本？ | `-f 文件` / `--stdin` / 直接传文本参数 |
| 文件不是 UTF-8？ | 另存为 UTF-8 再试（记事本 → 另存为 → UTF-8） |
| 长文怎么处理？ | 分段处理；复杂嵌套可能需人工复核 |
| 改写后变化不大？ | 原文 AI 味低；用 analyze 看命中规则，suggest 取润色建议 |
| rewrite vs suggest？ | rewrite 机械改写全文；suggest 给人工润色建议 |
| CI 拦截？ | `--gate --threshold 40`，命中退出码 1 |
| 会不会改坏原文？ | 只做确定性替换 + 修复清单 + before/after 评分，可核对 |

## 开发与校验

- 测试：python scripts/test_yotta_humanize.py（158 项）
- 基础校验：python tools/validate-skill.py yotta-humanize（在仓库根目录运行）
- 规则目录：references/patterns.md；评分公式：references/scoring.md；改写规则：references/rewriting.md

## 许可证

MIT © YottaMeta —— 详见 [LICENSE](./LICENSE)。
