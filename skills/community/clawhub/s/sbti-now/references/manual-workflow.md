# Manual Workflow

Use this fallback when the host AI can read the skill files but cannot execute Python scripts.
This keeps the skill portable across mainstream AI environments that support local resources but expose different execution toolchains.

## Resources

- Canonical data: `../data/question-bank.json`
- Script implementation: `../scripts/sbti_engine.py`

## Manual Steps

1. Ask the 30 standard questions from `questions`.
2. Ask the 2 hidden trigger questions from `specialQuestions`.
3. Sum the two answers for each dimension:
   - `2-3 => L`
   - `4 => M`
   - `5-6 => H`
4. Build the 15-dimension vector in `dimensionOrder`.
5. Compare the vector against each standard type pattern with Manhattan distance:
   - `L=1`
   - `M=2`
   - `H=3`
6. Convert the closest distance into similarity:
   - `similarity = round((1 - distance / 30) * 100)`
7. Apply overrides:
   - If the user drinks alcohol (`sq1 >= 2`) and drinks strong liquor like water (`sq2 == 3`), return `DRUNK`.
   - If the best standard similarity is below `60`, return `HHHH`.
8. Present:
   - personality code and localized name
   - similarity score
   - 15-dimension vector
   - top 3 matches
   - shareable text

## Notes

- This skill is entertainment-first, not clinical.
- Common lookup types include `CTRL`, `MALO`, `FAKE`, `MUM`, `LOVE-R`, `GOGO`, `IMSB`, `DRUNK`, and `HHHH`.
