# Skill 外部来源与检索（skill sources）

> 本文只解决两个问题：**优秀的 skill 去哪找**、**找到了怎么装进 WorkBuddy**。
> 分类口径见 [skill-taxonomy.md](skill-taxonomy.md)；安装动作属外部写入，**必须先经教授确认**。

## 一、来源优先级（优秀 skill 优先）

| 优先级 | 来源 | 定位 | 检索方式 |
|:---:|------|------|----------|
| **1** | **阿里 SkillsHub**<br>[skills.alibaba.org.cn](https://skills.alibaba.org.cn/) | **优秀 skill 的优先搜索来源**。107 个精选 Agent Skills（源自 anthropics / vercel-labs / obra / mattpocock / supabase 等官方仓库），带中文分类与描述、安装量与星数，数据可在 skills.sh 核验 | `python scripts/skillhub_alibaba.py search "<关键词>"` |
| 2 | SkillHub<br>[skillhub.cn](https://skillhub.cn/) | 国内通用托管源，自建/社区 skill 为主 | `skillhub search <关键词>` |
| 3 | skills.sh 全生态 | **兜底**：覆盖面最广（含未被精选的 skill），质量参差 | `npx skills find <关键词>` |

**选源规则**：

- 找**优秀/成熟** skill → 一律**先查阿里 SkillsHub**（精选项质量有把关，且有中文说明，判断成本最低）；
- 阿里站**未命中**或需要冷门/自建 skill → 退到 SkillHub；
- 仍无 → 用 skills.sh 全生态搜索，但**必须**额外做质量判断（安装量、来源可信度、SKILL.md 审阅）。

## 二、检索（阿里 SkillsHub）

配套脚本：`scripts/skillhub_alibaba.py`（零依赖、只读、自动缓存 6 小时）。

```bash
# 列出七大基础分类及收录数
python scripts/skillhub_alibaba.py categories

# 关键词检索（空格分隔多词）
python scripts/skillhub_alibaba.py search "数据分析"

# 按分类过滤（支持扩展类代码，会自动映射到最接近的基础类）
python scripts/skillhub_alibaba.py search 股票 --category finance

# 取详情 + 一键安装命令
python scripts/skillhub_alibaba.py info <skill-id>

# 站点结构变更或需最新数据时
python scripts/skillhub_alibaba.py refresh
```

要点：

- 脚本直接解析站点内嵌的 `skills-data` JSON（全量 107 条），**不经过 npx**，所以没有交互式 TUI 干扰，输出稳定；
- 检索命中后**先看**「安装量 / 来源仓库 / 简介」，再决定是否取详情；
- `info` 会由来源仓库自动推导安装命令（`npx skills add <owner/repo> --skill <id>`）。

## 三、安装与 WorkBuddy 适配（关键）

来源站推荐的一键安装命令走 skills.sh 官方 CLI：

```bash
npx skills add <owner/repo> --skill <skill-id>
```

**⚠️ 必须知道的落盘事实**（实测 2026-09-16，skills CLI v11.16.0）：

| 事实 | 说明 |
|------|------|
| 落盘位置 | `<cwd>/.agents/skills/<skill-id>/`（统一源），再复制/链接到各 agent 目录 |
| 支持的 agent | **79 个**（.claude / .codebuddy / .hermes / .windsurf / .zencoder …） |
| **WorkBuddy 不在其中** | `~/.workbuddy/skills/` **不会被自动写入** → 必须走下面的搬运步骤 |
| 安全评估 | CLI 会给出第三方安全评估（Gen / Socket / Snyk），可作为安装前的风险信号 |

### 搬运步骤（装入 WorkBuddy）

```bash
# 0) 前置：确认 npx 可用（Windows 见第四节坑位说明）
# 1) 在临时目录安装（--copy 避免符号链接；-a '*' 覆盖全部 agent 或按需指定单个）
mkdir -p /tmp/skill-install && cd /tmp/skill-install
npx skills add <owner/repo> --skill <skill-id> -a '*' --copy -y

# 2) 复制到 WorkBuddy 用户级 skill 目录
#    （源：.agents/skills/<skill-id> → 目标：~/.workbuddy/skills/<skill-id>）

# 3) 校验 SKILL.md frontmatter（name/description 是否完整），
#    再交教授确认后启用
```

**边界**：安装 = 环境变更，属外部写入动作。Agent 可以检索、取详情、给出安装命令和风险摘要，但**必须经教授确认后**才执行安装与搬运（自动化态只能入队 `pending_actions`）。

## 四、环境坑位（Windows 实测）

| 现象 | 原因 | 处理 |
|------|------|------|
| `npx` 报 `'C:\Program' 不是内部或外部命令` | node 装在含空格的路径（`C:\Program Files\nodejs`），`npx.cmd` 内部拼接未加引号 | 直接用完整路径调用：`"/c/Program Files/nodejs/npx.cmd"`；或改用 PowerShell 调用 |
| `npx <子命令> "带空格的查询词"` 失败 | 参数引号经 `.cmd` 传递时被拆断 | 查询词避免空格，或把查询拆成多个词分别搜 |
| managed node 目录无 `npm` / `npx` | 该发行只含 `node.exe` | 改用系统 Node（`C:\Program Files\nodejs`） |
| `npx skills find <词>` 输出被 TUI 框线干扰，`--json` 解析失败 | CLI 的 `--json` 与 `--list` 互斥、且渲染带 ANSI | **检索优先用本 skill 的脚本**，不走 npx |

## 五、与其它来源策略的关系

- 本 skill 的**达标检查执行器目录**是 [best-practices/toolbox.md](best-practices/toolbox.md)（skillhub.cn 托管的核心工具），与本文不冲突：toolbox 管「checklist 未达标该装哪个」的**内部目录**，本文管「从外部发现优秀 skill」的**检索与安装流程**；
- 已装/自建积木名册见 [skill-registry.md](skill-registry.md)——**先查名册**，名册没有才走本文的外部检索。
