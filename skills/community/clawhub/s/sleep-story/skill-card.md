## Description:

Creates warm sleep stories that combine relaxation methods such as progressive muscle relaxation, mindful breathing, visualization, safe-place imagery, gratitude recall, and hypnotic sleep suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soyof](https://clawhub.ai/user/soyof)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask the agent for a calming bedtime story when they want gentle narrative support for relaxation or sleep. The skill guides story type selection, non-stimulating content constraints, personalization, and optional series continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hypnotic-style sleep content may not be appropriate for every user.

Mitigation: Use the skill only with user awareness and comfort, and keep the interaction easy to stop.

Risk: Sleep metrics and preference tracking can expose sensitive personal patterns.

Mitigation: Require explicit opt-in, avoid storing unnecessary sleep metrics, keep profiles local and reviewable, and provide a simple way to delete all history and preferences.

Risk: Persistent personalization may store user preferences beyond a single story session.

Mitigation: Do not write preferences to shared agent memory such as TOOLS.md; store only local user-approved profile data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soyof/skills/sleep-story)
- [ClawDis Homepage](https://github.com/SoyooSkills/sleep-story)
- [README](artifact/README.md)
- [Integration Guide](artifact/INTEGRATION.md)
- [Psychology Techniques](artifact/references/psychology-techniques.md)
- [Story Templates](artifact/references/story-templates.md)
- [Story Types](artifact/references/story-types.md)
- [Research Evidence](artifact/references/research-evidence.md)
- [Personalization System](artifact/references/personalization-system.md)
- [Feedback Loop System](artifact/references/feedback-loop-system.md)
- [History Tracking](artifact/references/history-tracking.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Plain text or Markdown story content with optional JSON preference and history records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stories target 1000-2500 Chinese characters; personalization should remain local, reviewable, opt-in, and deletable.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
