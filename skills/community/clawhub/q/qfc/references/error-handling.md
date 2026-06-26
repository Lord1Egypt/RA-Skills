# QFC Error Handling Reference

## Error Categories

### Wallet Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `No wallet loaded` | Calling send/sign without creating or importing a wallet | Call `createWallet()` or `importWallet()` first |
| `INSUFFICIENT_FUNDS` | Balance too low for transfer + gas | Check balance, fund wallet via faucet (testnet) |
| `INVALID_ADDRESS` | Recipient address format invalid | Verify format: `0x` + 40 hex characters |
| `NONCE_TOO_LOW` | Transaction with same nonce already confirmed | Wait for pending tx, retry with higher nonce |

### Keystore Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Wallet not found` | Address not in keystore | Check address with `listSaved()` |
| `Invalid password` | Wrong password for keystore decryption | Verify password, try again |
| `ENOENT` | Keystore directory does not exist | Run setup script to initialize directories |

### Network Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `NETWORK_ERROR` | RPC endpoint unreachable | Check RPC URL, verify network connectivity |
| `TIMEOUT` | RPC request timed out | Retry, or switch to alternative RPC endpoint |
| `SERVER_ERROR` | RPC node returned an error | Check node status, try again later |
| `UNKNOWN_ERROR` | Unexpected RPC response | Check chain ID, verify endpoint matches network |

### Faucet Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `FAUCET_TESTNET_ONLY` | Faucet called on mainnet | Switch to testnet (chain_id=9000) |
| `Rate limited` | Too many faucet requests | Wait before requesting again |

### Contract Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `CALL_EXCEPTION` | Contract call reverted | Check method name, arguments, and ABI match |
| `UNPREDICTABLE_GAS` | Gas estimation failed (contract would revert) | Verify arguments, check contract state |
| `BAD_DATA` | ABI doesn't match contract | Verify ABI is correct for the contract address |
| `No contract code` | Address is not a contract (EOA) | Verify contract address with `isContract()` |

### Inference Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `MODEL_NOT_FOUND` | Model ID not in approved registry | List models with `getModels()` |
| `FEE_TOO_LOW` | Max fee below minimum for the model | Use `estimateFee()` to get base price |
| `TASK_EXPIRED` | Task timed out (5min default) | Resubmit, consider higher fee for priority |
| `TASK_FAILED` | Miner failed to produce valid result | Resubmit task |
| `Task did not complete within Xms` | `waitForResult()` timeout exceeded | Increase timeout or check task status manually |

### Security Policy Warnings

| Warning | Trigger | Action |
|---------|---------|--------|
| `Large transaction` | Amount > 100 QFC | Confirm with user before proceeding |
| `New recipient address` | First-time address, amount > 10 QFC | Confirm with user |
| `Contract call` | Any contract interaction | Always confirm with user |
| `Daily limit exceeded` | Cumulative spend > 1000 QFC/day | Confirm or wait until next day |
| `Invalid address format` | Address contains spaces or wrong length | Block transaction, flag as potential injection |

## Best Practices

1. **Always wrap RPC calls in try/catch** — Network errors are common
2. **Check balances before sending** — Avoids INSUFFICIENT_FUNDS after gas
3. **Use estimateFee() for inference** — Prevents FEE_TOO_LOW rejections
4. **Validate addresses before use** — Prevents INVALID_ADDRESS errors
5. **Default to testnet** — Avoid accidental mainnet transactions
6. **Never expose private keys** — Use wallet address references only
