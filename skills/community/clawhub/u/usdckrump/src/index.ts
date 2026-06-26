/**
 * USDC Krump (USDC.k) EVVM Payment Skill for OpenClaw
 * Enables autonomous agent payments via x402 protocol on Story Aeneid EVVM
 * Supports both Privy server wallets and direct private key signing
 */

import { ethers } from 'ethers';
import { generateX402Signature } from './x402-signer.js';
import { generateEVVMSignature } from './evvm-signer.js';
import { EVVMPaymentAdapter } from './payment-adapter.js';
import { PrivySigner } from './privy-signer.js';

export interface PaymentOptions {
  from: string;
  to: string;
  toIdentity?: string;
  amount: string;
  receiptId: string;
  privateKey: string;
  adapterAddress: string;
  usdcDanceAddress: string;
  evvmCoreAddress: string;
  evvmId: number;
  rpcUrl: string;
  validAfter?: number;
  validBefore?: number;
  useAsyncNonce?: boolean;
  /** When true, x402 signature uses adapter as EIP-712 verifyingContract (EVVM native adapter). */
  useNativeAdapter?: boolean;
}

export interface PrivyPaymentOptions {
  walletId: string;
  to: string;
  toIdentity?: string;
  amount: string;
  receiptId: string;
  adapterAddress: string;
  usdcDanceAddress: string;
  evvmCoreAddress: string;
  evvmId: number;
  rpcUrl: string;
  validAfter?: number;
  validBefore?: number;
  useAsyncNonce?: boolean;
  /** When true, x402 signature uses adapter as EIP-712 verifyingContract (EVVM native adapter). */
  useNativeAdapter?: boolean;
  privyAppId?: string;
  privyAppSecret?: string;
}

export interface PaymentResult {
  txHash: string;
  receiptId: string;
  from: string;
  to: string;
  amount: string;
  timestamp: number;
}

/**
 * Process a payment through EVVM using x402 protocol with Privy wallet
 */
export async function payViaEVVMWithPrivy(options: PrivyPaymentOptions): Promise<PaymentResult> {
  const {
    walletId,
    to,
    toIdentity = '',
    amount,
    receiptId,
    adapterAddress,
    usdcDanceAddress,
    evvmCoreAddress,
    evvmId,
    rpcUrl,
    validAfter,
    validBefore,
    useAsyncNonce = true,
    useNativeAdapter = false,
    privyAppId,
    privyAppSecret
  } = options;

  // Initialize Privy signer
  const privySigner = new PrivySigner({
    walletId,
    appId: privyAppId || process.env.PRIVY_APP_ID!,
    appSecret: privyAppSecret || process.env.PRIVY_APP_SECRET!,
    chainId: 1315, // Story Aeneid
    rpcUrl
  });

  // Get wallet address
  const from = await privySigner.getAddress();
  
  // Setup provider
  const provider = new ethers.JsonRpcProvider(rpcUrl);

  // Get current timestamp
  const now = Math.floor(Date.now() / 1000);
  const authValidAfter = validAfter || now;
  const authValidBefore = validBefore || now + 3600;

  // Generate unique nonces
  const x402Nonce = ethers.keccak256(ethers.toUtf8Bytes(`${receiptId}-${now}-x402`));
  
  // Get EVVM nonce
  const evvmCore = new ethers.Contract(
    evvmCoreAddress,
    [
      'function getNextCurrentSyncNonce(address user) view returns (uint256)',
      'function getIfUsedAsyncNonce(address user, uint256 nonce) view returns (bool)'
    ],
    provider
  );

  let evvmNonce: bigint;
  if (useAsyncNonce) {
    evvmNonce = BigInt(ethers.keccak256(ethers.toUtf8Bytes(`${receiptId}-${now}-evvm`)).slice(0, 10));
    const used = await evvmCore.getIfUsedAsyncNonce(from, evvmNonce);
    if (used) {
      throw new Error('EVVM async nonce already used, try again');
    }
  } else {
    evvmNonce = await evvmCore.getNextCurrentSyncNonce(from);
  }

  // Step 1: Generate x402 signature using Privy (use adapter as verifyingContract for native adapter)
  const x402Sig = await generateX402SignatureWithPrivy({
    from,
    to: adapterAddress,
    amount,
    validAfter: authValidAfter,
    validBefore: authValidBefore,
    nonce: x402Nonce,
    usdcDanceAddress,
    verifyingContract: useNativeAdapter ? adapterAddress : undefined,
    chainId: 1315,
    privySigner
  });

  // Step 2: Generate EVVM signature using Privy
  const evvmSig = await generateEVVMSignatureWithPrivy({
    from,
    to,
    toIdentity,
    token: usdcDanceAddress,
    amount,
    priorityFee: 0,
    senderExecutor: ethers.ZeroAddress,
    nonce: evvmNonce,
    isAsyncExec: useAsyncNonce,
    evvmId,
    evvmCoreAddress,
    privySigner
  });

  // Step 3: Call adapter (using Privy to sign the transaction)
  const adapter = new EVVMPaymentAdapter(adapterAddress, privySigner);
  
  const tx = await adapter.payViaEVVMWithX402({
    from,
    to,
    toIdentity,
    amount,
    validAfter: authValidAfter,
    validBefore: authValidBefore,
    nonce: x402Nonce,
    v: x402Sig.v,
    r: x402Sig.r,
    s: x402Sig.s,
    receiptId,
    evvmNonce,
    isAsyncExec: useAsyncNonce,
    evvmSignature: evvmSig.signature
  });

  const receipt = await tx.wait();

  return {
    txHash: receipt.hash,
    receiptId,
    from,
    to,
    amount,
    timestamp: Math.floor(Date.now() / 1000)
  };
}

/**
 * Process a payment through EVVM using x402 protocol (legacy private key method)
 */
export async function payViaEVVM(options: PaymentOptions): Promise<PaymentResult> {
  const {
    from,
    to,
    toIdentity = '',
    amount,
    receiptId,
    privateKey,
    adapterAddress,
    usdcDanceAddress,
    evvmCoreAddress,
    evvmId,
    rpcUrl,
    validAfter,
    validBefore,
    useAsyncNonce = true,
    useNativeAdapter = false
  } = options;

  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const signer = new ethers.Wallet(privateKey, provider);
  
  if (ethers.getAddress(from) !== signer.address) {
    throw new Error('from address must match private key');
  }

  const now = Math.floor(Date.now() / 1000);
  const authValidAfter = validAfter || now;
  const authValidBefore = validBefore || now + 3600;

  const x402Nonce = ethers.keccak256(ethers.toUtf8Bytes(`${receiptId}-${now}-x402`));
  
  const evvmCore = new ethers.Contract(
    evvmCoreAddress,
    [
      'function getNextCurrentSyncNonce(address user) view returns (uint256)',
      'function getIfUsedAsyncNonce(address user, uint256 nonce) view returns (bool)'
    ],
    provider
  );

  let evvmNonce: bigint;
  if (useAsyncNonce) {
    evvmNonce = BigInt(ethers.keccak256(ethers.toUtf8Bytes(`${receiptId}-${now}-evvm`)).slice(0, 10));
    const used = await evvmCore.getIfUsedAsyncNonce(from, evvmNonce);
    if (used) {
      throw new Error('EVVM async nonce already used, try again');
    }
  } else {
    evvmNonce = await evvmCore.getNextCurrentSyncNonce(from);
  }

  const x402Sig = await generateX402Signature({
    from,
    to: adapterAddress,
    amount,
    validAfter: authValidAfter,
    validBefore: authValidBefore,
    nonce: x402Nonce,
    usdcDanceAddress,
    verifyingContract: useNativeAdapter ? adapterAddress : undefined,
    chainId: 1315,
    privateKey
  });

  const evvmSig = await generateEVVMSignature({
    from,
    to,
    toIdentity,
    token: usdcDanceAddress,
    amount,
    priorityFee: 0,
    senderExecutor: ethers.ZeroAddress,
    nonce: evvmNonce,
    isAsyncExec: useAsyncNonce,
    evvmId,
    evvmCoreAddress,
    privateKey
  });

  const adapter = new EVVMPaymentAdapter(adapterAddress, signer);
  
  const tx = await adapter.payViaEVVMWithX402({
    from,
    to,
    toIdentity,
    amount,
    validAfter: authValidAfter,
    validBefore: authValidBefore,
    nonce: x402Nonce,
    v: x402Sig.v,
    r: x402Sig.r,
    s: x402Sig.s,
    receiptId,
    evvmNonce,
    isAsyncExec: useAsyncNonce,
    evvmSignature: evvmSig.signature
  });

  const receipt = await tx.wait();

  return {
    txHash: receipt.hash,
    receiptId,
    from,
    to,
    amount,
    timestamp: Math.floor(Date.now() / 1000)
  };
}

/**
 * Check payment status
 */
export async function checkPaymentStatus(
  receiptId: string,
  adapterAddress: string,
  rpcUrl: string
): Promise<{
  exists: boolean;
  from: string;
  to: string;
  amount: string;
  timestamp: number;
}> {
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const adapter = new ethers.Contract(
    adapterAddress,
    [
      'function getEVVMPaymentInfo(string memory receiptId) view returns (address from, address to, uint256 amount, uint256 timestamp, bool exists)'
    ],
    provider
  );

  const [from, to, amount, timestamp, exists] = await adapter.getEVVMPaymentInfo(receiptId);

  return {
    exists,
    from,
    to,
    amount: amount.toString(),
    timestamp: Number(timestamp)
  };
}

// Helper functions for Privy signing
async function generateX402SignatureWithPrivy(options: {
  from: string;
  to: string;
  amount: string;
  validAfter: number;
  validBefore: number;
  nonce: string;
  usdcDanceAddress: string;
  verifyingContract?: string;
  chainId: number;
  privySigner: PrivySigner;
}): Promise<{ v: number; r: string; s: string }> {
  const { privySigner, from, to, amount, validAfter, validBefore, nonce, usdcDanceAddress, verifyingContract: explicitVc, chainId } = options;
  const verifyingContract = explicitVc ?? usdcDanceAddress;

  const TRANSFER_WITH_AUTHORIZATION_TYPEHASH = ethers.keccak256(
    ethers.toUtf8Bytes('TransferWithAuthorization(address from,address to,uint256 amount,uint256 validAfter,uint256 validBefore,bytes32 nonce)')
  );

  const DOMAIN_TYPEHASH = ethers.keccak256(
    ethers.toUtf8Bytes('EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)')
  );

  const structHash = ethers.keccak256(
    ethers.AbiCoder.defaultAbiCoder().encode(
      ['bytes32', 'address', 'address', 'uint256', 'uint256', 'uint256', 'bytes32'],
      [TRANSFER_WITH_AUTHORIZATION_TYPEHASH, from, to, amount, validAfter, validBefore, nonce]
    )
  );

  // EIP-712 name must match EVVMNativeX402Adapter on-chain ("USDC Dance") for signature verification
  const domainSeparator = ethers.keccak256(
    ethers.AbiCoder.defaultAbiCoder().encode(
      ['bytes32', 'bytes32', 'bytes32', 'uint256', 'address'],
      [
        DOMAIN_TYPEHASH,
        ethers.keccak256(ethers.toUtf8Bytes('USDC Dance')),
        ethers.keccak256(ethers.toUtf8Bytes('1')),
        chainId,
        verifyingContract
      ]
    )
  );

  const digest = ethers.keccak256(
    ethers.concat([
      ethers.toUtf8Bytes('\x19\x01'),
      domainSeparator,
      structHash
    ])
  );

  const signature = await privySigner.signMessage(ethers.getBytes(digest));
  const sig = ethers.Signature.from(signature);

  return {
    v: sig.v,
    r: sig.r,
    s: sig.s
  };
}

async function generateEVVMSignatureWithPrivy(options: {
  from: string;
  to: string;
  toIdentity: string;
  token: string;
  amount: string;
  priorityFee: number;
  senderExecutor: string;
  nonce: bigint;
  isAsyncExec: boolean;
  evvmId: number;
  evvmCoreAddress: string;
  privySigner: PrivySigner;
}): Promise<{ signature: string }> {
  const { privySigner, to, toIdentity, token, amount, priorityFee, senderExecutor, nonce, isAsyncExec, evvmId, evvmCoreAddress } = options;

  const hashPayloadBytes = ethers.keccak256(
    ethers.AbiCoder.defaultAbiCoder().encode(
      ['string', 'address', 'string', 'address', 'uint256', 'uint256'],
      ['pay', to, toIdentity ?? '', token, amount, priorityFee]
    )
  );
  const hashPayloadHex = hashPayloadBytes.toLowerCase();

  const message = [
    String(evvmId),
    evvmCoreAddress.toLowerCase(),
    hashPayloadHex,
    (senderExecutor || ethers.ZeroAddress).toLowerCase(),
    String(nonce),
    isAsyncExec ? 'true' : 'false'
  ].join(',');

  // Debug: compare with contract buildSignaturePayload(evvmId, serviceAddress, hashPayload, executor, nonce, isAsyncExec)
  const messageBytes = new TextEncoder().encode(message);
  console.log('[EVVM signer] serviceAddress (evvmCoreAddress):', evvmCoreAddress.toLowerCase());
  console.log('[EVVM signer] hashPayload (hex):', hashPayloadHex);
  console.log('[EVVM signer] message (length ' + messageBytes.length + ' bytes):', message);
  console.log('[EVVM signer] message (length decimal for EIP-191):', String(messageBytes.length));

  const signature = await privySigner.signMessage(message);

  return { signature };
}

// Export helper functions
export { generateX402Signature } from './x402-signer.js';
export { generateEVVMSignature } from './evvm-signer.js';
export { EVVMPaymentAdapter } from './payment-adapter.js';
export { PrivySigner } from './privy-signer.js';
