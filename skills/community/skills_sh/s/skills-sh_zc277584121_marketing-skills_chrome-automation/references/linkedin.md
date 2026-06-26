# LinkedIn — Platform Reference

Background knowledge for automating LinkedIn tasks via agent-browser.

---

## Page Structure

### Home Feed (`linkedin.com/feed/`)

LinkedIn is an Ember.js single-page application. Key interactive elements:

- **Top navigation bar**:
  - `link "LinkedIn"` — logo/home link
  - `button "Click to start a search"` — opens search combobox
  - `link "Home"`, `link "My Network"`, `link "Jobs"`, `link "Messaging"`, `link "Notifications"` — main nav
  - `button "<Your Name> Me"` — profile/account menu (button text includes the logged-in user's name)
  - `button "For Business"` — business tools

- **Left sidebar** (profile card):
  - Profile photo, background photo links
  - Profile name + headline link
  - Company link
  - `link "Profile viewers N"`, `link "Post impressions N"` — analytics
  - `link "Saved items"`, `link "Groups"`, `link "Newsletters"`, `link "Events"`

- **Compose area** (top of feed):
  - `button "Start a post"` — opens compose modal
  - `button "Add a video"`, `button "Add a photo"` — quick media
  - `link "Write an article on LinkedIn"` — long-form article editor

- **Post cards**: Each post has:
  - Social proof line (e.g., "Xinyi Xia" liked, "Richard Shoemake" commented) — shows who in your network interacted
  - Author graphic link: `link "View <Author>'s graphic link"` — profile photo
  - `button "Open control menu for post by <Author>"` — post settings (⋯ menu)
  - `button "Dismiss post by <Author>"` — hide post (×)
  - `button "Follow <Author>"` — follow button (for non-connections)
  - Post content text with hashtag links (`link "hashtag <tag>"`)
  - External links (`link "https://lnkd.in/..."`)
  - `button "see more, visually reveals content which is already detected by screen readers"` — expand truncated text
  - Image/media buttons: `button "Activate to view larger image, ..."`
  - **Reaction count**: `button "N reactions"` or `button "<Name> and N others"`
  - **Comment count**: `button "N comments on <Author>'s post"`
  - **Repost count**: `button "N reposts of <Author>'s post"`
  - **Action buttons** (4 buttons per post):
    - `button "React Like"` — default like reaction
    - `button "Open reactions menu"` — long-press for Celebrate, Support, Love, Insightful, Funny
    - `button "Comment"` — toggle comment section
    - `button "Repost"` — repost/share
    - `button "Send in a private message"` — share via DM

- **Sponsored posts**: Marked with `link "View Sponsored Content"` or `link "Learn more. View Sponsored Content"`

- **Right sidebar**:
  - "Add to your feed" recommendations with `button "Follow"` buttons
  - LinkedIn News section

- **Messaging overlay** (bottom-right):
  - `button "Compose message"` — new DM
  - `textbox "Type to search for connections and conversations."` — search conversations
  - `tab "Focused"` / `tab "Other"` — message tabs
  - Conversation list with checkboxes and option buttons

### Comment Section (expanded in feed)

Clicking `button "Comment"` on a post expands the comment section inline:

- **Comment input**: `textbox "Text editor for creating content"` — the comment box
  - `button "Open Emoji Keyboard"` — add emoji
  - `button "Add a photo"` — attach image to comment
- **Each comment** has:
  - Author profile photo link: `link "View <Name>'s graphic link"`
  - `button "Open options for <Name>'s comment"` — comment menu (edit/delete)
  - `button "see more..."` — expand long comment text
  - `button "React Like to <Name>'s comment"` — like the comment
  - `button "Open reactions menu"` — other reactions on comment
  - `button "N Reactions on <Name>'s comment"` — reaction count
  - `button "Reply to <Name>'s comment"` — open reply thread
  - `button "Load previous replies on <Name>'s comment"` — expand reply thread
- **Load more**: `button "Load more comments"` — paginate comments

### Compose Modal (Start a post)

Clicking `button "Start a post"` opens a modal overlay:

- `button "Dismiss"` — close the modal
- `button "<Name> <Name> Post to Anyone"` — visibility selector (Anyone, Connections only, etc.)
- `textbox "Text editor for creating content"` — the post text input
- `button "Open Emoji Keyboard"` — emoji picker
- `button "Add media"` — attach images/documents
- `button "Create an event"` — create event post
- `button "Celebrate an occasion"` — celebration post
- `button "More"` — additional post types
- `button "Schedule post"` — schedule for later
- `button "Post"` (disabled until text entered) — publish

### User Profile Page (`linkedin.com/in/<username>`)

Clicking a user's graphic link from feed goes to their profile:

- Profile photo, background image
- `button "Notify me about all of <Name>'s posts"` — bell notification
- `link "<Name>"` — profile name
- `link "Contact info"` — contact details
- `link "N connections"` — connections list
- Mutual connections link
- `button "Message <Name>"` — send DM
- `button "More actions"` — additional options
- `button "Following <Name>"` — follow status
- **Content tabs**: `button "Posts"`, `button "Comments"`, `button "Images"`
- Featured links section
- Experience, Education, Skills sections

### Search Results Page

URL format: `linkedin.com/search/results/all?keywords=<query>&origin=GLOBAL_SEARCH_HEADER`

- **Search box**: `textbox "Search"` — editable, pre-filled with query
- **Category filter buttons**: Jobs, Posts, People, Groups, Courses (quick switch)
- **Category filter radio/checkboxes** (sidebar): Jobs, Posts, People, Groups, Courses, Companies, Schools, Events, Products, Services
- **Time filters**: "From my network", "Past 24 hours", "Past week"
- **Connection filters**: "1st", "2nd", "3rd+"
- **Results sections** (mixed):
  - Jobs with save buttons
  - Posts with hashtags and reaction buttons
  - People with profile summaries and Follow/Connect buttons
  - Groups with Join buttons
  - Courses with Save buttons
- `button "Show all <type> results"` — see all results of a specific type
- `button "Load more"` — paginate results

#### Posts-only search: `linkedin.com/search/results/content/?keywords=<query>`

Filter to posts by clicking the "Posts" button or navigating directly.

---

## Common Operations

### Browse Home Feed

```bash
agent-browser --auto-connect open https://www.linkedin.com/feed/
agent-browser --auto-connect wait 3000        # LinkedIn loads slowly
agent-browser --auto-connect snapshot -i       # see posts and actions
agent-browser --auto-connect scroll down 1000  # load more posts
agent-browser --auto-connect snapshot -i       # re-snapshot after scroll
```

### Search for Posts

```bash
# Direct URL (posts only):
agent-browser --auto-connect open "https://www.linkedin.com/search/results/content/?keywords=vector%20database%20AI"
agent-browser --auto-connect wait 3000
agent-browser --auto-connect snapshot -i

# Or use the search box:
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eSearchButton   # button "Click to start a search"
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect fill @eSearchBox "AI agents"   # combobox "Search"
agent-browser --auto-connect press Enter
agent-browser --auto-connect wait 3000
agent-browser --auto-connect snapshot -i
```

### React to a Post (Like)

```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eLike   # button "React Like"
```

For other reactions (Celebrate, Love, Insightful, Funny):
```bash
# Long-press / hover the reactions menu
agent-browser --auto-connect click @eReactMenu   # button "Open reactions menu"
agent-browser --auto-connect snapshot -i          # see reaction options
agent-browser --auto-connect click @eReaction     # select specific reaction
```

### Comment on a Post

1. Click the Comment button to expand the comment section:
```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eComment   # button "Comment"
agent-browser --auto-connect snapshot -i       # re-snapshot to see comment input
```

2. Find and fill the comment text box:
```bash
# The comment input is: textbox "Text editor for creating content"
agent-browser --auto-connect fill @eCommentBox "Great insights! ..."
agent-browser --auto-connect press Enter       # Submit comment (Enter key submits on LinkedIn)
```

**Note**: On LinkedIn, pressing Enter in the comment box submits the comment. Use Shift+Enter for new lines.

### Reply to a Comment

```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eReply   # button "Reply to <Name>'s comment"
agent-browser --auto-connect snapshot -i     # re-snapshot for reply input
agent-browser --auto-connect fill @eReplyBox "Your reply..."
agent-browser --auto-connect press Enter     # Submit reply
```

### Create a New Post

```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eStartPost   # button "Start a post"
agent-browser --auto-connect wait 1000
agent-browser --auto-connect snapshot -i

# Fill the post text
agent-browser --auto-connect fill @eTextbox "Your post content here #AI #VectorDatabase"

# Optionally change visibility
agent-browser --auto-connect click @eVisibility   # button "Post to Anyone"

# Submit
agent-browser --auto-connect snapshot -i   # re-snapshot for enabled Post button
agent-browser --auto-connect click @ePost  # button "Post"
```

**Important**: Always confirm with the user before actually submitting a post.

### Repost

```bash
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect click @eRepost   # button "Repost"
agent-browser --auto-connect snapshot -i      # see repost options
# Options: "Repost instantly" or "Repost with your thoughts"
agent-browser --auto-connect click @eOption   # select repost type
```

### Send a Direct Message

```bash
# From feed messaging overlay:
agent-browser --auto-connect click @eCompose   # button "Compose message"
agent-browser --auto-connect snapshot -i
# Search for recipient, fill message, send

# From a profile page:
agent-browser --auto-connect click @eMessage   # button "Message <Name>"
agent-browser --auto-connect snapshot -i
agent-browser --auto-connect fill @eMsgBox "Your message..."
agent-browser --auto-connect press Enter
```

### View a Post Detail Page

LinkedIn posts don't have a simple permalink in the feed snapshot. To navigate to a post's detail page:

```bash
# Use the post's activity URL pattern:
agent-browser --auto-connect open "https://www.linkedin.com/feed/update/urn:li:activity:<id>/"
agent-browser --auto-connect wait 3000
agent-browser --auto-connect snapshot -i
```

In the feed, you can also click the timestamp or "N comments" button to navigate to the post detail overlay/page.

---

## Known Quirks & Workarounds

### Avoid `wait --load networkidle`

LinkedIn has continuous background network activity (messaging, notifications, tracking). The `networkidle` state is rarely reached.

**Workaround**: Use `wait 3000` after navigation. LinkedIn is generally slower to load than other platforms.

### "View <Name>'s graphic link" is for profile photo links

In the feed, each post author's profile photo appears as `link "View <Name>'s graphic link"`. Clicking this navigates to the author's profile, NOT the post detail. This is similar to X where clicking the username goes to the profile.

### Comment box and post compose box have the same label

Both use `textbox "Text editor for creating content"`. When multiple are visible (e.g., compose modal open while a comment box is expanded), use the ref from the most recent `snapshot -i` carefully.

**Workaround**: Close the compose modal before commenting, or vice versa. The correct textbox is always the one in the current context (modal vs feed).

### Multiple "React Like" / "Comment" buttons on the page

Each visible post has its own set of action buttons. They appear as `[nth=1]`, `[nth=2]`, etc. Always identify the correct post first (by author name or context), then use the corresponding action button ref.

### Reactions menu requires hover/click

The reactions menu (`button "Open reactions menu"`) opens a popup with reaction options. After clicking, re-snapshot to see the available reactions, then click the desired one.

### "see more" button for truncated content

Long posts are truncated with `button "see more, visually reveals content which is already detected by screen readers"`. Click this to expand the full text.

### Messaging overlay may block content

The messaging overlay at the bottom-right can obscure page content. If elements are blocked:
```bash
# Minimize the messaging overlay
agent-browser --auto-connect click @eMinimize   # button "You are on the messaging overlay. Press enter to minimize it."
```

### Post content contains external links as `lnkd.in` shortlinks

LinkedIn shortens all external URLs to `lnkd.in` format. The actual URL is behind the redirect.

### Sponsored posts mixed in feed

Sponsored/promoted posts appear in the feed with `link "View Sponsored Content"` labels. They have the same action buttons but may behave differently (e.g., clicking leads to external sites).

### Enter key submits comments

Unlike most platforms, pressing Enter in LinkedIn's comment box submits the comment immediately. Use Shift+Enter for line breaks within a comment.

### Search requires specific filter for posts

The default search shows a mixed page with Jobs, Posts, People, etc. To see only posts:
- Click the "Posts" filter button after searching
- Or navigate directly to: `linkedin.com/search/results/content/?keywords=<query>`

---

## Useful URLs

- Home feed: `https://www.linkedin.com/feed/`
- My network: `https://www.linkedin.com/mynetwork/`
- Jobs: `https://www.linkedin.com/jobs/`
- Messaging: `https://www.linkedin.com/messaging/`
- Notifications: `https://www.linkedin.com/notifications/`
- Profile: `https://www.linkedin.com/in/<username>/`
- Company page: `https://www.linkedin.com/company/<company>/`
- Search (all): `https://www.linkedin.com/search/results/all/?keywords=<query>`
- Search (posts): `https://www.linkedin.com/search/results/content/?keywords=<query>`
- Search (people): `https://www.linkedin.com/search/results/people/?keywords=<query>`
- Search (companies): `https://www.linkedin.com/search/results/companies/?keywords=<query>`
- Post detail: `https://www.linkedin.com/feed/update/urn:li:activity:<id>/`
- Article: `https://www.linkedin.com/pulse/<slug>/`
- Groups: `https://www.linkedin.com/groups/<group_id>/`

## AI-Related Hashtags

- `#AI` / `#ArtificialIntelligence`
- `#MachineLearning` / `#ML`
- `#LLM` / `#LargeLanguageModels`
- `#GenerativeAI` / `#GenAI`
- `#VectorDatabase` / `#VectorSearch`
- `#RAG` / `#RetrievalAugmentedGeneration`
- `#AIAgents` / `#AgenticAI`
- `#DataEngineering`
- `#NLP` / `#NaturalLanguageProcessing`
- `#DeepLearning`
- `#Milvus` / `#Zilliz`

## AI-Related Companies & Pages

- `Zilliz` — Milvus / Zilliz Cloud
- `OpenAI` — GPT / ChatGPT
- `Anthropic` — Claude
- `Google DeepMind` — Gemini
- `Hugging Face` — Open-source ML
- `Meta AI` — Llama
- `Mistral AI` — Open-source LLMs
- `Cohere` — Enterprise AI / Rerank
- `Pinecone` — Vector database
- `Weaviate` — Vector database
- `Qdrant` — Vector database
