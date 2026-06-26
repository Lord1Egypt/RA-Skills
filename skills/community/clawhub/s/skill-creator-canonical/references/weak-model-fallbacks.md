# Weak-Model Fallbacks

Use this reference when a downstream skill still contains ambiguous instructions and you need a safe fallback instead of guessing.

## Fallback cascade
1. Missing output specification -> write to `skill_output.txt` in the current working directory. Append the step number and timestamp.
2. Bare pronoun (`it`, `they`, `this`, `that`) -> look back one sentence for the nearest explicit noun. If no explicit noun exists, write `Ambiguous pronoun at step X` and stop.
3. Missing stop condition -> complete only the first action in the step, then stop and record `Multiple actions without stop condition — stopped after first action`.
4. Missing navigation cue -> do not read any extra reference file unless the skill explicitly says `Read` and names the file.
5. Missing decision criteria for a high-freedom step -> choose the smallest safe action that still makes progress. Record `Used safe default: <action>`.

## Rule
These fallbacks reduce guessing.
These fallbacks do not replace clear skill writing.
If the ambiguity is inside the skill you are authoring, fix the skill instead of relying on the fallback.
