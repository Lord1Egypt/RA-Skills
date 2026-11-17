# Clarification Strategy

Use targeted clarification to resolve expensive ambiguity without turning the
task into a questionnaire.

## Build the Intent Model

Recover these fields from the request, repository, and supplied artifacts:

| Field | Question it answers |
|---|---|
| User and context | Who is using this, and under what conditions? |
| Job | What outcome must the user achieve? |
| Primary action | What should be easiest to find and complete? |
| Information hierarchy | What must be understood first, second, and later? |
| Content shape | Is the real content short, long, sparse, dense, or variable? |
| Frequency | Is this occasional guidance or repeated operational work? |
| Constraints | What platform, brand, accessibility, or technical limits apply? |
| Anti-goals | What must the result not feel like or encourage? |
| Success evidence | What visible or behavioral result would prove the intent? |

Mark each material decision `CONFIRMED`, `INFERRED`, `PROPOSED`, or `OPEN`.

## Choose Questions by Information Gain

Prioritize a question when all three are high:

1. **Materiality:** different answers produce meaningfully different user
   outcomes, structure, or interaction.
2. **Uncertainty:** the request and repository do not already support one answer.
3. **Cost of reversal:** choosing incorrectly would cause broad or expensive
   rework.

Ask one to three questions at a time. Resolve the highest-impact branch before
asking about details that depend on it.

Do not ask:

- for a value already defined by tokens or an existing pattern
- for CSS properties when the user can choose an observable outcome
- broad taste questions without examples or consequences
- every possible state before identifying the primary task

## Greenfield Ambiguity Checkpoint

In greenfield mode, stop before choosing a final page structure when the primary
user, job, action, or content shape is unknown and different answers would
produce different architecture. Ask the smallest set of questions that selects
the product model.

Until those answers are available, limit the response to repository
observations, one to three questions, and optional brief `PROPOSED` hypotheses.
Do not provide a completed design brief or recommend one final direction.

Do not convert subjective words into unsupported pixel values, colors, fonts,
or interaction flows. Present such choices only as labeled `PROPOSED` options
with the consequence of each, after the product model is sufficiently clear.

## Offer Concrete Choices

Make options mutually distinguishable and tie them to use:

> This page could behave as:
>
> - **Operational workspace:** compact rows, persistent filters, actions close
>   to the data; faster for repeated work but visually denser.
> - **Review surface:** stronger grouping, more explanatory context, fewer
>   visible actions; easier to scan but slower for bulk operations.
>
> The surrounding product uses the operational pattern. Which job is primary?

Recommend one option when evidence supports it. Do not offload every decision to
the user.

## Resolve Subjective Language

For a phrase such as "premium" or "clean":

1. treat the phrase as a desired perception
2. identify the design dimensions that could create that perception
3. use repository evidence to eliminate incompatible interpretations
4. present observable alternatives for the remaining material ambiguity
5. confirm the outcome, not a raw CSS value

When words remain inadequate, use references, sketches, wireframes, or rendered
variants. Ask what should be kept and rejected in each artifact instead of
asking whether the whole artifact is "good."

## Stop Clarifying

Stop asking and proceed when:

- the primary task and hierarchy are clear
- repository evidence answers the implementation conventions
- no high-cost `OPEN` decision remains
- remaining uncertainty is local, reversible, and can be stated as a proposal

Keep unresolved uncertainty visible in the UI Intent Contract.
