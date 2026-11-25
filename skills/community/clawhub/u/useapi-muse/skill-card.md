## Description:

Make Meta Muse AI images and 10-second videos with sound and spoken dialogue (muse.ai, Meta's AI agent) on your own Muse account, the free plan included, through the useapi.net Muse API, a third-party paid API not affiliated with Meta. Text to image, combine up to 9 photos into one picture, edit an image, restore and colorize an old photo, image to video that makes a photo talk, and video to video such as swapping a person in a clip. Saves the .webp or .mp4. Use when the user asks for a Muse or Meta Muse image or video, a talking photo, an old photo restored or animated, or a person swapped in a video. Needs bash, curl, jq and USEAPI_TOKEN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[useapi](https://clawhub.ai/user/useapi)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agents use their Muse account through useapi.net to generate and edit images, make short videos with sound, animate talking photos, and restore or colorize photos. The skill saves generated images as WebP and videos as MP4.

### Deployment Geography for Use:

Global API use; Muse account setup is documented for the United States, Canada, Japan, and Singapore.

## Known Risks and Mitigations:

Risk: The security analysis was partial: 7 of 9 components were fully inspected, and the download script was among those only partly inspected.

Mitigation: Review the scripts before use and use the skill only if you trust api.useapi.net with your API token.

Risk: Local image, video, and audio inputs may be uploaded to useapi.net for processing.

Mitigation: Send only media you are comfortable sharing with useapi.net, and keep USEAPI_TOKEN private.

## Reference(s):

- [useapi.net Muse API documentation](https://useapi.net/docs/api-muse-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-muse)
- [Set up a useapi.net account](https://useapi.net/docs/start-here/setup-useapi)
- [Connect a Muse account](https://useapi.net/docs/start-here/setup-muse)
- [useapi.net subscription](https://useapi.net/docs/subscription)
- [Muse API examples](https://github.com/useapi/muse-api)

## Skill Output:

**Output Type(s):** [Images, Videos, Files]

**Output Format:** [WebP images, MP4 videos, and JSON job records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Images are about 2 to 2.5 megapixels; videos are about 10 seconds at 720p with sound.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
