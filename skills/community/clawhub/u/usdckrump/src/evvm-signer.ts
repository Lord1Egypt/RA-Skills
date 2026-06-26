/**
 * EVVM Core EIP-191 Signature Generator
 */

import { ethers } from 'ethers';

export interface EVVMSignatureOptions {
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
  privateKey: string;
}

export interface EVVMSignature {
  signature: string;
  hashPayload: string;
}

/**
 * Generate EVVM Core payment signature (EIP-191)
 *
 * Message format (evvm-js): comma-separated string
 *   evvmId,evvmCoreAddress,hashPayload,executor,nonce,isAsyncExec
 * hashPayload = keccak256(abi.encode("pay", to, toIdentity, token, amount, priorityFee))
 * Sign with signMessage(message) only (no ABI-encode or double-hash).
 */
export async function generateEVVMSignature(
  options: EVVMSignatureOptions
): Promise<EVVMSignature> {
  const {
    from,
    to,
    toIdentity,
    token,
    amount,
    priorityFee,
    senderExecutor,
    nonce,
    isAsyncExec,
    evvmId,
    evvmCoreAddress,
    privateKey
  } = options;

  const signer = new ethers.Wallet(privateKey);

  // Build hashPayload (CoreHashUtils.hashDataForPay: "pay" + to + toIdentity + token + amount + priorityFee)
  const hashPayloadBytes = ethers.keccak256(
    ethers.AbiCoder.defaultAbiCoder().encode(
      ['string', 'address', 'string', 'address', 'uint256', 'uint256'],
      ['pay', to, toIdentity ?? '', token, amount, priorityFee]
    )
  );
  const hashPayloadHex = hashPayloadBytes.toLowerCase();

  // Message to sign: single comma-separated string (evvm-js / Core format)
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

  const signature = await signer.signMessage(message);

  return {
    signature,
    hashPayload: hashPayloadBytes
  };
}
