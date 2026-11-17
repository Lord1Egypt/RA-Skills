## Description:

Launches a real headless Chromium browser on a Linux server or Docker container to perform end-to-end QA testing by navigating pages, clicking controls, filling forms, and simulating user journeys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melnikdavid](https://clawhub.ai/user/melnikdavid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to run browser-based end-to-end checks against authorized web applications, collect screenshots, and produce a concise bug and coverage report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install browser and testing dependencies on the execution environment.

Mitigation: Run it in an authorized, disposable staging environment and review dependency installation steps before execution.

Risk: Automated clicks and form submissions can trigger real application actions.

Mitigation: Use staging targets, test accounts, strict URL allowlists, and confirmation or dry-run controls before submissions or destructive clicks.

Risk: Screenshots may capture sensitive application data.

Mitigation: Keep screenshots private, avoid sensitive authenticated sessions, and clean up generated screenshot directories after review.

Risk: Docker-oriented Chromium flags disable browser isolation for compatibility.

Mitigation: Run the browser inside a sandboxed, non-production container or VM, preferably as a non-root user with limited network and filesystem access.

## Reference(s):

- [Docker Setup Reference](references/docker-setup.md)
- [Test Phases - Full QA Script](references/test-phases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash and Python code blocks, plus a structured QA report and screenshot files from the test run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces screenshots under /tmp/qa_screenshots and reports coverage, bugs, warnings, untested areas, and a final verdict.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
