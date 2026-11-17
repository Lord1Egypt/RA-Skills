# B 类子契约 · 漫剧素材前期（storyforge-writing）

> 归属：B 视觉化（出料）+ C 制作后期（对接）。对应 StoryForge MOTION-DRAMA v1.2.0。
> **命名**：源仓库已将该产品**用户可见名**改为「漫剧素材」（产品 **id 不变**，仍为 motion-drama）；
> 本契约与 SKILL.md 路由表统一使用「漫剧素材前期」，「漫剧前期」仅作历史别名。
> **来源等级**：本文件若提及达芬奇 / ai-memory 等，均属**环境来源（INFERRED）**，不经 StoryForge 源仓库基线核验。
> 产物 = 交给外部 AI 图片/视频工具（默认 Seedance）的**专业前期生产包**，不是成片。

## 1. 生产主链（严格顺序）

```
一句话 / 已有小说 / 导入文本
→ 小说内容与来源冻结（source manifest + 源版本 + hash）
→ 系列定位 / 系列圣经 / 分集推进表
→ 角色/服装/场景/道具/声音物料 + 参考材料
→ 逐集集纲 / 漫剧剧本
→ 逐镜分镜（shot）
→ 分镜图 / 首尾关键帧 Image Prompt IR + 参考帧
→ Video Prompt IR
→ Seedance/Runway/LTX 等版本化适配包
→ 单集或整季前期生产 Release
```

**明确不拥有**：视频生成、视频候选选择、剪辑、字幕成片、调色、混音、最终漫剧文件、发布运营。

## 2. 物料字段闭集

物料类型（7 类，固定闭集）：
```
style | character | costume | location | prop | voice | sound
```
- `sound` 在具体用途上细分 ambience / sfx / music
- 每项拥有：稳定 key、文本定义、生成 Prompt、**禁止漂移项**、版本、候选、已选参考媒资、权利、contentHash

shot 参考帧：`start | key | end`，从已确认 shot 和精确物料版本编译，不升级为系列物料身份。

## 3. Provider-neutral IR（关键设计）

- 核心领域保存 **Image Prompt IR + Video Prompt IR**，**不**保存供应商槽位编号/临时参数为业务真理
- Seedance/Runway/LTX adapter 从 IR + 所选参考媒资 + 版本化 capability profile **确定性编译**
- 超能力必须拆分/降级/阻断，**不静默忽略引用**

## 4. 提示词自由与硬边界

作者可查/复制/编辑/保存/比较/恢复每步提示词，设 Work 默认或 episode 覆盖。
**作者不能通过提示词改变**：
- 产品/Work/episode/source/asset 作用域
- 已登记上下文源和可写字段
- 输出 schema、stable key、版本与引用完整性
- 调用/预算/repair/stale/媒资权利/确认门
- provider capability 和 Release 完成门

每次运行**冻结最终模板/变量/版本/hash**，保证候选可解释、Release 可复现。

## 5. 完成层级（两级，不建第二产品）

| 层级 | 含义 |
|---|---|
| `prompt-only` | 系列/剧本/分镜 + Image/Video Prompt IR 完整，但部分参考媒资未锁定 |
| `reference-ready` | 必需物料 + shot 参考帧已选择，引用实际存在/可解码/权利与 hash 完整，adapter 包通过 capability profile |

两级都**停在外部视频生成之前**。

## 6. 世界边界

V1 **不要求、不读取、不生成** WorldRelease；不向世界引擎写人物图/服装图/场景图/道具图/声音/剧本/分镜/Prompt。
（未来若允许显式世界来源，须另改总纲 + 需求适配器 + 产品契约。）

## 7. 与 C 类（后期）的交接

- 本契约产出的 **Image/Video Prompt IR + 适配包**是 C 类生成管线的输入
- C 类（`contracts/C-post.md`）负责把 prompt 包对接到 Seedance/达芬奇〔环境来源〕/剪辑
- 交接物冻结：来源 Work/范围/revision/hash + source manifest，**不反向写小说**

## 8. 所有权 · 不变量 · 禁止项（v0.4.0）

**所有权**：本技能 owns 漫剧素材前期的**主链顺序与物料闭集**；上游 owns MOTION-DRAMA 产品契约；
**作者** owns 系列走向与验收。

**不变量**
- `INV-BM-1` **生产主链严格顺序**：系列圣经 → 逐集 → 分镜 → Prompt IR → 适配包。
- `INV-BM-2` Prompt IR 必须 **provider-neutral**（不绑定单一模型/供应商）。
- `INV-BM-3` 完成层级**两级**（不建第二产品）。
- `INV-BM-4` 不可渲染/不可解析项**不得静默忽略**，须显式列出。

**禁止项**
- 不得把环境来源（如"达芬奇"）标为源仓库基线事实。
- 不得越过 C 类去做后期对接。
