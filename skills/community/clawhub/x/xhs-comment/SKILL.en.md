---
name: xhs-comment-scraper
description: Xiaohongshu (Little Red Book) comment scraper. When the user sends a Xiaohongshu profile URL, this skill automatically scrapes comments from all notes on that profile and saves them as local JSON files, optionally generating an HTML analysis report. Trigger: links containing xiaohongshu.com/user/profile or similar profile URLs.
readme: SKILL.en.md
metadata:
  language: en
  tags: [xiaohongshu, scraper, chinese, comments, browser, visualization]
  platform: windows
  requirements:
    bins: []
    npm: []
---

# xhs-comment-scraper — Xiaohongshu Comment Scraper

> ⚠️ **Read Before Use**: This document contains critical hard-won lessons. Read the "Key Learnings" section before running.

---

## Browser Setup

**Always use `profile="openclaw"`, NOT `profile="chrome"`!**

Browser Relay relies on Gateway tokens, which break after any Gateway restart — the extension can't reconnect without manual re-pairing. Use OpenClaw's built-in Chrome instead:

```
browser(action=start, target=host, profile=openclaw)
browser(action=navigate, target=host, profile=openclaw, url=<profile URL>)
```

User scans the QR code with the Xiaohongshu app once in the popup Chrome window. After that, everything is automatic.

---

## Data Format

Each note outputs one JSON file:
`xhs_comments_{blogger}_{note_id}_{timestamp}.json`

```json
{
  "blogger": { "name": "Blogger Name", "profile_url": "https://..." },
  "note": {
    "id": "noteId",
    "title": "Note Title",
    "url": "https://..."
  },
  "comments": [
    {
      "author": "Commenter Name",
      "content": "Full comment text",
      "time": "3 days ago / 2025-10-23",
      "likes": 42
    }
  ],
  "scraped_at": "2026-03-24T15:00:00",
  "total_comments": 100
}
```

Save path: `C:\Users\Downloads\xhs_comments\`

---

## ⚠️ Key Learnings (Tested on 2026-03-24 — Read First!)

### 1. Vue Rendering — DOM Selectors Are Useless

Xiaohongshu uses Vue dynamic rendering. All JS `querySelector` / `getElementById` calls return nothing.

**The ONLY reliable extraction method is `innerText`:**

```javascript
// ✅ CORRECT — get rendered text
browser(action=act, kind=evaluate,
       fn="document.body.innerText")

// ❌ WRONG — all DOM selectors return empty
document.querySelector('.comment-item')  // won't work
```

After getting the text, parse comments by fixed patterns in the text stream — username → content → time → likes are all in order.

### 2. "Expand Replies" Buttons Must Be Clicked Explicitly

XHS comments are collapsed by default. Full nested reply threads only load when expanded.

```javascript
// Click ALL "展开N条回复" (Expand N replies) buttons
var btns = Array.from(document.querySelectorAll('*')).filter(
  e => e.textContent.match(/^展开 \d+ 条回复$/)
);
btns.forEach(b => { try { b.click(); } catch(e) {} });
```

### 3. Note URL Formats

- **Image/text notes**: `/explore/{noteId}` — direct navigation works
- **Video notes**: Different URL format — use JS click instead of direct navigate
- **Pinned notes**: At the top of the note list, `index=0`

### 4. Captchas Are Inevitable

High-frequency access triggers XHS anti-bot captchas. When URL changes to `/website-login/captcha?...`:

- **Do NOT try to auto-solve** — it's futile
- Tell the user to complete the captcha manually in the Chrome window
- After completion, just continue — no page refresh needed

### 5. PowerShell `&&` Is Broken

PowerShell does not support `&&`. It throws `Unexpected token` errors.

**Always use `;` or Python directly:**
```
# ❌ WRONG
python script.py && echo done

# ✅ CORRECT
python script.py; echo done

# BEST: pure Python
python script.py
```

### 6. Python File Encoding

PowerShell redirection and subprocess calls default to GBK, corrupting Chinese filenames.

**Always specify UTF-8 explicitly:**
```python
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
```

Read with error replacement for robustness:
```python
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    data = json.load(f)
```

### 7. matplotlib Doesn't Support Emoji

STSong / SimHei fonts don't include emoji glyphs. `Glyph missing` warnings appear on charts.

**Fix: Use text-only labels in matplotlib charts. Save emoji for HTML reports only.**

---

## Full Workflow

### Step 1 — Initialize Browser

```
browser(action=start, target=host, profile=openclaw)
browser(action=navigate, target=host, profile=openclaw,
        url=https://www.xiaohongshu.com/user/profile/{userId})
```

Tell user: "Please scan the QR code with the Xiaohongshu app in the popup Chrome window."

### Step 2 — Collect Note List

Use JS to extract all note links from the profile page:

```javascript
var noteLinks = document.querySelectorAll(
  'a[href*="/user/profile/{userId}/"]'
);
// Extract noteId from href
noteLinks.forEach(link => {
  var href = link.getAttribute('href');
  // href: /user/profile/59757.../69bf6c43000000002800807a
  var parts = href.split('/');
  var noteId = parts[parts.length - 1].split('?')[0];
});
```

### Step 3 — Scrape Each Note

For each note:

1. **Enter note detail**
   ```javascript
   noteLinks[i].click()
   ```
   Wait 5 seconds: `browser(action=act, kind=wait, timeMs=5000)`

2. **Verify entry**
   Check URL is `/explore/{noteId}` — if still on profile, retry the click.

3. **Expand + Scroll**
   ```javascript
   // Expand all reply threads
   var btns = Array.from(document.querySelectorAll('*')).filter(
     e => e.textContent.match(/^展开 \d+ 条回复$/)
   );
   btns.forEach(b => { try { b.click(); } catch(e) {} });
   window.scrollBy(0, 800);
   ```

4. **Extract Comments** (Core!)
   ```javascript
   var bodyText = document.body.innerText;
   // bodyText format:
   // Username
   // Comment content...
   // 3 days ago
   // 赞 42
   // ---
   // Username2
   // Comment2...
   ```
   Split by `\n`, parse by fixed pattern (username → content → time → likes → separator).

5. **Return to Profile**
   ```javascript
   history.back();
   ```

### Step 4 — Save JSON

```python
import json, os
from datetime import datetime

data = {
    "blogger": {"name": "...", "profile_url": "..."},
    "note": {"id": "...", "title": "...", "url": "..."},
    "comments": [...],
    "scraped_at": datetime.now().isoformat(),
    "total_comments": len(comments)
}

out_dir = os.path.join(os.path.expanduser("~"), "Downloads", "xhs_comments")
os.makedirs(out_dir, exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"xhs_comments_{blogger}_{note_id}_{ts}.json"
with open(os.path.join(out_dir, filename), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### Step 5 — Analysis Report (Optional)

If user asks for visualization, generate in `Downloads\xhs_comments_analysis\`:

1. **Charts** (Python): jieba word segmentation + matplotlib + wordcloud
2. **HTML report**: Embed `ALL_NOTES` as JSON JS variable
3. **Dual-note comparison**: Two `<select>` dropdowns, keyword search with `data-content` attribute matching

Chart generation order: PNG charts first → HTML with local image refs → `Start-Process` to open.

---

## Error Handling

| Scenario | Response |
|----------|----------|
| Page load failure | Retry 2×, wait 5s each |
| 0 comments found | Log and skip to next note |
| Captcha trigger | Tell user to complete manually in Chrome |
| Note deleted (404) | Skip, continue to next |
| Scroll produces no new content | Assume fully loaded, stop |
| innerText returns empty | Wait longer, take screenshot for debugging |
| URL format wrong for navigate | Use JS click instead of navigate |

---

## Dependencies

- browser tool (`profile="openclaw"`, **not "chrome"**)
- Python 3 (jieba + matplotlib + wordcloud)
- Chinese font: `C:\Windows\Fonts\STSONG.TTF`
- User must scan XHS QR code once in the popup Chrome window

---

## Pre-Run Checklist

- [ ] Use `profile="openclaw"` not `profile="chrome"`
- [ ] Extract note list with JS `querySelectorAll` + href parsing
- [ ] Enter note via JS `element.click()`, not direct navigate
- [ ] Extract comments via `document.body.innerText`, not DOM selectors
- [ ] Explicitly click all "Expand N replies" buttons
- [ ] Captcha: tell user to complete manually, don't retry automatically
- [ ] JSON saves: `encoding='utf-8'` explicitly
- [ ] PowerShell commands use `;` not `&&`
- [ ] Screenshot on first entry to each note for debugging
