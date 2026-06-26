# UX Laws & Principles Reference

## Jakob's Law
> Users spend most of their time on other sites. They expect your site to work like sites they already know.

**Apply:**
- Follow established UI conventions (hamburger menu, logo top-left, search top-right)
- Don't reinvent interaction patterns without a compelling reason
- Social login at top matches user expectations from other platforms
- Navigation patterns: consistent with platform norms (iOS vs Android vs Web)

---

# Original Laws

## Fitts's Law
> The time to acquire a target is a function of the distance to and size of the target.

**Practical applications:**
- Place keyboard shortcuts next to the action they trigger (reduces memory load + distance)
- Make primary CTAs large and centrally positioned
- Place frequently used actions in thumb zones on mobile
- Navigation items placed at corners and edges are easiest to hit

## The Gutenberg Principle (Z-Pattern Layout)
Users' eyes naturally travel in a Z-shape:
1. Top-left (start)
2. Top-right
3. Bottom-left
4. Bottom-right (terminal area = best CTA placement)

**Apply:** Place the primary CTA at the terminal area (bottom-right of the Z-path). Don't fight natural eye movement.

## Hick's Law
> The time it takes to make a decision increases with the number and complexity of choices.

**Apply:**
- Limit menu items
- Highlight the recommended pricing plan to reduce decision paralysis
- Use one primary CTA per screen — multiple competing CTAs slow conversion

## Jakob's Law
> Users spend most of their time on other sites. They expect your site to work like sites they already know.

**Apply:**
- Don't reinvent navigation patterns without strong reason
- Social login at top matches user expectations from other platforms
- Follow platform conventions (back buttons, form layouts, etc.)

## Von Restorff Effect (Isolation Effect)
> Items that stand out are more likely to be remembered and noticed.

**Apply:**
- Highlight the best pricing plan with color + shadow + size (multiple attributes)
- Use brand color sparingly so highlighted elements truly pop
- Make selected states clearly distinct

## Miller's Law
> The average person can hold 7 (±2) items in working memory.

**Apply:**
- Keep navigation menus under 7 items
- Break long forms into steps
- Group related elements to reduce cognitive load

## Tesler's Law (Conservation of Complexity)
> Every application has an inherent amount of complexity that cannot be removed — only shifted.

**Apply:**
- Better to absorb complexity in the system than push it to users
- Pre-made templates in empty states absorb the complexity of starting from scratch
- Smart defaults reduce decisions users must make

## Color Accessibility (8-3-0 Rule)
- ~8% of men have color vision deficiency
- ~0.5% of women have color vision deficiency
- **Never use color as the only differentiator** — always pair with icon, shape, or label

## Type Scale System
Standard scale multiplier: **×1.25**

| Element | Example Size |
|---------|-------------|
| H1 Title | 40px |
| H2 Subtitle | 32px |
| H3 | 25.6px |
| Body | 16px |
| Small/Label | 12.8px |

Consistent scale creates automatic hierarchy without manual tuning.

## Line Width for Readability
- Optimal: **50–75 characters per line** (approximately 500–700px)
- CSS shortcut: `max-width: 65ch` (ch = width of "0" character)
- Too wide → eyes lose track when returning to next line
- Too narrow → choppy reading rhythm

## Padding Rules for Rounded Elements
- When inner element is round and outer container is rounded:
  `Outer Border Radius = 2 × Inner Border Radius`
- When edge element is NOT round (text, icon):
  Use **double padding** on that edge vs. the rounded side

## Social Login Best Practices
- Place social login **above** email/password (higher conversion)
- Always provide email/password fallback (privacy-conscious users avoid social login)
- Display social options prominently with recognizable brand colors + logos

## Deletion Validation Checklist
- [ ] Confirmation dialog or inline confirmation required
- [ ] Button copy describes specific action ("Delete 'Project Alpha'", not "Delete")
- [ ] Dangerous action visually de-emphasized (ghost button, warning color)
- [ ] Consider undo functionality as alternative to confirmation
- [ ] Never style delete button as primary action

---

## Peak-End Rule
> People judge an experience by its most intense point (peak) and how it ends — not the average.

**Apply:**
- Make the success moment (after completing a task) celebratory — "🎉 Your video is ready!"
- Fix the worst friction points in your flow (peak pain = peak memory)
- End onboarding with a win, not a form
- The last interaction before churn matters most — make it positive

## Doherty Threshold
> Productivity soars when a computer and user interact at a pace < 400ms.

**Apply:**
- Show loading states immediately (skeleton screens, not spinners)
- Give instant visual feedback on button clicks (pressed state, loading state)
- Optimistic UI updates (assume success, rollback on failure)
- Progress bars reduce perceived wait time even if they don't speed anything up

## Parkinson's Law
> Work expands to fill the time available.

**Apply:**
- Set deadlines in copy: "Your free trial ends in 3 days"
- Time-limited offers (real ones, not fake countdown timers)
- Break tasks into smaller pieces with their own deadlines

## Aesthetic-Usability Effect
> Users perceive aesthetically pleasing designs as easier to use.

**Apply:**
- Good visual design buys tolerance for usability issues
- Polish matters — rough-looking UIs get less patience from users
- Consistent spacing, typography, and color = perceived quality

## Serial Position Effect
> Users best remember the first and last items in a list.

**Apply:**
- Put your most important navigation items first or last
- Feature your strongest testimonial first AND last
- Key pricing benefits at the top and bottom of feature lists

## Goal-Gradient Effect
> People accelerate effort as they get closer to a goal.

**Apply:**
- Show progress bars even for simple tasks ("Profile 60% complete")
- Pre-fill some progress: "You've already done step 1!" for new users
- Break long forms into labeled steps with visible completion status

## Law of Proximity
> Objects near each other are perceived as related.

**Apply:**
- Group form fields by category (personal info, billing info)
- Labels must be closer to their input than to other inputs
- Action buttons near the content they affect (not in a distant footer)

## Law of Similarity
> Similar items are perceived as belonging together.

**Apply:**
- Same visual style for same-level navigation items
- Tags should look different from primary buttons
- Distinguish interactive from non-interactive elements visually
