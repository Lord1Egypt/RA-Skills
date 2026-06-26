# Transcript Cleaning

## Standard

Produce a transcript that is easier to read than raw ASR while preserving the speaker's actual meaning.

## Clean Aggressively

- obvious ASR homophone errors when context makes the correction clear
- repeated filler caused by decoding artifacts
- broken punctuation
- fragmented lines that should be one sentence
- malformed names when context clearly identifies the person or product
- subtitle fragments that should be merged into normal prose

## Preserve Carefully

- uncertainty
- hedging
- jokes and tone when they matter
- direct quotes that reveal stance
- approximate wording when the exact correction is unclear

## Do Not Overclaim

If a phrase remains ambiguous after context review:

- keep the safer wording
- or mark it as uncertain

## Useful Heuristics

- Use repeated mentions later in the transcript to correct earlier names.
- Use topic continuity to disambiguate short clauses.
- If a term is still uncertain, prefer a minimally edited version over inventing a polished replacement.
- If the source is subtitles, first reconstruct readable sentences, then do speaker segmentation on the reconstructed text.
