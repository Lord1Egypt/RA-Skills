---
name: release-writing
description: ZenStory AI 的发布标准与发布流程：切版本、写 CHANGELOG 与 GitHub release notes、修订往期发布、仓库改名后清理失效链接。当有人说“发个 release”“切 0.x.y”“整理 CHANGELOG”“release notes 怎么写”“把往期发布说明改一下”时使用。它规定本组织的格式与发布动作顺序；条目本身的起草可以借助任何 changelog 生成器。
license: MIT
---

# 发布写作

本 skill 管两件外部工具管不了的事：**本组织的格式约定**，和**发布这串动作的顺序与验收**。

条目怎么从 commit 里生成、怎么分类，现成的 changelog 生成器已经做得不错——实测在「这条改动
会不会拒绝旧输入」这类判断上，它们能主动去读源码并判进 `Changed`。**起草可以用它们**；本文
只规定成品长什么样、以什么顺序发出去。

格式骨架与模板见 [references/templates.md](references/templates.md)。

## 1. 组织标准

| 项目 | 标准 |
|---|---|
| 小节名 | 英文，Keep a Changelog 六类：`Added` `Changed` `Deprecated` `Removed` `Fixed` `Security` |
| 小节顺序 | 按上表，没有内容的省略 |
| 正文语言 | 跟随该仓库 README 的主语言 |
| 版本标题 | `## [X.Y.Z] - YYYY-MM-DD` |
| 待发布节 | `## [Unreleased]` |
| 底部链接 | 每个版本一行 compare 链接，必须维护 |
| 版本号 | Semantic Versioning |
| release 标题 | `vX.Y.Z — 三到八个字的主题` |
| release 正文 | 20 行以内，末尾链到该 tag 的 CHANGELOG 锚点 |

英文小节配中文正文是刻意的：六个类别是语义标签，英文让它们跨仓库可比；正文是给人读的。
一个仓库内部保持一致即可。

仓库若有自己的**分级细则**（例如区分「可阻断的约束」与「可覆盖的默认做法」），保留——那是
对分类判据的细化，与六个类别不冲突。

## 2. 发布流程

### 阶段一：确认可以发

```bash
git checkout main && git pull --ff-only
git status --porcelain                  # 必须为空
gh run list --branch main --limit 1     # main 上最近一次 CI 必须绿
```

跑仓库自己定义的发布检查（`CONTRIBUTING.md` 里通常有），不要只跑单元测试。

**测试和 push 不要串在一条命令里。** 失败时后面照样执行；分开跑，亲眼确认输出再继续。

### 阶段二：写 CHANGELOG

起草可借助生成器，再按 [第 1 节](#1-组织标准) 校格式：把 `## [Unreleased]` 切成
`## [X.Y.Z] - YYYY-MM-DD`、补底部 compare 链接、在上方留一个新的空 Unreleased 节。

### 阶段三：走 PR，不要直接推 main

```bash
git checkout -b release/vX.Y.Z
git add CHANGELOG.md && git commit -m "release: X.Y.Z"
git push -u origin release/vX.Y.Z
gh pr create --base main --title "release: X.Y.Z" --body "<要点与升级影响>"
gh pr checks <PR>                       # 全部 SUCCESS 再合
gh pr merge <PR> --squash --delete-branch
```

发布提交走同一条路径，分支保护、CI 和评审才仍然生效。

### 阶段四：打 tag

tag **必须打在已合并的 main 上**，否则它指向一个不在主线上的提交。

```bash
git checkout main && git pull --ff-only
git tag -a vX.Y.Z -m "vX.Y.Z"           # 带注释的 tag，不用轻量 tag
git push origin vX.Y.Z
```

### 阶段五：建 release

```bash
gh release create vX.Y.Z --title "vX.Y.Z — <主题>" --notes "$(cat <<'EOF'
<骨架见 references/templates.md>
EOF
)"
```

### 阶段六：发完验收

```bash
OWNER=<owner>; REPO=<repo>; V=X.Y.Z
git ls-remote --tags origin "refs/tags/v$V"
gh release view "v$V" --repo "$OWNER/$REPO" --json body --jq '.body' | wc -l   # ≤20
```

超过 20 行就回去删。**实测表明只写一个目标数字不管用**——同一份指引下产出仍在 27 行上下，
必须真的数一遍再删。优先删背景解释与根因叙述，保留变化本身和升级动作。

再手点一次正文里的 CHANGELOG 锚点和安装命令：锚点拼错、命令指向旧命名空间，是发完立刻
能看出来的两处。

### 出问题了

**已发布的 tag 不要删改**，往前修：release notes 用 `gh release edit` 直接改；代码问题发
补丁版本并在新版导语里说明规避方式；`gh release delete` 只在发布后极短时间内、确认无人
取用时考虑。

## 3. 哪些内容不进对外产物

读者一种在决定要不要用，一种在判断升级会不会弄坏东西。**判据是：读者需不需要据此采取行动。**

需要，就必须写——破坏性变更、升级步骤、能力退化，一条都不能省，隐瞒才是真问题。

不需要的，不要写：

- **「已知缺口」清单**。发布前实跑发现的问题，先核实（相当一部分是误读，读一遍那条规则或
  跑一次 `--help` 就能排除），**站得住的在发布前修掉**，而不是写成章节。这类问题通常改动
  很小；真正大到修不动的，单独开 issue 并在发布中提一句。
- 与竞品的对比；内部质量发现（工具与产物不匹配、文档自相矛盾）——那些是 issue 的内容。
- 自我批评的语气（「一直在空转」「此前零覆盖」）。同一件事总能只陈述结果：写「补齐了 X」，
  而不是「X 一直是坏的」。

**版本号与内容矛盾时要明说。** 补丁号不传达破坏性变更，这一版若有 `Changed`，导语要把它说清楚。
**别用固定套话开场**——「补丁号不传达这一点，故在此明说」这类句子把读者第一眼看到的位置浪费在
谈版本号上。第一句写读者要做的动作，第二句写为什么：

```markdown
升级后必须重新生成配置，旧配置会被拒绝。本版收紧了 X，补丁号不代表可以无脑升级。
```

判据是这一句能不能直接照着做。做不到就是还没写清楚。

## 4. 修订往期与改名清理

往期 release 页长期被人读到，可以修订：保留**实际做了什么**和**升级影响**，删掉取证叙事
与自我批评，压到 20 行内。**CHANGELOG 的历史小节不要回头改写**——release notes 是展示面，
CHANGELOG 是账本；改名导致的链接失效属于例外，那是修复失效引用。

仓库或组织改名后，往期 release notes 不会自动更新，安装命令会继续指向旧名字：

```bash
OWNER=<owner>; REPO=<repo>; OLD=<旧命名空间>
for t in $(gh release list --repo "$OWNER/$REPO" --limit 100 --json tagName --jq '.[].tagName'); do
  gh release view "$t" --repo "$OWNER/$REPO" --json body --jq '.body' > /tmp/b.txt
  grep -q "$OLD" /tmp/b.txt && { sed "s#$OLD/#$OWNER/#g" /tmp/b.txt > /tmp/n.txt; \
    gh release edit "$t" --repo "$OWNER/$REPO" --notes-file /tmp/n.txt && echo "$t 已修正"; }
done
```

顺带查标题：

```bash
gh release list --repo "$OWNER/$REPO" --limit 100 --json tagName,name \
  --jq '.[] | select((.name | contains("—")) | not) | "无主题: \(.tagName)"'
```

## 5. 把一个仓库迁到本标准

**不重写历史，从下一次发版开始切**，一次到位，不要分几版慢慢改。

1. CHANGELOG 头部补 Keep a Changelog 与 Semantic Versioning 声明（模板见 references）
2. 待发布节统一为 `## [Unreleased]`
3. 新版本节按 `## [X.Y.Z] - YYYY-MM-DD`、英文小节名写；历史小节保持原样
4. 补底部链接引用；历史版本标题没有方括号时，只补新版本的
5. 往期 release 标题补主题，跑第 4 节的改名审计

**compare 链接按实际 tag 相邻关系生成，不是按 CHANGELOG 标题相邻**——两者可能不一致
（曾遇到某版本有 tag、有 release，却没有 CHANGELOG 小节，按标题生成会跨掉一个版本）。
