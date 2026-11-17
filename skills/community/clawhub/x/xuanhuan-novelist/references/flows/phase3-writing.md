# 第三阶段：疯狂创作

**重要：全程无需再次向用户确认，必须逐章创作直到完成**

---

## 0. 启动检测与模式读取

开始创作前：
1. 读取 `02-写作计划.json`
2. 读取 `writingMode` 字段，进入对应模式流程
3. **提取 `writingRules` 字段作为创作约束**。如果 `writingRules` 字段不存在（旧项目兼容），使用默认推荐方案（所有规则 `enabled: true`，字数 3000-5000，对话 30%，张力波峰 2，无冲突上限 500）
4. 如果存在 `status: "in_progress"` 的章节 → 从该章节继续（中断续写）
5. 如果所有章节 `status: "pending"` → 从第 1 章开始
6. 如果存在 `status: "failed"` 的章节（Phase 4 回退）→ 从第一个 failed 章节开始

---

## 1. 逐章创作流程（通用，所有模式共用）

每章创作时严格执行以下步骤：

### 步骤 1: 写前分析（必须执行）

1. 读取 `02-写作计划.json` — 查看各章节状态，确定下一个待创作章节，**提取 `writingRules` 字段**
2. **读取 `01-大纲.md`** — 找到当前章节的规划信息，提取：核心事件、承接上章、悬念钩子、出场人物、场景列表、爽点/铺垫、主角境界
3. **读取 `00-人物档案.md`** — 根据大纲中本章的「出场人物」列表，提取每个出场角色的：性格核心、致命缺陷、说话风格/口头禅、修炼信息（境界/功法/法宝）、恐惧/弱项
4. **读取 `00-修炼体系.md`** — 确认主角当前境界、可用功法法宝、金手指当前阶段的能力和限制
5. **读取 `03-文风档案.md`**（如果存在）— 提取文风指纹、文风禁区、参照段落，确保本章写作风格与初稿一致
6. 更新 `02-写作计划.json` — 将本章 `status` 设为 `"in_progress"`

### 步骤 2: 撰写

7. 创建章节文件 — 文件名格式：`第{XX}章-{章节标题}.md`，使用 [chapter-template.md](../guides/chapter-template.md) 模板
8. **基于大纲规划创作** — 严格按照大纲中本章的核心事件和场景列表撰写正文
9. **撰写章首引子** — 按大纲中本章的章首引子类型，参考 [hook-techniques.md](../guides/hook-techniques.md)「章首引子七式」，创作 50-150 字的引子文字
10. 撰写正文 — **按 `writingRules.contentRules.chapterWordCount` 的 min/max 值控制字数**
   - 章首引子：已创作（步骤 9）
   - 正文开头：如果 `writingRules.styleRules.strongOpening.enabled`，第一段使用 [chapter-guide.md](../guides/chapter-guide.md) 十种开头技巧之一，建立即时冲突
   - **爽点检查**：如果 `writingRules.systemRules.chapterThrillPoint.enabled`，本章必须包含至少一个爽点或为下一个爽点做铺垫，参照 [xuanhuan-plot-patterns.md](../guides/xuanhuan-plot-patterns.md)
   - **战斗描写**：如有战斗场景，参照 [battle-writing.md](../guides/battle-writing.md) 的规范
   - **修炼描写**：如有修炼/突破场景，参照 [cultivation-system.md](../guides/cultivation-system.md) 的描写规范
   - 张力节奏：按 `writingRules.contentRules.tensionPeaks.minCount` 控制张力波峰数量；按 `writingRules.contentRules.maxNoConflictWords.maxWords` 控制无冲突字数上限
   - 对话要求：按 `writingRules.contentRules.dialogueRatio.minPercent` 控制对话比例；如果 `writingRules.styleRules.dialogueSubtext.enabled`，每段对话必须有潜台词或推进情节目的（参考 [dialogue-writing.md](../guides/dialogue-writing.md)）
   - 意外转折：如果 `writingRules.contentRules.unexpectedTwist.enabled`，每章至少 1 个读者预期之外的事件或信息
   - 人物一致性（核心规则）：对话和行为必须严格符合角色设定
   - 结尾钩子：如果 `writingRules.systemRules.chapterEndingHook.enabled`，按大纲悬念钩子设计结尾
   - 内容不足？使用 [content-expansion.md](../guides/content-expansion.md) 扩充技巧
11. 设置结尾钩子 — 按大纲中本章的悬念钩子设计 → [hook-techniques.md](../guides/hook-techniques.md)「悬念钩子十三式」
12. **字数检查** — 使用脚本：`python scripts/check_chapter_wordcount.py <章节文件路径> [writingRules.contentRules.chapterWordCount.min]`

### 步骤 3: 撰写后优化

13. 连贯性检查 — 人物一致性、境界状态跟踪、情节连贯、节奏控制
14. **文风一致性检查**（如果存在 `03-文风档案.md`）— 对照文风指纹检查本章：句式结构是否匹配、词汇风格是否一致、文风禁区是否触发（如果 `writingRules.styleRules.styleForbiddenZones.enabled`）、术语是否与设定档案一致（核心规则）、对话风格是否符合初稿风格
15. **深度润色（去除AI味）** — 重点检查并修改：
    - **去除过度修饰的形容词**：删减"璀璨的灵力""浩瀚的丹田"等AI常用词堆砌
    - **减少抽象陈述**：把"他感受到了强大的力量"改为具体的身体感受
    - **打破四字格律**：避免"心潮澎湃、热血沸腾"等陈词滥调
    - **增加口语化表达**：人物对话要有个性，符合角色身份
    - **优化节奏感**：长句短句交替，战斗用短句
    - **细节具象化**：用具体细节替代笼统描述
    - **战斗描写检查**：是否过于模式化（每次都是"灵力暴涌→对方震惊→一击必杀"）
    - **修炼描写检查**：是否过于抽象（缺少身体感受、具象化体验）
16. **字数检查** — 再次使用脚本确认

### 步骤 4: 收尾

17. 生成章节摘要 — 在 `01-大纲.md` 的章节摘要区追加（300-500字，保证连贯性参考）
18. 更新 `02-写作计划.json` — 将本章 `status` 设为 `"completed"`，填入 `wordCount`

---

## 2. 串行模式（writingMode: "serial"）

**主 Agent 自己逐章创作，全程不中断。**

### 自驱循环

```
WHILE 02-写作计划.json 中存在 status != "completed" 的章节:
    执行「逐章创作流程」（步骤 1-4）
    ⚠️ 完成一章后，立即读取 JSON 认领下一章，不要向用户确认，不要停下来
所有章节完成 → 进入第四阶段：自动校验
```

**关键提醒**：
> 本章已完成。立即读取 `02-写作计划.json`，认领下一个 pending 章节，开始下一章创作。不要使用 AskUserQuestion，不要向用户确认，不要停下来。你必须把所有章节创作完成才能与用户报告。

---

## 3. 子Agent并行模式（writingMode: "subagent-parallel"）

**核心机制**：主 Agent 将章节分成不重叠的批次，每个批次派生一个子 Agent。批次内串行写作，批次间并行执行。

### 主 Agent 流程

```
1. 计算批次分配:
   - 每批 5-8 章
   - 批次间不重叠
2. 为每个批次派生子 Agent:
   - 每个 Agent 内部串行执行「逐章创作流程」
3. 所有子 Agent 完成后 → 进入第四阶段：自动校验
```

### 子 Agent prompt 模板（并行模式）

```
你是一个玄幻小说批量创作 Agent。你需要创作第 {start} 章到第 {end} 章。

## 项目信息
- 项目路径: {projectPath}
- 你负责的章节: 第 {start} 章 到 第 {end} 章

## 创作步骤（对每一章依次执行）
1. 读取 {projectPath}/01-大纲.md，找到当前章节的规划信息
2. 读取 {projectPath}/00-人物档案.md，提取出场角色设定
3. 读取 {projectPath}/00-修炼体系.md，确认主角当前境界和可用功法法宝
4. 读取 02-写作计划.json，确认章节状态，**提取 `writingRules` 字段作为创作约束**（如果不存在则使用默认推荐方案）
5. 将当前章节 status 更新为 "in_progress"
6. 创建章节文件，基于大纲撰写正文（按 writingRules.contentRules.chapterWordCount 的 min/max 控制字数）
7. 按大纲中的章首引子类型创作引子（50-150字）
8. 如果 writingRules.styleRules.strongOpening.enabled，正文开头使用 chapter-guide.md 十种开头技巧之一
9. 如果 writingRules.systemRules.chapterThrillPoint.enabled，本章必须有爽点或铺垫
10. 战斗场景参照 battle-writing.md，修炼场景参照 cultivation-system.md
11. 按 writingRules.contentRules 配置控制张力波峰、无冲突字数上限、对话比例
12. 如果 writingRules.styleRules.dialogueSubtext.enabled，对话必须有潜台词和角色个性
13. 如果 writingRules.contentRules.unexpectedTwist.enabled，每章至少 1 个读者预期外的转折
14. 人物行为必须符合角色设定（核心规则，始终生效）
15. 如果 writingRules.systemRules.chapterEndingHook.enabled，结尾按大纲悬念钩子设计
16. 运行字数检查: python scripts/check_chapter_wordcount.py <文件路径> [writingRules.contentRules.chapterWordCount.min]
17. 深度润色（去除AI味，特别注意战斗和修炼描写不要模式化）
18. 再次字数检查
19. 在 01-大纲.md 追加 300-500 字章节摘要
20. 更新 status → "completed"，填入 wordCount
21. 立即继续下一章

## 重要约束
- 不要使用 AskUserQuestion，不要向用户确认任何事
- 每章开始前必须读取大纲和修炼体系（核心规则）
- 术语必须与设定档案一致（核心规则）
- 人物行为必须符合角色设定（核心规则）
- 你负责的所有章节必须全部完成

完成后报告: 各章编号、字数、是否通过字数检查
```

---

## 4. Agent Teams 模式（writingMode: "agent-teams"）

与子Agent并行模式类似，但通过 TeamCreate/TaskList/TaskUpdate 系统协调。团队成员 prompt 模板参照上述子 Agent 模板，增加 TaskList 认领机制。
