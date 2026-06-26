---
name: x
description: X platform skill for SurfAgent, covering route-aware workflows, proof rules, blockers, and when to use the X adapter over raw browser control.
version: 1.2.0
metadata:
  openclaw:
    homepage: https://surfagent.app
    emoji: "𝕏"
---

# X

> X-specific operating skill. Use this with the core `browser-operations` skill.

This skill teaches agents how to work X without guessing at selectors, trusting flaky button state, or claiming success from an attempted post.

## 1. Use this skill for

- home, notifications, search, profile, post, and community navigation
- timeline and thread extraction
- post creation and replies
- likes and lightweight engagement actions
- route-aware verification
- X-specific blockers and recoveries
- deciding when to use the X adapter instead of raw browser control

## 2. Tool preference

Use this order:
1. X adapter state and navigation tools
2. X adapter extraction and action tools
3. targeted browser evaluation only when needed
4. raw generic browser actions as fallback

Prefer X-native verbs over rediscovering the X DOM every run.

## 3. X truths that matter

X is not a generic site.

It has:
- route-specific UI states
- React-sensitive composer behavior
- flaky action button signals
- delayed state settlement after navigation and posting
- login walls and rate-limit surfaces that can look like normal content
- community pages with slightly different posting and feed behavior

Important: a visible button or a completed click is not proof that a post, reply, or like actually landed.

Also important: the wrong account doing the right action is still a failure.

Also important: on complex X surfaces, visual state beats partial extraction. If the switcher, composer, or community page is ambiguous, use a screenshot or visual snapshot instead of guessing.

## 4. Core X loop

Default loop:
1. confirm current X state
2. confirm the active account is the one you actually want
3. prefer the current feed or thread surface if the target is already visible
4. open the intended route deliberately only when needed
5. verify the route and surface are real
6. perform one X-native action
7. verify the visible result
8. recover if X settled into the wrong state

Default rule: **feed-first, permalink-only-when-needed**.

## 5. Verified posting flow

Known-good pattern:
- verify the active account before opening compose
- confirm logged-in X state
- open compose explicitly, or confirm the active composer is real
- inspect composer state before fill
- create the post through the X adapter
- if submit stays disabled, inspect composer diagnostics before guessing
- if text is visible but submit stays disabled, switch immediately to real keyboard-style input, not DOM-only insertion
- verify the composer cleared, closed, or transitioned
- verify the post text is visible in the expected surface, thread, or profile timeline

For replies:
- verify the active account before opening reply
- if the target is already visible in the feed or current thread, reply there first
- open the target post directly only when context or stability requires it
- confirm the reply surface belongs to that post
- submit the reply
- verify the reply appears in the feed, thread, or visible reply context

For community posts:
- verify the active account before joining or posting
- verify the current community name and membership state
- confirm the audience selector shows the intended community before typing
- verify the composer accepted the text as real input before submit
- after submit, confirm the post appears in the visible community feed under the correct account

## 6. Like and lightweight engagement rule

For like flows, minimum proof is:
1. target post is identified correctly
2. like action executes
3. visible state changes to the liked state, or re-extraction confirms the action

Do not claim success from only calling `x_like_post` without checking the resulting state.

## 7. Proof rules

For X, success requires visible evidence tied to the route.

Trust order when signals conflict:
1. visible active account label and route
2. screenshot or visual snapshot of the current X surface
3. visible button state, composer state, and resulting feed/thread state
4. targeted DOM extraction
5. wrapper success strings

Good proof usually includes:
- expected route or modal is open
- correct composer or thread is active
- intended text is present before submit when relevant
- post-action UI changed in the expected way
- the resulting post, reply, or liked state is visible afterward

Bad proof:
- click returned ok
- submit button was enabled
- no error was thrown
- the agent assumes success because the page looked stable

## 8. Surface selection rules

Prefer acting from the current surface when:
- the target post is already visible in the feed
- the feed item is stable and clearly identifiable
- a like, reply, or repost can be verified in place

Prefer opening a dedicated post route when:
- thread context matters
- the target item in the feed is ambiguous
- hydration/rendering is incomplete
- you need exact isolation for a higher-risk action

Repeatedly reopening the same post URL is usually a smell, not a best practice.

## 9. X adapter, when to use it

Prefer the X adapter for:
- opening X
- route-aware state inspection
- opening home, notifications, search, profiles, posts, and communities
- timeline extraction
- topic, profile, and community search
- composer inspection
- posting, replying, and liking
- X-specific recovery

Current X adapter verbs include:
- `x_health_check`
- `x_open`
- `x_get_state`
- `x_get_accounts`
- `x_switch_account`
- `x_open_home`
- `x_open_profile`
- `x_open_notifications`
- `x_open_search`
- `x_open_post`
- `x_get_timeline`
- `x_search_posts`
- `x_search_profiles`
- `x_search_communities`
- `x_open_community`
- `x_get_community_feed`
- `x_extract_post`
- `x_extract_profile`
- `x_get_profile_posts`
- `x_get_post_thread`
- `x_get_composer_state`
- `x_create_post`
- `x_reply_to_post`
- `x_like_post`
- `x_repost_post`
- `x_follow_profile`
- `x_verify_text_visible`
- `x_recover`
- `x_research_topic`
- `x_map_community`

## 10. When raw browser control is still acceptable

Use targeted evaluate or browser control when:
- you need a narrow UI probe not covered by the adapter
- you need render-only confirmation beyond adapter output
- you are handling a one-off X surface the adapter does not expose yet

Even then:
- keep calls targeted
- respect tab discipline
- verify the visible result afterward

## 11. Common X blockers

Watch for:
- acting from the wrong logged-in account
- login walls and auth redirects
- rate limits or "try again later" states
- stale composer state
- disabled Post/Reply buttons caused by character-limit overflow or unresolved compose state
- action buttons that render before the route is settled
- delayed thread hydration after opening a post
- community posting surfaces that differ from the main composer
- partial switcher extraction that hides available accounts
- text that appears in the composer but is not accepted as real typed input
- poisoned or frozen tabs after retries

When blocked:
- name the blocker plainly
- say whether it is retryable, recoverable with `x_recover`, or human-blocked
- do not quietly lower the proof bar
- if switcher or composer state is ambiguous, escalate to visual confirmation fast

## 12. Token-efficiency rules for X

Prefer:
- `x_get_state` over generic broad page inspection
- adapter extraction over full DOM reads
- route-specific verification over repeated giant snapshots
- small post-action checks over re-scraping whole timelines

Avoid:
- full-page HTML grabs for simple posting tasks
- repeated generic perception when the X adapter already knows the route
- reading giant feeds when only one post or thread matters

## 13. Minimal X checklist

Before claiming an X task done, confirm:
- correct account
- correct route
- correct target post/profile/community
- intended action executed
- visible result verified
- spare tabs cleaned up
- feed-first behavior used unless there was a real reason not to

Before claiming account switching done, confirm:
- switcher was actually opened
- intended account row was visible, ideally as a full user cell
- sidebar account label changed afterward
- destination route settled on a normal X surface

## 14. Account switching and composer recovery patterns

### Account switching

Known-good sequence:
1. inspect current active account from the sidebar first
2. open the bottom-left account switcher deliberately
3. if the menu contents are unclear, take a screenshot or visual snapshot
4. prefer clicking the full target account row, not random nearby text
5. verify the sidebar account label changed after the click
6. verify the route landed on a normal X page like Home, not a stale modal state

Do not conclude an account is unavailable from one weak extraction pass.
A hidden or partially extracted menu is common on X.

### Composer says text is there but Post is still disabled

This is a real X failure mode.

If the composer visibly contains text but submit is still disabled:
1. check character count or remaining characters
2. rule out overflow first
3. assume DOM-only insertion may not have registered as real input
4. switch to real keyboard-style interaction immediately
5. re-check the enabled state before submitting

Known-good fallback:
- focus composer
- select all
- clear
- type through the real input path
- verify remaining character count or enabled Post button
- only then submit

## 15. Relationship to other docs

Use alongside:
- `browser-operations` for universal browser rules
- `x-engagement` when the goal is audience growth, founder-style replies, and community participation
- `X_STATE_MAP.md` for concrete switcher, community, and composer landmarks
- SurfAgent skill for managed Chrome discipline
- X adapter docs for the concrete MCP/tool surface
