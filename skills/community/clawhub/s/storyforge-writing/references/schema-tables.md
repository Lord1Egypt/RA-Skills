# Schema Tables — 表 / 字段参考（**机械生成，非手写**）

> **来源**：`H:\storyforge-main` 的 `src/lib/db/schema.ts`（Dexie，schema v10）与 `src/lib/types/*.ts`
> **生成**：2026-10-06，逐行抽取；上游 MIT（见 `NOTICE.md`），本文件是其数据结构的**派生索引**
> **规则**：与源码不一致时**以源码为准**，并重新生成本文件。

## 0. 三个权威来源（别混用）

| 权威 | 位置 | 管什么 |
| --- | --- | --- |
| **本文件** | `references/schema-tables.md` | 表清单 · store 规格（**索引字段**）· TS 接口（字段与类型） |
| **FIELD_REGISTRY** | `src/lib/registry/field-registry.ts`（799 行）+ `adoption-schema.ts`（1049 行） | **AI 可写字段的唯一登记处**：未登记即被运行时拒绝（`src/lib/agent/run/contract.ts:117` → `unknown_write_field`） |
| **PROJECT_TABLES** | `src/lib/registry/project-tables.ts` | 导出 / 导入 / 删除 / 世界切换清单的**派生来源** |

> ⚠️ **store 规格里的字段是「主键与索引」**（`++id` = 自增主键；`&` = 唯一索引；`[a+b]` = 复合索引），
> **不是完整字段集**。完整字段看下面的 TS 接口；**可写字段**看 FIELD_REGISTRY。

## 1. 契约涉及的重点表

> **本节已去重（2026-10-07 大扫除）**：原为 21 张重点表的逐字段表格，其内容已被
> 两处**全量**来源完全覆盖 ——
> - **store 规格** → §2「全部表索引」（123 张，完整）
> - **字段清单（含继承展开与取值域 `⟨…⟩`）** → §4「全表字段清单」（106 张 / 1734 项）
>
> 保留节号只为让既有交叉引用（`SKILL.md` / `COMPAT.md` 中的「§1」）继续可解析；
> **字段与 store 一律以 §2 / §4 为单一来源**，本节不再重复维护。

## 2. 全部表索引（123 张，完整 store 规格）

> 下表为 `STORYFORGE_STORES`（schema v10 唯一可写 schema）的**完整**展开；
> `++id` = 自增主键，`&` = 唯一索引，`[a+b]` = 复合索引，`*` 前缀为 multiEntry。

| 表 | store 规格（完整） |
| --- | --- |
| `adaptationCausalEdges` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], [adaptationProjectId+manifestVersion], relation, authorStatus, updatedAt` |
| `adaptationDecisions` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], [adaptationProjectId+manifestVersion], action, authorStatus, updatedAt` |
| `adaptationProjects` | `++id, projectId, worldId, &workId, sourceWorkId, sourceOutlineRootId, sourceStartChapterId, sourceEndChapterId, medium, status, updatedAt` |
| `adaptationSourceFacts` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], [adaptationProjectId+manifestVersion], kind, authorStatus, updatedAt` |
| `adaptationSourceUnits` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+sourceUnitKey], [adaptationProjectId+manifestVersion], sourceOutlineNodeId, sourceChapterId, order` |
| `agentConversations` | `++id, projectId, worldGroupId, status, updatedAt` |
| `agentEvents` | `++id, projectId, conversationId, durableRunId, [conversationId+sequence], kind, createdAt` |
| `agentRunArtifacts` | `++id, projectId, &[projectId+artifactKind+contentHash], contentHash, retentionState, createdAt` |
| `agentRunCheckpoints` | `++id, projectId, worldGroupId, runId, &[runId+throughSequence], createdAt` |
| `agentRunEvents` | `++id, projectId, worldGroupId, runId, &[runId+sequence], type, createdAt` |
| `agentRuns` | `++id, projectId, workId, productRuntimeSessionId, productBuildId, worldGroupId, conversationId, parentRunId, &[parentRunId+parentRelation], status, updatedAt` |
| `aiTownAuthoringDrafts` | `++id, projectId, worldId, &workId, worldReleaseId, productionId, updatedAt` |
| `aiUsageLog` | `++id, projectId, timestamp, category, model` |
| `avgAuthoringDrafts` | `++id, projectId, worldId, &workId, worldReleaseId, productionId, updatedAt` |
| `avgDraftMedia` | `++id, projectId, worldId, workId, blobObjectId` |
| `chapters` | `++id, projectId, outlineNodeId, order, status` |
| `characterDrivenPlans` | `++id, projectId, status, parentPlanId, updatedAt` |
| `characterRelations` | `++id, projectId, fromCharacterId, toCharacterId` |
| `characters` | `++id, projectId, name, roleWeight, moralAxis, orderAxis, statusEvidenceChapterId` |
| `chatAuthoringDrafts` | `++id, projectId, worldId, &workId, worldReleaseId, productionId, updatedAt` |
| `codexCategories` | `++id, projectId, domain, parentId, builtInKey, order` |
| `codexEntries` | `++id, projectId, categoryId, worldGroupId, order, producerRunId` |
| `comicMediaAssets` | `++id, projectId, workId, adaptationProjectId, &[workId+stableKey], role, origin, panelId, subjectKey, blobObjectId, disposition, requestHash, &[workId+requestHash+candidateIndex], updatedAt` |
| `comicPagePlans` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], &[adaptationProjectId+manifestVersion+pageNumber], [adaptationProjectId+manifestVersion], chapterNumber, order, updatedAt` |
| `comicPages` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+stableKey], &[adaptationProjectId+order], chapterNumber, status, updatedAt` |
| `comicPanels` | `++id, projectId, workId, pageId, &[workId+stableKey], &[pageId+order], status, updatedAt` |
| `comicReviewIssues` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], [adaptationProjectId+manifestVersion], pageKey, panelKey, category, severity, status, updatedAt` |
| `comicScriptBeats` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], [adaptationProjectId+manifestVersion], chapterNumber, sectionKey, order, updatedAt` |
| `comicVisualSubjects` | `++id, projectId, workId, adaptationProjectId, &[workId+stableKey], kind, characterId, locationRefKey, status, updatedAt` |
| `creationReleaseAssets` | `++id, projectId, worldId, workId, releaseId, &[releaseId+assetKey], blobObjectId, contentHash, createdAt` |
| `creationReleases` | `++id, projectId, worldId, workId, productKind, &[workId+productKind+version], contentHash, parentReleaseId, createdAt` |
| `creativeRules` | `++id, projectId` |
| `cultivationProgress` | `++id, projectId, worldGroupId, characterId, cultivationSystemId, sourceChapterId, status` |
| `cultivationSystems` | `++id, projectId, worldGroupId, name` |
| `detailedOutlines` | `++id, projectId, outlineNodeId` |
| `emotionBeatCards` | `++id, projectId, chapterId` |
| `foreshadows` | `++id, projectId, status, type` |
| `geographies` | `++id, projectId` |
| `historicalKeywords` | `++id, projectId, category, era` |
| `historicalTimelineEvents` | `++id, projectId, era, year` |
| `histories` | `++id, projectId` |
| `importFiles` | `sessionId, fileHash, createdAt` |
| `importJobs` | `++id, projectId, type, status, createdAt` |
| `importLogs` | `++id, sessionId, chunkIndex, createdAt` |
| `importSessions` | `++id, projectId, status, updatedAt, fileHash, targetWorldGroupId` |
| `importantLocations` | `++id, projectId, parentId, sortOrder` |
| `inspirationWorkspaces` | `++id, projectId, updatedAt` |
| `itemLedger` | `++id, projectId, itemName, chapterId` |
| `knowledgeLedger` | `++id, projectId, worldGroupId, characterId, knowledgeKey, factId, sourceChapterId, status` |
| `mediaBlobObjects` | `++id, projectId, worldId, workId, &[workId+contentHash], mimeType, disposition, storageState, leaseExpiresAt, byteSize, updatedAt` |
| `motionDramaAssetBindings` | `++id, projectId, workId, adaptationProjectId, episodeNumber, shotKey, subjectKey, assetVersionKey, updatedAt` |
| `motionDramaAssetSubjects` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+stableKey], manifestVersion, kind, authorStatus, updatedAt` |
| `motionDramaAssetVersions` | `++id, projectId, worldId, workId, adaptationProjectId, &[adaptationProjectId+stableKey], &[adaptationProjectId+subjectKey+version], subjectKey, blobObjectId, contentHash, updatedAt` |
| `motionDramaEpisodes` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+episodeNumber], &[adaptationProjectId+stableKey], manifestVersion, authorStatus, updatedAt` |
| `motionDramaProductions` | `++id, projectId, worldId, &workId, adaptationProjectId, phase, currentEpisodeNumber, currentReleaseId, updatedAt` |
| `motionDramaPromptOverrides` | `++id, projectId, workId, stage, scope, episodeNumber, &[workId+stage+scope+episodeNumber], updatedAt` |
| `motionDramaPromptPacks` | `++id, projectId, workId, adaptationProjectId, episodeNumber, provider, &[adaptationProjectId+episodeNumber+provider+version], maturity, contentHash, createdAt` |
| `motionDramaReviewIssues` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], manifestVersion, episodeNumber, sceneKey, shotKey, category, severity, status, updatedAt` |
| `motionDramaScriptScenes` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+stableKey], &[adaptationProjectId+episodeNumber+sceneNumber], manifestVersion, episodeNumber, order, updatedAt` |
| `motionDramaSeriesBibles` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+version], sourceManifestVersion, contentHash, createdAt` |
| `motionDramaShotReferences` | `++id, projectId, worldId, workId, adaptationProjectId, &[adaptationProjectId+stableKey], shotKey, role, subjectKey, assetVersionId, blobObjectId, selected, updatedAt` |
| `motionDramaShots` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+stableKey], &[adaptationProjectId+episodeNumber+order], manifestVersion, sceneKey, episodeNumber, order, updatedAt` |
| `narrativeBeats` | `++id, projectId, moduleId, nodeKey, &[moduleId+beatKey], [moduleId+nodeKey], speakerCharacterId, order` |
| `narrativeChoices` | `++id, projectId, moduleId, sourceNodeKey, &[moduleId+choiceKey], [moduleId+sourceNodeKey], targetNodeKey, order` |
| `narrativeModules` | `++id, projectId, worldId, workId, kind, status, updatedAt` |
| `narrativeNodes` | `++id, projectId, moduleId, sourceOutlineNodeId, order` |
| `narrativeSummaryNodes` | `++id, projectId, worldGroupId, level, sourceChapterId, sourceOutlineNodeId, status` |
| `nodeFlows` | `++id, projectId, worldGroupId, updatedAt` |
| `nodeRuns` | `++id, projectId, flowId, status, updatedAt` |
| `notes` | `++id, projectId, chapterId, pinned` |
| `outlineNodes` | `++id, projectId, parentId, order, type` |
| `ownershipScopeChanges` | `++id, projectId, worldId, workId, tableName, recordId, createdAt` |
| `powerSystems` | `++id, projectId` |
| `productBuildArtifacts` | `++id, projectId, worldId, workId, buildId, &[buildId+artifactKey+version], [buildId+status], [buildId+requirementKey], producerRunId, blobObjectId, contentHash, createdAt` |
| `productBuilds` | `++id, projectId, worldId, workId, productionId, &[productionId+buildNumber], [productionId+status], sourceProductReleaseId, packageHash, previewHash, releasedProductReleaseId, updatedAt` |
| `productMediaAssets` | `++id, projectId, worldId, workId, ownerKind, productType, productReleaseId, productRuntimeSessionId, &[productReleaseId+assetKey+version], &[productRuntimeSessionId+assetKey+version], [workId+productType], contentHash, updatedAt` |
| `productMediaBlobs` | `++id, projectId, worldId, workId, &mediaAssetId, blobObjectId` |
| `productProductionBriefs` | `++id, projectId, worldId, workId, productionId, &[productionId+revision], [productionId+briefHash], [productionId+status], sourceWorldReleaseId, sourcePlanHash, confirmedBriefHash, createdAt` |
| `productProductionCommands` | `++id, projectId, worldId, workId, productionId, &[productionId+commandId], [productionId+status], type, createdAt` |
| `productProductions` | `++id, projectId, worldId, workId, productType, &[workId+productionKey], [workId+productType], status, currentProductReleaseId, updatedAt` |
| `productQualityGateReceipts` | `++id, projectId, worldId, workId, buildId, &[buildId+gateId+receiptHash], [buildId+gateId], [buildId+status], gateId, status, createdAt` |
| `productReleases` | `++id, projectId, worldId, workId, productType, productionKey, worldReleaseId, &[workId+productionKey+version], [workId+productType], contentHash, createdAt` |
| `productRuntimeCheckpoints` | `++id, projectId, worldGroupId, sessionId, [sessionId+throughSequence], createdAt` |
| `productRuntimeEvents` | `++id, projectId, worldGroupId, sessionId, &[sessionId+sequence], &[sessionId+commandId], type, createdAt` |
| `productRuntimeSessions` | `++id, projectId, worldGroupId, worldId, workId, productReleaseId, productBuildId, runtimeSourceHash, kind, status, parentSessionId, updatedAt` |
| `projects` | `++id, &workspaceUid, workspacePurpose, name, createdAt, updatedAt` |
| `promptTemplates` | `++id, scope, moduleKey, isActive, updatedAt` |
| `promptWorkflows` | `++id, scope, isDefault, updatedAt` |
| `referenceAnalysisRuns` | `++id, projectId, referenceId, [referenceId+version], status, updatedAt` |
| `referenceAnalysisSources` | `analysisRunId, fileHash, createdAt` |
| `referenceChunkAnalysis` | `++id, referenceId, analysisRunId, [analysisRunId+chunkIndex], chunkIndex` |
| `references` | `++id, projectId, type, createdAt` |
| `retrievalChunks` | `++id, projectId, worldGroupId, sourceChapterId` |
| `screenplayBeats` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], [adaptationProjectId+manifestVersion], [adaptationProjectId+episodeNumber], sectionKey, order, updatedAt` |
| `screenplayReviewIssues` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], [adaptationProjectId+manifestVersion], sceneKey, category, severity, status, updatedAt` |
| `screenplaySceneCards` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+manifestVersion+stableKey], &[adaptationProjectId+episodeNumber+sceneNumber], [adaptationProjectId+manifestVersion], beatKey, order, updatedAt` |
| `screenplayScenes` | `++id, projectId, workId, adaptationProjectId, &[adaptationProjectId+stableKey], &[adaptationProjectId+episodeNumber+sceneNumber], [adaptationProjectId+episodeNumber], order, status, updatedAt` |
| `shortNovelProductions` | `++id, projectId, worldId, &workId, phase, currentReleaseId, updatedAt` |
| `snapshots` | `++id, projectId, type, createdAt` |
| `stateCards` | `++id, projectId, category, entityName, lastChapterId` |
| `storyArcs` | `++id, projectId, type, sourceStoryCoreId, producerRunId` |
| `storyCores` | `++id, projectId` |
| `storyTimelineEvents` | `++id, projectId, chapterId, order` |
| `storylineCrossings` | `++id, projectId, arcIdA, arcIdB, chapterId` |
| `storylineProgress` | `++id, &arcId, projectId, status, lastActiveChapterId` |
| `temporalFacts` | `++id, projectId, worldGroupId, characterId, locationId, codexEntryId, predicate, status, sourceChapterId` |
| `ttrpgAuthoringDrafts` | `++id, projectId, worldId, &workId, worldReleaseId, productionId, savedRulePackId, updatedAt` |
| `ttrpgRulePacks` | `++id, projectId, worldId, workId, &[workId+ruleSystemId+ruleSystemVersion], [workId+status], contentHash, updatedAt` |
| `ttrpgRuntimeAssetRequests` | `++id, projectId, worldGroupId, worldId, workId, sessionId, &[sessionId+requestKey], [sessionId+slotKey], [sessionId+status], priority, mediaAssetId, processorLeaseExpiresAt, updatedAt` |
| `ttrpgSessionParticipants` | `++id, projectId, worldGroupId, worldId, workId, sessionId, &[sessionId+seatKey], &[sessionId+viewerKey], [sessionId+actorKey], role, controller, assignmentState, updatedAt` |
| `userStyleProfiles` | `++id, projectId` |
| `workCharacterBindings` | `++id, projectId, workId, characterId, &[workId+characterId], [projectId+workId]` |
| `works` | `++id, projectId, worldId, code, &[projectId+code], [projectId+worldId], [worldId+updatedAt], status, activeNarrativeModuleId` |
| `workspaceDocuments` | `++id, projectId, workspaceUid, documentId, &[projectId+documentId], relativePath, &[projectId+relativePath], tableName, recordId, &[projectId+tableName+recordId], worldCode, workCode, lastSyncRunId, updatedAt` |
| `worldDerivations` | `++id, projectId, worldId, sourceWorkspaceUid, sourceWorkCode, sourceContentHash, targetRevisionId, targetReleaseId, createdAt` |
| `worldGroupLinks` | `++id, projectId, fromGroupId, toGroupId` |
| `worldGroups` | `++id, projectId, type, order` |
| `worldNodes` | `++id, projectId, parentId, sortOrder` |
| `worldReleases` | `++id, releaseUid, projectId, worldId, revisionId, version, contentHash, createdAt` |
| `worldRevisions` | `++id, projectId, worldId, parentRevisionId, revision, contentHash, updatedAt` |
| `worldRulesProfiles` | `++id, projectId, worldGroupId` |
| `worlds` | `++id, projectId, identityKind, code, [projectId+identityKind], [projectId+updatedAt]` |
| `worldviews` | `++id, projectId` |

## 3. `FIELD_REGISTRY`（AI 可写字段）

> 位置：`src/lib/registry/field-registry.ts`；采纳扩展：`adoption-schema.ts`；
> 校验：`adopt.ts`（field/schema/外键/owner/作用域/stale 六项）。
>
> ✅ **逐表可写字段清单已抽取** → 见 **`references/field-registry.md`**
> （64 张表 / 528 项可写字段 + 25 项「AI 生成启用」子集 + 53 张集合表的写回策略）。
> 本文件只承载"表 / store 规格 / TS 接口"；**"AI 能写什么"以 `field-registry.md` 为准**。

## 4. 全表字段清单（106 表，机械抽取）

> **来源**：`src/lib/export/json-export.ts` 的 `ProjectExportData`（**权威「表 → TS 类型」映射**）＋ `src/lib/types/*.ts`（接口定义，含**继承链展开**）。
> **读法**：`字段?:类型`（`?` = 可选）；`⟨…⟩` = **取值域**（枚举闭集）；类型里的 `| null` 等原样保留。
> **「导出」行**：该表在导出信封里会做 `Omit<…>` 并附加 `_xxxExportId` —— 语料按**接口字段**写，导出加工由上游完成。
> **与其它文件的分工**：本节是**数据模型全貌**；「AI 能写什么」以 `field-registry.md` 为准；store 规格见 §2（**表名与 store 的单一来源**）；§1 已去重为空存根。
> **信封根字段（非表，见 `contracts/S-data-envelope.md`）**：
> `version`:number（必须 `14`）· `exportedAt`:number · `ownership`:{`contractVersion`,`worldExportId`,`workExportId`} · `project`（工作区根，`Project` 接口，**精确键集**见该契约 §1.1）

### `adaptationCausalEdges`

> 接口 `AdaptationCausalEdgeV1`（14 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`fromFactKey`:string  `toFactKey`:string  `relation`:AdaptationCausalRelationV1⟨cause·enables·motivates·reveals·prevents⟩
`rationale`:string  `sourceUnitKeys`:string[]  `authorStatus`:AdaptationAuthorStatusV1⟨confirmed·rejected⟩
`createdAt`:number  `updatedAt`:number
```

### `adaptationDecisions`

> 接口 `AdaptationDecisionV1`（13 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`action`:AdaptationDecisionActionV1⟨keep·cut·merge·reorder·externalize·add⟩  `sourceFactKeys`:string[]  `targetKeys`:string[]
`rationale`:string  `authorStatus`:AdaptationAuthorStatusV1⟨confirmed·rejected⟩  `createdAt`:number
`updatedAt`:number
```

### `adaptationProjects`

> ⚠️ 未在 `types/*.ts` 解析到接口 `AdaptationProject` 的字段 —— 请直接读源文件（本节不推断）。

### `adaptationSourceFacts`

> 接口 `AdaptationSourceFactV1`（14 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`kind`:AdaptationSourceFactKindV1⟨event·character-state·relationship·location·object·motif⟩  `statement`:string  `subjectKeys`:string[]
`sourceUnitKeys`:string[]  `confidence`:number  `authorStatus`:AdaptationAuthorStatusV1⟨confirmed·rejected⟩
`createdAt`:number  `updatedAt`:number
```

### `adaptationSourceUnits`

> 接口 `AdaptationSourceUnit`（16 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`·`sourceOutlineNodeId`·`sourceChapterId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `sourceKind`:AdaptationSourceUnitKind⟨work·outline-node·chapter⟩
`sourceOutlineNodeId`:number | null  `sourceChapterId`:number | null  `sourceUnitKey`:string
`order`:number  `label`:string  `contentHash`:string
`summary`:string  `wordCount`:number  `sourceUpdatedAt`:number | null
`createdAt`:number
```

### `agentConversations`

> 接口 `AgentConversation`（9 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `workId?`:number | null
`worldGroupId?`:number | null  `purpose`:string  `title`:string
`status`:'active' | 'archived'⟨active·archived⟩  `createdAt`:number  `updatedAt`:number
```

### `agentEvents`

> 接口 `AgentEvent`（11 项）；导出 `Omit`：`id`·`projectId`·`conversationId`·`durableRunId`

```text
`id?`:number  `projectId`:number  `workId?`:number | null
`conversationId`:number  `durableRunId`:number | null  `sequence`:number
`kind`:AgentEventKind  `role?`:'user' | 'assistant' | 'system'⟨user·assistant·system⟩  `content`:string
`payload`:string  `createdAt`:number
```

### `agentRunArtifacts`

> 接口 `AgentRunArtifactRecordV1`（12 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `encoding`:'utf-8'
`byteLength`:number  `content`:string | null  `retentionState`:ExactRunArtifactRetentionStateV1⟨available·evidence-pruned⟩
`pruneReceiptJson`:string | null  `pruneReceiptHash`:string | null  `createdAt`:number
`updatedAt`:number  `artifactKind`:ExactRunArtifactKindV1⟨context-manifest·selector-result·context-packet·source-snapshot·tool-result·rendered-request·raw-response⟩  `contentHash`:string
```

### `agentRunCheckpoints`

> 接口 `AgentRunCheckpointRecord`（13 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`·`runId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`runId`:number  `throughSequence`:number  `generation`:number
`contractHash`:string  `checkpointHash`:string  `projectionJson`:string
`projectionHash`:string  `resumePayloadJson?`:string | null  `resumePayloadHash?`:string | null
`createdAt`:number
```

### `agentRunEvents`

> 接口 `AgentRunEventRecord`（10 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`·`runId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`runId`:number  `sequence`:number  `generation`:number
`contractHash`:string  `type`:AgentRunEventTypeV1⟨run.created·contract.accepted·contract.revised·plan.replanned·step.scheduled·step.started·step.succeeded·step.failed·context.assembled·evidence.artifact.recorded·model.requested·model.responded·tool.called·tool.returned·candidate.persisted·candidate.revised·candidate.staled·candidate.carried-forward·runtime.candidate.adopted·step.verification.accepted·step.verification.staled·confirmation.recorded·adoption.started·adoption.committed·adoption.rejected·verification.started·verification.accepted·memory.settlement.recorded·verification.rejected·verification.staled·checkpoint.created·recovery.started·recovery.completed·budget.reserved·budget.settled·budget.exhausted·run.paused·run.cancelled·run.failed⟩  `payloadJson`:string
`createdAt`:number
```

### `agentRuns`

> 接口 `AgentRunRecord`（7 项）；导出 `Omit`：`id`·`projectId`·`workId`·`productRuntimeSessionId`·`productBuildId`·`worldGroupId`·`conversationId`·`parentRunId`

```text
`id?`:number  `projectId`:number  `workId?`:number | null
`productRuntimeSessionId?`:number | null  `productBuildId?`:number | null  `worldGroupId?`:number | null
`conversationId?`:number | null
```

### `avgAuthoringDrafts`

> ⚠️ 未在 `types/*.ts` 解析到接口 `AvgAuthoringDraftV1` 的字段 —— 请直接读源文件（本节不推断）。

### `avgDraftMedia`

> ⚠️ 未在 `types/*.ts` 解析到接口 `AvgDraftMediaV1` 的字段 —— 请直接读源文件（本节不推断）。

### `chapters`

> 接口 `Chapter`（21 项）；导出 `Omit`：`id`·`projectId`·`outlineNodeId`

```text
`id?`:number  `projectId`:number  `outlineNodeId`:number
`title`:string  `content`:string  `wordCount`:number
`status`:ChapterStatus⟨outline·draft·revised·polished·final⟩  `order`:number  `notes`:string
`perspectiveCharacterId?`:number | null  `summary?`:string  `continuityHandoff?`:ChapterContinuityHandoff
`summarySourceTextHash?`:string  `summaryTextNormalizationVersion?`:string  `planReconciliation?`:ChapterPlanReconciliation
`createdAt`:number  `updatedAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `characterDrivenPlans`

> 接口 `CharacterDrivenPlan`（11 项）；导出 `Omit`：`id`·`projectId`·`parentPlanId`

```text
`id?`:number  `projectId`:number  `name`:string
`arcs`:string  `userHint`:string  `generatedVolumes`:string
`status`:CharacterDrivenPlanStatus⟨draft·generated·adopted⟩  `version`:number  `parentPlanId`:number | null
`createdAt`:number  `updatedAt`:number
```

### `characterRelations`

> 接口 `CharacterRelation`（14 项）；导出 `Omit`：`id`·`projectId`·`fromCharacterId`·`toCharacterId`

```text
`id?`:number  `projectId`:number  `fromCharacterId`:number
`toCharacterId`:number  `relationType`:RelationType⟨family·lover·friend·rival·enemy·master·student·ally·subordinate·other⟩  `label`:string
`description`:string  `isBidirectional`:boolean  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `characters`

> 接口 `Character`（53 项）；导出 `Omit`：`id`·`projectId`·`homeWorldGroupId`

```text
`id?`:number  `projectId`:number  `name`:string
`roleWeight`:CharacterRoleWeight⟨main·secondary·npc·extra⟩  `moralAxis`:CharacterMoralAxis⟨good·neutral·evil⟩  `orderAxis`:CharacterOrderAxis⟨lawful·neutral·chaotic⟩
`shortDescription`:string  `appearance`:string  `personality`:string
`background`:string  `motivation`:string  `abilities`:string
`relationships`:string  `arc`:string  `identity?`:string
`profile?`:string  `values?`:string  `strengths?`:string
`weaknesses?`:string  `fears?`:string  `goals?`:string
`innerConflict?`:string  `keyEvents?`:string  `powerLevel?`:string
`speechStyle?`:string  `habits?`:string  `signatureItem?`:string
`location?`:string  `firstAppearance?`:string  `storyRole?`:string
`ending?`:string  `firstAppearChapterId?`:number | null  `activeChapterRange?`:string
`exitChapterId?`:number | null  `narrativeStatus?`:CharacterNarrativeStatus⟨planned·active·inactive·retired·deceased⟩  `statusEvidenceChapterId?`:number | null
`statusEvidenceStoryArcId?`:number | null  `statusReason?`:string  `statusProducerContractHash?`:string | null
`statusProducerCandidateHash?`:string | null  `homeWorldGroupId?`:number | null  `isCrossWorld?`:boolean
`raceEntryId?`:number | null  `cultivationSystemId?`:number | null  `powerSystemId?`:number | null
`cultivationStageId?`:string | null  `importantLocationId?`:number | null  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `codexCategories`

> 接口 `CodexCategory`（16 项）；导出 `Omit`：`id`·`projectId`·`parentId`

```text
`id?`:number  `projectId`:number  `domain`:CodexDomain⟨natural·humanity·origin⟩
`parentId`:number | null  `name`:string  `icon?`:string
`builtInKey?`:BuiltInCodexKey⟨mineral·herb·beast·race·faction·city·artifact·natStructure·natDimension·natTerrain·natWater·natClimate·humEra·humEvent·humSociety·humPolitics·humEconomy·humCulture·humConflict·originPower·originDeity⟩  `fieldSchema`:string  `hidden?`:boolean
`order`:number  `createdAt`:number  `updatedAt`:number
`ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number
`ragPolicyHash?`:string
```

### `codexEntries`

> 接口 `CodexEntry`（27 项）；导出 `Omit`：`id`·`projectId`·`categoryId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `categoryId`:number
`name`:string  `icon?`:string  `summary`:string
`description`:string  `fields`:string  `refs?`:string
`tags?`:string  `importance?`:number  `cultivationSystemId?`:number | null
`cultivationStageId?`:string | null  `importantLocationId?`:number | null  `origin`:'manual' | 'verbatim-extraction' | 'ai-created-suggestion' | 'import'⟨manual·verbatim-extraction·ai-created-suggestion·import⟩
`sourceEvidenceQuotes`:string  `sourceContentHash`:string  `producerRunId`:number | null
`producerCandidateHash`:string | null  `order`:number  `worldGroupId?`:number | null
`createdAt`:number  `updatedAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `comicMediaAssets`

> 接口 `ComicMediaAsset`（20 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`·`panelId`·`blobObjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `stableKey`:string  `role`:ComicMediaAssetRole⟨panel-render·character-sheet·location-sheet·prop-sheet·style-reference⟩
`panelId`:number | null  `subjectKey`:string | null  `blobObjectId`:number
`origin`:'generated' | 'uploaded'⟨generated·uploaded⟩  `candidateIndex`:number  `requestHash`:string | null
`promptHash`:string | null  `referenceAssetKeys`:string[]  `providerReceipt`:MediaProviderReceiptV1 | null
`rights`:MediaRightsV1  `quality`:ComicRenderQualityV1  `disposition`:'available' | 'rejected'⟨available·rejected⟩
`createdAt`:number  `updatedAt`:number
```

### `comicPagePlans`

> 接口 `ComicPagePlanV1`（19 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`chapterNumber`:number  `pageNumber`:number  `order`:number
`goal`:string  `beatKeys`:string[]  `endReveal`:string
`pageTurn`:'none' | 'setup' | 'reveal-after-turn' | 'cliffhanger'⟨none·setup·reveal-after-turn·cliffhanger⟩  `expectedPanelCount`:number  `textBudget`:number
`authorStatus`:'confirmed'  `revision`:number  `createdAt`:number
`updatedAt`:number
```

### `comicPages`

> 接口 `ComicPage`（14 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `stableKey`:string  `pagePlanKey?`:string
`chapterNumber`:number  `order`:number  `allowPanelOverlap`:boolean
`summary`:string  `status`:ComicPageStatus⟨planned·storyboarded·reviewed·locked⟩  `revision`:number
`createdAt`:number  `updatedAt`:number
```

### `comicPanels`

> 接口 `ComicPanel`（30 项）；导出 `Omit`：`id`·`projectId`·`workId`·`pageId`·`sourceUnitIds`

```text
`id?`:number  `projectId`:number  `workId`:number
`pageId`:number  `stableKey`:string  `order`:number
`nextPanelKey?`:string | null  `frame`:ComicNormalizedFrameV1  `sourceUnitIds`:number[]
`sourceReviewManifestVersion`:number  `shot`:ComicShotV1  `narrativeFunction?`:string
`moment?`:string  `action`:string  `visualPrompt`:string
`negativePrompt`:string  `continuityRefs`:ComicContinuityRefV1[]  `subjectStates?`:ComicSubjectStateV1[]
`protectedAreas?`:ComicNormalizedFrameV1[]  `lettering`:ComicLetteringItemV1[]  `selectedMediaAssetKey`:string | null
`imageTransform`:ComicImageTransformV1  `status`:ComicPanelStatus⟨draft·reviewed·locked⟩  `narrativeReviewRevision?`:number | null
`visualReviewRevision?`:number | null  `visualReviewBasis?`:'author-visual' | 'model-multimodal' | null⟨author-visual·model-multimodal⟩  `visualReviewedAt?`:number | null
`revision`:number  `createdAt`:number  `updatedAt`:number
```

### `comicReviewIssues`

> 接口 `ComicReviewIssueV1`（20 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`category`:ComicReviewCategoryV1⟨narrative·reading-order·lettering·continuity·rights·media-integrity⟩  `severity`:ComicReviewSeverityV1⟨critical·major·minor⟩  `pageKey`:string
`panelKey`:string | null  `subjectKey`:string | null  `assetKey`:string | null
`evidence`:string  `problem`:string  `suggestion`:string
`sourceUnitKeys`:string[]  `reviewedPanelRevision`:number | null  `status`:'open' | 'resolved' | 'dismissed'⟨open·resolved·dismissed⟩
`createdAt`:number  `updatedAt`:number
```

### `comicScriptBeats`

> 接口 `ComicScriptBeatV1`（21 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`sectionKey`:string  `chapterNumber`:number  `order`:number
`narrativeFunction`:'establish' | 'develop' | 'reveal' | 'reaction' | 'turn' | 'climax' | 'resolution' | 'transition'⟨establish·develop·reveal·reaction·turn·climax·resolution·transition⟩  `visualAction`:string  `dialogueIntent`:string
`emotion`:string  `causalFactKeys`:string[]  `decisionKeys`:string[]
`sourceUnitKeys`:string[]  `estimatedPanels`:number  `authorStatus`:'confirmed'
`revision`:number  `createdAt`:number  `updatedAt`:number
```

### `comicVisualSubjects`

> 接口 `ComicVisualSubject`（17 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`·`characterId`·`sourceUnitIds`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `stableKey`:string  `kind`:ComicVisualSubjectKind⟨character·location·prop·style⟩
`characterId`:number | null  `locationRefKey`:string | null  `label`:string
`design`:ComicVisualSubjectDesignV1  `sourceUnitIds`:number[]  `sourceReviewManifestVersion`:number
`selectedMediaAssetKey`:string | null  `status`:ComicPanelStatus⟨draft·reviewed·locked⟩  `revision`:number
`createdAt`:number  `updatedAt`:number
```

### `creationReleaseAssets`

> 接口 `CreationReleaseAssetV1`（13 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`releaseId`·`blobObjectId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `releaseId`:number  `assetKey`:string
`role`:ComicMediaAssetRole | 'motion-subject-reference' | 'motion-shot-reference' | 'motion-audio-reference'⟨motion-subject-reference·motion-shot-reference·motion-audio-reference⟩  `pageKey`:string | null  `panelKey`:string | null
`blobObjectId`:number  `contentHash`:string  `referenceAssetKeys`:string[]
`createdAt`:number
```

### `creationReleases`

> 接口 `CreationReleaseV1`（12 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`parentReleaseId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `productKind`:CreationProductKindV1⟨short-novel·screenplay·comic·motion-drama⟩  `version`:number
`label`:string  `parentReleaseId`:number | null  `sourceRevision`:number
`manifestJson`:string  `contentHash`:string  `createdAt`:number
```

### `creativeRules`

> 接口 `CreativeRules`（12 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `writingStyle`:string
`narrativePOV`:NarrativePOV⟨first-person·third-limited·third-omniscient·multi-pov⟩  `atmosphere`:string  `prohibitions`:string
`consistencyRules`:string  `specialRequirements`:string  `citedReferenceIds?`:string
`citedInsightIds?`:string  `createdAt`:number  `updatedAt`:number
```

### `cultivationProgress`

> 接口 `CultivationProgress`（18 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`characterId?`:number | null  `characterName`:string  `cultivationSystemId?`:number | null
`cultivationSystemName`:string  `stageId?`:string | null  `stageName`:string
`transition`:CultivationTransition  `sourceChapterId?`:number | null  `sourceChapterTitle`:string
`sourceQuote`:string  `sourceOffset`:number  `trigger`:string
`status`:CultivationProgressStatus  `createdAt`:number  `updatedAt`:number
```

### `cultivationSystems`

> 接口 `CultivationSystem`（8 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `name`:string
`description`:string  `stages`:string  `worldGroupId?`:number | null
`createdAt`:number  `updatedAt`:number
```

### `detailedOutlines`

> 接口 `DetailedOutline`（14 项）；导出 `Omit`：`id`·`projectId`·`outlineNodeId`

```text
`id?`:number  `projectId`:number  `outlineNodeId`:number
`scenes`:DetailedScene[]  `openingHook?`:string  `endingCliffhanger?`:string
`sceneLocation?`:string  `appearingCharacterIds?`:number[]  `foreshadowIds?`:number[]
`emotionArc?`:EmotionArc⟨rising·falling·flat·wave·climax⟩  `prohibitions?`:string[]  `lastUsedSummary?`:string
`createdAt`:number  `updatedAt`:number
```

### `emotionBeatCards`

> 接口 `EmotionBeatCard`（9 项）；导出 `Omit`：`id`·`projectId`·`chapterId`

```text
`id?`:number  `projectId`:number  `chapterId`:number
`chapterTitle`:string  `overallArc`:string  `beats`:EmotionBeat[]
`source`:'ai' | 'manual'⟨ai·manual⟩  `createdAt`:number  `updatedAt`:number
```

### `foreshadows`

> 接口 `Foreshadow`（20 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `name`:string
`type`:ForeshadowType⟨chekhov·prophecy·symbol·character·dialogue·environment·timeline·red-herring·parallel·callback⟩  `status`:ForeshadowStatus⟨planned·planted·echoed·resolved⟩  `description`:string
`plantChapterId`:number | null  `echoChapterIds`:string  `resolveChapterId`:number | null
`notes`:string  `timelinePosition?`:number  `expectedResolveChapterId?`:number | null
`importance?`:number  `urgency?`:ForeshadowUrgency⟨low·medium·high·critical⟩  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `geographies`

> 接口 `Geography`（8 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `overview`:string
`locations`:string  `worldMapData?`:string  `worldGroupId?`:number | null
`createdAt`:number  `updatedAt`:number
```

### `historicalKeywords`

> 接口 `HistoricalKeyword`（17 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `keyword`:string
`category`:HistoricalKeywordCategory⟨technology·institution·culture·economy·architecture⟩  `era`:HistoricalEra | string  `description`:string
`conceptNote?`:string  `aiBrainstorm?`:string  `aiConsult?`:string
`consultPrompt?`:string  `stormPrompt?`:string  `relatedChapterIds?`:number[]
`customTimeRange?`:string  `location?`:string  `worldGroupId?`:number | null
`createdAt`:number  `updatedAt`:number
```

### `historicalTimelineEvents`

> 接口 `HistoricalTimelineEvent`（21 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `era`:HistoricalEra | string
`year`:number  `date`:string  `title`:string
`description`:string  `conceptNote?`:string  `impact?`:string
`isHistorical`:boolean  `source?`:string  `aiBrainstorm?`:string
`aiConsult?`:string  `consultPrompt?`:string  `stormPrompt?`:string
`relatedChapterIds?`:number[]  `customTimeRange?`:string  `location?`:string
`worldGroupId?`:number | null  `createdAt`:number  `updatedAt`:number
```

### `histories`

> 接口 `History`（12 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `overview`:string
`eraSystem`:string  `events`:string  `worldGroupId?`:number | null
`createdAt`:number  `updatedAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `importantLocations`

> 接口 `ImportantLocation`（14 项）；导出 `Omit`：`id`·`projectId`·`parentId`

```text
`id?`:number  `projectId`:number  `name`:string
`tags`:string  `description`:string  `significance`:string
`parentId`:number | null  `sortOrder`:number  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `inspirationWorkspaces`

> 接口 `InspirationWorkspace`（7 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `workId?`:number | null
`fragments`:string  `versions`:string  `createdAt`:number
`updatedAt`:number
```

### `itemLedger`

> 接口 `ItemLedgerEntry`（15 项）；导出 `Omit`：`id`·`projectId`·`chapterId`

```text
`id?`:number  `projectId`:number  `itemName`:string
`action`:ItemLedgerAction⟨gain·consume⟩  `quantity`:number  `heldByName`:string
`characterId?`:number | null  `chapterId?`:number | null  `chapterTitle?`:string
`note?`:string  `createdAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `knowledgeLedger`

> 接口 `KnowledgeLedgerEntry`（17 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `workId?`:number | null
`worldGroupId?`:number | null  `characterId?`:number | null  `characterName`:string
`knowledgeKey`:string  `statement`:string  `factId?`:number | null
`action`:KnowledgeAction⟨learn·mislearn·forget·correct⟩  `belief?`:string | null  `sourceType`:KnowledgeSourceType⟨chapter·manual·import⟩
`sourceChapterId?`:number | null  `sourceQuote?`:string  `status`:KnowledgeEventStatus⟨candidate·confirmed·rejected·source-missing·invalid-range⟩
`createdAt`:number  `updatedAt`:number
```

### `mediaBlobObjects`

> 接口 `MediaBlobObjectRecordV1`（21 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`data`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `contentHash`:string  `mimeType`:string
`byteSize`:number  `backend`:"indexeddb" | "opfs"  `storageState`:"pending-write" | "ready" | "pending-delete" | "corrupt"
`data`:ArrayBuffer | null  `opfsPath`:string | null  `leaseOwner`:string | null
`leaseExpiresAt`:number | null  `lastVerifiedAt`:number | null  `width?`:number
`height?`:number  `disposition?`:"available" | "pending-delete"  `deleteRequestedAt?`:number | null
`deleteReceiptHash?`:string | null  `createdAt`:number  `updatedAt`:number
```

### `motionDramaAssetBindings`

> 接口 `MotionDramaAssetBindingV1`（11 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `episodeNumber`:number  `shotKey`:string | null
`subjectKey`:string  `assetVersionKey`:string | null  `usage`:string
`createdAt`:number  `updatedAt`:number
```

### `motionDramaAssetSubjects`

> 接口 `MotionDramaAssetSubjectV1`（23 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`kind`:MotionDramaAssetKindV1⟨character·costume·location·prop·style·voice·sound⟩  `label`:string  `identity`:string
`appearance`:string  `palette`:string[]  `materials`:string[]
`continuityLocks`:string[]  `prohibitedChanges`:string[]  `basePrompt`:string
`negativePrompt`:string  `referenceBrief`:string  `sourceUnitKeys`:string[]
`selectedVersionKey`:string | null  `authorStatus`:MotionDramaAuthorStatusV1  `revision`:number
`createdAt`:number  `updatedAt`:number
```

### `motionDramaAssetVersions`

> 接口 `MotionDramaAssetVersionV1`（19 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`adaptationProjectId`·`blobObjectId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `adaptationProjectId`:number  `subjectKey`:string
`stableKey`:string  `version`:number  `prompt`:string
`negativePrompt`:string  `referenceNotes`:string  `blobObjectId`:number | null
`origin`:'prompt-only' | 'author-upload' | 'provider-generated'⟨prompt-only·author-upload·provider-generated⟩  `provider`:string | null  `model`:string | null
`rights`:MediaRightsV1 | null  `contentHash`:string  `createdAt`:number
`updatedAt`:number
```

### `motionDramaEpisodes`

> 接口 `MotionDramaEpisodeV1`（20 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`episodeNumber`:number  `title`:string  `logline`:string
`synopsis`:string  `openingHook`:string  `beats`:MotionDramaEpisodeBeatV1[]
`endHook`:string  `continuityIn`:string[]  `continuityOut`:string[]
`sourceUnitKeys`:string[]  `authorStatus`:MotionDramaAuthorStatusV1  `revision`:number
`createdAt`:number  `updatedAt`:number
```

### `motionDramaProductions`

> 接口 `MotionDramaProductionV1`（12 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`adaptationProjectId`·`currentReleaseId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `adaptationProjectId`:number  `phase`:MotionDramaProductionPhaseV1⟨source·series-bible·asset-bible·episode-outline·script·storyboard·prompt-pack·review·release-ready·complete⟩
`activeSeriesBibleVersion`:number | null  `currentEpisodeNumber`:number  `currentReleaseId`:number | null
`revision`:number  `createdAt`:number  `updatedAt`:number
```

### `motionDramaPromptOverrides`

> 接口 `MotionDramaPromptOverrideV1`（10 项）；导出 `Omit`：`id`·`projectId`·`workId`

```text
`id?`:number  `projectId`:number  `workId`:number
`stage`:MotionDramaPromptStageV1  `scope`:'work' | 'episode'⟨work·episode⟩  `episodeNumber`:number | null
`instruction`:string  `revision`:number  `createdAt`:number
`updatedAt`:number
```

### `motionDramaPromptPacks`

> 接口 `MotionDramaPromptPackV1`（14 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `episodeNumber`:number  `provider`:MotionDramaProviderTargetV1
`version`:number  `maturity`:MotionDramaPromptPackMaturityV1⟨prompt-only·reference-ready⟩  `sourceManifestVersion`:number
`sourceRevision`:number  `promptVersions`:Record<MotionDramaPromptStageV1, string>  `manifestJson`:string
`contentHash`:string  `createdAt`:number
```

### `motionDramaReviewIssues`

> 接口 `MotionDramaReviewIssueV1`（19 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`episodeNumber`:number  `sceneKey`:string | null  `shotKey`:string | null
`subjectKey`:string | null  `category`:'story' | 'continuity' | 'visual' | 'motion' | 'prompt' | 'sound' | 'rights' | 'provider-capability'⟨story·continuity·visual·motion·prompt·sound·rights·provider-capability⟩  `severity`:'critical' | 'major' | 'minor'⟨critical·major·minor⟩
`evidence`:string  `problem`:string  `suggestion`:string
`status`:'open' | 'resolved' | 'dismissed'⟨open·resolved·dismissed⟩  `reviewedRevision`:number  `createdAt`:number
`updatedAt`:number
```

### `motionDramaScriptScenes`

> 接口 `MotionDramaScriptSceneV1`（27 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`episodeNumber`:number  `sceneNumber`:number  `order`:number
`heading`:string  `location`:string  `timeOfDay`:string
`dramaticPurpose`:string  `entryState`:string  `exitState`:string
`visibleAction`:string  `dialogue`:MotionDramaDialogueLineV1[]  `narration`:string
`soundCues`:MotionDramaSoundCueV1[]  `emotionalTurn`:string  `estimatedSeconds`:number
`characterKeys`:string[]  `sourceUnitKeys`:string[]  `authorStatus`:MotionDramaAuthorStatusV1
`revision`:number  `createdAt`:number  `updatedAt`:number
```

### `motionDramaSeriesBibles`

> 接口 `MotionDramaSeriesBibleRecordV1`（9 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `version`:number  `sourceManifestVersion`:number
`bible`:MotionDramaSeriesBibleV1  `contentHash`:string  `createdAt`:number
```

### `motionDramaShotReferences`

> 接口 `MotionDramaShotReferenceV1`（17 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`adaptationProjectId`·`assetVersionId`·`blobObjectId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `adaptationProjectId`:number  `shotKey`:string
`stableKey`:string  `role`:MotionDramaReferenceRoleV1⟨character·costume·location·prop·style·voice·start-frame·key-frame·end-frame⟩  `subjectKey`:string | null
`assetVersionId`:number | null  `blobObjectId`:number | null  `timing`:string
`note`:string  `rights`:MediaRightsV1 | null  `selected`:boolean
`createdAt`:number  `updatedAt`:number
```

### `motionDramaShots`

> 接口 `MotionDramaShotV1`（37 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`episodeNumber`:number  `sceneKey`:string  `shotNumber`:number
`order`:number  `narrativeFunction`:string  `targetSeconds`:number
`shotSize`:'extreme-wide' | 'wide' | 'full' | 'medium' | 'close-up' | 'extreme-close-up' | 'insert'⟨extreme-wide·wide·full·medium·close-up·extreme-close-up·insert⟩  `cameraAngle`:'eye-level' | 'high' | 'low' | 'overhead' | 'dutch' | 'pov'⟨eye-level·high·low·overhead·dutch·pov⟩  `cameraMovement`:'static' | 'pan' | 'tilt' | 'track' | 'dolly' | 'orbit' | 'zoom' | 'handheld'⟨static·pan·tilt·track·dolly·orbit·zoom·handheld⟩
`composition`:string  `visibleAction`:string  `performance`:string
`lighting`:string  `transitionIn`:string  `transitionOut`:string
`dialogue`:string  `narration`:string  `soundPlan`:MotionDramaSoundCueV1[]
`subjectKeys`:string[]  `sourceUnitKeys`:string[]  `imagePrompt`:string
`negativeImagePrompt`:string  `firstFramePrompt`:string  `keyFramePrompt`:string
`lastFramePrompt`:string  `videoPrompt`:string  `negativeVideoPrompt`:string
`authorStatus`:MotionDramaAuthorStatusV1  `revision`:number  `createdAt`:number
`updatedAt`:number
```

### `narrativeBeats`

> 接口 `NarrativeBeat`（15 项）；导出 `Omit`：`id`·`projectId`·`moduleId`·`speakerCharacterId`

```text
`id?`:number  `projectId`:number  `moduleId`:number
`nodeKey`:string  `beatKey`:string  `kind`:NarrativeBeatKind
`speakerCharacterId?`:number | null  `text`:string  `order`:number
`createdAt`:number  `updatedAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `narrativeChoices`

> 接口 `NarrativeChoice`（20 项）；导出 `Omit`：`id`·`projectId`·`moduleId`

```text
`id?`:number  `projectId`:number  `moduleId`:number
`sourceNodeKey`:string  `choiceKey`:string  `text`:string
`description`:string  `unavailableReason`:string  `targetNodeKey`:string
`displayConditionJson`:string  `availableConditionJson`:string  `effectsJson`:string
`tagsJson`:string  `order`:number  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `narrativeModules`

> 接口 `NarrativeModule`（17 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `worldId?`:number | null
`workId?`:number | null  `kind`:NarrativeModuleKind  `title`:string
`description`:string  `status`:'draft' | 'ready' | 'archived'⟨draft·ready·archived⟩  `sourceProjection`:'story-arc' | 'outline' | 'custom'⟨story-arc·outline·custom⟩
`sourceRefId?`:number | null  `entryNodeKey?`:string | null  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `narrativeNodes`

> 接口 `NarrativeNode`（18 项）；导出 `Omit`：`id`·`projectId`·`moduleId`·`sourceOutlineNodeId`

```text
`id?`:number  `projectId`:number  `moduleId`:number
`key`:string  `kind`:NarrativeNodeKind  `title`:string
`summary`:string  `conditionJson`:string  `effectsJson`:string
`successorKeysJson`:string  `sourceOutlineNodeId?`:number | null  `order`:number
`createdAt`:number  `updatedAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `nodeFlows`

> 接口 `NodeFlow`（8 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`name`:string  `description`:string  `graphJson`:string
`createdAt`:number  `updatedAt`:number
```

### `nodeRuns`

> 接口 `NodeRunRecord`（11 项）；导出 `Omit`：`id`·`projectId`·`flowId`

```text
`id?`:number  `projectId`:number  `flowId`:number
`status`:NodeRunStatus⟨running·paused·completed·failed·cancelled⟩  `inputSnapshotsJson`:string  `nodeResultsJson`:string
`executionPlanJson?`:string  `graphSnapshotJson?`:string  `startedAt`:number
`updatedAt`:number  `completedAt?`:number | null
```

### `notes`

> 接口 `Note`（8 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `chapterId?`:number
`content`:string  `color`:NoteColor⟨yellow·blue·green·pink·purple·orange⟩  `pinned`:boolean
`createdAt`:number  `updatedAt`:number
```

### `outlineNodes`

> 接口 `OutlineNode`（14 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `parentId`:number | null
`type`:OutlineNodeType⟨volume·arc·storyBlock·chapter⟩  `title`:string  `summary`:string
`order`:number  `worldGroupId?`:number | null  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `powerSystems`

> 接口 `PowerSystem`（9 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `name`:string
`description`:string  `levels`:string  `rules`:string
`worldGroupId?`:number | null  `createdAt`:number  `updatedAt`:number
```

### `productBuildArtifacts`

> 接口 `ProductBuildArtifactRecordV1`（27 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`buildId`·`producerRunId`·`blobObjectId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `buildId`:number  `artifactKey`:string
`requirementKey`:string | null  `version`:number  `kind`:ProductBuildArtifactKindV1
`mediaKind`:ProductMediaKind | null  `status`:ProductBuildArtifactStatusV1  `producerRunId`:number | null
`producerReceiptHash`:string | null  `controlEpoch`:number  `inputHash`:string
`contentHash`:string  `payloadJson`:string  `metadataJson`:string
`qualityJson`:string  `rightsJson`:string  `blobObjectId`:number | null
`mimeType`:string | null  `byteSize`:number  `parentArtifactHash`:string | null
`carriedFrom`:{ buildNumber: number; artifactKey: string; version: number; contentHash: string; /** Frozen witness over the exact parent Artifact and its producer/root Runs. */ proofHash?: string; } | null  `createdAt`:number  `updatedAt`:number
```

### `productBuilds`

> 接口 `ProductBuildRecordV1`（35 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`productionId`·`sourceProductReleaseId`·`releasedProductReleaseId`·`budgetLedgerJson`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `productionId`:number  `buildNumber`:number
`briefRevision`:number  `briefHash`:string  `parentBuildNumber`:number | null
`sourceProductReleaseId`:number | null  `status`:ProductBuildStatusV1  `resumeState`:ProductBuildStatusV1 | null
`stateRevision`:number  `controlEpoch`:number  `planRevision`:number
`planJson`:string  `planHash`:string  `budgetLedgerJson`:string
`manifestJson`:string  `manifestHash`:string  `packageHash`:string
`previewManifestJson`:string  `previewHash`:string  `qualityReportJson`:string
`qualityReportHash`:string  `compatibilityJson`:string  `rootTerminalReceiptHash`:string | null
`adoptionIntentHash`:string | null  `releasedProductReleaseId`:number | null  `failureJson`:string
`authorizedAt`:number  `startedAt`:number | null  `completedAt`:number | null
`createdAt`:number  `updatedAt`:number
```

### `productMediaAssets`

> 接口 `ProductMediaAsset`（25 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`productReleaseId`·`productRuntimeSessionId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `ownerKind`:'release' | 'runtime'⟨release·runtime⟩  `productType`:ProductionProductKindV1
`productReleaseId`:number | null  `productRuntimeSessionId`:number | null  `assetKey`:string
`version`:number  `kind`:ProductMediaKind  `name`:string
`mimeType`:string  `byteSize`:number  `width`:number | null
`height`:number | null  `durationMs`:number | null  `contentHash`:string
`source`:string  `license`:string  `altText`:string
`characterTag`:string  `sceneTag`:string  `createdAt`:number
`updatedAt`:number
```

### `productMediaBlobs`

> 接口 `ProductMediaBlob`（8 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`mediaAssetId`·`blobObjectId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `mediaAssetId`:number  `blobObjectId`:number
`data`:null  `createdAt`:number
```

### `productProductionBriefs`

> 接口 `ProductProductionBriefRecordV1`（34 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`productionId`·`sourceWorldReleaseId`·`sourceWorkId`·`sourceOutlineRootId`·`sourceStartChapterId`·`sourceEndChapterId`·`sourceChapterIdsJson`·`sourcePlanJson`·`candidateRunId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `productionId`:number  `revision`:number
`parentRevision`:number | null  `status`:"draft" | "authorized" | "superseded" | "withdrawn"  `briefKind?`:"product-production-v3" | "text-open-world-creator-v1"
`sourceKind?`:"world-release" | "novel"  `sourceWorldReleaseId`:number | null  `sourceWorldContentHash`:string | null
`sourceWorkId?`:number | null  `sourceOutlineRootId?`:number | null  `sourceStartChapterId?`:number | null
`sourceEndChapterId?`:number | null  `sourceChapterIdsJson?`:string  `sourceSelectionMode?`:import("./adaptation").AdaptationSourceSelectionV1["mode"] | null
`sourceVersionHash?`:string  `sourceBoundaryHash?`:string  `sourceBindingJson?`:string
`sourceBindingHash?`:string  `candidateRunId?`:number | null  `userIntentSummary`:string
`unresolvedJson`:string  `estimateJson`:string  `briefJson`:string
`briefHash`:string  `sourcePlanJson`:string  `sourcePlanHash`:string
`confirmedBriefJson`:string  `confirmedBriefHash`:string  `authorizedAt`:number | null
`createdAt`:number
```

### `productProductionCommands`

> 接口 `ProductProductionCommandRecordV1`（14 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`productionId`·`resultJson`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `productionId`:number  `commandId`:string
`type`:ProductProductionCommandTypeV1  `payloadHash`:string  `expectedStateRevision`:number | null
`status`:"claimed" | "succeeded" | "failed" | "abandoned"  `resultJson`:string  `errorCode`:string | null
`createdAt`:number  `completedAt`:number | null
```

### `productProductions`

> 接口 `ProductProductionRecordV1`（28 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`currentProductReleaseId`·`creatorSourceWorldReleaseId`·`creatorSourceWorkId`·`creatorSourceOutlineRootId`·`creatorSourceStartChapterId`·`creatorSourceEndChapterId`·`creatorSourceChapterIdsJson`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `productionKey`:string  `productType`:ProductionProductKindV1
`title`:string  `status`:ProductProductionStatusV1  `stateRevision`:number
`controlEpoch`:number  `currentBriefRevision`:number | null  `currentBuildNumber`:number | null
`currentProductReleaseId`:number | null  `creatorSourceKind?`:"world-release" | "novel" | null  `creatorSourceWorldReleaseId?`:number | null
`creatorSourceWorkId?`:number | null  `creatorSourceSelectionMode?`:import("./adaptation").AdaptationSourceSelectionV1["mode"] | null  `creatorSourceOutlineRootId?`:number | null
`creatorSourceStartChapterId?`:number | null  `creatorSourceEndChapterId?`:number | null  `creatorSourceChapterIdsJson?`:string
`creatorSourceVersionHash?`:string  `creatorSourceBoundaryHash?`:string  `creatorSourceBindingJson?`:string
`creatorSourceBindingHash?`:string  `lastErrorJson`:string  `createdAt`:number
`updatedAt`:number
```

### `productQualityGateReceipts`

> 接口 `ProductQualityGateReceiptRecordV1`（13 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`buildId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `buildId`:number  `gateId`:string
`gateVersion`:string  `verifierId`:string  `verifierVersion`:string
`status`:ProductQualityGateReceiptStatusV1  `receiptJson`:string  `receiptHash`:string
`createdAt`:number
```

### `productReleases`

> 接口 `ProductRelease`（13 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`worldReleaseId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `productionKey`:string  `productType`:ProductionProductKindV1
`worldReleaseId`:number | null  `version`:number  `label`:string
`manifestJson`:string  `contentHash`:string  `createdAt`:number
`distributionProvenance?`:ProductReleaseDistributionProvenanceV1
```

### `productRuntimeCheckpoints`

> 接口 `ProductRuntimeCheckpoint`（11 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`·`sessionId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`sessionId`:number  `throughSequence`:number  `name`:string
`purpose?`:ProductRuntimeCheckpointPurposeV1  `subjectKey?`:string | null  `stateJson`:string
`stateHash`:string  `createdAt`:number
```

### `productRuntimeEvents`

> 接口 `ProductRuntimeEvent`（13 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`·`sessionId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`sessionId`:number  `sequence`:number  `type`:ProductRuntimeEventType
`actorKey?`:string | null  `targetKey?`:string | null  `commandId?`:string | null
`baseSequence?`:number | null  `baseStateHash?`:string | null  `payloadJson`:string
`createdAt`:number
```

### `productRuntimeSessions`

> ⚠️ 未在 `types/*.ts` 解析到接口 `ProductRuntimeSession` 的字段 —— 请直接读源文件（本节不推断）。

### `referenceAnalysisRuns`

> 接口 `ReferenceAnalysisRun`（25 项）；导出 `Omit`：`id`·`projectId`·`referenceId`

```text
`id?`:number  `projectId`:number  `workId`:number
`referenceId`:number  `version`:number  `status`:ReferenceAnalysisRunStatus⟨analyzing·ready·active·superseded·failed·cancelled⟩
`depth`:ReferenceAnalysisDepth⟨quick·deep⟩  `sourceFilename`:string  `fileHash`:string
`totalChars`:number  `sourceKind`:ReferenceSourceKind⟨own-work·authorized·public-domain·research·unknown⟩  `usageScope`:ReferenceUsageScope⟨analysis-only·creative-reference·continuation-authorized⟩
`rightsNote`:string  `rightsConfirmed`:boolean  `rightsDeclaredAt`:number
`expectedChunks`:number  `completedChunks`:number  `progress`:number
`error?`:string | null  `analysisSummary?`:string  `mergedCharacters?`:string
`completedAt?`:number  `activatedAt?`:number  `createdAt`:number
`updatedAt`:number
```

### `referenceChunkAnalysis`

> 接口 `ReferenceChunkAnalysis`（29 项）；导出 `Omit`：`id`·`referenceId`·`analysisRunId`

```text
`id?`:number  `projectId?`:number  `workId?`:number | null
`referenceId`:number  `analysisRunId`:number  `chunkIndex`:number
`label?`:string  `startOffset?`:number  `endOffset?`:number
`narrativeStyle?`:string  `openingTechnique?`:string  `plotStructure?`:string
`pacingControl?`:string  `climaxDesign?`:string  `conflictEscalation?`:string
`characterCraft?`:string  `dialogueTechnique?`:string  `proseStyle?`:string
`emotionalBeats?`:string  `foreshadowing?`:string  `worldBuilding?`:string
`otherTechniques?`:string  `historicalContext?`:string  `socialInstitutions?`:string
`dailyLife?`:string  `materialCulture?`:string  `languageCustoms?`:string
`rawExcerpt?`:string  `createdAt`:number
```

### `references`

> 接口 `Reference`（25 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`title`:string  `author`:string  `type`:ReferenceType⟨story·style·historical⟩
`note`:string  `url`:string  `importedData?`:ImportedReferenceData
`genre?`:string  `totalChars?`:number  `fileHash?`:string
`importSessionId?`:number  `analysisDepth?`:ReferenceAnalysisDepth⟨quick·deep⟩  `analysisStatus?`:ReferenceAnalysisStatus⟨none·pending·analyzing·done·failed⟩
`analysisProgress?`:number  `analysisError?`:string | null  `analysisSummary?`:string
`mergedCharacters?`:string  `createdAt`:number  `updatedAt`:number
`ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number
`ragPolicyHash?`:string
```

### `screenplayBeats`

> 接口 `ScreenplayBeatV1`（23 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`sectionKey`:string  `sectionTitle`:string  `scope`:ScreenplayBeatScopeV1⟨act·sequence·episode⟩
`episodeNumber`:number  `order`:number  `objective`:string
`conflict`:string  `turn`:string  `outcome`:string
`causalFactKeys`:string[]  `decisionKeys`:string[]  `sourceUnitKeys`:string[]
`estimatedSeconds`:number  `authorStatus`:'confirmed'  `revision`:number
`createdAt`:number  `updatedAt`:number
```

### `screenplayReviewIssues`

> 接口 `ScreenplayReviewIssueV1`（18 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`category`:ScreenplayReviewCategoryV1⟨grounding·continuity·dramaturgy·format⟩  `severity`:ScreenplayReviewSeverityV1⟨critical·major·minor⟩  `sceneKey`:string
`blockId`:string | null  `evidence`:string  `problem`:string
`suggestion`:string  `sourceUnitKeys`:string[]  `reviewedSceneRevision`:number
`status`:'open' | 'resolved' | 'dismissed'⟨open·resolved·dismissed⟩  `createdAt`:number  `updatedAt`:number
```

### `screenplaySceneCards`

> 接口 `ScreenplaySceneCardV1`（22 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `manifestVersion`:number  `stableKey`:string
`beatKey`:string  `episodeNumber`:number  `sceneNumber`:number
`order`:number  `purpose`:string  `conflict`:string
`entryState`:string  `exitState`:string  `visibleAction`:string
`informationReveal`:string  `sourceUnitKeys`:string[]  `estimatedSeconds`:number
`authorStatus`:'confirmed'  `revision`:number  `createdAt`:number
`updatedAt`:number
```

### `screenplayScenes`

> 接口 `ScreenplayScene`（23 项）；导出 `Omit`：`id`·`projectId`·`workId`·`adaptationProjectId`·`sourceUnitIds`

```text
`id?`:number  `projectId`:number  `workId`:number
`adaptationProjectId`:number  `stableKey`:string  `planSectionKey`:string
`episodeNumber`:number  `sceneNumber`:number  `order`:number
`intExt`:'INT' | 'EXT' | 'INT_EXT'⟨INT·EXT·INT_EXT⟩  `location`:string  `timeOfDay`:string
`summary`:string  `estimatedSeconds`:number  `sourceUnitIds`:number[]
`sourceReviewManifestVersion`:number  `groundingReviewRevision?`:number | null  `dramaturgyReviewRevision?`:number | null
`blocks`:ScreenplayBlock[]⟨action·character·parenthetical·dialogue·transition·shot·note⟩  `status`:ScreenplaySceneStatus⟨card·draft·reviewed·locked⟩  `revision`:number
`createdAt`:number  `updatedAt`:number
```

### `shortNovelProductions`

> 接口 `ShortNovelProductionV1`（17 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`·`currentReleaseId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `phase`:ShortNovelProductionPhaseV1⟨intent·design·planning·drafting·review·release-ready·complete⟩  `revision`:number
`brief`:ShortNovelBriefV1 | null  `briefConfirmedAt`:number | null  `storyDesign`:ShortNovelStoryDesignV1 | null
`designConfirmedAt`:number | null  `latestReview`:ShortNovelReviewV1 | null  `reviewedManuscriptHash`:string | null
`currentReleaseId`:number | null  `planConfirmedHash?`:string | null  `expandedFromShort?`:{ convertedAt: number; targetWordCount: number; productionRevision: number } | null
`createdAt`:number  `updatedAt`:number
```

### `stateCards`

> 接口 `StateCard`（8 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `category`:StateCategory⟨character·location·item·faction·event⟩
`entityName`:string  `fields`:string  `lastChapterId?`:number
`createdAt`:number  `updatedAt`:number
```

### `storyArcs`

> 接口 `StoryArc`（17 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`name`:string  `type`:StoryArcType⟨main·sub⟩  `stages`:string
`description?`:string  `origin?`:StoryArcOrigin⟨manual·ai·import⟩  `status?`:StoryArcStatus⟨active·deprecated⟩
`sourceStoryCoreId?`:number  `sourceStoryCoreRevision?`:number  `sourceStoryCoreHash?`:string
`lastAlignedHash?`:string  `producerRunId?`:number  `producerCandidateHash?`:string
`createdAt`:number  `updatedAt`:number
```

### `storyCores`

> 接口 `StoryCore`（15 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `theme`:string
`centralConflict`:string  `plotPattern`:string  `logline?`:string
`concept?`:string  `mainPlot?`:string  `subPlots?`:string
`createdAt`:number  `updatedAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `storyTimelineEvents`

> 接口 `StoryTimelineEvent`（10 项）；导出 `Omit`：`id`·`projectId`·`chapterId`

```text
`id?`:number  `projectId`:number  `title`:string
`storyTime?`:string  `importance`:number  `description?`:string
`chapterId?`:number | null  `chapterTitle?`:string  `order`:number
`createdAt`:number
```

### `storylineCrossings`

> 接口 `StorylineCrossing`（10 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `arcIdA`:number
`arcIdB`:number  `chapterId?`:number | null  `chapterTitle?`:string
`note`:string  `evidenceQuote`:string  `createdAt`:number
`updatedAt`:number
```

### `storylineProgress`

> 接口 `StorylineProgress`（12 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `arcId`:number
`currentStageId?`:string | null  `status`:StorylineProgressStatus  `progressNote`:string
`lastActiveChapterId?`:number | null  `lastActiveChapterTitle?`:string  `involvedEntities`:string
`evidenceQuote?`:string  `createdAt`:number  `updatedAt`:number
```

### `temporalFacts`

> 接口 `TemporalFact`（35 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `workId?`:number | null
`worldGroupId?`:number | null  `characterId?`:number | null  `locationId?`:number | null
`storyArcId?`:number | null  `subjectWorldGroupId?`:number | null  `codexEntryId?`:number | null
`subjectName`:string  `objectCharacterId?`:number | null  `objectLocationId?`:number | null
`objectCodexEntryId?`:number | null  `predicate`:string  `factKind`:FactKind⟨state·event·derived⟩
`value`:string  `sourceType`:FactSourceType⟨chapter·manual·import·setting⟩  `sourceChapterId?`:number | null
`sourceRecordTable?`:string  `sourceQuote?`:string  `sourceWorldviewId?`:number | null
`sourcePowerSystemId?`:number | null  `sourceCultivationSystemId?`:number | null  `sourceStoryCoreId?`:number | null
`sourceCharacterId?`:number | null  `sourceField?`:string  `sourceFingerprint?`:string
`validFromChapterId?`:number | null  `validToChapterId?`:number | null  `status`:FactStatus⟨candidate·confirmed·rejected·superseded·stale·source-missing·invalid-range⟩
`locked`:boolean  `confidence?`:number  `supersedesFactId?`:number | null
`createdAt`:number  `updatedAt`:number
```

### `ttrpgRulePacks`

> 接口 `TtrpgRulePackRecordV1`（12 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`workId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `ruleSystemId`:string  `ruleSystemVersion`:string
`title`:string  `status`:"draft" | "validated" | "archived"  `rulePackJson`:string
`contentHash`:string  `createdAt`:number  `updatedAt`:number
```

### `ttrpgRuntimeAssetRequests`

> 接口 `TtrpgRuntimeAssetRequestRecordV1`（40 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`·`worldId`·`workId`·`sessionId`·`mediaAssetId`

```text
`id?`:number  `projectId`:number  `worldGroupId`:number | null
`worldId`:number  `workId`:number  `sessionId`:number
`requestKey`:string  `slotKey`:string  `kind`:TtrpgRuntimeMediaKindV1
`targetRef`:string  `audience`:TtrpgRuntimeMediaAudienceV1  `requesterViewerKey`:string
`prompt`:string  `negativePrompt`:string  `fallbackText`:string
`altText`:string  `styleBibleHash`:string  `inputHash`:string
`adapterId`:string  `status`:"queued" | "generating" | "available" | "failed" | "cancelled"  `priority`:number
`attemptCount`:number  `maximumAttempts`:number  `maximumSessionCostUsd`:number
`estimatedCostUsd`:number | null  `costReservationUsd`:number  `actualCostUsd`:number | null
`estimatedStorageBytes`:number | null  `mediaAssetId`:number | null  `mediaAssetVersion`:number | null
`mediaContentHash`:string | null  `processorLeaseId`:string | null  `processorLeaseExpiresAt`:number | null
`lastErrorCode`:string | null  `lastErrorDetail`:string | null  `requestedAtSequence`:number
`terminalEventSequence`:number | null  `revision`:number  `createdAt`:number
`updatedAt`:number
```

### `ttrpgSessionParticipants`

> 接口 `TtrpgSessionParticipantRecordV2`（22 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`·`worldId`·`workId`·`sessionId`

```text
`id?`:number  `projectId`:number  `worldGroupId`:number | null
`worldId`:number  `workId`:number  `sessionId`:number
`seatKey`:string  `role`:"gm" | "player" | "spectator"  `controller`:"human" | "ai" | "hybrid" | "vacant"
`actorKey`:string | null  `viewerKey`:string  `assignmentState`:"assigned" | "claimed" | "vacant" | "left"
`humanAssignmentPolicy`:"owner" | "invite" | "claim-at-session-zero" | null  `activation`:"manual" | "initiative" | "natural" | "pooled"  `aiProfile`:null | { agency: "reactive" | "balanced" | "proactive"; riskTolerance: "safe" | "balanced" | "bold"; latencyBudgetMs: number; costBudgetPerSessionUsd: number; }
`consent`:TtrpgSessionConsentPolicyV2  `sessionZeroAcceptedAtSequence`:number | null  `revision`:number
`lastCommandId`:string  `lastCommandFingerprint`:string  `createdAt`:number
`updatedAt`:number
```

### `userStyleProfiles`

> 接口 `UserStyleProfile`（13 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`workId`:number  `profile`:string  `enabled`:boolean
`sourceChapterIds`:string  `sampleCount`:number  `sampleWords`:number
`revisionPairs?`:string  `calibrationFeedback?`:string  `createdAt`:number
`updatedAt`:number
```

### `workCharacterBindings`

> 接口 `WorkCharacterBinding`（9 项）；导出 `Omit`：`id`·`projectId`·`workId`·`characterId`

```text
`id?`:number  `projectId`:number  `workId`:number
`characterId`:number  `role?`:string  `arc?`:string
`outcome?`:string  `createdAt`:number  `updatedAt`:number
```

### `works`

> 接口 `Work`（24 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`activeCharacterDrivenPlanId`·`activeNarrativeModuleId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`code`:string  `kind`:WorkKind⟨novel·screenplay·comic·motion-drama·avg·ttrpg·ai-town·character-interaction⟩  `novelProfile`:NovelWorkflowProfile | null
`title`:string  `description`:string  `genres`:string[]
`customGenre?`:string  `status`:WorkStatus⟨drafting·ongoing·paused·completed⟩  `targetWordCount`:number
`currentWordCount`:number  `coverImage?`:string  `writingStyleId?`:string
`methodologyId?`:string  `includeCultivationProgressInAI`:boolean  `activeCharacterDrivenPlanId`:number | null
`activeNarrativeModuleId`:number | null  `postAdoptionPolicy`:PostAdoptionPolicyV1⟨off·suggest·auto-with-budget⟩  `postAdoptionTaskTypes`:PostAdoptionTaskTypeV1[]⟨organization·memory·retrieval·consistency⟩
`postAdoptionBudget`:PostAdoptionBudgetV1  `createdAt`:number  `updatedAt`:number
```

### `worldDerivations`

> 接口 `WorldDerivationV1`（14 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`targetRevisionId`·`targetReleaseId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`sourceWorkspaceUid`:string  `sourceWorkCode`:string  `sourceWorkRevision`:number
`sourceRevisionVectorJson`:string  `sourceKind`:'long-novel' | 'short-novel'⟨long-novel·short-novel⟩  `sourceRangeJson`:string
`selectedResourceIdsJson`:string  `sourceContentHash`:string  `targetRevisionId`:number | null
`targetReleaseId`:number | null  `createdAt`:number
```

### `worldGroupLinks`

> 接口 `WorldGroupLink`（14 项）；导出 `Omit`：`id`·`projectId`·`fromGroupId`·`toGroupId`

```text
`id?`:number  `projectId`:number  `fromGroupId`:number
`toGroupId`:number  `linkType`:WorldGroupLinkType⟨portal·ascension·summon·branch·return·custom⟩  `name?`:string
`description?`:string  `bidirectional`:boolean  `createdAt`:number
`updatedAt`:number  `ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy
`ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

### `worldGroups`

> 接口 `WorldGroup`（19 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `name`:string
`description`:string  `type`:WorldGroupType⟨primary·traversal·instance·parallel·ascension·custom⟩  `icon?`:string
`color?`:string  `order`:number  `entryCondition?`:string
`exitCondition?`:string  `plannedChapterCount?`:number  `powerRestriction?`:string
`takeawayRules?`:string  `createdAt`:number  `updatedAt`:number
`ragDocumentId?`:string  `ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number
`ragPolicyHash?`:string
```

### `worldNodes`

> 接口 `WorldNode`（13 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `parentId`:number | null
`name`:string  `description`:string  `mapConfigJSON?`:string
`mapCacheJSON?`:string  `portalsJSON?`:string  `sortOrder`:number
`icon?`:string  `worldGroupId?`:number | null  `createdAt`:number
`updatedAt`:number
```

### `worldReleases`

> 接口 `WorldRelease`（11 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`revisionId`

```text
`id?`:number  `releaseUid`:string  `projectId`:number
`worldId`:number  `revisionId`:number  `version`:number
`label`:string  `manifestJson`:string  `contentHash`:string
`sourceWorldCode`:string  `createdAt`:number
```

### `worldRevisions`

> 接口 `WorldRevision`（10 项）；导出 `Omit`：`id`·`projectId`·`worldId`·`parentRevisionId`

```text
`id?`:number  `projectId`:number  `worldId`:number
`parentRevisionId`:number | null  `revision`:number  `label`:string
`manifestJson`:string  `contentHash`:string  `createdAt`:number
`updatedAt`:number
```

### `worldRulesProfiles`

> 接口 `WorldRulesProfile`（8 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `worldGroupId?`:number | null
`entries`:Record<string, WorldRuleEntry>  `customNodes`:CustomWorldRuleNode[]  `globalNote?`:string
`createdAt`:number  `updatedAt`:number
```

### `worlds`

> 接口 `World`（10 项）；导出 `Omit`：`id`·`projectId`

```text
`id?`:number  `projectId`:number  `identityKind`:WorldIdentityKind⟨workspace-scope·world-draft⟩
`code`:string  `name`:string  `description`:string
`currentVersion`:number  `communityOrigin?`:CommunityWorldOrigin  `createdAt`:number
`updatedAt`:number
```

### `worldviews`

> 接口 `Worldview`（27 项）；导出 `Omit`：`id`·`projectId`·`worldGroupId`

```text
`id?`:number  `projectId`:number  `worldOrigin?`:string
`powerHierarchy?`:string  `divineDesign?`:DivineDesign  `worldStructure?`:string
`worldDimensions?`:string  `continentLayout?`:string  `regionDimensions?`:string
`mountainsRivers?`:string  `climateByRegion?`:string  `naturalResourceOverview?`:string
`naturalResources?`:NaturalResources  `races?`:string  `factionLayout?`:string
`politicsOverview?`:string  `economyOverview?`:string  `cultureOverview?`:string
`internalConflicts?`:string  `itemDesign?`:string  `worldGroupId?`:number | null
`createdAt`:number  `updatedAt`:number  `ragDocumentId?`:string
`ragPolicy?`:RagDocumentPolicy  `ragPolicyRevision?`:number  `ragPolicyHash?`:string
```

