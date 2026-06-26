# Core Concepts

## Mental model

RNGNeeds centers on `ProbabilityList<T>`, a list of `ProbabilityItem<T>` entries. Each item has a value plus selection metadata.

Treat it as a gameplay-facing random system, not just a helper for `Random.Range`.

## Key terms

- **Probability List**: the container of possible outcomes.
- **Probability Item**: one outcome plus configuration.
- **BaseProbability**: the designed probability before runtime adjustment.
- **Probability**: the effective probability after influence and normalization.
- **Selection Method**: the algorithm used to select values.
- **Pick Count**: how many values are selected in one operation.
- **Repeat Prevention**: logic that reduces or removes consecutive repeats.
- **Influence Provider**: an object implementing `IProbabilityInfluenceProvider` that pushes odds up or down.
- **Depletable List**: a list where item units can be consumed.
- **Deck Extensions**: order-centric helpers that treat a `ProbabilityList<T>` like a card deck, with top at index `0` and bottom at the last index.
- **Pick History**: recent picks stored by index and reused by helper APIs.

## Base probability vs resulting probability

Do not equate the number shown in `BaseProbability` with what the player actually experiences.

- Runtime influence can push an item up or down.
- If totals exceed 100%, RNGNeeds normalizes the list before selecting.
- Disabled or depleted items can change perceived outcomes and pick counts.
- Repeat prevention can intentionally distort back-to-back behavior.

## Disabled items

Disabled items still exist in the probability space. A selection can land on them, then yield no usable result.

This means:

- returned pick count can be lower than requested
- single-value picks can fail
- `MaintainPickCountIfDisabled` trades exact distribution for “keep filling until count is reached” behavior

## Depletable lists

Use depletable lists for finite stock.

- The list must have `IsDepletable = true`.
- Individual items also have depletable state plus `Units` and `MaxUnits`.
- Consuming units makes depleted items behave like unavailable entries.

Use this for unique rewards, limited spawns, finite stock, or deck-like pools where exhaustion and duplicate-copy counts matter but live top/bottom order does not.

This means a simple card pool can still be modeled as a depletable list when the user does not care about shuffling, peeking, cutting, draw-pile vs discard-pile flow, or any other order-centric behavior.

## Deck extensions

Use deck extensions when **order itself** is part of the gameplay.

Typical signals:

- draw from the top
- place on the bottom
- move cards between draw pile, hand, discard, or table zones
- cut or shuffle a deck as an ordered stack
- inspect or explain how a shuffle changed the deck

Important consequences:

- top of deck is index `0`
- these operations are **not** weighted picks
- shuffle helpers use seeded index-based randomness to reorder items
- moving or reordering cards changes positional gameplay, not just probabilities

Use ordinary `PickValue()` or `PickValues()` when the user wants weighted outcome selection. Use deck extensions when the user wants card-flow or positional behavior.

## Repeat prevention

Use repeat prevention when the pool is still conceptually infinite but consecutive duplicates feel bad.

- `Spread`: fastest, strongest bias
- `Repick`: moderate speed, lower bias
- `Shuffle`: preserves distribution best, reduces repeats after selection, weaker across separate picks

Do not use repeat prevention as a substitute for finite inventory.

## Influence

Influence is a `float` from `-1` to `1` supplied by `IProbabilityInfluenceProvider`.

Each influenced item maps that input through its **Influence Spread**.

Important consequences:

- if one item is influenced, the list is treated as influenced
- probabilities are recalculated before picks
- positive influence on one item can lower others after normalization
- `InvertInfluence` lets the same provider push different items in opposite directions

## Seeding and determinism

Each pick uses a seed.

- default behavior: generate a new seed each selection
- `KeepSeed = true`: reuse the same seed
- `Seed = 1337`: set a deterministic seed when `KeepSeed` is on
- custom global behavior: implement `ISeedProvider` and call `RNGNeedsCore.SetSeedProvider(...)`

Use this for replays, debugging, and reproducible tests.

## Pick history

History stores indices, then helper properties expose values.

This matters because:

- `LastPickedValue` and `LastPickedValues` come from history
- history-aware behavior affects repeat prevention
- removing items clears history safety assumptions because indices change

## Shared result lists

`PickValues()` returns a shared internal list reference.

If you need to preserve results, copy them into your own list.

## Weights

RNGNeeds also supports weights.

Use weights when designers think in relative rarity rather than exact percentages. Keep in mind that weights are a friendlier authoring surface, not magically different randomness.
