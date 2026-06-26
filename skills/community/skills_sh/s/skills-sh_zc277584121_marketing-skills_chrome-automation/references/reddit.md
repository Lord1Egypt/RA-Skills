# Reddit — Platform Reference

Background knowledge for automating Reddit tasks via agent-browser.

---

## Page Structure

### Subreddit Feed (`/r/<subreddit>`)

The feed page uses custom web components (`faceplate-*`). Key interactive elements:

- **Top bar**: Search box, "Create Post" link, chat, inbox, user menu
- **Post cards**: Each post has: title link, Upvote/Downvote buttons, "Go to comments" link, "Give award" button, "Share" button, "Open user actions" button
- **Right sidebar**: Subreddit info, rules, community bookmarks
- **Left sidebar**: Navigation (Home, Popular, News, Explore), recent subreddits

The "Create Post" button appears twice: once in the top nav bar (`ref` labeled "Create post") and once in the subreddit header area ("Create Post"). Either works.

### Post Detail Page (`/r/<subreddit>/comments/<id>/...`)

- **Post content**: Title, body text or link, embedded media
- **Post actions**: Upvote, Downvote, "Go to comments", "Give award", "Share"
- **Comment input**: An unlabeled `textbox` appears below the post. Clicking it activates the editor with "Cancel" and "Comment" buttons.
- **Comments**: Each comment has: Upvote, Downvote, **Reply**, Give award, Share buttons, plus a "Toggle Comment Thread" to collapse/expand.
- **Sort**: "Sort by" dropdown (Top, Best, New, etc.) and a "Search Comments" button.

### Create Post Page (`/r/<subreddit>/submit`)

- **Subreddit selector**: Dropdown to choose the target subreddit
- **Post type tabs**: Text, Images & Video, Link, Poll, AMA
- **Title field**: `textbox "Title"` — standard input, use `fill`
- **Body field**: `textbox "Post body text field"` — this is a rich text editor with a formatting toolbar (Bold, Italic, Strikethrough, Superscript, Heading, Link, Image, Video, Bullet List, Number List, Spoiler, Quote Block, Code, Code Block, Table)
- **Flair**: "Add flair and tags" button (required in some subreddits)
- **Submit**: "Post" button (disabled until title is filled), "Save Draft" button
- **Drafts**: "Drafts" button to access saved drafts

### User Profile Page (`/user/<username>`)

- Overview of posts and comments
- Profile info sidebar

---

## Common Operations

### Browse a Subreddit

```bash
agent-browser --auto-connect tab list                     # check if already open
agent-browser --auto-connect open https://www.reddit.com/r/artificial/
agent-browser --auto-connect snapshot -i -c               # see posts and actions
agent-browser --auto-connect scroll down 800              # load more posts
```

### Read a Post

Option A — click by ref after snapshot:
```bash
agent-browser --auto-connect snapshot -i -c
# Find the post title link ref, then:
agent-browser --auto-connect click @eN
```

Option B — navigate directly (more reliable, avoids stale refs):
```bash
agent-browser --auto-connect open "https://www.reddit.com/r/<subreddit>/comments/<id>/..."
```

### Comment on a Post

1. Navigate to the post detail page
2. Find the comment textbox (unlabeled `textbox` below the post)
3. Click it to activate the editor
4. Type the comment — use `fill` since it's a standard textbox:
   ```bash
   agent-browser --auto-connect snapshot -i -c
   # Find the textbox ref (unlabeled textbox, NOT the search box)
   agent-browser --auto-connect click @eN
   agent-browser --auto-connect fill @eN "Your comment text here"
   ```
5. Click the "Comment" button to submit

### Reply to a Comment

1. Scroll to the target comment
2. Click the "Reply" button on that comment
3. A reply editor will appear — fill it similarly to the main comment box
4. Submit with the "Comment" or "Reply" button

### Upvote / Downvote

```bash
agent-browser --auto-connect snapshot -i -c
# Each post/comment has Upvote and Downvote buttons
agent-browser --auto-connect click @eN   # the Upvote button ref
```

### Create a New Post

```bash
agent-browser --auto-connect open "https://www.reddit.com/r/<subreddit>/submit"
agent-browser --auto-connect snapshot -i -c

# Fill title (standard input)
agent-browser --auto-connect fill @eTitle "Your post title"

# Fill body (rich text editor — use fill since Reddit exposes it as a textbox)
agent-browser --auto-connect fill @eBody "Your post body text"

# Add flair if required
agent-browser --auto-connect click @eFlair

# Submit
agent-browser --auto-connect click @ePost
```

**Important**: Always confirm with the user before actually submitting a post.

---

## Known Quirks & Workarounds

### `wait --load networkidle` times out on Reddit

Reddit uses continuous background network activity (analytics, real-time updates, ads). The `networkidle` state is never reached.

**Workaround**: Skip `wait --load networkidle` for Reddit. The `open` command itself waits for initial load, and its success message includes the page title — if you see the title, the page is ready. If needed, use `wait 2000` for a short fixed delay instead.

### `find text` strict mode fails on Reddit

Reddit renders many elements twice (e.g., a screen-reader-only version and a visible version of post titles). This causes `find text "..."` to match multiple elements and fail with a strict mode violation.

**Workaround**: Always prefer `snapshot -i` → find ref → `click @eN` over `find text`. If you must use `find text`, make the query very specific or use `find first text "..." click` if available.

### Post title links appear multiple times in snapshot

Each post title shows up as 2-3 separate link refs (screen-reader text, visible title, thumbnail). When clicking a post, prefer the one that contains the full title text, or better yet, extract the post URL from the error message or snapshot and use `open` to navigate directly.

### Refs go stale after scrolling

Reddit's infinite scroll dynamically loads content. After scrolling, previously captured refs may no longer be valid (timeout errors when clicking).

**Workaround**: Always re-run `snapshot -i` after scrolling before interacting with elements.

### Reddit's translation layer

If the user's Chrome has translation enabled, Reddit may show dual-language text (English + translated). This affects element labels in snapshots. The interactive elements (buttons, inputs) still work the same way — just be aware that text matching may need to account for translated text.

### Comment box is an unlabeled textbox

The main comment textbox on post detail pages has no label/placeholder text in the snapshot. It appears as just `textbox [ref=eN]`. To identify it:
- It's the textbox that is NOT the search box (which is labeled "Remove r/... filter and expand search to all of Reddit")
- It appears between the post actions and the comment sort controls

---

## Useful URLs

- Reddit homepage: `https://www.reddit.com`
- Specific subreddit: `https://www.reddit.com/r/<subreddit>`
- User profile: `https://www.reddit.com/user/<username>`
- Submit post: `https://www.reddit.com/r/<subreddit>/submit`
- Post detail: `https://www.reddit.com/r/<subreddit>/comments/<post_id>/<slug>/`

## AI-Related Subreddits

- `r/artificial` — General AI news and discussion
- `r/LocalLLaMA` — Local LLM deployment and usage
- `r/MachineLearning` — ML research and papers
- `r/singularity` — AGI and technological singularity
- `r/ChatGPTCoding` — AI-assisted coding
- `r/ClaudeAI` — Claude-specific discussion
- `r/ArtificialInteligence` — AI discussion (note: misspelled subreddit name)
- `r/Rag` — Retrieval-Augmented Generation
