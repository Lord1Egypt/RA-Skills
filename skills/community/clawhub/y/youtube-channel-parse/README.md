# YouTube Channel Parse

This skill helps product managers and researchers extract insights from YouTube channels and individual videos.

It ships inside the `product-research-suite` bundle and focuses on turning long-form video content into transcripts, summaries, notes, and structured datasets.

## What It Does

- analyze a full YouTube channel
- analyze a single YouTube video
- filter videos by date, topic, speakers, or metadata
- collect or generate transcripts
- produce summaries, notes, and reusable structured outputs

## Example Use Cases

- Parse all videos from a particular conference or other event and provide summaries and insights.
- Analyze a creator or company channel to understand positioning and recurring themes.
- Pull customer language from talks, interviews, demos, and product videos.
- Build a reusable research dataset from a filtered set of videos.

## Outputs

- channel inventory in JSON and markdown when needed
- filtered video datasets in JSON, CSV, and markdown when needed
- transcript files per video
- markdown summaries and notes
- channel-level reports with findings and caveats

## Included In

Install this skill through the main bundle:

```bash
npx skills add ulyanas/product-research-skills --skill product-research-suite -g -y
```

## Skill Files

- `SKILL.md` contains the runtime instructions for agents
- `references/` contains dependency, filtering, and output guidance
- `scripts/` contains the local workflow scripts for inventory, transcription, and report generation
