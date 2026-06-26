## Description: <br>
A seven-role financial analysis team for stock analysis, fund recommendations, portfolio review, asset allocation, market sentiment monitoring, and investment decision support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mx6315909](https://clawhub.ai/user/mx6315909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial-analysis agents use this skill to coordinate multiple specialist roles for stock research, portfolio diagnosis, asset allocation, technical signals, valuation, and sentiment-risk summaries. Outputs are for reference and should not be treated as personalized or guaranteed investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad command execution can run financial-analysis scripts or shell commands that have not been reviewed. <br>
Mitigation: Disable or tightly restrict exec by default, and review any stock_analysis.py or other executable file before allowing it to run. <br>
Risk: Memory-backed holdings or trading history can expose sensitive portfolio information. <br>
Mitigation: Avoid sharing brokerage credentials or private account documents, and minimize stored portfolio details to only what is needed for the current analysis. <br>
Risk: Financial recommendations, ratings, or trading signals may be incorrect, stale, or unsuitable for the user. <br>
Mitigation: Treat outputs as reference material, verify market data and assumptions independently, and consult qualified financial professionals before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mx6315909/xiaodi-financial-analysis-team) <br>
- [Skill Overview](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Agent Architecture](artifact/architecture.json) <br>
- [Collaboration Guide](artifact/collaboration-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, guidance, configuration, shell commands] <br>
**Output Format:** [Markdown reports with structured sections, ratings, tables, risk notes, and occasional JSON or shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web data sources and memory-backed portfolio context; financial outputs require independent verification.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
