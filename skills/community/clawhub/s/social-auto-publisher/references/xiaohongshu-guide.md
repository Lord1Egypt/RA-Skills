# Xiaohongshu Complete Operations Guide

## Platform Characteristics

| Attribute | Description |
|-----------|-------------|
| User Profile | 70% female, predominantly 18-35 years old, Tier 1 & 2 cities |
| Content Format | Image-text posts (mainstream), video posts |
| Distribution Mechanism | Tag matching → Small-scale testing → Expanded recommendation if data performs well |
| Best Publishing Time | 07:00-09:00, 12:00-14:00, 18:00-22:00 |

## Content Creation Standards

### Title Formulas
- Number + Keyword + Pain point / Benefit
- 15-20 characters is optimal
- Example: `✅ This is how you dress in spring! 158cm petite frame looks 10cm taller`
- Example: `💡 3 AI tools that save me 2 extra hours every day`

### Body Structure
1. **Opening (first 3 sentences)**: Grab attention, highlight a pain point or spark curiosity
2. **Main Body**: Discuss points separately, each accompanied by an emoji
3. **Closing**: Lead engagement + Call to action

### Hashtag Strategy
- High-traffic keywords (1-2): `#AI` `#ProductivityTools` `#Outfit`
- Precise long-tail keywords (3-5): `#AIWritingTools` `#PetiteStyleTips`
- Brand / Topic keywords (1-2): `#MyDisciplinedLife` `#CreatorDaily`

## Image Requirements

- Dimensions: 3:4 portrait (1080×1440)
- Quantity: 6-9 images is optimal
- Cover Image: Must include a text title so the topic is identifiable at a glance
- Style: Consistent color palette; Xiaohongshu aesthetic (bright, warm, lifestyle feel)

## Compliance Red Lines

❌ Absolute terms: best, number one, only, 100%
❌ Medical efficacy claims: cure, treat, therapeutic effect
❌ Price inducements: original price xxx, now xxx; flash sale
❌ False advertising: exaggerated effects, fabricated data
❌ Inducement behaviors: add WeChat, scan QR code, DM to receive

## Browser Operation Quick Reference

```bash
# Open the Creator Platform
browser navigate https://creator.xiaohongshu.com/publish/publish

# Get a page snapshot
browser snapshot refs=aria

# Take a screenshot of the current state
browser screenshot

# Click an element
browser act ref=<element-ref> kind=click

# Type text
browser act ref=<input-ref> kind=type text="Content"

# Upload an image
browser act ref=<upload-button-ref> kind=click
```

## Post-Publishing Operations

- **Within 24 hours**: Check basic metrics (impressions, clicks, engagement)
- **Within 48 hours**: Reply to all comments; observe data trends
- **After 72 hours**: Determine whether the post has entered a larger traffic pool
- **One week later**: Summarize and review; optimize the next post