## Description:

A CISSP exam preparation quiz API that delivers randomized questions, tracks session progress, and evaluates answers in real-time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, cybersecurity professionals, training organizations, and developers use this skill to start CISSP practice quizzes, submit answers, and receive scoring and domain-level performance feedback through the CISSPly API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an administrative database reload action without clear API-level safeguards.

Mitigation: Do not grant or use administrative credentials unless the reload endpoint is confirmed to be strongly protected and intended for the user.

Risk: Quiz session identifiers, answers, and timing data are sent to the hosted service.

Mitigation: Use non-identifying sessionId values and avoid including personal identity or sensitive information in quiz requests.

## Reference(s):

- [CISSPly ClawHub listing](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-cissply)
- [CISSPly API route](https://api.toolweb.in/tools/cissply)
- [CISSPly API docs](https://api.toolweb.in:8175/docs)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON API responses with quiz questions, answer evaluations, scores, and category performance metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API responses depend on sessionId, quiz length, submitted answers, and timeTaken values.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
