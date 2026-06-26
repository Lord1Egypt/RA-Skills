# Recommendation Rules

## Ranking dimensions

Rank skills by this order:

1. direct functional fit
2. same user scenario
3. same tool/runtime pattern
4. overlapping keywords
5. general relevance

## Match labels

- `direct-match`: directly solves the asked function
- `strong-adjacent`: close enough, small adaptation needed
- `overlap`: similar space, partial duplication
- `weak-adjacent`: related but not primary

## Duplicate hints

Mark potential duplication when:
- names are near-synonyms
- descriptions mention the same platform or same action pattern
- one skill looks like a broader wrapper around another

## Recommendation writing

For each top skill, explain:
- what it is best at
- why it matches this query
- what its boundary is
