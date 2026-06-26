# Ethical Web Scraping Best Practices

## Core Principles

1. **Respect robots.txt** - Always check and honor robots.txt directives
2. **Rate limiting** - Add delays between requests to avoid overwhelming servers
3. **Identify yourself** - Use descriptive user agents
4. **Cache when possible** - Don't re-scrape data unnecessarily
5. **Monitor for errors** - Watch for rate limit responses and adjust behavior

## Rate Limiting Strategy

### Random Delays

Add 1-3 second random delays between page requests:

```javascript
// In workflow
await browser_wait_for({ time: Math.random() * 2 + 1 }); // 1-3 seconds
```

### Adaptive Rate Limiting

Monitor response codes and adjust delays:

- **200 OK**: Normal delay (1-3s)
- **429 Too Many Requests**: Back off exponentially (5s, 10s, 20s, etc.)
- **503 Service Unavailable**: Pause scraping, wait 60s, retry
- **403 Forbidden**: Stop scraping this domain immediately

### Domain-Specific Delays

Different domains may have different tolerance levels:

- **High-traffic sites** (Amazon, eBay): 3-5s delays minimum
- **Small sites**: 5-10s delays to be extra respectful
- **APIs with rate limits**: Follow documented limits exactly

## Detecting Rate Limiting

### HTTP Response Codes

Watch for these indicators:

- 429 Too Many Requests
- 503 Service Unavailable
- 403 Forbidden (may indicate blocking)

### Console Messages

Check browser console for:

- "Rate limit exceeded"
- "Too many requests"
- "Please slow down"
- Captcha challenges

### Page Content

Look for:

- Captcha pages
- "Access denied" messages
- Error pages when expecting content
- Missing expected elements

## User Agent Best Practices

Use descriptive user agents that identify your bot:

```
Mozilla/5.0 (compatible; MyBot/1.0; +https://example.com/bot-info)
```

Include:
- Bot name and version
- Contact URL or email
- Purpose if appropriate

## Respecting robots.txt

### Checking robots.txt

Before scraping, verify the URL is allowed:

```bash
# Use validate_urls.py script
python scripts/validate_urls.py urls.txt --user-agent "MyBot/1.0"
```

### Common Directives

```
User-agent: *
Disallow: /admin/        # Don't scrape admin pages
Disallow: /api/          # Don't scrape API endpoints
Crawl-delay: 5           # Wait 5 seconds between requests
```

## Error Handling

### Network Errors

- **Timeout**: Retry with exponential backoff (3 attempts max)
- **Connection refused**: Skip URL, log error
- **DNS failure**: Skip URL, may indicate blocking

### Content Errors

- **404 Not Found**: Log and skip
- **500 Server Error**: Retry once after delay
- **Empty response**: Log and skip

### Recovery Strategies

1. **Log failed URLs** to a separate file for manual review
2. **Resume capability** - Save progress periodically
3. **Graceful degradation** - Continue with remaining URLs if some fail

## Data Storage Ethics

- **Don't republish copyrighted content** without permission
- **Respect privacy** - Don't scrape personal information
- **Check terms of service** - Some sites prohibit scraping
- **Attribute sources** when using scraped data publicly

## Performance vs. Politeness

Balance efficiency with respect:

| Approach | Requests/min | Appropriate For |
|----------|--------------|-----------------|
| Aggressive | 20-60 | Never recommended |
| Moderate | 10-20 | High-traffic sites with permission |
| Polite | 6-12 | Standard scraping (5-10s delays) |
| Very polite | 2-6 | Small sites, first-time scraping |

**Default recommendation**: Start with "Polite" and adjust based on site response.

## Monitoring Your Scraper

Track these metrics during execution:

- **Success rate** - Percentage of successful page loads
- **Error distribution** - Count by error type
- **Average response time** - Detect slowdowns
- **Rate limit hits** - Count of 429/503 responses
- **Data quality** - Percentage of pages with expected content

Stop scraping if:
- Success rate drops below 80%
- Multiple 429/503 responses in a row
- Console shows blocking messages
- Response times increase significantly
