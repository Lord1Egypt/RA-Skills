# Topic boundary guide

Use this reference when the relationship between requests is ambiguous.

## Usually the same work unit

- A user moves from analysis to interpretation, figure review, manuscript wording, or client communication for the same dataset.
- A debugging request changes from the observed error to configuration, versions, commands, or validation of the same system.
- A project moves through adjacent steps, such as 16S QC, ordination, PERMANOVA, differential abundance, and explaining the results.
- The user asks a general-looking follow-up whose answer depends on the session's files, parameters, or prior conclusion.

Do not recommend a new session in these cases merely because vocabulary changes.

## Usually a boundary candidate

- A completed annotation/debugging task is followed by an independent statistics or literature question.
- The user switches to another customer, experiment, dataset, codebase, paper, or deliverable with no shared dependencies.
- The user explicitly says the previous topic is done and asks to begin something else.

Example: after resolving a SnpEff/felCat8 configuration issue, a question about routine use of Kruskal–Wallis tests in metabolomics is normally a boundary candidate.

## Ambiguous cases

Continue when a new question could materially depend on the old project. If that dependency cannot be inferred safely, ask one short question rather than making a recommendation based on weak semantic similarity.

For a parked but unfinished topic, prefer a handoff only if switching would make resumption easier. Do not call it completed.

## Handoff quality checks

Before presenting a handoff, check that it:

- distinguishes confirmed facts from assumptions;
- gives a next session enough context to start productively;
- excludes secrets unless they are necessary and the user explicitly expects them to be carried;
- names unresolved items instead of hiding them; and
- remains brief enough to be cheaper and easier to use than the original conversation.
