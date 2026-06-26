## Description: <br>
Search and reference Simpsons episode scripts using Springfield! Springfield! as the source, with an optional local episode index for faster lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Smev1](https://clawhub.ai/user/Smev1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find Simpsons episodes, quote fragments, short script excerpts, source links, and grounded character-style guidance without loading a full script corpus into context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Corpus-building and fallback quote search can fetch and cache public script pages locally. <br>
Mitigation: Run corpus-building commands only when local caching is acceptable, and review cached reference files before redistribution. <br>
Risk: Script excerpts and character-style helpers can encourage long-form reproduction or misleading impersonation. <br>
Mitigation: Keep excerpts short, cite source links, write fresh character-inspired text, and avoid claiming to be an official character. <br>
Risk: Search results depend on a user-maintained public script source and may be incomplete or imperfect. <br>
Mitigation: Treat matches as approximate when appropriate and verify important quotes against the linked source page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Smev1/simpsons-search) <br>
- [Springfield! Springfield! Simpsons episode scripts](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-simpsons) <br>
- [simpsons-episodes.json](references/simpsons-episodes.json) <br>
- [simpsons-characters.json](references/simpsons-characters.json) <br>
- [simpsons-character-evidence.json](references/simpsons-character-evidence.json) <br>
- [simpsons-character-dossiers.json](references/simpsons-character-dossiers.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON with short excerpts, source links, search results, character briefs, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Excerpt quality depends on the source site and any local corpus or search index cache available to the agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
