# Hacker News — Platform Reference

Background knowledge for automating Hacker News (news.ycombinator.com) tasks via agent-browser.

---

## Page Structure

Hacker News is an extremely minimal, server-rendered HTML site with no JavaScript frameworks. All pages are plain HTML tables. This makes it the easiest platform to automate, but form fields have no labels or placeholders.

### Front Page (`news.ycombinator.com/`)

- **Top navigation bar**:
  - `link "Hacker News"` — home link
  - `link "new"`, `link "threads"`, `link "past"`, `link "comments"`, `link "ask"`, `link "show"`, `link "jobs"` — section links
  - `link "submit"` — submit new post
  - `link "<username>"` — your profile (if logged in)
  - `link "logout"` — log out

- **Post list**: Each post has:
  - `link "upvote"` — upvote arrow
  - **Title link**: `link "<Post Title>"` — the post title (clicking navigates to external URL or post detail)
  - **Domain link**: `link "<domain.com>"` — the source domain
  - **Author link**: `link "<username>"` — who submitted it
  - **Timestamp link**: `link "N hours ago"` — links to the post's comment page
  - `link "hide"` — hide the post
  - **Comments link**: `link "N comments"` — navigate to comment/discussion page
  - For posts with no comments: `link "discuss"` instead

- **Bottom**: `link "More"` to load next page of posts

- **Footer**: `textbox` (search box, unlabeled), Guidelines, FAQ, Lists, API, Security, Legal, Apply to YC, Contact

### Post Detail / Comments Page (`news.ycombinator.com/item?id=<id>`)

- **Post header**: Same structure as front page (upvote, title, domain, author, timestamp)
- **Additional post links**: `link "past"`, `link "favorite"`, `link "N comments"`
- **Comment input**: `textbox` (unlabeled) + `button "add comment"`
  - `link "help"` — formatting help
- **Comments**: Each comment has:
  - `link "upvote"` — upvote the comment
  - **Author link**: `link "<username>"`
  - **Timestamp link**: `link "N minutes ago"`
  - `link "[–]"` — collapse/fold the comment thread
  - Comment text (plain text, not interactive)
  - `link "reply"` — navigate to reply page

### Reply Page (`news.ycombinator.com/reply?id=<comment_id>&goto=...`)

Clicking `link "reply"` on a comment navigates to a **separate page** with:
- The parent comment displayed for context
- `link "upvote"` — upvote the parent
- `link "<username>"` — parent author
- `link "parent"`, `link "context"` — navigation links
- `link "<Original Post Title>"` — link back to original post
- `textbox` (unlabeled) — the reply textarea
- `link "help"` — formatting help
- `button "reply"` — submit the reply

### Submit Page (`news.ycombinator.com/submit`)

Three unlabeled form fields:
- `textbox` (1st) — **title** (`name="title"`, type text)
- `textbox` (2nd, `[nth=1]`) — **url** (`name="url"`, type url)
- `textbox` (3rd, `[nth=2]`) — **text** (`name="text"`, textarea, for text-only posts)

`button "submit"` — submit the post

**Note**: Submit either a URL or text, not both. If URL is provided, text is ignored.

### Other Pages

- **New**: `news.ycombinator.com/newest` — latest posts
- **Ask HN**: `news.ycombinator.com/ask` — question posts
- **Show HN**: `news.ycombinator.com/show` — project showcases
- **Jobs**: `news.ycombinator.com/jobs` — job listings
- **Past**: `news.ycombinator.com/front?day=YYYY-MM-DD` — historical front page
- **User profile**: `news.ycombinator.com/user?id=<username>`
- **Submissions by domain**: `news.ycombinator.com/from?site=<domain>`
- **User's submissions**: `news.ycombinator.com/submitted?id=<username>`
- **User's comments**: `news.ycombinator.com/threads?id=<username>`

### Search

HN's built-in search is minimal (footer textbox). The primary search engine is **Algolia HN Search**:
- `hn.algolia.com/?q=<query>` — full-text search of HN
- May timeout; if so, use the HN API or browse by domain/tag

---

## Common Operations

### Browse Front Page

```bash
agent-browser --auto-connect open https://news.ycombinator.com
agent-browser --auto-connect wait --load networkidle   # HN loads instantly
agent-browser --auto-connect snapshot -i
```

### Read Comments on a Post

```bash
# Click the comments link from the front page:
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eComments   # link "N comments"
agent-browser --auto-connect wait 1000
agent-browser --auto-connect snapshot -i

# Or navigate directly:
agent-browser --auto-connect open "https://news.ycombinator.com/item?id=<post_id>"
```

### Upvote a Post or Comment

```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eUpvote   # link "upvote"
```

### Comment on a Post

```bash
# Navigate to the post's comment page first
agent-browser --auto-connect open "https://news.ycombinator.com/item?id=<post_id>"
agent-browser --auto-connect snapshot -i

# The comment textbox is unlabeled — find it by ref
agent-browser --auto-connect fill @eTextbox "Your comment here"
agent-browser --auto-connect click @eAddComment   # button "add comment"
```

### Reply to a Comment

```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eReply   # link "reply" — navigates to reply page
agent-browser --auto-connect wait 1000
agent-browser --auto-connect snapshot -i

agent-browser --auto-connect fill @eTextbox "Your reply here"
agent-browser --auto-connect click @eReplyBtn   # button "reply"
```

**Note**: Clicking "reply" navigates to a separate page. This is different from most platforms where reply forms appear inline.

### Submit a New Post

```bash
agent-browser --auto-connect open https://news.ycombinator.com/submit
agent-browser --auto-connect snapshot -i

# Fill title (1st textbox)
agent-browser --auto-connect fill @e2 "Your Post Title"

# Fill URL (2nd textbox) for link posts:
agent-browser --auto-connect fill @e3 "https://example.com/article"

# OR fill text (3rd textbox) for text/Ask HN posts:
agent-browser --auto-connect fill @e4 "Your post text here"

# Submit
agent-browser --auto-connect click @e5   # button "submit"
```

**Important**: Always confirm with the user before actually submitting a post.

### Search HN

```bash
# Option 1: Algolia HN Search (may be slow/timeout)
agent-browser --auto-connect open "https://hn.algolia.com/?q=vector+database"
agent-browser --auto-connect wait 3000

# Option 2: Browse by domain
agent-browser --auto-connect open "https://news.ycombinator.com/from?site=zilliz.com"

# Option 3: Use the footer search box on HN itself
agent-browser --auto-connect snapshot -i
# Find the unlabeled textbox at the bottom of the page
agent-browser --auto-connect fill @eSearchBox "AI vector database"
agent-browser --auto-connect press Enter
```

---

## Known Quirks & Workarounds

### All form fields are unlabeled

HN uses bare `<input>` and `<textarea>` elements with no labels, placeholders, or aria attributes. In snapshots, they appear as just `textbox [ref=eN]`.

**Workaround**: Use positional refs from `snapshot -i`. On the submit page: 1st textbox = title, 2nd = url, 3rd = text. On comment/reply pages: the textbox is the comment input.

### Reply navigates to a separate page

Unlike most platforms where reply forms appear inline, HN's `link "reply"` navigates to `news.ycombinator.com/reply?id=...`. Always re-snapshot after clicking reply.

### `networkidle` works perfectly

HN is pure server-rendered HTML with minimal JS. `wait --load networkidle` completes almost instantly.

### Upvote is a link, not a button

The upvote arrow is `link "upvote"`, not a button. It works the same way with `click`.

### No downvote for new accounts

Downvoting requires sufficient karma. If the user's account is new, downvote links won't appear.

### Rate limiting

HN has rate limits on posting and commenting. If you submit too quickly, you may get a "submitting too fast" error. Wait a few minutes and retry.

### Comment formatting

HN comments support limited formatting:
- Blank line for paragraph break
- `*italic*` for italics
- Indent with 2+ spaces for code blocks
- URLs are auto-linked
- No bold, no headers, no images

### Duplicate submission detection

HN detects duplicate URLs. If someone already submitted the same URL, you'll be redirected to the existing discussion.

### "past" link on posts

Each post has a `link "past"` which shows previous submissions of the same URL. This is useful for finding earlier discussions.

### Search footer textbox appears on every page

Every HN page has an unlabeled `textbox` in the footer for search. Don't confuse it with comment input boxes. The comment box typically appears before the first comment, while the search box is at the very bottom of the page.

---

## Useful URLs

- Front page: `https://news.ycombinator.com/`
- Newest: `https://news.ycombinator.com/newest`
- Ask HN: `https://news.ycombinator.com/ask`
- Show HN: `https://news.ycombinator.com/show`
- Jobs: `https://news.ycombinator.com/jobs`
- Submit: `https://news.ycombinator.com/submit`
- Post detail: `https://news.ycombinator.com/item?id=<id>`
- User profile: `https://news.ycombinator.com/user?id=<username>`
- User submissions: `https://news.ycombinator.com/submitted?id=<username>`
- User comments: `https://news.ycombinator.com/threads?id=<username>`
- Submissions from domain: `https://news.ycombinator.com/from?site=<domain>`
- Historical front page: `https://news.ycombinator.com/front?day=YYYY-MM-DD`
- Algolia search: `https://hn.algolia.com/?q=<query>`
- HN API: `https://hacker-news.firebaseio.com/v0/`

## AI-Related Patterns on HN

HN is one of the most influential platforms for AI/tech discussions. Common AI-related content patterns:

- **Show HN posts**: Great for launching tools/products (`Show HN: <Product> – <Description>`)
- **Ask HN posts**: Good for gathering feedback (`Ask HN: Best vector database for <use case>?`)
- **Blog post submissions**: Submit technical blog posts from your domain
- **Comment engagement**: Thoughtful comments on trending AI posts build reputation

Popular AI topics on HN:
- LLM releases and benchmarks
- AI agent frameworks
- Vector databases and RAG
- Open-source AI tools
- AI safety and ethics
- Startup launches (especially YC companies)
