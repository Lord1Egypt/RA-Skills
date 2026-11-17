## Description:

Turns a name, an age and a few photos into a personalized AI birthday video on varg: a song that sings their name, their photo coming to life as they blow out the candles, a "then and now" montage, an epic trailer starring them, a pet's birthday, an animated e-card or invitation. Asks the 5 questions that make it theirs, makes the stills first (GPT Image 2.5 spells the name on the cake), animates them (Wan 3, Seedance 2.5), makes the song (ElevenLabs Music sings the name), then exports one file that plays on WhatsApp and iMessage. Use when someone asks for a birthday video, a happy birthday message, a birthday song with a name, a birthday surprise, a video for a friend's, partner's, mom's or dad's birthday, a milestone birthday (18, 30, 50, 80), a pet's birthday or a birthday invitation. Not for weddings, anniversaries and holiday greetings (use varg-occasion-video) or a business sending birthday videos to every customer (make-personalized-videos-at-scale on varg how to).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to plan and create a personalized birthday video from a name, personal details, and photos, including a custom song, animated scenes, a pet video, or an invitation. The agent provides prompts and workflow guidance for generating media and assembling an MP4 for messaging or display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may send identifiable photos and personal details to external generation services without a clear sharing notice.

Mitigation: Before generation, explain which photos and details may be sent to external services, obtain the person's agreement where required by the skill's consent rules, and use only materials the requester has approved for sharing.

Risk: The installation command is unpinned, so the installed source may change over time.

Mitigation: Review the source and verify the intended release before installing; use a version-pinned source when the installation method supports it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vargai/skills/varg-birthday-video)
- [Varg birthday video guide](https://varg.ai/how-to/make-a-birthday-video)
- [formats.md](artifact/references/formats.md)
- [song.md](artifact/references/song.md)
- [styles.md](artifact/references/styles.md)

## Skill Output:

**Output Type(s):** [Video, Audio, Images, Markdown guidance, Shell commands]

**Output Format:** [MP4 video with generated image and audio assets; Markdown prompts and workflow guidance; shell commands for media assembly]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized media based on supplied names, details, and photos; the workflow describes exports for messaging and display.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
