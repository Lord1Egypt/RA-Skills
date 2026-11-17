## Description:

使用虾盘云音乐将一句话主题或用户歌词创作为完整歌曲、纯音乐和 BGM，也可单独生成歌词或查询余额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn a brief idea or supplied lyrics into songs or instrumental background music, draft lyrics on their own, and check their account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions permit including a full API key in a recharge URL, which could expose the credential.

Mitigation: Remove that instruction. Use a credential-free recharge link and a dedicated, spending-limited key supplied through the environment; rotate any key already shared in a URL.

Risk: Prompts and lyrics are sent to external services, lyric drafting may incur a charge, and cards remain cached locally.

Mitigation: Avoid sending sensitive material, disclose the external processing and possible charge, and confirm each audio purchase. Check existing tasks or billing before rerunning an interrupted command.

## Reference(s):

- [虾盘云音乐画板](https://tu.u-claw.org.cn)
- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/xiapan-music)

## Skill Output:

**Output Type(s):** [Audio files, Lyrics, Account balance information]

**Output Format:** [MP3 audio files and text or JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio is saved as MP3; paid generation requires user confirmation.]

## Skill Version(s):

0.1.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
