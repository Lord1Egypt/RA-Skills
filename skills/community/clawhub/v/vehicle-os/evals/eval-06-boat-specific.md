# Eval 06: Non-Car Vehicle (Boat)

## Input
"Adding our boat. It's a 2020 Boston Whaler 170 Montauk with a Mercury 90hp outboard. We keep it on a trailer at the house."

## Expected Behavior
1. Creates vehicle profile: 2020 Boston Whaler 170 Montauk, type: boat, Mercury 90hp outboard
2. Notes it's trailer-kept (affects maintenance: no bottom paint needed)
3. Suggests boat-specific maintenance schedule: engine oil, lower unit gear oil, impeller, fuel filter, winterization, spring commissioning
4. Does NOT suggest car maintenance items (tire rotation, cabin filter, etc.)
5. Adjusts for trailer-kept vs. in-water (skips bottom paint schedule)

## What to Watch For
- Does it apply the correct boat schedule, not the car schedule?
- Does it account for trailer storage (no bottom paint)?
- Does it capture the engine details (Mercury 90hp)?
