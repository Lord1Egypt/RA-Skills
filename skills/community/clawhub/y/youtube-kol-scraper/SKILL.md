---
name: youtube-kol-scraper
description: |
  YouTube KOL info scraping: input search keyword → output creator list (channel name, URL, video count, most relevant video views, contact email/social links)
  Trigger scenarios:
  - "Search YouTube by keyword to find creator info"
  - "Collect YouTube creator contact info"
  - "Extract channel data and email from YouTube search results"
  - "YouTube KOL data scraping"
  - "Search YouTube creators and get contact info"
---

# YouTube — KOL Info Scraping

> Input search keyword → enter each creator's channel page from search results → extract channel name, URL, video count, most relevant video views, contact email (description regex → personal site email extraction → social link fallback)

## Goal

Search YouTube by keyword, collect channel info and contact details for each creator in the search results.

## Prerequisites

- Browser is open on YouTube: `https://www.youtube.com`

> Prerequisites describe the state the website must be in before starting. They do not specify how browser-act connects — the caller chooses the connection method based on their environment.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has already been updated, API Key verified, and usage loaded in the current session → skip this step.

Otherwise execute in order, abort if any step fails:
1. `uv tool upgrade browser-act-cli || uv tool install browser-act-cli --python 3.12`
2. `browser-act browser list` to verify the API Key is available. If it returns a missing-key error, show the full error message (including registration link) to the user and retry after they complete registration
3. Load browser-act usage via the Skill tool by calling `browser-act`

## Capability Components

All atomic capabilities discovered during exploration are listed below; combine as needed during execution.

### API: Keyword Search — Get Video List (first page)

After navigating to search page, extract results from page-embedded `ytInitialData`:

`browser-act navigate` to search page:
```
https://www.youtube.com/results?search_query={keyword}
```

After page loads, `browser-act eval` (runtime data extraction):
```javascript
// keyword={search keyword}
const d = ytInitialData;
const contents = d?.contents?.twoColumnSearchResultsRenderer?.primaryContents?.sectionListRenderer?.contents;
const videos = [];
contents.forEach(s => {
  (s?.itemSectionRenderer?.contents || []).forEach(i => {
    if (i.videoRenderer) {
      const v = i.videoRenderer;
      videos.push({
        title: v.title?.runs?.[0]?.text,
        videoId: v.videoId,
        views: v.viewCountText?.simpleText || v.viewCountText?.runs?.map(r => r.text).join(''),
        channel: v.ownerText?.runs?.[0]?.text,
        channelUrl: v.ownerText?.runs?.[0]?.navigationEndpoint?.browseEndpoint?.canonicalBaseUrl,
        channelId: v.ownerText?.runs?.[0]?.navigationEndpoint?.browseEndpoint?.browseId
      });
    }
  });
});
// extract continuation token for pagination
const lastItem = contents[contents.length - 1];
const continuationToken = lastItem?.continuationItemRenderer?.continuationEndpoint?.continuationCommand?.token;
JSON.stringify({ count: videos.length, videos, continuationToken: continuationToken || null })
```

Response structure: `{ "count": N, "videos": [...], "continuationToken": "..." }`

### API: Keyword Search — Load More Results (pagination)

`browser-act eval` (fetch executes in browser, session credentials auto-injected):
```javascript
// continuationToken={continuationToken from previous page}
const apiKey = ytcfg?.data_?.INNERTUBE_API_KEY;
const ctx = ytcfg?.data_?.INNERTUBE_CONTEXT;
const res = await fetch('https://www.youtube.com/youtubei/v1/search?prettyPrint=false&key=' + apiKey, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ context: ctx, continuation: '{continuationToken}' })
});
const data = await res.json();
const actions = data?.onResponseReceivedCommands?.[0]?.appendContinuationItemsAction?.continuationItems || [];
const videos = [];
actions.forEach(i => {
  if (i?.itemSectionRenderer?.contents) {
    i.itemSectionRenderer.contents.forEach(c => {
      if (c.videoRenderer) {
        const v = c.videoRenderer;
        videos.push({
          title: v.title?.runs?.[0]?.text,
          videoId: v.videoId,
          views: v.viewCountText?.simpleText || v.viewCountText?.runs?.map(r => r.text).join(''),
          channel: v.ownerText?.runs?.[0]?.text,
          channelUrl: v.ownerText?.runs?.[0]?.navigationEndpoint?.browseEndpoint?.canonicalBaseUrl,
          channelId: v.ownerText?.runs?.[0]?.navigationEndpoint?.browseEndpoint?.browseId
        });
      }
    });
  }
});
const nextToken = actions[actions.length - 1]?.continuationItemRenderer?.continuationEndpoint?.continuationCommand?.token;
JSON.stringify({ count: videos.length, videos, continuationToken: nextToken || null })
```

Response structure: same as first page. `continuationToken` is null when no more results.

### API: Channel Basic Info Extraction

After navigating to channel page, extract basic info from `ytInitialData`:

`browser-act navigate` to channel page:
```
https://www.youtube.com{channelUrl}
```

`channelUrl` format is `/@ChannelHandle` (obtained from search results).

After page loads, `browser-act eval`:
```javascript
const d = ytInitialData;
const meta = d?.metadata?.channelMetadataRenderer;
const h = d?.header?.pageHeaderRenderer?.content?.pageHeaderViewModel;
const rows = h?.metadata?.contentMetadataViewModel?.metadataRows;
const desc = meta?.description;
const emailMatch = desc?.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g);
JSON.stringify({
  channelName: meta?.title,
  channelUrl: meta?.vanityChannelUrl,
  channelId: meta?.externalId,
  description: desc,
  emailInDesc: emailMatch,
  handle: rows?.[0]?.metadataParts?.[0]?.text?.content,
  subscribers: rows?.[1]?.metadataParts?.[0]?.text?.content,
  videoCount: rows?.[1]?.metadataParts?.[1]?.text?.content
})
```

Response structure: `{ "channelName": "...", "channelUrl": "...", "channelId": "UC...", "description": "...", "emailInDesc": ["email@example.com"] | null, "handle": "@...", "subscribers": "100K subscribers", "videoCount": "546 videos" }`

### API: Channel About Data — Social Links Extraction

Get about data (social links, country, join date, etc.) via browse API on the channel page:

`browser-act eval` (fetch executes in browser, no login required):
```javascript
(async () => {
  const d = ytInitialData;
  const desc = d?.header?.pageHeaderRenderer?.content?.pageHeaderViewModel?.description?.descriptionPreviewViewModel;
  const ep = desc?.rendererContext?.commandContext?.onTap?.innertubeCommand?.showEngagementPanelEndpoint;
  const cont = ep?.engagementPanel?.engagementPanelSectionListRenderer?.content?.sectionListRenderer?.contents?.[0]?.itemSectionRenderer?.contents?.[0]?.continuationItemRenderer?.continuationEndpoint;
  const token = cont?.continuationCommand?.token;
  if (!token) return JSON.stringify({ error: 'no continuation token' });
  const apiKey = ytcfg?.data_?.INNERTUBE_API_KEY;
  const ctx = ytcfg?.data_?.INNERTUBE_CONTEXT;
  const res = await fetch('https://www.youtube.com/youtubei/v1/browse?prettyPrint=false&key=' + apiKey, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context: ctx, continuation: token })
  });
  const data = await res.json();
  const items = data?.onResponseReceivedEndpoints?.[0]?.appendContinuationItemsAction?.continuationItems;
  const aboutRenderer = items?.find(i => i?.aboutChannelRenderer);
  const vm = aboutRenderer?.aboutChannelRenderer?.metadata?.aboutChannelViewModel;
  if (!vm) return JSON.stringify({ error: 'no aboutChannelViewModel' });
  return JSON.stringify({
    country: vm.country,
    joinedDate: vm.joinedDateText?.content,
    subscribers: vm.subscriberCountText,
    videoCount: vm.videoCountText,
    viewCount: vm.viewCountText,
    links: (vm.links || []).map(l => ({
      title: l?.channelExternalLinkViewModel?.title?.content,
      link: l?.channelExternalLinkViewModel?.link?.content
    }))
  });
})()
```

Response structure: `{ "country": "...", "joinedDate": "...", "links": [{"title": "Instagram", "link": "instagram.com/xxx"}, ...] }`

### API: Filter Social Links for Personal Sites and Extract Email

From `links` returned by about data, filter out social platforms requiring login, keep only publicly accessible personal/company websites, visit each to extract emails.

**Filter rules** — exclude these domains (require login or no email):
`instagram.com`, `tiktok.com`, `linkedin.com`, `x.com`, `twitter.com`, `facebook.com`, `discord.gg`, `discord.com`, `skool.com`, `apps.apple.com`, `play.google.com`, `github.com`, `buymeacoffee.com`, `youtube.com`

`browser-act eval` (filter logic, can run in browser or locally):
```javascript
// links={links array from about data}
const socialDomains = ['instagram.com','tiktok.com','linkedin.com','x.com','twitter.com','facebook.com','discord.gg','discord.com','skool.com','apps.apple.com','play.google.com','github.com','buymeacoffee.com','youtube.com'];
const websiteLinks = links.filter(l => {
  const domain = l.link?.toLowerCase() || '';
  return !socialDomains.some(sd => domain.includes(sd));
});
JSON.stringify({ websiteLinks })
```

For each link in `websiteLinks`, navigate and extract email:

`browser-act navigate` to target site → `browser-act wait stable` → `browser-act eval`:
```javascript
// extract email addresses from page (regex + mailto links dual matching)
(() => {
  const text = document.body.innerText;
  const emailsInText = text.match(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g) || [];
  const mailtoLinks = Array.from(document.querySelectorAll('a[href^="mailto:"]')).map(a => a.href.replace('mailto:', '').split('?')[0]);
  const allEmails = [...new Set([...emailsInText, ...mailtoLinks])];
  return JSON.stringify({ emails: allEmails });
})()
```

If no email on home page, check for Contact/About page links and follow one level deeper:
```javascript
(() => {
  const contactLinks = Array.from(document.querySelectorAll('a')).filter(a => {
    const t = (a.textContent + ' ' + a.href).toLowerCase();
    return t.includes('contact') || t.includes('about');
  }).map(a => a.href).filter(h => h.startsWith('http'));
  return JSON.stringify({ contactLinks: [...new Set(contactLinks)].slice(0, 3) });
})()
```

Navigate to Contact page and repeat email extraction. Stop when email found; visit at most 2 levels (home page + Contact page).

## Enum Parameters

No enum parameters. Search keywords are specified by the user; no predefined enumerations.

## Pagination

**API pagination**: `continuationToken`, type: cursor, starting value: obtained from the last `continuationItemRenderer` in `ytInitialData`. Next page value: `continuationItemRenderer.continuationEndpoint.continuationCommand.token` from the last item in each API response. Termination: `continuationToken` is null or no new `videoRenderer` in response.

## Success Criteria

- Search results: `videos.length ≥ 1`
- Channel basic info: `channelName` and `channelId` non-empty
- About data: `links` array successfully obtained (can be empty)
- Email extraction: complete email extraction chain executed for each channel (description regex → personal site → social link fallback)
- Field completeness: `channelName`, `channelUrl`, `videoCount` non-empty rate = 100% per channel

## Known Limitations

- Email retrieval rate depends on whether creators expose their email publicly on personal sites; not all channels have emails
- Social platforms requiring login (Instagram, LinkedIn) are not visited; skipped directly
- Personal site email extraction goes at most 2 levels deep (home page + Contact page); no full-site crawling
- ~18–20 videos per search results page; pagination via continuation token
- `ytInitialData` and `ytcfg` are runtime variables embedded in YouTube pages; page structure changes may affect path access

## Experience Notes

Path: `{working_dir}/browser-act-skill-forge-memories/youtube-kol-scraper-youtube-kol-scraper.memory.md`

**Before execution**: If this file exists, read it first — it records unexpected events encountered in past executions (e.g., changed endpoints), and adjust execution accordingly.

**After execution**: If unexpected events occurred (endpoint failure, page redesign, anti-bot upgrade), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Do not write on normal execution.

File format example:
```markdown
# youtube-kol-scraper-youtube-kol-scraper experience notes

2026-04-16: YouTube reveal_business_email API returns 400 regardless of Stealth/Real Chrome (BotGuard encoding incompatible) → abandon reCAPTCHA path
2026-04-16: social platform bios (Instagram/X/TikTok) rarely contain emails → not worth visiting
2026-04-16: personal/company websites are the best email source (3/10 hit rate), extracted via mailto links + regex → use as primary email extraction path
```
