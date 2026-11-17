---
name: yoooclaw-hotspot-topic-scout-en
description: Use when users want to quickly identify hot-topic ideas, high-performing content references, competitor activity, and audience needs from message notifications and the web. It is suited to content creators, editors, and operations leads asking what was worth following yesterday, what can be adapted to their niche, or for direct topic suggestions.
---

# Hotspot Topic Scout

This Skill collects materials from two channels and combines them internally and externally:
- **Internal signals**: Message notifications on users’ mobile phones (content platform push, industry group chat, team discussion, fan feedback)
- **External hot spots**: Use `byted-web-search` to search for the latest industry trends, benchmark bloggers’ recent content, and hot topics on the track through the Internet

Users set three types of attention dimensions through the installation pop-up window:
- Who to follow: Benchmark bloggers, peer accounts, competing product creators, brand accounts or content sources that users clearly follow.
- What to focus on: account tracks, content positioning, audience portraits, industry keywords (models, products, platforms, companies, technical directions, consumer trends, policy events, etc.).
- Which groups and applications to pay attention to: monitored information source platforms and groups, such as Xiaohongshu, Bilibili, Jiji, official accounts, WeChat industry groups, creator groups, and internal team discussion groups.

Do not treat the following as hotspot output:
- Pure entertainment gossip, outfits, variety shows, and celebrity related content
- Pan-traffic topics weakly related to the user's main track
- Replies that are trolling and have no substantive information
- Family, express delivery, takeaway, and promotion notifications

## Workflow

### Phase 1: Collect internal signals

1. To query notifications within a specified time range, use exec to execute:
If the user does not provide the corresponding time, query notifications from yesterday to the current time:
```text
command: openclaw ntf search --from start time --to end time
yieldMs: 30000
```
Example:
```text
command: openclaw ntf search --from 2026-03-01T00:00:00+08:00 --to 2026-03-09T23:59:59+08:00
yieldMs: 30000
```
2. As long as the task involves "yesterday", "recent", "just now" and "latest notification", the query must be re-queried and the old results will not be reused.3. Read the user's settings of who to follow, what to follow, and which groups and applications to follow; if the user does not provide it, the most likely filtering direction is inferred from the current request and notification context.
4. Screen out content platform push, creator-related group chats, benchmark blogger updates, industry keyword hit content and fan feedback from notifications.
5. Extract key clues from internal signals: the topic selection direction of team discussions, industry events forwarded in the group, fans’ centralized questions or reminders for updates, and mentions of benchmarking bloggers.

### Stage 2: Search external hot spots online

Supplement external hotspots with `byted-web-search` (Volcano Engine Network Search) based on internal signals and user configuration.

Search strategy:
- Extract 3-5 groups of industry keywords from "What are you paying attention to" and search group by group
- Extract the name of the benchmarking blogger/competing product from "Who to follow" and search for their recent updates
- If a high-frequency topic appears in the internal signal but the information is incomplete, perform a supplementary search on the topic to obtain the complete background.
- Search terms plus today’s date, such as `{keyword} {M month D day}`, give priority to crawling the content of the current day and the past 48 hours
- No more than 10 total searches

Filter search results:
- Priority retention: industry media, official updates from content platforms, public content from benchmarking bloggers, and authoritative data reports
- Prioritize discarding: soft article advertisements, SEO content, general information irrelevant to the user’s track

### Phase 3: Merger, sorting and output

6. Combine internal signals and external search results to identify candidate materials: new model releases, industry trends, platform trends, controversies, peer reviews, popular content, competitive product actions, team proactive focus, and fans’ centralized questions or reminders for updates.
7. Combine the same event, the same competing product action or similar fan needs to avoid repeated listing. When internal and external sources mention the same event, they are combined into one and marked as "internal + external" dual signals.
8. Classify materials into four categories:
- Topic inspiration: hot topics, trends, controversies, experiences or issues that can be turned into user account content.
- Reference for popular items: title, cover, structure, expression, interactive mechanism or data performance worth learning from.
- Competitive product dynamics: the release, topic selection, style, and action changes of benchmarking bloggers, peer accounts, and competing product brands in "Who to Follow".
- Fan needs: recurring questions, reminders, feedback and content demands in comments, private messages, community or team reports.
9. Evaluate each material along three dimensions:
- Popularity: Number of source mentions and source quality (both internal and external mentions > external only > internal only)
-Positioning relevance: the degree of fit with the content positioning and industry keywords in "What to Focus on"
- Timeliness: Is it appropriate to follow up today or within the next 48 hours?
10. Each section can output multiple pieces of material, sorted by star rating and recommendation value; do not default to outputting only 1 piece per category.11. Output the recommendation priority, and give the angle of entry, content format and necessary reminders.
12. If the data is sparse and there is not enough available material, output a brief copy instead of forcibly making up the topic.

## Output requirements

The output is session text, no file is generated. Default structure:

```text
🔥 Yesterday’s hot material capture (YYYY-MM-DD)

M pieces of available material are summarized from notifications + Internet search and classified according to content value:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Inspiration for topic selection
  List multiple items by recommendation degree, 1-N items can be output; if there is no valid material, write "None".

  ⭐⭐⭐⭐⭐ ｜ Topic name A
    Source: List key sources (marked with 🔔notification / 🌐online search)
    Key message: distill 1-2 sentences of facts
    Reason for recommendation: explain why it is suitable for the current content positioning
    Suggestions for entry: Give title direction, point of view or content form

  ⭐⭐⭐⭐ ｜ Topic name B
    Source: List key sources (marked with 🔔notification / 🌐online search)
    Key message: distill 1-2 sentences of facts
    Reason for recommendation: explain why it is suitable for the current content positioning
    Suggestions for entry: Give title direction, point of view or content form

2. Reference for popular items
  List multiple items according to their reference value, and can output 1-N items; if there is no valid material, write "None".

  ⭐⭐⭐⭐⭐ ｜ Content/Account Name A
    Points for reference: title, structure, cover, interaction, comment area or data highlights
    Transformable method: explain how to transform it into your own content, do not copy it

3. Competitive product dynamics
  List multiple items according to their impact on content strategy, and you can output 1-N items; if there is no valid material, write "None".

  ⭐⭐⭐⭐⭐ ｜ Benchmark blogger/competitive product name A
    Action: Release, revision, topic change, cooperation, controversy or frequency change
    Implications/risks: What are the implications for your own content strategy?

4. Fans’ needs
  List multiple items according to demand intensity and convertible value, and can output 1-N items; if there is no valid material, write "None".

  ⭐⭐⭐⭐⭐ ｜ Requirement Topic A
    Feedback sources: comments, private messages, communities or team reports
    Content opportunities: Responsive questions, tutorials, reviews, checklists, or avoidance content

━━ Filtered ━━
  Describe the filtered topic categories and, if necessary, explain why they are not included in the main list.
```

If there is not enough valid material, you must output:

```text
🔥 Yesterday’s hot material capture (YYYY-MM-DD)

The harvest of materials is not abundant today.
```

## Decision Criteria

- Who to follow, what to follow, which groups and applications to follow as set by the user are the highest priority for filtering clues. Related messages must be prioritized to determine whether they can be converted into material.- When the same event is mentioned internally and externally at the same time, the popularity will be doubled and recommendations will be given priority.
- Topics that have been proposed within the team should be given higher priority.
- When benchmarking bloggers or competing products experience changes such as continuous releases, sudden suspensions, hot sales, transformations, disputes, business cooperation, etc., you should enter "Competitive Product Updates".
- When fans mention the same issue multiple times, urge updates on the same topic, or express similar confusion, they should enter "Fan Demand".
- Topics that are not core topics but have high traffic are not directly included in the main list. They can be placed in "Filtered" and optional corner cuts added.
- Controversial or sensitive topics should be clearly reminded of the risks of expressing them, and do not just judge the traffic.
- When the data is sparse, it is better to output full-text copy instead of generating weak material just to make up the structure.

## Output style

- Prioritize sorting by recommendation value rather than time.
- Each material is marked with the source type (🔔Notification / 🌐Web search) to let users know where the signal comes from.
- Only the most critical information is retained for each hotspot without lengthy retelling.
- The conclusion should be directly communicated in the topic selection meeting.
