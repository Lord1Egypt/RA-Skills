# Expression Tags

> **⚠️ Status: Partially implemented / Mostly imperceptible**
>
> Supertonic accepts inline tags in text, but **only a subset produces clearly audible expression** in the output. The rest either insert minor pauses (not perceptible as the intended emotion) or have no effect at all.

## User-Verified Tags

| Tag | Status | Effect | Example |
|-----|--------|--------|---------|
| `<laugh>` | ✅ **Works** | Audible laughter burst | `"You did it <laugh> I am so proud."` |

## Documented but Unverified / Weak

| Tag | Status | Notes |
|-----|--------|-------|
| `<breath>` | ⚠️ Unverified | May insert a pause. Not confirmed as audible breathing. |
| `<sigh>` | ⚠️ Unverified | May insert a pause. Not confirmed as audible sighing. |

## Tested but Failed (no audible effect)

These tags were tested with M5, M3, and F2. Duration occasionally increased slightly (suggesting the model processes the token), but **the output did not contain the intended expression**:

- `<sarcastic>` — reads as a slight pause, not sarcasm
- `<excited>` — reads as a slight pause, not excitement
- `<whisper>` — reads at normal volume
- `<shout>` — reads at normal volume
- `<happy>`, `<sad>`, `<angry>` — no emotional shift
- `<chuckle>`, `<giggle>`, `<snort>`, `<gasp>`, `<grunt>`, `<cough>`, `<scream>` — no audible reaction
- `<sing>` — no melodic delivery
- `<cry>`, `<yawn>`, `<hmm>`, `<aha>` — no effect

## Correct Syntax

Tags are **self-closing** — place them inline where the reaction would naturally occur:

```python
# ✅ Correct — self-closing inline tag
text = "You did it <laugh> I am so proud."

# ❌ Wrong — do not wrap text
text = "<laugh>I am so proud.</laugh>"
```

## What Actually Works for Expression

Since tags are mostly non-functional, use these reliable techniques:

| Emotion | Technique | Example |
|---------|-----------|---------|
| Happy | Upbeat words + `speed=1.1` | `"This is incredible!" --speed 1.1` |
| Sad | Subdued words + `speed=0.85` | `"I'm sorry... this is hard." --speed 0.85` |
| Excited | Exclamations + `speed=1.15` | `"We did it! Amazing!" --speed 1.15` |
| Urgent | Short imperatives + `speed=1.2` | `"Move. Now." --speed 1.2` |
| Serious | Direct words + `speed=0.95` | `"Mission parameters confirmed." --speed 0.95` |

## References

- [Main repo README](https://github.com/supertone-inc/supertonic) — claims 10 tags, only lists `<laugh>, <breath>, <sigh>`
- [Python SDK docs](https://supertone-inc.github.io/supertonic-py/) — no tag documentation
- [HF model card](https://huggingface.co/Supertone/supertonic-3) — only mentions `<laugh>, <breath>, <sigh>`

**Bottom line:** Use `<laugh>` if you need a laugh. For everything else, use word choice + speed.
