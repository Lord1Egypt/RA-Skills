# 赛道分析方法

用来回答三个问题：这个赛道有谁、它们各自覆盖了什么、哪一段没人做。

`scripts/analyze.mjs` 是这个方法的部分自动化，读它的输出前先看最后一节「局限」。

## 三步

### 1. 找同类

```bash
node scripts/analyze.mjs "agent skill registry" --top 6
```

脚本在 skills.sh 上用几个变体词搜，合并去重后按安装量排序。

一个踩过的坑：单个模糊查询会被热门大词淹没。搜 `skill publish` 时，排在最前的是 `find-skills`（429 万安装）、`azure-deploy`（66 万），跟发布无关。所以脚本改成拆词分别搜、按交集过滤。

自己手工验证时，用精确的复合词（`skill-publishing`、`publish-skill`）比用自然语句准。

### 2. 拆能力

把「一个 skill 从写完到被人装上」拆成十一段，逐段看谁覆盖了：

| # | 维度 | 判定线索 |
| --- | --- | --- |
| 1 | SKILL.md 写法 | description 当触发器、渐进披露、正文结构 |
| 2 | frontmatter 校验 | 检查 name/description/license 合法性 |
| 3 | 多 skill 仓库布局 | `skills/<name>/` 结构、monorepo |
| 4 | 打包与版本管理 | 语义化版本、changelog、release |
| 5 | 推送到 GitHub | git push、创建仓库、分支管理 |
| 6 | 分发到本机 agent | `~/.agents/skills`、symlink、多 agent 链接 |
| 7 | 发布到第三方目录 | clawhub、registry publish、市场提交 |
| 8 | 收录与索引验证 | 遥测、`api/search`、收录判定 |
| 9 | 名字占用检查 | 撞名检测、改名建议 |
| 10 | 发布前脱敏 | PII、密钥、个人路径、内部 URL |
| 11 | SEO metadata | topics、可发现性、搜索关键词 |

拆到这十一项是因为它们能独立判定，且每一项都对应一个实际会卡住的地方。粒度再细就重复，再粗就看不出空白。

### 3. 读空白

空白点的三种情况，处理方式完全不同：

| 情况 | 特征 | 动作 |
| --- | --- | --- |
| 真空白 | 没人做，且社区有抱怨 | 值得切入 |
| 伪需求 | 没人做，因为不需要 | 跳过 |
| 隐性覆盖 | 看似空白，实际藏在别的工具里 | 先查再动 |

判断属于哪种，靠搜 issue 和讨论，不靠猜。这次做 `skill-registry-publish` 之前，搜 `publish` 相关关键词拿到 100 条结果，逐条读下来发现 7 个真做 skill 发布的，全都停在「推到 GitHub」，没有讲收录机制的，而且社区确实有「发了但搜不到」的抱怨，才算真空白。

## 实测案例：skill 发布赛道

2026-11 的数据，安装量取自 skills.sh。

| skill | 安装量 | 覆盖到哪一段 |
| --- | --- | --- |
| camacho/ai-skills @publish-skill | 399 | 正文取不到，无法判定 |
| joeseesun/qiaomu-skill-publisher | 263 | 1 部分、2、5、6 |
| aperivue/medsci-skills @publish-skill | 110 | 10 最完整 |
| glebis/claude-skills @publish-skill | 87 | 5（自建站点出口） |
| mercatorproj/skill-publisher | 76 | 2、3、4、5 |
| stealth-factory/skills @skill-publishing | 41 | 1 最完整、2、3、11 |
| zihad550/skills @ship-skill | 18 | 3、6 |

第 7、8、9 三段（第三方目录、收录验证、取名）七个工具都没有覆盖。

同时得到一个市场判断：这个赛道最大安装量 399，属于需求真实但小众。参照系是 `google/agents-cli` 的子技能 562.9K、`chat-share-reader` 在 clawhub 三天 89 次下载。

## 局限

这套方法产出的是初筛结论，不是决策依据。

**关键词匹配不等于语义理解。** `analyze.mjs` 用正则判断能力覆盖，措辞不同就漏判，正文写得好但没用这些词的项目会被判为未覆盖。

**候选筛选靠 id 里的词。** 搜 `registry` 会同时命中 skill 目录和容器镜像仓库（`azure-container-registry`、`kafka-schema-registry`），语义完全不同。必须人工过一遍。

**正文取不到的全判空白。** 私有仓库、非 main 分支、路径不标准的都读不到，会显示成 `(正文取不到)`，这些项目的矩阵格子全空，会人为放大空白。

**安装量不等于质量。** 高安装量可能来自母仓库的整套工具（`google/agents-cli` 的子技能），也可能来自早期红利。它只反映被装过多少次。

**赛道小不等于不值得做。** 天花板低的领域适合把知识固化下来自用，顺便公开。指望它出圈是不现实的。

## 结论怎么用

分析完写在 SKILL.md 的「和同类的关系」一节，格式是：

1. 一句话说清别人管哪段、你管哪段
2. 直接写赛道规模，别回避
3. 明确列出不做什么

这样用户看到时能立刻判断该不该用，而不是被描述里的形容词带着走。
