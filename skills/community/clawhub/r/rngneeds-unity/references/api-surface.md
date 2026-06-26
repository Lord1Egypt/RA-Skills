# API Surface

This is a practical subset, not an exhaustive dump.

## `ProbabilityList<T>`

### Core configuration

- `ListName`
- `SelectionMethodID`
- `PreventRepeat`
- `ShuffleIterations`
- `PickCountMin`
- `PickCountMax`
- `LinkPickCounts`
- `MaintainPickCountIfDisabled`
- `PickCountCurve`
- `KeepSeed`
- `Seed`
- `CurrentSeed`
- `PickHistory`
- `LastPickCount`
- `LastPickedIndex`
- `LastPickedValue`
- `LastPickedIndices`
- `LastPickedValues`
- `BaseWeight`
- `WeightsPriority`
- `TotalWeight`
- `ItemCount`
- `EnabledItemsCount`
- `UnlockedItemsCount`
- `IsDepletable`
- `IsListInfluenced`

### List editing

- `AddItem(T value, bool enabled = true, bool locked = false)`
- `AddItem(T value, float baseProbability, bool enabled = true, bool locked = false)`
- `AddItem(T value, int weight, bool enabled = true, bool locked = false)`
- `AddItem(ProbabilityItem<T> item)`
- `AddItems(...)`
- `RemoveItem(...)`
- `RemoveItemAtIndex(...)`
- `ClearList()`
- `GetProbabilityItem(int index)`
- `TryGetProbabilityItem(int index, out ProbabilityItem<T> item)`
- `TryGetProbabilityItem(T value, out ProbabilityItem<T> item)`
- `IndexOf(...)`

### Probability and weights

- `GetItemProbability(int index)`
- `GetItemBaseProbability(int index)`
- `SetItemBaseProbability(int index, float baseProbability, bool normalize = true)`
- `AdjustItemBaseProbability(int index, float amount)`
- `NormalizeProbabilities()`
- `ResetAllProbabilities()`
- `GetItemWeight(int index)`
- `SetItemWeight(int index, int weight)`
- `CalculatePercentageFromWeights()`
- `ResetWeights()`
- `RecalibrateWeights()`

### Item state and influence helpers

- `SetItemEnabled(int index, bool enabled)`
- `SetAllItemsEnabled(bool enabled)`
- `SetItemLocked(int index, bool locked)`
- `SetAllItemsLocked(bool locked)`
- `SetItemProperties(int index, float baseProbability, bool enabled, bool locked)`
- `SetItemInfluenceProvider(int index, IProbabilityInfluenceProvider influenceProvider)`
- `SetItemInfluenceSpread(int index, Vector2 spread)`
- `SetItemInvertInfluence(int index, bool invertInfluence)`

### Selection

- `PickValue()`
- `TryPickValue(out T value)`
- `TryPickValueWithIndex(out T value, out int index)`
- `PickValues()`
- `PickValues(int pickCount)`
- `PickValues(int pickCountMin, int pickCountMax)`
- `PickValues(List<T> listToFill)`
- `PickValues(List<T> listToFill, int pickCount)`
- `PickValues(List<T> listToFill, int pickCountMin, int pickCountMax)`

### History and diagnostics

- `GetLastPickedIndices(List<int> listToFill)`
- `GetLastPickedValues(List<T> listToFill)`
- `SetHistoryCapacity(int capacity)`
- `ClearHistory()`
- `RunTest()`

### Depletable list helpers

- `RefillItems()`
- `SetAllItemsUnits(int units)`
- `SetAllItemsMaxUnits(int units)`
- `SetAllItemsDepletable(bool depletable)`
- `SetItemDepletable(int index, bool depletable = true, int units = 1, int maxUnits = 1)`
- `SetAllItemsDepletableProperties(bool depletable = true, int units = 1, int maxUnits = 1)`
- `GetTotalUnits()`
- `GetTotalMaxUnits()`

## `ProbabilityItem<T>`

### Core properties

- `Value`
- `BaseProbability`
- `Probability`
- `Enabled`
- `Locked`
- `Weight`

### Influence

- `InfluenceSpread`
- `InvertInfluence`
- `InfluenceProvider`
- `ValueIsInfluenceProvider`
- `IsInfluencedItem`
- `GetInfluencedProbability(float influence)`

### Depletable item state

- `IsDepletable`
- `Units`
- `MaxUnits`
- `IsDepleted`
- `IsSelectable`
- `Refill()`
- `SetDepletable(bool depletable = true, int units = 1, int maxUnits = 1)`

## Card Deck Extensions on `ProbabilityList<T>`

Use these when the list should behave like an ordered deck, not a weighted table.

### Peek and draw

- `PeekTopItem()`
- `TryPeekTopItem(out ProbabilityItem<T> item)`
- `PeekTop()`
- `TryPeekTop(out T value)`
- `PeekAtItem(int index)`
- `TryPeekAtItem(int index, out ProbabilityItem<T> item)`
- `DrawTopItem()`
- `TryDrawTopItem(out ProbabilityItem<T> item)`
- `DrawAtItem(int index)`
- `TryDrawAtItem(int index, out ProbabilityItem<T> item)`

### Place and move

- `PlaceItemOnTop(ProbabilityItem<T> item)`
- `TryPlaceItemOnTop(ProbabilityItem<T> item)`
- `PlaceItemOnBottom(ProbabilityItem<T> item)`
- `TryPlaceItemOnBottom(ProbabilityItem<T> item)`
- `PlaceAtItem(int index, ProbabilityItem<T> item)`
- `TryPlaceAtItem(int index, ProbabilityItem<T> item)`
- `DealItemToDeck(ProbabilityList<T> target)`
- `TryDealItemToDeck(ProbabilityList<T> target, out ProbabilityItem<T> item)`

### Reorder and shuffle

- `TryCut(int index)`
- `TryReverseDeck()`
- `CreateShufflePlan()`
- `CreateShufflePlan(IDeckShuffleMethod shuffleMethod)`
- `ApplyShufflePlan(DeckShufflePlan shufflePlan)`
- `TryApplyShufflePlan(DeckShufflePlan shufflePlan)`
- `ShuffleDeck()`
- `TryShuffleDeck()`
- `ShuffleDeck(IDeckShuffleMethod shuffleMethod)`
- `TryShuffleDeck(IDeckShuffleMethod shuffleMethod)`
- `RiffleShuffle()`
- `TryRiffleShuffle()`
- `OverhandShuffle()`
- `TryOverhandShuffle()`
- `CutNearHalf()`
- `TryCutNearHalf()`

### Deck shuffle planning types

- `IDeckShuffleMethod`
- `DeckShufflePlan`
  - `MethodId`
  - `DisplayName`
  - `Steps`
  - `FinalOrder`
- `DeckShuffleStep`
  - `StepType`
  - `Description`
  - `SourceIndices`
  - `ResultIndices`
- `DeckShuffleMethods`
  - `Default`
  - `Uniform`
  - `Riffle`
  - `Overhand`
  - `CutNearHalf`

## `PLCollection<T>`

Use this when many named lists belong together.

- `AddList(...)`
- `RemoveList(...)`
- `GetList(...)`
- `SetListName(...)`
- `ClearCollection()`
- `ClearList(...)`
- `ClearAllLists()`
- `MoveListUp(int index)`
- `MoveListDown(int index)`
- `PickValueFrom(...)`
- `PickValuesFrom(...)`
- `PickValuesFromAll()`
- `RefillList(...)`
- `RefillAllLists()`

## `IProbabilityInfluenceProvider`

Implement:

- `float ProbabilityInfluence`
- `string InfluenceInfo`

Return a meaningful `-1..1` influence value and a designer-readable explanation.

## `ISelectionMethod`

Implement when built-in selection behavior is not enough.

- `string Identifier`
- `string Name`
- `NativeList<int> SelectItems(IProbabilityList probabilityList, int pickCount)`

Register it with `RNGNeedsCore.RegisterSelectionMethod(...)`.

## `RNGNeedsCore`

Useful static entry points:

- `DefaultSelectionMethodID`
- `RegisteredSelectionMethods`
- `NewSeed`
- `SetSeedProvider(ISeedProvider seedProvider)`
- `ResetSeedProvider()`
- `RegisterSelectionMethod(ISelectionMethod selectionMethod)`
- `GetSelectionMethod(string identifier)`
- `WarmupHistoryEntries(int count)`
