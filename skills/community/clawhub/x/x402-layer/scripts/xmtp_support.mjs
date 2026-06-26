#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { privateKeyToAccount } from "viem/accounts";
import { toBytes } from "viem";

const STUDIO_BASE = "https://studio.x402layer.cc";
const XMTP_ENV = process.env.XMTP_ENV || "production";

function usage() {
  console.log([
    "Usage:",
    "  node xmtp_support.mjs status <thread_id>",
    "  node xmtp_support.mjs messages <thread_id>",
    "  node xmtp_support.mjs send <thread_id> <message>",
    "  node xmtp_support.mjs revoke-others",
  ].join("\n"));
}

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Set ${name}`);
  }
  return value;
}

function normalizeWallet(address) {
  return address.trim().toLowerCase();
}

function getDbPath(walletAddress) {
  const explicit = process.env.XMTP_DB_PATH;
  if (explicit) return explicit;
  const dir = path.join(os.homedir(), ".x402studio", "xmtp");
  fs.mkdirSync(dir, { recursive: true });
  return path.join(dir, `xmtp-${XMTP_ENV}-${walletAddress}.db3`);
}

async function supportToken() {
  const existing = process.env.SUPPORT_AGENT_TOKEN;
  if (existing) return existing;

  const wallet = normalizeWallet(requireEnv("WALLET_ADDRESS"));
  const privateKey = requireEnv("PRIVATE_KEY");
  const account = privateKeyToAccount(privateKey);

  const nonceResponse = await fetch(`${STUDIO_BASE}/api/support/agent/auth/nonce`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    body: JSON.stringify({ wallet_address: wallet }),
  });
  const nonceData = await nonceResponse.json();
  if (!nonceResponse.ok) {
    throw new Error(nonceData.error || "Failed to create support auth nonce");
  }

  const signature = await account.signMessage({ message: nonceData.message });
  const verifyResponse = await fetch(`${STUDIO_BASE}/api/support/agent/auth/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    body: JSON.stringify({
      wallet_address: wallet,
      nonce: nonceData.nonce,
      signature,
    }),
  });
  const verifyData = await verifyResponse.json();
  if (!verifyResponse.ok) {
    throw new Error(verifyData.error || "Failed to verify support auth");
  }

  return verifyData.token;
}

async function supportRequest(pathname, init = {}) {
  const token = await supportToken();
  const headers = new Headers(init.headers || {});
  headers.set("Accept", "application/json");
  headers.set("Authorization", `Bearer ${token}`);
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${STUDIO_BASE}${pathname}`, { ...init, headers });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || `Support request failed with status ${response.status}`);
  }
  return data;
}

async function createXmtpClient() {
  let Client;
  let IdentifierKind;
  try {
    const sdk = await import("@xmtp/node-sdk");
    Client = sdk.Client;
    IdentifierKind = sdk.IdentifierKind;
  } catch (error) {
    throw new Error(
      "XMTP Node SDK could not load on this machine. Install the required native dependencies or run this helper in an environment where @xmtp/node-sdk is supported."
    );
  }

  const wallet = normalizeWallet(requireEnv("WALLET_ADDRESS"));
  const privateKey = requireEnv("PRIVATE_KEY");
  const account = privateKeyToAccount(privateKey);

  const signer = {
    type: "EOA",
    getIdentifier: () => ({
      identifier: wallet,
      identifierKind: IdentifierKind.Ethereum,
    }),
    signMessage: async (message) => {
      const signature = await account.signMessage({ message });
      return toBytes(signature);
    },
  };

  const client = await Client.create(signer, {
    env: XMTP_ENV,
    dbPath: getDbPath(wallet),
    appVersion: "x402-layer-agent/1.9.1",
  });

  if (!(await client.isRegistered())) {
    await client.register();
  }

  await client.conversations.sync();
  return { client, wallet, IdentifierKind, Client };
}

function renderableText(message) {
  const content = message?.content;
  if (typeof content === "string" && content.trim()) return content.trim();
  if (typeof content?.text === "string" && content.text.trim()) return content.text.trim();
  if (typeof content?.content === "string" && content.content.trim()) return content.content.trim();
  if (typeof content?.message === "string" && content.message.trim()) return content.message.trim();
  if (typeof message?.fallback === "string" && message.fallback.trim() && message.fallback.trim() !== "[Unsupported message]") {
    return message.fallback.trim();
  }
  return null;
}

async function resolveConversation(threadId) {
  const threadData = await supportRequest(`/api/support/agent/threads/${threadId}`);
  const { thread, participant } = threadData;
  const { client, wallet, IdentifierKind, Client } = await createXmtpClient();

  const counterpartyWallets = (participant.counterparty_base_wallets || [])
    .map((value) => String(value).toLowerCase())
    .filter((value) => value && value !== wallet);

  if (counterpartyWallets.length === 0) {
    throw new Error("No reachable counterparty wallet is available for this thread");
  }

  const canMessage = await Client.canMessage(
    counterpartyWallets.map((identifier) => ({ identifier, identifierKind: IdentifierKind.Ethereum })),
    XMTP_ENV
  );
  const reachable = counterpartyWallets.filter((candidate) => canMessage.get(candidate));

  if (reachable.length === 0) {
    throw new Error("The other side has not turned on XMTP for any linked Base wallet yet");
  }

  let conversation = null;
  if (thread.xmtp_conversation_id) {
    conversation = await client.conversations.getConversationById(thread.xmtp_conversation_id);
  }

  if (!conversation) {
    for (const candidate of reachable) {
      conversation = await client.conversations.fetchDmByIdentifier({
        identifier: candidate,
        identifierKind: IdentifierKind.Ethereum,
      });
      if (!conversation) {
        conversation = await client.conversations.createDmWithIdentifier({
          identifier: candidate,
          identifierKind: IdentifierKind.Ethereum,
        });
      }
      if (conversation) break;
    }
  }

  if (!conversation) {
    throw new Error("Failed to resolve an XMTP conversation for this thread");
  }

  if (thread.xmtp_conversation_id !== conversation.id || thread.status === "pending_xmtp") {
    await supportRequest(`/api/support/agent/threads/${threadId}`, {
      method: "PATCH",
      body: JSON.stringify({
        xmtp_conversation_id: conversation.id,
        status: "open",
      }),
    });
  }

  return { client, thread, participant, conversation, wallet };
}

async function showStatus(threadId) {
  const { thread, participant, conversation, wallet } = await resolveConversation(threadId);
  console.log(JSON.stringify({
    thread_id: thread.id,
    status: thread.status,
    role: participant.role,
    wallet,
    xmtp_conversation_id: conversation.id,
    counterparty_wallets: participant.counterparty_base_wallets,
  }, null, 2));
}

async function listMessages(threadId) {
  const { conversation } = await resolveConversation(threadId);
  await conversation.sync();
  const messages = await conversation.messages();
  const rendered = messages
    .map((message) => ({
      id: message.id,
      senderInboxId: message.senderInboxId,
      sentAt: message.sentAt?.toISOString?.() || null,
      text: renderableText(message),
    }))
    .filter((message) => message.text);
  console.log(JSON.stringify({ messages: rendered }, null, 2));
}

async function sendMessage(threadId, text) {
  if (!text.trim()) {
    throw new Error("Message text is empty");
  }
  const { conversation } = await resolveConversation(threadId);
  await conversation.sendText(text.trim());
  await conversation.sync();
  console.log(JSON.stringify({ ok: true }, null, 2));
}

async function revokeOthers() {
  const { client, wallet } = await createXmtpClient();
  await client.revokeAllOtherInstallations();
  console.log(JSON.stringify({ ok: true, wallet }, null, 2));
}

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  if (!command) {
    usage();
    process.exit(0);
  }

  if (command === "status") {
    await showStatus(rest[0]);
    return;
  }
  if (command === "messages") {
    await listMessages(rest[0]);
    return;
  }
  if (command === "send") {
    await sendMessage(rest[0], rest.slice(1).join(" "));
    return;
  }
  if (command === "revoke-others") {
    await revokeOthers();
    return;
  }

  usage();
  process.exit(1);
}

main().catch((error) => {
  console.error(JSON.stringify({ error: error instanceof Error ? error.message : String(error) }, null, 2));
  process.exit(1);
});
