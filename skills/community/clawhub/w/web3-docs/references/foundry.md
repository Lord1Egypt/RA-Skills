# Foundry Reference

## Project Setup

```bash
curl -L https://foundry.paradigm.xyz | bash && foundryup
forge init my-project && cd my-project
```

Structure:
```
my-project/
├── src/          ← contracts
├── test/         ← Solidity tests
├── script/       ← deployment scripts
├── lib/          ← dependencies (git submodules)
└── foundry.toml  ← config
```

## Common Commands

```bash
forge build                          # compile
forge test                           # run all tests
forge test -vvv                      # verbose (shows traces)
forge test --match-test testFoo      # run specific test
forge test --fork-url $RPC_URL       # fork mainnet
forge coverage                       # coverage report
forge snapshot                       # gas snapshot

forge script script/Deploy.s.sol --rpc-url $RPC --broadcast --verify
forge verify-contract <addr> src/MyContract.sol:MyContract --chain optimism

cast call <addr> "balanceOf(address)(uint256)" <wallet> --rpc-url $RPC
cast send <addr> "transfer(address,uint256)" <to> <amount> --private-key $KEY
cast abi-encode "f(address,uint256)" 0x123... 1000
cast sig "transfer(address,uint256)"   # → 0xa9059cbb

anvil                                # local testnet (chainId 31337)
anvil --fork-url $RPC_URL            # fork for testing
```

## Writing Tests

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import {Test, console} from "forge-std/Test.sol";
import {MyContract} from "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public c;
    address user = makeAddr("user");

    function setUp() public {
        c = new MyContract();
        deal(address(this), 10 ether);          // give ETH
        deal(address(token), user, 1000e18);    // give ERC-20
    }

    function test_BasicFlow() public {
        vm.prank(user);                          // next call is from user
        c.doSomething();
        assertEq(c.value(), 42);
    }

    function testFuzz_Deposit(uint256 amount) public {
        amount = bound(amount, 1, 1000e18);     // constrain fuzzing
        c.deposit{value: amount}();
        assertEq(c.balance(), amount);
    }

    function test_RevertOnBadInput() public {
        vm.expectRevert(MyContract.Unauthorized.selector);
        c.adminOnly();
    }
}
```

## Deployment Script

```solidity
// script/Deploy.s.sol
pragma solidity ^0.8.20;
import {Script} from "forge-std/Script.sol";

contract Deploy is Script {
    function run() external returns (address) {
        vm.startBroadcast();
        MyContract c = new MyContract();
        vm.stopBroadcast();
        return address(c);
    }
}
```

## foundry.toml Config

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
optimizer = true
optimizer_runs = 200
solc = "0.8.24"

[rpc_endpoints]
optimism = "${OPTIMISM_RPC_URL}"
base = "${BASE_RPC_URL}"

[etherscan]
optimism = { key = "${ETHERSCAN_API_KEY}", chain = 10 }
```

## Installing Dependencies

```bash
forge install OpenZeppelin/openzeppelin-contracts
forge install transmissions11/solmate
forge install foundry-rs/forge-std   # usually already included
```
