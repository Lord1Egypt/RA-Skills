<!-- skill_version: 2.0.0 -->
---
name: skillnav
description: "Search 3,900+ MCP servers with install commands, get daily AI brief, query papers, search everything, and discover trending tools — in Chinese. Data from skillnav.dev editorial team."
version: 2.0.0
argument-hint: "brief | mcp <keyword> | search <keyword> | paper <id|keyword> | trending | update"
allowed-tools: WebFetch, Bash
metadata:
  openclaw:
    emoji: "🧭"
    homepage: https://github.com/skillnav-dev/skillnav-skill
    requires:
      bins:
        - curl
---

Route based on $ARGUMENTS[0]:

| Command   | Action                                                       |
|-----------|--------------------------------------------------------------|
| brief     | If $ARGUMENTS[1] is "papers", "news", or "tools": WebFetch https://skillnav.dev/api/skill/query?type=brief&section=$ARGUMENTS[1]. Otherwise: WebFetch https://skillnav.dev/api/skill/query?type=brief |
| mcp       | WebFetch https://skillnav.dev/api/skill/query?type=mcp&q=$ARGUMENTS[1] |
| search    | WebFetch https://skillnav.dev/api/skill/query?type=search&q=$ARGUMENTS[1..] (join remaining args with space, URL-encode) |
| paper     | If $ARGUMENTS[1] matches arXiv ID pattern (YYMM.NNNNN): WebFetch https://skillnav.dev/api/skill/query?type=paper&id=$ARGUMENTS[1]. Otherwise: WebFetch https://skillnav.dev/api/skill/query?type=paper&q=$ARGUMENTS[1] |
| trending  | WebFetch https://skillnav.dev/api/skill/query?type=trending  |
| update    | Bash: curl -sL https://raw.githubusercontent.com/skillnav-dev/skillnav-skill/main/SKILL.md -o ~/.claude/skills/skillnav/SKILL.md && echo "SkillNav Skill updated." |
| (other)   | Show usage message — do NOT fetch any URL                    |

If $ARGUMENTS is empty or does not match any command above, show this usage message and STOP (do NOT fetch any URL):

```
SkillNav — AI 开发者工具站 (skillnav.dev)

  /skillnav brief              今日 AI 日报
  /skillnav mcp <keyword>      搜索 MCP Server
  /skillnav search <keyword>   搜索文章、工具、概念
  /skillnav trending           本周热门工具
  /skillnav paper <arxiv-id>   查看论文详情
  /skillnav update             更新到最新版本
```

---

## Format Rules

### Version check

After every API response, compare `meta.skill_version` from the response with this file's version (2.0.0).
If the API version is newer, append at the very end of your output:

> 💡 SkillNav Skill 有新版本可用 — `/skillnav update`

### brief (full or section-filtered)

If `section` field is absent (full brief), format as:

1. **TL;DR**: One bold sentence summarizing the headline
2. Headline title with `> why_important` in blockquote
3. Bulleted highlights, each with editor comment in parentheses
4. If `papers` array is non-empty, show "论文速递":
   - **{title}** `{attitude}`
     {what}
     > {implication}
5. If `is_fallback` is true: "(注意：这是 {date} 的日报，今日暂无更新)"
6. Footer: "完整日报 → {url}"

If `section` is `"papers"`, format papers only:

1. Header: "论文速递 · {date}"
2. For each paper:
   **{title}** `{attitude}`
   {what}
   > {implication}
   趋势：{trend}
   → arXiv: {url}
3. Footer: "完整日报 → {url}"

If `section` is `"news"`, format highlights only:

1. Header: "行业动态 · {date}"
2. Headline (if non-empty): **{headline.title}** — {headline.why_important}
3. Bulleted highlights with editor comments
4. Footer: "完整日报 → {url}"

### mcp

Format each result as a numbered list with one blank line between items:

1. **{name}** `{category}` ⭐ {stars}
   {description_zh}
   > {editor_comment_zh}
   ```
   {install_command}
   ```

If `editor_comment_zh` is null, skip the blockquote line.
If results are empty: "未找到匹配的 MCP Server，试试更宽泛的关键词。"
Footer: "共 {returned} 个结果{has_more ? '（更多结果请访问 skillnav.dev）' : ''}"

### search

Group results by `result_type` in this order: concept > mcp > skill > article.

**Concept**:
  **{term}**（{zh}）— {one_liner}
  → {url}

**MCP / Skill**:
  **{name}** ⭐ {stars} — {description_zh}
  > {editor_comment_zh}
  ```
  {install_command}
  ```

If `editor_comment_zh` is null, skip the blockquote line.
If `install_command` is null, skip the code block.

**Article**:
  **{title_zh}** ({source}, {reading_time}min)
  {summary_zh}
  → {url}

If results are empty: "未找到与 "{query}" 相关的内容，试试其他关键词。"
Footer: "共 {returned} 个结果"

### trending

Format as a ranked list grouped by tool_type:

**MCP Server**
1. **{name}** ⭐ {stars} (+{weekly_stars_delta} this week)
   > {editor_comment_zh}

**Skill**
1. **{name}** ⭐ {stars} (+{weekly_stars_delta} this week)
   > {editor_comment_zh}

If a group has no items, omit it entirely.

### paper (single by ID)

If `has_translation` is true:

1. **{translation.title_zh}** `{brief_card.attitude}` (if brief_card exists)
2. If brief_card exists: {brief_card.what}
   > {brief_card.implication}
3. "已有完整中文翻译 → {translation.url}"

If `has_translation` is false:

1. If brief_card exists:
   **{brief_card.title}** `{brief_card.attitude}`
   {brief_card.what}
   > {brief_card.implication}
   趋势：{brief_card.trend}
2. If no brief_card: "未找到该论文的导读信息。"
3. "arXiv 原文 → {arxiv_url}"

### paper (keyword search)

1. Header: "论文搜索 · 最近 {days} 天 · "{query}""
2. For each result:
   **{title}** `{attitude}` · {date}
   {what}
   > {implication}
   → arXiv: {url}
3. If results are empty: "最近 {days} 天未找到与 "{query}" 相关的论文。"
4. Footer: "共 {returned} 篇结果"

---

## Global Footer

Append this line at the very end of EVERY output (after all content, after version check if present):

```
— SkillNav · skillnav.dev
```

## Error Handling

- If WebFetch fails or returns non-JSON: "SkillNav API 暂时不可用，请直接访问 skillnav.dev"
- If API returns `{ "error": ... }`: Show the `message` field to the user
- NEVER fabricate data or suggest keywords that weren't in the response
