# Lipsync Decision Tree

## Principle

Lipsync is an optional downstream enhancement, not a default requirement.

## When to enable lipsync

Enable only if at least one is true:
- the user explicitly asks for mouth-audio alignment
- the scene is clearly dialogue-bearing
- the clip will be judged mainly on talking realism

## When NOT to enable lipsync

Do not enable by default when:
- the user only wants ambience or narration
- quota is too tight for experimental retries
- the result may shorten or degrade a formally accepted main clip

## Decision path

### Case A — complete dialogue clip needed
- start from the full accepted base video
- generate dialogue audio from approved text
- run lipsync provider
- verify duration, naturalness, and scene integrity
- only replace the base clip if the result is clearly better

### Case B — provider returns shortened or degraded output
- keep the base clip as truth
- treat lipsync output as `lipsync-candidate`
- optionally use only the aligned portion in a later controlled fusion step
- never silently redefine the candidate as the final clip

### Case C — prompt already implies talking motion
If the video prompt says things like:
- opening mouth
- self-talking
- speaking naturally

then you must explicitly choose one of:
- add real dialogue
- regenerate without speaking cues
- keep it silent but warn the user about the mismatch

## Provider strategy

- Prefer the provider that preserves near-full clip duration when possible
- If a provider repeatedly collapses output into a short talking fragment, treat it as risky for full-clip replacement
