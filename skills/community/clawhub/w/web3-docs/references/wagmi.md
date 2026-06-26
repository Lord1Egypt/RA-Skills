# Wagmi 2.x Reference (React)

## Setup

```bash
npm install wagmi viem @tanstack/react-query
```

```typescript
// app.tsx — wrap your app
import { WagmiProvider, createConfig, http } from 'wagmi'
import { optimism, base, mainnet } from 'wagmi/chains'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { injected, walletConnect } from 'wagmi/connectors'

const config = createConfig({
  chains: [optimism, base],
  connectors: [injected(), walletConnect({ projectId: 'YOUR_PROJECT_ID' })],
  transports: { [optimism.id]: http(), [base.id]: http() },
})
const queryClient = new QueryClient()

export function App() {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <YourApp />
      </QueryClientProvider>
    </WagmiProvider>
  )
}
```

## Connect Wallet

```typescript
import { useConnect, useDisconnect, useAccount } from 'wagmi'

function ConnectButton() {
  const { connect, connectors } = useConnect()
  const { disconnect } = useDisconnect()
  const { address, isConnected } = useAccount()

  if (isConnected) return (
    <div>
      Connected: {address}
      <button onClick={() => disconnect()}>Disconnect</button>
    </div>
  )

  return connectors.map(c => (
    <button key={c.id} onClick={() => connect({ connector: c })}>{c.name}</button>
  ))
}
```

## Read Contract

```typescript
import { useReadContract } from 'wagmi'
import { erc20Abi } from 'viem'

function TokenBalance({ token, owner }: { token: `0x${string}`, owner: `0x${string}` }) {
  const { data: balance, isPending, error } = useReadContract({
    address: token,
    abi: erc20Abi,
    functionName: 'balanceOf',
    args: [owner],
  })
  if (isPending) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  return <div>Balance: {formatUnits(balance!, 18)}</div>
}
```

## Write Contract

```typescript
import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi'

function TransferButton() {
  const { writeContract, data: hash, isPending } = useWriteContract()
  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({ hash })

  function submit() {
    writeContract({
      address: tokenAddr,
      abi: erc20Abi,
      functionName: 'transfer',
      args: ['0xrecipient...', parseUnits('100', 18)],
    })
  }

  return (
    <button onClick={submit} disabled={isPending || isConfirming}>
      {isPending ? 'Signing...' : isConfirming ? 'Confirming...' : 'Transfer'}
    </button>
  )
}
```

## Send ETH

```typescript
import { useSendTransaction } from 'wagmi'

const { sendTransaction } = useSendTransaction()
sendTransaction({ to: '0x...', value: parseEther('0.01') })
```

## Watch Events

```typescript
import { useWatchContractEvent } from 'wagmi'

useWatchContractEvent({
  address: contractAddr,
  abi,
  eventName: 'Transfer',
  onLogs(logs) { console.log(logs) },
})
```

## Get Current Chain & Switch

```typescript
import { useChainId, useSwitchChain } from 'wagmi'
import { optimism } from 'wagmi/chains'

const chainId = useChainId()
const { switchChain } = useSwitchChain()

if (chainId !== optimism.id) switchChain({ chainId: optimism.id })
```
