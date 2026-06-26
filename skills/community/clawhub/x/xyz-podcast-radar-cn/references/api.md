# API Notes

## Ranking Endpoints

The skill relies on four ranking endpoints from 中文播客榜:

- `https://xyzrank.com/api/episodes`
- `https://xyzrank.com/api/podcasts`
- `https://xyzrank.com/api/new-episodes`
- `https://xyzrank.com/api/new-podcasts`

They all support:

- `offset`
- `limit`

Typical shape:

```json
{
  "items": [],
  "total": 1000,
  "limit": 50,
  "offset": 0
}
```

## Hot vs New

- `hot-*`: better when the user wants current winners, stable attention leaders, or reference shows
- `new-*`: better when the user wants rising programs, fresh discoveries, or new entrants

## Podcasts vs Episodes

- `*-podcasts`: better for show-level discovery, creator benchmarking, and curation lists
- `*-episodes`: better for single-item recommendations, topic scouting, and downstream distribution ideas

## User Language Mapping

In Chinese, users often say `播客` loosely when they actually mean `最近值得点开的内容`.

Default interpretation:

- `热门播客`
- `最近热门播客`
- `推荐几个最近很火的播客`

Map these to `*-episodes` first unless the user clearly asks for show/channel-level entities.

Use `*-podcasts` when the wording explicitly asks for:

- `播客频道`
- `播客栏目`
- `节目主页`
- `频道级榜单`
- `栏目级榜单`
- benchmark lists of shows

Rule of thumb:

- listener discovery wording -> episodes
- channel / show / benchmark wording -> podcasts

## Useful Episode Fields

- `rank`
- `title`
- `podcastID`
- `podcastName`
- `primaryGenreName`
- `playCount`
- `commentCount`
- `subscription`
- `duration`
- `postTime`
- `link`
- `lastReleaseDateDayCount`

## Useful Podcast Fields

- `rank`
- `id`
- `name`
- `primaryGenreName`
- `authorsText`
- `trackCount`
- `avgDuration`
- `avgPlayCount`
- `avgCommentCount`
- `avgOpenRate`
- `lastReleaseDateDayCount`
- `links`

## Field Caveats

### Genre

`primaryGenreName` is useful but incomplete, especially on `new-*` lists. When it is blank:

- treat it as `未分类`
- do not invent a hard genre unless the title makes it obvious and the claim is clearly framed as an inference

### Open Rate

`openRate` and `avgOpenRate` can be greater than `1` in live data.

Do not present them as literal open rates or probabilities. If you mention them at all:

- call them ranking signals
- keep the interpretation light

### podcastID vs Xiaoyuzhou pid

For episodes:

- ranking `podcastID` aligns with the ranking dataset
- it is not the same as Xiaoyuzhou `pid`

If you need the Xiaoyuzhou podcast URL and only have an episode URL:

1. enrich the episode page
2. read `episode.pid`
3. derive `https://www.xiaoyuzhoufm.com/podcast/<pid>`

## Xiaoyuzhou Enrichment

When enriching a small set of pages, you can pull from `#__NEXT_DATA__`.

Useful episode fields:

- `episode.description`
- `episode.shownotes`
- `episode.duration`
- `episode.playCount`
- `episode.commentCount`
- `episode.favoriteCount`
- `episode.clapCount`
- `episode.pubDate`
- `episode.pid`
- nested `episode.podcast`

Useful podcast fields:

- `podcast.title`
- `podcast.author`
- `podcast.brief`
- `podcast.description`
- `podcast.subscriptionCount`
- `podcast.episodeCount`
- `podcast.latestEpisodePubDate`
- `podcast.podcasters`

Remember: enrichment is optional and capped. Ranking-first remains the default.
