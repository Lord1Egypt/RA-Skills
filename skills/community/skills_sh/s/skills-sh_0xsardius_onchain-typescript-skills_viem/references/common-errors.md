# Viem Common Errors & Debugging

## Error Handling Pattern

```typescript
import {
  BaseError,
  ContractFunctionRevertedError,
  TransactionExecutionError,
  InsufficientFundsError,
  UserRejectedRequestError,
} from 'viem'

try {
  const { request } = await publicClient.simulateContract({ ... })
  const hash = await walletClient.writeContract(request)
} catch (err) {
  if (err instanceof BaseError) {
    // Walk the error chain to find specific error type
    const revertError = err.walk(e => e instanceof ContractFunctionRevertedError)
    
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName
      const args = revertError.data?.args
      console.error(`Contract reverted: ${errorName}`, args)
      return
    }
    
    if (err.walk(e => e instanceof InsufficientFundsError)) {
      console.error('Insufficient funds for gas')
      return
    }
    
    if (err.walk(e => e instanceof UserRejectedRequestError)) {
      console.error('User rejected transaction')
      return
    }
  }
  
  throw err // Re-throw unknown errors
}
```

## Common Errors & Solutions

### "ABI encoding params do not match"
**Cause**: Arguments don't match function signature types
**Fix**:
```typescript
// ❌ Wrong: string instead of bigint
args: ['0x...', '1000']

// ✅ Correct: use BigInt
args: ['0x...', 1000n]

// ❌ Wrong: number for uint256
args: ['0x...', 1000]

// ✅ Correct: BigInt literal
args: ['0x...', BigInt(1000)]
```

### "Execution reverted" with no reason
**Cause**: Contract reverted but no error message returned
**Debug**:
```typescript
// Use simulateContract to get better error messages
try {
  await publicClient.simulateContract({
    account, // Include account for accurate simulation
    address,
    abi,
    functionName,
    args,
  })
} catch (err) {
  // Simulation gives more detailed revert info
  console.error(err)
}
```

### "Insufficient funds for gas * price + value"
**Causes**:
1. Account has insufficient ETH for gas
2. Sending ETH but don't have enough
3. Gas estimate is too low

**Fix**:
```typescript
// Check balance first
const balance = await publicClient.getBalance({ address: account.address })

// Estimate gas needed
const gas = await publicClient.estimateContractGas({ ... })
const { maxFeePerGas } = await publicClient.estimateFeesPerGas()
const gasCost = gas * maxFeePerGas

if (balance < gasCost + valueToSend) {
  throw new Error('Insufficient balance')
}
```

### "Nonce too low" / "Nonce too high"
**Cause**: Transaction nonce doesn't match expected
**Fix**:
```typescript
// Get current nonce
const nonce = await publicClient.getTransactionCount({
  address: account.address,
  blockTag: 'pending', // Include pending transactions
})

const hash = await walletClient.writeContract({
  ...request,
  nonce,
})
```

### "Replacement transaction underpriced"
**Cause**: Trying to replace pending tx with same nonce but lower gas
**Fix**:
```typescript
// Get pending tx gas price and bump by 10%+
const pendingTx = await publicClient.getTransaction({ hash: pendingHash })
const bumpedGas = pendingTx.maxFeePerGas * 110n / 100n

const hash = await walletClient.writeContract({
  ...request,
  nonce: pendingTx.nonce,
  maxFeePerGas: bumpedGas,
})
```

### "Transaction type not supported"
**Cause**: Chain doesn't support EIP-1559 transactions
**Fix**:
```typescript
// Use legacy gas pricing
const hash = await walletClient.writeContract({
  ...request,
  gasPrice: await publicClient.getGasPrice(),
  maxFeePerGas: undefined,
  maxPriorityFeePerGas: undefined,
})
```

### "RPC rate limited" / "429 Too Many Requests"
**Fix**:
```typescript
import { http, fallback } from 'viem'

// Use fallback transports
const transport = fallback([
  http('https://eth-mainnet.g.alchemy.com/v2/KEY1'),
  http('https://mainnet.infura.io/v3/KEY2'),
  http('https://rpc.ankr.com/eth'),
])

const client = createPublicClient({
  chain: mainnet,
  transport,
})
```

## Debugging Tips

### Enable Verbose Logging
```typescript
// Log all RPC calls
const transport = http('https://...', {
  onRequest: (request) => {
    console.log('RPC Request:', request.method, request.params)
  },
  onResponse: (response) => {
    console.log('RPC Response:', response)
  },
})
```

### Trace Transaction Execution
```typescript
// Use trace_call for detailed execution trace (requires archive node)
const trace = await publicClient.request({
  method: 'trace_call',
  params: [
    {
      to: address,
      data: encodeFunctionData({ abi, functionName, args }),
    },
    ['trace'],
    'latest',
  ],
})
```

### Check Contract State
```typescript
// Verify contract exists
const code = await publicClient.getBytecode({ address })
if (!code || code === '0x') {
  throw new Error('No contract at address')
}

// Check if contract is proxy
const implementationSlot = '0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'
const impl = await publicClient.getStorageAt({ address, slot: implementationSlot })
```
