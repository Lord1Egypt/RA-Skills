# People, projects, filters and tags

The core rules in [SKILL.md](../SKILL.md) apply. Use Memo for shared knowledge and project associations.

## People and links

- Use `zm personal meetings people <name-or-email>` before choosing `--identity-id`; inspect ambiguity and
  `item.next` / `item.page.next_cursor`, even for empty pages. Names alone do not prove identity.
- `meetings link <ref> --participant-id <id> --person <uid>` previews a person association;
  `meetings link <ref> --event-id <id>` previews an event association. `--yes` applies authorized local changes;
  expected-current flags (`--expected-person`, `--expected-event-id`) guard against changed links. Additional target
  accounts must be explicit (`--source`). Never infer that a linked participant spoke a particular cue.
- `meetings context person:<id>` follows explicit identity links.
- `meetings task-proposal <ref> --type question|request|mention|promise` returns a proposal, not a saved task.

## Project evidence

`zm personal meetings projects evidence <project>` searches one existing canonical project's name, key and aliases,
including meetings without confirmed membership. Keep its coverage and frozen continuation; it reads the existing
index and neither refreshes it nor assigns project membership.

When the project is unknown, use the search hit's `meeting` field for the parent reference, not its transcript-cue
`ref`. `meetings projects scan <parent-ref> --json` compares one bounded local evidence page with existing global
project names, keys and aliases. It reads the shared project catalog explicitly, never creates membership, and needs
no model or network.

- Keep `metadata-title` hints apart from transcript citations, and retain ambiguity, fingerprints, omitted matches
  and both candidate and evidence coverage.
- Defaults: 20 cues, 10 candidates, 128 projects / 64 KiB catalog, 32 KiB cue packet, 16 KiB item. Hard maxima:
  100 cues, 10 candidates, 64 KiB stored bytes per read and 64 KiB item. Over-budget catalogs refuse; select a known
  project for evidence search instead.
- Resume with `evidence.coverage.next_cursor`, the same parent ref and `--cursor`; a title or project may repeat.
  Candidate truncation needs a larger limit or bytes, separately from cue continuation.
- No cues, byte truncation and no cursor means an oversized cue, not an absence of discussion. Over MCP the scan is
  the same command.
- Confirm reviewed links through `memo projects meetings link` with the exact stored meeting ID and
  `--account zoom:zm-profile:<label>`. An existing proposal needs its own Memo fingerprint; candidate and vocabulary
  fingerprints do not substitute for it. The scan itself saves nothing.

## Tag suggestions

The agent selects evidence and proposes a small list; no built-in model is invoked.

- Reuse Memo's released `vocabulary list 'kind:tag'`, `vocabulary check <name> --kind tag` and
  `vocabulary check --kind tag` with explicit catalog and comparison bounds.
- Preflight reuses exact canonical names and aliases and flags lexical alternatives. An incomplete audit is not
  uniqueness proof, and `create` is not approval to create. Similarity is a review hint, not a reason to merge.
- Keep supporting meeting and cue refs, vocabulary and creation fingerprints, and uncertain synonyms.
- Apply only reviewed existing labels through Memo with `--meeting <id> --account zoom:zm-profile:<label>`; new names
  and aliases require the existing reviewed vocabulary workflow. Do not add another label store or automatically
  accept a creation fingerprint. No tag write is part of Zoom preparation.
