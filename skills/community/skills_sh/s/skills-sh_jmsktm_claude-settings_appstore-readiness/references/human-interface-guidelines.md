# Human Interface Guidelines (iOS) — Reference

**Official URL:** https://developer.apple.com/design/human-interface-guidelines/

This document covers the essential iOS Human Interface Guidelines that affect App Store approval and user experience quality.

---

## Core Design Principles

### The Three Pillars

| Principle | Meaning | Implementation |
|-----------|---------|----------------|
| **Clarity** | Text is legible at every size, icons are precise and lucid, adornments are subtle and appropriate | Use SF Pro or SF Compact, proper contrast ratios, clear iconography |
| **Deference** | Fluid motion and a crisp, beautiful interface help people understand and interact with content while never competing with it | Content-first design, minimal chrome, purposeful motion |
| **Depth** | Distinct visual layers and realistic motion impart vitality and heighten people's delight and understanding | Proper use of materials, shadows, and hierarchy |

---

## Designing for iOS

### Device Characteristics

| Aspect | iOS Behavior |
|--------|--------------|
| **Display** | Medium-size, high-resolution |
| **Ergonomics** | One or both hands, portrait/landscape switching |
| **Inputs** | Multi-Touch gestures, virtual keyboards, voice control, pencil |
| **Interactions** | Brief (1-2 min) to extended (1+ hour) sessions |

### Best Practices

1. **Limit onscreen controls** — Focus on primary tasks/content, not UI chrome
2. **Adapt to appearance changes** — Support device orientation, Dark Mode, Dynamic Type
3. **Support comfortable interactions** — Controls in middle/bottom of display are easier to reach
4. **Integrate platform capabilities** — Payments, biometric auth, location (with permission)

---

## Navigation Patterns

### Tab Bar

| Requirement | Details |
|-------------|---------|
| **Item count** | 2-5 tabs (more requires "More" tab) |
| **Purpose** | Top-level navigation between parallel sections |
| **NOT for** | Actions, modal operations, single-use functions |
| **Position** | Bottom of screen, always visible |
| **Icons** | Filled = selected, outline = unselected |

### Navigation Bar

| Requirement | Details |
|-------------|---------|
| **Back button** | Left side, must return to previous screen |
| **Title** | Center, describes current content |
| **Actions** | Right side, contextual actions |
| **Behavior** | Shows hierarchy, enables back navigation |

### Modal Presentations

| Use Case | When Appropriate |
|----------|------------------|
| **Full screen** | Immersive tasks, content creation |
| **Sheet** | Focused tasks that require dismissal |
| **Popover** | iPad, additional options without navigation |
| **Alert** | Critical information requiring acknowledgment |

**Sheet Height Options:**
- `.medium` — Half screen
- `.large` — Full screen
- Custom detents available

---

## Controls and Interactions

### Touch Targets

| Requirement | Minimum Size |
|-------------|--------------|
| **Tappable elements** | 44pt × 44pt minimum |
| **Buttons** | 44pt height recommended |
| **List rows** | 44pt height minimum |
| **Interactive areas** | Include padding around visual element |

### Button Styles

| Style | Use Case |
|-------|----------|
| **Filled** | Primary actions |
| **Tinted** | Secondary actions |
| **Gray** | Tertiary/destructive |
| **Plain** | In-content links |
| **Bordered** | Less emphasis than filled |

### Form Inputs

| Element | Best Practice |
|---------|---------------|
| **Text fields** | Clear label, placeholder text, appropriate keyboard |
| **Pickers** | Native pickers for dates, times, selections |
| **Toggles** | For binary on/off states |
| **Steppers** | For small numeric adjustments |
| **Sliders** | For continuous value ranges |

---

## Typography

### System Fonts

| Font | Use Case |
|------|----------|
| **SF Pro** | iOS default |
| **SF Compact** | Apple Watch, widgets |
| **SF Mono** | Code, monospace content |
| **SF Symbols** | Icons and symbols |

### Text Styles (Dynamic Type)

| Style | Purpose |
|-------|---------|
| **Large Title** | Screen titles, navigation |
| **Title 1-3** | Section headers |
| **Headline** | Important information |
| **Body** | Main content |
| **Callout** | Secondary content |
| **Subhead** | Tertiary content |
| **Footnote** | Fine print, captions |
| **Caption 1-2** | Labels, metadata |

### Dynamic Type Requirements

- **Must support** text scaling from accessibility settings
- **Use system text styles** or custom styles with proper scaling
- **Test at all sizes** — especially largest accessibility sizes
- **Don't clip text** — allow multiline or truncation

---

## Color

### System Colors

| Category | Examples |
|----------|----------|
| **Label** | `.label`, `.secondaryLabel`, `.tertiaryLabel`, `.quaternaryLabel` |
| **Fill** | `.systemFill`, `.secondarySystemFill`, `.tertiarySystemFill` |
| **Background** | `.systemBackground`, `.secondarySystemBackground`, `.tertiarySystemBackground` |
| **Tint** | App accent color, adaptable to Dark Mode |

### Color Requirements

| Requirement | Details |
|-------------|---------|
| **Contrast ratios** | 4.5:1 for normal text, 3:1 for large text |
| **Dark Mode support** | Colors must adapt or use semantic colors |
| **Color blindness** | Don't rely solely on color to convey information |
| **System integration** | Respect user's accent color preferences |

---

## Dark Mode

### Requirements

| Aspect | Light Mode | Dark Mode |
|--------|------------|-----------|
| **Background** | Light colors | Dark colors |
| **Text** | Dark colors | Light colors |
| **Images** | Standard | May need adjustment |
| **Icons** | Standard | May need light variant |
| **Elevation** | Shadows | Lighter backgrounds |

### Implementation

- Use semantic colors (`.label`, `.systemBackground`)
- Provide asset variants for both appearances
- Test all screens in both modes
- Don't use pure black backgrounds (use `.systemBackground`)
- Increase elevation with lighter tones, not shadows

---

## Accessibility

### Required Support

| Feature | Requirement |
|---------|-------------|
| **VoiceOver** | All interactive elements must be accessible |
| **Dynamic Type** | Text must scale with user preferences |
| **Reduce Motion** | Provide alternatives to complex animations |
| **Color** | Don't rely solely on color for meaning |
| **Touch Accommodations** | Respect user's touch settings |

### VoiceOver Best Practices

- Provide meaningful accessibility labels
- Use accessibility hints for additional context
- Group related elements with accessibility containers
- Ensure logical reading order
- Test with VoiceOver enabled

### Reduce Motion

When user enables Reduce Motion:
- Replace complex animations with fades or crossfades
- Reduce parallax effects
- Limit auto-playing video/animation
- Provide static alternatives

---

## Layout

### Safe Areas

| Area | Requirement |
|------|-------------|
| **Top safe area** | Account for notch, Dynamic Island |
| **Bottom safe area** | Account for Home indicator |
| **Keyboard** | Adjust layout when keyboard appears |
| **Navigation elements** | Don't overlap with system UI |

### Orientation

| Orientation | When to Support |
|-------------|-----------------|
| **Portrait only** | Simple utilities, messaging apps |
| **Landscape only** | Games, video players |
| **Both** | Most apps (recommended) |

### Size Classes

| Size Class | Devices |
|------------|---------|
| **Compact width** | iPhone portrait, split-screen secondary |
| **Regular width** | iPad, iPhone landscape, split-screen primary |
| **Compact height** | iPhone landscape |
| **Regular height** | iPhone portrait, iPad |

---

## Icons and Images

### App Icon Requirements

| Platform | Size | Notes |
|----------|------|-------|
| **App Store** | 1024×1024 pt | Required, no transparency |
| **iPhone** | Multiple sizes | Auto-generated from 1024 |
| **iPad** | Multiple sizes | Auto-generated from 1024 |

### SF Symbols

- Use SF Symbols for system-consistent iconography
- Over 4,000 symbols available
- Automatically scale with Dynamic Type
- Support multiple rendering modes (monochrome, hierarchical, palette, multicolor)

### Image Requirements

- Provide @1x, @2x, @3x assets
- Use vector assets when possible
- Support Dark Mode variants
- Consider memory usage for large images

---

## Gestures

### Standard Gestures

| Gesture | System Behavior |
|---------|-----------------|
| **Tap** | Activate control |
| **Drag** | Scroll, move, adjust |
| **Swipe** | Navigate, delete (swipe actions) |
| **Pinch** | Zoom in/out |
| **Rotate** | Rotate content |
| **Long press** | Context menu, edit mode |
| **Edge swipe** | Back navigation (left edge) |

### Custom Gestures

- Don't override system gestures
- Provide discoverable alternatives
- Support standard gestures for standard actions
- Test with all input methods (touch, pencil, trackpad)

---

## Common HIG Violations That Cause Rejection

| Violation | Fix |
|-----------|-----|
| Tab bar used for actions | Use toolbar instead |
| Non-standard back navigation | Use system back button |
| Touch targets under 44pt | Increase tap area |
| No Dynamic Type support | Implement text scaling |
| Dark Mode not supported | Add dark appearance assets |
| Custom gestures override system | Use different gesture or location |
| Inaccessible UI | Add accessibility labels, VoiceOver support |
| Text clipped at large sizes | Use multiline or scrolling |

---

## Specific Component Guidelines

### In-App Purchase Design

| Requirement | Details |
|-------------|---------|
| **Experience first** | Let people use app before purchase |
| **Integrated shopping** | Not jarring or separate from app |
| **Simple names** | Clear product names |
| **Price prominence** | Total billing price most prominent |
| **Context** | Only show store when payments can be made |
| **Confirmation** | Use default confirmation sheet |

### Subscription Sign-Up Screen

**Must include:**
- Subscription name and duration
- Content/services provided during subscription
- **Full renewal price (most prominent element)**
- Localized pricing
- Sign in / restore purchases option
- Terms of Service link
- Privacy Policy link

---

*HIG updated regularly. Always verify against current Apple documentation.*
