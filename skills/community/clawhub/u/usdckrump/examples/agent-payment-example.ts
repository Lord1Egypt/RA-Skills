/**
 * Example: OpenClaw Agent Making Payment via EVVM (Legacy Private Key Method)
 */

import { payViaEVVM, checkPaymentStatus } from '../src/index.js';

async function example() {
  // Agent configuration
  const agentPrivateKey = process.env.AGENT_PRIVATE_KEY!;
  const humanOwnerAddress = '0x...'; // Human owner receives payments
  
  // Contract addresses (Story Aeneid testnet – Bridge USDC.d)
  const adapterAddress = '0x00ed0E80E5EAE285d98eC50236aE97e2AF615314'; // Bridge EVVM adapter
  const usdcDanceAddress = '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40'; // BridgeUSDC
  const evvmCoreAddress = '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b';
  
  // Make payment
  const result = await payViaEVVM({
    from: '0x...', // Agent address (derived from privateKey)
    to: humanOwnerAddress,
    toIdentity: '', // Empty if using address, or EVVM username
    amount: '1000000', // 1 USDC.d (6 decimals)
    receiptId: `payment_${Date.now()}`,
    privateKey: agentPrivateKey,
    adapterAddress,
    usdcDanceAddress,
    evvmCoreAddress,
    evvmId: 1140,
    rpcUrl: 'https://aeneid.storyrpc.io',
    useAsyncNonce: true // Use async nonce for parallel payments
  });
  
  console.log('Payment successful!');
  console.log('Receipt ID:', result.receiptId);
  console.log('Transaction:', result.txHash);
  
  // Check payment status
  const status = await checkPaymentStatus(
    result.receiptId,
    adapterAddress,
    'https://aeneid.storyrpc.io'
  );
  
  console.log('Payment status:', status);
}

example().catch(console.error);
