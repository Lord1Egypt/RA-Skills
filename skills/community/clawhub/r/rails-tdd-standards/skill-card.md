## Description:

Rails TDD Standards provides RSpec testing standards and best practices for Rails applications, including FactoryBot setup, test structure, Rails 8 gotchas, service specs, ActionCable specs, external service stubs, serializer specs, and test commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write, review, and debug Rails RSpec tests with consistent conventions for factories, callbacks, authentication, channels, external service stubs, serializers, and CI test database setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for general test-writing requests where Rails and RSpec conventions are not applicable.

Mitigation: Confirm the target project uses Rails and RSpec before applying its testing conventions.

Risk: Generated Rails database commands could affect a non-test environment if run without review.

Mitigation: Review database commands and environment variables before execution, and run CI database setup only against the test environment.

Risk: Example external service stubs and token patterns can be misapplied to real API calls or credentials.

Mitigation: Keep external service examples as test doubles or HTTP stubs, and avoid using production tokens or live network calls in tests.

## Reference(s):

- [Rails TDD Standards on ClawHub](https://clawhub.ai/djc00p/skills/rails-tdd-standards)
- [Publisher profile: djc00p](https://clawhub.ai/user/djc00p)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Ruby, YAML, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; guidance assumes a Rails project with RSpec and Bundle-managed dependencies.]

## Skill Version(s):

1.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
