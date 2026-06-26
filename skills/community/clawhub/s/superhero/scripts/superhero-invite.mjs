#!/usr/bin/env node
// Generate invite links with AE rewards on superhero.com
// Uses AffiliationTreasury contract via CommunityFactory
import { AeSdk, Node, MemoryAccount, Contract } from '@aeternity/aepp-sdk';
import fs from 'fs';
import BigNumber from 'bignumber.js';

const NODE_URL = 'https://mainnet.aeternity.io';

function loadAccount() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set. Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  return new MemoryAccount(privateKey);
}
const FACTORY_ADDRESS = 'ct_25cqTw85wkF5cbcozmHHUCuybnfH9WaRZXSgEcNNXG9LsCJWTN';
const INVITE_BASE_URL = 'https://superhero.com#invite_code=';
const REDEMPTION_FEE_COVER = 10n ** 15n; // 0.001 AE to cover gas for redemption

async function getTreasury(aeSdk) {
  const factoryAci = JSON.parse(
    fs.readFileSync('./contracts/CommunityFactory.aci.json', 'utf8')
  );
  const factory = await Contract.initialize({
    aci: factoryAci,
    address: FACTORY_ADDRESS,
    onAccount: aeSdk,
    onNode: aeSdk.api,
  });
  const treasuryAddress = await factory.affiliation_treasury().then(r => r.decodedResult);
  return await Contract.initialize({
    aci: factoryAci,
    address: treasuryAddress,
    onAccount: aeSdk,
    onNode: aeSdk.api,
  });
}

async function main() {
  const command = process.argv[2] || 'help';

  if (command === 'help') {
    console.log(`
Invite Commands:

  generate <amount_ae> [count]
    Generate invite links with AE reward for each recipient

    amount_ae   AE gift per invite link
    count       Number of links to generate (default: 1)

  revoke <invite_address>
    Revoke an unused invite and reclaim funds

Examples:
  node scripts/superhero-invite.mjs generate 1 5
  node scripts/superhero-invite.mjs generate 0.5
  node scripts/superhero-invite.mjs revoke ak_...

Note: Total cost = (amount_ae + redemption_fee) × count + gas.
      Redemption fee cover: 0.001 AE per invite.
`);
    process.exit(0);
  }

  const account = loadAccount();
  const node = new Node(NODE_URL);
  const aeSdk = new AeSdk({
    nodes: [{ name: 'mainnet', instance: node }],
    accounts: [account],
  });

  switch (command) {
    case 'generate': {
      const amountAE = parseFloat(process.argv[3]);
      const count = parseInt(process.argv[4]) || 1;

      if (!amountAE || amountAE <= 0) {
        console.error('Usage: node scripts/superhero-invite.mjs generate <amount_ae> [count]');
        process.exit(1);
      }

      // Generate keypairs for invite codes
      const keyPairs = Array.from({ length: count }, () => MemoryAccount.generate());
      const inviteAmount = BigInt(new BigNumber(amountAE).shiftedBy(18).toFixed(0));

      // Total cost: (invite_amount + redemption_fee) per invite
      const totalPerInvite = inviteAmount + REDEMPTION_FEE_COVER;
      const totalCost = totalPerInvite * BigInt(count);
      const totalCostAE = new BigNumber(totalCost.toString()).shiftedBy(-18).toFixed(4);

      console.error(`Generating ${count} invite(s) with ${amountAE} AE each...`);
      console.error(`Total cost: ~${totalCostAE} AE (+ gas)`);

      const treasury = await getTreasury(aeSdk);

      const result = await treasury.register_invitation_code(
        keyPairs.map(kp => kp.address),
        REDEMPTION_FEE_COVER,
        inviteAmount,
        { amount: totalCost.toString() },
      );

      // Build links and output to caller
      const newInvites = keyPairs.map(kp => ({
        invite_address: kp.address,
        link: `${INVITE_BASE_URL}${kp.secretKey}`,
        amount_ae: amountAE,
      }));

      console.log(JSON.stringify({
        success: true,
        count,
        amount_ae_per_invite: amountAE,
        total_cost_ae: totalCostAE,
        tx_hash: result.hash,
        links: newInvites.map(i => i.link),
      }));
      break;
    }

    case 'revoke': {
      const inviteAddress = process.argv[3];
      if (!inviteAddress) {
        console.error('Usage: node scripts/superhero-invite.mjs revoke <invite_address>');
        process.exit(1);
      }

      const treasury = await getTreasury(aeSdk);
      console.error(`Revoking invite ${inviteAddress}...`);
      const result = await treasury.revoke_invitation_code(inviteAddress);

      console.log(JSON.stringify({
        success: true,
        revoked_address: inviteAddress,
        tx_hash: result.hash,
      }));
      break;
    }

    default:
      console.error(`Unknown command: ${command}. Run with 'help' for usage.`);
      process.exit(1);
  }
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });
