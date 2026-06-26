---
name: ljg-paper-flow
description: "Paper workflow: read papers + cast 取景框 library cards in one go. Takes one or more arxiv links, paper URLs, PDFs, or paper names. For each paper, runs ljg-paper (generates org analysis) then ljg-library (distills the paper's 取景框 into a 2050 library card PNG). Use when user says '论文流', 'paper flow', '读论文并做卡片', '论文卡片', or provides multiple papers wanting both analysis and cards."
user_invocable: true
version: "1.1.0"
---

# ljg-paper-flow: 论文流

一条命令完成：读论文 → 生成解读 → 铸成取景框借书卡。支持多篇并行。

## 模式

**强制 NATIVE 模式。** 本 workflow 是纯 skill 管道（ljg-paper → ljg-library），不需要 Algorithm 的七步流程。直接按下方执行步骤调用 skill，不走 OBSERVE/THINK/PLAN/BUILD/EXECUTE/VERIFY/LEARN。

## 参数

无 flag。论文来源从对话或命令里取（arxiv URL、PDF 路径、论文名）。每篇论文走 ljg-paper → ljg-library，卡片类型固定为取景框借书卡——ljg-library 只产这一种卡，没有 ljg-card 那套 `-l/-i/-c/-v` 模具可选。

## 执行

### 1. 收集论文列表

从用户消息中提取所有论文来源（arxiv URL、PDF 路径、论文名称等）。

### 2. 并行处理每篇论文

对每篇论文，启动一个 Agent subagent，每个 subagent 按顺序执行两步：

**步骤 A — 读论文（ljg-paper）：**

调用 Skill tool 执行 `ljg-paper`，传入该论文的来源。等待完成，获得生成的 org 文件路径。

**步骤 B — 铸取景框卡（ljg-library）：**

读取步骤 A 生成的 org 文件——里面已经把这篇论文的命题、内核、它带来的新看世界方式拆透了，这正是 ljg-library 要的「已想透的取景框思想」。把这份思想连同论文标题 / 作者 / arxiv 信息交给 Skill tool 执行 `ljg-library`：走它的输入弹性路径（给了思想就只校验 + 画图，跳过从零提炼），产出取景框借书卡 PNG。等待完成，获得 PNG 路径。

### 3. 汇总报告

所有论文处理完成后，汇总输出：

```
════ 论文流完成 ═══════════════════════
📄 {论文标题1}
   📝 解读: {org 文件路径}
   🃏 取景框卡: {PNG 文件路径}

📄 {论文标题2}
   📝 解读: {org 文件路径}
   🃏 取景框卡: {PNG 文件路径}
...
```

## 关键约束

- 每篇论文的两步必须串行（先 paper 后 library），但多篇论文之间并行
- ljg-paper 和 ljg-library 各自的质量标准、红线、品味准则不变
- 卡片的取景框来自生成的 org 文件（已拆透的命题 + 内核），不是原始论文
- **论文 ≠ 书，素材降级**：ljg-library 的封面（weread）/ 作者头像（维基）/ 出版社字段是为书设计的。论文走 arxiv：weread 多半搜不到 → 封面落 CSS 占位；arxiv 作者多半不在维基 → 头像省略；书目行改用 arxiv 元数据（作者 · arXiv:ID · 年份）。卡的命在取景框意向画面 + 费曼讲解 + 手绘图，这部分论文完全适配，封面 / 头像缺位不伤核心。
- **并行隔离 /tmp 竞争**：ljg-library 默认把封面 / 头像写死在 `/tmp/lib_cover.jpg`、`/tmp/lib_avatar.jpg`；多篇并行会互相串图。每个 subagent 必须用唯一路径（如 `/tmp/lib_cover_{slug}.jpg`），渲染后亲眼验图确认没串。
