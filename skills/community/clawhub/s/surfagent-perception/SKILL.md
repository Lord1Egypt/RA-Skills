---
name: surfagent-perception
description: Agent vision for web pages — scene summaries, attention-ranked elements, annotated screenshots, and state diffing via SurfAgent's perception engine.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://surfagent.app
    emoji: "👁️"
---

# SurfAgent Perception — Agent Vision Skill

> How to see, understand, and verify web pages through SurfAgent's perception engine.

---

## What This Is

SurfAgent Perception gives you **human-like page understanding** in ~200 tokens instead of parsing a 50K-token DOM. Three MCP tools, one workflow loop.

**Without perception:** You get a raw DOM dump or a dumb screenshot. You have to figure out what's on the page yourself.

**With perception:** You get a scene summary, ranked interactive elements, spatial clusters, viewport state, and optionally an annotated screenshot with numbered bounding boxes + a legend mapping each number to a ref.

**Requires:** [SurfAgent](https://surfagent.app) daemon running (port 7201) with a managed Chrome instance (port 9222).

---

## The Three Tools

### `surf_perceive` — Your Primary Eyes

The main tool. Call this to understand what's on screen.

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `tabId` | string | active tab | Target a specific tab |
| `since` | string | — | State token from a previous call. Includes delta of what changed |
| `maxAnnotations` | number | 15 | How many elements to rank (1-50) |
| `annotate` | boolean | false | Include annotated screenshot with numbered bounding boxes |

**Returns:**
- **Scene summary** — one-liner + top 5 ranked actions + state notes (blockers, modals, forms, auth, scroll %)
- **Viewport info** — scroll position, fold split, document dimensions
- **Top elements** — attention-ranked, with refs for clicking/typing
- **Clusters** — semantic groups of related elements (nav cluster, form cluster, etc.)
- **State token** — pass as `since` next time to get delta
- **Annotated screenshot + legend** (if `annotate: true`)

**When to use:** Start of any page interaction. After navigation. When you need to understand the page before acting.

---

### `surf_annotate` — Quick Visual Reference

Lighter than `surf_perceive`. Just the annotated screenshot + legend, no scene analysis.

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `tabId` | string | active tab | Target a specific tab |
| `maxAnnotations` | number | 15 | How many elements to annotate (1-50) |

**Returns:**
- Annotated screenshot (base64 PNG) with numbered colored bounding boxes
- Legend mapping each number to element ref, role, location, and status

**When to use:** When you already know the page context but need to identify specific elements visually. Good for "which button do I click?" scenarios.

---

### `surf_scene_diff` — What Changed?

Compare current state to a previous state token. Answers: "did my action work?"

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `since` | string | ✅ | State token from a previous `surf_perceive` call |
| `tabId` | string | — | Target a specific tab |

**Returns:**
- Current one-liner scene description
- Delta: new elements, removed elements, value changes, page type changes, auth state changes
- New state token for the next diff

**When to use:** After clicking, typing, submitting, or scrolling. Verifies your action had the intended effect.

---

## The Core Loop

This is the pattern for any page interaction:

```
1. PERCEIVE  →  Understand what's on screen
2. ACT       →  Click, type, scroll, fill
3. DIFF      →  Verify the action worked
4. REPEAT    →  Back to perceive if more actions needed
```

### Example: Login Flow

```
Step 1: surf_perceive()
  → "[GitHub · login · logged_out] Login form on GitHub"
  → Top actions: [1] Username input, [2] Password input, [3] Sign in button
  → State token: st_abc_1

Step 2: Type username into element [1], type password into [2], click [3]

Step 3: surf_scene_diff(since: "st_abc_1")
  → "auth state changed, page type changed"
  → "[GitHub · dashboard · logged_in] Dashboard — 4 sections"
  → ✅ Login worked

Step 4: surf_perceive() to explore the dashboard
```

### Example: Verify a Click

```
Step 1: surf_perceive() → get state token
Step 2: Click the "Submit" button
Step 3: surf_scene_diff(since: token)
  → "1 element removed, modal appeared"
  → "📋 Modal: Order Confirmed (2 actions)"
  → ✅ Submission worked
```

### Example: Monitor a Value

```
Step 1: surf_perceive() → note BTC price, get token
Step 2: Wait 30 seconds
Step 3: surf_scene_diff(since: token)
  → "2 elements changed: price_display $65,100→$65,234"
```

---

## Reading the Scene Summary

The scene summary has a consistent format:

```
[Domain · pageType · authState] Context description

Top actions:
1. Buy Button (button, center-right)
2. Price Input (textbox, top-center)
3. Symbol Search (textbox, top-left)

State notes:
⚠ Cookie banner: Accept cookies to continue (auto-dismissable)
📝 Form: 2/5 fields, submit: ref_submit_btn
📜 Scrolled 45%
🔒 Not logged in

Δ 2 elements changed: price $65,100→$65,234, volume +12.3K
```

### One-Liner Format
`[Domain · pageType · authState] Description`

**Page types:** login, signup, feed, detail, dashboard, chat, search_results, checkout, compose, settings, profile, docs, table, media, error_page, captcha, blank, other

**Auth states:** logged_in, logged_out, session_expired, unknown

### State Notes (what to look for)
| Symbol | Meaning |
|--------|---------|
| ⚠ | Blocker detected (cookie banner, captcha, auth wall). Check if `auto-dismissable` |
| 📋 | Modal is open — has title and action count |
| 📝 | Active form — shows filled/total fields and submit ref |
| 🔒 | Not logged in or session expired |
| 📜 | Page is scrolled — shows percentage |

### Delta Format
When you pass a `since` token, the delta section tells you exactly what changed:
- URL/title/page type/auth state changes
- Elements changed (with from→to values)
- New elements appeared (with role)
- Elements removed
- Regions updated

---

## Annotated Screenshots

When you call `surf_perceive(annotate: true)` or `surf_annotate()`, you get:

1. **A screenshot** with numbered colored bounding boxes on interactive elements
2. **A legend** mapping each number to structured info:

```
[1] Sign In (button, center) — clickable
[2] Email: user@email.com (textbox, top-center) — editable
[3] Remember me (checkbox, center-left) — unchecked
```

### Color Coding
- 🟢 Green: buttons, submit actions
- 🔵 Blue: text inputs, textareas, selects
- 🟣 Purple: links, navigation
- 🟡 Yellow: checkboxes, radio buttons, toggles
- ⚪ Gray: headings, labels, static content

### Using Annotations for Action
The legend gives you element refs. Use those refs with SurfAgent's click/type/fill tools to interact with the exact elements you identified visually.

---

## Element Ranking: How Attention Scoring Works

Not all elements are equal. The perception engine scores elements across 7 dimensions:

1. **Centrality** — Distance from viewport center (center elements rank higher)
2. **Context relevance** — Page-type-aware boosting (login → password/submit boosted, feed → content/compose boosted, dashboard → metrics/actions boosted, checkout → payment/order boosted)
3. **Role score** — Buttons > inputs > links > headings > images
4. **Visual weight** — Size, font weight, contrast against background
5. **Proximity to focus** — Elements near the viewport center or active form
6. **Visibility** — Above-fold elements rank higher than below-fold
7. **Action density** — Elements in clusters of interactive elements get boosted

Final score = weighted combination → top N returned.

---

## Clusters

Elements are spatially grouped into clusters (50px proximity threshold):

```
Cluster: "Navigation" (top-left)
  - Home link, Dashboard link, Settings link

Cluster: "Login Form" (center)
  - Email input, Password input, Sign In button, Forgot Password link
```

Use clusters to understand the page layout at a glance. Each cluster has:
- Label (auto-inferred from content)
- Bounding rect
- Primary action (the highest-scored interactive element in the cluster)
- Member elements

---

## Performance

- **~200 tokens** per scene summary (vs ~50K for raw DOM)
- **<200ms** per perceive call (no LLM involved — all heuristic)
- **State tokens** are lightweight ring buffers (5 per tab, 20 tabs max)
- **Annotated screenshots** add ~100-200ms for Canvas overlay

---

## Anti-Patterns

❌ **Don't call `surf_perceive` AND `surf_page_state` on the same page** — perceive already includes everything page_state gives you, plus attention ranking and scene summary. It's redundant.

❌ **Don't call `surf_annotate` unless you actually need the screenshot** — the image is large (base64 PNG). If you just need to know what's on the page, use `surf_perceive` without `annotate: true`.

❌ **Don't ignore state tokens** — always capture them. They're your "save point" for diffing later.

❌ **Don't perceive after every micro-action** — if you're typing into a field, you don't need to perceive after each keystroke. Perceive before the interaction, act, then diff after.

❌ **Don't assume element refs are permanent** — refs are content-hashed and stable across re-rankings of the same page, but they change when the page content changes. Re-perceive after navigation.

---

## Decision Tree: Which Tool Do I Use?

```
Need to understand the page?           → surf_perceive()
Need to verify an action worked?       → surf_scene_diff(since: your_token)
Need to visually identify an element?  → surf_annotate()
Need both understanding AND visual?    → surf_perceive(annotate: true)
Just need basic page info?             → surf_page_state() (lighter, no scoring)
```

---

## Integration with Other SurfAgent Tools

| After perceive... | Use this to act |
|-------------------|-----------------|
| Identified a button to click | `/browser/click` with element ref or coordinates |
| Found a form to fill | `/browser/fill` with selector from element data |
| Detected a blocker | `/browser/resolve-blocker` to auto-dismiss |
| Need to scroll for more content | `/browser/scroll` then `surf_scene_diff` |
| Want to navigate somewhere | `/browser/navigate` then `surf_perceive` |
| Detected a captcha | `/browser/captcha/solve` |

---

## Daemon HTTP Endpoints (Direct API)

If calling the daemon directly instead of through MCP:

### `POST /browser/perceive`
```json
{
  "tabId": "optional",
  "since": "optional state token",
  "maxAnnotations": 15,
  "annotate": false
}
```

Returns: `{ ok, scene, viewport, topElements, clusters, stateToken, annotatedScreenshot?, legend? }`

### `POST /browser/annotate`
```json
{
  "tabId": "optional",
  "maxAnnotations": 15
}
```

Returns: `{ ok, annotatedScreenshot, legend }`

Both endpoints require Bearer auth token (`~/.surfagent/daemon-token.txt`).
