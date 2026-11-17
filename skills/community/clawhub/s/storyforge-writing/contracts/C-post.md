# C 类子契约 · 漫剧后期对接（storyforge-writing）

> 归属：C 制作后期。对应 StoryForge 生成管线的下游：把 B 类产出的
> Image/Video Prompt IR + 适配包，对接到达芬奇〔环境来源〕 MCP / 生成管线（Seedance/Runway/LTX）。
> 本文件是"交接约定"，不重复 B 类 IR 定义；引用 B-motion-drama.md 的 Prompt IR。
>
> ⚠️ **来源等级标注（v0.2.0 新增）**：下文「达芬奇〔环境来源〕 MCP 15 条铁律」「agent-change-safety」**不来自**
> StoryForge 源仓库 —— 在 `H:\storyforge-main` 全文检索"达芬奇〔环境来源〕" **0 命中**（`REV-20261005-015` #5）。
> 它们来自本 agent 自身环境/记忆资产，等级 = **`INFERRED`（环境内置约定）**，**不属于**声明的数据契约基线。
> 因此：凡涉及达芬奇的操作，**必须先在 `ai-memory` 中检索到对应条目再执行**；
> 检不到就停下问用户，不得凭本文件的行文当依据。

## 1. C 类职责边界

**C 类只做**：
- 接收 B 类（漫剧素材前期）的 **版本化 prompt 包 + 参考帧 + capability profile**
- 调用生成管线（Seedance/达芬奇〔环境来源〕 MCP 三服务器）产出图/视频/素材
- 生成结果回填媒资（blob + contentHash + 权利 + provider receipt）
- 剪辑/调色/混音/成片（达芬奇〔环境来源〕 MCP 15 条铁律范围内）
- 发布前质检（引用完整性、权利、hash、capability 通过门）

**C 类不做**（归 B 类）：
- 系列圣经/逐集剧本/分镜规划（那是前期创作）
- Prompt IR 的定义与稳定 key（B 类冻结）

## 2. 交接物（B → C，全部带版本 + hash）

| 交接物 | 来源（B 类） | C 类校验 |
|---|---|---|
| Image Prompt IR | B-motion-drama §3 | 字段完整、referenceAssetKeys 可解析 |
| Video Prompt IR | B-motion-drama §3 | provider-neutral，可编译到目标 adapter |
| 参考帧（start/key/end） | B §6 | 从已确认 shot + 精确物料版本编译 |
| 物料（7 类）+ 权利 + hash | B §2 | rights 声明齐全，blob 可解码 |
| capability profile（版本化） | B §3 | 超能力已拆分/降级/阻断，不静默忽略 |
| 来源 manifest + revision | B 生产链 | 来源未变，stale 检查通过 |

## 3. 生成管线对接（达芬奇〔环境来源〕 MCP / Seedance）

- **达芬奇操作**：遵守 ai-memory「达芬奇 MCP 15 条铁律」（**环境来源，非源仓库基线**）；多序列先与用户确认目标（agent-change-safety）
- **Seedance/Runway/LTX**：从 IR + 参考媒资 + capability profile **确定性编译**，不复用 B 类之外的供应商参数
- 生成结果**不回流**改写 B 类 prompt IR；只写媒资 + receipt
- 每次生成记录 provider receipt（provider/model/requestId/capabilitySnapshotHash）+ 权利 + contentHash

## 4. 完成门（两级，同 B 类成熟度，不建第二产品）

| 层级 | C 类职责 |
|---|---|
| `prompt-only` | 仅冻结 prompt 包，**不**触发生成（参考媒资未锁定时不得标 reference-ready） |
| `reference-ready` | 必需物料 + shot 参考帧已选、引用可解码、权利 + hash 完整、adapter 通过 capability profile → 才进入生成 |

## 5. 媒资与 Blob 纪律

- 图片/音频字节复用共享 Blob 基础设施；**语义 owner 不转移**给世界引擎/页漫/上层产品/供应商
- 一条媒资只能有**一种有效 owner**（release 或 session），不得同时归属
- 发布前冻结媒资；已发布媒资不可变

## 6. 生成后一致性

- 生成结果 = 媒资 + 证据（receipt/hash/权利），**不是** Canon 设定
- 不自动回写 B 类 Prompt IR / 世界引擎
- 超能力或引用缺失 → 阻断，不静默忽略（同 B §3）

## 7. 与 15 条铁律的引用（环境来源，须先检索）

达芬奇剪辑/调色/合成操作 → **先在 `ai-memory` 检索**「达芬奇 剪辑 调色 操作铁律」，逐条执行；
多序列/多项目先确认目标，不擅自切换（agent-change-safety 红线）。

**纪律**：若检索不到条目，**停止并向用户确认**，不得以本契约的行文当作操作依据
（本条即 `SKILL.md` 治理红线 §6「证据分级」在 C 类的落地：环境约定 = `INFERRED`，非 `OBSERVED` 基线事实）。

## 8. 所有权 · 不变量 · 禁止项（v0.4.0）

**所有权**：本技能 owns 交接物的**形状与校验**；上游 owns 生成管线；**作者** owns 生成执行与验收。

**不变量**
- `INV-CP-1` 交接物**全部带版本 + hash**（B → C）。
- `INV-CP-2` 媒资走 **Blob 纪律**：引用而非内联。
- `INV-CP-3` 完成门**两级**（同 B 类成熟度，不建第二产品）。

**禁止项**
- 不得声称已调用生成管线或已产出成片。
- 不得把"环境来源"（达芬奇 / Seedance 等）当作可核验的源仓库事实。
