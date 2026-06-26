# Common Patterns

## Weighted loot drop

Use one `ProbabilityList<Item>`.

- one pick for a single drop
- multiple picks for bundles
- use weights if designers think in rarity tiers

Add repeat prevention only if back-to-back duplicates feel bad.

## Chest with categories

Use one higher-level table to choose category, then one table per category.

Good fits:

- `ProbabilityList<ItemCollection>` where each collection owns its own `ProbabilityList<Item>`
- `PLCollection<T>` when many named tables must be organized together

This keeps authoring modular and makes balancing easier.

## Gacha or summon banner

Use a `ProbabilityList<Character>` or `ProbabilityList<Reward>`.

Common additions:

- fixed multi-pulls with `PickValues(10)`
- seeded pulls for reproducible tests
- pick history if later systems need to inspect outcomes

If the design requires pity or guarantee logic, treat RNGNeeds as one part of the system and add explicit game logic around it.

## Dynamic spawn selection

Use `ProbabilityList<SpawnLocation>` or `ProbabilityList<EnemyType>` plus influence providers.

Example signals:

- distance to player
- current threat level
- time of day
- room occupancy

Use `InvertInfluence` when one signal should boost one option while suppressing another.

## AI decision weighting

Use `ProbabilityList<Action>` or `ProbabilityList<DamageType>`.

Good when the AI should feel varied but still biased toward context.

Pair with influence providers for health, cooldown state, stamina, or player distance.

## Dialogue, voice lines, and audio responses

Use `ProbabilityList<AudioClip>` or `ProbabilityList<string>`.

Add repeat prevention so the same bark does not fire twice in a row. Usually `Repick` is a good default.

## Unique rewards

Use a depletable list where each item has `Units = 1`.

This is the cleanest way to say “once claimed, it is gone until refill.”

## Finite pool with duplicates but no positional order

Use a depletable list where each unique item is one entry and `Units` holds the copy count.

This fits “draw without replacement” systems where exhaustion matters but top/bottom position does not.

That includes lightweight card-deck style workflows where the user wants multiple copies of the same card but does **not** care about live ordering, shuffling behavior, peeking, or moving cards between gameplay zones.

## True ordered card deck

Use Card Deck Extensions on `ProbabilityList<Card>` when the design cares about top-of-deck order.

Good fits:

- drawing from the top into a hand
- discarding to the bottom of another pile
- maintaining separate draw, hand, table, discard, or graveyard zones
- cutting, reversing, or otherwise reordering a live deck

Prefer deck helpers like `TryDrawTopItem(...)`, `TryPlaceItemOnTop(...)`, and `TryPlaceItemOnBottom(...)` over manual index code when the built-in flow already matches the gameplay.

## Inspectable physical-style shuffle

Use shuffle plans when the deck should behave like a physical stack and the shuffle itself should be explainable.

Good fits:

- card battlers or tabletop-inspired systems
- debug tools that need to show how the order changed
- tutorials that compare `Riffle`, `Overhand`, and `CutNearHalf`

Typical flow:

1. create a `DeckShufflePlan`
2. inspect or print its steps
3. apply it to the deck

## Multi-zone card flow

Use one `ProbabilityList<Card>` per gameplay zone.

Common zones:

- draw pile
- hand
- discard pile
- table / board
- graveyard / exile

Move `ProbabilityItem<T>` references between zones when card identity and current state should stay attached to the moved card.

## Distinct multi-pick rewards

Use depletable lists plus `PickValues(count)`.

This gives distinct results naturally while units remain.

If the requested count exceeds total remaining units, expect fewer results unless infinite items are mixed in.

## Weighted bool or gate checks

Use `ProbabilityList<bool>` for simple yes/no random gates.

Useful for:

- should spawn
- should crit
- should play idle animation

Keep it only for simple switches. If the design is richer than yes/no, model explicit outcomes instead.
