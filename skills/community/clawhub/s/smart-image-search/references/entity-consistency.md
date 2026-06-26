# Entity consistency

Use entity consistency to avoid selecting results that are official-looking but about the wrong thing.

## Goal

Keep results aligned with the core entity in the cleaned query.

## Practical rules

- Split the cleaned core query into meaningful tokens.
- Distinguish:
  - strong entity tokens: names, mascot names, school names, brand names
  - weak modifier tokens: image, photo, hd, official, logo, wallpaper, avatar, meme
- Require at least one strong entity token match for most queries.
- For multi-token entity queries, strongly prefer candidates matching 2+ strong tokens.
- If a candidate matches only generic official words but none of the strong entity tokens, penalize heavily.

## Official mode

For `official` intent, do not let whitelist words such as `official`, `baike`, `logo`, or `emblem` outweigh entity mismatch.
A page can look official and still be wrong.

## Examples

Query: `acme mascot official image`
- `acme` and `mascot` are strong entity tokens.
- A candidate about `Acme Robotics` may be related but not identical.
- A candidate containing `acme mascot` should outrank a generic `acme` result.
- A candidate containing neither `acme` nor `mascot` should be strongly penalized.
