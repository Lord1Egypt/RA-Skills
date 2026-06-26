# Examples · Real Outputs as Reference

These are **actual outputs** produced by Content Engine v0.2.0, kept here as learning samples and a quality baseline.

Not templates — real artifacts. You can see the entire chain "deconstruction card → our brand version" in concrete form.

---

## Three samples

```
examples/
├── v1-deconstruction-card/         ← Starting point: the v1 deconstruction of a viral XHS link
│   └── AIC-260426-001-deconstruction.md
│
├── v2-image-example/               ← v2 image-type output (based on the card above)
│   ├── script.md                   Image plan (6 images + holistic narrative)
│   ├── cover.png + cover.txt       Cover image (with Chinese overlay text) + text backup
│   ├── frames/frame_001.png        Reference frame (Nano Banana, vertical 9:16)
│   ├── desc.txt                    XHS post body
│   └── tags.txt                    Hashtags
│
└── v2-video-example/               ← v2 video-type output (same source card)
    ├── script.md                   Video script (5 cinema shots)
    ├── caption.txt                 On-screen captions
    ├── cover.png + cover.txt       Cover image + text
    ├── frames/frame_001.png        Key frame (1 image, for shoot reference)
    ├── desc.txt + tags.txt         Post-publishing assets
    └── seedance-prompt.md          Seedance 2.0 cinema-style prompt
                                    (v2.0 doesn't generate real video; outputs this prompt
                                     as substitute. v2.1 will auto-execute it.)
```

---

## How these samples were produced

### Commands

```bash
# Deconstruct (v1) — produces the card
python3 scripts/extract_xhs.py "https://www.xiaohongshu.com/explore/69d4e2f7000000002202853a"

# Generate (v2) — based on the card + your brand
python3 scripts/generate_xhs.py "https://www.xiaohongshu.com/explore/69d4e2f7000000002202853a" \
  --type image --count 1 \
  --product-usp "Heritage womenswear: silk vest + embroidered shirt"

python3 scripts/generate_xhs.py "https://www.xiaohongshu.com/explore/69d4e2f7000000002202853a" \
  --type video --count 1 \
  --product-usp "Heritage womenswear: silk vest"
```

### The reference content

XHS link `69d4e2f7000000002202853a` is a 34-second product display video from "见花开 / Shenzhen / What does wearing a season of spring feel like?" — 330 likes / 231 saves / 133 comments (save-to-like ratio 70%). Classic "immersive merchandising" viral format.

### Brand setup (demo)

`--product-usp "Heritage womenswear: silk vest + embroidered shirt"` is **fictional demo data**, not a real brand. In production you'd pass your actual product USPs.

### Performance data

| Type | LLM calls | Image calls | Total time | Estimated cost |
|---|---|---|---|---|
| image (count=1) | 4 | 2 | ~127s | ~$0.20 |
| video (count=1) | 5 | 2 | ~190s | ~$0.30 |

---

## What to look at in these samples

### v1 → v2 correspondence

Open `v1-deconstruction-card/...md` and `v2-image-example/script.md` side by side:

- Card §4 "Reference content deconstruction" shows the immersive merchandising 3-layer structure → image script.md reproduces this as "image plan, 3-layer narrative"
- Card §7 "Emotion hook" identifies "Aspiration｜atmospheric immersion" → image script.md reuses this hook
- Card §13 "Reference body copy" has restrained negative-space tone → desc.txt continues that

**v2 isn't free generation — it's evidence-based competitor mirroring.**

### Visual consistency

Open `v2-image-example/cover.png` and `v2-image-example/frames/frame_001.png`:

- ✅ Both vertical 9:16
- ✅ Both single images (no collage)
- ✅ Same aesthetic (restrained eastern, natural light, craft texture)
- ✅ Cover has Chinese overlay text "把一朵花绣进春天里" ("Embroider a flower into spring")

These are the post-fix v2 stable quality — `build_prompt`'s "three-path constraint + anti-collage" mechanism in action.

### Seedance prompt format

Open `v2-video-example/seedance-prompt.md` to see 5 shots in standard Seedance 6-dim format (shot type / subject / setting / camera movement / mood / duration). This is the format v2.1 will feed Seedance directly when integrated.

The file header has a blockquote explaining v2.0's current usage paths (run manually / wait for v2.1 / hand to a videographer).

---

## NOT how to use these samples

⚠️ **Do not directly copy these outputs and publish them**. Reasons:

1. The brand data is fictional demo (the source XHS account is "见花开", which is the *competitor*, not you)
2. In your real use case, brand-voice / brand-story / segments should be filled (these examples were generated in objective mode with empty graph templates)
3. Real usage: fill graph first, then generate — output upgrades from "generic style" to "brand-specific"

Proper usage: **treat these as a quality baseline** — your outputs should hit this bar (or higher) before you publish.

---

## Reproduction cost

- 1 deconstruction ≈ $0.50 (TikHub API + LLM analyzing 17 frames)
- 1 image generation (count=1) ≈ $0.20
- 1 video generation (count=1) ≈ $0.30
- **Full pipeline ≈ $1 per cycle**

In production batches (1 deconstruction + N generation variants), the deconstruction cost amortizes across multiple generations.
