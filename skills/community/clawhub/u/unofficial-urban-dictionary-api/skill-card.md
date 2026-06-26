## Description: <br>
Query the Unofficial Urban Dictionary API for slang definitions. Use when asked to define slang/phrases, fetch random Urban Dictionary entries, browse by letter/new, or get entries by author/date. Supports endpoints /api/search, /api/random, /api/browse, /api/author, and /api/date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougbtv](https://clawhub.ai/user/dougbtv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Urban Dictionary-style slang definitions, random entries, browse results, and entries by author or date through an unofficial third-party API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup terms are sent to an unofficial third-party API. <br>
Mitigation: Use the skill only when sending the requested slang lookup terms to the external API is acceptable. <br>
Risk: Returned entries may include offensive or NSFW user-generated content. <br>
Mitigation: Present results neutrally, avoid adding extra offensive language, and summarize only the entries needed for the user request. <br>
Risk: The third-party API may fail, return bad responses, or return no entries. <br>
Mitigation: Retry once on bad responses, broaden overly strict searches when appropriate, and clearly report API or network failures. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dougbtv/unofficial-urban-dictionary-api) <br>
- [Unofficial Urban Dictionary API endpoint](https://unofficialurbandictionaryapi.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Markdown summaries of API results, with optional JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top entries are summarized by default; long entries should be truncated cleanly with an offer to provide the full output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
