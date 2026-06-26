# Changelog | 更新日志

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 规范。

---

## [v0.8.2] - 2026-05-19

### 🐛 修复：SKILL.md 世应生克规则缺失导致 AI 分析错误

跨平台 agent（WorkBuddy/ClawHub/SkillHub）在分析世应关系时产生"木克水"误判，
根因是 SKILL.md 缺少世应生克计算方法的明确指令。

#### Fixed / 修复

- **`SKILL.md` Layer 5 新增世应生克规则**：
  - 明确要求：世应生克必须使用**地支五行**计算，不能用六亲标签
  - 附带正确/错误示例对比
  - 原理说明：六亲(宫位维度) ≠ 世应生克(地支维度)
  - 新增推演后验证项 [世应生克检查]

#### 错误重现

```
用户数据： 世爻=官鬼卯木(木), 应爻=妻财子水(水)
AI 误判： "官鬼克妻财" → "木克水" ❌（六亲标签混用）
正确判断： 子水(水)生卯木(木) → "应生世" ✅（地支五行）
```

---

## [v0.8.1] - 2026-05-19

### 🐛 修复：六神排列算法（日干起法）

六神排列算法从错误的"日支起法"修正为正确的"日干起法"。

#### Fixed / 修复

- **`scripts/liuyao.py` 六神排列日干修正**：
  - 原算法：`ZHI_ORDER.index(day_branch) % 6`（按日支起六神，❌ 错误）
  - 新算法：`GAN_TO_LIUSHOU[day_stem]`（按日干起六神，✅ 正确）
  - 规则对照：甲乙→青龙、丙丁→朱雀、戊→勾陈、己→螣蛇、庚辛→白虎、壬癸→玄武

#### Changed / 变更

- **`scripts/liuyao.py`**：新增 `GAN_TO_LIUSHOU` 映射字典
- 调用 `_get_liushou_order()` 时传入 `day_stem` 而非 `day_branch`

---

## [v0.8.0] - 2026-05-19

### 🏗️ 架构重构：放弃 PyArmor 混淆，完全开源

本版本彻底删除 PyArmor 混淆保护层，恢复所有核心算法为明文 Python。
解决自 v0.6.0 累积的运行时分发问题，实现全平台零障碍分发。

#### Removed / 删除

- **`scripts/protected/`** — PyArmor 加密保护层，整目录删除
- **`pyarmor_runtime_000000/`** — PyArmor 运行时的二进制文件，整目录删除

#### Added / 新增

- **`scripts/wangshuai_score.py`** — 旺衰评分引擎（明文开源）
  - 从原内联代码抽取为独立模块
  - 月建旺相休囚死 + 日建七效应（临/生/克/冲/合/刑/害）复合评分
  - 帝旺、墓库、回头生克、绝地等辅助判断

#### Changed / 变更

- **`scripts/liuyao.py`**：导入路径从 `protected.wangshuai_score` 改为 `wangshuai_score`
- **`scripts/xiang_query.py`**：恢复完整实现（原为薄包装器委托给 protected/xiang_engine.py）
- **`SKILL.md`**：更新技术架构图，移除 protected 保护层
- **`.gitignore`**：移除 `*.pyd` 排除规则（不再需要）

#### Fixed / 修复

- **PyArmor 运行时分发缺陷**（自 v0.6.0 累积）：
  - `pyarmor_runtime.pyd` 因 `.gitignore` 排除从未被提交到仓库
  - v0.6.0 和 v0.7.0 的所有安装均缺失运行时文件，排盘功能完全不可用
  - 影响 ClawHub 538 次安装

#### 全平台分发

- ✅ **GitHub**：纯文本，无二进制文件限制
- ✅ **ClawHub**：纯文本包，安装即用
- ✅ **SkillHub**：纯文本，支持完整功能

---

## [v0.7.0] - 2026-05-19

### 🔧 排盘核心全面修复：纳甲/六亲/卦宫/编码体系

六爻排盘系统存在自最初版本以来的多项基础数据与算法错误，导致排盘结果与正统京房纳甲体系不符。
本版本对排盘核心进行了系统性审查和全面修复，经验证水地比→地水师排盘结果与标准排盘图片完全一致。

#### Fixed / 修复

- **`scripts/liuyao.py` TRIGRAM_TO_NAJIA 映射错误（6/8 错）**：
  - 原6个八卦→卦宫映射与 `_hex_to_binary` 输出约定不一致
  - 修正为：`(1,1,1)→乾宫, (1,1,0)→兑宫, (1,0,1)→离宫, (1,0,0)→震宫, (0,1,1)→巽宫, (0,1,0)→坎宫, (0,0,1)→艮宫, (0,0,0)→坤宫`

- **`scripts/liuyao.py` HEXAGRAM_EARTHLY_BRANCH 纳甲数据完全错误**：
  - 原表仅12个地支机械分配到8宫，不符合京房纳甲体系
  - 替换为 `NAJIA_INNER`（内卦纳甲）+ `NAJIA_OUTER`（外卦纳甲），按上下卦各自八纯卦纳甲

- **`scripts/liuyao.py` 六亲以世爻五行为本（错误）→ 以卦宫五行为本（正确）**：
  - 新增 `PALACE_WUXING` 字典（乾宫金、坤宫土、震宫木、巽宫木、坎宫水、离宫火、艮宫土、兑宫金）
  - 六亲计算统一使用 `palace_wx`（卦宫五行）而非 `shi_wx`（世爻五行）

- **`scripts/liuyao.py` 变卦六亲以变卦世爻五行为本（错误）→ 以本卦卦宫五行为本（正确）**：
  - 变卦六亲同样以本卦卦宫五行为"我"（传统六爻标准排法）

- **`scripts/liuyao.py` HEXAGRAMS 64卦数据重新生成**：
  - 按八宫世系（本宫→一世→二世→三世→四世→五世→游魂→归魂）程序化生成
  - 修正卦名、世应位置、卦类型
  - 修正 `_hex_to_binary` 输出与 HEXAGRAMS key 约定一致（1=阳, 0=阴）

- **`scripts/liuyao.py` _hex_to_binary 阴阳方向与 HEXAGRAMS key 不一致**：
  - 修正输出约定为 `1 if x in [2,3] else 0`（1=阳, 0=阴），与 HEXAGRAMS key 一致

- **`scripts/liuyao.py` _init_hexagram_map 多项错误**：
  - 卦序错误：`up_bin + down_bin` → 修正为 `down_bin + up_bin`（从初爻到上爻）
  - 巽卦硬编码：`[0,0,1]` → 修正为 `[0,1,1]`
  - 改为直接引用 `TRIGRAM_BINARY`，消除硬编码

- **`scripts/liuyao.py` deduce_moving_lines 索引方向混乱**：
  - 原返回 `5-i`（初=5,上=0）→ 修正为返回 `i`（初=0,上=5）

- **`scripts/liuyao.py` _generate_changed_hexagram 变爻方向反转**：
  - fallback 分支中 `3→2, 4→1` → 修正为 `3→1（老阳→少阴）, 4→2（老阴→少阳）`

- **`scripts/liuyao.py` line_names/line_symbols 标签与符号错误**：
  - `{3:"纯阳",4:"纯阴"}` → 修正为 `{3:"老阳",4:"老阴"}`
  - 动爻符号修正：`3:"----- ○", 4:"-- -- ×"`

- **`scripts/meihua.py` BA_GUA 坤卦编号 0 导致卦名查找失败**：
  - `{0:"坤"}` → `{8:"坤"}`，避免模运算结果0导致 `_GUA_HU` 查表失败
  - `compute_meihua` 中 `% 8` 结果为0时映射到8（坤）

- **`scripts/qigua.py` meihua_date_qigua 动爻索引计算错误**：
  - `idx = 6 - change_line` → 修正为 `idx = change_line - 1`

- **`scripts/qigua.py` COIN_TO_LINE 注释补充**：
  - 明确标注每个结果的阴阳爻类型

- **`scripts/liuyao.py` arrange_hexagram_by_name 动爻索引映射错误**：
  - `enc_idx = 5 - idx` → 修正为 `enc_idx = idx`

#### Changed / 变更

- 编码体系统一化：`1=少阴(阴爻静), 2=少阳(阳爻静), 3=老阳(阳爻动), 4=老阴(阴爻动)`
- `_hex_to_binary` 输出统一：`1=阳, 0=阴`
- `binary_to_hexagram_encoding` 保持一致：`1(阳)→2(少阳), 0(阴)→1(少阴)`

---

## [v0.6.0] - 2026-05-18

### 🛡️ 核心算法保护：pyarmor 混淆部署

独创算法（类象展开引擎 xiang_engine、旺衰精算 wangshuai_score）从纯文本 Python 转为 pyarmor 运行时加密分发。

#### Added / 新增

- **`scripts/protected/` 保护层**：
  - `xiang_engine.py` — 类象知识库查询引擎（类象分类体系、语境匹配权重、维度映射）
  - `wangshuai_score.py` — 旺衰精算引擎（月建旺相休囚死 + 日建七效应复合评分）
  - 以上两个模块经 **pyarmor 加密混淆**，运行时自动解密，源码不可读

- **`pyarmor_runtime_000000/`** — pyarmor 运行时支持库，确保加密模块正常加载

#### Changed / 变更

- **`scripts/xiang_query.py`**：改为薄包装器，核心实现委托给 `protected/xiang_engine.py`
- **`scripts/liuyao.py`**：旺衰评分函数（`_get_seasonal_status`、`_calculate_yao_strength`、`_batch_calculate_strength`）移至 `protected/wangshuai_score.py`，原文件改为 import 引用
- **`scripts/__init__.py`**：新增包初始化文件

#### Security / 安全

- 独创算法从 MIT 开源 → pyarmor 加密分发，提高复制门槛
- 用户本地执行、零网络依赖、零额外安装步骤
- 保护层与原文件解耦：开源层（MIT）与保护层（加密）清晰分离

---

## [v0.5.0] - 2026-05-18

### 🔄 架构回滚：核心算法从远程 API 恢复为本地执行

v0.4.0 尝试的"IP保护分层重构"（核心算法转移至远程 API）导致技能在远程服务不可用时完全瘫痪。
本版本回滚到 v0.3.x 的本地执行架构，远程仅作为可选增强层。

#### Changed / 变更

- **架构恢复**：7 个核心脚本全部从 `.gitignore` 移除，恢复 Git 追踪
  - `scripts/calendar.py` — 历法精算
  - `scripts/meihua.py` — 梅花易数
  - `scripts/liuyao.py` — 六爻纳甲
  - `scripts/qigua.py` — 起卦引擎（含前一版本的 bug 修复）
  - `scripts/liuren.py` — 大六壬
  - `scripts/qimen.py` — 奇门遁甲
  - `scripts/xiang_query.py` — 类象查询引擎
- **删除 `API.md`**：远程 API 文档已移除（API 服务不再作为核心依赖）
- **`requirements.txt`**：恢复 Git 追踪，依赖包（swisseph, lunar-python）在本地可用
- **LICENSE 恢复**：从 MIT-0 恢复为 MIT License
- **SKILL.md 全面更新**：所有 `/api/` 引用改回本地脚本调用，架构图更新为 `Skill + Python 脚本层`

#### Fixed / 修复

- **根本性故障恢复**：远程 API 不可用时技能 100% 可用（本地执行，零依赖网络）
- **`scripts/qigua.py` 两处 Bug 已在 v0.4.1 基础上保留**：
  - `TRIGRAM_BINARY` 中巽卦映射 `[0,0,1]` → `[0,1,1]`
  - `_gua_name_to_encoding` 移除多余的 `reversed()` 调用

---

## [v0.4.1] - 2026-05-17

### 🔥 Hotfix：修复 ClawHub 发布版本无法使用的问题

#### Fixed / 修复

- **`scripts/qigua.py` 编码映射错误**：
  - `TRIGRAM_BINARY` 中 `巽` 的二进制值从错误的 `[0,0,1]` 修正为 `[0,1,1]`
  - `_gua_name_to_encoding()` 中移除了对 `TRIGRAM_BINARY` 的 `reversed()` 调用（二进制已经是初→上顺序，不应反转）
  - **以上两处 bug 导致梅花起卦的卦象编码全部偏移，六爻排盘结果错误**
- **删除 `skill/SKILL.MD`（文件名大写错误）**：该文件导致 ClawHub 安装时 skill 加载失败，已删除整个 `skill/` 目录
- **`_meta.json` 版本号（0.2.3）与 `config.json`（0.3.0）不一致**：统一修正为 0.4.1

#### Changed / 变更

- **ClawHub 发布包结构修正**：移除冗余的 `skill/` 目录，确保 `SKILL.md` 在根目录且大小写正确

---

## [v0.2.6] - 2026-05-17

### 🎯 文档优化 + 多平台兼容声明

#### Added / 新增

- **config.json**: triggers 改为 array 格式（兼容 ClawHub 解析器）；新增 description_fr、description_es
- **README.md**: 全面重写，面向多平台非专业用户
- **SKILL.md**: 新增 §14 新人引导与起卦方式说明
- **SKILL.md frontmatter**: 更新多语言 triggers 和描述

#### Changed / 变更

- **README.md** 重构结构：
  - 🎯 适用范围：明确列出 WorkBuddy/OpenClaw/Hermes/QClaw/ArcLaw 及自媒体平台 AI Agent
  - ⚡ 30 秒快速安装：ClawHub 链接安装 + CLI 命令
  - 🗣️ 使用示例：完整对话流程
  - ⚠️ 起卦方式说明：日期起卦 vs 人工起卦差异（进阶功能支持范围）
  - 🖥️ 专业用户配置：环境要求、本地安装、项目结构
- **SKILL.md** 新增：
  - §14.1 新人引导规则：首次使用自动引导话术
  - §14.2 起卦推演规则：两种方式支持的功能范围
  - §14.3 输入检测逻辑：自动判断起卦方式
  - §14.4 多平台兼容说明

---

## [v0.2.0] - 2026-05-16

### 🎉 重大更新：Phase 1 全部完成

#### Added / 新增

**核心算法脚本（6 个，全部完成）**

- **`scripts/calendar.py`** — 干支历法精算模块
  - 基于 Swiss Ephemeris 的高精度天文计算
  - 输出：年柱/月柱/日柱/时柱（八字）、节气信息、旬空、月建
  - 时区：默认 Asia/Shanghai

- **`scripts/meihua.py`** — 梅花易数起卦模块
  - 函数 `compute_meihua(year, month, day, hour)`
  - 输出：本卦/上卦/下卦/体卦/用卦/变爻/变卦/互卦/错卦/综卦
  - 辅助函数 `gua_to_lines()` 将卦名转为六爻数字编码，供六爻模块使用

- **`scripts/liuyao.py`** — 六爻纳甲排盘模块
  - 函数 `arrange_hexagram(六爻, datetime, 事项)`
  - 输出：本卦（宫位/世应爻/六亲/地支/五行/六兽）、变卦、旬空、月建
  - 纳甲规则：上卦取本宫纳甲，下卦取自卦纳甲（京房规则）
  - 旺衰算法：月建用旺相休囚死（季节旺衰），日建用七效应（临/生/克/冲/合/刑/害）

- **`scripts/liuren.py`** — 大六壬排盘模块
  - 天地盘/四课/三传/贵人计算
  - 用户触发模式（基础推演完成后询问是否展开）

- **`scripts/qimen.py`** — 奇门遁甲排盘模块
  - 地盘/天盘/八门/九星/八神五层排盘
  - 用户触发模式

- **`scripts/xiang_query.py`** — 类象查询 SDK（★ 核心新增）
  - `query(symbol, context?, dimension?)` — 精确查询，支持语境 fallback 到 general
  - `expand_full(symbol, context?)` — 人类可读的多行展开文本
  - `multi_query(symbols[], context?)` — 批量符号查询
  - `expand_for_context(symbols[], context)` — 批量合并展开
  - `get_wuxing_combo(symbols[])` — 多符号五行组合查询
  - `available_symbols()` / `available_categories()` — 元数据查询

**类象知识库（28 个 JSON 文件，6 大类别，全部完成）**

路径：`data/xiang/`

| 类别 | 文件数 | 包含符号 |
|------|--------|----------|
| `bagua/` | 8 | qian / kun / zhen / xun / kan / li / gen / dui |
| `liuqin/` | 5 | fumu / xiongdi / qicai / guangui / zisun |
| `liushen/` | 6 | qinglong / zhuque / gouchen / tengshe / baihu / xuanwu |
| `ganzhi/` | 2 | tiangan / dizhi |
| `wuxing/` | 1 | shengke |
| `guayao/` | 6 | liuhe / liuchong / sanhe / sanxing / liuhai / gong_guayao |

每个 JSON 文件结构（同构）：
```json
{
  "symbol": "乾",
  "category": "bagua",
  "trigram": "☰",
  "core_properties": ["健","阳","刚","上","圆","创始"],
  "wu_xing": "金",
  "contexts": {
    "general":      {"person":[...],"object":[...],"time":[...],"space":[...],"state":[...]},
    "career":       {"person":[...],"object":[...],"state":[...]},
    "health":       {"person":[...],"state":[...]},
    "relationship": {"person":[...],"state":[...]},
    "finance":      {"object":[...],"state":[...]}
  }
}
```

**★ 新增机制（SKILL.md v0.2.0）**

- **反馈引导系统**（§4）
  - 推演完成后主动询问用户帮助程度
  - 反馈以 JSONL 格式存入 `feedback/local_feedback.jsonl`
  - 每收到 5 条有效反馈自动触发 Prompt 优化

- **风格记忆系统**（§5）
  - 每次对话结束，若用户有反馈或偏好表达，写入 `MEMORY.md`
  - 连续 3 次同类型纠正 → 永久注册为偏好
  - 单次纠正 → 标记为"待验证"
  - 每 10 次推演后回顾风格记忆一致性

- **验证闭环**（§6）
  - 推演前：时间解析/卦象计算/事项语境 三检查
  - 象展开时：类象层次/关键象覆盖/象间一致性 三检查
  - 推演后：可能性覆盖/禁用语检查/启发提问/结束语 四检查

- **自我评估与修正**（§7）
  - 输出前对 5 个维度打分（准确性/丰富性/相关性/启发性/开放性，各 1-5 分）
  - 任一维度 < 3 分 → 重新生成该部分
  - 总分 < 18 分 → 回到 Layer 5 重新展开

#### Fixed / 修复

- **纳甲归属错误**：修复上卦/下卦纳甲混用问题，上卦取本宫纳甲，下卦取自卦纳甲（京房规则）
- **旺衰算法混淆**：修复月建旺衰混用日建生克的问题，月建完全通过旺相休囚死判断，日建独立计算七效应
- **旬空计算公式错误**：修复简化公式导致的偏差，改为基于 60 甲子循环位置的精确查找
- **五卦合参逻辑**：修复本卦/互卦/变卦/错卦/综卦在推演中的权重分配

#### Changed / 变更

- 更新 SKILL.md §3 工作流，Step 2-4 包含具体函数调用和 SDK API 说明
- 更新 SKILL.md §9 知识库结构，从占位描述更新为实际 28-JSON/6-类别布局
- 更新 SKILL.md §10 技术架构，标记全部脚本为 ✅ 完成
- 更新 README.md 安装命令：`gamma skill install sitiantai-xiangtuie`（待确认 CLI 命令正确性）

#### Technical Highlights / 技术亮点

- 月建旺衰：完全通过旺相休囚死判断，不混用生克
- 日建七效应：临 / 生 / 克 / 冲（散·暗动）/ 合 / 刑 / 害 独立计算
- 旬空精算：基于 60 甲子循环位置精确查找，非简化公式
- 京房纳甲：上卦/下卦纳甲分离，符合京房八宫规则
- 五卦合参：本卦 + 互卦 + 变卦 + 错卦 + 综卦 综合推演
- 类象五维：人(person) / 物(object) / 时(time) / 空(space) / 态(state) × 5 语境

---

## [v0.1.0] - 2026-05-14

### Added / 新增

**初始 Skill 框架**

- 四象合参（Four-Elephant Synthesis）架构设计
- 象推演（Xiang Tuiye）方法论：发散式符号推演 vs 收敛式吉凶判断
- Layer 分层架构设计（Layer 0-6）

**Layer 0-2 自动执行层**

- Layer 0：干支历法（自动执行）— 八字、节气、旬空、月建
- Layer 1：梅花易数（自动执行）— 时间起卦、体用判定、错综卦生成
- Layer 2：六爻纳甲（自动执行）— 本变卦、世应爻、六亲、六神、旺衰

**Layer 5-6 推演层**

- Layer 5：象展开（核心）— 对关键符号进行五维度语义展开
- Layer 6a：基础综合推演 — 按三传时间线组织 3~7 个可能性叙述

**辅助系统**

- 六壬/奇门改为用户触发模式（基础推演完成后询问）
- 最终输出结构化报告：卦象总览 / 象展开 / 可能性推演 / 补充视角 / 启发提问
- 结束语强制要求："以上是根据卦象展开的可能性推演，并非确定性结论……"

**禁用语与鼓励语规则（§8）**

- 🚫 严禁：一定、必然、大吉、大凶、宜、忌、应该、必须
- ✅ 鼓励：可能、或许、含有…之象、与…相呼应、启发式提问

**待完成（TODO）**

- 推理链与推理示例（后续深入讨论）
- 类象知识库建设计划执行

---

## [Unreleased] / 待发布

### Phase 2 规划（Skill + MCP）

- 将 Python 脚本升级为 MCP 工具，标准化接口
- 支持 OpenClaw MCP 直接调用（无需 Python 子进程）
- 推理链（Reasoning Chain）可视化输出
- 推理示例库（5 个典型场景）
- 类象知识库持续扩充（更多符号 + 更多语境）

---

## 许可证说明

| 部分 | 许可证 |
|------|----------|
| `scripts/`（算法代码） | MIT |
| `data/xiang/`（类象知识库） | CC BY-NC-SA 4.0 |
| `SKILL.md`（推理规则） | CC BY-NC-SA 4.0 |
