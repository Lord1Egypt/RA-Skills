# Viem Contract Patterns

## Advanced Read Patterns

### Reading with Block Tags
```typescript
// Historical reads
const balance = await publicClient.readContract({
  address: '0x...',
  abi,
  functionName: 'balanceOf',
  args: ['0x...'],
  blockNumber: 18000000n, // Specific block
})

// Pending state
const pending = await publicClient.readContract({
  ...params,
  blockTag: 'pending',
})
```

### Batch Reads with Multicall
```typescript
const results = await publicClient.multicall({
  contracts: tokens.map(token => ({
    address: token,
    abi: erc20Abi,
    functionName: 'balanceOf',
    args: [userAddress],
  })),
  allowFailure: true, // Don't revert entire batch on single failure
})

// Handle mixed results
results.forEach((result, i) => {
  if (result.status === 'success') {
    console.log(`Token ${i}: ${result.result}`)
  } else {
    console.log(`Token ${i} failed: ${result.error}`)
  }
})
```

## Advanced Write Patterns

### Gas Estimation
```typescript
// Estimate gas before sending
const gas = await publicClient.estimateContractGas({
  account,
  address: '0x...',
  abi,
  functionName: 'transfer',
  args: ['0x...', amount],
})

// Add buffer for safety
const { request } = await publicClient.simulateContract({
  ...params,
  gas: gas * 120n / 100n, // 20% buffer
})
```

### EIP-1559 Gas Pricing
```typescript
const { maxFeePerGas, maxPriorityFeePerGas } = await publicClient.estimateFeesPerGas()

const hash = await walletClient.writeContract({
  ...request,
  maxFeePerGas,
  maxPriorityFeePerGas,
})
```

### Nonce Management (Sequential Transactions)
```typescript
let nonce = await publicClient.getTransactionCount({ address: account.address })

for (const tx of transactions) {
  const hash = await walletClient.writeContract({
    ...tx,
    nonce: nonce++,
  })
  // Don't wait for receipt - fire and forget for speed
}
```

## Event Patterns

### Fetching Historical Events
```typescript
const logs = await publicClient.getContractEvents({
  address: '0x...',
  abi,
  eventName: 'Transfer',
  fromBlock: 18000000n,
  toBlock: 18001000n,
})
```

### Filtering Events
```typescript
const logs = await publicClient.getContractEvents({
  address: '0x...',
  abi,
  eventName: 'Transfer',
  args: {
    from: '0x...', // Filter by sender
  },
  fromBlock: 'earliest',
})
```

### Watching with Polling vs WebSocket
```typescript
// HTTP polling (default)
const unwatch = publicClient.watchContractEvent({
  address: '0x...',
  abi,
  eventName: 'Transfer',
  pollingInterval: 1000, // 1 second
  onLogs: (logs) => { ... },
})

// WebSocket (real-time)
import { webSocket } from 'viem'

const wsClient = createPublicClient({
  chain: mainnet,
  transport: webSocket('wss://eth-mainnet.g.alchemy.com/v2/KEY'),
})
```

## Encoding/Decoding

### Manual ABI Encoding
```typescript
import { encodeFunctionData, decodeFunctionResult } from 'viem'

const data = encodeFunctionData({
  abi,
  functionName: 'transfer',
  args: ['0x...', 1000n],
})

// For raw eth_call
const result = await publicClient.call({
  to: '0x...',
  data,
})

const decoded = decodeFunctionResult({
  abi,
  functionName: 'transfer',
  data: result.data,
})
```

### Working with Signatures
```typescript
import { parseSignature, serializeSignature } from 'viem'

// Sign a message
const signature = await walletClient.signMessage({
  message: 'Hello World',
})

// Parse signature components
const { r, s, v } = parseSignature(signature)
```

## Utility Patterns

### Address Validation
```typescript
import { isAddress, getAddress } from 'viem'

if (!isAddress(userInput)) {
  throw new Error('Invalid address')
}

// Checksum address
const checksummed = getAddress(userInput)
```

### Unit Conversion
```typescript
import { parseEther, formatEther, parseUnits, formatUnits } from 'viem'

const wei = parseEther('1.5')      // 1500000000000000000n
const eth = formatEther(wei)       // "1.5"

const usdc = parseUnits('100', 6)  // 100000000n (6 decimals)
const formatted = formatUnits(usdc, 6) // "100"
```

### Contract Deployment
```typescript
const hash = await walletClient.deployContract({
  abi,
  bytecode: '0x...',
  args: [constructorArg1, constructorArg2],
})

const receipt = await publicClient.waitForTransactionReceipt({ hash })
const contractAddress = receipt.contractAddress
```
