# 夸克网盘懒人追剧、追番 SKILL

基于 QAS（夸克网盘自动转存项目）的懒人追剧、追番 SKILL，也内置了一个 CLI 工具。即使 QAS 的剧集订阅失效，它也可以重新搜索资源、探查多级资源目录，并在多个最新候选资源中按用户偏好（如更高清晰度）转存新剧集和缺失剧集，并修复订阅链接。

可以交给本地 OpenClaw、Hermes Agent 或其他 Agent 使用，用来设置定时任务、定时汇报，并在订阅失败时辅助修复。
有 Python 运行环境的进阶用户，也可以把它当作命令行工具使用。

本项目不是对QAS Web UI的替代，而聚焦订阅剧集的”偷懒的更新“。

## 核心需求：

- QAS 的订阅时常会失效<br>
  手工查询、维护订阅任务很麻烦。等忙完想起来再去找新资源时，资源可能已经失效了。

- Infuse、Emby 的海报墙被重复剧集搞乱<br>
  分享资源内容可能重复，例如：凡人修仙传.S05E01.4K.mkv、凡人修仙传.S05E01.dv.mkv。用正则模板转存时，可能会把两个文件都转存下来，造成剧集文件混乱，让 Infuse、Emby 等媒体库的海报墙乱掉，需要手动删除、改名和维护。

- 喜欢最高视频编码的资源<br>
  如果偏好最高视频编码的资源，或希望选择较小体积的视频，通常需要手动下探搜索结果目录、挑选和比对。

- Agent 来了，自己更懒了<br>
  让 Agent 忙起来，自己安心当懒人。

## 项目甜点：

- 再也不操心订阅失效<br>

- 节省 Token。命名规范、发布清晰的分享资源，可以交给 `code` 顾问执行；复杂资源情况则交给 Agent 或 LLM 大模型判断和决策<br>

- Agent 可以使用 SKILL 分析资源的发布规律，并配置合理的订阅更新时间<br>

- 多资源匹配用户需求、精准指定目标文件名做转存，有效规避资源目录多个相同剧集都下载搞了视频目录、资源发布时间和剧集顺序不相符情况 会看过的剧集<br>

## 四种更新运行模式

`LAZY_CLI_ADVISOR` 是网盘资源搜索后的决策机制，用来决定候选资源怎么选，不是聊天模式。

- `code`：用代码规则自动决策。适合后台任务、资源发布规范的剧集、资源目录有“更新至n集”；速度快，无需交互，不消耗 LLM Token。<br>
- `llm`：后台任务中引入大模型做资源选择。适合多版本编号冲突等复杂资源；可配合 `--add-prompt` 改AI大模型定制判断规则。例如：让大模型帮你判断是动漫还是真人版的剧集、你订阅任务是剧集的中文名称，告诉大模型剧集的英文名称等。<br>
- `agent`：由当前 Agent 在和用户交互过程中判断候选资源。适合复杂场景的临时更新，或者在Openclaw Heateat机制里，维护和修复复杂订阅更新的场景使用。记得让Agent更新时，要求看订阅剧集.md文档中，你对剧集转存的要求。<br>
- `human`：用户人工选择。适合用户想亲自确认资源的场景。<br>

详细用法读取：`references/顾问模式.md`。
---

## 使用概览

### 1. 手动追剧更新

```bash
# 追新：只转存高于当前最高集的新资源
qslazy update new 凡人修仙传

# 全量：补漏 + 追新
qslazy update all 凡人修仙传
```

### 2. 查看订阅状态

```bash
qslazy task list
qslazy task status 凡人修仙传
```

`task status` 会展示本地网盘状态、缺集情况、搜索到的资源发布时间，适合用来判断订阅是否正常，也可以帮助 Agent 推算最佳订阅更新时间。

### 3. Agent / OpenClaw / Hermes 用法

本项目提供 [SKILL.md](./SKILL.md)，包含更详细的 Agent 操作说明：

- 如何查看订阅任务和单个剧集状态
- 如何根据资源发布时间制定最佳订阅更新时间
- `LAZY_CLI_ADVISOR=agent` 的决策文件工作流
- Hermes Agent / OpenClaw 的后台执行与轮询方式
- `--add-prompt` 的复杂资源筛选用法

详细 Agent 用法请阅读 [SKILL.md](./SKILL.md)。

---

## 2. 安装和环境配置

安装分两步：**Skill 文档**（告诉 Agent 怎么用）和 **qslazy CLI**（真正干活的命令）。两个都要装。

### 第一步：安装 Skill 文档

skills.sh / 通用 Agent：

```bash
npx skills add jesustoachild/quark-lazy-cli
```

OpenClaw / ClawHub：

```bash
openclaw skills install quark-lazy-cli
```

> Skill 安装只安装 SKILL.md、示例配置和辅助资源，不安装 Python 包。

### 第二步：安装 qslazy CLI（必须）

**pipx 安装（推荐）**：适用 Linux 服务器 / 已具备 Python 3.10+ 和 pipx 的用户。

```bash
pipx install git+https://github.com/jesustoachild/quark-lazy-cli.git
```

**源码安装**：

```bash
git clone https://github.com/jesustoachild/quark-lazy-cli.git
cd quark-lazy-cli
pip install -e .
```

## 快速开始
- 让你的 OpenClaw Agent 完成配置<br>
- 或者，有 Python 运行环境的进阶用户可以手动配置和使用

### 1. 配置环境

```bash
cd /<skill>/quark-lazy-cli
cp .env.local.example .env
```

如果安装后的目录没有 `.env.local.example`，请读取 `references/环境变量.md`，根据里面的完整模板手动创建并编辑 `.env`。

详细使用方式请阅读 `SKILL.md`。


### 2. 查看订阅

```bash
qslazy task list
```

### 3. 查看订阅任务状态

```bash
qslazy task status 凡人修仙传
```
---

### 4. 追更新集

```bash
qslazy update new 凡人修仙传
```

### 5. 补全缺集 + 追新

```bash
qslazy update all 凡人修仙传
```


## 许可证

MIT
