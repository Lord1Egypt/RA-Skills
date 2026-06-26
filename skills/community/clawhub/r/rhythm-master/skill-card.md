## Description: <br>
This skill enables playing a rhythm game called "节奏大师" (Rhythm Master) similar to QQ Dance/DDR. Players press arrow keys and spacebar in time with falling notes to score points. The game features multiple difficulty levels, combo system, judgment ratings (PERFECT/GREAT/GOOD/BAD/MISS), local leaderboard, and can be extended with online leaderboards. Use this skill when the user wants to play a rhythm game, test their reflexes, or have fun with a keyboard-based music game. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dletter2](https://clawhub.ai/user/dletter2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to play or host a keyboard rhythm game in a browser, with difficulty selection, scoring, combo tracking, and local leaderboard support. Developers can extend it with an online leaderboard after adding appropriate Firebase or backend configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The online leaderboard setup can expose player score data and a Firebase database to public tampering if followed with open read/write rules. <br>
Mitigation: Use the local HTML game for low-risk play, prefer non-personal player names, and do not publish an online leaderboard until Firebase rules are locked down, writes are validated and rate-limited, users know what data is uploaded, and stored scores can be managed or deleted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dletter2/rhythm-master) <br>
- [Game mechanics](artifact/references/game_mechanics.md) <br>
- [Leaderboard system](artifact/references/leaderboard_system.md) <br>
- [Firebase setup](artifact/FIREBASE_SETUP.md) <br>
- [Firebase documentation](https://firebase.google.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes browser game files and optional leaderboard configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
