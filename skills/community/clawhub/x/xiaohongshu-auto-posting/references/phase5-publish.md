# Phase 5 Reference — Publish Execution

## TOC

- §0 Windows Execution Rules (read first)
- §1 Content Verification Gate (mandatory pre-publish check)
- §2 Image Generation (Text-to-Image)
- §3 External Image Upload Flow
- §4 Creator Center Form Fill & Publish
- §5 Correct Way to Write Title (native setter)
- §6 Post-Publish note_id Capture
- §7 Publish Record Write

---

> **Session convention**: All bash commands use `$SESSION` and all Python subprocess calls use the variable `SESSION` — both refer to the dynamic session name generated in Phase 0.5 (e.g., `xhs-20260611-1430`). Set `SESSION = "<generated name>"` at the top of any Python script.

## §0 Operational Rules

Three rules that apply to **every** browser-act automation session. Violating any one causes silent failures or long hangs regardless of platform.

### Rule 1 — Redirect state output to a file before grepping

Piping `browser-act state` directly into `grep` is unreliable when the page contains multi-byte characters: the shell tool may background the command, making the result unavailable synchronously. Always redirect first:

```bash
# WRONG — may background silently, result never arrives
browser-act --session $SESSION state | grep "Publish"

# CORRECT — redirect then grep the file
browser-act --session $SESSION state > /tmp/s.txt 2>&1
grep "Publish" /tmp/s.txt
```

This pattern also makes it easy to re-grep the same snapshot without re-running state.

### Rule 2 — Encode all non-ASCII content before passing to eval --stdin

`browser-act eval --stdin` reads JS source as a byte stream. When the JS contains non-ASCII literals (Chinese, emoji, etc.), encoding mismatches between the shell, Python, and browser-act can cause `surrogates not allowed` or silent truncation. The safe pattern: escape every non-ASCII character to `\uXXXX` before sending:

```python
def to_ascii_js(source: str) -> str:
    return ''.join(
        r'\u{:04x}'.format(ord(c)) if ord(c) > 127 else c
        for c in source
    )

js_safe = to_ascii_js(open('tmp/script.js', encoding='utf-8').read())
result = subprocess.run(
    ['browser-act', '--session', SESSION, 'eval', '--stdin'],
    input=js_safe.encode('ascii'),
    capture_output=True,
    timeout=15,
)
```

For body/title text injected via `json.dumps`, the JSON encoding already escapes non-ASCII if `ensure_ascii=True` (the default), so no extra step is needed there.

### Rule 3 — Never use eval to trigger navigation

`eval` waits for a return value. When a click inside the eval callback causes page navigation (e.g., clicking the Publish button), the eval context is destroyed mid-execution and the call either hangs until timeout (~30 s) or returns empty. Always use `browser-act click <index>` for any action that may redirect the page, then verify the outcome by re-reading the URL:

```bash
browser-act --session $SESSION click <publish_index>
sleep 3
browser-act --session $SESSION state > /tmp/s.txt 2>&1
head -3 /tmp/s.txt   # URL should contain published=true
```

---

## §1 Content Verification Gate

Run the following checks before publishing — **if any fails, block publish and prompt user to fix**:

| Check | Pass condition |
|-------|----------------|
| Title length | `len(title) <= 20` (character count, Chinese counts as 1) |
| Title no external link | Title does not contain `http` / `www` |
| Body non-empty | `len(body.strip()) > 0` |
| Body no external link | Body does not contain `http://` / `https://` / `www.` |
| Body no contact info | Body does not contain WeChat ID / phone format (`1[3-9]\d{9}`) / QQ |
| Topic tags >= 1 | At least 1 `#tag` at end of body |
| Image ready | `file_id` is not empty, or text-to-image has been generated |

Only proceed to §4 after all checks pass.

---

## §2 Image Generation (Text-to-Image, recommended)

XHS Creator Center has a built-in "文字配图" feature — no external AI image needed, just input text to generate.

```bash
# Navigate to publish page
browser-act --session $SESSION navigate "https://creator.xiaohongshu.com/publish/publish?source=official"
browser-act --session $SESSION wait stable

# Switch to "upload image-text" tab
browser-act --session $SESSION state
# Find "上传图文" tab index and click
browser-act --session $SESSION click <upload_image_tab_index>
browser-act --session $SESSION wait stable

# Click "文字配图" button
browser-act --session $SESSION state
# Find "文字配图" button index
browser-act --session $SESSION click <text2img_btn_index>
browser-act --session $SESSION wait stable
```

In the text-to-image dialog, input image title (≤ 12 characters):

```bash
browser-act --session $SESSION state
# Find input box index
browser-act --session $SESSION input <text_input_index> "<image title>"
# Click generate
browser-act --session $SESSION click <generate_btn_index>
browser-act --session $SESSION wait stable --timeout 30000
```

After generation, select a style and click "Use":

```bash
browser-act --session $SESSION state
browser-act --session $SESSION click <select_image_index>
# Confirm use
browser-act --session $SESSION click <use_btn_index>
browser-act --session $SESSION wait stable
```

After the image is used, it appears in the editor — the XHS frontend already holds the `file_id`, no need to record manually.

**Text-to-Image API endpoint** (for debugging reference only, do not call directly in Skill):
```
POST https://creator.xiaohongshu.com/api/galaxy/v2/creator/post/inspiration/text2imgv3
```

---

## §3 External Image Upload Flow (optional, for local images)

If uploading a locally generated image (PNG/JPG), use two-step upload:

### Step 1 — Get Upload Credentials

```bash
browser-act --session $SESSION navigate "https://creator.xiaohongshu.com/publish/publish?source=official"
browser-act --session $SESSION wait stable
# Switch to image-text tab
browser-act --session $SESSION click <upload_image_tab_index>
browser-act --session $SESSION wait stable
```

Inject file into file input via JS to trigger the frontend to automatically get upload credentials:

```javascript
(async () => {
  // Note: base64Data must be provided externally
  const base64Data = '<base64_string>';
  const byteString = atob(base64Data);
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i);
  const blob = new Blob([ab], {type: 'image/png'});
  const file = new File([blob], 'cover.png', {type: 'image/png'});
  const input = document.querySelector('input[type=file].upload-input');
  const dt = new DataTransfer();
  dt.items.add(file);
  input.files = dt.files;
  input.dispatchEvent(new Event('change', {bubbles: true}));
  return 'injected';
})()
```

```bash
browser-act --session $SESSION wait stable
browser-act --session $SESSION network requests --filter "upload/creator/permit" --type xhr,fetch
browser-act --session $SESSION network request <permit_request_id>
```

Extract `file_id` (format: `spectrum/<hash>`) and `token` from the response.

### Step 2 — PUT Upload File

The frontend will automatically complete the PUT upload — no manual curl needed. The `file_id` is already held by the frontend; proceed directly to §4 to fill the publish form.

---

## §4 Creator Center Form Fill & Publish

### 4.1 Navigate to Publish Page (if not already there)

```bash
browser-act --session $SESSION navigate "https://creator.xiaohongshu.com/publish/publish?source=official"
browser-act --session $SESSION wait stable
browser-act --session $SESSION click <upload_image_tab_index>
browser-act --session $SESSION wait stable
```

### 4.2 Fill Body Text

The XHS Creator Center body area is a Tiptap rich text editor. Use a Python script to inject via `execCommand` (see §0 Rule 2 for encoding):

```python
# tmp/inject_body.py
import subprocess, json

# IMPORTANT: append topic hashtags directly in body_text (see §4.3)
body_text = """<body content>
#大模型 #AI工具 #人工智能"""  # <-- hashtags go here

escaped = json.dumps(body_text)
js_code = f"""(function() {{
  const editors = document.querySelectorAll('[contenteditable=true]');
  let editor = null;
  for (const e of editors) {{
    if (e.closest('.tiptap-container, .ql-editor, .editor')) {{ editor = e; break; }}
  }}
  if (!editor) editor = editors[0];
  if (!editor) return 'no editor found';
  editor.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('delete', false, null);
  document.execCommand('insertText', false, {escaped});
  editor.dispatchEvent(new InputEvent('input', {{bubbles: true}}));
  return 'injected: ' + editor.textContent.length + ' chars';
}})()"""

result = subprocess.run(
    ['browser-act', '--session', SESSION, 'eval', '--stdin'],
    input=js_code.encode('utf-8'), capture_output=True
)
print(result.stdout.decode('utf-8', errors='replace'))
```

```bash
python tmp/inject_body.py
```

Verify the returned char count matches expected body length.

### 4.3 Add Topic Tags

**⚠️ Known trap — chip clicking does NOT work after execCommand injection.**

When body is injected via `execCommand`, Tiptap's internal ProseMirror cursor state is invalid. Clicking topic chips silently fails to insert `tiptap-topic` nodes regardless of manual focus/selection. Do not attempt the chip-clicking path.

**Correct method: embed hashtags directly in body_text before injection**

Add the topic tags as plain `#tag` text at the end of `body_text` in the `inject_body.py` script:

```python
body_text = f"""{main_body}
#{tag1} #{tag2} #{tag3} #{tag4} #{tag5}"""
```

XHS recognizes `#keyword` plain text as topic links on publish. Use 3–5 tags from the style fingerprint. Choose from terms visible in `tag-group` chips on the current page — those are confirmed valid XHS topics.

**How to find valid topic terms**: after body injection, save state to a file and inspect the `tag-group` section (see §0 Rule 1):

```bash
browser-act --session $SESSION state > /tmp/s.txt 2>&1
grep -A 1 "span class=tag" /tmp/s.txt
```

Pick 3–5 of the chips shown and include them verbatim (without `#`) as hashtags in `body_text`.

### 4.4 Fill Title

Title input requires native setter to bypass React/Vue onChange hijacking. Use a Python script (see §0 Rule 2):

```python
# tmp/inject_title.js  — write this file, all non-ASCII as \uXXXX
(function() {
  var inputs = document.querySelectorAll('input[type=text]');
  var titleInput = null;
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].placeholder && inputs[i].placeholder.indexOf('标题') >= 0) {
      titleInput = inputs[i]; break;
    }
  }
  if (!titleInput && inputs.length > 0) titleInput = inputs[0];
  if (!titleInput) return 42;
  var title = "你的标题";   // <-- replace with actual title as \uXXXX
  var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(titleInput, title);
  titleInput.dispatchEvent(new Event('input', { bubbles: true }));
  titleInput.dispatchEvent(new Event('change', { bubbles: true }));
  return titleInput.value.length;
})()
```

```python
# Run it:
def to_ascii_js(s):
    return ''.join(r'\u{:04x}'.format(ord(c)) if ord(c) > 127 else c for c in s)

js = to_ascii_js(open('tmp/inject_title.js', encoding='utf-8').read())
result = subprocess.run(
    ['browser-act', '--session', SESSION, 'eval', '--stdin'],
    input=js.encode('ascii'), capture_output=True, timeout=15
)
# Should print the character count of the title
print(result.stdout.decode('utf-8', errors='replace'))
```

After filling, take a screenshot to confirm the title appears:

```bash
browser-act --session $SESSION screenshot "workspaces/xhs-posting/<date>/drafts/pre_publish.png"
```

### 4.5 Final Confirm & Publish

**Critical: always re-fetch state immediately before clicking publish.** Button indices shift as the page scrolls and panels open — never reuse an index from an earlier state call.

```bash
# Re-fetch state RIGHT BEFORE clicking
browser-act --session $SESSION state > /tmp/s.txt 2>&1
grep -n "Shadow\|button type=button\|发布\|暂存" /tmp/s.txt
# The 发布 button is ALWAYS the last button inside Shadow Content
# 暂存离开 comes first, 发布 comes second

browser-act --session $SESSION screenshot "workspaces/xhs-posting/<date>/drafts/pre_publish.png"
```

Show the screenshot to the user for Gate confirmation, then:

```bash
# Use browser-act click — NEVER use eval to click publish (see §0 Rule 3)
browser-act --session $SESSION click <publish_btn_index>
sleep 3
browser-act --session $SESSION state > /tmp/s.txt 2>&1
head -3 /tmp/s.txt   # URL must contain published=true
```

If URL does NOT show `published=true` after 3 seconds:
1. Check note manager (`https://creator.xiaohongshu.com/new/note-manager?type=normal`) for the note
2. If not there, re-navigate to publish page and repeat from §4.1

---

## §5 Correct Way to Write Title (native setter)

XHS title input is managed by React/Vue — directly setting `.value` does not trigger framework updates, causing the title to be empty or silently truncated on publish.

**Must use native setter**:

```javascript
const inp = document.querySelector('input[placeholder*="标题"], .title-input input');
const nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
nativeSetter.call(inp, 'title content');  // max 20 characters
inp.dispatchEvent(new Event('input', {bubbles: true}));
```

When exceeding 20 characters, XHS will not error but will silently truncate or reject publish. Must verify `len(title) <= 20` before writing.

---

## §6 Post-Publish note_id Capture

After successful publish, page redirects to:

```
https://creator.xiaohongshu.com/publish/publish?source=official&published=true
```

Extract `note_id` from the URL, page title, or success toast:

```bash
browser-act --session $SESSION eval "window.location.href"
# Check if contains published=true
browser-act --session $SESSION network requests --filter "sns/v2/note" --type xhr,fetch
browser-act --session $SESSION network request <publish_request_id>
# Extract note_id from response: response_body.data.note_id
```

XHS note public URL format: `https://www.xiaohongshu.com/explore/<note_id>`

If note_id cannot be auto-captured (note under review), record `status: pending_review` and manually fill in after review passes.

---

## §7 Publish Record Write

After successful publish, append record to `workspaces/xhs-posting/tracking/published.json`:

```json
{
  "note_id": "<captured_note_id>",
  "title": "<published title>",
  "url": "https://www.xiaohongshu.com/explore/<note_id>",
  "published_at": "<YYYY-MM-DD HH:MM>",
  "keyword": "<source keyword>",
  "source_topic_url": "<original post URL referenced in Phase 1>",
  "status": "published",
  "tracking": {
    "likes_24h": null,
    "collects_24h": null,
    "comments_24h": null,
    "views_24h": null,
    "last_checked": null
  }
}
```

Also update `posting.last_posted_at` in `session_state.json` to current time, increment `posting.today_count` by 1.
