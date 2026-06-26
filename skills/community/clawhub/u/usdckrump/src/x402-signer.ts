/**
 * x402 Protocol (EIP-3009) Signature Generator for USDC Krump (USDC.k) payments on Story Aeneid EVVM
 */

import { ethers } from 'ethers';

export interface X402SignatureOptions {
  from: string;
  to: string;
  amount: string;
  validAfter: number;
  validBefore: number;
  nonce: string; // bytes32
  /** EIP-712 verifying contract. For EVVM native adapter use adapter address; for token EIP-3009 use token address. */
  usdcDanceAddress: string;
  /** Optional. When set (e.g. to adapter address), used as EIP-712 verifyingContract instead of usdcDanceAddress. */
  verifyingContract?: string;
  chainId: number;
  privateKey: string;
}

export interface X402Signature {
  v: number;
  r: string;
  s: string;
  domainSeparator: string;
  structHash: string;
  digest: string;
}

const TRANSFER_WITH_AUTHORIZATION_TYPEHASH = ethers.keccak256(
  ethers.toUtf8Bytes('TransferWithAuthorization(address from,address to,uint256 amount,uint256 validAfter,uint256 validBefore,bytes32 nonce)')
);

const DOMAIN_TYPEHASH = ethers.keccak256(
  ethers.toUtf8Bytes('EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)')
);

/**
 * Generate EIP-3009 signature for x402 protocol (EIP-712 signTypedData so contract ecrecover matches)
 */
export async function generateX402Signature(
  options: X402SignatureOptions
): Promise<X402Signature> {
  const {
    from,
    to,
    amount,
    validAfter,
    validBefore,
    nonce,
    usdcDanceAddress,
    verifyingContract: explicitVerifyingContract,
    chainId,
    privateKey
  } = options;

  const signer = new ethers.Wallet(privateKey);
  const verifyingContract = (explicitVerifyingContract ?? usdcDanceAddress) as `0x${string}`;

  // EIP-712 name must match EVVMNativeX402Adapter on-chain ("USDC Dance") for signature verification
  const domain = {
    name: 'USDC Dance',
    version: '1',
    chainId,
    verifyingContract
  };
  const types = {
    TransferWithAuthorization: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'amount', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' }
    ]
  };
  const value = {
    from,
    to,
    amount: BigInt(amount),
    validAfter: BigInt(validAfter),
    validBefore: BigInt(validBefore),
    nonce: nonce as `0x${string}`
  };

  const signature = await signer.signTypedData(domain, types, value);
  const sig = ethers.Signature.from(signature);

  // Recompute for return (optional; callers mainly need v,r,s)
  const structHash = ethers.keccak256(
    ethers.AbiCoder.defaultAbiCoder().encode(
      ['bytes32', 'address', 'address', 'uint256', 'uint256', 'uint256', 'bytes32'],
      [TRANSFER_WITH_AUTHORIZATION_TYPEHASH, from, to, amount, validAfter, validBefore, nonce]
    )
  );
  const domainSeparator = ethers.keccak256(
    ethers.AbiCoder.defaultAbiCoder().encode(
      ['bytes32', 'bytes32', 'bytes32', 'uint256', 'address'],
      [
        DOMAIN_TYPEHASH,
        ethers.keccak256(ethers.toUtf8Bytes('USDC Dance')),
        ethers.keccak256(ethers.toUtf8Bytes('1')),
        chainId,
        usdcDanceAddress
      ]
    )
  );
  const digest = ethers.keccak256(
    ethers.concat([ethers.toUtf8Bytes('\x19\x01'), domainSeparator, structHash])
  );

  return {
    v: sig.v,
    r: sig.r,
    s: sig.s,
    domainSeparator,
    structHash,
    digest
  };
}
