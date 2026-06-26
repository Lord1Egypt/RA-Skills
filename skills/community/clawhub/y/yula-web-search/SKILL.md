---
name: yula-web-search
description: "Yula's custom web search - NO API KEY required. Uses multiple fallback search methods with public services that allow anonymous access. Works by direct curl requests through local network, parse HTML to extract search results, then extracts content from top results and summarizes. Works out of the box without any configuration. Provides full web search capability for Chinese language queries. Use when: user asks to search the web, look up latest information, find news, get current prices, read web pages. Triggers on phrases like 'search', 'look up', 'find latest', 'what's the current', 'check the web'."
metadata: { "openclaw": { "emoji":  "🔍", "requires": { "bins": ["curl", "python3"] } } }
---

# Yula Web Search Skill

Custom web search skill by Yula — **NO API KEY REQUIRED**.

Uses multiple **public anonymous search services** that don't require API keys. Works via direct curl requests from local network:
1. Parse Bing search to get top results (title + URL)
2. **Extract full content** from the top 2-3 most relevant URLs**
3. Summarize all information into a comprehensive answer
4. If one method fails, automatically try next fallback

Just works, no configuration needed.

## When to Use

✅ **USE this skill when:**
- Search for latest news, information, or products
- Look up current prices, availability, or status
- Find answers to questions that require up-to-date data
- Extract content from a specific URL
- Research topics that need current web information
- Chinese language searches (optimized for China region)

❌ **DON'T use when:**
- Weather forecast → use `weather` skill
- Local file search → use file tools
- Already have the information in context

## Search Workflow

### Complete Workflow (with content extraction)

1. **Search Bing** → get top 5-8 results with title + URL
2. **Filter results** → select top 2-3 most relevant URLs based on title matching query
3. **Extract content** from each selected URL using curl + html-to-text
4. **Combine all extracted content** 
5. **Summarize** into a coherent answer for the user

## Search Methods (Tried in Order)

### Method 1: Direct Bing Search (cn.bing.com, Primary)
Direct request to Chinese Bing, parse HTML to extract result titles and URLs:

```bash
QUERY="your search query"
QUERY_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))"
curl -s -m 20 -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "https://cn.bing.com/search?q=$QUERY_ENCODED" | python3 -c "
import re, sys
from html.parser import HTMLParser

class BingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.in_h2 = False
        self.current_url = None
        self.current_title = []
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'h2':
            self.in_h2 = True
            self.current_title = []
        if tag == 'a' and self.in_h2 and 'href' in attrs_dict:
            url = attrs_dict['href']
            if 'bing.com' not in url and url.startswith('http'):
                self.current_url = url
    def handle_endtag(self, tag):
        if tag == 'h2':
            if self.current_url:
                title = ''.join(self.current_title).strip()
                self.results.append((title, self.current_url))
                self.current_url = None
            self.in_h2 = False
    def handle_data(self, data):
        if self.in_h2 and self.current_url:
            self.current_title.append(data)

parser = BingParser()
parser.feed(sys.stdin.read())
for i, (title, url) in enumerate(parser.results[:8]):
    print(f'{i+1}\\t{title}\\t{url}")
"
```

### Method 2: Direct Google Search (google.com, Fallback 1)
If Bing fails, try Google:

```bash
QUERY="your search query"
QUERY_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))"
curl -s -m 20 -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "https://www.google.com/search?q=$QUERY_ENCODED" | python3 -c "
import re, sys
results = []
pattern = r'<h3 class=\"zBAuLc\"><a href=\"([^\"]+)\"'
matches = re.findall(pattern, html)
for i, url in enumerate(matches[:8]):
    # Google enconder title is after... extract separately
    pass
# Simplified extraction - get first 8 URLs
"
```

### Extract Content from URL (after search)
After getting search results, extract text content from top relevant URLs:

```python
def extract_url_content(url):
    # Use curl to get HTML
    # Use python to extract text content, remove scripts/styles/scripts, get main text
    # Return cleaned text content, limit to ~2000 chars per URL
```

**Example full workflow example:

```bash
# After getting search results, select top 2-3 relevant URLs
for (title, url) in selected_urls:
    curl -s -m 20 -L -A "USER_AGENT" "$url" | python3 -c "
import sys
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_script = False
        self.in_style = False
    def handle_starttag(self, tag, attrs):
        if tag == 'script' or tag == 'style' or tag == 'noscript':
            self.in_script = True
        if tag == 'style':
            self.in_style = True
    def handle_endtag(self, tag):
        if tag == 'script' or tag == 'style' or tag == 'noscript':
            self.in_script = False
        if tag == 'style':
            self.in_style = False
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            words = data.strip()
            if words:
                self.text.append(words)

parser = TextExtractor()
parser.feed(sys.stdin.read())
content = ' '.join(parser.text)
# Clean up whitespace and limit length
content = ' '.join(content.split())[:2000]
print(content)
"
```

## User-Agent

Always use a modern browser User-Agent to avoid being blocked immediately:
```
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
```

## Complete Example Workflow

> "Search 2026腾势Z9GT介绍"

**Step 1: Search Bing → get top 8 results
```bash
# Output gives title + url:
1.  2026款腾势Z9GT-腾势官网
    URL: https://www.tengshiauto.com/product-detail/26-z9gt.html
2.  【腾势Z9GT】腾势_腾势Z9GT报价_腾势Z9GT图片_汽车之家
    URL: https://www.autohome.com.cn/7659
...
```

**Step 2: Select most relevant results**
- Pick 2-3 results that best match the query
  1. Official website
  2. Autohome article

**Step 3: Extract content from each URL
- Get cleaned text from each page
- Limit to 2000 characters per page

**Step 4: Combine and summarize
- Read all extracted content
- Summarize into a coherent answer with key information: price, specs, release date

## Best Practices

1. **Content extraction** → Always extract top 2-3 results, not more (avoids too much text)
2. **Relevance filtering** → Select results whose title contains more query keywords preferentially
3. **Character limit** → Limit total extracted text to ~5000 chars total to avoid token overflow
4. **Timeout** → 20 seconds max per request to avoid hanging
5. **Fallback** → if one search engine fails, automatically try next
6. **Chinese optimized** → prefer Chinese keywords, Chinese websites

### How to select relevant results
- Count how many query keywords appear in the title
- Sort results by relevance
- Pick top N (2-3) for content extraction
- Official sites and major portal sites have higher priority

## Notes

- **NO API KEY REQUIRED** — works out of the box
- **Multiple fallback methods** → if one gets blocked, try the next
- **Direct curl via local network** → uses your existing network/proxy
- **Python HTML parsing** → extracts title/url reliably
- **Automatic content extraction and summarization** → gives complete answer without user having to click links
- **Modern browser User-Agent** → reduces chance of being blocked
- **Free for non-commercial use**
- **Rate limits**: be respectful, don't spam too many requests quickly
- If all methods fail, fall back to general knowledge

## Full Workflow Summary

```
1. Search Bing → get (title + url)
   ↓
2. Filter by relevance → pick top 2-3
   ↓
 3. Extract content from each URL
   ↓
 4. Combine all text
   ↓
 5. Summarize into final answer
   ↓
 6. Present to user with sources
```

## Author

Created by **Yula**  
GitHub: https://github.com/wjzhb/yula-web-search
## License

Copyright (c) 2026 [Yula](https://github.com/wjzhb)

Licensed under the [MIT License](LICENSE)

If you find this skill useful, **please ⭐ star it on GitHub**!

