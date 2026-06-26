# WeRead Markdown Template

当前目标模板如下：

```md
---
title: {{title}}
author: {{author}}
bookId: {{bookId}}
source: weread
lastNoteUpdate: {{lastNoteUpdateIso}}
highlightCount: {{highlightCount}}
reviewCount: {{reviewCount}}
tags:
{{#each tags}}
  - {{this}}
{{/each}}
---

# {{title}}

{{#if bookmarks}}
## 划线

### {{chapterName}}

<!-- bookmarkId: {{bookmarkId}} -->
<!-- time: {{date}} -->
<!-- chapterUid: {{chapterUid}} -->

> {{quote}}
{{/if}}

{{#if reviews}}
## 想法

### {{chapterName}}

<!-- reviewId: {{reviewId}} -->
<!-- time: {{date}} -->
<!-- chapterUid: {{chapterUid}} -->

> **摘录**：{{quote}}
>
> **想法**：{{note}}
{{/if}}

{{#if deleted}}
## 已删除

### 划线

{{deletedBookmarks}}

### 想法

{{deletedReviews}}
{{/if}}
```

## Rules

- 如果 `划线` 为空，则不生成 `## 划线`
- 如果 `想法` 为空，则不生成 `## 想法`
- 如果 `已删除` 为空，则不生成 `## 已删除`
- `划线` 按章节名组织
- `想法` 按章节名组织
- 不再给每条想法重复生成 `### 想法`
- 保留隐藏 `bookmarkId` / `reviewId` 供 merge 使用
