# Brand Checklist & Design Patterns

This skill is generic — collect the following from the user before building,
then apply the patterns below. If the user has a brand reference file, read it
instead of asking.

## Collect from the user
1. **Logo** — image file. Best on a white or transparent background. Trim the
   whitespace, composite onto white, and embed as base64 so the HTML stays
   self-contained. Show it on a white rounded plate with a soft shadow on the
   end card. If no logo is provided, keep the "YOUR LOGO" placeholder and say so.
2. **Product name, price, and domain.**
3. **The pain point** — the customer complaint in their own words (this becomes
   the first bubble). Ask "what does your customer say right before they need you?"
4. **One concrete proof point** — official source, time saved, credential,
   number ("backed by official public data", "done in an hour").
5. **The expensive alternative** — for the struck-through price anchor
   ("$300+ consultant" → "$29"). Skip the anchor if there isn't a clear one.
6. **Accent color** (optional) — otherwise pick one per the theming pattern below.

## Color theming pattern
Give each product a distinct accent so ads are distinguishable in rotation.
Link-card gradient: `linear-gradient(135deg, <very dark accent> 0%, <accent> 65%, <light accent> 100%)`.
End card: near-black background tinted toward the accent (e.g. `rgba(5,10,18,.94)`
for blue), `em` highlight in the light accent, CTA button in the main accent.
Example set: blue `#0a84ff`, orange `#e8720c`, violet `#7c3aed`, green `#12a35a`.
Keep the chat itself standard iMessage (blue outgoing `#0a84ff`, gray incoming
`#26262a`, dark background) — the accent lives in the link card and end card only.

## Copy voice
- **Hook** = the customer's pain, first bubble, outgoing (blue), their own words.
- **Friend** = calm, confident, specific: product, price, one proof point.
- **Positive framing.** Describe what the customer gains, not what's absent —
  avoid stacked negations ("No X. No Y."). Put cost comparisons in the visual
  price anchor, not the dialogue.
- Emojis: max 1 per bubble, only where a real texter would (😩 😳 🙄 🙌 🙏).
- Keep bubbles under ~90 characters (1–2 lines at 15px in a 78%-width bubble).

## Platform specs
- Output: 1080×1920 (9:16), 30fps, H.264 + AAC, ~15s, faststart — works as-is on
  YouTube Shorts, Reels, TikTok, and Meta feed.
- Feeds autoplay muted: visuals must carry the message; sound is a bonus.
- Ad platforms add their own "Sponsored" label; if a reviewer flags the
  dramatized format, add a small "Dramatization" line to the end card.

## Caption formulas (offer after delivering the video)
- **YouTube title:** pain/objection + price hook ("X Won't Win Your Claim —
  This Will ($10)").
- **YouTube description:** 2 sentences (pain → product + price + time), an
  emoji + URL line, 4–6 hashtags.
- **Instagram:** 'Authority: "<demand>" / You: *<confident action>*' beat, then
  product + price + "Link in bio", then 5–8 lowercase hashtags mixing category
  and audience tags.
