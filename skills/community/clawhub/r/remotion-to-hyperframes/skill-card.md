## Description: <br>
Translate an existing Remotion React video composition into a HyperFrames HTML composition when the user explicitly asks to port, convert, migrate, translate, or rewrite Remotion source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video engineers use this skill to migrate existing Remotion compositions to HyperFrames HTML, GSAP timelines, and related assets. It also helps identify Remotion patterns that should use runtime interop instead of lossy translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation can execute project code or package scripts from the source project. <br>
Mitigation: Run validation in a disposable checkout or sandbox and review package scripts and setup.sh before execution. <br>
Risk: Generated examples can load third-party scripts or browser dependencies. <br>
Mitigation: Prefer vendored or pinned local browser dependencies over CDN script tags before production use. <br>
Risk: Secrets available to the render environment could be exposed during validation or rendering. <br>
Mitigation: Keep secrets out of the render environment and use minimal credentials when validating untrusted projects. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lucas-kay8/remotion-to-hyperframes) <br>
- [Remotion to HyperFrames API Map](references/api-map.md) <br>
- [Runtime interop escape hatch](references/escape-hatch.md) <br>
- [Translation evaluation guide](references/eval.md) <br>
- [Translation limitations](references/limitations.md) <br>
- [HyperFrames runtime interop PR #214](https://github.com/heygen-com/hyperframes/pull/214) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an index.html HyperFrames composition, TRANSLATION_NOTES.md, validation commands, and recommendations to use runtime interop when blockers are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
