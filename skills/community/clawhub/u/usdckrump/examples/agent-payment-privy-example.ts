/**
 * Example: OpenClaw Agent Making Payment via EVVM using Privy Wallet
 */

import { payViaEVVMWithPrivy, checkPaymentStatus } from '../src/index.js';

async function example() {
  // Privy wallet configuration
  const walletId = process.env.PRIVY_WALLET_ID!; // Get from Privy dashboard or create via Privy skill
  const humanOwnerAddress = '0x...'; // Human owner receives payments
  
  // Contract addresses (Story Aeneid testnet – Bridge USDC.d)
  const adapterAddress = '0x00ed0E80E5EAE285d98eC50236aE97e2AF615314'; // Bridge EVVM adapter
  const usdcDanceAddress = '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40'; // BridgeUSDC
  const evvmCoreAddress = '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b';
  
  // Make payment using Privy wallet
  const result = await payViaEVVMWithPrivy({
    walletId,
    to: humanOwnerAddress,
    toIdentity: '', // Empty if using address, or EVVM username like "humanowner"
    amount: '1000000', // 1 USDC.d (6 decimals)
    receiptId: `payment_${Date.now()}`,
    adapterAddress,
    usdcDanceAddress,
    evvmCoreAddress,
    evvmId: 1140,
    rpcUrl: 'https://aeneid.storyrpc.io',
    useAsyncNonce: true, // Use async nonce for parallel payments
    // privyAppId and privyAppSecret optional if set in OpenClaw config
  });
  
  console.log('✅ Payment successful!');
  console.log('📋 Receipt ID:', result.receiptId);
  console.log('🔗 Transaction:', result.txHash);
  console.log('👤 From:', result.from);
  console.log('👤 To:', result.to);
  console.log('💰 Amount:', result.amount);
  
  // Check payment status
  const status = await checkPaymentStatus(
    result.receiptId,
    adapterAddress,
    'https://aeneid.storyrpc.io'
  );
  
  console.log('\n📊 Payment Status:');
  console.log('   Exists:', status.exists);
  console.log('   Timestamp:', new Date(status.timestamp * 1000).toISOString());
}

example().catch(console.error);
