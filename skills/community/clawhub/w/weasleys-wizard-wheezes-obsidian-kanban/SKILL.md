---
name: weasleys-wizard-wheezes-obsidian-kanban
description: Create, normalize, and reorganize Obsidian Kanban plugin markdown boards. Display name: Weasleys Wizard Wheezes - Obsidian Kanban. Use when working with Obsidian Kanban `.md` files, turning ledgers, review ledgers, tables, checklists, audit notes, or issue lists into board columns and cards, reformatting existing Kanban boards for readability, or preserving full content while making cards easier to scan. Trigger on requests like “把台账转成 Obsidian 看板”, “整理这个 Kanban 文件”, “优化看板格式但不要删内容”, or “把 Markdown 清单改成 Kanban”.
---

# Weasleys Wizard Wheezes - Obsidian Kanban

Use this skill to edit **Obsidian Kanban plugin markdown files** directly and safely.

## 0. Quick examples

### Example A: ledger → board

User request:

> 把《第一轮评论台账》整理成 Obsidian 看板，不要删内容。

Expected approach:

1. read the source ledger
2. identify the main organizing axis, usually status or priority
3. create columns
4. convert each row into one card
5. shorten only the card title
6. preserve the full details in nested bullets

### Example B: messy board → cleaner board

User request:

> 这个 Kanban 太难看了，帮我整理一下，但别删信息。

Expected approach:

1. keep frontmatter and kanban settings
2. keep existing columns unless the user asks to change them
3. shorten card titles for scanability
4. move detail into nested bullets
5. add lightweight markers only if they improve readability

## 1. Core principle

1. Preserve plugin-recognized structure.
2. Prefer direct markdown editing over UI simulation.
3. Unless the user explicitly asks for compression, **do not delete content**.
4. Optimize for two layers at once:
   1. board-level scanability
   2. card-level information fidelity

## 2. Recognize a standard board

Treat the file as an Obsidian Kanban board when it contains both of these markers:

```md
---
kanban-plugin: board
---
```

and/or a settings block like:

```md
%% kanban:settings
```

Column headings are typically `## Column Name`.
Cards are typically markdown task items under each column.

## 3. Safe editing rules

1. Keep the frontmatter valid.
2. Keep the `kanban-plugin: board` marker intact.
3. Preserve the `%% kanban:settings %%` block unless the user explicitly asks to change board behavior.
4. Do not silently convert the board into a normal note.
5. Do not remove card details when the user asks only for formatting or reorganization.
6. When uncertain about advanced plugin-specific syntax, read the existing file first and make the smallest valid edit.

## 4. Default transformation strategy

When converting a structured source document into a Kanban board:

1. Choose columns using the source's strongest organizing axis:
   1. status
   2. priority
   3. workflow stage
   4. owner / reviewer
2. Turn each row / ledger item / issue into one card.
3. Use a **short scanable title** for the card first line.
4. Put the full original content into indented bullet lines under the card.
5. Preserve important fields explicitly, such as:
   - source location
   - status
   - priority
   - impact
   - owner
   - due date
   - rewrite-needed / approval-needed flags

## 5. Card formatting pattern

Prefer this pattern unless the user requests another layout:

```md
- [ ] Short card title
  - 原始内容：完整原文或压缩后不丢信息的版本
  - 对应位置：...
  - 判断类型：...
  - 当前状态：...
  - 优先级：...
```

Guidelines:

1. The first line should help the user scan the board quickly.
2. The nested bullets should preserve detail.
3. If the source item is already concise, keep it verbatim as the card title.
4. If the source item is long, compress only the **title**, not the stored detail.

## 6. Reformatting an existing board

When the board already exists but is hard to read:

1. Keep the existing columns unless the user asks to change the board logic.
2. Shorten only card titles.
3. Move full detail into nested bullets.
4. Add lightweight visual markers only if they improve scanability, for example:
   - 🔥 urgent / P0
   - 📝 pending absorption
   - ✅ done
   - 📚 terminology
5. Avoid decorative formatting that makes raw markdown harder to maintain.

## 7. Handling “do not delete content” requests

When the user says not to delete content:

1. Preserve every source item.
2. Preserve all semantic fields.
3. Preserve important wording inside the detail bullets.
4. You may rewrite card titles for readability.
5. If full fidelity and compactness conflict, choose fidelity and explain the tradeoff briefly.

## 8. Recommended workflows

### 8.1 Ledger/table → Kanban

1. Read the source note.
2. Identify the organizing axis.
3. Draft column layout.
4. Convert each entry into one card.
5. Verify no rows were dropped.
6. Write back valid Kanban markdown.

### 8.2 Existing Kanban → cleaner Kanban

1. Read the board.
2. Preserve frontmatter and settings.
3. Preserve columns unless asked otherwise.
4. Refactor card titles for scanability.
5. Push full detail into nested bullets.
6. Verify the board still parses as Kanban markdown.

## 9. What this skill is for

Use this skill for:

1. Obsidian Kanban plugin `.md` files
2. converting review ledgers, issue lists, audit notes, or task tables into boards
3. formatting-heavy board cleanup where the content must be preserved
4. repeated board normalization across a vault or project

## 10. What this skill is not for

Do not use this skill alone for:

1. generic Obsidian note authoring without board structure
2. `.canvas` files
3. `.base` files
4. workflows that require Obsidian UI behavior rather than markdown file editing

In those cases, use the more specific Obsidian skill instead.
