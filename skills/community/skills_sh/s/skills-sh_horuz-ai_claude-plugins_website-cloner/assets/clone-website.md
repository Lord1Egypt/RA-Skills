---
description: Clone any website with pixel-perfect fidelity using specialized sub-agents
argument-hint: "<url>"
allowed-tools: Bash, Task, Read, Write, Glob
---

# Clone Website Orchestrator

**Target URL:** $ARGUMENTS

You are the ORCHESTRATOR for cloning a website. You do NOT write code yourself - you delegate ALL work to specialized sub-agents and coordinate the workflow.

## Phase 0: Setup

First, detect the project type and create task folder structure:

```bash
DOMAIN=$(echo "$ARGUMENTS" | sed -E 's|https?://([^/]+).*|\1|' | sed 's/www\.//')
TASK_DIR=".tasks/clone-${DOMAIN}"

# Create task folder for screenshots and context
mkdir -p "${TASK_DIR}/screenshots"

# Create public folders for assets (if they don't exist)
mkdir -p "public/images" "public/videos" "public/icons"

cat > "${TASK_DIR}/context.md" << 'EOF'
# Website Clone Task

**Target URL:** $ARGUMENTS
**Created:** $(date)
**Status:** In Progress

---

EOF

echo "✅ Task folder created: ${TASK_DIR}"
echo "✅ Public asset folders ready"
```

Detect project type:
```bash
# Check package.json for framework
if grep -q '"next"' package.json 2>/dev/null; then
  echo "📦 Detected: Next.js"
elif grep -q '"@tanstack/start"' package.json 2>/dev/null; then
  echo "📦 Detected: TanStack Start"
elif grep -q '"vite"' package.json 2>/dev/null; then
  echo "📦 Detected: Vite"
fi
```

Store TASK_DIR and project type for reference throughout the workflow.

---

## Phase 1: Screenshot Capture

**Invoke the `website-screenshotter` sub-agent:**

```
Use the website-screenshotter agent to capture comprehensive screenshots of $ARGUMENTS

Task folder: ${TASK_DIR}
Screenshot output: ${TASK_DIR}/screenshots/
Context file: ${TASK_DIR}/context.md

Capture:
- Full page at desktop (1920x1080), tablet (1024x768), and mobile (375x812)
- Each section individually
- Key components with hover states
- Any animations or interactive elements

Update context.md with the screenshot inventory when done.
```

**Wait for completion before proceeding.**

---

## Phase 2: Asset & Style Extraction

**Invoke the `website-extractor` sub-agent:**

```
Use the website-extractor agent to extract all assets and styles from $ARGUMENTS

Task folder: ${TASK_DIR}
Context file: ${TASK_DIR}/context.md

Asset output folders:
- Images: public/images/
- Videos: public/videos/
- Icons: public/icons/

Extract:
- All images, videos, SVGs, icons → save to appropriate public/ subfolder
- Complete color palette with exact hex values
- Typography (fonts, sizes, weights, line-heights)
- Spacing patterns (padding, margins, gaps)
- Component styles (buttons, cards, inputs, shadows, border-radius)
- Animation definitions
- Page structure breakdown

Write style information to context.md in a well-organized format.
Document asset paths so the cloner knows where to reference them.
```

**Wait for completion before proceeding.**

---

## Phase 3: Implementation

**Invoke the `website-cloner` sub-agent:**

```
Use the website-cloner agent to implement a pixel-perfect clone

Task folder: ${TASK_DIR}
References:
- Screenshots: ${TASK_DIR}/screenshots/
- Assets: public/images/, public/videos/, public/icons/
- Styles & info: ${TASK_DIR}/context.md
- Review notes (if exists): ${TASK_DIR}/review-notes.md

Requirements:
- DETECT PROJECT TYPE first (Next.js, TanStack Start, Vite, etc.)
- Create a SINGLE React component file in the appropriate location
- Use TAILWIND CSS for all styling (arbitrary values like [#hex] for exact colors)
- Use MOTION (from "motion/react") for animations - NOT framer-motion
- Divide sections with multi-line comments
- Reference assets from /images/, /videos/, /icons/ paths
- Match EXACT colors, fonts, spacing from context.md

Output location (based on project):
- Next.js App Router: app/clone/page.tsx
- Next.js Pages: pages/clone.tsx
- TanStack Start: src/routes/clone.tsx
- Vite: src/pages/Clone.tsx

If review-notes.md exists, prioritize fixing listed issues.
```

**Wait for completion before proceeding.**

---

## Phase 4: QA Review

**Invoke the `website-qa-reviewer` sub-agent:**

```
Use the website-qa-reviewer agent to review the clone

Original: $ARGUMENTS
Clone: React component (start dev server with `npm run dev` to preview)
Screenshots: ${TASK_DIR}/screenshots/
Output: ${TASK_DIR}/review-notes.md

The clone is a React component using Tailwind CSS and motion.
Start the dev server and navigate to the clone route to review.

Perform:
- Side-by-side comparison at all viewports
- Check every section systematically
- Verify Tailwind classes produce correct colors, spacing, shadows
- Check motion animations match original
- Verify all images loading from public/ folders
- Document ALL discrepancies found

Classify issues as Critical, Major, or Minor.
Set status to NEEDS_WORK, ACCEPTABLE, or PERFECT.
```

**Wait for completion and read the results.**

---

## Phase 5: Iteration Loop

Read `${TASK_DIR}/review-notes.md` and check the status:

### If Status = PERFECT ✅
```
🎉 Clone complete!

Output: ${TASK_DIR}/output/index.html
Assets: ${TASK_DIR}/assets/

The website has been cloned with pixel-perfect accuracy.
```
**End workflow.**

### If Status = ACCEPTABLE ⚠️
Ask the user:
```
The clone is good but has minor issues. Would you like to:
1. Accept as-is
2. Continue refining

Minor issues found:
[List from review-notes.md]
```
If user wants to continue → go back to Phase 3.
If user accepts → end workflow.

### If Status = NEEDS_WORK 🔄
```
Issues found that need fixing. Starting iteration [N]...
```
Go back to **Phase 3: Implementation**.

**Maximum iterations: 5** (to prevent infinite loops)

After 5 iterations, if still not perfect:
```
⚠️ Maximum iterations reached.

Current status: [status]
Remaining issues: [list from review-notes.md]

The clone is functional but may need manual refinement.
Output: ${TASK_DIR}/output/index.html
```

---

## Completion Summary

When finished, provide:

```markdown
## Clone Complete 🎉

**Original:** $ARGUMENTS
**Project Type:** [Next.js / TanStack Start / Vite / etc.]
**Clone Location:** [path to component file]

### What was cloned:
- [List sections]
- [X] screenshots captured
- [X] assets downloaded
- [X] iterations performed

### Output files:
- `[component path]` - The React component clone
- `public/images/` - Downloaded images
- `public/videos/` - Downloaded videos
- `public/icons/` - Downloaded icons/SVGs
- `${TASK_DIR}/context.md` - Extracted styles reference
- `${TASK_DIR}/screenshots/` - Visual references

### Tech Stack Used:
- React component (single file)
- Tailwind CSS (arbitrary values for exact matching)
- motion for animations

### Known limitations (if any):
- [List any unresolved issues]

### Next steps:
- Run `npm run dev` and navigate to /clone (or appropriate route)
- Modify content as needed
- Assets are in public/ folder
```

---

## Important Notes for Sub-Agents

When invoking each sub-agent, include these instructions:

1. **Always provide the full task folder path**
2. **Tell them to read context.md first if it exists**
3. **Remind them to update context.md with their output**
4. **Specify that they should use Playwright MCP for browser operations**
5. **Emphasize pixel-perfect accuracy is the goal**
6. **Remind cloner to use Tailwind CSS and motion (not framer-motion)**
7. **Assets go to public/ folder, not task folder**

---

## Error Handling

### If a sub-agent fails:
1. Note the error
2. Retry once with more specific instructions
3. If still failing, report to user with details

### If website requires authentication:
```
⚠️ This website requires authentication.
Cannot proceed with automated cloning.
```

### If website blocks automation:
```
⚠️ This website has bot protection.
Try using a different approach or manual capture.
```
