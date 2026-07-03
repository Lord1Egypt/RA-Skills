import { createWalletClient, formatEther, getAddress, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

import { erc20Abi, minterAbi } from './abi.mjs';
import { fetchMintAllowlistProof } from './allowlist.mjs';
import { createChainClient } from './chain.mjs';
import { requireRpc, requireSigner, requireWallet } from './config.mjs';
import { loadMintPhases } from './mint.mjs';
import {
  PAYMENT_FREE,
  phaseIsOpen,
} from './policy.mjs';
import { loadState, saveState } from './state.mjs';

export const PAYMENT_ETH = 1;
export const PAYMENT_URU = 2;
export const PAYMENT_URU_CURVE = 3;
const CURVE_SLIPPAGE_BPS = 500n;

function maxPaymentWithSlippage(quote) {
  return (quote * (10_000n + CURVE_SLIPPAGE_BPS)) / 10_000n;
}

function mintTxValue(phase, quantity) {
  return phase.payment === PAYMENT_ETH ? phase.price * BigInt(quantity) : 0n;
}

export async function requestRandomnessTickets(config, { nonce, paramsHash, phaseId, phase, quantity, maxPayment }) {
  const res = await fetch(`${config.siteUrl}/api/randomness/ticket`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chainId: config.chainId,
      contract: config.minter,
      action: 'mint',
      user: getAddress(config.wallet),
      nonce: nonce.toString(),
      paramsHash,
      params: {
        phaseId,
        payment: phase.payment,
        price: phase.price.toString(),
        quantity,
        maxPerWallet: phase.maxPerWallet,
        maxPayment: maxPayment.toString(),
      },
    }),
  });
  const text = await res.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    body = { error: text };
  }
  if (!res.ok) {
    const err = new Error(body.error || res.statusText || 'randomness ticket failed');
    err.status = res.status;
    throw err;
  }

  const rawTickets = body.tickets ?? [body.ticket];
  const signatures = body.signatures ?? [body.signature];
  const tickets = rawTickets.map((ticket) => ({
    action: ticket.action,
    user: ticket.user,
    nonce: BigInt(ticket.nonce),
    deadline: BigInt(ticket.deadline),
    serverSeed: ticket.serverSeed,
    paramsHash: ticket.paramsHash,
  }));
  return { tickets, signatures };
}

export async function previewPaidMint(config, { phaseId, quantity = 1 } = {}) {
  requireWallet(config);
  requireRpc(config);
  const client = createChainClient(config);
  const phases = await loadMintPhases(client, config.minter, config.wallet);

  const target = phaseId !== undefined
    ? phases.find((p) => p.phaseId === phaseId)
    : phases.find((p) => p.open && p.info.payment !== PAYMENT_FREE && p.remaining >= quantity);

  if (!target) {
    return { eligible: false, reason: 'no open paid phase found', phases: phases.map(summarizePaidPhase) };
  }

  const allowlist = await fetchMintAllowlistProof(config.siteUrl, target.info.merkleRoot, config.wallet);
  const maxPayment = await resolveMaxPayment(client, config, target, quantity);

  return {
    eligible: target.open && target.remaining >= quantity && allowlist !== null,
    phaseId: target.phaseId,
    payment: target.info.payment,
    quantity,
    maxPayment: maxPayment.toString(),
    ethValue: mintTxValue(target.info, quantity).toString(),
    hasAllowlist: allowlist !== null,
    phases: phases.map(summarizePaidPhase),
  };
}

function summarizePaidPhase(phase) {
  return {
    phaseId: phase.phaseId,
    payment: phase.info.payment,
    open: phase.open,
    remaining: phase.remaining,
    price: formatEther(phase.info.price),
  };
}

async function resolveMaxPayment(client, config, target, quantity) {
  const { info } = target;
  if (info.payment === PAYMENT_URU_CURVE) {
    const quote = await client.readContract({
      address: config.minter,
      abi: minterAbi,
      functionName: 'currentMintPrice',
      args: [target.phaseId, quantity],
    });
    return maxPaymentWithSlippage(quote);
  }
  if (info.payment === PAYMENT_URU) {
    return info.price * BigInt(quantity);
  }
  return 0n;
}

export async function runPaidMint(config, { phaseId, quantity = 1, force = false } = {}) {
  requireWallet(config);
  requireRpc(config);
  requireSigner(config);

  const account = privateKeyToAccount(requireSigner(config));
  if (account.address.toLowerCase() !== config.wallet.toLowerCase()) {
    throw new Error('URUFU_PRIVATE_KEY does not match URUFU_WALLET');
  }

  const state = await loadState(config.statePath);
  const preview = await previewPaidMint(config, { phaseId, quantity });
  if (!preview.eligible) {
    return { skipped: true, reasons: [preview.reason || 'not eligible'], preview };
  }

  const client = createChainClient(config);
  const phases = await loadMintPhases(client, config.minter, config.wallet);
  const target = phases.find((p) => p.phaseId === preview.phaseId);
  if (!target) return { skipped: true, reasons: ['phase not found'], preview };

  const allowlist = await fetchMintAllowlistProof(config.siteUrl, target.info.merkleRoot, config.wallet);
  if (!allowlist) return { skipped: true, reasons: ['not on allowlist'], preview };

  const maxPayment = await resolveMaxPayment(client, config, target, quantity);
  const [nonce, paramsHash] = await Promise.all([
    client.readContract({
      address: config.minter,
      abi: minterAbi,
      functionName: 'mintNonce',
      args: [getAddress(config.wallet)],
    }),
    client.readContract({
      address: config.minter,
      abi: minterAbi,
      functionName: 'mintParamsHash',
      args: [target.phaseId, quantity, maxPayment],
    }),
  ]);

  const { tickets, signatures } = await requestRandomnessTickets(config, {
    nonce,
    paramsHash,
    phaseId: target.phaseId,
    phase: target.info,
    quantity,
    maxPayment,
  });

  const walletClient = createWalletClient({
    account,
    chain: base,
    transport: http(config.rpcUrl),
  });

  if (target.info.payment === PAYMENT_URU || target.info.payment === PAYMENT_URU_CURVE) {
    const allowance = await client.readContract({
      address: config.uru,
      abi: erc20Abi,
      functionName: 'allowance',
      args: [getAddress(config.wallet), config.minter],
    });
    if (allowance < maxPayment) {
      const approveHash = await walletClient.writeContract({
        address: config.uru,
        abi: erc20Abi,
        functionName: 'approve',
        args: [config.minter, maxPayment],
      });
      await client.waitForTransactionReceipt({ hash: approveHash });
    }
  }

  const value = mintTxValue(target.info, quantity);
  const txHash = await walletClient.writeContract({
    address: config.minter,
    abi: minterAbi,
    functionName: 'mintBatchWithTickets',
    args: [target.phaseId, allowlist.proof, tickets, signatures, maxPayment],
    value,
  });

  state.lastMintAtMs = Date.now();
  state.lastMintTxHash = txHash;
  state.consecutiveErrors = 0;
  await saveState(config.statePath, state);

  return {
    skipped: false,
    txHash,
    paidByUser: true,
    ethValue: value.toString(),
    maxPayment: maxPayment.toString(),
    phaseId: target.phaseId,
    preview,
  };
}

export function pickOpenPhase(phases, { preferFree, phaseId, quantity = 1 }) {
  if (phaseId !== undefined) return phases.find((p) => p.phaseId === phaseId) ?? null;
  if (preferFree) {
    return phases.find((p) => p.open && p.info.payment === PAYMENT_FREE && p.remaining >= quantity) ?? null;
  }
  return phases.find((p) => p.open && p.info.payment !== PAYMENT_FREE && p.remaining >= quantity) ?? null;
}

export { phaseIsOpen };
