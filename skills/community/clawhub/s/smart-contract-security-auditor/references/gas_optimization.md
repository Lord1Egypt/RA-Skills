# Gas and Performance Optimization

This reference provides strategies for optimizing resource usage (Gas in EVM, execution cost in Cosmos/Hyperledger).

## Solidity Gas Optimization

1. **Storage Optimization**:
    - Pack variables in structs (e.g., using `uint128` next to `uint128` takes 1 slot instead of 2).
    - Avoid repeatedly reading/writing storage variables in loops. Cache them in `memory` or `calldata`.

2. **Data Location**:
    - Use `calldata` instead of `memory` for read-only function arguments, especially strings and arrays.

3. **Efficient Operations**:
    - `++i` is generally cheaper than `i++`.
    - `x = x + y` is cheaper than `x += y` (in some older compiler versions, but less relevant in newer).
    - Short-circuiting in `require` statements (put the cheapest check first).
    - Use custom errors (`error MyError(); require(..., MyError())`) instead of string revert messages.

## Go (Cosmos SDK / Hyperledger) Optimization

1. **State Access**:
    - Minimize KVStore reads and writes. Group operations if possible.
    - Use appropriate key structures to allow prefix iteration instead of scanning entire stores.

2. **Serialization**:
    - Avoid expensive serialization/deserialization in tight loops.

3. **Memory Management**:
    - Reuse slices instead of constantly reallocating, especially when processing large blocks of transactions.
