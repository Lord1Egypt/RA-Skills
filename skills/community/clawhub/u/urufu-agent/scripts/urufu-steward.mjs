#!/usr/bin/env node
import { loadConfig } from './config.mjs';
import { printCheckReport, runCheck, runClaim } from './claim.mjs';
import { printMintReport, runMint, runMintPreview } from './mint.mjs';
import { previewPaidMint, runPaidMint } from './mint-paid.mjs';

function parseFlag(args, name) {
  const hit = args.find((a) => a.startsWith(`${name}=`));
  return hit ? hit.split('=').slice(1).join('=') : undefined;
}

function usage() {
  console.log(`urufu-steward — urufu gēmu agent CLI

Usage:
  node urufu-steward.mjs check
  node urufu-steward.mjs claim [--force]
  node urufu-steward.mjs mint-preview [--phase=N] [--qty=N]
  node urufu-steward.mjs mint [--force] [--phase=N] [--qty=N]
  node urufu-steward.mjs mint-paid [--force] [--phase=N] [--qty=N]

Env:
  URUFU_WALLET          wallet address (required)
  URUFU_PRIVATE_KEY     signing key (claim/mint)
  URUFU_RPC_URL         YOUR Base RPC (required — Alchemy, QuickNode, etc.)
  URUFU_INDEXER         indexer base URL
  URUFU_SITE_URL        site for gasless relay (default urufu.xyz)
  URUFU_MINTER          ChibiMinter address
  URUFU_AGENT_STATE     state file path
  URUFU_CLAIM_INTERVAL_MS  claim cooldown (default 6h)
  URUFU_MINT_INTERVAL_MS   mint cooldown (default 24h)
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  if (!command || command === '--help' || command === '-h') {
    usage();
    process.exit(command ? 0 : 1);
  }

  const config = loadConfig();
  const force = args.includes('--force');
  const phaseRaw = parseFlag(args, '--phase');
  const qtyRaw = parseFlag(args, '--qty');
  const phaseId = phaseRaw !== undefined ? Number(phaseRaw) : undefined;
  const quantity = qtyRaw !== undefined ? Number(qtyRaw) : 1;

  if (command === 'check') {
    const report = await runCheck(config);
    console.log(printCheckReport(report));
    console.log(JSON.stringify({
      ok: true,
      claim: report.claim,
      mint: report.mint,
      yield: report.yield,
      mintPreview: report.mintPreview,
    }, null, 2));
    return;
  }

  if (command === 'claim') {
    const result = await runClaim(config, { force });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'mint-preview') {
    const report = await runMintPreview(config, { phaseId, quantity });
    console.log(printMintReport(report));
    console.log(JSON.stringify({ ok: true, mint: report.mint, preview: report.preview }, null, 2));
    return;
  }

  if (command === 'mint') {
    const result = await runMint(config, { force, phaseId, quantity });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'mint-paid') {
    const result = await runPaidMint(config, { force, phaseId, quantity });
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'mint-paid-preview') {
    const preview = await previewPaidMint(config, { phaseId, quantity });
    console.log(JSON.stringify({ ok: true, preview }, null, 2));
    return;
  }

  usage();
  process.exit(1);
}

main().catch((error) => {
  console.error(JSON.stringify({
    ok: false,
    error: error.message,
    status: error.status ?? null,
    backoffMs: error.backoffMs ?? null,
  }, null, 2));
  process.exit(1);
});
