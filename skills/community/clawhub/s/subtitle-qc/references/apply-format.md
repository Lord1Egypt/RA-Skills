# Edits file for `apply`

`apply FILE EDITS.json -o OUT` reads a JSON object with a `cues` list. Cue
numbers are 1-based positions in FILE (after `fix`, use the numbers from the
`--todo` file, which refer to the fixed file). Use `\n` for a line break.

```json
{
  "cues": [
    { "cue": 4, "text": "Fix it right there.\nThen export it." },

    { "cue": 7, "split": [
        { "text": "If a subtitle flashes by," },
        { "text": "the viewer has missed it." }
    ] },

    { "cue": 9, "split": [
        { "text": "First part.", "end": "00:01:02,400" },
        { "text": "Second part." }
    ] },

    { "cue": 12, "start": "00:01:10,000", "end": "00:01:12,500" }
  ]
}
```

- **Text edit**: `text` replaces the cue's lines. Times stay.
- **Split**: two or more parts inside the original span. Give `end` on every
  part but the last to set the times yourself; leave them all out to share the
  span by character count. Each next part starts 80 ms (`--min-gap`) after the
  previous one ends.
- **Time correction**: `start` and/or `end` (`HH:MM:SS,mmm`), alone or with
  `text`. Use it to resolve overlaps and reversed times that `check` reports as
  hard problems.

Times also accept `.` instead of `,` before the milliseconds.
