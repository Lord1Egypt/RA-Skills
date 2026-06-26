# Common Smart Contract Vulnerabilities

This reference outlines common vulnerabilities in smart contract development across Solidity and Go (Cosmos SDK / Hyperledger). Use this when analyzing code.

## Solidity Vulnerabilities

1. **Reentrancy**: Occurs when a contract calls an external contract before resolving state changes (e.g., updating balances).
    - *Detection*: Look for external calls (`call.value`, `transfer`, `send`) before state modifications.
    - *Mitigation*: Use the Checks-Effects-Interactions pattern or ReentrancyGuard.

2. **Arithmetic Over/Underflow**: While Solidity >=0.8.0 handles this natively, it can still occur in older versions, assembly blocks, or when `unchecked` is used.
    - *Detection*: Math operations without `SafeMath` in older code, or unsafe `unchecked` blocks.

3. **Access Control Flaws**: Improper use of `public` vs `private`, or missing `onlyOwner`/role modifiers on sensitive functions.
    - *Detection*: Functions that mint tokens, withdraw funds, or change state without access restrictions.

4. **Front-Running (Transaction-Ordering Dependence)**: Malicious actors can observe pending transactions and submit their own with a higher gas price to get executed first.
    - *Detection*: Marketplaces, DEXs without slippage limits, or logic depending on transaction order.

## Go (Cosmos SDK / Hyperledger) Vulnerabilities

1. **Deterministic Execution Flaws**: In Cosmos/Hyperledger, all nodes must reach the same state. Using non-deterministic functions (like system time, random number generators, or iterating over unsorted maps) breaks consensus.
    - *Detection*: Usage of `time.Now()`, `math/rand`, or iterating over standard Go `map`.
    - *Mitigation*: Use block time from context, deterministic RNG from chain state, and sort map keys before iteration.

2. **State Transition/Access Control**: Unauthorized state modifications.
    - *Detection*: Missing permission checks in message handlers (`Msg`). Ensure `msg.GetSigners()` matches the required roles.

3. **Denial of Service (DoS) via State Bloat**: Allowing users to write unlimited data to state without appropriate costs.
    - *Detection*: Unbounded loops over state entries, or lack of fees for storing data.
