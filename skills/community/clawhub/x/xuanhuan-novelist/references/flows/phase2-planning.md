# 第二阶段：规划 + 二次确认

> **前置条件**：本阶段使用 Phase 1 Layer 3 用户确认的小说标题。标题信息从对话上下文中获取。

执行以下步骤：

1. **清理临时文件**：如果存在 `{base}/.pending-title`，读取标题后删除该文件
2. **创建项目文件夹**：`{base}/{YYYYMMDD-HHmmss}-{Layer 3 确认的标题}/`
3. **生成修炼体系设定**：创建 `00-修炼体系.md`，参照 [cultivation-system.md](../guides/cultivation-system.md) 和 Phase 1 中用户选择的修炼体系方向，设计完整的境界划分、金手指详情、辅助力量体系。**金手指设计参照规则配置**：如果 `writingRules.systemRules.goldenFingerEarlyAppearance.withinChapters` 为 5，则大纲规划时金手指可出现在前5章；如果 `goldenFingerLimitations.minCount` 为 1，则只需设计 1 种限制
4. **生成势力与地图**：创建 `00-势力地图.md`，参照 [xuanhuan-worldbuilding.md](../guides/xuanhuan-worldbuilding.md) 设计地图递进、势力体系、宗门架构
5. **生成人物档案**：创建 `00-人物档案.md`，使用 [character-template.md](../guides/character-template.md) 模板，参照 [character-building.md](../guides/character-building.md) 创建主角、反派、配角档案。**人物档案必须详细**：每个角色的性格核心、致命缺陷、说话风格/口头禅、修炼信息（境界/功法/法宝）、恐惧/弱项、背景故事都要具体到可以直接指导写作
6. **生成大纲**：创建 `01-大纲.md`，使用 [outline-template.md](../guides/outline-template.md) 模板，参照 [plot-structures.md](../guides/plot-structures.md) 和 [xuanhuan-plot-patterns.md](../guides/xuanhuan-plot-patterns.md) 填入完整的章节规划。**大纲必须以人物驱动情节**，包含爽点分布规划
7. **生成写作计划**：创建 `02-写作计划.json`，结构如下。**将 Phase 1 Q9 收集到的规则选择写入 `writingRules` 字段；如果用户跳过了 Q9（说"跳过""下一步""不用选了"等），自动使用上述默认推荐方案的值，不追问**：
   ```json
   {
     "version": 1,
     "novelName": "[小说名称]",
     "projectPath": "{base}/{timestamp}-[小说名称]"
     "totalChapters": [章节数],
     "minWordsPerChapter": 3000,
     "createdAt": "[ISO时间]",
     "updatedAt": "[ISO时间]",
     "status": "planning",
     "writingMode": "[serial|subagent-parallel|agent-teams]",
     "cultivationSystem": {
       "name": "[修炼体系名称]",
       "levels": ["境界1", "境界2", "..."],
       "subLevels": ["初期", "中期", "后期", "巅峰"],
       "protagonistStartLevel": "[初始境界]",
       "protagonistEndLevel": "[终章境界]"
     },
     "factionMap": {
       "factions": ["势力1", "势力2"],
       "mapProgression": ["起始地", "第二地图", "..."]
     },
     "writingRules": {
       "contentRules": {
         "chapterWordCount": { "enabled": true, "min": 3000, "max": 5000 },
         "dialogueRatio": { "enabled": true, "minPercent": 30 },
         "tensionPeaks": { "enabled": true, "minCount": 2 },
         "maxNoConflictWords": { "enabled": true, "maxWords": 500 },
         "unexpectedTwist": { "enabled": true }
       },
       "styleRules": {
         "strongOpening": { "enabled": true },
         "styleForbiddenZones": { "enabled": true },
         "dialogueSubtext": { "enabled": true }
       },
       "systemRules": {
         "goldenFingerEarlyAppearance": { "enabled": true, "withinChapters": 3 },
         "goldenFingerLimitations": { "enabled": true, "minCount": 2 },
         "powerHierarchyAbsolute": { "enabled": true },
         "chapterThrillPoint": { "enabled": true },
         "chapterEndingHook": { "enabled": true }
       }
     },
     "chapters": [
       {
         "chapterNumber": 1,
         "title": "[章节标题]",
         "filePath": "第01章-[章节标题].md",
         "status": "pending",
         "wordCount": null,
         "wordCountPass": null,
         "retryCount": 0
       }
     ]
   }
   ```

完成后，执行以下两步：

**1. 展示规划摘要并请求确认**

向用户展示规划摘要（小说名称、总章数、修炼体系、势力地图、主要人物、爽点分布）并请求确认。

**2. 写作模式选择**（用户确认规划后）

使用 `AskUserQuestion` 询问：

```
Question: 选择写作模式
Options:
- 逐章串行（主 Agent 自己逐章写，全程无中断，适合短中篇）
- 子Agent并行（分批派生子 Agent 并行写作，大纲驱动连贯性，适合中长篇）
- Agent Teams（多 Agent 协作模式，Agent 间可通讯，需手动开启）
```

用户选择后：
- 更新 `02-写作计划.json` 的 `writingMode` 字段
- 更新 `status` 为 `"in_progress"`
- 进入第三阶段：疯狂创作 → 详见 [phase3-writing.md](phase3-writing.md)
