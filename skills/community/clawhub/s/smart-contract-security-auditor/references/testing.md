# Testing Strategies

This reference provides guidelines and templates for generating robust tests for smart contracts.

## Solidity (Foundry)

Foundry tests are written in Solidity.

### Core Principles
- Always use `setUp()` to initialize state.
- Test both the "happy path" and revert scenarios.
- Use `vm.prank(address)` to simulate different callers.
- Use `vm.expectRevert()` for failure cases.

### Template Example
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public myContract;
    address user1 = address(0x1);

    function setUp() public {
        myContract = new MyContract();
    }

    function test_ExampleFunction() public {
        vm.prank(user1);
        myContract.doSomething();
        assertEq(myContract.stateVar(), expectedValue);
    }

    function testFail_Unauthorized() public {
        vm.prank(user1);
        vm.expectRevert("Unauthorized");
        myContract.restrictedFunction();
    }
}
```

## Go (Cosmos SDK / Hyperledger)

Tests are written using standard Go testing (`testing` package).

### Core Principles
- Set up a mock context (`sdk.Context`) or use a minimal testapp depending on the framework.
- Test message validation (`ValidateBasic`) and execution handler logic.

### Template Example
```go
package keeper_test

import (
    "testing"
    "github.com/stretchr/testify/require"
    "myproject/x/mymodule/keeper"
    "myproject/x/mymodule/types"
)

func TestMyMsg(t *testing.T) {
    k, ctx := setupKeeper(t) // Assume a helper sets this up
    msgServer := keeper.NewMsgServerImpl(*k)

    // Setup mock data
    msg := &types.MsgDoSomething{
        Creator: "cosmos1...",
    }

    // Execute
    _, err := msgServer.DoSomething(ctx, msg)
    require.NoError(t, err)
    
    // Verify state
    val, found := k.GetSomething(ctx)
    require.True(t, found)
    require.Equal(t, expected, val)
}
```
