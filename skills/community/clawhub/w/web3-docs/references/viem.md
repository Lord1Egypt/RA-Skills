# Viem 2.x Reference

## Setup

```bash
npm install viem
```

```typescript
import { createPublicClient, createWalletClient, http, parseEther, formatEther } from 'viem'
import { optimism, base, mainnet } from 'viem/chains'
import { privateKeyToAccount } from 'viem/accounts'

const publicClient = createPublicClient({ chain: optimism, transport: http() })
const account = privateKeyToAccount(`0x${process.env.PRIVATE_KEY}`)
const walletClient = createWalletClient({ account, chain: optimism, transport: http() })
```

## Read Contract State

```typescript
const balance = await publicClient.readContract({
  address: '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',
  abi: erc20Abi,
  functionName: 'balanceOf',
  args: [account.address],
})
// balance is typed as bigint

// Get ETH balance
const ethBalance = await publicClient.getBalance({ address: account.address })
console.log(formatEther(ethBalance))
```

## Write Contract

```typescript
const { request } = await publicClient.simulateContract({
  account,
  address: contractAddr,
  abi,
  functionName: 'transfer',
  args: [recipient, parseUnits('100', 6)],  // USDC has 6 decimals
})
const hash = await walletClient.writeContract(request)
const receipt = await publicClient.waitForTransactionReceipt({ hash })
```

## Send ETH

```typescript
const hash = await walletClient.sendTransaction({
  to: recipient,
  value: parseEther('0.01'),
})
await publicClient.waitForTransactionReceipt({ hash })
```

## Watch Events

```typescript
const unwatch = publicClient.watchContractEvent({
  address: contractAddr,
  abi,
  eventName: 'Transfer',
  args: { to: account.address },  // filter by indexed param
  onLogs: (logs) => console.log(logs),
})
// Call unwatch() to stop
```

## Multicall

```typescript
const results = await publicClient.multicall({
  contracts: [
    { address: tokenA, abi: erc20Abi, functionName: 'balanceOf', args: [wallet] },
    { address: tokenB, abi: erc20Abi, functionName: 'balanceOf', args: [wallet] },
    { address: tokenA, abi: erc20Abi, functionName: 'totalSupply' },
  ]
})
// results[0].result, results[1].result, etc.
```

## Common Utilities

```typescript
import { parseEther, parseUnits, formatEther, formatUnits, keccak256, toHex, encodeFunctionData, decodeFunctionResult, getContract } from 'viem'

parseEther('1.5')              // 1500000000000000000n
parseUnits('100', 6)           // 100000000n (USDC)
formatEther(1500000000000000000n) // '1.5'
keccak256(toHex('hello'))      // hash
```
