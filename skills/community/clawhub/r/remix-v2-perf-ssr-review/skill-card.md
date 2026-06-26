## Description: <br>
Reviews Remix v2 code for caching header misuse, missing server/client split, hydration mismatches, prefetch hygiene, and asset bottlenecks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to review Remix v2 TypeScript route modules for SSR and performance defects before changing production code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review findings could be incorrect or misleading if they are applied without checking the cited source location. <br>
Mitigation: Verify each reported file, line, and quote before changing production code. <br>
Risk: Caching and hydration recommendations can affect correctness, privacy, or user-visible behavior. <br>
Mitigation: Review session, cookie, cache, and render-path context before accepting a recommendation. <br>


## Reference(s): <br>
- [Caching Headers Review](artifact/references/caching-headers.md) <br>
- [Server/Client Split Review](artifact/references/server-client-split.md) <br>
- [Hydration Safety Review](artifact/references/hydration.md) <br>
- [Prefetch & Streaming Review](artifact/references/prefetch-streaming.md) <br>
- [Assets, Images, Fonts & CSS Review](artifact/references/assets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review findings with file and line evidence] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should be treated as review advice and verified against source evidence before production changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
