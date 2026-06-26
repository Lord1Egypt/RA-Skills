---
name: super-novel-generator
description: "根据用户提供的题材、方向或关键词，生成中文网文小说的提示词、大纲、章节正文与连续性记忆文件。适用于爽文、都市、修仙、玄幻、重生、系统流等创作任务。Use when user asks to write a novel, generate fiction, create stories, or mentions 爽文、小说、写作。"
---

# 爽文小说生成器

根据用户给出的题材、脑洞或续写需求，产出中文网文的提示词、大纲、章节正文，以及在需要长期连载时维护 `.learnings/` 连续性记忆。

## 执行边界

- 用户只要提示词、梗概、章节正文、续写片段时，直接在对话中产出，不强制落盘。
- 只有当用户明确要求保存产物、维护长期连载、初始化工作区，或当前任务本身就在本 skill 工作目录中时，才写入 `output/` 和 `.learnings/`。
- 如果是续写已有工程，先读取现有 `output/`、`.learnings/`，只做增量更新，不重新初始化。

## 资源导航

只在任务需要时读取资源，不要一次性加载全部参考资料。

### 需要时再读 `references/`

- `references/prompt-guide.md`：把一句话题材补全成可写的创作提示词。
- `references/plot-structures.md`：设计卷结构、章节节奏、爽点密度。
- `references/character-arcs.md`：角色成长停滞、关系线发虚时使用。
- `references/antagonist-design.md`：反派压迫感不足或同质化时使用。
- `references/de-ai-writing.md`：正文太像模板、总结腔太重时使用。
- `references/examples.md`：需要最小示例格式时使用。

### 优先复用 `assets/`

- `assets/PROMPT-TEMPLATE.md`：提示词输出骨架。
- `assets/VOLUME-TEMPLATE.md`：卷级大纲骨架。
- `assets/SCENE-CARD-TEMPLATE.md`：先拆场景卡再写正文。
- `assets/CHAPTER-TEMPLATE.md`：章节文件骨架。
- `assets/LEARNINGS-TEMPLATE.md`：`.learnings/` 模板与字段格式。

## 核心流程

### 1. 生成或完善提示词

当用户只给一句方向时，至少补齐以下信息：

- 题材定位：主类型 + 子类型。
- 主角设定：身份、起点、优势或金手指。
- 成长机制：等级体系，或资源/地位/势力跃迁路径。
- 核心冲突：主线矛盾与前几章即时冲突。
- 爽点设计：打脸、反转、碾压、身份揭秘等主要来源。
- 开篇钩子：第一章如何抓人。

如果用户需要保存，写入 `output/提示词.md`；否则直接在回复中给出。

### 2. 规划大纲

先判断题材类型：

- 修仙、玄幻、高武、异能、游戏升级流：给明确力量或等级体系。
- 都市、重生、现实、职场、悬疑：不给生硬境界表，改为成长路径、资源阶梯、身份跃迁或势力格局。

大纲至少包含：

- 基本信息：题材、预计章节数、每章字数范围。
- 成长体系或成长路径。
- 分卷主线：每卷核心冲突、主角成长、主要爽点。
- 关键转折点：重要反转、揭秘、卷终高潮。

### 3. 生成章节

生成章节前，若工作区存在 `.learnings/`，必须优先读取：

- `.learnings/CHARACTERS.md`
- `.learnings/LOCATIONS.md`
- `.learnings/PLOT_POINTS.md`
- `.learnings/STORY_BIBLE.md`

若准备融入热梗，再额外检查：

- `.learnings/HUMOR_REFERENCES_USED.md`
- `时事热梗素材/`

章节写作要求：

- 每章有明确冲突推进。
- 每章至少有一个可感知的小爽点。
- 章末留钩子，推动读者继续看。
- 与已有角色状态、地点、伏笔、设定保持一致。
- 对话要有人物差异，避免所有角色一个腔调。

如需稳定结构，优先复用 `assets/CHAPTER-TEMPLATE.md`；如果章节发散，先用 `assets/SCENE-CARD-TEMPLATE.md` 拆 3-6 个场景。

### 4. 维护记忆

章节定稿后按需更新：

- 新角色或角色状态变化：`CHARACTERS.md`
- 新地点：`LOCATIONS.md`
- 关键事件：`PLOT_POINTS.md`
- 新世界规则：`STORY_BIBLE.md`
- 已实际写入正文的热梗：`HUMOR_REFERENCES_USED.md`
- 生成失败、设定矛盾、越界内容：`ERRORS.md`

如果图解与 `.learnings/` 或正文冲突，以 `.learnings/` 和正文为准。

## 安全与命名约束

- 默认使用虚构人名、地名、组织名、学校名、企业名、政体名。
- 不直接使用现代真实城市名、真实名人姓名、现实领导人姓名。
- 如用户输入含真实名称，保留气质和功能，但改写成虚构名称。
- 不写现实政治敏感、历史敏感、军警机密、体制负面、恐怖主义、分裂、美化侵略或侮辱英烈内容。
- 不写性行为、露骨亲热、未成年暧昧、乱伦、低俗性暗示或过度身体描写。
- 涉及国家、历史、权力背景时，默认改写为架空世界、虚构势力、虚构政体。

## 输出建议

- 提示词：`output/提示词.md`
- 大纲：`output/大纲.md`
- 章节：`output/章节/第XX章_章节名.md`
- 图解：按需生成 Mermaid 图并保存为对应 `.md`

## 初始化工作区

仅当用户明确要求新建小说工程，或当前目录尚无工作区时，运行：

```bash
./scripts/init-novel.sh 小说名称
```

- 默认补建缺失目录和模板，不覆盖已有记忆文件。
- 只有用户明确要“从头重开”时才考虑 `--clean`。
