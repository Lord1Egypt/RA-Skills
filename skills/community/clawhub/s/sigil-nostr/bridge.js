#!/usr/bin/env node
/**
 * Sigil Nostr Bridge — connects OpenClaw/Hermes agents to Nostr P2P messaging
 *
 * This bridge:
 * 1. Connects to Nostr relays with a persistent keypair
 * 2. Listens for NIP-04 encrypted DMs
 * 3. Forwards messages to an agent via HTTP (OpenClaw gateway) or stdin/stdout
 * 4. Sends agent responses back as encrypted Nostr DMs
 *
 * Usage:
 *   node bridge.js                          # standalone (stdin/stdout)
 *   node bridge.js --gateway http://localhost:18789  # OpenClaw gateway mode
 *   node bridge.js --hermes                 # Hermes CLI mode
 *
 * Environment:
 *   SIGIL_RELAY    — Nostr relay URL (default: wss://relay.damus.io)
 *   SIGIL_AGENT    — Agent name for key file (default: "agent")
 *   SIGIL_MODE     — "personal" or "service" (default: personal)
 *   SIGIL_OWNER    — Owner npub for personal mode
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { execSync, spawn } from "node:child_process";

const SIGIL_DIR = join(homedir(), ".sigil");
const RELAY = process.env.SIGIL_RELAY || "wss://relay.damus.io";
const AGENT_NAME = process.env.SIGIL_AGENT || "agent";
const MODE = process.env.SIGIL_MODE || "personal";

// Ensure .sigil directory exists
mkdirSync(SIGIL_DIR, { recursive: true });

// Parse CLI args
const args = process.argv.slice(2);
const gatewayUrl = args.includes("--gateway")
  ? args[args.indexOf("--gateway") + 1]
  : null;
const hermesMode = args.includes("--hermes");

console.log(`╔══════════════════════════════════════════╗`);
console.log(`║  Sigil Nostr Bridge                      ║`);
console.log(`║  P2P encrypted messaging for AI agents   ║`);
console.log(`╚══════════════════════════════════════════╝`);
console.log();
console.log(`  Agent:  ${AGENT_NAME}`);
console.log(`  Relay:  ${RELAY}`);
console.log(`  Mode:   ${gatewayUrl ? "OpenClaw Gateway" : hermesMode ? "Hermes CLI" : "Standalone"}`);
console.log();

// Key management
const keyFile = join(SIGIL_DIR, `${AGENT_NAME}.key`);
const accessFile = join(SIGIL_DIR, `${AGENT_NAME}.access.json`);

function loadOrCreateKey() {
  if (existsSync(keyFile)) {
    return readFileSync(keyFile, "utf-8").trim();
  }
  // Generate key using sigil CLI if available, otherwise random
  try {
    const output = execSync("sigil qr 2>/dev/null", { encoding: "utf-8" });
    const nsec = readFileSync(join(SIGIL_DIR, "user.key"), "utf-8").trim();
    writeFileSync(keyFile, nsec);
    return nsec;
  } catch {
    console.log("  Note: Install sigil-cli for key generation");
    console.log("  cargo install --git https://github.com/lmanchu/sigil sigil-cli");
    process.exit(1);
  }
}

function loadAccessControl() {
  if (existsSync(accessFile)) {
    return JSON.parse(readFileSync(accessFile, "utf-8"));
  }
  const config = {
    mode: MODE,
    owner: process.env.SIGIL_OWNER || "",
    authorized: [],
    reject_message:
      "This is a personal agent. You are not authorized to interact with it.",
  };
  writeFileSync(accessFile, JSON.stringify(config, null, 2));
  return config;
}

function isAuthorized(senderNpub, access) {
  if (access.mode === "service") return true;
  return senderNpub === access.owner || access.authorized.includes(senderNpub);
}

// Message routing
async function routeToAgent(message, senderNpub) {
  if (gatewayUrl) {
    // OpenClaw gateway mode — POST to gateway HTTP API
    try {
      const resp = await fetch(`${gatewayUrl}/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          channel: "nostr",
          sender: senderNpub,
        }),
      });
      const data = await resp.json();
      return data.response || data.message || "(no response)";
    } catch (e) {
      return `(gateway error: ${e.message})`;
    }
  } else if (hermesMode) {
    // Hermes CLI mode
    try {
      const result = execSync(
        `hermes chat -q "${message.replace(/"/g, '\\"')}" -Q -t clarify,delegation,browser`,
        { encoding: "utf-8", timeout: 60000 }
      );
      // Remove session_id line
      return result
        .split("\n")
        .filter((l) => !l.startsWith("session_id:"))
        .join("\n")
        .trim();
    } catch (e) {
      return `(hermes error: ${e.message})`;
    }
  } else {
    // Standalone mode — echo
    return `Echo: ${message}`;
  }
}

// Main
const nsec = loadOrCreateKey();
const access = loadAccessControl();

console.log(`  Key:    ${keyFile}`);
console.log(`  Access: ${accessFile}`);
console.log(`  Owner:  ${access.owner ? access.owner.slice(0, 20) + "..." : "(not set)"}`);
console.log();
console.log(
  "  To connect: install sigil-cli (Rust) for full Nostr bridge,",
);
console.log(
  "  or use the Rust hermes_bridge example for production use.",
);
console.log();
console.log("  This Node.js bridge is a reference implementation.");
console.log("  For production, use: cargo run --example hermes_bridge");
console.log();

// Note: Full Nostr WebSocket + NIP-04 in pure Node.js requires
// nostr-tools npm package. This script serves as the skill entry
// point and documentation. The actual bridge logic is in Rust
// (sigil-core/examples/hermes_bridge.rs) for performance and
// proper async WebSocket handling.

console.log("Bridge ready. Use the Rust binary for live operation:");
console.log("  cd ~/Dropbox/Dev/sigil && cargo run --example hermes_bridge");
