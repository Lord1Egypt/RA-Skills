# Write user documentation

1. Start with the reader's task and intended result. Put prerequisites before
   commands and expected results after them. Include one minimal working example
   the reader can follow from start to finish.
2. Verify commands, options, defaults, and limitations against the implementation.
   Preserve exact names in code formatting. Distinguish tested behavior from
   assumptions, and explain limitations beside the action they affect.
3. Edit for clarity. Use direct verbs, short sentences, normal word spacing, and
   one topic per paragraph. Replace vague claims such as "robust" or "seamless"
   with the specific behavior the reader needs to know.
4. Organize for scanning. Use sentence-case headings, numbered steps for ordered
   tasks, and tables for settings or comparisons. Link to detailed references
   instead of repeating them. Keep retry history, pipeline IDs, commit hashes,
   and agent bookkeeping in the MR or work log; user guides describe current
   behavior.
5. Read the rendered page as a user before committing. Check that prerequisites,
   commands, expected results, and links are easy to find. Remove repeated
   summaries, irrelevant implementation details, and decorative emphasis. Run
   the repository's existing documentation lint and build checks.

## Example

Before:

> The chart enables post-installation validation of service discoverability.

After:

> After installation, run `helm test openclaw -n openclaw` to check that cluster
> DNS can resolve the Service.
