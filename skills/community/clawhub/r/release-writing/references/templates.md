# 格式骨架与词表

可直接复制的骨架，配合 `SKILL.md` 第 1 节的组织标准使用。

## 目录

1. [小节词表](#1-小节词表)
2. [新建 CHANGELOG](#2-新建-changelog)
3. [一个完整的版本节](#3-一个完整的版本节)
4. [底部链接引用](#4-底部链接引用)
5. [Release notes 骨架](#5-release-notes-骨架)
6. [常见偏离](#6-常见偏离)

## 1. 小节词表

**小节名统一用英文**，即 Keep a Changelog 的六个类别；**正文语言跟随仓库 README 的主语言**。

| 小节 | 含义 |
|---|---|
| `Added` | 新功能、新能力、新的可选项 |
| `Changed` | 既有行为改变；**收紧到会拒绝旧输入的都归这里** |
| `Deprecated` | 标记将来移除，当前仍可用 |
| `Removed` | 公开接口、命令或配置项被删除 |
| `Fixed` | 修 bug、放宽过严的限制、补齐文档与实现的不一致 |
| `Security` | 安全问题的修补 |

顺序固定按上表，没有内容的小节直接省略，不要留空标题。

英文小节配中文正文是刻意的：六个类别是语义标签，英文让它们跨仓库可比、可被工具识别；正文
是写给人读的，用哪种语言取决于读者是谁。真正要避免的是**同一个仓库里两种写法并存**。

`Unreleased` 同理用英文：`## [Unreleased]`。

## 2. 新建 CHANGELOG

正文为中文的仓库：

```markdown
# Changelog

本文件记录本项目所有值得注意的变更。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]
```

正文为英文的仓库：

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
```

若仓库有自己的分级细则（例如区分「可阻断的约束」与「可覆盖的默认做法」），写在开头这段之后，
一句话说清哪种进哪个小节——它会成为后来者判断的依据，且不与上面六个类别冲突。

## 3. 一个完整的版本节

```markdown
## [0.4.0] - 2026-07-27

<2–4 行导语：这一版主要在做什么，需不需要迁移。有破坏性变更时在这里明说。>

### Changed

**任务必须点名来源条目**。`prepare` 现在要求 `source_entry` 指向对应标题并核对正文，任一
漂移都 fail closed。

*升级*：旧版本建立的任务若缺 `source_entry` 会被拒绝。补上该字段并让两处正文一致即可。

### Added

**支持 Windows 原生环境**。此前在入口即失败。目录访问改为双后端，并在打开前后比对文件身份。

### Fixed

**长文档可以直接滚动**。正文面板此前不能收缩，长内容会把布局撑出横向滚动。
```

条目也可以用列表形式（`- **标题**。说明`）。同一个仓库里选一种，不要混排。

## 4. 底部链接引用

用了 `## [X.Y.Z]` 这种方括号标题，就必须在文件末尾维护对应的链接，否则括号不指向任何东西：

```markdown
[Unreleased]: https://github.com/<owner>/<repo>/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/<owner>/<repo>/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/<owner>/<repo>/compare/v0.3.2...v0.3.3
```

每次发版加一行，并把 `Unreleased` 的起点改成新版本。

组织标准要求方括号写法，所以这套链接是必须维护的。历史版本此前没有方括号标题时，
只补新版本的链接即可，不必回头改写历史小节。

## 5. Release notes 骨架

```markdown
<一到两句：这一版是什么性质，要不要迁移>

### 主要变化

- **加粗标题**。一句话说明，必要时补一句边界。

### 升级提示

<仅当有 Changed 时出现。写用户要做的动作。>

```bash
<安装或升级命令>
```

完整变更见 [CHANGELOG](https://github.com/<owner>/<repo>/blob/vX.Y.Z/CHANGELOG.md#xyz---yyyy-mm-dd)。
```

标题：`vX.Y.Z — 三到八个字的主题`。

锚点由版本标题生成——`## [0.4.0] - 2026-07-27` 对应 `#040---2026-07-27`（去掉方括号与点，
空格和短横线折成连字符）。拿不准就发布后点一下链接验证。

## 6. 常见偏离

按影响排序，前两条会真的误导人：

- **收紧写进了 Fixed**。读者据此以为可以无脑升级，然后在生产环境被拒。
- **安装命令指向改名前的地址**。仓库改名后往期 release notes 不会自动更新，用户复制到的是
  错误的命名。
- **整版写成一段没有小节的长文**。读者需要扫描，判断有没有影响到自己，而不是从头读到尾。
- **release notes 是 CHANGELOG 的副本**。几百行不叫摘要。
- **release 标题只有版本号**。列表里一排 `v0.7.4 / v0.7.5 / v0.7.6`，没人知道哪版该看。
- **方括号标题没有底部链接引用**。
- **CHANGELOG 链接指向 `main`**，下一版就失效；应指向 tag。
