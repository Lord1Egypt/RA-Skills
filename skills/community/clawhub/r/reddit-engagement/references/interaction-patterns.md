# Reddit Interaction Patterns (Accessibility-First)

## 0) Dynamic Subreddit Analysis Framework

**Purpose:** Handle new/unseen subreddits that don't have pre-defined cultural profiles in `post-strategy.md`.

### When to Use

Trigger this framework when:
- User requests posting/commenting in a subreddit NOT listed in `post-strategy.md` §1
- Subreddit name is extracted from user request (e.g., "去 r/Entrepreneur 发个帖")
- No cached archive exists in `sub-archives/` directory

### Step-by-Step Analysis Flow

#### Step 1: Navigate to Subreddit About Page
```
URL: https://www.reddit.com/r/<subname>/about
```
- Navigate to the about page
- Snapshot with `refs=aria`, `depth=12`

#### Step 2: Extract Community Metadata
Locate and extract these elements by semantic cues:

| Field | Semantic Locator | Fallback |
|-------|------------------|----------|
| **Member count** | text containing "members" / "Members" | regex: `[\d,\.]+[kKmM]?` near "member" |
| **Online count** | text containing "online" / "Online" | same as above |
| **Description** | paragraph under "About Community" heading | first non-nav paragraph in sidebar |
| **Created date** | text containing "Created" | regex: `[A-Z][a-z]+ \d+, \d{4}` |

#### Step 3: Extract Community Rules
```
Target: "R/<SUBNAME> RULES" section (may need to expand)
```

**Expand Rules Section (if collapsed):**
1. Find button/heading with text "Rules" or "R/<subname> RULES"
2. If rules not visible, look for expand arrow (role=button, name contains "expand" or "show")
3. Click to expand, wait 500ms, re-snapshot

**Extract Each Rule:**
For each rule item in the rules list:
- Rule number/title (e.g., "Rule 1: Be respectful")
- Rule description (paragraph under the rule title)
- Any associated icons (warning/restriction indicators)

Store rules as structured list:
```markdown
### Rules
1. **Rule Name**: Description
2. **Rule Name**: Description
...
```

#### Step 4: Analyze Recent Posts (Optional but Recommended)
```
URL: https://www.reddit.com/r/<subname>/new
```
Navigate to /new tab and snapshot to analyze:

| Signal | What to Look For |
|--------|------------------|
| **Post frequency** | Timestamp of last 5-10 posts |
| **Common flairs** | Flair text near post titles |
| **Title patterns** | Common prefixes/suffixes, question vs statement ratio |
| **Engagement level** | Comment counts and upvote ratios |
| **Content type** | Text posts vs links vs images |

#### Step 5: Generate Subreddit Profile
Create a concise profile following the format in `sub-archives.md`:

```markdown
## r/{SUBNAME}

| Field | Value |
|-------|-------|
| **Members** | X |
| **Posting Threshold** | |
| **AI Detection** | |
| **Language** | |
| **Tone** | |
| **Self-promo** | |

### Top 3 Rules
1.
2.
3.

### What Works
-

### Title Patterns
-

### Notes

```

#### Step 6: Append to Archive File

Append the generated profile to:
```
references/sub-archives.md
```

Use the template format at the bottom of `sub-archives.md`. Keep it concise — only core info needed for posting decisions.

### Integration with Content Generation

After generating the dynamic archive:

1. **Load the archive** as if it were a pre-defined profile in `post-strategy.md` §1
2. **Extract cultural signals** (tone, welcome/avoid patterns, title styles)
3. **Apply to content generation** following `SKILL.md` Workflow Router
4. **Flag for user review** if confidence is low (e.g., rules unclear, sparse data)

### Confidence Scoring

After analysis, assign confidence level:

| Level | Criteria | Action |
|-------|----------|--------|
| **High** | Rules clear + 10+ recent posts analyzed | Proceed with content generation |
| **Medium** | Rules clear but few posts, or vice versa | Generate content but flag for user review |
| **Low** | Rules missing/unclear + sparse data | Ask user for more context or manual review |

### Error Handling

| Error | Recovery |
|-------|----------|
| About page blocked (private sub) | Report "Subreddit is private" and ask for alternate |
| Rules section not found | Proceed without rules, flag as "unmoderated or rules hidden" |
| Rate limited / captcha | Pause and ask user to complete challenge |
| Subreddit doesn't exist | Check spelling, suggest similar subs |

---

## 1) Create Post

### Strategy Layer (Content Generation)

**Before executing this playbook:**

- If user provided fuzzy request (e.g., "post about OpenClaw") → execute content generation flow in `SKILL.md` Workflow Router first
- Load `references/post-strategy.md` for:
  - Subreddit cultural profile (§1)
  - Anti-AI writing rules (§2)
  - Content angle selection (§3)
  - Engagement triggers (§4)
- Load `PERSONA.md` for authentic personal facts
- Generate title and body content
- Obtain user confirmation (unless pre-authorized)

**This playbook assumes content is ready to publish.**

---

### Preconditions
- User provides: subreddit + title + body (or content generated via strategy layer)
- Browser is open on reddit and authenticated
- Content confirmed by user (if not pre-authorized)

### Steps
1. Navigate to subreddit URL (`/r/<name>`).
2. Snapshot (`refs=aria`).
3. Find post composer entry by semantic labels like:
   - "Create post"
   - "Create"
   - "Post"
4. Open composer and re-snapshot.
5. Fill title field (role textbox, name includes "Title").
6. Fill body field when provided (textbox/editor region named "Body", "Text", or "Post body").
7. Optional type switch (Text/Image/Link/Poll) by tab/button role with matching names.
8. Verify submit button semantic name in {"Post", "Submit", "Publish"} and enabled.
9. Click submit.
10. Verify success via one or more:
   - Post detail page opens
   - New post title visible
   - Success toast/banner

### Failure Recovery
- If composer not found: search global "Create" button from top nav.
- If subreddit posting restricted: return restriction reason and ask alternate subreddit.

---

## 2) Create Comment

### Strategy Layer (Content Generation)

**Before executing this playbook:**

- If user provided fuzzy request (e.g., "comment on this post") → execute content generation flow in `SKILL.md` Workflow Router first
- Load `references/comment-strategy.md` for comment-specific tactics (when available)
- Load `references/post-strategy.md` §2 for anti-AI writing rules (shared)
- Load `PERSONA.md` for authentic personal facts
- Read target post/comment to understand context
- Generate comment content with information increment (not just "+1")
- Obtain user confirmation (unless pre-authorized)

**This playbook assumes content is ready to publish.**

---

### Preconditions
- User provides: post URL + comment text (or content generated via strategy layer)
- Browser is open on reddit and authenticated
- Content confirmed by user (if not pre-authorized)

### Steps
1. Open target post URL.
2. Snapshot (`refs=aria`, depth=10) to find initial placeholder textbox.
3. Locate placeholder textbox (typically `textbox [ref=e267]` with `/placeholder: Join the conversation`).
   - ⚠️ Do NOT type into this placeholder ref — it is a custom web component (`faceplate-textarea-input`), not a real textarea.
4. **Click** the placeholder textbox ref to activate the Slate editor.
5. **Re-snapshot at depth=13** — this is required. The active editor appears deeply nested inside the ad block's thumbnail link element in the ARIA tree (an Reddit layout quirk). At shallower depths it won't appear.
6. Find `textbox [active] [ref=eXXXX]` — the high-numbered ref is the real Slate editor. Also note `button "Comment" [ref=eYYYY]` at the same level — you'll need it for submit.
7. Type comment text into the **active** textbox ref.
8. Click the `button "Comment"` ref found in step 6 (do NOT use evaluate to click "Comment" — use the direct ref to avoid hitting wrong elements).
9. Verify: evaluate `document.body.innerText.includes('<unique snippet>')`.

### ARIA Tree Quirk — Where the Editor Lives
After clicking the placeholder, Reddit renders the full Slate editor nested inside:
```
generic [ad block] [ref=e205]:
  link [Thumbnail image: ...] [ref=e253]:
    paragraph [ref=eXXX]
    textbox [active] [ref=eXXXX]   ← your typing target
      paragraph [ref=eXXX]
      button "Comment" [ref=eYYYY]  ← your submit target
      button "Cancel" [ref=eZZZZ]
    button "Show formatting options" [ref=...]
```
This structure is consistent across posts — always depth=13 to see it.

### Failure Recovery
- If locked thread/mod restrictions: report exact restriction text.
- If submit disabled: ensure non-empty content and no markdown-mode validation blocks.
- If "The field is required and cannot be empty" appears: you clicked submit on an empty editor. Reload the page and restart from step 2.
- If comment not found after submit: page may have redirected to user profile (normal Reddit behavior after submit) — navigate back to post and verify with evaluate.

---

## 3) Upvote

### Preconditions
- User provides target URL (post/comment) or clear target description.

### Steps
1. Open target context.
2. Snapshot (`refs=aria`).
3. Locate vote control near intended entity (post card or comment container).
4. Pick control whose accessible name implies upvote semantics:
   - "Upvote"
   - "Vote up"
   - localized equivalent with up-arrow context
5. Click once.
6. Verify state change via one or more:
   - button pressed/selected state
   - score increment (if visible)
   - control style/state indicates active vote

### Failure Recovery
- If already upvoted, return idempotent success.
- If ambiguous (multiple upvotes), anchor to nearest container that matches target title/snippet.

---

## 4) Candidate Scoring Heuristic

Use weighted scoring when multiple elements match.

- +8 exact role match
- +10 exact/strong accessible-name intent match
- +6 synonym match
- +7 in expected semantic container (composer/action row/comment item)
- +5 visible in viewport
- +2 enabled
- -3 outside viewport and no scroll evidence
- -5 conflicts with target entity context

Pick highest score above threshold 10.

If top-2 delta < 4, mark as ambiguous and do not click yet.

## 4.1) Uniqueness + Context-Lift Fallback

When selector returns multiple nodes:

1. Stop action.
2. Lift context to nearest parent semantic region.
3. Re-score with composite conditions:
   - role
   - aria-label / placeholder / accessible text
   - parent region match
4. If still ambiguous, return top 3–5 candidates and let planner choose.
5. Never spin on the same ambiguous ref id.

This avoids deadlocks caused by volatile refs like `e47` that map to multiple nodes.

---

## 5) Synonym Bank (EN/ZH)

- Post submit: Post / Submit / Publish / 发布 / 提交
- Comment submit: Comment / Reply / Post / 评论 / 回复 / 发布
- Upvote: Upvote / Vote up / 顶 / 赞同 / 点赞
- Composer: Create post / Start a post / 创建帖子 / 发帖

---

## 6) Anti-Brittle Rules

- Do not bind to `id`, dynamic class hashes, or nth-child paths.
- Do not assume fixed layout for old/new Reddit.
- Always refresh semantic map after action-induced rerender.
- Prefer intent anchor + local container instead of global first match.

---

## 7) Known Pitfalls (Hard-Won)

| Pitfall | Cause | Fix |
|---------|-------|-----|
| Typed text disappears / textbox stays empty | Reddit uses React — raw DOM `.value` JS assignment is silently ignored | Always use CDP `act type` (not `evaluate` to set `.value`) |
| `faceplate-textarea-input` doesn't accept input | It's a custom web component shell, not a real textarea | Click it first to expand the real Slate editor, then re-snapshot and target the new `textbox [active]` ref |
| "The field is required" error on submit | Clicked Comment button while textbox was still empty (typed into wrong ref) | Reload page, restart from step 1, be sure to click placeholder → snapshot → find `[active]` ref before typing |
| Comment not visible after clicking Comment | Reddit redirected to user profile (`/user/szy1840/`) after submit — this is normal | Navigate back to the post URL and verify with `evaluate document.body.innerText.includes(...)` |
| `textbox [active]` not visible in snapshot | Snapshot depth too shallow (< 13) | Always use `depth=13` after activating the editor |
| Wrong element clicked when using evaluate | `querySelectorAll('button')` may match multiple "Comment" buttons on the page | Use the direct `ref` from snapshot, not evaluate-based queries, for submit |
| Locked post — no comment box | Some subreddit posts are locked by mods | Check ARIA tree for "Locked post" text before attempting; skip and move to next post |
