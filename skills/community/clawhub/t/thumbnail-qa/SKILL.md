---
name: thumbnail-qa
version: "1.0.0"
description: |
  Thumbnail image QA: browse every page, detect images poorly cropped in their
  containers, compute fine-grained object-position values, and auto-fix with
  before/after evidence. Each fix gets its own atomic commit.
  Use when asked to "check thumbnails", "fix image cropping", "thumbnail qa",
  or after uploading new images.
  Proactively suggest when the user adds or replaces images in /public.
allowed-tools:
  - Bash
  - Read
  - Edit
  - AskUserQuestion
triggers:
  - thumbnail qa
  - fix image cropping
  - check thumbnails
homepage: https://github.com/kaicianflone/thumbnail-qa-skill
repository: https://github.com/kaicianflone/thumbnail-qa-skill
author: kaicianflone
license: MIT
---

# Thumbnail QA Skill

## Overview

This skill browses every page of the Next.js site, detects images that are poorly cropped
in their containers, computes optimal `object-position` values based on focal point analysis,
and applies fine-grained CSS fixes — each with a before/after screenshot and its own atomic commit.

---

## Setup

```bash
# Find browse binary
B=$(command -v browse 2>/dev/null || echo "$HOME/.claude/skills/gstack/browse/bin/browse")

# Verify browse is available
if [ ! -x "$B" ]; then
  echo "ERROR: browse binary not found at $B"
  echo "Install gstack or ensure browse is on PATH."
  exit 1
fi
```

### Check working tree cleanliness

Run `git status --porcelain`. If output is non-empty, ask the user:

> "Your working tree has uncommitted changes. Before running thumbnail QA, would you like to:
> 1. Commit your changes now
> 2. Stash your changes (git stash)
> 3. Abort and handle it manually
>
> Which option?"

Proceed only after the working tree is clean (or the user explicitly chooses option 3 and understands the risk).

### Check dev server

```bash
# Check if dev server is running
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|301\|302" && echo "running" || echo "not running"
```

If not running, start it:

```bash
npm run dev &
DEV_PID=$!
# Wait for server to be ready (up to 30 seconds)
for i in $(seq 1 30); do
  curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|301\|302" && break
  sleep 1
done
```

### Configure viewport and output directory

```bash
# Set viewport
$B viewport 1280x800

# Create output directory
mkdir -p .gstack/thumbnail-qa/screenshots

# Ensure .gstack/ is in .gitignore
if ! grep -q "^\.gstack/" .gitignore 2>/dev/null; then
  echo ".gstack/" >> .gitignore
  git add .gitignore
  git commit -m "chore: add .gstack/ to .gitignore"
fi
```

---

## Phase 1: Build Image Registry

### Step 1.1 — Grep for fill-mode Next.js Image components

```bash
grep -rn "<Image" --include="*.tsx" --include="*.ts" --include="*.jsx" --include="*.js" . \
  | grep -v "node_modules" \
  | grep "fill"
```

For each file that contains a match, **READ THE ENTIRE FILE** using the Read tool (not just a 25-line window). Understanding the full component is required to correctly resolve conditional classNames and dynamic src values.

### Step 1.2 — Extract per-image metadata

For each `<Image` with the `fill` prop, record:

| Field | Description |
|-------|-------------|
| `id` | Sequential number (1, 2, 3, ...) |
| `file_path` | Absolute path to TSX file |
| `line_number` | Line where `<Image` starts |
| `page_route` | URL path (e.g., `/`, `/about`, `/connect`) |
| `src` | Value of the `src` prop (string or expression) |
| `className` | Full className string or expression |
| `current_position` | Extracted object-position class (e.g., `object-top`, `object-[50%_25%]`, or `none`) |
| `container_classes` | Classes on the wrapping div (especially overflow-hidden, aspect-*, h-*, w-*) |
| `conditional_key` | If className is conditional, the field/expression it keys on |
| `notes` | Any dynamic/conditional complexity |

### Step 1.3 — Filter out non-candidates

Skip images where:
- No `fill` prop present
- `src` contains `"logo"` (case-insensitive)
- Container div has `rounded-full` class (avatar/icon treatment)
- Image uses `object-contain` (intentionally letterboxed)

### Step 1.4 — Handle dynamic values

**Dynamic src** (e.g., `src={photo.src}` or `src={item.image}`):
- Expand each unique value in the data source as a separate registry entry
- Read the data file to enumerate all actual values

**Conditional className** (e.g., `className={category.id === 'worship' ? 'object-top' : 'object-center'}`):
- Record `conditional_key` as the field driving the condition (e.g., `category.id`)
- Document each branch as a separate sub-entry
- When applying fixes in Phase 3, use a position map keyed on the SAME field

### Step 1.5 — Print registry

Print a numbered list of all candidate images:

```
IMAGE REGISTRY (N candidates)
================================
[1] src: /images/team/alice.jpg
    route: /about
    file: components/TeamSection.tsx:42
    current position: object-top
    container: relative overflow-hidden h-64 w-full

[2] src: (dynamic) photo.src — 6 entries from data/photos.ts
    route: /gallery
    file: components/Gallery.tsx:18
    current position: object-center (static)
    conditional_key: none
    notes: expand 6 photo entries individually
...
```

Expected total: ~15 entries across the full site.

---

## Phase 2: Visual Analysis

### Step 2.1 — Group images by route

Group all registry entries by `page_route` to minimize browser navigation (visit each page once).

### Step 2.2 — Navigate and screenshot

For each page:

```bash
# Navigate
$B goto http://localhost:3000/PAGE_ROUTE

# Wait for images to load
sleep 1

# Screenshot the PARENT DIV (overflow-hidden container), not the img tag
$B screenshot ".gstack/thumbnail-qa/screenshots/IMAGE_ID-current.png" \
  --selector "div.relative.overflow-hidden:has(img[src*='FILENAME'])"
```

If the selector fails (dynamic src, complex DOM), fall back to:

```bash
$B screenshot ".gstack/thumbnail-qa/screenshots/IMAGE_ID-current.png" \
  --selector "CLOSEST_IDENTIFIABLE_PARENT"
```

Document selector used in analysis notes.

### Step 2.3 — Analyze original image

Use the Read tool to view the original image from `public/`:

```
Read: public/images/PATH_TO_IMAGE.jpg
```

This gives a visual view of the full uncropped image.

### Step 2.4 — Determine focal point

Analyze the full image and classify:

| Photo Type | Focal Point Priority Rules |
|------------|---------------------------|
| **Person / Portrait** | Face fully visible, forehead to chin. Eyes positioned in upper third of container. |
| **Group / Team** | Maximize number of visible faces. Favor horizontal center. Avoid cutting anyone. |
| **Architecture / Building** | Show full structure. Roofline and entryway both visible when possible. |
| **Worship / Activity / Event** | Keep primary action or speaker in frame. Avoid cropping hands/gestures. |
| **Landscape / Scene** | Key subject centered; horizon placement depends on sky vs ground interest. |

Record focal point as percentage coordinates: `X_PERCENT% Y_PERCENT%` (e.g., `50% 25%`).

### Step 2.5 — Evaluate current crop

Compare the screenshotted crop against the focal point rules. Determine:

- **OK**: Current crop keeps the focal point visible and well-framed. The face (forehead to chin) is fully in frame for people photos. The existing position class achieves an acceptable result.
- **NEEDS_FIX**: Focal point is clipped, partially obscured, or poorly positioned

**Do NOT mark an image as NEEDS_FIX if the current position already satisfies the focal point rules.** If `object-top` shows the face correctly, leave it. Do not replace a working value with a computed one that might be worse. The goal is curated results, not uniform syntax.

### Step 2.6 — Compute optimal object-position

**How `object-position` works:** `object-position: X Y` aligns the X% point of the image to the X% point of the container, and the Y% point of the image to the Y% point of the container.

- `object-top` (= `50% 0%`) pins the top of the image to the top of the container. Best for tall portraits where the face is in the upper portion.
- `object-center` (= `50% 50%`) centers the image. Works when the subject is in the middle.
- `object-bottom` (= `50% 100%`) pins the bottom.

**Key insight for tall portrait images in short wide containers:** The container crops a horizontal band from the middle of the image by default. To show content near the TOP of a tall image, use `object-top` or very low Y values (0-10%). A value like `object-[50%_20%]` does NOT mean "show the top 20%" — it shifts the view DOWN, which is the opposite of what you want for faces near the top of a portrait.

**Rules of thumb:**
- Face in the top 30% of a tall portrait → use `object-top` or `object-[50%_5%]`
- Face at center of image → `object-center` is fine
- Face in bottom third → use higher Y values (60-80%)
- Standard values (`object-top`, `object-center`) are preferred when they work — only use arbitrary values when fine-tuning is genuinely needed

Round to nearest 5% for cleaner values.

Record per-image analysis:

```
[1] alice.jpg — NEEDS_FIX
    photo type: portrait (tall image, face near top)
    focal point: 50% 20% (face, eyes near top of image)
    current: object-center (face cut off — container shows middle of image)
    recommended: object-top
    reason: Face is in upper portion of tall portrait — object-top pins the top of the image to show the face

[2] group-photo.jpg — OK
    photo type: group
    focal point: 50% 40% (faces clustered in center)
    current: object-top
    recommended: keep current
    reason: object-top already shows all faces — do not replace a working value
```

---

## Phase 3: Apply Fixes

Process each NEEDS_FIX image in order.

### Step 3.1 — Take "before" screenshot

```bash
$B goto http://localhost:3000/PAGE_ROUTE
sleep 1
$B screenshot ".gstack/thumbnail-qa/screenshots/IMAGE_ID-before.png" \
  --selector "div.relative.overflow-hidden:has(img[src*='FILENAME'])"
```

### Step 3.2 — Apply the CSS fix

Select the correct edit pattern based on the registry entry:

**Pattern A — Static className string**

Find the existing `object-*` class (or position to insert one) and replace/add:

```tsx
// Before
className="relative overflow-hidden h-64 object-center"
// After
className="relative overflow-hidden h-64 object-[50%_25%]"
```

Use the Edit tool. Do not change any other part of the className.

**Pattern B — Conditional ternary (keyed on a field)**

Replace the ternary with a position map that keys on the SAME field as the original condition:

```tsx
// Before (keyed on category.id)
className={`... ${category.id === 'worship' ? 'object-top' : 'object-center'}`}

// After (position map, same key: category.id)
const positionMap: Record<string, string> = {
  worship: 'object-[50%_20%]',
  music: 'object-[50%_35%]',
  community: 'object-[50%_45%]',
}
// In JSX:
className={`... ${positionMap[category.id] ?? 'object-center'}`}
```

If the conditional keys on `photo.caption` or similar string content rather than an ID, prefer adding a `position` field to the data objects and reading from that instead.

**Pattern C — Existing `object-[X_Y]` arbitrary value**

Replace only the arbitrary value portion:

```tsx
// Before
object-[50%_50%]
// After
object-[50%_25%]
```

### Step 3.3 — Wait for hot reload

```bash
sleep 2
```

### Step 3.4 — Take "after" screenshot

```bash
$B screenshot ".gstack/thumbnail-qa/screenshots/IMAGE_ID-after.png" \
  --selector "div.relative.overflow-hidden:has(img[src*='FILENAME'])"
```

### Step 3.5 — Verify fix against focal point rules

Display both before and after screenshots inline. Then **re-apply the focal point rules from Step 2.4 against the AFTER screenshot:**

- For people photos: is the face FULLY visible (forehead to chin)? Are the eyes in the frame?
- For group photos: are MORE faces visible than before, not fewer?
- For architecture: is the structure MORE complete than before?

**If the after screenshot fails any focal point rule that the BEFORE screenshot passed:** the fix made things WORSE. This is the most common failure mode — the computed position looked right on paper but the actual crop is worse.

1. Revert the file change using Edit (restore the original className)
2. Mark the entry as `MANUAL_REVIEW` with a note: "computed position {X} degraded framing vs original {Y}"
3. Do NOT commit

**If the after screenshot is ambiguous** (marginal improvement, unclear if better): mark as `MANUAL_REVIEW` rather than committing. Err on the side of keeping the original position.

Only proceed to commit if the after screenshot is CLEARLY better than the before.

### Step 3.6 — Atomic commit

After a confirmed good fix:

```bash
git add PATH/TO/CHANGED_FILE.tsx
git commit -m "style: reposition FILENAME thumbnail — REASON"

# Example:
# git commit -m "style: reposition alice.jpg thumbnail — pull frame up to keep face centered"
```

One commit per image. Exception: when multiple images share the same conditional block in one file (e.g., a position map covers 6 images in one component), commit them together with a message listing all affected images.

---

## Phase 4: Summary Report

### Step 4.1 — Collect results

Gather all per-image outcomes:
- **OK**: No fix needed
- **REPOSITIONED**: Fix applied and committed
- **SKIPPED**: Filtered out (logo, icon, object-contain)
- **MANUAL_REVIEW**: Fix attempted but result was poor or ambiguous

### Step 4.2 — Print structured report

```
THUMBNAIL QA REPORT
===================
Date:      YYYY-MM-DD
Viewport:  1280x800
Pages checked: N

RESULTS SUMMARY
---------------
Total candidates checked:  N
  OK (no fix needed):      N
  Repositioned:            N
  Skipped (filtered):      N
  Manual review needed:    N

REPOSITIONED IMAGES
-------------------
| # | Image | Page | Before Class | After Class | Reason |
|---|-------|------|--------------|-------------|--------|
| 1 | alice.jpg | /about | object-top | object-[50%_15%] | Face centered with forehead visible |
...

OK IMAGES (no change)
---------------------
| # | Image | Page | Position | Notes |
...

SKIPPED IMAGES
--------------
| # | Image | Reason |
...

MANUAL REVIEW NEEDED
--------------------
| # | Image | Page | Attempted Fix | Issue |
...

COMMITS
-------
  abc1234  style: reposition alice.jpg thumbnail — ...
  def5678  style: reposition team-photo.jpg thumbnail — ...

SCREENSHOTS
-----------
  .gstack/thumbnail-qa/screenshots/
```

### Step 4.3 — Save report to disk

```bash
REPORT_DATE=$(date +%Y-%m-%d)
REPORT_PATH=".gstack/thumbnail-qa/report-${REPORT_DATE}.md"
# Write the structured report above to $REPORT_PATH
```

### Step 4.4 — Final message

> "Thumbnail QA complete. N images repositioned across N pages. Report saved to `.gstack/thumbnail-qa/report-YYYY-MM-DD.md`. Run `/thumbnail-qa` again after your next image upload."
