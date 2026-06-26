# Screenshot Creation Workflow

## Phase 1: Project Setup

### Create Project Folder
```
mkdir -p ~/screenshots/{app-slug}/raw
cd ~/screenshots/{app-slug}
```

### Create Config
Write `config.md`:
```markdown
# {App Name} Screenshots

## Brand
- **Primary color:** #XXXXXX
- **Secondary color:** #XXXXXX
- **Font:** {Font name}

## Style
- **Background:** gradient | solid | image
- **Device frame:** with-frame | frameless | floating
- **Text position:** top | bottom | overlay

## Target Stores
- [ ] App Store
- [ ] Google Play

## Languages
- [ ] English
- [ ] Spanish
- [ ] ...
```

---

## Phase 2: Raw Capture

### Simulator Screenshots (Recommended)
1. Run app in iPhone 15 Pro Max simulator (highest res)
2. Capture key screens: `Cmd + S` or `xcrun simctl io booted screenshot`
3. Name clearly: `01-home.png`, `02-feature-x.png`

### Device Screenshots
1. Use highest-resolution device available
2. Clear notifications, use clean status bar
3. Use fake time (Settings > Developer > Status Bar)

### What to Capture
- Home/main screen
- 3-4 key features in action
- Empty states (if compelling)
- Onboarding highlights
- Any "wow" moments

---

## Phase 3: Size Generation

### Process
1. Start with highest resolution raw capture
2. For each target size (per `specs.md`):
   - Scale proportionally
   - Handle aspect ratio difference (letterbox or crop)
   - Verify text remains readable

### Output Structure
```
~/screenshots/{app-slug}/v1/
├── ios/
│   ├── 6.7/
│   │   ├── en/
│   │   │   ├── 01-home.png
│   │   │   └── ...
│   │   └── es/
│   │       └── ...
│   ├── 6.5/
│   └── 5.5/
└── android/
    └── phone/
```

---

## Phase 4: Visual Polish

### Apply Template
1. Select template from `templates.md` based on app category
2. Create background using brand colors
3. Add device frame if specified in config
4. Position text overlays

### Add Marketing Elements
1. Write headlines per `text-style.md`
2. Position in safe zones
3. Ensure thumbnail readability

### Consistency Pass
- Same font across all screenshots
- Same text position pattern
- Same device frame style
- Color palette matches throughout

---

## Phase 5: Quality Review

### Vision Model Check
Before presenting to user, verify with vision:
1. "Is all text readable at 150px width?"
2. "Are there any visual inconsistencies?"
3. "Does anything look unprofessional?"

### Manual Checklist
- [ ] No debug/placeholder text visible
- [ ] Status bar looks realistic
- [ ] No sensitive data visible
- [ ] All required sizes generated
- [ ] Localized versions match layout

---

## Phase 6: User Review

### Presentation
Show all screenshots in context:
- "Here's your App Store set"
- Side-by-side comparison if requested
- Note any concerns proactively

### Iteration Handling
When user requests changes:
1. Clarify scope: "Just this screenshot or all?"
2. Make changes
3. Regenerate affected sizes
4. Re-run quality checks

### Approval
Once approved:
- Symlink `latest` to current version
- Note in version log what was approved

---

## Phase 7: Export & Delivery

### File Naming
App Store Connect expects:
- Sequential or descriptive names
- Uploaded in order shown in store

Play Console:
- Less strict, but consistent naming helps

### Packaging
Create delivery folder:
```
delivery-YYYY-MM-DD/
├── app-store/
│   ├── 6.7-inch/
│   ├── 6.5-inch/
│   └── ipad-12.9/
└── play-store/
    └── phone/
```

### Handoff
Provide user with:
1. Organized folders ready for upload
2. Preview HTML/PDF if multiple variants
3. Notes on which is which (for A/B tests)

---

## Ongoing: Updates

When app UI changes:
1. Get new raw captures
2. Reuse existing `config.md` and templates
3. Create new version folder `v{n+1}`
4. Run same pipeline
5. Compare to previous version

Keep old versions for rollback.
