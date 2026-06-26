## Description: <br>
Acts as a Chinese-language judge for the Who Is Undercover party game, using local scripts to assign words, run description and voting rounds, tally eliminations, and produce an end-of-game recap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loongfay](https://clawhub.ai/user/loongfay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and group-game hosts use this skill to run a structured Who Is Undercover session in Chinese, with the agent serving as judge, record keeper, vote collector, and final reviewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores party-game records and message-sender IDs in a local SQLite database. <br>
Mitigation: Install only where this local storage is acceptable, treat the database as private game data, and delete old records when no longer needed. <br>
Risk: The skill relies on direct-message and sender-ID access to validate players and collect votes. <br>
Mitigation: Grant the agent only the DM and sender-ID access needed to run the game. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loongfay/undercover-is-who) <br>
- [Publisher profile](https://clawhub.ai/user/loongfay) <br>
- [Word pair reference](references/word_pairs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese game prompts, JSON command results, Markdown game exports, and shell commands for local Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local SQLite game records and player sender IDs during gameplay.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
