---
name: ship-skill
description: 把一个 agent skill 发布到公开渠道并尽可能被人发现。覆盖 repo 布局改造、frontmatter 要件、clawhub 提交、skills.sh 遥测触发、索引验证、搜索曝光优化。用户要说「发布这个 skill」「上架」「让人能搜到」「publish to clawhub/skills.sh」时用。
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["node", "git"]
triggers:
- 发布 skill
- 上架 skill
- skill 怎么发布
- 让 skill 被搜到
- publish skill
- 发布到 clawhub
- 上 skills.sh
- skill 收录
---

# ship-skill

发布 agent skill 并争取被发现。这套流程是在一个真实 skill 上跑完整轮之后固化下来的，每一步都对应一个实际踩过的坑。

## 先明确一件事

**符合 SKILL.md 规范不等于会被索引。** 这是最容易搞错的地方：

| 事实 | 含义 |
| --- | --- |
| CLI 能列出并安装你的 skill | 只说明格式和路径对了 |
| skills.sh 网站能搜到 | 需要真实安装事件被后端处理，两回事 |
| clawhub 有发布命令 | 要审核，24 到 72 小时 |

没有任何渠道保证收录。能做的是把可控项做到位，剩下等。

## 流程

### 1. 改布局

必须是 `skills/<name>/SKILL.md`。根目录直接放 SKILL.md 在一些扫描逻辑里会提前返回，导致子目录里的 skill 扫不到。

```
repo/
├── README.md          仓库门面（不是 skill 的一部分）
├── LICENSE
└── skills/
    └── my-skill/
        ├── SKILL.md   frontmatter + 指令
        ├── scripts/
        └── references/
```

本机继续用同一份源码的办法：`~/.agents/skills/<name>` 指向仓库里的 `skills/<name>`。Windows 用 junction（`New-Item -ItemType Junction`），不要复制，否则两处会漂移。

改完必须自检：

```bash
npx skills add <owner>/<repo> --list    # 能列出才算布局对
```

列不出来就是 frontmatter 或路径问题，别往下走。

### 2. frontmatter 补齐

```yaml
---
name: my-skill                    # kebab-case，和目录名一致
description: 一句话说清做什么 + 什么时候用，把用户会搜的词放前面
license: MIT                      # clawhub 校验这个字段，缺了会报 acceptLicenseTerms
metadata:
  openclaw:
    requires:
      bins: ["node"]              # 运行时硬依赖，必须诚实声明
    optional:
      bins: ["google-chrome"]     # 可选依赖
triggers:
- 中文触发词
- english keywords
---
```

`description` 是 agent 决定是否加载的唯一依据，前 30 字最关键。

### 3. 发布到 clawhub

```bash
npx clawhub login                 # 设备码：浏览器打开链接输入码
npx clawhub skill publish ./skills/my-skill \
  --slug my-skill --version 0.1.0 \
  --tags "export,backup,automation" \
  --changelog "首版"
```

- 设备码登录必须人在浏览器里操作，自动化点不出来
- 发布后进安全扫描队列，24 到 72 小时，期间不公开
- 后续更新要升语义化版本号，重跑同一条命令

### 4. 触发 skills.sh 遥测

**这一步的判断是整套流程里最容易错的。**

```javascript
// skills CLI 源码，dist/cli.mjs
function isEnabled() {
  return !process.env.DISABLE_TELEMETRY && !process.env.DO_NOT_TRACK;
}
```

只看「变量存不存在」，不看值。所以 `DISABLE_TELEMETRY=0` 和 `=1` 效果一样，遥测全程关闭，安装再多次也不会上报。

正确做法：

```bash
DISABLE_TELEMETRY= DO_NOT_TRACK= npx skills add <owner>/<repo> --skill <name> -y
```

装之前先确认环境干净：

```bash
env | grep -iE "disable_telemetry|do_not_track"   # 有输出就要覆盖成空值
```

### 5. 验证

```bash
node scripts/check.mjs <owner>/<repo> [skill-name]
```

脚本查三件事：skills.sh 索引、clawhub 下载量、仓库布局。也可以手工查：

```bash
# skills.sh 是否有索引（唯一可信的判断方式）
curl -s "https://www.skills.sh/api/search?q=<skill-name>"

# clawhub 下载量
curl -s "https://api.clawhub.ai/api/search?q=<skill-name>"
```

CLI 能装、页面 200、README 有链接，都不能证明被索引。只认 API 返回的 `count`。

## 三个反直觉的事实

1. **clawhub 搜索只匹配 displayName**。description 和 tags 不参与检索。实测 `chat` 能命中，`backup`、`导出对话` 一律无结果。所以名字里要含高频词，描述优化只影响用户点进来之后的转化。
2. **skills.sh 没有提交入口**。没有表单、没有 publish 命令，只有安装遥测这一条路。
3. **Cloudflare 那类「访问量」不等于流量**。渠道的真正价值看它自己的搜索/榜单是否能带来安装，clawhub 在零 star 零推广下三天跑出 89 次下载，是唯一被验证有效的。

## 渠道优先级

按「真实流量 × 进入成本」排，细节见 `references/channels.md`。

| 顺序 | 渠道 | 进入方式 | 成本 |
| --- | --- | --- | --- |
| 1 | clawhub.ai | CLI 发布 + 审核 | 30 分钟 + 等 1 到 3 天 |
| 2 | skills.sh | 安装遥测，无提交 | 5 分钟 + 等 |
| 3 | GitHub 直发 | push | 一次性，喂饱所有自动抓取目录 |
| 4 | smithery | **已关停，跳过** | - |
| 5 | 小站表单 | 人工填表 | 每个 10 分钟，合计约 300K 访问 |

六个目录（skillsmp、claudepluginhub、claudemarketplaces 等）自动抓 GitHub，仓库做规范就自动进，不需要额外动作。

## 不要做的事

- 不要为了「让 skills.sh 收录」去跑定时重装刷安装量。官方明确禁止，而且事件带机器标识，刷不出来。
- 不要同时维护两份 skill 副本。用链接，一份源码。
- 不要在 CI 里触发安装测收录。CI 事件会被单独标记，行为与本地不同。
- 不要把「CLI 能列出」当成「已收录」写进 README 徽章，会变成死链。

## 参考

- `references/channels.md`：各渠道流量、进入方式、审核规则、实测状态
- `references/pitfalls.md`：完整踩坑清单，每条带现象和根因
- `scripts/check.mjs`：发布状态自检
