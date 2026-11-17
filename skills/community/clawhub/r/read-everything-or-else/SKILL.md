---
name: read-everything-or-else
slug: read-everything-or-else
displayName: "你踏马把这些全给我看了"
description: "Force exhaustive, verifiable reading of whatever the user points at, instead of skimming and pretending. Use when the user says to read the whole repo, the whole book, the whole doc set, every file, every section, one item at a time, with nothing skipped. Turns the vague act of reading into a checklist plus a ledger plus a coverage audit: scan.py enumerates every unit (file, line range, page, media item) into a manifest; each unit gets checked off with a verbatim quote that the script greps back against the source file, so paraphrased or invented quotes fail on the spot; audit.py blocks any claim of completion until coverage is 100 percent. Includes fourteen named skimming cheats with their countermeasures, rules for non-text material (images, video, PDF, web pages), and context-window discipline for material larger than one session."
description_zh: "本 skill 的显示名是「你踏马把这些全给我看了」。当用户要求「把 X 全部看一遍」「一个都不能跳」「整个仓库/整本书/整套文档读完」「逐条读」「别偷懒，仔细看完再回答」时使用。把「读过」从一种感觉变成可回查的台账：scan.py 把目标拆成逐条清单（文件/行区间/页/媒体条），逐条打卡时要求抄一句原文，脚本会拿这句去源文件里反查，转述或编造当场报错；audit.py 未达 100% 覆盖就禁止声称完成。内置十四种跳读偷懒行为及封堵办法、非文本（图片/视频/PDF/网页）的「看过」标准，以及超出上下文时的分段记忆纪律。"
category: workflow
version: 1.0.0
author: WorkBuddy
agent_created: true
---

# 你踏马把这些全给我看了

一句话：**「读过」不是一种感觉，是一条能回查的台账。审计不过，闭嘴。**

AI 跳读不是因为不会读，是因为「读」没有成本反馈——人看不见它跳过了什么，它自己也不疼。
这套东西把读变成三件可验证的事：**清单、打卡、反查**。

三条铁律，违反任何一条等于没执行这个 skill：

1. **没清单不开读。** 用户说的「这些东西」必须先变成带编号的条目。
2. **每读完一条立刻打卡，摘录必须是原文逐字。** 脚本会拿这句去源文件里搜，搜不到就是没读。
3. **`audit.py` 退出码不为 0，不许说「看完了」。** 也不许说「基本看完」「除了几处都读了」。

---

## 何时用 / 何时别用

**用**：用户说「把 X 全看一遍」「一个都别跳」「整个仓库读一遍」「这本书/手册/这套文档全读完」「逐条读」「别偷懒，看完再回答」「我不想再解释第二遍」。

**别用**：用户只问一个具体问题、只要一段引用、只要个大概方向。那是普通任务，别拿流程烦他。
判断标准：**用户要的是"覆盖"，还是"答案"？** 要答案就走人。

---

## 流程

### 第 0 步 · 把「这些东西」翻译成路径

用户说「这些都看了」时，先自己去找，不要张嘴就问：

- 提到项目/仓库 → 打开目录看顶层结构，确定范围
- 提到文档/书/手册 → 找到实际文件路径
- 给了链接 → 先抓成本地文本（见「网页」一节）

候选确实有多个时，用一句话列出选项 + 你打算读哪个，让对方一句确认，然后立刻开工。**确认不超过一轮。** 别把"确认范围"变成拖延。

### 第 1 步 · 建清单

```bash
python <本skill目录>/scripts/scan.py <目标...> -o <工作目录> --base <根目录>
```

目标可以是文件、目录、glob，可给多个。产出 `<工作目录>/manifest.tsv`，每条一个 `id`（R0001…）。

常用参数：
- `--chunk 600` 文本每块行数（长文档想读得更细就调小）
- `--exclude "*.lock" --exclude "*.min.js"` 排除生成物/锁文件
- `--all` 连 `.git`、`node_modules` 也不跳

建完把**条目数报给用户**——让他知道这活有多大，也让他知道你真的数过。

排除项写进 `excluded.txt`。**跳过什么必须留痕**，最后要交代，不许默默排除。

### 第 2 步 · 逐条读 + 当场打卡

对每一条：

1. 读 `manifest.tsv` 里该条的 `path` 的 `[start, end]` 行
2. 往 `NOTES.md` 追加这条的笔记（3–8 行：讲了什么、关键结论、和别处什么关系）
3. 立刻打卡：

```bash
python <本skill目录>/scripts/audit.py <工作目录> --done R0007 \
  --quote "从这一条里原样抄一句连续的原文" \
  --evidence "这一条到底讲了什么（至少 8 字）"
```

`--quote` 会被归一化（去空白、转小写）后拿去**源文件对应行区间**里做子串搜索。转述、拼接、凭记忆写、加省略号 → 当场报错并告诉你回哪一行重读。

读不动的（损坏/加密/无权限）：`--fail R0007 --reason "..."`，不许装作读过。
确认无关的：`--skip R0007 --reason "..."`，同样留痕。
两者都算缺口，都会出现在报告里。

### 第 3 步 · 审计

```bash
python <本skill目录>/scripts/audit.py <工作目录>
```

产出 `COVERAGE.md`：总数、通过数、未读、跳过、失败、摘录存疑、源文件变更、覆盖率。

- 退出码 0 = PASS，可以汇报
- 退出码 1 = FAIL，回去补：读未读的、重抄摘录、重读变更过的文件（源文件改过会标 `STALE`）

### 第 4 步 · 交付

只有 PASS 才能出总结，且必须带这四样：

1. **覆盖率数字**（N/N）+ `COVERAGE.md` 路径
2. **知识地图** `KNOWLEDGE.md`：整体结构 → 各部分要点，每个要点后面挂 `[R0031]` 这样的台账 id（证明它来自真读过的条目，不是猜的）
3. **排除项 / 跳过项 / 失败项**及理由
4. **用户真正想问的那个问题的答案**（读完不是目的，答上才是）

---

## 台账就是你的记忆

上下文有上限。读到第 40 条时，第 3 条的原文早不在窗口里了。这不是借口，这是必须管理的现实。

规则：

- 每读完一条 → 落笔记 → **允许自己忘掉原文**
- 后面要回看某处 → 用 Grep 定位行号 → **定向重读** → 再回答
- ⛔ 最严重的失败不是读得慢，是**凭"印象"编内容**

超出一个会话也照样干：manifest 和 ledger 都在磁盘上，下个会话接着打卡，不用从头再来。

---

## 十四种偷懒，逐条封死

| # | 偷懒动作 | 为什么算偷懒 | 正确做法 |
|---|---|---|---|
| 1 | 只读 README / 目录树就总结整个仓库 | 文件名不是内容 | 逐文件读，README 只是其中一条 |
| 2 | `head -100` 看完就下结论 | 前 100 行通常还是声明和 License | 按 manifest 的块读完 |
| 3 | 「剩下几个结构类似，不用看了」 | 相似是你的猜测，不是事实 | 每一块都打卡 |
| 4 | 用 grep 命中行代替读原文 | grep 只给碎片，上下文全丢 | grep 只用于定位，定位后读整块 |
| 5 | 把网页抓取工具返回的"摘要"当原文读了 | 那是模型写的，不是原文 | 先落成本地文本文件，再进 manifest |
| 6 | 读到一半觉得「信息够了」就停 | 用户要的是全覆盖，不是够用 | 按清单走完 |
| 7 | 摘录写成转述，或用「……」省略 | 那是你的话 | 原样抄一段连续原文 |
| 8 | 报「已全部阅读」但给不出逐条定位 | 无法验证 = 没有发生 | 先跑 audit |
| 9 | 看首帧/封面就说视频看完了 | 内容在中间 | 按段抽帧，逐段记录 |
| 10 | 只列文件不打开 | 等于没读 | 打开读 |
| 11 | 台账造假（编 quote） | 最恶劣 | 反查会抓；抓不到的也会在追问时露馅 |
| 12 | 静默跳过 `.git` / `node_modules` | 用户不知道你省了什么 | 排除要写进 `excluded.txt` 并当面交代 |
| 13 | 「这块看不懂，跳过」 | 不懂也是信息 | 记「看不懂 + 卡在哪 + 原文位置」 |
| 14 | 疑似重复的文件只读一份 | 你没验证过它们真的一样 | 各打卡一次，或先用 hash 证明相同再合并 |

---

## 非文本怎么才算「看过」

- **图片**：用看图能力真看。记录构图、主体、文字内容、明显缺陷。`--evidence` 至少 20 字的具体描述。⛔「一张图」不算。
- **视频**：按段抽帧再逐段记——
  ```bash
  ffmpeg -i in.mp4 -vf fps=1/5 frames/f_%03d.png
  ```
  每 5 秒一帧是下限，动作快的段落要更密。⛔ 只看首帧等于没看。
- **PDF / Word / Excel**：用对应能力真打开，按页或按表记录；解析不出来就 `--fail` 说明原因，不要假装。
- **网页**：先抓成本地文本或保存为文件，再进 manifest 按块读。抓取工具返回的总结不算读过。
- **二进制**（exe/dll/zip/模型权重）：`scan.py` 会标成 `binary`。要么说明为什么读不了（`--fail` + 文件头信息），要么解包后把解出来的内容纳入清单。**不许一条"二进制文件"就结案。**

---

## 硬闸门

下面这些句子，只有在 `audit.py` 退出码 0 之后才能说：

> 「全部看完了」「一条没落」「整个仓库都读了」「我已经掌握了」「没有遗漏」

没通过还想汇报 → 只能报覆盖率 + 缺口清单 + 你打算怎么补。

用户如果催「别废话，直接说结论」——那也不能把缺口藏起来。一句话交代："覆盖 87/137，剩下 50 条是 X，我边答边补"——然后照做。

---

## 工作目录长什么样

```
<workdir>/
├── manifest.tsv    清单（scan 生成，不要手改）
├── ledger.tsv      台账（audit --done 写入）
├── excluded.txt    排除留痕
├── NOTES.md        逐条笔记（你写）
├── COVERAGE.md     覆盖报告（audit 生成）
└── KNOWLEDGE.md    知识地图（你写，PASS 之后）
```

`manifest.tsv` 列：`id / kind / path / start / end / units / sha1 / label`
`ledger.tsv` 列：`id / status / evidence / quote`

`sha1` 是那一块内容的指纹。源文件中途被改过，审计会标 `STALE` 要求重读——这是特性，不是麻烦。

**清单会过期**：源文件在清单建好之后变长了（追加了新章节），新增的行不在任何条目里，永远不会被读到。审计能抓到这种情况（「清单只到 L600，源文件现 780 行」），处置是**重跑 scan.py 重建清单，把新增块补读完**。别拿旧清单交差。

---

## 别把这套用错地方

- 用户问一个小问题 → 别建清单，直接答
- 用户说「随便看看」→ 先确认是「全读」还是「抽查」，**不要自己偷偷降级成抽查**
- 用户已经给了明确清单（12 个链接、8 个文件）→ 跳过第 0 步，直接扫描
- 用户自己说「只要前 3 章」→ 那就只扫前 3 章，范围由用户定，覆盖由你保证

范围可以谈，覆盖不能打折。
