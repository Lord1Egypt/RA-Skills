---
name: telegram-formatting
description: Formats Telegram replies using Telegram's actual supported formatting - when to use bold, code, quotes, headings, and structure without overusing them.
homepage: https://core.telegram.org/bots/features#rich-messages
---

# Telegram formatting

Apply this whenever replying in the `telegram` channel. Telegram is not a generic markdown renderer - only specific tags/syntax actually render, and which set is available depends on one config flag. Check it once per session, don't assume:

```bash
openclaw config get channels.telegram.richMessages
```

If `true` or unset-but-you've-confirmed-it-works, use the **Rich messages** section below. If `false`/unset and unconfirmed, use the **Standard mode** section only - rich syntax (`#`, `<details>`, tables) will either get stripped or show as literal characters in standard mode.

**Version check, once per session, before trusting any "broken"/"works" claim in the Rich messages table below:**

```bash
openclaw --version
```

This skill's Rich messages test results are tied to a specific version (see "Tested on" in that section). If your version matches, trust the table as-is. If it differs - older or newer - treat every status in that table as unverified, not fact: send a real test message for whichever block you're about to use (a throwaway DM to yourself works) before relying on it in a live reply. OpenClaw's rich-message renderer is actively developed; bugs marked broken here may get fixed, and things marked working could regress. Don't carry this table forward blindly across versions, and don't skip testing just because the spec says a tag should work - the spec already turned out wrong once in this skill's own testing (`<details>` looked correct on paper and broke in practice).

If you re-test and find a status has changed, update this file so the next read is accurate - that's the whole point of keeping test results instead of copying the spec.

## Standard mode (always available, parse_mode=HTML)

| Tag | Renders as | Use for |
|---|---|---|
| `<b>text</b>` | **bold** | The 1-3 truly key words per message - a decision, a number, a name. Not every noun. |
| `<i>text</i>` | *italic* | A brief aside, a soft caveat, a term being introduced. |
| `<u>text</u>` | underline | Rare. Skip it - bold already carries emphasis; underline reads as a link on mobile and confuses people. |
| `<s>text</s>` | ~~strike~~ | Showing something superseded ("~~v1~~ -> v2"). Rare. |
| `<code>text</code>` | inline monospace | Filenames, commands, model IDs, env var names, exact values - anything the user might copy-paste or that must be read literally. |
| `<pre><code class="language-x">...</code></pre>` | code block | Actual code, logs, config blocks, tables of data. Add the language for syntax highlighting. |
| `<blockquote>text</blockquote>` | quoted block | Quoting the user back, or quoting an external source (an error message, a doc excerpt). |
| `<blockquote expandable>text</blockquote>` | collapsible quote | Long supplementary detail (full logs, a long excerpt) that isn't needed to understand the reply - collapse it so the main point isn't buried. |
| `<a href="url">text</a>` | link | Only when there's a real destination worth clicking. Never bare URLs as filler. |
| `<tg-spoiler>text</tg-spoiler>` | spoiler blur | Essentially never for assistant replies - this is a joke/game mechanic, not a formatting tool. Using it to "hide" real information reads as gimmicky. |

No native list tags exist in Telegram HTML. For lists, use plain lines with `-` or numbers and real line breaks - do not wrap them in any tag.

Escape literal `<`, `>`, `&` in text as `&lt;` `&gt;` `&amp;` if they appear outside a tag (rare - OpenClaw's renderer usually handles this for you).

## Rich messages mode (`channels.telegram.richMessages: true`)

Write plain Markdown for these - not the HTML tags above - and OpenClaw's renderer converts it to native Bot API 10.2 rich blocks. Test results below are from live testing on OpenClaw 2026.7.1-2; if your version differs and behavior seems off, re-verify with a real test message before trusting either this table or your assumptions - renderer bugs get fixed over time.

| Block | Syntax | Status (tested on 2026.7.1-2) |
|---|---|---|
| Heading | `# H1` ... `###### H6` | Works - real heading, **only when the message has no images.** |
| Table | markdown table, `\| a \| b \|`, max 20 columns | Works - real bordered table, image-free messages. |
| Blockquote | `> text` | Works - real styled quote block, image-free messages. |
| Collapsible | `<details open><summary>label</summary>...</details>` | Broken - flattens to plain always-visible text. Tested 3 variants (with/without `open`, with/without blank lines), all failed identically, with zero images present - not an image issue, the renderer doesn't implement this block. Use `> text` instead. |
| Checklist | `- [ ] task` / `- [x] done` | Broken - renders as literal `• [ ] task` text, not a real checkbox. Write "Done: X, Pending: Y" as plain text instead. |
| Pull quote | `<aside>quote<cite>Author</cite></aside>` | Broken - tags silently stripped, quote and author text run together with no separator. Use `> text` instead. |
| Slideshow / Collage | `<tg-slideshow>`/`<tg-collage>` + `![](url)` per image | Not usable - OpenClaw does not implement outbound Telegram media groups yet ([upstream issue, open](https://github.com/openclaw/openclaw/issues/14027)). Each image sends as its own separate photo message instead of a grouped carousel, regardless of tag or syntax. This is a missing feature, not a syntax problem - don't try to work around it with different markup. |

**Critical rule: any image in the message drops the whole thing to a photo caption**, which only supports plain HTML (no headings/tables/blockquote-as-rich-block) and caps at 1024 characters. Confirmed by sending an identical heading with and without an attached image - only the image-free version rendered as a real heading. If a reply needs both a heading/table and an image, send them as separate messages.

**Bottom line: heading, table, and blockquote are the only proven-reliable rich blocks, and only in image-free messages.** Treat collapsible, checklist, pull quote, and slideshow/collage as unusable until you've personally re-verified them working - don't trust this table blindly if you're on a different OpenClaw version, but don't trust the spec blindly either. Send a real test message first.

**Compatibility risk:** some Telegram clients (older Desktop/Web/Android/third-party) don't support Bot API 10.2 and may render rich messages as broken or "unsupported message." If a reply looks wrong to the user, ask what client they're on before assuming a formatting bug.

## Decide by message shape, not by habit

**Short reply (1-2 sentences, a quick answer, a confirmation):** no formatting at all. A bolded word in a one-line reply reads as shouting.

**Medium reply (a short paragraph, an explanation with a couple of technical terms):** plain prose, `<code>` for the 1-3 literal terms (a filename, a command), maybe one `<b>` if there's a genuine headline result. That's it.

**Long / structured reply (multi-step instructions, a status report, several findings):** break into short paragraphs with blank lines between them - blank-line separation does more for readability than any tag. In standard mode use `<b>` as inline section labels ("Status:", "Next step:"); in rich mode with no images, a real `#`/`##` heading can do the same job. Use a plain `-` list when enumerating items. Push anything genuinely optional (full logs, long background) into `<blockquote expandable>` (standard mode) or `> text` (rich mode) so the reply stays scannable at a glance.

## The overuse tells

If you're about to bold more than ~3 things in one message, you're not emphasizing anymore - you're just formatting for its own sake. Pick the one thing that actually matters. Same logic for code tags: not every word that happens to be technical needs `<code>` - only things meant to be copied or read character-for-character.

If you're about to reach for `<u>` or `<tg-spoiler>`, don't - there's almost always a better tag or no tag at all.

In rich mode, a heading or table for an ordinary answer that a short paragraph would serve just as well is the same failure, just with bigger tools. A one-line answer never needs a `#` heading.

## The underuse tell

If a reply is more than ~6 lines of unbroken prose with no paragraph breaks, it needs structure - not necessarily bold or code, just blank lines between ideas and a `-` list if there are parallel items. A wall of text is the more common failure mode than over-formatting.
