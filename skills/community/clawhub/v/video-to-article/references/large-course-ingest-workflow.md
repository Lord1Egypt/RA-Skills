# Large Course Ingest: Six-Phase Details

## Course Directory Layout

```text
CourseName/
├── Level 1 - Basics/
│   ├── 1. Intro.mp4 + 1. Intro.en.srt
│   └── ...
├── Level 2 - Advanced/
├── _preprocessed/        <- output of Phase 2
├── _screenshot_plan.json <- output of Phase 3
└── _batch_screenshots.sh <- output of Phase 3
```

## Phase 1: Directory analysis

Match directory names by exact numeric prefix such as `"1 "` for Level 1. Avoid fuzzy matching.

## Phase 2: Subtitle preprocessing

Use `scripts/preprocess-srt.py`:
1. copy or edit the config
2. run the script
3. produce one plain-text file per section

## Phase 3: Screenshot planning

Use `scripts/plan-screenshots.py` to determine frame counts by duration:
- under 30 seconds: 1 frame
- 30 to 120 seconds: 2 frames
- over 120 seconds: 3 frames

Do not place screenshots for intros or recap-style lessons.

## Phase 4: Batch screenshots

```bash
bash _batch_screenshots.sh
```

Run in the background, but keep `ffmpeg` sequential because it is CPU-intensive.

## Phase 5: Parallel article writing

Recommended parallel allocation:
- up to 3 subagents
- up to 4 sections per subagent

### Recommended context template

Keep the context compact and explicit:

```text
Write the course note in English.

Input: {path}/section-{N}.txt

All screenshots are already prepared. Do not verify files.
Reference them directly as:
  ![[../../../assets/{course}/{slug}-{label}.jpg]]

Slug table (each slug has overview/detail/result unless noted otherwise):
- Overview -> overview (no screenshots)
- Installation -> installation (3 screenshots)

Density: Intro and recap lessons get no screenshots. Other lessons get 3 screenshots each.

Output: {vault}/sources/{course}/section-{N}-{slug}.md
```

### What subagents should not do

- do not modify `index.md`
- do not verify screenshot files
- do not compute slugs

## Phase 6: Wrap-up

1. The main agent updates `index.md`
2. Write an import log
3. Commit the result

## Common pitfalls

- **Incorrect level mapping**: verify each section's `level` field
- **Video prefix mismatch**: match the full prefix such as `"2.2. "` instead of `"2.2"`
- **`index.md` separator traps**: insert content using a stable marker, not a loose `---`
