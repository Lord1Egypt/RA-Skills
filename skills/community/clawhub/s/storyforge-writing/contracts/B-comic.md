# B 类子契约 · 漫画（storyforge-writing）

> 归属：B 视觉化。对应 StoryForge INDEPENDENT-CREATION §小说转漫画 + schema v5 comic 表。
> 产物给视觉生成用；脚本侧（章节/对白）依赖 A 类，分镜/格/视觉主体归 B。

## 1. 漫画字段闭集（schema v5）

```
comicScriptBeats   id, workId, adaptationProjectId, stableKey, manifestVersion, chapterNumber, sectionKey, order
comicPagePlans     id, workId, adaptationProjectId, stableKey, manifestVersion, pageNumber, chapterNumber, order
comicPages         id, workId, adaptationProjectId, stableKey, order, chapterNumber, status
comicPanels        id, workId, pageId, stableKey, order, status
comicVisualSubjects id, workId, adaptationProjectId, stableKey, kind, characterId, locationRefKey, status
comicMediaAssets   id, workId, adaptationProjectId, stableKey, role, origin, panelId, subjectKey, blobObjectId, disposition, requestHash
comicReviewIssues  id, workId, adaptationProjectId, stableKey, pageKey, panelKey, category, severity, status
```

## 2. 生成内容（B 类出料）

| 语料块 | 内容 | 说明 |
|---|---|---|
| 漫画分镜脚本 | 章 → 节 → 格（page/panel）的视觉编排 | 每格描述画面/视角/镜头/动作 |
| 视觉主体卡（comicVisualSubjects） | kind：人物/场景/道具；绑 characterId + locationRefKey | 供一致性参考 |
| 媒资需求清单（comicMediaAssets） | role/origin/panelId/subjectKey | 标 disposition，字节归共享 Blob |
| 格级 beat（comicScriptBeats） | sectionKey + order | 对白/动作节拍 |
| 审校问题（comicReviewIssues） | pageKey/panelKey/category/severity | 连续性/格式 |

## 3. 与 A 类边界

- **章节/对白/人物** = A 类长篇语料（comic 复用长篇 work 的正文）
- **分镜/页/格/视觉主体/媒资需求** = B 类
- 转换必须保存 **source manifest + 源版本 + 原文证据**，产物不静默改写源作品
- 媒资字节归漫画 work 的 Blob，**语义 owner 不转移给世界引擎**

## 4. 生产链（漫画侧）

```
源文（长篇/短篇）解析与范围冻结
→ 事实/人物/场景/动作/对白提取（A 类）
→ 改编 Brief 与删改原则
→ 分镜规划（场景→页→格）
→ 视觉主体卡 + 媒资需求（B 类）
→ 格级 beat + 对白
→ 连续性/格式/源文证据审校
→ 作者修改与批准
→ 不可变漫画版本 / 导出
```

## 5. 纪律

- 格/页/视觉主体全部走**候选→采纳**（同总入口 SOP）
- 区分"忠实保留/合理改编/新增假设"，作者可追溯删改
- 媒资缺失可出 prompt-only，但不得标 reference-ready

## 6. 所有权 · 不变量 · 禁止项（v0.4.0）

**所有权**：本技能 owns 视觉化产物的字段闭集；上游 owns schema v5 comic 系列表；**作者** owns 画风与分镜取舍。

**不变量**
- `INV-BC-1` 字段必须 ∈ schema v5 comic 表闭集。
- `INV-BC-2` B 类**只做视觉化**：剧情/设定来自 A 类产物，不在此重写。

**禁止项**
- 不得代写或改写剧情设定（越 A 类边界）。
- 不得声称已产出图片/页面渲染结果（本技能只出分镜与描述）。
