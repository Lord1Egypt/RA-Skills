# 写作流程与编辑 playbook

> 写作不是等灵感，是可复现的流程。本 playbook 给通用写作流程、流程选择决策树、可运行的写作体检命令、量化编辑清单与常见坑。方法论改编自 `mblode/agent-skills@docs-writing`（800 installs，Diataxis + 48 条 voice/structure/clarity 规则）并本地化为本库的短文案 / 技术文章 / 长文三类文体。

## 1. 通用写作流程

```
1. 定受众与目的   — 写给谁？希望对方读完做什么？
2. 列结构骨架     — 标题 + 小标题 + 每节一句话论点
3. 起草（求完整） — 初稿只管写完，不边写边改
4. 编辑（求清晰） — 删冗余、强逻辑、调节奏
5. 标题与开场     — 最后打磨，决定打开率
6. 验收           — 对照目标与 §4 清单逐条检查
```

**铁律**：起草阶段禁编辑，编辑阶段禁新增大段，分开才高效。

## 2. 流程选择决策树（先选对流程，再动手）

```
接到写作任务，按文体分流：
│
├─ 短文案（标题/广告语/CTA/着陆页/邮件）？
│     → 走 [copywriter 子技能](../skills/copywriter/SKILL.md) 的 PAS/AIDA/BAB 框架，不进长流程。
│
├─ 技术文章（选题 → 发布全流程）？
│     → 走 [technical-writer 子技能](../skills/technical-writer/SKILL.md) 的 7 阶段全流程。
│
├─ 长文博客 / 操作指南（重信息增益）？
│     → 走 [content-writer 子技能](../skills/content-writer/SKILL.md) 的 QAE 模式 + 字数分档。
│
├─ 已写完、要发布前验收？
│     → 先过本篇 §3 体检命令 + [seo-content-strategy 策略层](seo-content-strategy.md) 策略层
│       → 再跑 [seo-checker 技术层](../skills/seo-checker/SKILL.md) 11 项。
│
└─ 不确定文体 / 内容散？
      → 用 §3 体检命令量化（句子长度、注水词、段落结构），再按 §5 文体要点校准。
```

> 规则 3 合规：决策树与量化判据的框架源自 `mblode/agent-skills@docs-writing` 的「Mode dispatch + Audit/Writing workflow + clarity rules」，本地化为三类文体；具体产出框架仍在各子技能，本篇只做分流与体检。

## 3. 可运行的写作体检命令

> 编辑不是"读着顺"就过关。下面命令对 `draft.md`（换成你的稿件路径）做量化体检，输出可直接判读。

### 3.1 注水词 / 填充词检测（AI 味的头号信号）

```bash
grep -nE "事实上|值得注意的是|总而言之|简单来说|在当今|随着.*发展|不可或缺的|毋庸置疑|众所周知|显而易见" draft.md
```

有输出 = 命中注水表达，逐条改掉或删掉（能省则省）。

### 3.2 被动语态检测（谁做的动作被藏起来了）

```bash
grep -nE "被[一-龥]{0,10}(了|过|完成|实现|处理|加载|创建|删除|更新|执行|调用|返回)|由[一-龥]{0,10}(进行|完成|实现|处理|执行)" draft.md
```

有输出 = 被动句，尽量改为主动（"服务器加载配置" 而非 "配置被服务器加载"）。

> 为什么动词表要写全：只查 `被…(了|过)` 会漏掉最常见的一类——"配置被服务器加载"结尾没有
> "了/过"，正则直接放过，连本节自己举的反面例句都抓不到。`被` 与 `由` 两支必须各带自己的动词表，
> 不能把动词表只挂在 `由` 上。`[一-龥]{0,10}` 的上限限制施动者长度，避免跨句误命中。

### 3.3 句子长度 / 可读性估算（Python，无需装包）

> 先剥离标题、代码块、引用、表格与图片语法，再切句。否则 Markdown 结构行会被当成"句子"，
> 中位数被一堆 2–8 字的标题拉低，`§4` 的"中位 ≤ 40 CJK"这条判据就永远为真、形同没查。

```bash
python3 - <<'PY'
import re, statistics as st
FENCE = chr(96) * 3          # 用 chr 拼反引号，避免代码块自我嵌套
raw = open('draft.md', encoding='utf-8').read()
raw = re.sub(FENCE + r'.*?' + FENCE, '', raw, flags=re.S)     # 去代码块
body = '\n'.join(l for l in raw.split('\n')
                 if not l.lstrip().startswith(('#', '>', '|')))  # 去标题/引用/表格
body = re.sub(r'!\[[^]]*\]\([^)]*\)', '', body)              # 去图片语法
sents = [s for s in re.split(r'[。！？；\n]', body)
         if len(re.findall(r'[一-龥]', s)) >= 4]             # 4 CJK 以下视为碎片
cjk = [len(re.findall(r'[一-龥]', s)) for s in sents]
if not cjk:
    print('无可判定正文句子'); raise SystemExit
longs = [c for c in cjk if c > 60]
print(f'句子数={len(cjk)} 中位CJK={int(st.median(cjk))} 最长CJK={max(cjk)} '
      f'超长句(>60CJK)={len(longs)} 占比={len(longs)*100//len(cjk)}%')
PY
```

输出直接给出**超长句占比**，对齐 §3.5 阈值表的 `<10%` 判据，不用自己再算一遍。

### 3.4 段落结构：一段一意

```bash
python3 - <<'PY'
import re
FENCE = chr(96) * 3
raw = open('draft.md', encoding='utf-8').read()
raw = re.sub(FENCE + r'.*?' + FENCE, '', raw, flags=re.S)
line_no, paras, cur, start = 0, [], [], 1
for line in raw.split('\n'):
    line_no += 1
    if line.strip():
        if not cur: start = line_no
        cur.append(line)
    elif cur:
        paras.append((start, '\n'.join(cur))); cur = []
if cur: paras.append((start, '\n'.join(cur)))
for ln, p in paras:
    if p.lstrip().startswith(('#', '>', '|')): continue      # 跳过标题/引用/表格块
    p = re.sub(r'!\[[^]]*\]\([^)]*\)', '', p)
    if len(re.findall(r'[一-龥]', p)) < 8: continue           # 跳过图片/链接行
    n = len([s for s in re.split(r'[。！？]', p) if s.strip()])
    print(f'L{ln}: {n}句' + ('  ⚠ >5句/段，拆段' if n > 5 else ''))
PY
```

一段超过 5 句，通常塞了多个论点 → 拆段，每段只讲一件事。

> 输出用**行号**而非"段 N"：把标题行、图片行也算作段落时，"段 7" 对不上编辑器里的任何位置，
> 拿到告警还得回头数一遍。行号可以直接跳过去改。

### 3.5 篇幅体检

```bash
wc -m draft.md   # 中文字符数
wc -w draft.md   # 英文词数
```

**判读阈值表（对照 §4 清单）**：

| 指标 | 健康区间 | 越界处置 |
|------|----------|----------|
| 句子中位 CJK | ≤ 40 | >40 → 拆长句 |
| 超长句(>60 CJK)占比 | < 10% | 超限 → 强制断句 |
| 注水词命中 | 0 | >0 → 逐条删 |
| 被动句命中 | 0 | >0 → 转主动 |
| 段落句子数 | 2–5 | >5 → 拆段 |

### 3.6 这些命令查不到什么（别把绿灯当合格）

| 命令 | 抓得到 | 抓不到 | 补救 |
|------|--------|--------|------|
| §3.1 注水词 | 固定词表内的表达 | 词表外的新套话、整段废话 | 词表按自己的口头禅扩充 |
| §3.2 被动语态 | `被/由` + 动词表 | 无标记被动（"问题得到解决"）、英文被动 | 人工过一遍动词是谁做的 |
| §3.3 句长 | 中文句长分布 | 纯英文稿（CJK 计数为 0 → 全被过滤） | 英文稿改用 `wc -w` 加人工 |
| §3.4 段落 | 句数超限 | 一段里逻辑跳跃但只有 3 句 | 逻辑连贯性只能人读 |
| §3.5 篇幅 | 字符/词数 | 内容是否值这个篇幅 | 对照 `content-writer` 字数分档 |

**共同盲区**：全部命令只看**表层形式**，不看论点是否成立、证据是否可信、结论是否有信息增益。
形式项零告警只说明"没有明显硬伤"，不等于文章好。信息增益判断走
[seo-content-strategy 策略层](seo-content-strategy.md) §2，观点与调性由人拍板。

## 4. 编辑清单（量化版）

- [ ] 每段一个核心意思，无冗余（段落 ≤5 句，见 §3.4）
- [ ] 逻辑衔接顺畅（读者不卡壳）
- [ ] 术语已解释或链接
- [ ] 长短句交替，节奏不单调
- [ ] 行动指引明确（读完知道做什么）
- [ ] **注水词 = 0**（§3.1 命令零输出）
- [ ] **被动句 = 0**（§3.2 命令零输出）
- [ ] **句子中位长度 ≤ 40 CJK**（§3.3 指标）
- [ ] 标题层级不跳级（H2 下直接 H4 算跳级）

> 前 5 项是"读着顺"的软判据；后 4 项是 §3 命令可硬验证的量化判据。编辑以量化项为准，软判据为辅。

## 5. 常见文体要点

| 文体 | 重点 |
|------|------|
| 短文案 | 一个主张 + 一个 CTA，字字算 ROI |
| 技术文章 | 问题→方案→证据，可复现 |
| 长文博客 | 信息增益 + 结构清晰 + 内链 |

**落地映射**（本篇定文体要点 → 子技能出具体产出）：短文案 → [copywriter 子技能](../skills/copywriter/SKILL.md)（PAS/AIDA/BAB 框架）；
技术文章 → [technical-writer 子技能](../skills/technical-writer/SKILL.md)（7 阶段全流程 + 8 种内容类型模板）；
长文博客 → [content-writer 子技能](../skills/content-writer/SKILL.md)（QAE 模式 + 字数分档）；发布前验收 → [seo-checker 技术层](../skills/seo-checker/SKILL.md)。
本流程篇不复制这些框架内容，只负责"什么时候用哪一个 + 写完怎么体检"。

## 6. 常见坑

- **起草即编辑**：边写边改，进度龟速且打断心流。
- **信息密度低**：注水凑字数，读者流失。
- **标题敷衍**：好内容被烂标题埋没。
- **无行动指引**：读完无下文，转化归零。
- **文体误判**：把长文当短文案写 → 结构缺失、信息增益为零；按 §2 决策树先分流。
- **把润色排在结构前面**：串行逗号这类 polish 会掩盖结构问题——先修 CRITICAL（结构/清晰度），再抠 MEDIUM 细节。
- **被要求"审"时却重写**：先报 findings + 建议改法，除非对方说"直接改"，否则只评不改。
- **体检命令没在真稿上验过就信它**：正则和切句逻辑很容易"看起来对、实际全绿"。新增或改动
  §3 命令后，先拿一份**故意写坏的样稿**（塞注水词、被动句、超长句、6 句大段、缺 alt 图片）跑一遍，
  确认每条都能被抓出来，再拿它验真稿。参见 §3.6 的盲区表。

## 7. 边界声明（别重复劳动）

本篇是**流程 / 方法论层**：通用流程、流程选择决策树、写作体检命令、量化编辑清单。

具体产出框架由子技能承担，本篇不复制：

- [copywriter 子技能](../skills/copywriter/SKILL.md) — 6 种标题公式、PAS/AIDA/BAB
- [technical-writer 子技能](../skills/technical-writer/SKILL.md) — 10 种标题钩子、7 阶段、8 种模板
- [content-writer 子技能](../skills/content-writer/SKILL.md) — QAE 模式、字数分档
- [seo-checker 技术层](../skills/seo-checker/SKILL.md) — 发布前 11 项 Pass/Fail 技术验收
- [seo-content-strategy 策略层](seo-content-strategy.md) — SEO 策略层（意图对齐 / 信息增益 / 内链集群）

顺序：先过本篇流程与体检 → 再跑 seo-content-strategy 策略层 → 最后 seo-checker 技术层。三层各管一段，不重叠。
