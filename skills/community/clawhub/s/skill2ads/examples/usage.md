# Usage Examples

## Basic: Generate ads from a website

```
User: Generate ads for https://sarahsbakery.com

Agent: I'll scrape the website and generate brand-matched ads for you.

[Scraping https://sarahsbakery.com... 3 pages crawled]
[Analyzing brand... Sarah's Bakery | Voice: warm and community-driven]
[Generating 5 ad variants...]

Here are 5 Instagram ad variants for Sarah's Bakery:

1. **"Your Sourdough Alarm Clock"**
   Wake up to the smell of fresh sourdough — order by 8pm, warm loaf by 7am.
   CTA: Order Tonight →
   Schedule: 6:00-8:30 AM weekdays (wake scroll)

2. **"The Bread Your Neighborhood Talks About"**
   3,000+ loaves delivered this month. Your neighbors already know.
   CTA: Try Us This Week →
   Schedule: 8:30-10:30 PM Mon-Thu (evening wind-down)

...
```

## With platform and budget

```
User: Generate Facebook ads for https://cocacola.com with a $500/week budget

Agent: [Scraping... Analyzing... Generating...]

Brand detected: Coca-Cola | Voice: optimistic, youthful, universal
Geographic focus: Global
5 Facebook ad variants generated with $500/week budget optimization.
```

## Scrape only (for inspection)

```
User: Just scrape https://example.com so I can see the content

Agent: [Uses scrape_website tool]
Scraped 3 pages from example.com:
- Homepage: 2,400 words
- About: 1,100 words  
- Products: 1,800 words
```

## Two-step: Scrape then generate with edits

```
User: Scrape my site https://mycoach.com

Agent: [Scrapes site, shows content summary]

User: Good, but focus the ads on my executive coaching, not the group programs

Agent: [Uses generate_ads with filtered content, emphasizing executive coaching]
```
