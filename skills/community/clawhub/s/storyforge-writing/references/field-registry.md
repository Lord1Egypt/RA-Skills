# Field Registry — AI 可写字段参考（**机械生成，非手写**）

> **来源**：`H:\storyforge-main` 的 `src/lib/registry/field-registry.ts`（799 行）与 `adoption-schema.ts`（1049 行）
> **生成**：2026-10-06，逐条抽取（**展开解析**，0 条未解析）；上游 MIT（见 `NOTICE.md`），本文件是其登记表的**派生索引**
> **规则**：与源码不一致时**以源码为准**，并重新生成本文件。

## 0. 这份文件管什么（别混用）

| 权威 | 位置 | 管什么 |
| --- | --- | --- |
| **本文件** | `references/field-registry.md` | **AI/结构化采纳可写字段**（`FIELD_REGISTRY`）+ **集合表写回策略**（`ADOPTION_SCHEMAS`） |
| `references/schema-tables.md` | 同目录 | 表清单 · store 规格（索引）· TS 接口字段与类型 |
| 上游 `src/lib/registry/project-tables.ts` | 上游仓库 | 导出 / 导入 / 删除 / 作用域 / 引用重映射（生命周期） |

> ⚠️ **未登记即被拒**：运行时校验在 `src/lib/agent/run/contract.ts`（`unknown_write_field`）。
> 本文件之外的字段**不得**由 AI 写入。这里给出的是**登记类型**，
> **不等于**该字段可自由生成（是否可生成还受作用域 / 依赖 / 政策约束）。

## 1. `FIELD_REGISTRY` — 可写字段总表（**64 张表 / 528 项**）

> 展开自 `FIELD_REGISTRY`（含 `...WORLDVIEW_GENERATABLE_FIELD_SPECS` 18 项 与 `...STORY_CORE_GENERATABLE_FIELD_SPECS` 7 项，共 25 项）。
> 「AI 生成」列 = 该字段位于上述两个**生成启用子集**内（其余字段可被采纳写入，但不属生成启用集）。

### `projects`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `enableMultiWorld` | `boolean` | — | — |
| `name` | `string` | — | — |

### `worlds`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `name` | `string` | — | — |

### `works`（9 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `customGenre` | `string` | — | — |
| `description` | `longtext` | — | — |
| `genres` | `array` | — | — |
| `includeCultivationProgressInAI` | `boolean` | — | — |
| `methodologyId` | `string` | — | — |
| `status` | `enum` | `drafting`·`ongoing`·`paused`·`completed` | — |
| `targetWordCount` | `number` | — | — |
| `title` | `string` | — | — |
| `writingStyleId` | `string` | — | — |

### `shortNovelProductions`（3 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `brief` | `object` | — | — |
| `latestReview` | `object` | — | — |
| `storyDesign` | `object` | — | — |

### `adaptationProjects`（3 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `brief` | `object` | — | — |
| `plan` | `object` | — | — |
| `visualBible` | `object` | — | — |

### `adaptationSourceFacts`（5 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `confidence` | `number` | — | — |
| `kind` | `enum` | `event`·`character-state`·`relationship`·`location`·`object`·`motif` | — |
| `sourceUnitKeys` | `array` | — | — |
| `statement` | `longtext` | — | — |
| `subjectKeys` | `array` | — | — |

### `adaptationCausalEdges`（5 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `fromFactKey` | `string` | — | — |
| `rationale` | `longtext` | — | — |
| `relation` | `enum` | `cause`·`enables`·`motivates`·`reveals`·`prevents` | — |
| `sourceUnitKeys` | `array` | — | — |
| `toFactKey` | `string` | — | — |

### `adaptationDecisions`（4 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `action` | `enum` | `keep`·`cut`·`merge`·`reorder`·`externalize`·`add` | — |
| `rationale` | `longtext` | — | — |
| `sourceFactKeys` | `array` | — | — |
| `targetKeys` | `array` | — | — |

### `screenplayBeats`（13 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `causalFactKeys` | `array` | — | — |
| `conflict` | `longtext` | — | — |
| `decisionKeys` | `array` | — | — |
| `episodeNumber` | `number` | — | — |
| `estimatedSeconds` | `number` | — | — |
| `objective` | `longtext` | — | — |
| `order` | `number` | — | — |
| `outcome` | `longtext` | — | — |
| `scope` | `enum` | `act`·`sequence`·`episode` | — |
| `sectionKey` | `string` | — | — |
| `sectionTitle` | `longtext` | — | — |
| `sourceUnitKeys` | `array` | — | — |
| `turn` | `longtext` | — | — |

### `screenplaySceneCards`（12 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `beatKey` | `string` | — | — |
| `conflict` | `longtext` | — | — |
| `entryState` | `longtext` | — | — |
| `episodeNumber` | `number` | — | — |
| `estimatedSeconds` | `number` | — | — |
| `exitState` | `longtext` | — | — |
| `informationReveal` | `longtext` | — | — |
| `order` | `number` | — | — |
| `purpose` | `longtext` | — | — |
| `sceneNumber` | `number` | — | — |
| `sourceUnitKeys` | `array` | — | — |
| `visibleAction` | `longtext` | — | — |

### `screenplayReviewIssues`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `blockId` | `string` | — | — |
| `category` | `enum` | `grounding`·`continuity`·`dramaturgy`·`format` | — |
| `evidence` | `longtext` | — | — |
| `problem` | `longtext` | — | — |
| `sceneKey` | `string` | — | — |
| `severity` | `enum` | `critical`·`major`·`minor` | — |
| `sourceUnitKeys` | `array` | — | — |
| `suggestion` | `longtext` | — | — |

### `screenplayScenes`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `blocks` | `array` | — | — |
| `estimatedSeconds` | `number` | — | — |
| `intExt` | `enum` | `INT`·`EXT`·`INT_EXT` | — |
| `location` | `string` | — | — |
| `planSectionKey` | `string` | — | — |
| `sourceUnitIds` | `array` | — | — |
| `summary` | `longtext` | — | — |
| `timeOfDay` | `string` | — | — |

### `comicPages`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `pagePlanKey` | `string` | — | — |
| `summary` | `longtext` | — | — |

### `comicPanels`（13 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `action` | `longtext` | — | — |
| `continuityRefs` | `array` | — | — |
| `frame` | `object` | — | — |
| `lettering` | `array` | — | — |
| `moment` | `longtext` | — | — |
| `narrativeFunction` | `string` | — | — |
| `negativePrompt` | `longtext` | — | — |
| `nextPanelKey` | `string` | — | — |
| `protectedAreas` | `array` | — | — |
| `shot` | `object` | — | — |
| `sourceUnitIds` | `array` | — | — |
| `subjectStates` | `array` | — | — |
| `visualPrompt` | `longtext` | — | — |

### `comicVisualSubjects`（3 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `design` | `object` | — | — |
| `label` | `string` | — | — |
| `sourceUnitIds` | `array` | — | — |

### `comicScriptBeats`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `causalFactKeys` | `array` | — | — |
| `decisionKeys` | `array` | — | — |
| `dialogueIntent` | `longtext` | — | — |
| `emotion` | `string` | — | — |
| `narrativeFunction` | `string` | — | — |
| `sectionKey` | `string` | — | — |
| `sourceUnitKeys` | `array` | — | — |
| `visualAction` | `longtext` | — | — |

### `comicPagePlans`（4 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `beatKeys` | `array` | — | — |
| `endReveal` | `longtext` | — | — |
| `goal` | `longtext` | — | — |
| `pageTurn` | `string` | — | — |

### `comicReviewIssues`（10 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `assetKey` | `string` | — | — |
| `category` | `string` | — | — |
| `evidence` | `longtext` | — | — |
| `pageKey` | `string` | — | — |
| `panelKey` | `string` | — | — |
| `problem` | `longtext` | — | — |
| `severity` | `string` | — | — |
| `sourceUnitKeys` | `array` | — | — |
| `subjectKey` | `string` | — | — |
| `suggestion` | `longtext` | — | — |

### `motionDramaSeriesBibles`（1 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `bible` | `object` | — | — |

### `motionDramaEpisodes`（9 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `beats` | `array` | — | — |
| `continuityIn` | `array` | — | — |
| `continuityOut` | `array` | — | — |
| `endHook` | `longtext` | — | — |
| `logline` | `longtext` | — | — |
| `openingHook` | `longtext` | — | — |
| `sourceUnitKeys` | `array` | — | — |
| `synopsis` | `longtext` | — | — |
| `title` | `string` | — | — |

### `motionDramaScriptScenes`（14 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `characterKeys` | `array` | — | — |
| `dialogue` | `array` | — | — |
| `dramaticPurpose` | `longtext` | — | — |
| `emotionalTurn` | `longtext` | — | — |
| `entryState` | `longtext` | — | — |
| `estimatedSeconds` | `number` | — | — |
| `exitState` | `longtext` | — | — |
| `heading` | `longtext` | — | — |
| `location` | `string` | — | — |
| `narration` | `longtext` | — | — |
| `soundCues` | `array` | — | — |
| `sourceUnitKeys` | `array` | — | — |
| `timeOfDay` | `string` | — | — |
| `visibleAction` | `longtext` | — | — |

### `motionDramaAssetSubjects`（12 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `appearance` | `longtext` | — | — |
| `basePrompt` | `longtext` | — | — |
| `continuityLocks` | `array` | — | — |
| `identity` | `longtext` | — | — |
| `kind` | `enum` | `character`·`costume`·`location`·`prop`·`style`·`voice`·`sound` | — |
| `label` | `string` | — | — |
| `materials` | `array` | — | — |
| `negativePrompt` | `longtext` | — | — |
| `palette` | `array` | — | — |
| `prohibitedChanges` | `array` | — | — |
| `referenceBrief` | `longtext` | — | — |
| `sourceUnitKeys` | `array` | — | — |

### `motionDramaShots`（23 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `cameraAngle` | `enum` | `eye-level`·`high`·`low`·`overhead`·`dutch`·`pov` | — |
| `cameraMovement` | `enum` | `static`·`pan`·`tilt`·`track`·`dolly`·`orbit`·`zoom`·`handheld` | — |
| `composition` | `longtext` | — | — |
| `dialogue` | `longtext` | — | — |
| `firstFramePrompt` | `longtext` | — | — |
| `imagePrompt` | `longtext` | — | — |
| `keyFramePrompt` | `longtext` | — | — |
| `lastFramePrompt` | `longtext` | — | — |
| `lighting` | `longtext` | — | — |
| `narration` | `longtext` | — | — |
| `narrativeFunction` | `longtext` | — | — |
| `negativeImagePrompt` | `longtext` | — | — |
| `negativeVideoPrompt` | `longtext` | — | — |
| `performance` | `longtext` | — | — |
| `shotSize` | `enum` | `extreme-wide`·`wide`·`full`·`medium`·`close-up`·`extreme-close-up`·`insert` | — |
| `soundPlan` | `array` | — | — |
| `sourceUnitKeys` | `array` | — | — |
| `subjectKeys` | `array` | — | — |
| `targetSeconds` | `number` | — | — |
| `transitionIn` | `longtext` | — | — |
| `transitionOut` | `longtext` | — | — |
| `videoPrompt` | `longtext` | — | — |
| `visibleAction` | `longtext` | — | — |

### `motionDramaReviewIssues`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `category` | `enum` | `story`·`continuity`·`visual`·`motion`·`prompt`·`sound`·`rights`·`provider-capability` | — |
| `evidence` | `longtext` | — | — |
| `problem` | `longtext` | — | — |
| `sceneKey` | `string` | — | — |
| `severity` | `enum` | `critical`·`major`·`minor` | — |
| `shotKey` | `string` | — | — |
| `subjectKey` | `string` | — | — |
| `suggestion` | `longtext` | — | — |

### `worldGroups`（10 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `entryCondition` | `longtext` | — | — |
| `exitCondition` | `longtext` | — | — |
| `icon` | `string` | — | — |
| `name` | `string` | — | — |
| `order` | `number` | — | — |
| `plannedChapterCount` | `number` | — | — |
| `powerRestriction` | `longtext` | — | — |
| `takeawayRules` | `longtext` | — | — |
| `type` | `enum` | `traversal`·`instance`·`parallel`·`ascension`·`custom` | — |

### `worldviews`（18 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `climateByRegion` | `longtext` | — | ✓ |
| `continentLayout` | `longtext` | — | ✓ |
| `cultureOverview` | `longtext` | — | ✓ |
| `divineDesign` | `object` | — | ✓ |
| `economyOverview` | `longtext` | — | ✓ |
| `factionLayout` | `longtext` | — | ✓ |
| `internalConflicts` | `longtext` | — | ✓ |
| `itemDesign` | `longtext` | — | ✓ |
| `mountainsRivers` | `longtext` | — | ✓ |
| `naturalResourceOverview` | `longtext` | — | ✓ |
| `naturalResources` | `object` | — | ✓ |
| `politicsOverview` | `longtext` | — | ✓ |
| `powerHierarchy` | `longtext` | — | ✓ |
| `races` | `longtext` | — | ✓ |
| `regionDimensions` | `longtext` | — | ✓ |
| `worldDimensions` | `longtext` | — | ✓ |
| `worldOrigin` | `longtext` | — | ✓ |
| `worldStructure` | `longtext` | — | ✓ |

### `worldRulesProfiles`（3 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `customNodes` | `array` | — | — |
| `entries` | `object` | — | — |
| `globalNote` | `longtext` | — | — |

### `geographies`（3 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `locations` | `json` | — | — |
| `overview` | `longtext` | — | — |
| `worldMapData` | `json` | — | — |

### `histories`（3 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `eraSystem` | `longtext` | — | — |
| `events` | `json` | — | — |
| `overview` | `longtext` | — | — |

### `powerSystems`（4 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `levels` | `json` | — | — |
| `name` | `string` | — | — |
| `rules` | `longtext` | — | — |

### `storyCores`（7 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `centralConflict` | `longtext` | — | ✓ |
| `concept` | `longtext` | — | ✓ |
| `logline` | `longtext` | — | ✓ |
| `mainPlot` | `longtext` | — | ✓ |
| `plotPattern` | `longtext` | — | ✓ |
| `subPlots` | `longtext` | — | ✓ |
| `theme` | `longtext` | — | ✓ |

### `characters`（45 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `abilities` | `longtext` | — | — |
| `activeChapterRange` | `string` | — | — |
| `appearance` | `longtext` | — | — |
| `arc` | `longtext` | — | — |
| `background` | `longtext` | — | — |
| `cultivationStageId` | `string` | — | — |
| `cultivationSystemId` | `number` | — | — |
| `ending` | `longtext` | — | — |
| `exitChapterId` | `number` | — | — |
| `fears` | `longtext` | — | — |
| `firstAppearChapterId` | `number` | — | — |
| `firstAppearance` | `string` | — | — |
| `goals` | `longtext` | — | — |
| `habits` | `longtext` | — | — |
| `homeWorldGroupId` | `number` | — | — |
| `identity` | `longtext` | — | — |
| `importantLocationId` | `number` | — | — |
| `innerConflict` | `longtext` | — | — |
| `isCrossWorld` | `boolean` | — | — |
| `keyEvents` | `longtext` | — | — |
| `location` | `string` | — | — |
| `moralAxis` | `enum` | `good`·`neutral`·`evil` | — |
| `motivation` | `longtext` | — | — |
| `name` | `string` | — | — |
| `narrativeStatus` | `enum` | `planned`·`active`·`inactive`·`retired`·`deceased` | — |
| `orderAxis` | `enum` | `lawful`·`neutral`·`chaotic` | — |
| `personality` | `longtext` | — | — |
| `powerLevel` | `string` | — | — |
| `powerSystemId` | `number` | — | — |
| `profile` | `string` | — | — |
| `raceEntryId` | `number` | — | — |
| `relationships` | `longtext` | — | — |
| `roleWeight` | `enum` | `main`·`secondary`·`npc`·`extra` | — |
| `shortDescription` | `longtext` | — | — |
| `signatureItem` | `string` | — | — |
| `speechStyle` | `longtext` | — | — |
| `statusEvidenceChapterId` | `number` | — | — |
| `statusEvidenceStoryArcId` | `number` | — | — |
| `statusProducerCandidateHash` | `string` | — | — |
| `statusProducerContractHash` | `string` | — | — |
| `statusReason` | `longtext` | — | — |
| `storyRole` | `longtext` | — | — |
| `strengths` | `longtext` | — | — |
| `values` | `longtext` | — | — |
| `weaknesses` | `longtext` | — | — |

### `characterRelations`（6 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `fromCharacterId` | `number` | — | — |
| `isBidirectional` | `boolean` | — | — |
| `label` | `string` | — | — |
| `relationType` | `enum` | `family`·`lover`·`friend`·`rival`·`enemy`·`master`·`student`·`ally`·`subordinate`·`other` | — |
| `toCharacterId` | `number` | — | — |

### `creativeRules`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `atmosphere` | `longtext` | — | — |
| `citedInsightIds` | `json` | — | — |
| `citedReferenceIds` | `json` | — | — |
| `consistencyRules` | `json` | — | — |
| `narrativePOV` | `enum` | `first-person`·`third-limited`·`third-omniscient`·`multi-pov` | — |
| `prohibitions` | `json` | — | — |
| `specialRequirements` | `longtext` | — | — |
| `writingStyle` | `longtext` | — | — |

### `outlineNodes`（6 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `order` | `number` | — | — |
| `parentId` | `number` | — | — |
| `summary` | `longtext` | — | — |
| `title` | `string` | — | — |
| `type` | `enum` | `volume`·`arc`·`storyBlock`·`chapter` | — |
| `worldGroupId` | `number` | — | — |

### `chapters`（13 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `content` | `longtext` | — | — |
| `continuityHandoff` | `object` | — | — |
| `notes` | `longtext` | — | — |
| `order` | `number` | — | — |
| `outlineNodeId` | `number` | — | — |
| `perspectiveCharacterId` | `number` | — | — |
| `planReconciliation` | `object` | — | — |
| `status` | `enum` | `outline`·`draft`·`revised`·`polished`·`final` | — |
| `summary` | `longtext` | — | — |
| `summarySourceTextHash` | `string` | — | — |
| `summaryTextNormalizationVersion` | `string` | — | — |
| `title` | `string` | — | — |
| `wordCount` | `number` | — | — |

### `detailedOutlines`（10 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `appearingCharacterIds` | `array` | — | — |
| `emotionArc` | `enum` | `rising`·`falling`·`flat`·`wave`·`climax` | — |
| `endingCliffhanger` | `longtext` | — | — |
| `foreshadowIds` | `array` | — | — |
| `lastUsedSummary` | `longtext` | — | — |
| `openingHook` | `longtext` | — | — |
| `outlineNodeId` | `number` | — | — |
| `prohibitions` | `array` | — | — |
| `sceneLocation` | `string` | — | — |
| `scenes` | `array` | — | — |

### `emotionBeatCards`（5 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `beats` | `json` | — | — |
| `chapterId` | `number` | — | — |
| `chapterTitle` | `string` | — | — |
| `overallArc` | `longtext` | — | — |
| `source` | `enum` | `ai`·`manual` | — |

### `foreshadows`（12 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `echoChapterIds` | `json` | — | — |
| `expectedResolveChapterId` | `number` | — | — |
| `importance` | `number` | — | — |
| `name` | `string` | — | — |
| `notes` | `longtext` | — | — |
| `plantChapterId` | `number` | — | — |
| `resolveChapterId` | `number` | — | — |
| `status` | `enum` | `planned`·`planted`·`echoed`·`resolved` | — |
| `timelinePosition` | `number` | — | — |
| `type` | `enum` | `chekhov`·`prophecy`·`symbol`·`character`·`dialogue`·`environment`·`timeline`·`red-herring`·`parallel`·`callback` | — |
| `urgency` | `enum` | `low`·`medium`·`high`·`critical` | — |

### `storyArcs`（12 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `lastAlignedHash` | `string` | — | — |
| `name` | `string` | — | — |
| `origin` | `enum` | `manual`·`ai`·`import` | — |
| `producerCandidateHash` | `string` | — | — |
| `producerRunId` | `number` | — | — |
| `sourceStoryCoreHash` | `string` | — | — |
| `sourceStoryCoreId` | `number` | — | — |
| `sourceStoryCoreRevision` | `number` | — | — |
| `stages` | `json` | — | — |
| `status` | `enum` | `active`·`deprecated` | — |
| `type` | `enum` | `main`·`sub` | — |

### `storylineProgress`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `arcId` | `number` | — | — |
| `currentStageId` | `string` | — | — |
| `evidenceQuote` | `longtext` | — | — |
| `involvedEntities` | `json` | — | — |
| `lastActiveChapterId` | `number` | — | — |
| `lastActiveChapterTitle` | `string` | — | — |
| `progressNote` | `longtext` | — | — |
| `status` | `enum` | `dormant`·`active`·`climax`·`resolved`·`abandoned` | — |

### `storylineCrossings`（6 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `arcIdA` | `number` | — | — |
| `arcIdB` | `number` | — | — |
| `chapterId` | `number` | — | — |
| `chapterTitle` | `string` | — | — |
| `evidenceQuote` | `longtext` | — | — |
| `note` | `longtext` | — | — |

### `codexCategories`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `builtInKey` | `string` | — | — |
| `domain` | `enum` | `natural`·`humanity`·`origin` | — |
| `fieldSchema` | `json` | — | — |
| `hidden` | `boolean` | — | — |
| `icon` | `string` | — | — |
| `name` | `string` | — | — |
| `order` | `number` | — | — |
| `parentId` | `number` | — | — |

### `codexEntries`（19 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `categoryId` | `number` | — | — |
| `cultivationStageId` | `string` | — | — |
| `cultivationSystemId` | `number` | — | — |
| `description` | `longtext` | — | — |
| `fields` | `json` | — | — |
| `icon` | `string` | — | — |
| `importance` | `number` | — | — |
| `importantLocationId` | `number` | — | — |
| `name` | `string` | — | — |
| `order` | `number` | — | — |
| `origin` | `enum` | `manual`·`verbatim-extraction`·`ai-created-suggestion`·`import` | — |
| `producerCandidateHash` | `string` | — | — |
| `producerRunId` | `number` | — | — |
| `refs` | `json` | — | — |
| `sourceContentHash` | `string` | — | — |
| `sourceEvidenceQuotes` | `json` | — | — |
| `summary` | `longtext` | — | — |
| `tags` | `json` | — | — |
| `worldGroupId` | `number` | — | — |

### `cultivationSystems`（4 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `name` | `string` | — | — |
| `stages` | `json` | — | — |
| `worldGroupId` | `number` | — | — |

### `cultivationProgress`（14 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `characterId` | `number` | — | — |
| `characterName` | `string` | — | — |
| `cultivationSystemId` | `number` | — | — |
| `cultivationSystemName` | `string` | — | — |
| `sourceChapterId` | `number` | — | — |
| `sourceChapterTitle` | `string` | — | — |
| `sourceOffset` | `number` | — | — |
| `sourceQuote` | `longtext` | — | — |
| `stageId` | `string` | — | — |
| `stageName` | `string` | — | — |
| `status` | `enum` | `confirmed`·`stale`·`source-missing` | — |
| `transition` | `enum` | `enter`·`advance`·`regress`·`switch` | — |
| `trigger` | `longtext` | — | — |
| `worldGroupId` | `number` | — | — |

### `importantLocations`（6 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `description` | `longtext` | — | — |
| `name` | `string` | — | — |
| `parentId` | `number` | — | — |
| `significance` | `longtext` | — | — |
| `sortOrder` | `number` | — | — |
| `tags` | `json` | — | — |

### `worldNodes`（1 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `mapConfigJSON` | `json` | — | — |

### `itemLedger`（8 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `action` | `enum` | `gain`·`consume` | — |
| `chapterId` | `number` | — | — |
| `chapterTitle` | `string` | — | — |
| `characterId` | `number` | — | — |
| `heldByName` | `string` | — | — |
| `itemName` | `string` | — | — |
| `note` | `longtext` | — | — |
| `quantity` | `number` | — | — |

### `knowledgeLedger`（12 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `action` | `enum` | `learn`·`mislearn`·`forget`·`correct` | — |
| `belief` | `longtext` | — | — |
| `characterId` | `number` | — | — |
| `characterName` | `string` | — | — |
| `factId` | `number` | — | — |
| `knowledgeKey` | `string` | — | — |
| `sourceChapterId` | `number` | — | — |
| `sourceQuote` | `longtext` | — | — |
| `sourceType` | `enum` | `chapter`·`manual`·`import` | — |
| `statement` | `longtext` | — | — |
| `status` | `enum` | `candidate`·`confirmed`·`rejected`·`source-missing`·`invalid-range` | — |
| `worldGroupId` | `number` | — | — |

### `storyTimelineEvents`（7 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `chapterId` | `number` | — | — |
| `chapterTitle` | `string` | — | — |
| `description` | `longtext` | — | — |
| `importance` | `number` | — | — |
| `order` | `number` | — | — |
| `storyTime` | `string` | — | — |
| `title` | `string` | — | — |

### `references`（10 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `analysisDepth` | `enum` | `quick`·`deep` | — |
| `analysisError` | `longtext` | — | — |
| `analysisProgress` | `number` | — | — |
| `analysisStatus` | `enum` | `none`·`pending`·`analyzing`·`done`·`failed` | — |
| `analysisSummary` | `longtext` | — | — |
| `fileHash` | `string` | — | — |
| `genre` | `string` | — | — |
| `importSessionId` | `number` | — | — |
| `mergedCharacters` | `longtext` | — | — |
| `totalChars` | `number` | — | — |

### `referenceAnalysisRuns`（20 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `activatedAt` | `number` | — | — |
| `analysisSummary` | `longtext` | — | — |
| `completedAt` | `number` | — | — |
| `completedChunks` | `number` | — | — |
| `depth` | `enum` | `quick`·`deep` | — |
| `error` | `longtext` | — | — |
| `expectedChunks` | `number` | — | — |
| `fileHash` | `string` | — | — |
| `mergedCharacters` | `longtext` | — | — |
| `progress` | `number` | — | — |
| `referenceId` | `number` | — | — |
| `rightsConfirmed` | `boolean` | — | — |
| `rightsDeclaredAt` | `number` | — | — |
| `rightsNote` | `longtext` | — | — |
| `sourceFilename` | `string` | — | — |
| `sourceKind` | `enum` | `own-work`·`authorized`·`public-domain`·`research`·`unknown` | — |
| `status` | `enum` | `analyzing`·`ready`·`active`·`superseded`·`failed`·`cancelled` | — |
| `totalChars` | `number` | — | — |
| `usageScope` | `enum` | `analysis-only`·`creative-reference`·`continuation-authorized` | — |
| `version` | `number` | — | — |

### `inspirationWorkspaces`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `fragments` | `json` | — | — |
| `versions` | `json` | — | — |

### `characterDrivenPlans`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `generatedVolumes` | `json` | — | — |
| `status` | `enum` | `draft`·`generated`·`adopted` | — |

### `referenceChunkAnalysis`（25 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `analysisRunId` | `number` | — | — |
| `characterCraft` | `longtext` | — | — |
| `chunkIndex` | `number` | — | — |
| `climaxDesign` | `longtext` | — | — |
| `conflictEscalation` | `longtext` | — | — |
| `dailyLife` | `longtext` | — | — |
| `dialogueTechnique` | `longtext` | — | — |
| `emotionalBeats` | `longtext` | — | — |
| `endOffset` | `number` | — | — |
| `foreshadowing` | `longtext` | — | — |
| `historicalContext` | `longtext` | — | — |
| `label` | `string` | — | — |
| `languageCustoms` | `longtext` | — | — |
| `materialCulture` | `longtext` | — | — |
| `narrativeStyle` | `longtext` | — | — |
| `openingTechnique` | `longtext` | — | — |
| `otherTechniques` | `longtext` | — | — |
| `pacingControl` | `longtext` | — | — |
| `plotStructure` | `longtext` | — | — |
| `proseStyle` | `longtext` | — | — |
| `rawExcerpt` | `longtext` | — | — |
| `referenceId` | `number` | — | — |
| `socialInstitutions` | `longtext` | — | — |
| `startOffset` | `number` | — | — |
| `worldBuilding` | `longtext` | — | — |

### `historicalTimelineEvents`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `aiBrainstorm` | `longtext` | — | — |
| `aiConsult` | `longtext` | — | — |

### `historicalKeywords`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `aiBrainstorm` | `longtext` | — | — |
| `aiConsult` | `longtext` | — | — |

### `userStyleProfiles`（5 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `enabled` | `boolean` | — | — |
| `profile` | `longtext` | — | — |
| `sampleCount` | `number` | — | — |
| `sampleWords` | `number` | — | — |
| `sourceChapterIds` | `json` | — | — |

### `productProductionBriefs`（2 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `briefJson` | `json` | — | — |
| `userIntentSummary` | `longtext` | — | — |

### `productBuilds`（5 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `compatibilityJson` | `json` | — | — |
| `manifestJson` | `json` | — | — |
| `planJson` | `json` | — | — |
| `previewManifestJson` | `json` | — | — |
| `qualityReportJson` | `json` | — | — |

### `productBuildArtifacts`（4 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `metadataJson` | `json` | — | — |
| `payloadJson` | `json` | — | — |
| `qualityJson` | `json` | — | — |
| `rightsJson` | `json` | — | — |

### `ttrpgRulePacks`（6 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `contentHash` | `string` | — | — |
| `rulePackJson` | `json` | — | — |
| `ruleSystemId` | `string` | — | — |
| `ruleSystemVersion` | `string` | — | — |
| `status` | `enum` | `draft`·`validated`·`archived` | — |
| `title` | `string` | — | — |

### `stateCards`（4 项）

| 字段 | 类型 | 枚举值 | AI 生成 |
| --- | --- | --- | --- |
| `category` | `enum` | `character`·`location`·`item`·`faction`·`event` | — |
| `entityName` | `string` | — | — |
| `fields` | `json` | — | — |
| `lastChapterId` | `number` | — | — |

## 2. 登记类型语义

| 登记类型 | 含义 |
| --- | --- |
| `string` | 短文本（登记时带 `trimString` 清洗） |
| `longtext` | 长文本（同上） |
| `number` / `boolean` | 数值 / 布尔 |
| `json` | **以 JSON 字符串形式存储**的复合结构 |
| `object` | IndexedDB **原生对象**字段（区别于以字符串存的 `json`） |
| `array` | 数组 |
| `enum` | 枚举，取值见「枚举值」列 |

## 3. `ADOPTION_SCHEMAS` — 集合表写回策略（**53 张表**）

> 单例表走 `FIELD_REGISTRY` 定位记录；**集合表必须在此登记** identity / 去重 / 盖章 / FK 策略。
> `identity` 的 `composite(...)` 表示复合键（`+` 连接各字段）。

| 表 | identity | 去重策略 | 必需字段 | 自动盖章 | 外键校验 | ownerFrom |
| --- | --- | --- | --- | --- | --- | --- |
| `adaptationCausalEdges` | `id` | `error` | — | `updatedAt` | — | `work` |
| `adaptationDecisions` | `id` | `error` | — | `updatedAt` | — | `work` |
| `adaptationProjects` | `id` | `error` | — | `updatedAt` | — | `work` |
| `adaptationSourceFacts` | `id` | `error` | — | `updatedAt` | — | `work` |
| `chapters` | `composite(outlineNodeId+title)` | `update` | `outlineNodeId`, `title` | `projectId`, `createdAt`, `updatedAt` | `outlineNodeId→outlineNodes`, `perspectiveCharacterId→characters` | `work` |
| `characterDrivenPlans` | `id` | `update` | — | `projectId`, `workId`, `createdAt`, `updatedAt` | — | `work` |
| `characterRelations` | `composite(fromCharacterId+toCharacterId+relationType)` | `skip` | `fromCharacterId`, `toCharacterId`, `relationType`, `label`, `isBidirectional` | `projectId`, `createdAt`, `updatedAt` | `fromCharacterId→characters`, `toCharacterId→characters` | `—` |
| `characters` | `composite(homeWorldGroupId+name)` | `merge` | `name`, `roleWeight`, `moralAxis`, `orderAxis` | `projectId`, `homeWorldGroupId`, `createdAt`, `updatedAt` | — | `—` |
| `codexCategories` | `composite(domain+parentId+name)` | `skip` | `domain`, `name` | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | `parentId→codexCategories` | `—` |
| `codexEntries` | `composite(worldGroupId+categoryId+name)` | `merge` | `categoryId`, `name` | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | `categoryId→codexCategories`, `importantLocationId→importantLocations` | `—` |
| `comicPagePlans` | `id` | `error` | — | `updatedAt` | — | `work` |
| `comicPages` | `id` | `error` | — | `updatedAt` | — | `work` |
| `comicPanels` | `id` | `error` | — | `updatedAt` | — | `work` |
| `comicReviewIssues` | `id` | `error` | — | `updatedAt` | — | `work` |
| `comicScriptBeats` | `id` | `error` | — | `updatedAt` | — | `work` |
| `comicVisualSubjects` | `id` | `error` | — | `updatedAt` | — | `work` |
| `creativeRules` | `id` | `error` | — | `projectId`, `workId`, `createdAt`, `updatedAt` | — | `work` |
| `cultivationProgress` | `composite(characterId+sourceChapterId+stageId+sourceQuote)` | `skip` | `characterId`, `characterName`, `cultivationSystemId`, `cultivationSystemName`, `stageId`, `stageName`, `transition`, `sourceChapterId`, `sourceChapterTitle`, `sourceQuote`, `sourceOffset`, `status` | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | `characterId→characters`, `cultivationSystemId→cultivationSystems`, `sourceChapterId→chapters` | `—` |
| `cultivationSystems` | `composite(worldGroupId+name)` | `merge` | `name`, `description`, `stages` | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | — | `—` |
| `detailedOutlines` | `composite(outlineNodeId)` | `update` | `outlineNodeId` | `projectId`, `createdAt`, `updatedAt` | `outlineNodeId→outlineNodes` | `work` |
| `emotionBeatCards` | `composite(chapterId)` | `update` | `chapterId`, `chapterTitle`, `overallArc`, `beats`, `source` | `projectId`, `createdAt`, `updatedAt` | `chapterId→chapters` | `work` |
| `foreshadows` | `name` | `merge` | `name`, `type`, `status`, `description` | `projectId`, `createdAt`, `updatedAt` | `plantChapterId→chapters`, `resolveChapterId→chapters`, `expectedResolveChapterId→chapters` | `—` |
| `historicalKeywords` | `id` | `update` | — | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | — | `—` |
| `historicalTimelineEvents` | `id` | `update` | — | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | — | `—` |
| `importantLocations` | `name` | `merge` | `name` | `projectId`, `createdAt`, `updatedAt` | `parentId→importantLocations` | `—` |
| `itemLedger` | `composite(chapterId+itemName+action+heldByName+note)` | `skip` | `itemName`, `action`, `quantity`, `heldByName` | `projectId`, `createdAt` | `chapterId→chapters`, `characterId→characters` | `—` |
| `knowledgeLedger` | `composite(characterId+knowledgeKey+action+sourceChapterId+statement)` | `skip` | `characterName`, `knowledgeKey`, `statement`, `action`, `sourceType`, `status` | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | `characterId→characters`, `factId→temporalFacts`, `sourceChapterId→chapters` | `—` |
| `motionDramaAssetSubjects` | `id` | `error` | — | `updatedAt` | — | `work` |
| `motionDramaEpisodes` | `id` | `error` | — | `updatedAt` | — | `work` |
| `motionDramaReviewIssues` | `id` | `error` | — | `updatedAt` | — | `work` |
| `motionDramaScriptScenes` | `id` | `error` | — | `updatedAt` | — | `work` |
| `motionDramaSeriesBibles` | `id` | `error` | — | — | — | `work` |
| `motionDramaShots` | `id` | `error` | — | `updatedAt` | — | `work` |
| `outlineNodes` | `composite(parentId+type+title)` | `skip` | `type`, `title` | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | `parentId→outlineNodes` | `—` |
| `projects` | `id` | `error` | — | `updatedAt` | — | `—` |
| `referenceAnalysisRuns` | `id` | `update` | — | `projectId`, `createdAt`, `updatedAt` | `referenceId→references` | `—` |
| `referenceChunkAnalysis` | `composite(analysisRunId+chunkIndex)` | `update` | `referenceId`, `analysisRunId`, `chunkIndex` | `createdAt` | `referenceId→references`, `analysisRunId→referenceAnalysisRuns` | `—` |
| `references` | `id` | `update` | — | `projectId`, `createdAt`, `updatedAt` | — | `—` |
| `screenplayBeats` | `id` | `error` | — | `updatedAt` | — | `work` |
| `screenplayReviewIssues` | `id` | `error` | — | `updatedAt` | — | `work` |
| `screenplaySceneCards` | `id` | `error` | — | `updatedAt` | — | `work` |
| `screenplayScenes` | `id` | `error` | — | `updatedAt` | — | `work` |
| `stateCards` | `composite(category+entityName)` | `merge` | `category`, `entityName`, `fields` | `projectId`, `createdAt`, `updatedAt` | `lastChapterId→chapters` | `—` |
| `storyArcs` | `name` | `merge` | `name`, `type` | `projectId`, `createdAt`, `updatedAt` | — | `—` |
| `storyCores` | `id` | `error` | — | `projectId`, `workId`, `createdAt`, `updatedAt` | — | `work` |
| `storyTimelineEvents` | `composite(chapterId+title)` | `update` | `title`, `importance` | `projectId`, `createdAt` | `chapterId→chapters` | `—` |
| `storylineCrossings` | `composite(arcIdA+arcIdB+chapterId)` | `update` | `arcIdA`, `arcIdB`, `note`, `evidenceQuote` | `projectId`, `createdAt`, `updatedAt` | `arcIdA→storyArcs`, `arcIdB→storyArcs`, `chapterId→chapters` | `—` |
| `storylineProgress` | `composite(arcId)` | `update` | `arcId`, `status`, `progressNote`, `involvedEntities` | `projectId`, `createdAt`, `updatedAt` | `arcId→storyArcs`, `lastActiveChapterId→chapters` | `—` |
| `ttrpgRulePacks` | `composite(ruleSystemId+ruleSystemVersion)` | `update` | `ruleSystemId`, `ruleSystemVersion`, `title`, `status`, `rulePackJson`, `contentHash` | `projectId`, `worldId`, `workId`, `createdAt`, `updatedAt` | — | `work` |
| `works` | `id` | `error` | — | `updatedAt` | — | `world` |
| `worldGroups` | `name` | `error` | `name`, `type`, `description`, `icon`, `order`, `entryCondition`, `powerRestriction`, `plannedChapterCount` | `projectId`, `worldId`, `createdAt`, `updatedAt` | — | `world` |
| `worldNodes` | `id` | `update` | — | `projectId`, `worldGroupId`, `createdAt`, `updatedAt` | — | `world` |
| `worlds` | `id` | `error` | — | `updatedAt` | — | `—` |

> `recordOnly` 为真（仅记录、不走集合采纳路径）的表：`adaptationCausalEdges`, `adaptationDecisions`, `adaptationProjects`, `adaptationSourceFacts`, `characterDrivenPlans`, `comicPagePlans`, `comicPages`, `comicPanels`, `comicReviewIssues`, `comicScriptBeats`, `comicVisualSubjects`, `creativeRules`, `historicalKeywords`, `historicalTimelineEvents`, `motionDramaAssetSubjects`, `motionDramaEpisodes`, `motionDramaReviewIssues`, `motionDramaScriptScenes`, `motionDramaSeriesBibles`, `motionDramaShots`, `projects`, `referenceAnalysisRuns`, `references`, `screenplayBeats`, `screenplayReviewIssues`, `screenplaySceneCards`, `screenplayScenes`, `storyCores`, `works`, `worldNodes`, `worlds`。

## 4. 只读表（无 FIELD_REGISTRY 条目）

以下表在 `schema-tables.md` 中有定义，但 **FIELD_REGISTRY 没有条目**（即 AI 不可写）：

| 表名 | 用途 | 说明 |
| --- | --- | --- |
| `temporalFacts` | 时间事实登记 | 由系统自动生成（从章节/大纲推导），AI 不直接写入。`knowledgeLedger.factId` 指向此表，但 AI 生成时通常留空或填 null |
| `narrativeSummaryNodes` | 叙事摘要节点 | 由系统自动生成（从大纲/章节聚合），AI 不直接写入 |

**契约矛盾**：`knowledgeLedger.factId` 的 FK 指向 `temporalFacts`，但该表无 FIELD_REGISTRY 条目。这意味着：
- AI 生成 `knowledgeLedger` 时，`factId` 字段留空（`null`）—— **不要填 0**（0 会被校验器判为悬空外键）
- 如果确实需要填写，必须先确认 `temporalFacts` 中存在对应记录（由系统生成）
- 这是上游 StoryForge 的设计决策，不是技能缺陷

**校验器行为**：`check_framework_artifact.py` 对写入这些表报 `TABLE_NOT_WRITABLE`（默认 WARN，`--strict` 下 ERROR）。
