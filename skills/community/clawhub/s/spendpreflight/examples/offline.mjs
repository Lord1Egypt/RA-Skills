import { preflight_payment, check_payee } from '../scripts/offline.mjs';

// Fictional local data, not a live quote or a request to screen/pay this address.
const merchant = '0x1111111111111111111111111111111111111111';
const asset = '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913';
const policy = {
  version: 1, dailyCapUsd: 1, maxPerCallUsd: 0.05, holdAboveUsd: 0.05,
  merchantAllowlist: [merchant], merchantBlocklist: [],
  networkAllowlist: ['eip155:8453'], assetAllowlist: [{ network: 'eip155:8453', asset }],
};
const requirement = { scheme: 'exact', network: 'eip155:8453', asset, amount: '20000', payTo: merchant };
const challenge = { x402Version: 2, resource: { url: 'https://example.com/data' }, accepts: [requirement] };
console.log(JSON.stringify({
  preflight: await preflight_payment({ challenge, selected_requirement: requirement }, policy),
  payee: await check_payee({ address: merchant }, policy),
}, null, 2));
