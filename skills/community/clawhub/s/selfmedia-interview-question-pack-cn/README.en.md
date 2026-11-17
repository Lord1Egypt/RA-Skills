# Interview Questions & Follow-up Pack

Turn public background materials, an interview topic, and a duration into a record-ready Chinese interview outline. The result orders questions along a narrative arc, adds conditional follow-ups, and flags facts or assets to verify. It uses only material supplied by the user and never invents the interviewee's views.

## Install

```bash
npx skills add xxjrq/selfmedia-interview-question-pack-cn
```

## Input and result

Input: public-profile excerpts, topic, and duration; audience or editorial boundaries are optional. Result: a timed question flow, conditional follow-ups, known facts, and a pre-recording verification list. If any required input is missing, it returns the missing fields and a copyable template instead of fabricating an outline.

See [SKILL.md](SKILL.md), the [successful example](fixtures/success.md), and the [missing-input example](fixtures/failure-missing-input.md). Run `python3 scripts/self_test.py` to validate the standalone package.

## License and source note

The documentation, process, and examples are original. The public purpose of [marketingskills customer-research](https://github.com/coreyhaines31/marketingskills/tree/main/skills/customer-research) was reviewed; no text or code was copied. Licensed under [MIT-0](LICENSE).

Actual forward references: [success](fixtures/forward-success.md) and [missing input](fixtures/forward-failure.md). Questions do not assume that a later activity caused earlier repeat visits; supplied source attribution is retained.
