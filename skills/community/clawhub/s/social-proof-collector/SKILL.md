# Social Proof Collector Skill

Automatically collect, organize, and display customer reviews and testimonials from across the web.

## What This Skill Does

1. **Scrape Reviews** — Pull reviews from Google, Yelp, Facebook, Trustpilot, G2, Capterra
2. **Filter & Rank** — Surface the best testimonials (4-5 stars, keyword-rich)
3. **Format for Display** — Generate embed-ready HTML widgets, social media graphics, or email snippets
4. **Monitor New Reviews** — Alert when new reviews are posted
5. **Respond to Reviews** — Draft professional responses to both positive and negative reviews

## Usage

### Collect Reviews
```
Collect reviews for [business name] from Google and Yelp
```

### Generate Testimonial Widget
```
Create a testimonial carousel from our top 5 reviews
```

### Monitor & Alert
```
Check for new reviews daily and alert me if any are below 3 stars
```

## Workflow

### Step 1: Discovery
Search for the business across review platforms:
- Google Business Profile
- Yelp
- Facebook Reviews
- Industry-specific (Trustpilot, G2, Capterra, Houzz, Avvo, etc.)

### Step 2: Extraction
For each platform, extract:
- Reviewer name
- Star rating
- Review text
- Date posted
- Platform source

### Step 3: Scoring
Score each review by usefulness:
- Star rating (4-5 = high)
- Length (50+ words = more credible)
- Keyword relevance (mentions specific services/results)
- Recency (last 6 months preferred)
- Sentiment analysis

### Step 4: Output Formats

**HTML Widget:**
```html
<div class="testimonial">
  <div class="stars">★★★★★</div>
  <p class="quote">"[review text]"</p>
  <p class="author">— [name], [platform]</p>
</div>
```

**Social Media Post:**
```
🌟 What our clients say:

"[best quote from review]"
— [Name]

[Your CTA + link]
```

**Email Signature Snippet:**
```
⭐⭐⭐⭐⭐ Rated 4.8/5 on Google (150+ reviews)
```

### Step 5: Review Response Drafts
For negative reviews, generate empathetic, professional responses:
- Acknowledge the concern
- Apologize without admitting fault
- Offer to resolve offline
- Keep it under 100 words

## Configuration
```json
{
  "business_name": "Your Business",
  "platforms": ["google", "yelp", "facebook"],
  "min_stars": 4,
  "alert_below": 3,
  "check_frequency": "daily"
}
```

## Requirements
- Brave Search API (for scraping public reviews)
- OpenClaw with web search capability
- Optional: notification channel for alerts
