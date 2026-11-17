## Description:

Recursive Maths Animator helps agents plan, code, render, version, and verify Manim-based mathematical animations with optional voiceover, built-in design systems, reusable chart and statistics patterns, and frame-based review loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[science-prof-robot](https://clawhub.ai/user/science-prof-robot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, analysts, and content teams use this skill to turn mathematical ideas and data stories into narrated Manim animations, reusable scene code, approval previews, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawHub security verdict is suspicious and reports purpose-mismatched audit guidance in the artifact.

Mitigation: Use the server-provided security verdict as authoritative, review the helper code before installation, and do not rely on artifact audit commentary to dismiss scanner concerns.

Risk: A deletion helper may remove files outside the intended project area when given untrusted scene or branch names.

Mitigation: Avoid untrusted names with ManimProject helpers, review target paths before delete or rollback operations, and test project operations on disposable copies first.

Risk: Remote TTS services can send narration text to an external provider.

Mitigation: Do not enable gTTS or Gemini TTS for confidential narration unless that data sharing is approved; use offline TTS or omit voiceover for sensitive content.

Risk: Dependencies are specified with version ranges rather than hash-locked packages.

Mitigation: Use pinned and hash-locked dependencies before deploying the skill in sensitive or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/science-prof-robot/skills/recursive-maths-animator)
- [Manim guide](references/manim_guide.md)
- [Video verification rubric](references/video_verification_rubric.md)
- [Pattern library](references/pattern_library/__init__.py)
- [Design systems registry](references/design_systems/__init__.py)
- [Manim project versioning helper](references/manim_versioning.py)
- [Verification frame extraction script](scripts/extract_verification_frames.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell code blocks plus generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Manim scene code, project scaffolds, verification notes, and rendered MP4 or GIF outputs through local tools.]

## Skill Version(s):

1.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
