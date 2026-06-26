# Decision Guide

Start from the gameplay requirement, then map it to RNGNeeds.

## If the user wants one weighted random result

Use `ProbabilityList<T>` with `PickValue()`.

Examples: one loot drop, one enemy archetype, one dialogue bark.

## If the user wants multiple weighted results at once

Use `ProbabilityList<T>` with `PickValues(...)` and configure pick counts.

- fixed amount: `PickValues(count)`
- variable amount: `LinkPickCounts = false`, set `PickCountMin`, `PickCountMax`, optionally `PickCountCurve`

## If the user wants limited stock or true exhaustion without positional deck order

Use a **depletable list**.

Choose this for:

- unique rewards
- finite loot pool
- limited enemy reinforcements
- card pools where duplicate copies matter but live deck order does not
- any finite pool where order is not itself gameplay

Do **not** use repeat prevention for this.

## If the user wants a true ordered deck with top or bottom behavior

Use **Card Deck Extensions** on `ProbabilityList<T>`.

Choose this for:

- draw from top of deck
- place cards on top or bottom
- move cards between draw pile, hand, discard pile, graveyard, or table zones
- cut or reorder a deck while preserving card order

Reach for methods like `TryDrawTopItem(...)`, `TryPlaceItemOnTop(...)`, `TryPlaceItemOnBottom(...)`, `TryCut(...)`, and `DealItemToDeck(...)`.

## If the user wants an explainable or inspectable shuffle

Use **shuffle plans**.

Choose this for:

- physical-card-feel shuffles
- debugging or visualizing deck order changes
- tutorials that should explain what the shuffle did
- deterministic “plan first, apply second” workflows

Reach for `CreateShufflePlan(...)`, `ApplyShufflePlan(...)`, or `ShuffleDeck(..., DeckShuffleMethods.Riffle/Overhand/CutNearHalf)`.

## If the user wants “do not repeat twice in a row” but not finite stock

Use **repeat prevention**.

- best feel-first choice: `Repick`
- best distribution preservation: `Shuffle`
- fastest but more biased: `Spread`

## If the user wants probabilities to react to game state

Use **influence providers**.

Choose this for:

- health-based drops
- distance-based spawns
- reputation-based dialogue
- time-of-day enemy tables

Use `IProbabilityInfluenceProvider`, `InfluenceSpread`, and possibly `InvertInfluence`.

## If the user wants deterministic or replayable results

Use seeding.

- same list, same results: `KeepSeed = true`
- known sequence: assign `Seed`
- global custom rule: `RNGNeedsCore.SetSeedProvider(...)`

## If the user wants designer-friendly rarity knobs instead of raw percentages

Use weights.

Look at `Weight`, `BaseWeight`, `WeightsPriority`, and related weight conversion helpers.

## If the user wants grouped tables or multi-stage loot

Use nested lists or `PLCollection<T>`.

Choose this for:

- chest chooses category, then item
- biome chooses subtable, then encounter
- deck builder chooses a collection, then cards from it

## If the user wants exact top-of-deck or bottom-of-deck behavior

Do **not** use weighted random picks.

Prefer deck extensions first.

Use manual index traversal only when the user needs a lower-level custom flow that the built-in deck helpers do not already express.

## If the user is debugging “wrong probabilities”

Check these first:

1. influenced list normalization
2. disabled or depleted items
3. repeat prevention bias
4. `MaintainPickCountIfDisabled`
5. shared `PickValues()` result reuse
