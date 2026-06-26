# X (Twitter) — Platform Reference

Background knowledge for automating X (formerly Twitter) tasks via agent-browser.

---

## Page Structure

### Home Feed (`x.com/home` or `x.com`)

The home feed uses a single-page React app. Key interactive elements:

- **Left sidebar navigation**: Home, Search and explore, Notifications, Follow, Direct Messages, Grok, Profile, More menu items, Post button
- **Feed tabs**: `tab "For you"` (algorithmic) and `tab "Following"` (chronological)
- **Compose box** (inline at top of feed): `textbox "Post text"` with action buttons:
  - "Add photos or video", "Choose File", "Add a GIF", "Enhance your post with Grok", "Add poll", "Add emoji", "Schedule post", "Tag location", "Content disclosure"
  - `button "Post"` (disabled until text entered)
- **Post cards**: Each post in the feed has:
  - User name link (with "Verified account" label if verified)
  - Handle link (`@username`)
  - Timestamp link (clicking this navigates to post detail page)
  - `button "Grok actions"` — AI-related actions
  - `button "More"` — additional options menu
  - `button "Show more"` — expand truncated post text
  - `button "N Replies. Reply"` — reply count + reply action
  - `button "N reposts. Repost"` — repost/retweet count + action
  - `button "N Likes. Like"` — like count + action
  - `link "N views. View post analytics"` — view count
  - `button "Bookmark"` — save to bookmarks
  - `button "Share post"` — share options
- **Pinned/Recommended**: Some posts show `button "Pinned by people you follow More"` section

### Post Detail Page (`x.com/<username>/status/<id>`)

- **Back button**: `button "Back"` to return to previous page
- **Post header**: User name, handle, Follow button, Grok actions, More button
- **Post content**: Full text (with `button "Show translation"` for non-English posts)
- **Timestamp**: `link "H:MM AM/PM · Mon DD, YYYY"` format
- **View count**: `link "N Views"`
- **Action buttons** (same as feed but with full counts):
  - `button "N Replies. Reply"`
  - `button "N reposts. Repost"`
  - `button "N Likes. Like"`
  - `button "N Bookmarks. Bookmark"` (shows bookmark count on detail page)
  - `button "Share post"`
- **Sort control**: `button "Relevant"` to change reply sort order
- **Quotes**: `link "View quotes"` to see quote tweets
- **Reply box**: Below the post, shows:
  - `button "Replying to @username"` label
  - Current user name link
  - `textbox "Post text"` — the reply input
  - Action buttons: photos/video, GIF, Grok enhance, emoji, location, content disclosure
  - `button "Reply"` (disabled until text entered)

### Reply/Comment Structure

Replies appear below the reply input box. Each reply has the same structure as a feed post:
- User name + handle + timestamp links
- Grok actions, More button
- Reply/Repost/Like/Views/Bookmark/Share buttons
- Nested replies show threading via indentation

### Search/Explore Page (`x.com/explore` or `x.com/search`)

#### Explore page (`x.com/explore`):
- **Search box**: `combobox "Search query"` — type and press Enter to search
- **Settings**: `link "Settings"` for search settings
- **Tabs**: For You, Trending, News, Sports, Entertainment
- **Trending topics**: Each shows title, category, post count, and `button "More"` for options

#### Search results (`x.com/search?q=<query>&src=typed_query`):
- **Search box**: `combobox "Search query"` (editable, pre-filled with query)
- **Back button**: `button "Back"`
- **Filter menu**: `button "More"` next to search box
- **Tabs**: Top, Latest, People, Media, Lists
- **Results**: Same post card structure as home feed

### Compose Modal (Post button in sidebar)

Clicking `link "Post"` in the left sidebar opens a modal overlay:
- `button "Close"` — dismiss the modal
- `button "Drafts"` — access saved drafts
- `textbox "Post text"` — the compose input (contenteditable div)
- `button "Everyone can reply"` — set reply permissions
- Action buttons: photos/video, GIF, Grok enhance, poll, emoji, schedule, location, content disclosure
- `button "Post"` (disabled until text entered)

### User Profile Page (`x.com/<username>`)

- Profile photo, banner
- `button "More"` — additional options
- `button "Message"` — send DM
- `button "Follow @username"` — follow/unfollow
- Verification badge: `button "Provides details about verified accounts."`
- Bio with `button "Show translation"` if applicable
- Join date, Following count, Followers count
- **Tabs**: Posts, Replies, Highlights, Articles, Media

---

## Common Operations

### Browse Home Feed

```bash
agent-browser --auto-connect open https://x.com/home
agent-browser --auto-connect wait 3000        # X loads slowly, avoid networkidle
agent-browser --auto-connect snapshot -i       # see posts and actions
agent-browser --auto-connect scroll down 1000  # load more posts
agent-browser --auto-connect snapshot -i       # re-snapshot after scroll
```

### Search for Posts

```bash
agent-browser --auto-connect open "https://x.com/search?q=AI%20agents&src=typed_query"
agent-browser --auto-connect wait 3000
agent-browser --auto-connect snapshot -i

# Or navigate to explore and type:
agent-browser --auto-connect open https://x.com/explore
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect fill @eSearchBox "vector database AI"
agent-browser --auto-connect press Enter
agent-browser --auto-connect wait 3000
agent-browser --auto-connect snapshot -i

# Switch to Latest tab for most recent results:
agent-browser --auto-connect click @eLatestTab
```

### Read a Post (Detail Page)

Option A — click the timestamp link in the feed:
```bash
agent-browser --auto-connect snapshot -i
# Find the timestamp link (e.g., "Mar 3", "3 hours ago") — this navigates to the post detail page
agent-browser --auto-connect click @eTimestamp
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i
```

Option B — navigate directly:
```bash
agent-browser --auto-connect open "https://x.com/<username>/status/<tweet_id>"
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i
```

**Important**: Clicking the user name link navigates to the user's profile, NOT the post. Always click the timestamp link to go to the post detail page.

### Reply to a Post

1. Navigate to the post detail page
2. Find the reply `textbox "Post text"` (below the post, after the action buttons)
3. Fill and submit:
```bash
agent-browser --auto-connect snapshot -i
# Find the textbox ref for "Post text"
agent-browser --auto-connect fill @eReplyBox "Your reply text here"
agent-browser --auto-connect snapshot -i   # re-snapshot to get enabled Reply button
agent-browser --auto-connect click @eReply  # button "Reply"
```

### Like / Repost / Bookmark

```bash
agent-browser --auto-connect snapshot -i
# Each post has clearly labeled buttons:
agent-browser --auto-connect click @eLike     # button "N Likes. Like"
agent-browser --auto-connect click @eRepost   # button "N reposts. Repost"
agent-browser --auto-connect click @eBookmark # button "Bookmark"
```

### Create a New Post

#### Via sidebar Post button (opens modal):
```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @ePostLink   # link "Post" in sidebar
agent-browser --auto-connect wait 1000
agent-browser --auto-connect snapshot -i

agent-browser --auto-connect fill @eTextbox "Your post content here"
agent-browser --auto-connect snapshot -i   # re-snapshot to get enabled Post button
agent-browser --auto-connect click @ePost  # button "Post"
```

#### Via inline compose box on home feed:
```bash
agent-browser --auto-connect open https://x.com/home
agent-browser --auto-connect wait 3000
agent-browser --auto-connect snapshot -i

# The textbox "Post text" is at the top of the feed
agent-browser --auto-connect fill @eTextbox "Your post content here"
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @ePost  # button "Post"
```

**Important**: Always confirm with the user before actually submitting a post.

### Follow / Unfollow a User

```bash
# From a post detail page or user profile:
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eFollow   # button "Follow @username"
```

---

## Known Quirks & Workarounds

### `open x.com` often times out

X loads slowly and the default 10s timeout for `open` frequently fails.

**Workaround**: If the browser already has X open in a tab, use `tab list` and `tab <index>` to switch to it instead of opening a new page. If you must open fresh, retry or use a longer timeout:
```bash
AGENT_BROWSER_DEFAULT_TIMEOUT=30000 agent-browser --auto-connect open https://x.com/home
```

### Avoid `wait --load networkidle`

Like Reddit, X uses continuous background network activity (streaming, analytics, real-time updates). The `networkidle` state is rarely or never reached.

**Workaround**: Use `wait 2000` or `wait 3000` for a fixed delay after navigation. Or wait for a specific element:
```bash
agent-browser --auto-connect wait "[data-testid='primaryColumn']"
```

### Clicking user name navigates to profile, not post

In the feed, both the user name and the timestamp are clickable links. Clicking the user name goes to the profile page; clicking the timestamp (e.g., "Mar 3", "3 hours ago") goes to the post detail page.

**Workaround**: Always click the timestamp link to navigate to a specific post.

### Post text input is a contenteditable div

The compose and reply textboxes use `contenteditable="true"` divs (DraftJS editor), not standard `<input>` or `<textarea>` elements. The `data-testid` is `tweetTextarea_0`.

**Workaround**: Use `fill @ref "text"` which works with contenteditable elements in agent-browser. If fill doesn't work, try `click @ref` first, then `keyboard type "text"`.

### Refs go stale after scrolling or navigation

X's SPA architecture means DOM changes frequently. After scrolling, navigating, or any action that changes the page content, refs become invalid.

**Workaround**: Always re-run `snapshot -i` after any action before using refs.

### Translation layer affects element labels

If Chrome has translation enabled, buttons and labels may show dual-language text (e.g., `button "Post 帖子"`, `button "Reply 回复"`). Interactive elements still work — just be aware that text matching may need to account for translated text.

### Multiple textboxes on the page

The post detail page may have both the search box and the reply textbox labeled "Post text". To identify the correct one:
- The reply textbox appears after the post action buttons and `button "Replying to @username"`
- Use `snapshot -i` to see the full context and pick the right ref

### "Show more" button for truncated posts

Long posts are truncated in the feed with a `button "Show more"` to expand. Click it to see the full text before interacting.

---

## Useful URLs

- Home feed: `https://x.com/home`
- Explore/Trending: `https://x.com/explore`
- Search: `https://x.com/search?q=<query>&src=typed_query`
- User profile: `https://x.com/<username>`
- Post detail: `https://x.com/<username>/status/<tweet_id>`
- Notifications: `https://x.com/notifications`
- Direct Messages: `https://x.com/messages`
- Bookmarks: `https://x.com/i/bookmarks`
- Lists: `https://x.com/<username>/lists`
- Compose (direct): `https://x.com/compose/post`

## AI-Related Accounts & Hashtags

### Key AI accounts to follow/engage:
- `@OpenAI` — OpenAI official
- `@AnthropicAI` — Anthropic official
- `@GoogleDeepMind` — Google DeepMind
- `@karpathy` — Andrej Karpathy
- `@ylecun` — Yann LeCun
- `@geoffreyhinton` — Geoffrey Hinton
- `@fchollet` — François Chollet
- `@jimfan` — Jim Fan (NVIDIA)
- `@emaborevkova` — Emad Mostaque
- `@huggingface` — Hugging Face

### AI-related search queries:
- `AI agent` / `AI agents`
- `vector database` / `vector search`
- `RAG` / `retrieval augmented generation`
- `LLM` / `large language model`
- `Claude` / `GPT` / `Gemini`
- `embedding` / `semantic search`
- `Milvus` / `Zilliz`
