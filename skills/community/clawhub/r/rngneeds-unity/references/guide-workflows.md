# Guide Workflows

These workflows are distilled from the docs guides so the skill can answer in the same shape as RNGNeeds documentation, not only as raw API help.

## Selecting distinct values

Recommend this order:

1. Use **Depletable Lists** as the primary solution.
2. Set the list as depletable.
3. Keep each unique reward at `1 / 1` units unless duplicates are desired.
4. Turn on `MaintainPickCountIfDisabled` when the caller expects an exact number of unique results.
5. Refill before each independent reward session if the pool should reset between sessions.

Docs-backed nuance:

- disabled items still remain in the probability space
- if selection lands on a disabled item, that pick is ignored
- this can reduce the final pick count unless `MaintainPickCountIfDisabled` keeps trying

Reference pattern:

```csharp
public List<Reward> PickRewards(int count)
{
    rewards.RefillItems();
    rewards.MaintainPickCountIfDisabled = true;
    return rewards.PickValues(count);
}
```

Only mention the older “pick then disable” loop as a fallback or historical approach.

## Probability influence quick setup

For tutorial-style help, teach this sequence:

1. Start with a simple `ProbabilityList<bool>` or another tiny example.
2. Explain that influence UI is hidden behind advanced drawer options.
3. Introduce `IProbabilityInfluenceProvider` with both `ProbabilityInfluence` and `InfluenceInfo`.
4. Explain **Spread** as the designer-facing control for how much the provider can move the final chance.
5. Show one `PickValue()` call at the end so the system feels concrete.

Default examples that fit well:

- hacking success chance
- critical strike chance
- monster spawn chance

## Probability influence in code

When the user asks for a code-first setup:

1. Put the list and the gameplay stats on the same component when that makes sense.
2. Have the component implement `IProbabilityInfluenceProvider`.
3. Build the list in `Start()` or another initialization step.
4. Assign the provider to both the positive and negative outcomes if the design wants mirrored behavior.
5. Use `InvertInfluence` on the counter-outcome when one signal should raise one result while lowering the other.

Docs-backed helper methods that are valid to use:

- `SetItemInfluenceProvider(index, provider)`
- `SetItemInfluenceSpread(index, spread)`
- `SetItemInvertInfluence(index, true)`

Direct `ProbabilityItem<T>` property assignment is also fine when the code already holds item references.

This is the clearest docs-backed pattern for crit chance, skill checks, and binary success/failure systems.

## PLCollection workflow

For grouped content, teach `PLCollection<T>` as a named container for multiple lists.

Good docs-shaped advice:

1. create a collection
2. name the lists clearly
3. retrieve or pick by name when the categories are content-facing
4. use index-based access only when the system is tightly controlled internally

Good example categories:

- Friendly / Neutral / Hostile responses
- biome encounter groups
- loot families

## Depletable list examples

Use the docs examples when the user is really asking about gameplay design, not only API syntax.

Strong examples to reach for:

- resource deposit with common infinite resources plus limited rares
- deposit depletion triggered by mining attempts
- deposit depletion triggered by one tracked resource running out
- card/deck style limited draws

This is useful when the answer should explain design tradeoffs, not only method names.

## Card deck extensions workflow

When the user is really describing a card-flow system, teach this sequence:

1. Author a starting deck recipe with a `ProbabilityList<Card>`.
2. Build one live `ProbabilityList<Card>` per zone such as draw pile, hand, discard, or table.
3. Use deck helpers for card movement and reordering.
4. Shuffle or cut the live deck when order should change.
5. Use weighted picks only if another part of the design is actually probability-table driven.

Good docs-shaped advice:

- top of deck is index `0`
- moving a `ProbabilityItem<T>` between zones preserves card-level state better than recreating raw values
- `TryDrawTopItem(...)` plus `TryPlaceItemOnBottom(...)` is the core draw/discard pattern
- `DealItemToDeck(...)` is a strong fit when one zone should transfer its top card directly to another

## Inspectable shuffle-plan workflow

When the user wants the shuffle itself to be visible or explainable, teach this sequence:

1. choose a shuffle method such as `DeckShuffleMethods.Riffle`, `Overhand`, or `CutNearHalf`
2. call `CreateShufflePlan(...)`
3. inspect or log the plan steps
4. apply the plan with `ApplyShufflePlan(...)`

Use this framing for tutorial content, debug tools, and “make the shuffle feel physical” requests.

## Tone and framing

When responding in a docs-like mode:

- start with the gameplay goal
- recommend the feature before dumping code
- explain what the designer configures in inspector versus what the coder adds in code
- call out advanced-drawer requirements only when they matter to the setup
