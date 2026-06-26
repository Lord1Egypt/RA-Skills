# UX Writing Reference

## Core Principles

### 1. Be Specific, Not Generic
Every UI text should answer: "What exactly will happen?"

| Context | ❌ Bad | ✅ Good |
|---------|--------|--------|
| Delete confirm | "Are you sure?" | "Delete 'Marketing Campaign 2024'? This can't be undone." |
| Button | "Submit" | "Send My Application" |
| Error | "Error occurred" | "Payment declined. Check your card details or try a different card." |
| Success | "Done!" | "Your video is being processed. We'll email you in ~3 minutes." |
| Loading | "Loading..." | "Generating your script... (usually takes 30 seconds)" |
| Empty state | "No data" | "No campaigns yet. Create your first campaign to start tracking results." |

### 2. Reduce Anxiety at Decision Points
Users pause before irreversible actions. Microcopy near CTAs resolves the hesitation.

**Patterns:**
- Near "Subscribe" → "Cancel anytime. No questions asked."
- Near "Delete" → make it a ghost button + specific copy
- Near "Connect Account" → "We only read your data. We never post."
- Near payment → "Secured by Stripe. Your card info never touches our servers."
- Near "Start Trial" → "No credit card required"

### 3. Active Voice, User-Centered
Frame copy from the user's perspective:

| ❌ System-centric | ✅ User-centric |
|------------------|----------------|
| "Your account has been created" | "You're in! Let's set up your workspace." |
| "Payment was processed" | "You're all set. Your credits are ready to use." |
| "An error has occurred" | "Something went wrong. Here's what you can try:" |

### 4. Microcopy Placement
Put the most important clarifying text **immediately adjacent** to the element it describes:
- Inline under an input (not in a separate help section)
- Directly below a CTA button (not in the footer)
- Inside the tooltip (not in a separate FAQ page)

### 5. Button Copy Formula
`[Verb] + [Object] + [Benefit/Timeframe]`

Examples:
- "Start Free Trial" (verb + free modifier)
- "Download Report" (verb + object)
- "Book Demo — 15 min" (verb + object + timeframe)
- "Create My First Video" (possessive makes it personal)

### 6. Error Message Formula
`[What happened] + [Why] + [What to do next]`

Examples:
- "Couldn't upload your file. Files must be under 10MB. [Choose a smaller file]"
- "We couldn't find that email. Double-check the spelling or [create a new account]."
- "Your session expired after 30 minutes of inactivity. [Log in again to continue]"

### 7. Empty State Formula
`[Illustration/Icon] + [What's missing] + [Value of filling it] + [Primary CTA] + [Secondary help link]`

Example:
```
🎬 (icon)
No videos yet
Your AI-generated videos will appear here.
[Create Your First Video]  [See how it works →]
```

## Tone & Voice Guidelines

### Match Tone to Context
- **Success states:** Celebratory, warm — "🎉 Your video is ready!"
- **Error states:** Calm, helpful — never apologize excessively
- **Warnings:** Direct, clear — "This will permanently delete your data"
- **Onboarding:** Encouraging, confident — "You're 2 steps away from your first video"
- **Empty states:** Inviting, not clinical — "Start something amazing →"

### Avoid These Patterns
- **Jargon:** "Authenticate your OAuth token" → "Connect your account"
- **Double negatives:** "Don't not enable notifications" → "Enable notifications"
- **Vague time:** "Soon" / "Shortly" → "In about 3 minutes" / "Within 24 hours"
- **Over-apologizing:** "We're so sorry..." → "Something went wrong. Let's fix it:"
- **All caps for emphasis:** Use bold or color instead

## Notification & Alert Copy

### Hierarchy of Alerts
1. **Error (red):** Something failed. User must act. → "Payment failed. Update your card."
2. **Warning (orange):** Something might go wrong. → "Your storage is 90% full."
3. **Info (blue):** Useful but not urgent. → "New AI model available for video generation."
4. **Success (green):** Positive confirmation. → "Changes saved."

### Alert Copy Rules
- One sentence max for inline alerts
- Include a link/action when the user can fix it
- Auto-dismiss success messages after 3–5 seconds
- Don't auto-dismiss errors — user needs to acknowledge

## Placeholder Text Best Practices

### Do
- Show the **format**: "john@company.com"
- Give an **example**: "e.g., A robot falls in love in 2087 Tokyo"
- Indicate **constraints**: "Max 280 characters"

### Don't
- Repeat the label: Label "Email" → Placeholder "Email" (redundant)
- Use placeholder as the only instruction (it disappears on type)
- Use placeholder for required format info — put that below the field permanently
