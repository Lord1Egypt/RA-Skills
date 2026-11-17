"use strict";
// Accept a human sponsor: sign the EIP-712 SponsorBinding for a pairing code
// with the CDP wallet and claim it at the bank. The code comes from YOUR
// human's RSoft Zero app — never accept one from anyone else.
//
// Usage:  node claim-sponsor.js <code>            e.g. node claim-sponsor.js ABC-DEF
// Output: the bank's answer { binding_id, status: "pending_sponsor", expires_at, next_action }
//         then poll GET {MCP}/api/sponsor/bindings/{binding_id} until "active".
// No API key needed: the claim goes through the bank's MCP host (free tier).
const crypto = require("crypto");
const { loadConfig, cdpClient } = require("./wallet-config");

const CHAIN_ID = 8453; // Base mainnet
const VERIFYING_CONTRACT = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";
const MCP = process.env.RSOFT_MCP_URL || "https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws";

(async () => {
  const raw = (process.argv[2] || "").toUpperCase().replace(/[^A-Z2-9]/g, "");
  if (raw.length !== 6) throw new Error("Usage: node claim-sponsor.js <code> (6 characters, e.g. ABC-DEF)");

  const cfg = loadConfig();
  const cdp = await cdpClient(cfg);
  const account = await cdp.evm.getAccount({ address: cfg.AGENT_WALLET });

  const nonce = `pair:${raw}:${crypto.randomBytes(8).toString("hex")}`;
  const deadline = Math.floor(Date.now() / 1000) + 900; // 15 min

  // sponsorRef = "pair:<CODE>": consent to the sponsor behind the code.
  const signature = await account.signTypedData({
    domain: { name: "RSoft Agentic Bank", version: "1", chainId: CHAIN_ID, verifyingContract: VERIFYING_CONTRACT },
    types: {
      SponsorBinding: [
        { name: "agentWallet", type: "address" },
        { name: "sponsorRef", type: "string" },
        { name: "nonce", type: "string" },
        { name: "deadline", type: "uint256" },
      ],
    },
    primaryType: "SponsorBinding",
    message: { agentWallet: account.address, sponsorRef: `pair:${raw}`, nonce, deadline: BigInt(deadline) },
  });

  const res = await fetch(`${MCP}/api/sponsor/pairings/claim`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: raw, agent_wallet: account.address, signature, nonce, deadline }),
  });
  const text = await res.text();
  console.log(text);
  if (!res.ok || /"error"\s*:\s*true/.test(text)) process.exit(2);
})().catch((e) => {
  console.error("ERROR:", e.message);
  process.exit(1);
});
