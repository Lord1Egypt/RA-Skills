---
name: skill-registry-publish
description: "Take an agent skill from personal use to public release, then get it discovered. 把一个自用 skill 泛化成可公开发布的版本，再推到公开目录。Includes a generalization pass (hardcoded paths, internal addresses, credentials), a market scan that derives capability dimensions from peer SKILL.md headings, name collision checks across three registries, one-command publish, and index verification. 含泛化检查、赛道分析、取名占用检查、一键发布、收录验证。用户要说「发布这个 skill」「上架」「泛化」「起个名字」「这个赛道有谁」「让人能搜到」时用。"
license: MIT
metadata:
  version: 0.6.0
  openclaw:
    requires:
      bins: ["node", "git"]
triggers:
- 发布 skill
- 上架 skill
- skill 怎么发布
- 让 skill 被搜到
- 给 skill 取名
- skill 名字重复
- 这个赛道有谁
- skill 竞品分析
- publish skill
- 发布到 clawhub
- 上 skills.sh
- skill 收录
---

# skill-registry-publish

发布 agent skill 到公开目录，并争取被发现。

## 五个环节

| 环节 | 做什么 | 方法 | 脚本（可选） |
| --- | --- | --- | --- |
| 泛化 | 把自用版本改成别人装得上、看得懂的 | 见「零、泛化」的五类判断 | `generalize.mjs` |
| 定位 | 这个赛道有谁，它们覆盖什么，哪段空白 | 见「一、赛道分析」的五步 | `analyze.mjs` |
| 取名 | 候选 + 三渠道占用检查 | 见「二、取名」的四步 | `name-check.mjs` |
| 发布 | 检查、提交、推送、clawhub、触发遥测 | 见「三、发布」的四个小节 | `publish.mjs` |
| 验证 | 索引是否真的生效 | 只认 api/search 的 count | `check.mjs` |

**方法和脚本是两回事。** 每个环节都有一套可以手算的步骤，脚本只是把其中查网页、数标题、比对字符串的体力活自动化。没有脚本照样能做，有脚本做得快。

泛化是第一步，因为它会改文件内容。跳过它直接发，别人装上去看到的是你的机器路径。

## 零、泛化

自用的 skill 和能公开发布的 skill 差在什么地方：自用版本里到处是自己环境的痕迹，别人装上去第一步就报错。

```bash
node scripts/generalize.mjs <仓库路径>
```

扫三类问题，分三级处理：

| 级别 | 内容 | 处理 |
| --- | --- | --- |
| block | 绝对路径、内网地址、凭据形态 | 必须清零 |
| warn | 个人用户名、私有项目名、会过期的数字 | 逐条确认 |
| info | 安装命令里的账号 | 保留，本来就该是你的 |

```
=== 必须改（别人跑不起来或看到错误指引） ===
✗ 绝对路径  src/config.mjs:12
  "/path/to/your/local/file.json"
  为什么：别人机器上没有这个路径，报错信息会指错方向
```

### 脚本扫不出来的

文本扫描只能抓字符串。下面这些要靠人读代码判断：

**写死的端口和路径假设。** 默认用 9333 端口但不处理被占用、默认 `~/.config/x` 却不检查是否存在。

**依赖某个工具已装。** 代码里直接 spawn 一个命令，没装就崩，且报错说不清缺什么。

**示例数据的可信度。** 示例里用了自己的真实文件名、真实会话标题，能跑但会让人觉得这个 skill 只对作者有用。

**语言假设。** 输出全是中文，非中文用户看不懂。要么接受这个限制并在描述里说明，要么做成双语。

**平台假设。** 只写了 Windows 的 junction，macOS 和 Linux 用户不知道用什么；反过来也一样。

通用化的做法是：把环境相关的东西全部外置成配置项或环境变量，代码里只留默认值和清楚的报错。



### 输出语言

全部五个脚本的输出都跟随系统 locale，也可用 `REG_LANG=en` 或 `REG_LANG=zh` 强制。

`generalize.mjs`、`check.mjs`、`publish.mjs`、`analyze.mjs`、`name-check.mjs` 的标题、状态词、判定文本、局限说明都是双语的。

## 一、赛道分析

要回答三个问题：这个赛道有谁、它们各自覆盖了什么、哪一段没人做。

方法本身不需要脚本。脚本只是把这套步骤里读文件、数标题的体力活自动化。

### 方法

**第 1 步 找同类**

```bash
npx skills find "<关键词>"
```

或者直接翻 skills.sh 的搜索结果页。列 5 到 8 个。

筛选标准只有一个：描述读下来，它解决的问题和你一样。名字里带关键词不算，`kafka-schema-registry` 和 skill 目录没有关系。

**第 2 步 抄章节标题**

每个同类拉下 SKILL.md，把它所有的二级三级标题抄出来。

标题是作者自己对能力的划分，比 description 可靠。description 写给检索用，标题写给读者用。

**第 3 步 归并成能力**

把标题按首词归一。`extract text`、`extract images`、`extract pages` 是同一项能力 `extract`；`add watermark`、`add signature` 都是 `add`。

然后统计每项能力在几个同类里出现。

**第 4 步 分档**

| 出现范围 | 含义 | 怎么用 |
| --- | --- | --- |
| 六成以上 | 标配 | 不构成差异，写了也只是及格 |
| 两成到六成 | 中性 | 看你的目标决定做不做 |
| 只有一两个 | 差异空间 | 候选方向，但要先确认不是伪需求 |

**第 5 步 判断空白真假**

空白有三种，处理方式完全不同：

| 类型 | 特征 | 动作 |
| --- | --- | --- |
| 真空白 | 没人做，且社区有抱怨或提问 | 值得切入 |
| 伪需求 | 没人做，因为不需要 | 跳过 |
| 隐性覆盖 | 看着没人做，实际藏在别的工具或流程里 | 先查再动 |

区分办法是搜 issue、搜讨论区，看有没有人抱怨过这件事。凭直觉判断准确度很低。

### 输出模板

```markdown
## 同类

| 工具 | 安装量 | 覆盖到的能力 | 缺什么 |
| --- | --- | --- | --- |
| owner/repo@skill | 399 | 校验、打包、推仓库 | 目录发布、收录验证 |

## 能力分布

- 标配（多数都有）：frontmatter 校验、推送到仓库
- 差异空间（只有一两个有）：脱敏、名字检查、收录验证
- 无人做：索引验证

## 结论

我做「索引验证」这一段，因为 A 和 B 都停在推仓库，
而社区里存在「发了但搜不到」的抱怨，属于真空白。
```

### 脚本加速

```bash
node scripts/analyze.mjs "<关键词>" --top 6
```

它完成第 1 到第 3 步：搜索、拉文件、抄标题、归并、计数。

判读仍然要人做。脚本按字符串匹配，措辞不同就漏判，同词不同义会混进来，正文取不到的项目会全部记成「未覆盖」。

### 什么情况下不用脚本

同类少于三个的时候，直接读几篇更快。脚本的价值在批量。


## 二、取名

名字决定可检索性。clawhub 的搜索只匹配 `displayName`，skills.sh 的模糊搜索里同词越多单个越难被点到。

### 方法

**第 1 步 组候选**

从「功能动词 + 宾语」组合，出 3 到 5 个。动词优先选检索高频的：export、backup、archive、publish、sync、search、reader。

**第 2 步 三处查**

| 查哪 | 查什么 | 判定 |
| --- | --- | --- |
| skills.sh | 有没有同名的 skill id | 有就是硬撞车 |
| clawhub | 有没有同名条目（displayName 精确匹配） | 有就是硬撞车 |
| GitHub | 有多少同名仓库 | 不同领域同名很常见，只作密度参考 |

```bash
npx skills find "<候选名>"
curl -s "https://www.skills.sh/api/search?q=<候选名>"
curl -s "https://clawhub.ai/api/search?q=<候选名>"
```

**第 3 步 判定**

| 判定 | 条件 | 动作 |
| --- | --- | --- |
| 干净 | skills.sh 和 clawhub 都无同名，命中数少 | 用 |
| 拥挤 | 无同名，但 skills.sh 命中超过 10 条或 GitHub 同名超过 50 个 | 可用，注意辨识度 |
| 太泛 | 命中超过 50 条 | 换，搜索时会沉底 |
| 撞名 | skills.sh 或 clawhub 已有同名 | 必须换 |

**第 4 步 命名原则**

- 含高频检索词，但不超过两个，否则泛化
- 避开已被占用的语义。`ship` 在 skill 语境里已经指「铺到本机各 agent」，`publisher` 指「打包推仓库」
- 两到三个词，超过四个词记不住也打不对
- 用 kebab-case，和目录名、frontmatter 的 `name` 三者一致

### 输出模板

```markdown
| 候选 | skills.sh | clawhub | GitHub | 判定 |
| --- | --- | --- | --- | --- |
| chat-publish | 6 hits | free | 34 repos | 干净 |
| export-chat | 16 hits | free | 115 repos | 拥挤 |
| chat-history | 100 hits | free | 1187 repos | 太泛 |

选定：chat-publish
理由：无同名，命中数最低，含高频词 publish。
```

### 脚本加速

```bash
node scripts/name-check.mjs <候选1> <候选2> --owner <账号>
node scripts/name-check.mjs --suggest "export chat conversations"
```

第一种查你给的名字，第二种从一句描述生成候选并排序。`--owner` 用来排除自己已发布的条目，否则每次都误报占用。


## 三、发布

一条命令跑完检查和发布：

```bash
node scripts/publish.mjs --repo <仓库路径> --version 0.5.0 --dry-run   # 先看计划
node scripts/publish.mjs --repo <仓库路径> --version 0.5.0             # 执行
```

它依次做：定位 skill、校验 frontmatter 必填项、提交推送、clawhub 发布、触发 skills.sh 遥测、打印后续动作。

两处会停下来要人接手：

- **clawhub 未登录**。设备码必须在浏览器里输入，脚本没法代做。
- **git 有冲突**。脚本不处理合并，报错退出。

`--dry-run` 只打印计划，`--skip-clawhub` / `--skip-git` 跳过对应步骤。

下面是每一步的细节，出问题时对着看。

### 3.1 布局

必须是 `skills/<name>/SKILL.md`。根目录直接放 SKILL.md 会让部分扫描逻辑提前返回。

本机继续用同一份源码，不要复制两份：把 `~/.agents/skills/<name>` 链接到仓库里的 `skills/<name>`。

```bash
# macOS / Linux
ln -s /path/to/repo/skills/<name> ~/.agents/skills/<name>

# Windows，用目录联接，不需要管理员权限
# PowerShell: New-Item -ItemType Junction -Path <link> -Target <target>
# cmd:        mklink /J <link> <target>
```

两份副本一周内必然漂移，链接不会。

**完成条件**：`npx skills add <owner>/<repo> --list` 能列出这个 skill。

### 3.2 frontmatter

```yaml
---
name: <name>                      # kebab-case，与目录名一致
description: 做什么 + 什么时候用，高频词放最前
license: MIT                      # clawhub 校验，缺失会报 acceptLicenseTerms
metadata:
  openclaw:
    requires:
      bins: ["node"]
triggers:
- 中文触发词
- english keywords
---
```

**完成条件**：`node scripts/check.mjs <owner>/<repo>` 的仓库、布局、frontmatter 三项全绿。

### 3.3 clawhub

```bash
npx clawhub login                       # 设备码，必须人工在浏览器输入
npx clawhub skill publish ./skills/<name> \
  --slug <name> --version 0.1.0 \
  --tags "a,b,c" --changelog "..."
```

发布后进安全扫描队列 24 到 72 小时。版本号必须语义化递进。设备码登录没法自动化。

**完成条件**：返回 `Update submitted for <name>@<version>`。

### 3.4 skills.sh 遥测

**最容易白做的一步。** CLI 的判断只看变量是否存在：

```js
function isEnabled() {
  return !process.env.DISABLE_TELEMETRY && !process.env.DO_NOT_TRACK;
}
```

`DISABLE_TELEMETRY=0` 也算存在，等于关闭。

```bash
env | grep -iE "disable_telemetry|do_not_track"    # 先确认
DISABLE_TELEMETRY= DO_NOT_TRACK= npx skills add <owner>/<repo> --skill <name> -y
```

**完成条件**：安装输出有摘要，目标目录出现 `SKILL.md`。

## 四、验证

```bash
node scripts/check.mjs <owner>/<repo> <name>
```

只认 skills.sh 的 `api/search` 返回 count。CLI 能装、页面 200、README 有链接，都不是收录证据。

## 发布前 checklist

- [ ] `--list` 能列出这个 skill
- [ ] `name-check.mjs` 判定不是撞名或太泛
- [ ] frontmatter 有 `name`、`description`、`license`
- [ ] 脱敏：脚本里没有个人路径、密钥、账号、内部 URL
- [ ] README 首屏有安装命令，徽章不指向可能不存在的页面
- [ ] 仓库 `topics` 填了，这是 GitHub 侧的 SEO

## 三个反直觉的事实

1. **clawhub 搜索只匹配 displayName**。描述和 tags 不参与检索。实测 `chat` 命中、`backup` 无结果。
2. **skills.sh 没有提交入口**。没有表单、没有 publish 命令，只有安装遥测一条路。
3. **HTTP 200 不等于有内容**。skills.sh 是 SPA，未收录的路径也回 200。必须看 API 的 count。

## 渠道优先级

| 顺序 | 渠道 | 进入方式 | 成本 |
| --- | --- | --- | --- |
| 1 | clawhub.ai | CLI 发布 + 审核 | 30 分钟 + 等 1 到 3 天 |
| 2 | skills.sh | 安装遥测 | 5 分钟 + 等 |
| 3 | GitHub 直发 | push | 一次性，喂饱 6 个自动抓取目录 |
| 4 | 小站表单 | 人工填表 | 每个 10 分钟 |

smithery 已于 2026-10-31 关停。

## 和同类的关系

| 同类 | 它解决什么 |
| --- | --- |
| `mercatorproj/skill-publisher` | 校验、打包、推到自己仓库 |
| `zihad550/skills` @ship-skill | 铺到本机各 agent |
| `glebis/claude-skills` @publish-skill | 发到自建站点 |
| `openclaw/openclaw` @clawhub | clawhub CLI 用法 |
| `stealth-factory/skills` @skill-publishing | SKILL.md 写法与 skills CLI 参数 |

一句话分辨：别人管「文件怎么放过去」，这里管「放过去之后为什么搜不到」。

这个赛道不大，同类安装量在 18 到 399 之间。别抱不切实际的期待。

## 参考

- `references/positioning.md`：赛道分析的方法、实测案例、局限
- `references/channels.md`：16 个渠道的流量、进入方式、失效状态
- `references/pitfalls.md`：11 条踩坑，带现象与根因
- `scripts/generalize.mjs`：泛化检查（个人路径、内网地址、凭据）
- `scripts/analyze.mjs`：赛道分析（自下而上提炼维度）
- `scripts/name-check.mjs`：取名与占用检查
- `scripts/publish.mjs`：一键发布
- `scripts/check.mjs`：发布状态自检
