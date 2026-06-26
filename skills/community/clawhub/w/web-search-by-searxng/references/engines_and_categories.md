# SearXNG Engines and Categories Reference

## Categories (Tabs)

SearXNG organizes engines into categories (displayed as tabs in UI). Categories not listed can still be searched using search syntax.

| Category | Description | Bang Prefix |
|----------|-------------|-------------|
| `general` | General web search | `!general` |
| `images` | Image search | `!images` |
| `videos` | Video search | `!videos` |
| `news` | News articles | `!news` |
| `map` | Maps and locations | `!map` |
| `music` | Music and audio | `!music` |
| `it` | IT/Technology resources | `!it` |
| `science` | Scientific publications | `!science` |
| `files` | Files and torrents | `!files` |
| `social_media` | Social media content | `!social_media` |

## Using Categories and Engines in API

### Category Selection
Use the `categories` parameter with comma-separated values:
```
categories=general,news
```

### Engine Selection
Use the `engines` parameter with comma-separated engine names:
```
engines=google,duckduckgo,wikipedia
```

Or use bang syntax in the query:
```
q=!google+python+tutorial
q=!wp+artificial+intelligence
```

## Common Engines by Category

### General (`!general`)

| Engine | Bang | Features |
|--------|------|----------|
| Google | `!go` | Paging, Locale, Safe search, Time range |
| DuckDuckGo | `!ddg` | Paging, Locale, Safe search, Time range |
| Brave | `!br` | Paging, Locale, Safe search, Time range |
| Startpage | `!sp` | Paging, Locale, Safe search, Time range |
| Bing | `!bi` | Paging, Locale, Safe search, Time range |
| Wikipedia | `!wp` | Locale |
| Wikidata | `!wd` | Locale |
| Baidu | `!bd` | Paging, Time range (Chinese) |
| Naver | `!nvr` | Paging, Time range (Korean) |

### Images (`!images`)

| Engine | Bang | Features |
|--------|------|----------|
| Google Images | `!goi` | Paging, Locale, Safe search, Time range |
| Bing Images | `!bii` | Paging, Locale, Safe search, Time range |
| DuckDuckGo Images | `!ddi` | Paging, Locale, Safe search |
| Unsplash | `!us` | - |
| Flickr | `!fl` | Paging, Time range |
| Pexels | `!pe` | Paging, Time range |
| Pixabay | `!pixi` | Paging, Safe search, Time range |

### Videos (`!videos`)

| Engine | Bang | Features |
|--------|------|----------|
| YouTube | `!yt` | Paging, Time range |
| Google Videos | `!gov` | Paging, Locale, Safe search, Time range |
| Bing Videos | `!biv` | Paging, Locale, Safe search, Time range |
| Dailymotion | `!dm` | Paging, Locale, Safe search, Time range |
| Vimeo | `!vm` | Paging |
| Bilibili | `!bil` | Paging (Chinese) |
| Niconico | `!nico` | Paging, Time range (Japanese) |

### News (`!news`)

| Engine | Bang | Features |
|--------|------|----------|
| Google News | `!gon` | Locale, Safe search |
| Bing News | `!bin` | Paging, Locale, Time range |
| DuckDuckGo News | `!ddn` | Paging, Locale, Safe search |
| Yahoo News | `!yhn` | Paging |
| Reuters | `!reu` | Paging, Time range |
| Wikinews | `!wn` | Paging |

### Maps (`!map`)

| Engine | Bang | Features |
|--------|------|----------|
| OpenStreetMap | `!osm` | - |
| Photon | `!ph` | - |
| Apple Maps | `!apm` | - |

### Music (`!music`)

| Engine | Bang | Features |
|--------|------|----------|
| YouTube | `!yt` | Paging, Time range |
| SoundCloud | `!sc` | Paging |
| Bandcamp | `!bc` | Paging |
| Genius (Lyrics) | `!gen` | Paging |
| Radio Browser | `!rb` | Paging, Locale |
| Mixcloud | `!mc` | Paging |
| Deezer | `!dz` | Paging |

### IT (`!it`)

| Engine | Bang | Features |
|--------|------|----------|
| GitHub | `!gh` | - |
| GitLab | `!gl` | Paging |
| Stack Overflow | `!st` | Paging |
| Ask Ubuntu | `!ubuntu` | Paging |
| SuperUser | `!su` | Paging |
| Arch Linux Wiki | `!al` | Paging, Locale |
| Gentoo Wiki | `!ge` | Paging |
| PyPI | `!pypi` | - |
| Docker Hub | `!dh` | Paging |
| NPM | `!npm` | Paging |
| MDN | `!mdn` | Paging |
| Hacker News | `!hn` | Paging, Time range |

### Science (`!science`)

| Engine | Bang | Features |
|--------|------|----------|
| Google Scholar | `!gos` | Paging, Locale, Safe search, Time range |
| arXiv | `!arx` | Paging |
| PubMed | `!pub` | - |
| Semantic Scholar | `!se` | Paging |
| Crossref | `!cr` | Paging |
| OpenAlex | `!oa` | Paging |

### Files (`!files`)

| Engine | Bang | Features |
|--------|------|----------|
| The Pirate Bay | `!tpb` | - |
| 1337x | `!1337x` | Paging |
| BT4G | `!bt4g` | Paging, Time range |
| Kickass | `!kc` | Paging |
| Library Genesis | `!lg` | - |
| Anna's Archive | `!aa` | Paging, Locale |
| F-Droid | `!fd` | Paging |
| APK Mirror | `!apkm` | Paging |

### Social Media (`!social_media`)

| Engine | Bang | Features |
|--------|------|----------|
| Reddit | `!re` | - |
| Lemmy Posts | `!lepo` | Paging |
| Lemmy Comments | `!lecom` | Paging |
| Mastodon Users | `!mau` | - |
| Mastodon Hashtags | `!mah` | - |
| 9GAG | `!9g` | Paging |

## Engine Features Legend

| Feature | Description |
|---------|-------------|
| Paging | Supports pagination via `pageno` parameter |
| Locale | Supports language/locale filtering |
| Safe search | Supports safe search filtering (0, 1, 2) |
| Time range | Supports time-based filtering (day, month, year) |

## API Examples with Categories/Engines

### Search only news category
```bash
curl 'https://searx.example.org/search?q=python&categories=news&format=json'
```

### Search using specific engines
```bash
curl 'https://searx.example.org/search?q=python&engines=google,duckduckgo&format=json'
```

### Search with bang syntax
```bash
curl 'https://searx.example.org/search?q=!github+python+web+framework&format=json'
```

### Combined filters
```bash
curl 'https://searx.example.org/search?q=AI&categories=news,general&time_range=day&language=en&format=json'
```

## Important Notes

1. **Enabled by Default**: Each instance has different engines enabled by default. Check the instance's preferences page.

2. **Engine Availability**: Not all engines are available on all instances. Instance administrators can enable/disable engines.

3. **Rate Limits**: Some engines (like Google) may have stricter rate limits than others.

4. **Time Range Support**: Not all engines support time range filtering. Check the features table above.

5. **Language Support**: Locale/language filtering varies by engine. Some engines support it, others don't.

6. **Category vs Engine**: Using `categories` searches all engines in that category. Using `engines` searches only specified engines.
