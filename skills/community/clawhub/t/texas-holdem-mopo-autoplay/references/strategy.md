# ABC Baseline (Runtime, legality-first)

## Priority order
1) **Legality first**
2) Strategy second

## Non-negotiable legality rules
- If `to_call > 0`: `check` is illegal.
- If `to_call == 0`: prefer `check` unless raising by strategy.
- If legal action set is provided, action must be inside that set.

## Simple ABC heuristic
- Premium / strong made hand: raise (respect min_raise / min_raise_to)
- Medium hand: call/check
- Weak hand facing bet: fold
- No bet to call: check

## Sizing
- Prefer 50%-75% pot for value/semi-bluff raises
- Never below min raise
- Never above stack
- For non-raise actions (`check/call/fold`), always send `amount=0`

## Fallback ladder
- Preferred action illegal -> try legal `call` (if `to_call>0`)
- Else legal `check` (if `to_call==0`)
- Else `fold`
- Never resubmit same known-invalid action repeatedly
