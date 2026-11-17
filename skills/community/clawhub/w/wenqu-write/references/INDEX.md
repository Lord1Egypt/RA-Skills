# wenqu-write 内容索引

## 核心文件

| 文件 | 内容 |
|------|------|
| `SKILL.md` | 三条主流程（从0到1 / 修改 / 审查）与核心原则 |
| `references/INDEX.md` | 本文件，全局内容导航 |

> **配图**已拆分为独立技能 **wenqu-image**（写画图提示、调用 gpt-image-2 生成、质检、上传、写入文章）。本技能的写作阶段先插入占位标记 `> 🖼️ 待配图：[描述]`；一章的概念结构确认后即可逐张调用 wenqu-image，见 `SKILL.md` Step 5。
>
> **审查**（R0~R7）已拆分为独立技能 **wenqu-review**。用户独立触发"审查"时用 `Skill` 工具调用它；写作/修改过程中反复用到的 R5/R1/R2/R3，直接 Read 它的 `references/` 文件内联执行，不发起 `Skill` 调用；R4/R6/R7 在完整审查或实质改动收尾时运行，见 `SKILL.md`「审查」一节。
>
> **翻译**（英文素材转中文）已拆分为独立技能 **wenqu-translate**。Step 2 素材是英文时用 `Skill` 工具调用它，它会自己当场触发 wenqu-review 的 R2 审查，本技能不用重复触发。

---

## references/planning/ — 规划阶段

| 文件 | 内容 |
|------|------|
| `questionnaire.md` | 项目问卷生成指南：证据前置扫描、六维问题（含范围锁定）、SKILL.md/materials/index.md/preferences.md 写入格式、后续会话加载、补充提问规则 |
| `modes.md` | A/B/C 三种文章模式骨架模板（快速入门 / 架构深挖 / 方案对比） |
| `skeleton.md` | 骨架写作指南：颗粒度要求、素材引用标注、示例格式、变更历史表、大改时的变更写法 |
| `wenqu-profile.md` | 写作画像、设计决策图与章节职责卡：供骨架、R6 与自研方案写作使用 |
| `change-impact.md` | 实质改动的影响记录模板：供 R7 检查术语、结构、图文与交叉引用是否闭环 |
| `materials-governance.md` | 素材可信度与冲突裁决：避免将互相矛盾的资料直接写入正文 |
| `terms.md` | 文章级术语表模板：统一跨章节概念的推荐词、范围与首次定义位置 |
| `content-provenance.md` | 内容来源与评测结论表述：区分实现事实、团队选择、外部研究、推断与简化场景，并说明评测结论边界 |
| `wenqu-status.md` | 文章生命周期状态与完成条件核对：记录跨会话进度、待复查项和章节、图片、全文完成条件 |
| `iterative-revision.md` | 已有长文的分章修改：任务边界、重读素材与人工编辑保护 |

---

## references/writing/ — 写作规范

| 文件 | 内容 |
|------|------|
| `style-guide.md` | 完整写作风格规范（行文、结构、语言，含 Hard Gates） |
| `anti-patterns.md` | 禁止事项清单（35 条），含定稿自检清单 |
| `system-implementation.md` | 自研系统、架构设计与工程实践文章的按需写法 |
