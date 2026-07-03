import { getAddress } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

import { minterAbi } from './abi.mjs';
import { fetchMintAllowlistProof } from './allowlist.mjs';
import { createChainClient } from './chain.mjs';
import { requireSigner, requireWallet } from './config.mjs';
import {
  evaluateMintSession,
  parseMintPhase,
  PAYMENT_FREE,
  phaseIsOpen,
  ZERO_MERKLE_ROOT,
} from './policy.mjs';
import { loadState, saveState } from './state.mjs';

export const MINT_INTENT_TYPES = {
  MintIntent: [
    { name: 'user', type: 'address' },
    { name: 'phaseId', type: 'uint32' },
    { name: 'quantity', type: 'uint32' },
    { name: 'nonce', type: 'uint256' },
    { name: 'deadline', type: 'uint64' },
    { name: 'paramsHash', type: 'bytes32' },
  ],
};

export function mintDomain(chainId, minter) {
  return {
    name: 'UrufuRandomness',
    version: '1',
    chainId,
    verifyingContract: minter,
  };
}

const PHASE_SCAN_LIMIT = 16;

export async function loadMintPhases(client, minter, wallet) {
  const phaseCount = Number(await client.readContract({
    address: minter,
    abi: minterAbi,
    functionName: 'phaseCount',
  }));

  const ids = Array.from(
    { length: Math.min(Math.max(phaseCount, 0), PHASE_SCAN_LIMIT) },
    (_, i) => i,
  );

  const phases = [];
  for (const phaseId of ids) {
    const [phaseRaw, mintCount, walletMintCount] = await Promise.all([
      client.readContract({ address: minter, abi: minterAbi, functionName: 'phases', args: [BigInt(phaseId)] }),
      client.readContract({ address: minter, abi: minterAbi, functionName: 'phaseMintCount', args: [phaseId] }),
      client.readContract({
        address: minter,
        abi: minterAbi,
        functionName: 'walletPhaseMintCount',
        args: [phaseId, getAddress(wallet)],
      }),
    ]);
    const info = parseMintPhase(phaseRaw);
    phases.push({
      phaseId,
      info,
      mintCount: Number(mintCount),
      walletMintCount: Number(walletMintCount),
      open: phaseIsOpen(info),
      remaining: Math.max(0, info.maxMints - Number(mintCount)),
    });
  }
  return phases;
}

export async function previewGaslessMint(config, { phaseId, quantity = 1 } = {}) {
  const wallet = requireWallet(config);
  const client = createChainClient(config);
  const phases = await loadMintPhases(client, config.minter, wallet);

  let target = phaseId !== undefined
    ? phases.find((p) => p.phaseId === phaseId)
    : phases.find((p) => p.open && p.info.payment === PAYMENT_FREE && p.remaining > 0);

  if (!target && phaseId === undefined) {
    target = phases.find((p) => p.info.payment === PAYMENT_FREE);
  }

  if (!target) {
    return {
      gaslessEligible: false,
      phaseId: null,
      quantity,
      hasAllowlist: null,
      phaseOpen: false,
      walletCapReached: false,
      phaseSoldOut: true,
      phases: phases.map(summarizePhase),
    };
  }

  const allowlist = target.info.merkleRoot.toLowerCase() === ZERO_MERKLE_ROOT
    ? { proof: [], source: 'open phase' }
    : await fetchMintAllowlistProof(config.siteUrl, target.info.merkleRoot, wallet);

  const walletCapReached = target.info.maxPerWallet > 0
    && target.walletMintCount + quantity > target.info.maxPerWallet;
  const phaseSoldOut = target.remaining < quantity;

  return {
    gaslessEligible: target.info.payment === PAYMENT_FREE,
    phaseId: target.phaseId,
    quantity,
    hasAllowlist: allowlist !== null,
    merkleProof: allowlist?.proof ?? [],
    allowlistSource: allowlist?.source ?? null,
    phaseOpen: target.open,
    walletCapReached,
    phaseSoldOut,
    payment: target.info.payment,
    price: target.info.price.toString(),
    phases: phases.map(summarizePhase),
  };
}

function summarizePhase(phase) {
  return {
    phaseId: phase.phaseId,
    payment: phase.info.payment,
    open: phase.open,
    remaining: phase.remaining,
    walletMintCount: phase.walletMintCount,
    maxPerWallet: phase.info.maxPerWallet,
    merkleRoot: phase.info.merkleRoot,
  };
}

export async function signMintIntent(account, config, { phaseId, quantity, nonce, paramsHash }) {
  const intentDeadline = BigInt(Math.floor(Date.now() / 1000) + config.mintIntentTtlSeconds);
  const message = {
    user: getAddress(config.wallet),
    phaseId,
    quantity,
    nonce,
    deadline: intentDeadline,
    paramsHash,
  };
  const intentSignature = await account.signTypedData({
    domain: mintDomain(config.chainId, config.minter),
    types: MINT_INTENT_TYPES,
    primaryType: 'MintIntent',
    message,
  });
  return { intentDeadline, intentSignature, message };
}

export async function relayFreeMint(config, body) {
  const res = await fetch(`${config.siteUrl}/api/randomness/free-mint`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chainId: config.chainId,
      contract: config.minter,
      user: getAddress(config.wallet),
      phaseId: body.phaseId,
      quantity: body.quantity,
      nonce: body.nonce.toString(),
      paramsHash: body.paramsHash,
      intentDeadline: body.intentDeadline.toString(),
      intentSignature: body.intentSignature,
      merkleProof: body.merkleProof,
    }),
  });

  const text = await res.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = { error: text };
  }
  if (!res.ok) {
    const err = new Error(parsed.error || res.statusText || 'free mint relay failed');
    err.status = res.status;
    throw err;
  }
  return parsed;
}

export async function runMintPreview(config, options = {}) {
  const wallet = requireWallet(config);
  const state = await loadState(config.statePath);
  const preview = await previewGaslessMint(config, options);
  const decision = evaluateMintSession(state, preview, Date.now(), config.mintMinIntervalMs);
  return { wallet, preview, mint: decision, state };
}

export async function runMint(config, { force = false, phaseId, quantity = 1 } = {}) {
  const wallet = requireWallet(config);
  const privateKey = requireSigner(config);
  const account = privateKeyToAccount(privateKey);
  if (account.address.toLowerCase() !== wallet.toLowerCase()) {
    throw new Error('URUFU_PRIVATE_KEY does not match URUFU_WALLET');
  }

  const state = await loadState(config.statePath);
  const preview = await previewGaslessMint(config, { phaseId, quantity });
  const decision = evaluateMintSession(state, preview, Date.now(), config.mintMinIntervalMs);

  if (!force && !decision.allowed) {
    return { skipped: true, reasons: decision.reasons, preview };
  }
  if (!preview.gaslessEligible || preview.phaseId === null) {
    return { skipped: true, reasons: ['no gasless free phase'], preview };
  }
  if (!preview.hasAllowlist) {
    return { skipped: true, reasons: ['wallet not on allowlist'], preview };
  }

  const client = createChainClient(config);
  const [nonce, paramsHash] = await Promise.all([
    client.readContract({
      address: config.minter,
      abi: minterAbi,
      functionName: 'mintNonce',
      args: [getAddress(wallet)],
    }),
    client.readContract({
      address: config.minter,
      abi: minterAbi,
      functionName: 'mintParamsHash',
      args: [preview.phaseId, quantity, 0n],
    }),
  ]);

  const signed = await signMintIntent(account, config, {
    phaseId: preview.phaseId,
    quantity,
    nonce,
    paramsHash,
  });

  try {
    const result = await relayFreeMint(config, {
      phaseId: preview.phaseId,
      quantity,
      nonce,
      paramsHash,
      intentDeadline: signed.intentDeadline,
      intentSignature: signed.intentSignature,
      merkleProof: preview.merkleProof,
    });

    state.lastMintAtMs = Date.now();
    state.lastMintTxHash = result.txHash ?? null;
    state.consecutiveErrors = 0;
    await saveState(config.statePath, state);

    return {
      skipped: false,
      txHash: result.txHash,
      relayer: result.relayer,
      count: result.count,
      phaseId: preview.phaseId,
      preview,
    };
  } catch (error) {
    state.consecutiveErrors = (state.consecutiveErrors || 0) + 1;
    await saveState(config.statePath, state);
    throw error;
  }
}

export function printMintReport(report) {
  const lines = [
    `wallet: ${report.wallet}`,
    `gasless phase: ${report.preview.phaseId ?? 'none'}`,
    `mint allowed: ${report.mint.allowed}`,
  ];
  if (report.mint.reasons.length) lines.push(`reasons: ${report.mint.reasons.join('; ')}`);
  if (report.preview.phases?.length) {
    lines.push(`phases: ${report.preview.phases.map((p) => `#${p.phaseId} pay=${p.payment} open=${p.open} left=${p.remaining}`).join(', ')}`);
  }
  return lines.join('\n');
}
