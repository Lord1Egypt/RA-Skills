# Solidity 0.8.x Reference

## Contract Structure

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract MyContract {
    // State variables (storage — expensive)
    address public owner;
    uint256 private _value;
    mapping(address => uint256) public balances;

    // Events
    event ValueSet(address indexed by, uint256 value);

    // Custom errors (cheaper than revert strings)
    error Unauthorized();
    error InvalidAmount(uint256 got, uint256 min);

    // Modifiers
    modifier onlyOwner() {
        if (msg.sender != owner) revert Unauthorized();
        _;
    }

    constructor(uint256 initialValue) {
        owner = msg.sender;
        _value = initialValue;
    }

    function setValue(uint256 v) external onlyOwner {
        _value = v;
        emit ValueSet(msg.sender, v);
    }

    function getValue() external view returns (uint256) {
        return _value;
    }
}
```

## Data Locations

| Location | Where | Cost | Use when |
|----------|-------|------|----------|
| `storage` | blockchain | expensive (SLOAD/SSTORE) | persistent state |
| `memory` | function execution | medium | temporary data in function |
| `calldata` | function input | cheapest | read-only params |
| `stack` | EVM stack | free | local vars (max 16) |

```solidity
// calldata for read-only array params — cheaper than memory
function sum(uint256[] calldata nums) external pure returns (uint256 total) {
    for (uint256 i; i < nums.length; ) {
        unchecked { total += nums[i]; i++; }
    }
}
```

## Common Patterns

### Reentrancy Guard
```solidity
uint256 private _locked = 1;
modifier nonReentrant() {
    require(_locked == 1, "Reentrant");
    _locked = 2;
    _;
    _locked = 1;
}
// Or use OZ's ReentrancyGuard
```

### Pull-over-push (safe ETH transfer)
```solidity
mapping(address => uint256) public pendingWithdrawals;

function withdraw() external {
    uint256 amount = pendingWithdrawals[msg.sender];
    pendingWithdrawals[msg.sender] = 0;   // zero before transfer
    (bool ok,) = msg.sender.call{value: amount}("");
    require(ok, "Transfer failed");
}
```

### Access Control
```solidity
// Simple
address public owner;
modifier onlyOwner() { require(msg.sender == owner); _; }

// Role-based (OZ)
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
```

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Stack too deep` | >16 local vars | Use structs, split function |
| `Contract size limit` | Bytecode >24kb | Split into libraries |
| `Out of gas` | Unbounded loops | Add pagination or limits |
| `Invalid opcode` | Division by zero, assert | Check conditions first |
| `Arithmetic overflow` | Math overflow pre-0.8 | 0.8+ checks by default; use `unchecked` intentionally |

## Storage Layout (Important for Upgrades)

```solidity
// Slots are assigned in order of declaration
uint256 a;    // slot 0
uint256 b;    // slot 1
address c;    // slot 2 (takes 20 bytes of 32-byte slot)
uint96 d;     // slot 2 (packed with c — they fit in 32 bytes)

// Mappings: keccak256(key . slot)
// Dynamic arrays: length at slot N, elements at keccak256(N)+i
```

## Interfaces and ABIs

```solidity
interface IERC20 {
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address) external view returns (uint256);
}

// Call any ERC-20 without importing the full contract
IERC20(tokenAddr).transfer(recipient, amount);
```
