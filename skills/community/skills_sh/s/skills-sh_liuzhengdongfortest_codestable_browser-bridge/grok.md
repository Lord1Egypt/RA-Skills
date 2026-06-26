---
name: Grok via browser-bridge
description: How to interact with xAI Grok on grok.com through the Browser Bridge Chrome extension
type: reference
---

# Grok via Browser Bridge

Use this when a task needs to operate xAI Grok at `https://grok.com` through Browser Bridge.

## Page Structure

- Chat input is a ProseMirror editor: `.tiptap.ProseMirror`.
- Submit button is usually `[data-testid="chat-submit"]`.
- User messages use `[data-testid="user-message"]`.
- Assistant responses are in `.response-content-markdown`.
- The model selector button is `#model-select-trigger` and shows the current model, such as `Auto`.
- The `新建聊天` button starts a new conversation.

## Command Patterns

Navigate:

```bash
python <skill-dir>/scripts/browser.py navigate "https://grok.com"
```

Find the editor:

```bash
python <skill-dir>/scripts/browser.py exec "document.querySelector('.tiptap.ProseMirror')"
```

Type text into the editor. Dispatch `input`; otherwise React/ProseMirror bindings may not notice the change.

```bash
python <skill-dir>/scripts/browser.py exec "
const editor = document.querySelector('.tiptap.ProseMirror');
editor.focus();
editor.innerHTML = '<p>your question here</p>';
editor.dispatchEvent(new Event('input', {bubbles: true}));
"
```

Submit by clicking the submit button. This is more reliable than synthesizing Enter on the current Grok UI.

```bash
python <skill-dir>/scripts/browser.py exec "document.querySelector('[data-testid=chat-submit]')?.click()"
```

If the button is unavailable, try Enter as a fallback:

```bash
python <skill-dir>/scripts/browser.py exec "
const editor = document.querySelector('.tiptap.ProseMirror');
editor.dispatchEvent(new KeyboardEvent('keydown', {
  key: 'Enter',
  code: 'Enter',
  keyCode: 13,
  which: 13,
  bubbles: true,
  cancelable: true
}));
"
```

Extract the latest assistant response:

```bash
python <skill-dir>/scripts/browser.py exec "
const blocks = document.querySelectorAll('.response-content-markdown');
const lastBlock = blocks[blocks.length - 1];
return lastBlock?.textContent || '';
"
```

## Timing

- Simple chat responses usually take about 20-30 seconds.
- Web search and summarization usually take about 40-60 seconds.
- Use `--timeout 60` or higher for search-heavy prompts.
- For long generations, poll `.response-content-markdown` periodically instead of assuming the first response is final.

## Observed Capabilities

- Grok can search current web sources, extract key information, and compile structured summaries with source attribution.
- Chinese prompts work naturally, and responses can be requested in Chinese.
- Search and answer generation may show transient status text, such as searching, extracting, or compiling.
