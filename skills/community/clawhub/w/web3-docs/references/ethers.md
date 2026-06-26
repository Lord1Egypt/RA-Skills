# ethers.js v6 Reference

ethers.js 6.x — key patterns for connecting to EVM chains, signing, reading contracts, sending transactions.

## Installation

```bash
npm install ethers@6
```

## Providers

```typescript
import { ethers } from 'ethers';

// JSON-RPC (any chain)
const provider = new ethers.JsonRpcProvider('https://mainnet.optimism.io');

// Browser wallet (MetaMask)
const provider = new ethers.BrowserProvider(window.ethereum);

// WebSocket
const provider = new ethers.WebSocketProvider('wss://...');
```

## Signers

```typescript
// From private key
const wallet = new ethers.Wallet(privateKey, provider);

// From browser wallet
const signer = await provider.getSigner();

// Connect wallet to a different provider
const wallet = new ethers.Wallet(privateKey).connect(provider);
```

## Reading Chain State

```typescript
// ETH balance
const balance = await provider.getBalance(address);
const ethStr = ethers.formatEther(balance); // "1.23456"

// Block number
const blockNum = await provider.getBlockNumber();

// Gas price (EIP-1559)
const feeData = await provider.getFeeData();
// feeData.maxFeePerGas, feeData.maxPriorityFeePerGas, feeData.gasPrice
```

## Interacting with Contracts

```typescript
// Read-only (no signer needed)
const contract = new ethers.Contract(address, abi, provider);
const value = await contract.someView();

// Write (needs signer)
const contract = new ethers.Contract(address, abi, wallet);
const tx = await contract.someFunction(arg1, arg2);
const receipt = await tx.wait(); // wait for confirmation
console.log('Gas used:', receipt.gasUsed.toString());
```

## Encoding / Decoding

```typescript
// ABI-encode calldata
const iface = new ethers.Interface(abi);
const data = iface.encodeFunctionData('transfer', [to, amount]);

// Decode return data
const [result] = iface.decodeFunctionResult('balanceOf', returnData);

// Parse units
const wei = ethers.parseEther('1.0');     // 1 ETH → BigInt in wei
const usdc = ethers.parseUnits('100', 6); // 100 USDC (6 decimals)
const eth = ethers.formatEther(wei);      // BigInt → "1.0"
```

## Sending ETH

```typescript
const tx = await wallet.sendTransaction({
  to: recipient,
  value: ethers.parseEther('0.1'),
  // EIP-1559 (recommended):
  maxFeePerGas: feeData.maxFeePerGas,
  maxPriorityFeePerGas: feeData.maxPriorityFeePerGas,
});
const receipt = await tx.wait();
```

## Events

```typescript
// Query past events
const filter = contract.filters.Transfer(null, recipientAddress);
const events = await contract.queryFilter(filter, fromBlock, toBlock);

// Listen for new events
contract.on('Transfer', (from, to, amount, event) => {
  console.log(`${from} → ${to}: ${ethers.formatEther(amount)} ETH`);
});

// Remove listener
contract.off('Transfer', handler);
```

## ERC-20 Common Pattern

```typescript
const ERC20_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'event Transfer(address indexed from, address indexed to, uint256 value)',
];

const token = new ethers.Contract(tokenAddress, ERC20_ABI, wallet);
const balance = await token.balanceOf(wallet.address);
```

## v5 → v6 Migration Notes

| v5 | v6 |
|----|-----|
| `ethers.providers.JsonRpcProvider` | `ethers.JsonRpcProvider` |
| `ethers.utils.parseEther` | `ethers.parseEther` |
| `ethers.utils.formatEther` | `ethers.formatEther` |
| `BigNumber.from(x)` | `BigInt(x)` |
| `gasPrice` (legacy) | `maxFeePerGas` / `maxPriorityFeePerGas` |
| `provider.getGasPrice()` | `provider.getFeeData()` |

## Error Handling

```typescript
try {
  const tx = await contract.someFunction();
  await tx.wait();
} catch (err) {
  if (err.code === 'CALL_EXCEPTION') {
    // Contract reverted — check err.reason
    console.error('Revert reason:', err.reason);
  } else if (err.code === 'INSUFFICIENT_FUNDS') {
    console.error('Not enough ETH for gas');
  } else if (err.code === 'NETWORK_ERROR') {
    // RPC issue, retry
  }
}
```
