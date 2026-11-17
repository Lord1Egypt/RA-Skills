## Description:

Make vertical 9:16 (or square 1:1) short videos for YouTube Shorts, Instagram Reels and TikTok from footage the user already has, with automatic reframing of 16:9 clips. Local with Reelary on Mac or Windows. Trigger on "shorts", "reels", "tiktok", "vertical video", "9:16", "square video", "social clip from my footage", "repurpose my footage for social". Not for posting to social networks or AI avatar videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reelary](https://clawhub.ai/user/reelary)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and video editors use this skill to turn footage they already have into short vertical or square clips for social platforms. It guides scene selection, project saving, and export; it does not post videos to social networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command-line fallback uses the Reelary package through npx; the package and application are outside this artifact inspection.

Mitigation: Review Reelary's setup before installing, and prefer a reviewed, pinned CLI version before running the fallback.

Risk: Indexing footage can expose more media than intended to the workflow.

Mitigation: Choose only the footage folders you want indexed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reelary/skills/reelary-vertical-video)

## Skill Output:

**Output Type(s):** [Video files, Text guidance, Shell commands]

**Output Format:** [Reelary project and exported short-video files, with scene-selection guidance and optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [9:16 or 1:1 aspect ratio; scenes are guided toward a total runtime under 60 seconds. The documented free export tier is 720p, watermarked, and limited to five exports per month.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
