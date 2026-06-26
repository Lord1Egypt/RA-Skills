# Message Formatting — Telegram Bot API

## Parse Modes Comparison

| Feature | HTML | MarkdownV2 | Markdown (legacy) |
|---------|------|------------|-------------------|
| Bold | `<b>text</b>` | `*text*` | `*text*` |
| Italic | `<i>text</i>` | `_text_` | `_text_` |
| Underline | `<u>text</u>` | `__text__` | ❌ |
| Strikethrough | `<s>text</s>` | `~text~` | ❌ |
| Spoiler | `<tg-spoiler>text</tg-spoiler>` | `\|\|text\|\|` | ❌ |
| Code | `<code>text</code>` | `` `text` `` | `` `text` `` |
| Code block | `<pre>text</pre>` | ` ```text``` ` | ` ```text``` ` |
| Link | `<a href="url">text</a>` | `[text](url)` | `[text](url)` |
| Mention | `<a href="tg://user?id=123">name</a>` | `[name](tg://user?id=123)` | ❌ |
| Emoji | `<tg-emoji emoji-id="ID">emoji</tg-emoji>` | `![emoji](tg://emoji?id=ID)` | ❌ |
| Blockquote | `<blockquote>text</blockquote>` | `>text` | ❌ |

**Recommendation:** Use HTML. Fewer escape issues, more readable.

---

## HTML Formatting

### Basic Formatting

```html
<b>bold</b>
<strong>bold</strong>
<i>italic</i>
<em>italic</em>
<u>underline</u>
<ins>underline</ins>
<s>strikethrough</s>
<strike>strikethrough</strike>
<del>strikethrough</del>
<tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>strikethrough</s></i></b>
```

### Code

```html
<code>inline code</code>
<pre>code block</pre>
<pre><code class="language-python">
def hello():
    print("Hello")
</code></pre>
```

### Links

```html
<a href="https://example.com">link text</a>
<a href="tg://user?id=123456789">mention by ID</a>
```

### Blockquotes

```html
<blockquote>This is a quote</blockquote>
<blockquote expandable>
Long quote that can be collapsed...
</blockquote>
```

### Escaping HTML

Only escape these characters:
- `<` → `&lt;`
- `>` → `&gt;`
- `&` → `&amp;`

```python
def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
```

---

## MarkdownV2 Formatting

### Characters That Must Be Escaped

**Always escape these outside code blocks:**
```
_ * [ ] ( ) ~ ` > # + - = | { } . !
```

Escape with backslash: `\*` `\_` etc.

### Basic Formatting

```markdown
*bold*
_italic_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~strikethrough~ __underline italic bold___ bold*
```

### Code

```markdown
`inline code`
```
code block
```
```python
code block with language
```
```

### Links and Mentions

```markdown
[link text](https://example.com)
[mention](tg://user?id=123456789)
![👍](tg://emoji?id=5368324170671202286)
```

### Blockquotes

```markdown
>single line quote
>multiline
>quote continues

**>expandable quote
that can be collapsed
|
```

### Escaping Function

```python
import re

def escape_markdown_v2(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
```

---

## Common Formatting Patterns

### Progress Bar

```python
def progress_bar(percent, width=10):
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent}%"
# Output: [████████░░] 80%
```

### Status Message

```html
<b>📊 Status Update</b>

<b>Server:</b> Online ✅
<b>Users:</b> 1,234
<b>Uptime:</b> 99.9%

<i>Last checked: 2 minutes ago</i>
```

### Error Message

```html
<b>❌ Error</b>

<code>Error code: 403</code>

<blockquote>Access denied. You don't have permission to perform this action.</blockquote>

<i>Contact @admin for help.</i>
```

### List with Checkboxes

```html
<b>📋 Task List</b>

✅ Task completed
☑️ Task in progress
⬜ Task pending
❌ Task failed
```

### Code Example

```html
<b>Example Code</b>

<pre><code class="language-python">import requests

response = requests.get("https://api.example.com")
print(response.json())</code></pre>
```

---

## Tips

1. **Test formatting first** — Send to yourself before production
2. **Fallback to plain text** — If formatting fails, send without parse_mode
3. **Don't over-format** — Too much bold/italic is hard to read
4. **Use emojis for visual breaks** — ✅ ❌ 📊 📝 🔔
5. **Keep messages scannable** — Use headings and spacing
