# Podcast Feed Check reference

Load this reference when checking one deployed podcast feed, diagnosing one direct episode-media URL, or comparing exactly two public feeds.

All three calls are read-only and make live requests that may take up to 60 seconds.

## What the feed check measures

`powmcp-podcast-feed-check:podcast_feed_check` checks one public podcast RSS feed.

It measures:

- Feed XML and namespace rules against separately dated Apple Podcasts, Spotify, and Podcasting 2.0 profiles.
- Required feed metadata with exact source paths.
- Artwork dimensions and format from the fetched asset.
- HEAD and byte-range delivery behavior on recent enclosures.
- One bounded ffprobe media sample when probing is enabled.

The structural inspection covers the selected recent-episode window. Delivery probing covers at most the newest 10 episodes, and sampled-media facts come from at most 2 MB from one reachable enclosure.

## Feed-check inputs requiring judgment

- `url` is the deployed public podcast RSS URL, including the protocol.
- `recentEpisodes` accepts 1 to 25 and defaults to 10.
- `probeMedia` defaults to true.
- Disable `probeMedia` only when the requested scope excludes the bounded media sample.

Call once for the chosen input. After a fix and republication, rerun on the same URL with the same chosen inputs.

## Reading the feed-check result

Read `ready`, blocking errors, per-profile results, warnings, then exact feed and asset evidence.

Quote returned profiles, rules, source paths, figures, and asset evidence verbatim. Fix blocking errors before relevant warnings.

When `ready` is true, the selected profiles produced no blocking error in the inspected evidence. This does not establish directory acceptance, and it says nothing about content outside the bounded window.

A skipped episode or probe, exhausted byte budget, deadline, or unavailable sampled media is unassessable. Put it under “Not checked in this run” with the returned reason.

## What the episode check measures

`powmcp-podcast-feed-check:podcast_episode_check` diagnoses one supplied direct public episode-media URL independently of its feed.

It inspects:

- Redirect chain.
- Final HTTP status.
- Content type and length.
- HEAD support.
- Byte-range behavior for seeking and resumable downloads.
- Cache headers.
- ffprobe container, codec, and sample-rate facts from a bounded 2 MB sample.

The only input is `url`, which must be the public direct episode audio or video enclosure URL including the protocol.

Read redirects and final status before interpreting the remaining delivery and media evidence. HEAD rejection alone is not a failure when GET succeeds.

A successful observation applies only to the supplied URL and sampled bytes. It does not assess feed metadata, other enclosures, complete duration, or release-wide audio consistency.

## What the comparison measures

`powmcp-podcast-feed-check:podcast_feed_compare` checks exactly two public podcast RSS feeds under identical bounds.

It summarizes:

- Per-profile readiness deltas.
- Blocking-error differences.
- Show metadata and namespace changes.
- Episode GUID overlap.
- Enclosure host and type changes.
- Artwork changes.
- Byte-range delivery regressions.

## Comparison inputs requiring judgment

- `urls` contains exactly two public podcast RSS feed URLs.
- `recentEpisodes` accepts 1 to 10 and defaults to 5.

Use comparison for a hosting migration or before-and-after revision. Name a safer feed only when the returned evidence supports one.

The comparison does not assess episodes outside the selected window and does not turn unavailable evidence into a clean result.

## Failure handling

An invalid-arguments error identifies the failing field. Tell the user:

> The check rejected the arguments at the named field. I will correct that field and call the same tool again.

Do not treat invalid arguments as a missing tool.

When only a rule id and location are available, open the cited location and apply the returned message. A rule id alone does not support an expanded diagnosis.

When a live request, probe, byte budget, deadline, or sample prevents assessment, quote the returned reason and place the item in the not-checked list.

## What a result does not establish

- Acceptance by Apple Podcasts, Spotify, or another directory.
- Condition outside the inspected recent-episode window.
- Full-media facts beyond the bounded sample.
- A clean result for skipped or unavailable evidence.
- LUFS loudness, true peak, clipping, or release-wide consistency.

Use Audio Master Check for the last job: https://powmcp.com/apps/audio-release-check/

## Non-PowMCP path

Use Apple's feed-validation workflow and a public podcast feed validator. Manually request the feed, artwork, and enclosure URLs, verify redirects and delivery behavior, inspect downloaded artwork and media with suitable local tools, and compare the revised feed with a saved prior version for GUID changes.

That path separates the checks and does not return Podcast Feed Check's unified measured feed, artwork, enclosure-delivery, and sampled-media evidence. Keep the same publish, inspect, fix, republish, rerun, and handoff procedure.

## Source-of-truth links

- Podcast Feed Check app page: https://powmcp.com/apps/podcast-feed-check/
- Apple feed validation: https://podcasters.apple.com/support/829-validate-your-podcast
- Current Apple feed requirements cited by the job packet: https://podtools.cc/apple-podcasts-rss-feed-requirements-checklist/
- Spotify feed submission guidance cited by the job packet: https://rss.com/blog/how-to-upload-a-podcast-to-spotify/
- Podcast validation error reference: https://correctfeed.com/help/podcast-feed-validation-errors/
