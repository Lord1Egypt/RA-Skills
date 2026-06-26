# Mainland Vs Global

Use this file whenever Tencent recommendations could change by geography, language, or rollout model.

## The Default Assumption Is Unsafe

Never assume a mainland recommendation works internationally, or that an international workflow is valid for mainland deployment.

## Questions That Change The Answer

| Question | Why it matters |
|----------|----------------|
| Is the target audience inside mainland China? | Product availability, residency, and launch steps may differ |
| Which language should docs and console steps use? | English mirrors can lag or omit detail |
| Does the user need local merchant settlement? | Payment and legal paths diverge quickly |
| Is the launch public, internal, or partner-only? | Approval and distribution rules change |
| Does traffic cross borders? | Latency, compliance, and architecture guidance change |

## Common Mainland Risks

- discovering late that the operational team cannot use the needed language or docs
- choosing an international product page that hides mainland-only steps
- assuming cross-border architecture is only a latency question
- ignoring entity, merchant, or compliance blockers until implementation

## Output Contract

For any region-sensitive answer, include:
- target geography
- whether the recommendation is mainland-safe, international-safe, or split
- which assumptions need legal, compliance, or operator confirmation
- what to verify before launch

## Escalation Rule

If the task touches payments, regulated data, identity, or public launch in mainland China, explicitly mark legal and compliance review as external dependencies.
