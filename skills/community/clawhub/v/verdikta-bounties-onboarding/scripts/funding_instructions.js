#!/usr/bin/env node
import './_env.js';
import { arg, getNetwork } from './_lib.js';
const address = arg('address');
if (!address) throw new Error('Usage: funding_instructions.js --address 0x...');
const network = getNetwork();
console.log(`Fund the approved bot wallet ${address} with ETH on ${network}.`);
console.log('Use a small owner-approved amount for the reward, evaluation prepay and gas. Keep a reserve for Base L1 data fees.');
console.log('Base Sepolia uses test ETH. Funding, signing and withdrawals require separate approval. No token swap is needed.');
