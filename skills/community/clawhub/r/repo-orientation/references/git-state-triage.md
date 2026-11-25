# git 状态只读体检（引用链断裂时）

用于：勘察一个仓库时发现 `git log` 报 `fatal: bad object HEAD` / `invalid sha1 pointer`，需要判断「工作树改动是否安全、有没有可恢复的提交、引用链断在哪一环」。
**全程只读**：不跑 `gc` / `reflog expire` / `reset` / `update-ref` / 删 `.git` 内文件——这些是不可逆动作，须主人明示。

## 1. 确认症状

```bash
git -C <root> log --oneline -5
git -C <root> status --short
git -C <root> fsck --no-progress
```

`fsck` 输出的三类信号要分开读：

| 输出 | 含义 |
|---|---|
| `invalid sha1 pointer`（指向 refs/heads/X 或 HEAD） | 该 ref 指向的 commit 对象不在库里 —— 引用链断，工作树内容通常完好 |
| `missing blob` / `missing tree` | 对象真丢了 —— 被这些对象引用到的历史内容不可恢复 |
| `dangling commit` / `dangling blob` | 对象还在、只是没被任何 ref 指着 —— **这是可恢复锚点** |

## 2. 找存活的 ref

```bash
cat <root>/.git/HEAD
cat <root>/.git/packed-refs          # 打包的全部 ref，含其它分支
find <root>/.git/refs -type f -exec sh -c 'echo "$1: $(cat "$1")"' _ {} \;
git -C <root> show-ref                # 只列当前可解析的 ref
```

判断口径：`packed-refs` 里其它分支的 sha 若能被 `git -C <root> cat-file -t <sha>` 认成 `commit`，说明**这些分支可作为恢复基线**；只有主分支的指针坏了。

```bash
git -C <root> cat-file -t <sha>      # 期望输出 commit
git -C <root> log --oneline -3 <sha> # 该分支最近提交
```

## 3. 找恢复锚点

`fsck` 报的 dangling commit 逐个验：

```bash
git -C <root> log --oneline -3 <dangling-sha>
git -C <root> show --stat <dangling-sha>
```

悬空 commit 里如果有近期提交（作者时间新、且带工作区里能对上的文件改动），它就是 HEAD 丢失后最可能的替代基线——**把它和「工作树当前未提交改动」一起作为候选，报告给主人，由主人决定重接哪一条**。

## 4. 结论怎么写

- 说清**断点位置**：哪个 ref 坏了、坏成什么形态（对象缺失 vs 仅指针悬空）。
- 说清**工作树安全否**：文件内容在磁盘上，不受 ref 损坏影响；丢的是历史锚点。
- 说清**可恢复来源**：列出存活分支 ref 与悬空 commit 的 sha 与日期。
- **不给「已修复」结论**——修复动作（重接 HEAD、备份 .git、gc 抢救）属另一轮，且要主人点头；主人授权动手修时走 `git-repo-repair`（含「对象丢 ≠ 内容丢」的判定与逐字节复活 commit 的验收判据）。

## 5. 追加判定：对象丢 ≠ 内容丢

`missing blob` 出现时，**先确认内容是否还在工作区**，再下「不可恢复」的结论：

```bash
git -C <root> hash-object <工作区同名文件>   # 与 fsck 报的 missing blob 哈希比对
```

哈希相同 ⇒ 内容完好，恢复时把 blob 重新写回对象库即可（`git hash-object -w`），不必去任何外部备份找。哈希不同 ⇒ 该 blob 的内容确实无处可寻，只能靠别的锚点重建那棵树。
