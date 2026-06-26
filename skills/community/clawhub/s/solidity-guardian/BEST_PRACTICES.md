# Solidity Security Best Practices

A comprehensive guide for writing secure smart contracts. Based on patterns from Trail of Bits, OpenZeppelin, Consensys, and real-world audits.

## 🔴 Critical: Must Follow

### 1. Reentrancy Protection

**Problem:** External calls can re-enter your contract before state is updated.

```solidity
// ❌ VULNERABLE
function withdraw() external {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;  // State updated AFTER external call
}

// ✅ SECURE
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

function withdraw() external nonReentrant {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;  // State updated BEFORE external call
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

**Rules:**
- Always use `ReentrancyGuard` on functions with external calls
- Follow checks-effects-interactions pattern
- Update state BEFORE making external calls
- Use pull-over-push for payments when possible

### 2. Access Control

**Problem:** Sensitive functions accessible by anyone.

```solidity
// ❌ VULNERABLE
function setPrice(uint256 newPrice) external {
    price = newPrice;  // Anyone can call!
}

// ✅ SECURE
import "@openzeppelin/contracts/access/Ownable.sol";

function setPrice(uint256 newPrice) external onlyOwner {
    price = newPrice;
}
```

**Rules:**
- Use `Ownable` or `AccessControl` from OpenZeppelin
- Apply modifiers to all admin functions
- Consider timelocks for critical operations
- Implement two-step ownership transfer

### 3. Input Validation

```solidity
// ❌ VULNERABLE
function setRecipient(address _recipient) external onlyOwner {
    recipient = _recipient;  // Could be set to zero address!
}

// ✅ SECURE
function setRecipient(address _recipient) external onlyOwner {
    require(_recipient != address(0), "Zero address");
    recipient = _recipient;
}
```

**Rules:**
- Always validate addresses are non-zero
- Check array lengths match when processing pairs
- Validate amounts are within expected ranges
- Use SafeERC20 for token transfers

## 🟠 High: Should Follow

### 4. Safe External Calls

```solidity
// ❌ RISKY - Some tokens don't return bool
token.transfer(recipient, amount);

// ✅ SAFE
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;

token.safeTransfer(recipient, amount);
```

### 5. Integer Safety

```solidity
// For Solidity < 0.8.0
// ❌ VULNERABLE
uint256 result = a + b;  // Can overflow!

// ✅ SAFE
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
using SafeMath for uint256;
uint256 result = a.add(b);

// For Solidity >= 0.8.0
// ✅ Built-in overflow checks
uint256 result = a + b;  // Reverts on overflow
```

### 6. Avoid tx.origin

```solidity
// ❌ VULNERABLE - Phishing attack vector
require(tx.origin == owner, "Not owner");

// ✅ SECURE
require(msg.sender == owner, "Not owner");
```

### 7. Secure Randomness

```solidity
// ❌ VULNERABLE - Predictable/manipulable
uint256 random = uint256(keccak256(abi.encodePacked(
    block.timestamp, 
    block.difficulty
)));

// ✅ SECURE - Use Chainlink VRF
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

function getRandomNumber() internal returns (bytes32 requestId) {
    return requestRandomness(keyHash, fee);
}
```

## 🟡 Medium: Consider Following

### 8. Pin Pragma Version

```solidity
// ❌ RISKY - Different compiler versions
pragma solidity ^0.8.0;

// ✅ BETTER - Pinned version
pragma solidity 0.8.20;
```

### 9. Timestamp Considerations

```solidity
// ⚠️ ACCEPTABLE for coarse timing (days, hours)
require(block.timestamp >= unlockTime, "Locked");

// ❌ RISKY for fine-grained timing or randomness
uint256 random = block.timestamp % 10;
```

Miners can manipulate `block.timestamp` by ~15 seconds. Acceptable for subscription billing, not for gambling.

### 10. Avoid Loops with External Calls

```solidity
// ❌ VULNERABLE - DoS if one transfer fails
function distributeRewards(address[] calldata users) external {
    for (uint i = 0; i < users.length; i++) {
        payable(users[i]).transfer(rewards[users[i]]);
    }
}

// ✅ SECURE - Pull pattern
mapping(address => uint256) public pendingRewards;

function claimReward() external {
    uint256 amount = pendingRewards[msg.sender];
    pendingRewards[msg.sender] = 0;
    payable(msg.sender).transfer(amount);
}
```

## 🔵 Low: Best Practices

### 11. Emit Events

```solidity
event PriceUpdated(uint256 oldPrice, uint256 newPrice);

function setPrice(uint256 newPrice) external onlyOwner {
    uint256 oldPrice = price;
    price = newPrice;
    emit PriceUpdated(oldPrice, newPrice);  // Enable off-chain tracking
}
```

### 12. Use Named Constants

```solidity
// ❌ UNCLEAR
uint256 fee = amount * 25 / 10000;

// ✅ CLEAR
uint256 constant FEE_BPS = 25;
uint256 constant BPS_DENOMINATOR = 10000;
uint256 fee = amount * FEE_BPS / BPS_DENOMINATOR;
```

### 13. Explicit Visibility

```solidity
// ❌ IMPLICIT
function _internalHelper() { }

// ✅ EXPLICIT
function _internalHelper() internal { }
```

### 14. NatSpec Documentation

```solidity
/// @notice Transfers tokens to a recipient
/// @param recipient The address receiving tokens
/// @param amount The amount to transfer
/// @return success Whether the transfer succeeded
function transfer(address recipient, uint256 amount) 
    external 
    returns (bool success) 
{
    // ...
}
```

## 📋 Pre-Deployment Checklist

### Security
- [ ] All external/public functions reviewed for access control
- [ ] Reentrancy guards on functions with external calls
- [ ] SafeERC20 used for token transfers
- [ ] Zero address checks on address parameters
- [ ] No tx.origin authentication
- [ ] Chainlink VRF for randomness (if needed)

### Code Quality  
- [ ] Pragma pinned to specific version
- [ ] All functions have explicit visibility
- [ ] Events emitted for state changes
- [ ] NatSpec on public functions
- [ ] No magic numbers

### Testing
- [ ] Unit tests for all functions
- [ ] Edge case tests (0 amounts, max values)
- [ ] Access control tests
- [ ] Reentrancy tests
- [ ] Fuzzing with Foundry/Echidna

### External Review
- [ ] Run Slither: `slither .`
- [ ] Run Solidity Guardian: `node analyze.js ./contracts/`
- [ ] Manual review by second developer
- [ ] Consider professional audit for high-value contracts

## 📚 Resources

- [Trail of Bits - Building Secure Contracts](https://github.com/crytic/building-secure-contracts)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [Consensys Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [SWC Registry](https://swcregistry.io/)
- [Slither](https://github.com/crytic/slither)
- [Foundry Book - Security](https://book.getfoundry.sh/forge/security)

---

*Security is not a feature, it's a requirement.* 🔐
