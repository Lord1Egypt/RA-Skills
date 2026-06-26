# YumFu v1.7.8 — Storybook Quality + Ending Auto-Generation 📚

This release upgrades YumFu’s storybook system from a nice export feature into a much more reliable end-of-journey delivery flow.

## ✨ Highlights

### 1. Better storybook HTML quality
- Upgraded `generate_storybook_v3.py`
- Storybooks now render with a more formal illustrated-storybook presentation
- Scene blocks stay image-bound instead of drifting toward detached galleries or transcript dumps

### 2. Unicode-escaped titles now render correctly
- Fixed accidental raw escape output like `\u9aa8\u602a\u7cbe\u7075`
- Titles and prose now decode before rendering into the final HTML storybook

### 3. Final stats section is much more reliable
- Storybook stats now pull from multiple save fields instead of failing open into empty sections
- Better extraction for:
  - HP / stamina / level
  - attributes
  - inventory
  - relationships
  - skills / spells / achievements
- Avoids ugly raw dict dumps in the rendered page

### 4. Image captions are scene-aware
- Captions no longer fall back so easily to lazy filename fragments like `Watch` or `Thread`
- They now prefer scene metadata, descriptions, and story prose for more meaningful captions

### 5. End-of-journey storybooks can auto-generate
- Added `scripts/prepare_end_storybook.py`
- Ending / retire / archive branches can now refresh or generate the final HTML storybook automatically

### 6. Ending storybooks are now wired into the standard delivery helper
- `scripts/deliver_yumfu_turn.py` now supports `--ending-storybook`
- End-of-run delivery can prepare:
  - final text
  - TTS
  - final HTML storybook
  in one structured payload

### 7. Storybook flow documentation is now consistent
- Updated `SKILL.md`, `STORYBOOK_SYSTEM.md`, and `IMPLEMENTATION_SUMMARY.md`
- Deprecated old `generate_storybook.py` / `generate_storybook_v2.py` flows for new usage
- Standardized on:
  - `generate_storybook_v3.py` for canonical HTML storybooks
  - `deliver_yumfu_turn.py --ending-storybook` for ending delivery

### 8. GitHub Pages storybook demo is now live
- Added a live storybook demo index
- Added the featured Journey to the West / White Bone demo page
- Linked the live demos from `README.md` and `README.zh.md`

## 🔗 Live demo
- Storybook index: https://yumyumtum.github.io/yumfu/storybooks/
- Featured demo: https://yumyumtum.github.io/yumfu/storybooks/journey-to-west-white-bone/

## 🧪 Verified
- Storybook integration test updated and passing
- Real save end-storybook preparation verified on LOTR
- GitHub Pages deployment verified live

## Notes
- HTML remains the canonical storybook output
- PDF remains optional and should only be treated as a secondary export after layout is visually confirmed
