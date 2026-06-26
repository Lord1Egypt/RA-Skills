---
name: skool-all-in-one-api
description: Full read AND write access to Skool communities. Use when user asks to manage Skool members (approve, reject, list pending), read or create posts, reply to comments, mention users, or automate community management. The only Skool tool with write capabilities.
metadata: {"openclaw":{"emoji":"🎓","homepage":"https://apify.com/cristiantala/skool-all-in-one-api","requires":{"env":["APIFY_TOKEN"],"bins":["node","mcpc"]},"primaryEnv":"APIFY_TOKEN","install":[{"id":"mcpc","kind":"node","package":"@apify/mcpc","bins":["mcpc"],"label":"Install mcpc CLI (npm)"}]}}
---

# Skool All-in-One API

Full read AND write access to Skool communities via Apify.

## Prerequisites

- `.env` file with `APIFY_TOKEN`
- Node.js 20.6+
- `mcpc` CLI tool

## CRITICAL: Skool Data Model

**Posts and comments are the SAME object in Skool.**
- To read comments: use `posts:getComments` — NOT `comments:list`
- To create a comment: use `posts:createComment` — NOT `comments:create`
- There is NO `comments:` namespace. Everything is `posts:`.

**Content is PLAIN TEXT, not HTML.**
- CORRECT: `Hello world`
- WRONG: `<p>Hello world</p>`

**User mentions:** `[@Display Name](obj://user/{userId})`

## Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Determine action needed
- [ ] Step 2: Login (auth:login) or use existing cookies
- [ ] Step 3: Execute the action
- [ ] Step 4: Present results
```

### Step 1: Determine Action

Select the action based on user needs:

| User Need | Action | Params |
|-----------|--------|--------|
| **Authentication** | | |
| Login to Skool | `auth:login` | email, password, groupSlug |
| **Posts** | | |
| List posts | `posts:list` | page?, sortType? |
| Filter posts (date, unanswered) | `posts:filter` | since?, until?, notAnsweredBy?, maxPosts? |
| Get single post | `posts:get` | postId |
| Create post | `posts:create` | title, content (plain text), labelId? |
| Edit post or comment | `posts:update` | postId, title?, content? |
| Delete post or comment | `posts:delete` | postId |
| Pin/unpin post | `posts:pin` / `posts:unpin` | postId |
| Like/unlike | `posts:vote` | postId, vote ("up" or "") |
| **Comments** | | |
| Get comments (nested tree) | `posts:getComments` | postId |
| Reply to post | `posts:createComment` | content, rootId=postId, parentId=postId |
| Reply to comment (nested) | `posts:createComment` | content, rootId=postId, parentId=commentId |
| **Members** | | |
| List members | `members:list` | page? |
| List pending applications | `members:pending` | (none) |
| Approve member | `members:approve` | memberId (use member.memberId, NOT member.id) |
| Reject member | `members:reject` | memberId |
| Ban member | `members:ban` | memberId |
| **Events** | | |
| List calendar events | `events:list` | (none) |
| List upcoming events | `events:upcoming` | (none) |

### Step 2: Authentication

**Recommended flow (fast):**

1. Run `auth:login` once to get cookies
2. Use cookies in all subsequent calls (~2s each instead of ~10s)
3. Cookies expire every ~3.5 days — re-login when you get auth errors

```bash
# Login and get cookies
export $(grep APIFY_TOKEN .env | xargs)
RESULT=$(curl -s -X POST "https://api.apify.com/v2/acts/cristiantala~skool-all-in-one-api/runs?token=$APIFY_TOKEN&waitForFinish=120" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "auth:login",
    "email": "USER_EMAIL",
    "password": "USER_PASSWORD",
    "groupSlug": "GROUP_SLUG"
  }')

RUN_ID=$(echo $RESULT | jq -r '.data.id')
COOKIES=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN" | jq -r '.[0].cookies')
echo "Cookies saved. Valid for ~3.5 days."
```

### Step 3: Execute Action

**With cookies (fast, ~2s):**

```bash
export $(grep APIFY_TOKEN .env | xargs)
curl -s -X POST "https://api.apify.com/v2/acts/cristiantala~skool-all-in-one-api/runs?token=$APIFY_TOKEN&waitForFinish=120" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "ACTION_NAME",
    "cookies": "COOKIES_FROM_LOGIN",
    "groupSlug": "GROUP_SLUG",
    "params": { PARAMS_HERE }
  }'
```

**With email+password (slower, ~10s, uses Playwright):**

```bash
export $(grep APIFY_TOKEN .env | xargs)
curl -s -X POST "https://api.apify.com/v2/acts/cristiantala~skool-all-in-one-api/runs?token=$APIFY_TOKEN&waitForFinish=120" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "ACTION_NAME",
    "email": "USER_EMAIL",
    "password": "USER_PASSWORD",
    "groupSlug": "GROUP_SLUG",
    "params": { PARAMS_HERE }
  }'
```

**Get results from dataset:**

```bash
RUN_ID=$(echo $RESULT | jq -r '.data.id')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN" | jq .
```

### Step 4: Present Results

Format results based on the action:

- **posts:list** — Show title, author, likes, commentCount, url
- **posts:getComments** — Show nested comment tree with replies
- **members:pending** — Show name, bio, location, application answers, source
- **members:list** — Show name, level, points, bio, social links

## Common Workflows

### Get unanswered posts from last 7 days

To find which posts the user hasn't replied to, you need their Skool user ID.

```
1. auth:login → save cookies
2. members:list → find the user by name/email → get their "id" field (this is the user ID, NOT memberId)
3. posts:filter with params:
   {
     "since": "2026-03-20T00:00:00Z",
     "notAnsweredBy": "USER_ID_FROM_STEP_2",
     "maxPosts": 50
   }
4. Show the filtered posts — these are posts the user has NOT replied to
```

**How to get USER_ID:** Run `members:list` and find the user by firstName/lastName. The `id` field (NOT `memberId`) is what you pass to `notAnsweredBy`.

**Alternative — just get posts with 0 comments:**
```
1. auth:login → save cookies
2. posts:list with params: { "page": 1 }
3. Filter results where commentCount === 0
```

### Approve pending members

```
1. auth:login → save cookies
2. members:pending → get list with application answers
3. For each member to approve: members:approve with params: { "memberId": member.memberId }
IMPORTANT: Use member.memberId (membership ID), NOT member.id (user ID)
```

### Reply to a post with user mention

```
1. auth:login → save cookies
2. posts:createComment with params:
   - content: "Great point [@Name](obj://user/{userId})! I agree with your analysis."
   - rootId: "post-id"
   - parentId: "post-id" (same as rootId for top-level comment)
```

### Reply to a specific comment (nested)

```
1. posts:getComments → find the comment ID
2. posts:createComment with params:
   - content: "Thanks for sharing!"
   - rootId: "original-post-id" (ALWAYS the root post, never a comment)
   - parentId: "comment-id" (the comment you're replying to)
```

## Important Notes

1. **memberId vs id**: For approve/reject/ban, use `memberId` field (membership ID), NOT `id` (user account ID). They are different.
2. **Content format**: Posts and comments use PLAIN TEXT. Never send HTML tags.
3. **Mentions**: Use `[@Name](obj://user/{userId})` format. Get userId from members:list.
4. **Rate limits**: Skool limits writes to ~20-30/min. Reads are ~60/min.
5. **Cookie expiry**: Cookies last ~3.5 days. Re-login when you get 403 errors.
6. **Comment nesting**: rootId is ALWAYS the original post ID. parentId is the post (for top-level) or comment (for nested reply).

## Actor Details

- **Actor**: `cristiantala~skool-all-in-one-api`
- **Actor ID**: `g2VGrINIS7pb8t2bs`
- **Apify Store**: https://apify.com/cristiantala/skool-all-in-one-api
