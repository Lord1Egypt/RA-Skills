# Complete Example

Deploy to CreateOS with plain fetch + viem. No mppx dependency needed.

```ts
import { privateKeyToAccount } from "viem/accounts";
import { createWalletClient, createPublicClient, http } from "viem";
import { arbitrumSepolia } from "viem/chains";
import { randomUUID } from "crypto";

const GATEWAY = "https://mpp-createos.nodeops.network";
const account = privateKeyToAccount("0xPRIVATE_KEY");

const ERC20_ABI = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "value", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

const auth = async () => {
  const nonce = randomUUID();
  const timestamp = String(Date.now());
  const signature = await account.signMessage({
    message: `${account.address}:${timestamp}:${nonce}`,
  });
  return {
    "X-Wallet-Address": account.address,
    "X-Signature": signature,
    "X-Timestamp": timestamp,
    "X-Nonce": nonce,
  };
};

const body = {
  uniqueName: `app-${Date.now()}`,
  displayName: "My App",
  upload: {
    type: "files",
    files: [
      {
        path: "index.js",
        content: btoa(
          'require("http").createServer((q,s)=>s.end("ok")).listen(3000)',
        ),
      },
      { path: "package.json", content: btoa('{"name":"app"}') },
    ],
  },
};

// 1. Get quote
const quoteRes = await fetch(`${GATEWAY}/agent/deploy`, {
  method: "POST",
  headers: { "Content-Type": "application/json", ...(await auth()) },
  body: JSON.stringify(body),
});
const quote = await quoteRes.json(); // 402

// 2. Pay
const walletClient = createWalletClient({
  account,
  chain: arbitrumSepolia,
  transport: http(),
});
const publicClient = createPublicClient({
  chain: arbitrumSepolia,
  transport: http(),
});

const txHash = await walletClient.writeContract({
  address: "0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d",
  abi: ERC20_ABI,
  functionName: "transfer",
  args: [quote.pay_to, BigInt(quote.amount_token)],
});
await publicClient.waitForTransactionReceipt({ hash: txHash });

// 3. Deploy
const deployRes = await fetch(`${GATEWAY}/agent/deploy`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-Payment-Tx": txHash,
    "X-Payment-Chain": quote.payment_chain,
    "X-Payment-Token": quote.token,
    ...(await auth()),
  },
  body: JSON.stringify(body),
});
const { projectId, deploymentId } = await deployRes.json();

// 4. Poll
let endpoint;
while (!endpoint) {
  await new Promise((r) => setTimeout(r, 5000));
  const s = await fetch(
    `${GATEWAY}/agent/deploy/${projectId}/${deploymentId}/status`,
    {
      headers: await auth(),
    },
  );
  const d = await s.json();
  if (d.status === "ready") endpoint = d.endpoint;
  if (d.status === "failed") throw new Error(d.reason);
}
console.log(`Live: ${endpoint}`);
```

## With zip

Replace `upload` in body:

```ts
import { readFileSync } from 'fs';

upload: {
  type: 'zip',
  data: readFileSync('code.zip').toString('base64'),
  filename: 'code.zip',
}
```
