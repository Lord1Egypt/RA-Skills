---
name: release-gate-audit
description: "发布前放行门禁：判定一个产物能否公开发布。与常规密钥扫描器的根本区别是判定对象——它以 git 已追踪内容 + 全部提交历史构成的「公开面」为准，而不是 ls 看到的工作目录，因此既不会把本地文件误报成泄露，也不会漏掉当前已删除但仍存在于旧 commit 中的凭证。四类威胁分离处置（凭证需吊销 / 雇主内部信息需泛化 / PII 兼可移植性缺陷 / 本地专属产物需停止追踪），并提供整改闭环的机器验证（前后报告对比 + 历史残留核查 + 强制吊销清单），避免『我觉得修好了』。内部词表一律外部注入，工具自身可开源。适用场景：开源仓库首次公开、分享 skill/文章/demo/slide、代码外发、合规审查、发版前放行、以及排查『内部信息是否泄露到公开产物』。"
description_zh: 发布前放行门禁审查
description_en: Pre-release publish gate audit
license: Apache-2.0
---

# Release Gate Audit — 发布前放行门禁

## 这个Skill 解决什么问题

发布是不可逆的。凭证泄露还能吊销，但内网域名、组织架构、同事姓名一旦公开就永久公开
——而且通常在几分钟内就进了爬虫。

常规密钥扫描器解决的是「**代码里有没有密钥**」。本 Skill 解决的是
「**这个产物现在能不能发出去**」。两者差一层，而这一层最容易出事。

### 与常规扫描器的关键区别：判定对象是「公开面」

对一个 git 仓库来说，别人真正能看到的是：

1. **被 git 追踪的文件** —— 未追踪 / 已 gitignore 的本地文件不算
2. **全部提交历史** —— 当前删掉了，旧 commit 里依然人人可clone

这与 `ls` 看到的内容差别极大。只扫工作目录会**同时犯两种错**：

| 错误 | 后果 |
|------|------|
| 把本地文件（agent 状态、编辑器配置、草稿）报成泄露 | 告警噪音 → 团队整体忽略扫描结果 |
|漏掉「当前已删除但仍在历史里」的凭证 | **最典型的真实事故形态被判为"干净"** |

实测对比（同一个仓库、同一套规则）：

```
只扫工作树   → 未发现任何命中，裁决"可发布"      ←漏检
公开面判定   → 4 项 P0（历史中的 PAT / 真密码连接串 / 内网域名）
```

## 适用场景

出现以下情况时使用本 Skill：

- 准备把仓库开源、首次公开推送
- 要分享 skill / 文章 / demo / slide / 截图录屏到外部平台
- 代码需要外发给客户、合作方、供应商
- 发版前的放行检查、合规审查
- 询问「有没有敏感信息」「会不会泄露内部信息」「能不能公开」
- 排查「内部信息是否已经泄露到公开产物里」
- 整改之后需要**证明**确实修好了

## 运行要求：零依赖，独立可用

| 项目 | 要求 |
|------|------|
| Python | 3.9+，**只用标准库**（argparse / json / os / re / subprocess / sys / dataclasses / pathlib） |
| 外部包 | **无**，不需要 pip install |
| 其他 Skill | **无**，不依赖任何其他 Skill |
| git | 需要 `git` 命令用于公开面判定；非 git 目录会自动退化为目录扫描 |

装上就能用。下文提到的 `secret-scanner` 是**可选增强**，不装也不影响任何功能。

## 与 secret-scanner 的关系：可选互补，非依赖

如果你的环境里恰好也装了 `secret-scanner`，两者可以互补——但**本 Skill 不依赖它**，
单独使用功能完整。

| 维度 | secret-scanner | release-gate-audit（本 Skill） |
|------|----------------|------------------------------|
| 定位 | 日常仓库密钥扫描 | 发布前放行裁决 |
| 判定对象 | 工作目录文件 | git 公开面（已追踪 + 全历史） |
| 模式库 | 65+ 种，覆盖极广 | 通用凭证格式 + 外部注入内部词 |
| 威胁分类 | 按服务厂商分类 | 按**处置方式**分四类 |
| 整改验证 | 建议人工重扫 | 机器对比 + 吊销清单 + 历史残留核查 |
| 输出 | 分级报告 | **放行/阻断裁决** |

### 单独使用（默认，推荐从这里开始）

```bash
# 一条命令完成公开面判定
python3 scripts/release_gate.py <repo> --org-config <你的词表>

# 整改后做机器验证
python3 scripts/release_gate.py <repo> --format json > after.json
python3 scripts/verify_remediation.py before.json after.json
```

### 若已装 secret-scanner，可加一步广谱扫描（可选）

它的模式库更全（65+ 种，覆盖大量具体服务商），适合先拉一遍最大范围的线索，
再用本 Skill 判断哪些真的会公开出去：

```bash
# 可选前置：更广的模式覆盖
python3 <secret-scanner 路径>/scripts/secret_scanner.py <repo> --severity LOW

# 然后照常做公开面裁决
python3 scripts/release_gate.py <repo> --org-config <你的词表>
```

> 不装 secret-scanner 时，若担心自研凭证格式漏检，用 `--org-config`
> 补充自定义词条即可达到同等效果。

## 快速开始

### 一、公开面判定（默认模式）

```bash
python3 scripts/release_gate.py <目标仓库>
```

默认扫描 git 已追踪文件 + 全部提交历史，输出放行裁决。

### 二、注入雇主内部词表

内部词表**必须外部注入**，脚本里不含任何雇主特定内容（详见下方「设计约束」）：

```bash
# 方式一：配置文件（推荐，参考 assets/org-terms.txt 模板）
python3 scripts/release_gate.py <目标仓库> --org-config assets/org-terms.txt

# 方式二：环境变量（临时使用，逗号分隔）
ORG_PATTERNS="corp.example.com,InternalWiki,ProjectCodename" \
  python3 scripts/release_gate.py <目标仓库>
```

#### 词条语法：默认字面匹配，可选前缀改变行为

| 写法 | 行为 | 处置动作 |
|------|------|---------|
| `corp.example.com` | 字面匹配（默认，忽略大小写） |泛化/移除 |
| `cred:MYCO-` | 归类为**凭证** | **吊销并轮换** |
| `regex:MYCO-[A-Za-z0-9]{16}` | 按正则匹配 | 泛化/移除 |
| `cred+regex:INT-[0-9a-f]{32}` | 正则 + 凭证 | **吊销并轮换** |

`cred:` 前缀很重要：自研token 若只归为「内部标识」，处置建议会是"泛化"，
但凭证的正确处置是**吊销**——分类错了，修复动作就错了。

含冒号的字面内容不会被误判为前缀（`https://x.com`、`host:8080` 均按字面处理）。
无效正则会被跳过并在stderr 提示，不会中断扫描。

> ⚠️ 内部词表文件本身就是一份敏感清单，**不要提交进仓库**，请加入 `.gitignore`。

### 三、其他模式

```bash
# 只扫工作目录（含未追踪文件）——排查本地状态时用
python3 scripts/release_gate.py <目标> --mode worktree

# 只扫提交历史——专门排查历史残留
python3 scripts/release_gate.py <目标> --mode history

# 三者全跑
python3 scripts/release_gate.py <目标> --mode all

# 机器可读输出（用于 CI 或整改对比）
python3 scripts/release_gate.py <目标> --format json > report.json

# 调整报告级别（默认 P1）
python3 scripts/release_gate.py <目标> --severity P0   # 只看阻断项
python3 scripts/release_gate.py <目标> --severity P2   # 看全部
```

退出码：`0` 可放行 · `1` 存在公开面 P0 · `2` 用法错误

**自动排除的文件**（无需配置，也不依赖目标仓库的 `.gitignore`）：

| 排除对象 | 原因 |
|---------|------|
| 二进制与媒体文件、`node_modules`/`dist`/`.venv` 等构建目录 | 无文本可扫，纯噪音 |
| `--baseline` 与 `--org-config` 指向的文件 | 它们记录着豁免片段与内部词，自己必然命中，形成清不掉的循环 |
| 本工具产出的中间报告（`before.json` / `after.json` / `*.report.json`） | 报告里复述了命中原文，会把同一条泄露重复报一遍（工作树与历史两处都已处理） |

### 四、整改闭环验证

整改最容易失败的不是「没找到」，而是「以为修好了」。

```bash
# 1. 整改前留存基线
python3 scripts/release_gate.py <目标> --format json > before.json

# 2. 完成整改
# 3. 再跑一次
python3 scripts/release_gate.py <目标> --format json > after.json

# 4. 机器验证整改效果
python3 scripts/verify_remediation.py before.json after.json
```

验证器会给出：**已消除 / 仍存在 / 新引入** 三种状态，并强制产出**吊销清单**。

实测效果——对一次「只删当前文件、没清历史」的假修复：

```
已消除 : 1← 真修好的部分被认可
仍存在 : 5
未消除的公开面 P0（3 项）
  · [history] commit:0338864GitHub 细粒度 PAT
必须吊销的凭证清单（2 项）
  [ ] GitHub 细粒度 PAT （出现于 commit:0338864）
裁决：整改未达标
```

## 完整工作流

### 阶段一：界定范围

1. 明确哪些产物会真的公开。**不要只查用户提到的那一个**——如果要分享一个
   skill，接下来大概率会分享其他的，应当扫**整类**。
2. 对 git 仓库，先分清公开面与本地噪音：

```bash
git ls-files | wc -l                # 公开面文件数
git status --porcelain | wc -l           # 本地噪音，不属于公开面
```

### 阶段二：自动扫描

运行 `release_gate.py`，得到分类分级的线索清单。这一步已经足够完整。
（可选：若环境里装了 `secret-scanner`，可额外跑一遍拿到更广的模式覆盖。）

### 阶段三：逐条判定（**不可跳过**）

自动扫描给的是**线索**，不是结论。加载 `references/false-positive-playbook.md`，
按「判定四问」逐条过：

1. 这个值是真的吗？（占位符特征 / 厂商示例串 / 变量插值）
2. 它在什么位置？（测试与示例路径 vs 生产代码 vs git 历史）
3. 暴露面有多大？（公开仓库 / 私有仓库 / 未追踪）
4. 凭证现在还有效吗？（去控制台查——**有效就立刻吊销，不要先讨论**）

工具已自动标注两类误报信号（内容特征 + 路径性质），输出中带
`<- 疑似误报，需读上下文`。**标注只是提示，判定权在人。**

### 阶段四：按类别处置

加载 `references/threat-categories.md`，按类别执行：

| 类别 | 处置 |
|------|------|
| CREDENTIAL | **① 吊销 → ② 轮换 → ③ 删代码 → ④ 清历史**，顺序不能颠倒 |
| ORG_INTERNAL | 泛化为通用描述（保留结论，去掉标识）或移除 |
| PII | 改相对路径 / 环境变量 / 裸包名（同时修掉可移植性缺陷） |
| LOCAL_ONLY | `.gitignore` + `git rm --cached` 停止追踪 |

### 阶段五：闭环验证与留痕

1. 跑 `verify_remediation.py` 做机器验证
2. 确认吊销清单逐项完成
3. 报告里**逐条留痕**——列出每条命中的判定与依据

> 「0 findings」且无证据的报告是无效的。
> 「6 项 P0，逐条核实全部为测试固定装置，附每条依据」才是一次审计。

## 设计约束：审查工具必须自己先过审

`scripts/release_gate.py` 里**不含任何雇主特定内容**——没有内网域名、
没有内部平台名、没有组织标识。全部通过 `--org-config` 或`ORG_PATTERNS` 注入。

原因很直接：**一旦把公司内部词硬编码进代码，这个工具本身就带着内部信息，
无法作为开源产物发布。** 这是本 Skill 的一条硬性设计约束，也是它能被公开分享的前提。

同理，`assets/org-terms.txt` 只是**模板**，里面全是 `example.com` 占位符。
真实词表请本地维护并加入 `.gitignore`。

## 参考资料加载时机

| 文件 | 何时加载 |
|------|---------|
| `references/threat-categories.md` | 处置阶段；需要解释某类问题该怎么修时 |
| `references/false-positive-playbook.md` | 判定阶段；每次有P0/P1 命中时**必读** |
| `assets/org-terms.txt` | 首次为某个组织配置内部词表时（模板，含占位符） |
| `assets/self-audit-baseline.json` | 参考基线文件的写法；这是本 Skill 自审的真实基线 |

> `assets/self-audit-baseline.json` 是一个可直接参考的范例：本 Skill 的文档里
> 大量引用了「什么是误报」的示例串（如 AWS 官方示例 Key），扫描自身时会全部命中。
> 逐条判定后写入基线，并在文件里记录了判定理由与日期——这就是基线该有的样子。

## 铁律

1. **正则只能高召回，工具不代替你下结论。** 逐条读上下文是必须的步骤。
2. **删凭证 ≠ 吊销凭证。** 泄露出去的那把钥匙不会因为你删了代码而失效。
3. **工作树 ≠ 公开面。** 用 `git ls-files` / `git log --all -p` 判断，别靠 `ls`。
4. **历史里的等于公开的。** 当前文件干净不代表仓库干净。
5. **不要通过放宽规则来"通过"。** 确认为误报的写基线，逐条问责；
   放宽正则是批量免责，会让同类真问题从此隐形。
6. **不要过度脱敏。** 去掉可定位的标识，保留工程结论——否则产物失去价值。
7. **公开产品名不是秘密**，内部专用系统才是。判定前先确认它到底是哪种。
8. **文件名只能降低怀疑度，不能免检。** `.env.example` 里手滑填真值极其常见。

## 局限与边界

- 基于正则，**不做熵分析**。自研凭证格式用 `--org-config` 的
  `cred:` / `cred+regex:` 词条即可覆盖（大多数内部 token 都有固定前缀）；
  若环境里另有更广模式库的扫描器（如 `secret-scanner`），也可作为补充手段。
- 历史扫描只覆盖**本地已有的提交**。fork、PR、CI 缓存、镜像仓库中的副本
  不在检测范围内——这也是「必须吊销而非仅清理历史」的原因。
- 二进制文件、图片、截图、录屏中的敏感信息**无法检测**，需人工检查
  （架构图水印、浏览器地址栏、终端提示符是高频泄露点）。
- 非 git 目录会退化为普通目录扫描，此时无法区分公开面。
