# Dev.to — Platform Reference

Background knowledge for automating Dev.to (DEV Community) tasks via agent-browser.

---

## Page Structure

### Home Feed (`dev.to/`)

Dev.to is a Forem-based Ruby on Rails application. The page structure is straightforward HTML with minimal JavaScript framework overhead.

- **Top navigation bar**:
  - `link "DEV Community Home"` — logo/home link
  - `textbox "Search..."` — search box + `button "Search"`
  - `link "Create Post"` — navigate to post editor
  - `link "Notifications"` — notification center
  - `button "Navigation menu"` — hamburger menu (profile/settings)

- **Left sidebar**:
  - `link "Home"`, `link "DEV++"`, `link "Reading List"`, `link "Videos"`
  - `link "DEV Education Tracks"`, `link "DEV Challenges"`, `link "DEV Help"`
  - `link "Advertise on DEV"`, `link "Organization Accounts"`, `link "DEV Showcase"`
  - `link "About"`, `link "Contact"`, `link "Forem Shop"`
  - Social links: Twitter, Facebook, Github, Instagram, Twitch, Mastodon, Bluesky
  - `link "Customize tag priority"` — customize feed algorithm
  - Partner links: Google AI, Neon, Algolia

- **Feed area**:
  - `textbox "What's on your mind?"` — quick post prompt (links to editor)
  - Feed tabs: `link "Discover"` / `link "Following"`
  - `button "Toggle dropdown menu"` — feed sort options
  - **Article cards**: Each is a simple `link` with title and comment count, e.g.:
    - `link "I Run a Solo Company with AI Agent Departments 8 comments"`
  - Cards also contain tag links like `link "#discuss"`, `link "#ai"`

- **Right sidebar**:
  - Active discussions list with links
  - Sponsor/partner content
  - Listings

### Article Detail Page (`dev.to/<username>/<slug>`)

- **Left floating action bar** (sticky sidebar):
  - `button "reaction-drawer-trigger"` — open reaction drawer
  - `button "Jump to Comments"` — scroll to comments
  - `button "Add to reading list"` — bookmark/save
  - `button "Boost"` — boost the post
  - `button "Share post options"` — share menu

- **Article header**:
  - Author name link: `link "<Author Name>"` (appears twice — avatar and text)
  - **Reaction buttons** (5 types):
    - `button "Like"` — heart reaction
    - `button "Unicorn"` — unicorn reaction
    - `button "Exploding Head"` — mind blown
    - `button "Raised Hands"` — celebrate
    - `button "Fire"` — fire reaction
  - **Tag links**: `link "# <tag>"` (e.g., `link "# ai"`, `link "# agents"`)

- **Article content**: Standard HTML with links, code blocks, images

- **Comment section**:
  - `button "Sort comments"` — sort options
  - `button "Subscribe"` — subscribe to comment thread
  - **Main comment input**: `textbox "Add a comment to the discussion"` — top-level comment box (Markdown supported)
  - **Each comment** has:
    - Author profile image link: `link "<username> profile image"`
    - `button "<Name> profile details"` — view author details
    - Timestamp link: `link "Mar 4"` etc.
    - `button "Toggle dropdown menu"` — comment options (edit/delete/report)
    - `button "like"` — like the comment
    - `button "Comment button Reply"` — open reply form

### Reply Form (expanded under a comment)

Clicking `button "Comment button Reply"` expands a reply form:

- `textbox "Reply to a comment..."` — the reply input (Markdown supported)
- **Markdown toolbar**:
  - `button "Bold"`, `button "Italic"`, `button "Link"`
  - `button "Ordered list"`, `button "Unordered list"`
  - `button "Heading"`, `button "Quote"`
  - `button "Code"`, `button "Code block"`
  - `button "Embed"`, `button "Upload image"`
  - `button "More options"`
- `button "Submit"` (disabled until text entered)
- `button "Preview"` (disabled until text entered)
- `button "Dismiss"` — close the reply form

### Create Post Page (`dev.to/new`)

- **Editor tabs**: `button "Edit"` / `button "Preview"`
- `button "Close the editor"` — exit without saving
- **Cover image**: `button "Upload Cover Image"` + `button "🍌 Generate Image"` (AI image generation)
- `button "Cover Video Link"` — add cover video
- `textbox "Post Title"` — article title
- `textbox "Add up to 4 tags"` — tag input (combobox for tag suggestions)
- **Markdown toolbar** (same as reply form):
  - Bold, Italic, Link, Ordered list, Unordered list, Heading, Quote, Code, Code block, Embed, Upload image
  - `link "Upload Agent Session"` — upload agent session
  - `button "More options"` — additional formatting
- `textbox "Post Content"` — the main article body (Markdown)
- **Action buttons**:
  - `button "Publish"` — publish immediately
  - `button "Save draft"` — save as draft
  - `button "Advanced Post options"` — series, canonical URL, etc.
  - `button "Toggle AI Editor Helper"` — AI writing assistant

### Search Results Page (`dev.to/search?q=<query>`)

- `textbox "Search term"` — editable search box
- **Sort options**: `link "Most Relevant"` / `link "Newest"` / `link "Oldest"`
- **Filter tabs**: `link "Posts"` / `link "People"` / `link "Organizations"` / `link "Tags"` / `link "Comments"` / `link "My posts only"`
- **Result cards**: Each has:
  - Article title link (appears twice — card and title)
  - Author profile link + `button "profile details"`
  - Date link
  - Tag links (`link "# <tag>"`)
  - Reaction count link: `link "N reactions"`
  - Comment link: `link "Add a comment to post - <title>"`
  - Save button: `button "Save post <title> to reading list"`

### User Profile Page (`dev.to/<username>`)

- User avatar, name, bio
- Follow button
- Stats (posts, comments, followers)
- Article list

---

## Common Operations

### Browse Home Feed

```bash
agent-browser --auto-connect open https://dev.to
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect scroll down 800     # load more articles
agent-browser --auto-connect snapshot -i          # re-snapshot
```

### Search for Posts

```bash
# Direct URL:
agent-browser --auto-connect open "https://dev.to/search?q=vector+database+AI"
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i

# Or use the search box:
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect fill @eSearchBox "AI agents"   # textbox "Search..."
agent-browser --auto-connect press Enter
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i
```

### Read an Article

```bash
# Click article title from feed or search results:
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eArticleLink   # link "<Article Title>"
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i

# Or navigate directly:
agent-browser --auto-connect open "https://dev.to/<username>/<slug>"
```

### React to an Article

Dev.to has 5 reaction types (can use multiple):
```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eLike          # button "Like"
agent-browser --auto-connect click @eUnicorn       # button "Unicorn"
agent-browser --auto-connect click @eExploding     # button "Exploding Head"
agent-browser --auto-connect click @eRaisedHands   # button "Raised Hands"
agent-browser --auto-connect click @eFire          # button "Fire"
```

### Comment on an Article

```bash
agent-browser --auto-connect snapshot -i
# Find the main comment textbox:
agent-browser --auto-connect fill @eCommentBox "Your comment here (supports **Markdown**)"
# textbox "Add a comment to the discussion"

# Submit: need to look for Submit button after typing
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eSubmit   # button "Submit"
```

### Reply to a Comment

```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eReply      # button "Comment button Reply"
agent-browser --auto-connect snapshot -i        # re-snapshot for reply form

agent-browser --auto-connect fill @eReplyBox "Your reply (supports **Markdown**)"
# textbox "Reply to a comment..."
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eSubmit     # button "Submit"
```

### Create a New Post

```bash
agent-browser --auto-connect open https://dev.to/new
agent-browser --auto-connect wait 2000
agent-browser --auto-connect snapshot -i

# Fill title
agent-browser --auto-connect fill @eTitle "Your Article Title"
# textbox "Post Title"

# Add tags
agent-browser --auto-connect fill @eTags "ai, vectordatabase, rag, tutorial"
# textbox "Add up to 4 tags"

# Fill content (Markdown)
agent-browser --auto-connect fill @eContent "## Introduction\n\nYour article content here..."
# textbox "Post Content"

# Publish or save draft
agent-browser --auto-connect click @ePublish    # button "Publish"
# or
agent-browser --auto-connect click @eSaveDraft  # button "Save draft"
```

**Important**: Always confirm with the user before actually publishing a post.

### Save to Reading List

```bash
# From article detail page:
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eSave   # button "Add to reading list"

# From search results:
agent-browser --auto-connect click @eSavePost   # button "Save post <title> to reading list"
```

---

## Known Quirks & Workarounds

### Dev.to is fast and simple

Unlike X and LinkedIn, Dev.to loads quickly and `wait --load networkidle` usually works. The DOM is straightforward server-rendered HTML without heavy SPA frameworks.

### Article cards in feed are simple links

Unlike other platforms where posts have inline action buttons (like, comment, share), Dev.to feed articles are mostly just title links with comment counts. You need to click into the article to interact (react, comment, etc.).

### Markdown everywhere

Both the article editor and comment forms accept Markdown. Use `fill` with Markdown syntax:
```bash
agent-browser --auto-connect fill @eContent "## My Heading\n\n- bullet 1\n- bullet 2\n\n```python\nprint('hello')\n```"
```

### Comment form uses standard textarea

Unlike LinkedIn/X which use contenteditable divs, Dev.to uses standard `<textarea>` elements for comments and post content. `fill` works reliably.

### Multiple "Toggle dropdown menu" buttons

Each comment and some UI sections have their own dropdown menu button. Use the ref from `snapshot -i` to identify the correct one.

### Search is powered by Algolia

Dev.to search uses Algolia and is fast. The search URL format is: `dev.to/search?q=<query>`. Results can be filtered by Posts, People, Organizations, Tags, Comments.

### Tags limited to 4 per post

The editor allows up to 4 tags per post. The tag input has autocomplete/suggestions via a combobox.

### "What's on your mind?" textbox

The `textbox "What's on your mind?"` on the home feed is just a link to the Create Post page — it doesn't open an inline editor.

### Multiple reaction types

Unlike most platforms with a single "like" button, Dev.to has 5 reaction types (Like, Unicorn, Exploding Head, Raised Hands, Fire). Users can give multiple reactions to the same post. Each reaction has its own button on the article detail page.

### AI Editor Helper

The Create Post page has a `button "Toggle AI Editor Helper"` for AI-powered writing assistance. This is a built-in Dev.to feature.

---

## Useful URLs

- Home feed: `https://dev.to/`
- Create post: `https://dev.to/new`
- Search: `https://dev.to/search?q=<query>`
- User profile: `https://dev.to/<username>`
- Article: `https://dev.to/<username>/<slug>`
- Tag page: `https://dev.to/t/<tag>`
- Reading list: `https://dev.to/readinglist`
- Notifications: `https://dev.to/notifications`
- Dashboard: `https://dev.to/dashboard`
- Settings: `https://dev.to/settings`
- Organization page: `https://dev.to/<org-name>`

## AI-Related Tags

- `#ai` / `#artificialintelligence`
- `#machinelearning` / `#ml`
- `#llm`
- `#genai` / `#generativeai`
- `#vectordatabase`
- `#rag`
- `#agents` / `#aiagents`
- `#nlp`
- `#deeplearning`
- `#openai` / `#chatgpt`
- `#python`
- `#tutorial`
- `#beginners`
