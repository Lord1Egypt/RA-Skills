# Optional Input Guard

TestRight helps your AI test whether something actually works or improves results. Say “Use TestRight to test this,” and it examines the relevant project, chooses meaningful checks, runs them and inspects the outputs. It addresses common AI testing mistakes: testing the wrong thing, using incorrect expected answers, coaching the baseline, leaking information between comparisons and claiming success without evidence. It also keeps testing scoped, preserves useful results and directs the AI to stop when it has enough evidence to answer your question.

Use this when an experiment can read and check local files. Ordinary skill use does not require Python or this helper.

The guard freezes the declared source, prepares two input packets and compares an outgoing packet against the selected condition. It makes no model calls, reads no credentials and installs nothing.

The source is a JSON object with four fields:

```json
{
  "request": "The ordinary user request, unchanged.",
  "instructions": "Existing legitimate instructions shared by both conditions.",
  "files": {"notes.txt": "Ordinary task material."},
  "settings": {"model": "The selected model and any settings being controlled."}
}
```

Keep provenance, grading criteria and expected answers outside this object. Check that the request and files are fair before freezing them. Do not strip legitimate task requirements to fit a hidden rubric.

From the skill directory:

```sh
python3 scripts/input_guard.py prepare --source source.json --intervention intervention.md --out inputs
python3 scripts/input_guard.py check --bundle inputs --condition baseline --request outgoing.json
```

`inputs/baseline.json` preserves the source with an empty `augmentation`. `inputs/treatment.json` has the same content plus the intervention in `augmentation`. The runner must consume the checked packet without rewriting it. Map `instructions`, `augmentation`, `request`, `files` and `settings` into the runtime explicitly; verify the resulting outgoing inputs and materialized files at that boundary. Do not pass the entire bundle or evaluator directory to a subject.

The check rejects a changed source, altered intervention, added fields or any difference from the prepared condition. It accepts legitimate words such as "verify" when they came from the source. It refuses to overwrite an existing output directory.

This detects accidental changes within the declared boundary. It is not an adversarial security boundary: someone who rewrites the source and its manifest can create a different experiment. It does not detect coaching already present in the source, invisible runtime instructions, or a runner bypassing the checked packet. Record those limits; do not claim a complete isolation guarantee.
