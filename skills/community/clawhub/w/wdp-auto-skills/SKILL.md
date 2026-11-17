---
name: experience-forge
description: 经验锻造/经验收割。Use when a problem was just solved (especially after 2+ rounds of repeated fixes), a non-obvious pitfall was hit, a reusable design decision was made, the user expressed a preference or correction, or the user asks to 总结经验 / 沉淀经验 / 记录教训 / 复盘 / 形成 skill / 更新用户画像. Distills the session's experience into structured reusable knowledge, files it by category (personal / project / domain), and incrementally updates the user profile so the AI keeps evolving.
---

# Experience Forge — 经验锻造炉

**一句话定位**：在解决问题的时刻判断"这次经验值不值得沉淀"，经用户确认后蒸馏成结构化知识、分类入库，并增量更新用户画像——让每一次会话都使下一次会话更聪明。

## 何时触发（自检清单）

会话进入"问题解决 / 任务完成"状态后自检，命中任一条**且本会话尚未建议过**，用一句话询问用户是否蒸馏：

- [ ] 同一问题经过 ≥2 轮修改/纠正才改对（最强信号）
- [ ] 踩到不直观的坑：版本不兼容、环境怪癖、未文档化行为、文档与实际不符
- [ ] 做出了可复用的设计决策
- [ ] 用户明确表达了偏好或纠正（"以后都用 X"、"别这样写"）——即使不蒸馏经验，也应更新用户画像

用户主动说"总结经验 / 记录一下 / 这个教训要记住"时，跳过自检直接进入工作流。

## 评分标准（值不值得记）

| 信号 | 权重 |
|---|---|
| 反复修改才改对（≥2 轮） | +3 |
| 用户明确表达偏好/纠正 | +3（直接进用户画像） |
| 根因不直观（环境/版本/未文档化行为） | +2 |
| 可复用的好设计决策 | +2 |
| 一次性笔误、纯 CRUD、文档已有记载 | 0，不触发 |

≥3 分 → 建议沉淀；≥5 分 → 向用户强调其价值。

## 铁律（违反任何一条都视为执行失败）

1. **绝不静默写入**：所有写入必须先给用户看草稿并获确认，用户可逐条 确认 / 修改 / 放弃。
2. **每会话最多主动建议 1 次**：被拒绝后本次会话不再推荐；用户连续拒绝 2 次，主动提出降低建议频率（写入画像的协作偏好）。
3. **先查重再写入**：写前检索 user-profile.md、经验库、项目 CLAUDE.md 中的已有条目；与旧条目冲突时**更新旧条目**，不新增。
4. **条目克制**："通用规则"字段必须一行、可被 AI 直接执行；不写过程流水账。
5. **不臆造**：来源字段只记录本次会话真实发生的事，不外推、不脑补。
6. **画像只增量合并，不重写**：新偏好覆盖旧偏好时，在画像的"变更日志"留痕。

## 工作流（6 步）

1. **回看**：回顾本次会话的编辑历史、错误路径、用户反馈，一句话概括：什么问题 / 走过什么弯路 / 根因 / 最终解法。
2. **评分**：按上表打分，<3 分不打扰用户。
3. **草拟**：产出 1~3 条候选经验（模板见 `references/templates.md`）+ 画像更新建议（如有），每条标注分类：
   - **个人通用**（与项目无关的方法论、通用坑）→ `~/.claude/experience/general/<topic>.md`
   - **项目**（本项目专属坑、约定、环境怪癖）→ 当前项目 `CLAUDE.md` 的 `## 经验与坑` 小节（没有则创建）
   - **行业领域**（行业知识、业务规则，如 GIS/GeoAI）→ `~/.claude/skills/<领域>-experience/`（不存在则经确认后创建最小 skill 骨架）
4. **确认**：逐条请用户 确认 / 修改 / 放弃。
5. **写入**：
   - 个人通用：并入或新建主题文件，并在 `~/.claude/experience/general/README.md` 索引登记一行；
   - 项目：追加到项目 `CLAUDE.md`；
   - 领域：写入对应领域 skill；
   - 画像：按 `references/templates.md` 的字段定义增量合并进 `~/.claude/user-profile.md`（每条带日期与来源）。
6. **闭环反馈**：一句话告知用户写到了哪里、下次什么场景会自动生效。

## 落库位置速查

| 分类 | 位置 | 生效范围 |
|---|---|---|
| 用户画像 | `~/.claude/user-profile.md` | 所有项目（全局 CLAUDE.md 已 @引入） |
| 个人通用经验 | `~/.claude/experience/general/` | 所有项目（经 README 索引） |
| 行业领域经验 | `~/.claude/skills/<领域>-experience/` | 同领域项目 |
| 项目经验 | 项目 `CLAUDE.md` | 仅当前项目 |

存储一律使用中立 Markdown，不绑定特定工具格式，便于未来同步到 Cursor 等其他 AI 工具。

## 自进化（本 skill 自身也在进化范围内）

若蒸馏出的经验属于"如何更好地蒸馏经验"（如某信号误报率高、模板字段冗余、分类边界模糊），经用户确认后可直接更新本 `SKILL.md` 或 `references/templates.md`，并在文末"变更日志"登记来源。

## 维护命令

用户说"整理经验 / 经验体检"（或 `--tidy`）时：
1. 扫描全部四轨存储，找出相似条目（合并）、相互矛盾条目（以新代旧并留痕）、明显过时条目（加 ⚠️ 标注，不删除）；
2. 输出清理清单请用户确认后执行。

## 变更日志
- 2026-08-27 v0.1 初版：自检清单 + 评分标准 + 四轨落库 + 画像增量维护
