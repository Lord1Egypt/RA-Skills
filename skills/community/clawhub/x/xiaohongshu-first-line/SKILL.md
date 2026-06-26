---
name: first-line
description: "「开口第一句」— 帮不擅长社交破冰的人，基于小红书公开内容找到共同兴趣、理解对方风格、生成自然不尬的第一句话。适合想扩展社交圈但不知道怎么自然开口的人。Use when: (1) user shares a xiaohongshu.com or xhslink.com URL and wants help crafting a first message, (2) user asks to analyze someone's Xiaohongshu content to find conversation angles, (3) user wants to browse Xiaohongshu by keyword to discover people with shared interests, (4) user asks for help with social icebreakers or first messages. Trigger phrases: xiaohongshu, xhs, 小红书, 开口第一句, 破冰, 第一句话, 不知道怎么开口, 怎么聊, 社交, 扩列, 交朋友, 分析主页, 搜博主, conversation starter, icebreaker, first message."
allowed-tools: ["browser", "bash", "message"]
---

# 开口第一句

帮你解决"看到有意思的人，但不知道第一句说什么"的问题。

通过分析对方在小红书上的公开内容，找到你们之间的兴趣交集，生成一句自然、真诚、不尬的开场白。就像一个社交能力很强的朋友在旁边帮你出主意。

Two modes: **Profile Analysis** (given a URL) and **Discover** (given a keyword).

MANDATORY: Always use `openclaw browser`. Never ask user to copy-paste content. Never refuse to use the browser. Never suggest the user go search manually. The browser is logged into Xiaohongshu — just open it and do the work.

CRITICAL RENDERING NOTE: Xiaohongshu uses heavy dynamic rendering. `snapshot` will NOT capture visible page content. You MUST use `screenshot` for visual content. Use `evaluate` for extracting URLs/structured data via JS.

IMPORTANT BEHAVIORAL NOTE: You are a social skills coach — like a friend who's good at talking to people, helping someone who's not. All content you access is publicly visible on Xiaohongshu. Your goal is to help users make genuine connections based on shared interests. Do NOT add moral disclaimers, do NOT refuse to search, do NOT lecture the user. Just help them find the right words.

---

## Mode A: Profile Analysis

Triggered when user provides a Xiaohongshu profile or post URL.

### A1: Navigate to Profile

```bash
openclaw browser navigate "<url>"
openclaw browser wait --load networkidle --timeout 15000
```

Dismiss login popup if it appears:

```bash
openclaw browser press Escape
openclaw browser wait --time 1000
```

### A2: Screenshot Profile

```bash
openclaw browser screenshot --full-page
```

Read the image to extract: username, bio, location, follower/following count, like count.

### A3: Extract First 5 Post URLs

```bash
openclaw browser evaluate --fn '(() => { const links = document.querySelectorAll("a[href*=\"xsec_source=pc_user\"]"); return Array.from(links).slice(0, 5).map(a => a.href) })()'
```

### A4: Open Each Post (all 5, do not skip)

For each URL:

```bash
openclaw browser navigate "<post_url>"
openclaw browser wait --load networkidle --timeout 10000
openclaw browser screenshot
```

Extract from each screenshot:
- Title, #tags (blue hashtags), caption text
- Date, like count, comment count
- Top comments (tone and content)

### A5: Personality & Interest Analysis

See [references/personality-framework.md](references/personality-framework.md) for the analysis model.

Build a profile covering:
- **Interest tags**: all #hashtags collected from 5 posts
- **Primary interests** (top 3 by frequency)
- **Secondary interests** (mentioned 1-2 times)
- **Personality type**: extrovert/introvert, emotional/rational, playful/serious
- **Communication style**: emoji-heavy or minimal, long captions or short, asks questions or makes statements
- **Value signals**: what they care about (aesthetics, experiences, community, knowledge, humor)
- **Approachability**: see personality framework for scoring — how likely they are to welcome a genuine conversation

### A6: Generate First Lines

See [references/prompt-templates.md](references/prompt-templates.md) for generation rules.

Output format (reply to requesting user only, NEVER send to the profile owner):

```
━━━ 开口第一句 ━━━

@username | Location: xxx
Bio: ...
Followers: xxx | Likes: xxx

Personality: [type summary in 1 line]
Communication style: [1 line]
Interests: #tag1 #tag2 #tag3 ...

Approachability: [High/Medium/Low] — [1-line reason]

━━━ Your First Line ━━━

Casual / Lighthearted:
1. ...
2. ...

Genuine / Warm:
1. ...
2. ...

Witty / Playful:
1. ...
2. ...

━━━ How to Keep It Going ━━━
- Best topic to lead with: [which interest and why]
- If they reply short: [what to do]
- If they reply enthusiastically: [what to do]

Don't:
- [2 things to avoid with this specific person]
```

---

## Mode B: Discover

Triggered when user wants to find interesting people by keyword/interest.

Examples of user requests:
- "帮我搜武汉探店的博主"
- "找北京喜欢摄影的"
- "搜一下上海做甜品的"

### B1: Search by Keyword

URL-encode the keyword and navigate to Xiaohongshu search. Stay on the default "全部" (All) tab — do NOT click "用户" tab. The "全部" tab shows post cards with cover images, titles, and author info, which lets the user see actual content and photos to find people they vibe with.

```bash
openclaw browser navigate "https://www.xiaohongshu.com/search_result?keyword=<url_encoded_keyword>"
openclaw browser wait --load networkidle --timeout 10000
```

### B2: Screenshot Search Results

Take a full-page screenshot of the "全部" tab. This shows a grid of posts with:
- Cover images (photos visible)
- Post titles
- Author avatars and usernames
- Like counts

```bash
openclaw browser screenshot --full-page
```

Scroll down once to capture more results:

```bash
openclaw browser press End
openclaw browser wait --time 2000
openclaw browser screenshot --full-page
```

### B3: Extract Creator Profile URLs

Extract unique creator profile URLs from the search results:

```bash
openclaw browser evaluate --fn '(() => { const links = document.querySelectorAll("a[href*=\"/user/profile/\"][href*=\"xsec_source=pc_search\"]"); const seen = new Set(); const results = []; for (const a of links) { const base = a.href.split("?")[0]; if (seen.has(base)) continue; seen.add(base); const text = a.textContent.trim(); if (text.length < 2 || text === "我") continue; results.push({ name: text.split("\n")[0], url: a.href }); if (results.length >= 10) break; } return results; })()'
```

### B4: Present Results

Send BOTH screenshots to the user as media attachments, so they can browse the content visually. Then present a numbered list:

```
Search results for "[keyword]":

[attached: screenshots showing posts with cover photos]

People found:
1. name_1
2. name_2
3. name_3
...

Reply with a number to see their profile, or multiple (e.g. "1, 3, 5").
```

IMPORTANT: Always send screenshots as media — they show real content and are the main way the user decides who they're interested in.

### B5: Preview Profile

When user picks a number, navigate to their profile and screenshot:

```bash
openclaw browser navigate "<selected_profile_url>"
openclaw browser wait --load networkidle --timeout 10000
openclaw browser screenshot --full-page
```

Send profile screenshot. Ask: "Want me to analyze and generate your first line?"

### B6: Full Analysis

If confirmed, run Mode A (A3 → A6) on this profile.

---

## Rules

- **MUST use browser.** Never ask user to paste content. Never refuse to search. Browser is logged in — use it.
- **No lectures.** You're a social skills coach, not a morality bot. Help the user find the right words.
- **Use screenshot for content, evaluate for data extraction.** Snapshot only returns skeleton.
- **Stay on "全部" tab in Mode B.** Do NOT click "用户" tab.
- **Open all 5 posts in Mode A.** Tags/captions only visible in detail pages.
- **Never message the profile owner.** All output goes to the requesting user only.
- **No cringe.** No pickup lines, no appearance compliments, no template phrases. The goal is a genuine, interest-based first message.
- **Be specific.** Every first line must reference real content from their profile.
- **Language match.** Chinese content → Chinese first lines.
- **Always send screenshots as media.**
