import { PrivyClient } from '@privy-io/node';
import { createViemAccount } from '@privy-io/node/viem';
import {
  encodeAbiParameters,
  keccak256,
  type Address,
  type Hex,
  type LocalAccount,
} from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { getUserOperationHash } from 'viem/account-abstraction';
import { type ResolvedChain, type SignerBackend } from './types.ts';

const ENTRYPOINT_ADDRESS = '0x0000000071727De22E5E9d8BAf0edAc6f37da032' as Address;
const HEX32_RE = /^0x[a-fA-F0-9]{64}$/;

/**
 * Compute and ABI-encode a SuperValidator-format userOp.signature.
 *
 * SuperValidatorBase._decodeSignatureData expects:
 *   abi.encode(uint64[], uint48, uint48, bytes32, bytes32[], DstProof[], bytes)
 *
 * The inner ECDSA signature is over:
 *   toEthSignedMessageHash(keccak256(abi.encode("SuperValidator", merkleRoot)))
 */
async function buildSuperValidatorSig(
  userOp: Record<string, string>,
  chainId: number,
  superValidatorAddress: Address,
  signer: LocalAccount,
): Promise<Hex> {
  const validUntil = Math.floor(Date.now() / 1000) + 15 * 60; // 15 min
  const validAfter = 0;

  // ERC-4337 v0.7 userOpHash (excludes signature field; viem packs gas fields internally)
  const userOpHash = getUserOperationHash({
    userOperation: {
      sender: userOp.sender as Address,
      nonce: BigInt(userOp.nonce),
      callData: userOp.callData as Hex,
      callGasLimit: BigInt(userOp.callGasLimit),
      verificationGasLimit: BigInt(userOp.verificationGasLimit),
      preVerificationGas: BigInt(userOp.preVerificationGas),
      maxFeePerGas: BigInt(userOp.maxFeePerGas),
      maxPriorityFeePerGas: BigInt(userOp.maxPriorityFeePerGas),
      signature: '0x',
    },
    entryPointAddress: ENTRYPOINT_ADDRESS,
    entryPointVersion: '0.7',
    chainId,
  });

  // SuperValidator._createLeaf: keccak256(keccak256(abi.encode(userOpHash, validUntil, validAfter, chainsWithDest, address(this))))
  const svLeaf = keccak256(keccak256(encodeAbiParameters(
    [
      { type: 'bytes32' },
      { type: 'uint48' },
      { type: 'uint48' },
      { type: 'uint64[]' },
      { type: 'address' },
    ],
    [userOpHash, validUntil, validAfter, [], superValidatorAddress],
  )));
  const svMerkleRoot = svLeaf; // single-op tree: root = leaf, proof = []

  // SuperValidatorBase._createMessageHash then _processECDSASignature (personal sign)
  const messageHash = keccak256(encodeAbiParameters(
    [{ type: 'string' }, { type: 'bytes32' }],
    ['SuperValidator', svMerkleRoot],
  ));
  const ecdsaSig = await signer.signMessage({ message: { raw: messageHash } }) as Hex;

  // ABI-encode the full SuperValidator SignatureData
  return encodeAbiParameters(
    [
      { type: 'uint64[]' },
      { type: 'uint48' },
      { type: 'uint48' },
      { type: 'bytes32' },
      { type: 'bytes32[]' },
      {
        type: 'tuple[]',
        components: [
          { name: 'proof', type: 'bytes32[]' },
          { name: 'dstChainId', type: 'uint64' },
          {
            name: 'info',
            type: 'tuple',
            components: [
              { name: 'data', type: 'bytes' },
              { name: 'chainId', type: 'uint64' },
              { name: 'account', type: 'address' },
              { name: 'executor', type: 'address' },
              { name: 'dstTokens', type: 'address[]' },
              { name: 'intentAmounts', type: 'uint256[]' },
              { name: 'validator', type: 'address' },
            ],
          },
        ],
      },
      { type: 'bytes' },
    ],
    [[], validUntil, validAfter, svMerkleRoot, [], [], ecdsaSig],
  ) as Hex;
}

function parseGasInfo(raw: unknown): Record<string, string> | null {
  if (!raw || typeof raw !== 'object') return null;
  const gas = raw as Record<string, unknown>;
  if (
    typeof gas.gasLimit === 'string' &&
    typeof gas.maxFeePerGas === 'string' &&
    typeof gas.maxPriorityFeePerGas === 'string'
  ) {
    return {
      gasLimit: gas.gasLimit,
      maxFeePerGas: gas.maxFeePerGas,
      maxPriorityFeePerGas: gas.maxPriorityFeePerGas,
    };
  }
  return null;
}

export function createPrivySigner(
  appId: string,
  appSecret: string,
  walletId: string,
  walletAddress: Address,
): LocalAccount {
  const client = new PrivyClient({ appId, appSecret });
  return createViemAccount(client, {
    walletId,
    address: walletAddress,
  });
}

export function createSigner(params: {
  signerBackend: SignerBackend;
  walletAddress: Address;
  privy?: {
    appId: string;
    appSecret: string;
    walletId: string;
  };
  privateKey?: Hex;
}): LocalAccount {
  if (params.signerBackend === 'privy') {
    if (!params.privy) {
      throw new Error('Missing Privy config for SIGNER_BACKEND=privy.');
    }
    return createPrivySigner(
      params.privy.appId,
      params.privy.appSecret,
      params.privy.walletId,
      params.walletAddress,
    );
  }

  if (!params.privateKey) {
    throw new Error('Missing SIGNER_PRIVATE_KEY for SIGNER_BACKEND=private-key.');
  }
  const account = privateKeyToAccount(params.privateKey);
  if (account.address.toLowerCase() !== params.walletAddress.toLowerCase()) {
    throw new Error(
      `SIGNER_PRIVATE_KEY address ${account.address} does not match walletAddress ${params.walletAddress}.`,
    );
  }
  return account;
}

interface IntentSigningPayload {
  domain: {
    name: string;
    version: string;
    chainId: number;
    verifyingContract: Address;
  };
  primaryType: 'Intent';
  types: Record<string, Array<{ name: string; type: string }>>;
  message: {
    merkleRoot: Hex;
    chainId: number;
    expiry: number;
    validAfter: number;
  };
}

interface IntentEnvelopeForSigning extends Record<string, unknown> {
  chainId: number;
  merkleRoot: Hex;
  userOps: Array<Record<string, unknown>>;
  signing?: IntentSigningPayload;
  eip7702AuthRequest?: unknown;
}

function parseIntentEnvelope(raw: unknown): IntentEnvelopeForSigning {
  if (!raw || typeof raw !== 'object') {
    throw new Error('yield_prepare did not return intentEnvelope.');
  }
  const envelope = raw as IntentEnvelopeForSigning;
  if (typeof envelope.chainId !== 'number') {
    throw new Error('intentEnvelope.chainId is missing.');
  }
  if (typeof envelope.merkleRoot !== 'string' || !HEX32_RE.test(envelope.merkleRoot)) {
    throw new Error('intentEnvelope.merkleRoot is missing or invalid.');
  }
  if (!Array.isArray(envelope.userOps) || envelope.userOps.length === 0) {
    throw new Error('intentEnvelope.userOps is missing.');
  }
  return envelope;
}

function parseSigningPayload(raw: unknown): IntentSigningPayload {
  if (!raw || typeof raw !== 'object') {
    throw new Error('intentEnvelope.signing is missing.');
  }
  const signing = raw as IntentSigningPayload;
  if (typeof signing.domain?.name !== 'string' || typeof signing.domain?.version !== 'string') {
    throw new Error('intentEnvelope.signing.domain is invalid.');
  }
  if (typeof signing.domain.chainId !== 'number' || typeof signing.domain.verifyingContract !== 'string') {
    throw new Error('intentEnvelope.signing.domain chain/verifier is invalid.');
  }
  if (signing.primaryType !== 'Intent') {
    throw new Error('intentEnvelope.signing.primaryType must be Intent.');
  }
  if (!signing.types?.Intent || !Array.isArray(signing.types.Intent)) {
    throw new Error('intentEnvelope.signing.types.Intent is missing.');
  }
  if (
    typeof signing.message?.merkleRoot !== 'string' ||
    !HEX32_RE.test(signing.message.merkleRoot) ||
    typeof signing.message?.chainId !== 'number'
  ) {
    throw new Error('intentEnvelope.signing.message is invalid.');
  }
  return signing;
}

export interface SignPreparedResult {
  intentEnvelope: Record<string, unknown>;
  intentSignature: Hex;
  included7702AuthRequest: boolean;
}

export async function signPreparedPayload(
  params: {
    preparePayload: Record<string, unknown>;
    signer: LocalAccount;
    chain: ResolvedChain;
    publicClient: {
      getTransactionCount: (args: { address: Address }) => Promise<number | bigint>;
    };
  },
): Promise<SignPreparedResult> {
  const { preparePayload, signer, chain, publicClient } = params;
  const envelope = parseIntentEnvelope(preparePayload.intentEnvelope);

  if (envelope.chainId !== chain.chainId) {
    throw new Error(
      `intentEnvelope.chainId (${envelope.chainId}) does not match selected chain (${chain.chainId}).`,
    );
  }
  const firstOp = envelope.userOps[0] as Record<string, unknown>;
  const firstUserOperation = firstOp.userOperation as Record<string, unknown> | undefined;
  const opSender = typeof firstUserOperation?.sender === 'string' ? firstUserOperation.sender : '';
  if (!/^0x[a-fA-F0-9]{40}$/.test(opSender)) {
    throw new Error('intentEnvelope.userOps[0].userOperation.sender is missing or invalid.');
  }
  if (opSender.toLowerCase() !== signer.address.toLowerCase()) {
    throw new Error(
      `userOperation.sender (${opSender}) does not match signer address (${signer.address}).`,
    );
  }

  const signing = parseSigningPayload(envelope.signing);
  if (signing.domain.chainId !== chain.chainId) {
    throw new Error(
      `signing.domain.chainId (${signing.domain.chainId}) does not match selected chain (${chain.chainId}).`,
    );
  }
  if (signing.message.chainId !== envelope.chainId) {
    throw new Error(
      `signing.message.chainId (${signing.message.chainId}) does not match envelope chainId (${envelope.chainId}).`,
    );
  }
  if (signing.message.merkleRoot.toLowerCase() !== envelope.merkleRoot.toLowerCase()) {
    throw new Error(
      `signing.message.merkleRoot (${signing.message.merkleRoot}) does not match envelope merkleRoot (${envelope.merkleRoot}).`,
    );
  }

  let included7702AuthRequest = false;
  if (envelope.eip7702AuthRequest) {
    const authRequest = envelope.eip7702AuthRequest as {
      contractAddress?: string;
      chainId?: number;
      nonce?: number | string;
    };
    if (!authRequest.contractAddress || typeof authRequest.chainId !== 'number') {
      throw new Error('intentEnvelope.eip7702AuthRequest is invalid.');
    }

    const txCount = await publicClient.getTransactionCount({ address: signer.address });
    const nonce = typeof authRequest.nonce === 'number'
      ? authRequest.nonce
      : typeof authRequest.nonce === 'string'
        ? Number(authRequest.nonce)
        : Number(txCount);

    const auth = await signer.signAuthorization({
      contractAddress: authRequest.contractAddress as Address,
      chainId: authRequest.chainId,
      nonce,
    });

    const firstOp = envelope.userOps[0] as Record<string, unknown>;
    firstOp.eip7702Auth = [auth];
    envelope.userOps[0] = firstOp;
    included7702AuthRequest = true;
  }

  // Compute the on-chain SuperValidator-format signature for every UserOp.
  // This is what goes into userOp.signature when submitting to the bundler.
  // Stored as a separate field so the intent Merkle (which uses signature:'0x') stays valid.
  const superValidatorAddress = signing.domain.verifyingContract;
  for (let i = 0; i < envelope.userOps.length; i++) {
    const op = envelope.userOps[i] as Record<string, unknown>;
    const userOperation = op.userOperation as Record<string, string>;
    const svSig = await buildSuperValidatorSig(
      userOperation,
      envelope.chainId,
      superValidatorAddress,
      signer,
    );
    op.superValidatorSig = svSig;
    envelope.userOps[i] = op;
  }

  const intentSignature = await signer.signTypedData({
    domain: signing.domain,
    types: signing.types,
    primaryType: signing.primaryType,
    message: signing.message,
  }) as Hex;

  return {
    intentEnvelope: envelope,
    intentSignature,
    included7702AuthRequest,
  };
}

export function getPrepareGasInfo(preparePayload: Record<string, unknown>): Record<string, string> | null {
  if (preparePayload.needsSetup === true) {
    const setup = preparePayload.setup as Record<string, unknown> | undefined;
    return parseGasInfo(setup?.gas);
  }
  const execution = preparePayload.execution as Record<string, unknown> | undefined;
  return parseGasInfo(execution?.gas);
}
