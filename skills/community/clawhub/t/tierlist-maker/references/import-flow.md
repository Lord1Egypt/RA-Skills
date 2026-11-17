# The Import Flow (final-step wording)

What actually happens at `https://tiervibe.com/t/import`, so your final message
matches reality.

**The single path is a `launcher.html` redirect - never an OS open command, never a file drop.** `SKILL.md` → "Emit + hand off via launcher.html"
is the source of truth: you base64 the JSON into `#data=`, write a `launcher.html` that redirects to it, and the user opens that file. Do NOT ask the user to drag the JSON or paste the URL into chat - the launcher.html already carries the data; the file drop below exists only for the rare oversized board.

## Path A — launcher.html redirect via `#data=` (the only normal path)

The user opens `launcher.html`; the user's default browser lands on
`/t/import#data=<base64>` (standard base64 of the UTF-8 JSON, then `encodeURIComponent` - NOT base64url; see SKILL.md step 2). Then:

- The page reads the hash on mount, base64-decodes it as UTF-8, validates it, and
  navigates straight to `/t/new` with tiers, cards, commentary, and background
  already filled in. No drop zone, no file picker.
- On a validation error it shows the message and stays put. Nothing is sent to
  the server.
- Past 2,000,000 characters of `#data=` it refuses with a "too large" error —
  but your shell's command-line limit will bind long before that. See the table
  in `SKILL.md`.

### The login detour

`/t/import` is auth-protected. If the user isn't logged in, they're bounced to
`/login`, and the pending board rides along in the router's location state.

Either sign-in method — email or Google — returns to the board with the hash
intact, and the import runs. Signing up works too: the pending location is
forwarded through `/signup`.

So there's no need to steer the user toward a particular button. If anything does
go wrong, nothing is lost on your side: have them open `launcher.html` again once they're
logged in and the board loads.

## Path B — file drop (rare fallback - only when #data= exceeds 2,000,000 chars)

Use this only when the #data= URL exceeds the 2,000,000-char ceiling of the import page - there is no shell limit anymore, because the URL lives in `launcher.html`, not a command. Then the
page works as a classic drop zone:

- A centered drop zone: "点击选择或拖入文件" (click to choose or drop a file),
  accepting `.tiervibe.json`.
- Clicking opens a file picker; dragging the file onto the zone also works.
- While processing: a spinner, "正在导入…".
- Valid file → same destination as Path A: `/t/new`, fully populated.
- Invalid file → red error message, page stays put, nothing sent to the server.

## In the editor (both paths)

- Tiers and cards appear pre-filled; commentary is attached to its cards.
- The user's remaining job: **drag cards to sort them** into final positions. For embedded local images (`data:image/`), the images already appear and publish uploads them to the platform CDN. Only for image mode + branch B2 (the agent cannot read local files), the user swaps placeholder text cards using the manifest file (`对照表.md` / `manifest.md`) you saved next to `launcher.html` - they can't see your chat or console from the browser, so that file is their only reference.
- Then click **发布** (Publish) to post, or save as a draft.

## How to phrase the final step (templates)

In the user's language. **Path A — what you'll use almost every time:**

> 榜单已经在浏览器里打开了。
> 1. 如果提示登录,登录完会自动回到榜单
> 2. 层级、卡片、讲解都已经填好了
> 3. 拖动卡片排好最终顺序
> 4. 点「发布」

> Your board is open in the browser.
> 1. If it asks you to log in, it'll come back to the board afterwards
> 2. Tiers, cards, and commentary are already filled in
> 3. Drag the cards into your final order
> 4. Click 发布 (Publish)

**Path B — only if you had to fall back to a file:**

> 榜单太大,URL 放不下,所以存成了文件:`<absolute path>`
> 1. 打开 https://tiervibe.com/t/import
> 2. 点击中间区域选择这个文件(或直接拖进去)
> 3. 如果提示登录,登录完回到这个页面再选一次文件
> 4. 拖动卡片排好顺序,点「发布」

Do not add steps about uploading images or calling APIs — opening the board is
the only handoff.
