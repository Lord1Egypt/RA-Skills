import { Type } from "@sinclair/typebox";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-runtime";
import { jsonResult, readStringParam, readNumberParam } from "openclaw/plugin-sdk/provider-web-search";

function getBaseUrl(api: OpenClawPluginApi): string {
  return (api.config as any)?.apiUrl || "https://pay.frontiercompute.io";
}

function getApiKey(api: OpenClawPluginApi): string | undefined {
  return (api.config as any)?.apiKey;
}

async function zap1Fetch(url: string, init?: RequestInit): Promise<unknown> {
  const resp = await fetch(url, init);
  if (!resp.ok) throw new Error(`ZAP1 API returned ${resp.status}`);
  return resp.json();
}

export function createZap1Tools(api: OpenClawPluginApi) {
  const base = getBaseUrl(api);

  return [
    {
      name: "zap1_protocol_info",
      label: "ZAP1 Protocol Info",
      description: "Get ZAP1 protocol metadata: version, event types, hash function, FROST status.",
      parameters: Type.Object({}, { additionalProperties: false }),
      execute: async (_toolCallId: string, _rawParams: Record<string, unknown>) => {
        return jsonResult(await zap1Fetch(`${base}/protocol/info`));
      },
    },
    {
      name: "zap1_stats",
      label: "ZAP1 Stats",
      description: "Get current network stats: anchor count, leaf count, event type distribution.",
      parameters: Type.Object({}, { additionalProperties: false }),
      execute: async (_toolCallId: string, _rawParams: Record<string, unknown>) => {
        return jsonResult(await zap1Fetch(`${base}/stats`));
      },
    },
    {
      name: "zap1_verify_proof",
      label: "ZAP1 Verify Proof",
      description: "Check if an attestation proof is valid by leaf hash. Returns validity status.",
      parameters: Type.Object({
        leaf_hash: Type.String({ description: "64-char hex leaf hash to verify" }),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const leaf = readStringParam(rawParams, "leaf_hash", { required: true });
        return jsonResult(await zap1Fetch(`${base}/verify/${leaf}/check`));
      },
    },
    {
      name: "zap1_get_proof_bundle",
      label: "ZAP1 Proof Bundle",
      description: "Get the full proof bundle for a leaf hash. Contains leaf, proof path, root, anchor txid, and block height for independent verification.",
      parameters: Type.Object({
        leaf_hash: Type.String({ description: "64-char hex leaf hash" }),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const leaf = readStringParam(rawParams, "leaf_hash", { required: true });
        return jsonResult(await zap1Fetch(`${base}/verify/${leaf}/proof.json`));
      },
    },
    {
      name: "zap1_anchor_status",
      label: "ZAP1 Anchor Status",
      description: "Get current Merkle tree state: root, unanchored leaves, anchor recommendation.",
      parameters: Type.Object({}, { additionalProperties: false }),
      execute: async (_toolCallId: string, _rawParams: Record<string, unknown>) => {
        return jsonResult(await zap1Fetch(`${base}/anchor/status`));
      },
    },
    {
      name: "zap1_anchor_history",
      label: "ZAP1 Anchor History",
      description: "Get all anchored Merkle roots with txids and block heights.",
      parameters: Type.Object({}, { additionalProperties: false }),
      execute: async (_toolCallId: string, _rawParams: Record<string, unknown>) => {
        return jsonResult(await zap1Fetch(`${base}/anchor/history`));
      },
    },
    {
      name: "zap1_recent_events",
      label: "ZAP1 Recent Events",
      description: "Get recent attestation events from the protocol.",
      parameters: Type.Object({
        limit: Type.Optional(Type.Number({ description: "Number of events to return (default 10)", minimum: 1, maximum: 100 })),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const limit = readNumberParam(rawParams, "limit", { integer: true }) || 10;
        return jsonResult(await zap1Fetch(`${base}/events?limit=${limit}`));
      },
    },
    {
      name: "zap1_decode_memo",
      label: "ZAP1 Decode Memo",
      description: "Decode a Zcash shielded memo. Identifies ZAP1, ZIP 302, text, binary, and empty formats.",
      parameters: Type.Object({
        memo_hex: Type.String({ description: "Hex-encoded memo bytes" }),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const hex = readStringParam(rawParams, "memo_hex", { required: true });
        const resp = await fetch(`${base}/memo/decode`, { method: "POST", body: hex });
        if (!resp.ok) throw new Error(`Decode returned ${resp.status}`);
        return jsonResult(await resp.json());
      },
    },
    {
      name: "zap1_create_event",
      label: "ZAP1 Create Event",
      description: "Create an attestation event. Requires API key. Supported lifecycle: CONTRACT_ANCHOR, DEPLOYMENT, HOSTING_PAYMENT, SHIELD_RENEWAL, TRANSFER, EXIT. Governance: GOVERNANCE_PROPOSAL, GOVERNANCE_VOTE, GOVERNANCE_RESULT. Agent: AGENT_REGISTER, AGENT_POLICY, AGENT_ACTION.",
      parameters: Type.Object({
        event_type: Type.String({ description: "Event type name" }),
        wallet_hash: Type.String({ description: "Participant wallet identifier" }),
        serial_number: Type.Optional(Type.String({ description: "Machine/asset serial" })),
        contract_sha256: Type.Optional(Type.String({ description: "Contract artifact SHA-256 (CONTRACT_ANCHOR)" })),
        facility_id: Type.Optional(Type.String({ description: "Facility identifier (DEPLOYMENT)" })),
        month: Type.Optional(Type.Number({ description: "Month 1-12 (HOSTING_PAYMENT)" })),
        year: Type.Optional(Type.Number({ description: "Year (HOSTING_PAYMENT, SHIELD_RENEWAL)" })),
        new_wallet_hash: Type.Optional(Type.String({ description: "New owner wallet (TRANSFER)" })),
        proposal_id: Type.Optional(Type.String({ description: "Proposal ID (governance types)" })),
        proposal_hash: Type.Optional(Type.String({ description: "Proposal hash (GOVERNANCE_PROPOSAL)" })),
        vote_commitment: Type.Optional(Type.String({ description: "Vote hash (GOVERNANCE_VOTE)" })),
        result_hash: Type.Optional(Type.String({ description: "Result hash (GOVERNANCE_RESULT)" })),
        agent_id: Type.Optional(Type.String({ description: "Agent identifier (AGENT_*)" })),
        pubkey_hash: Type.Optional(Type.String({ description: "Agent public key hash (AGENT_REGISTER)" })),
        model_hash: Type.Optional(Type.String({ description: "Model hash (AGENT_REGISTER)" })),
        policy_hash: Type.Optional(Type.String({ description: "Policy hash (AGENT_REGISTER)" })),
        policy_version: Type.Optional(Type.Number({ description: "Policy version (AGENT_POLICY)" })),
        rules_hash: Type.Optional(Type.String({ description: "Rules hash (AGENT_POLICY)" })),
        action_type: Type.Optional(Type.String({ description: "Action type (AGENT_ACTION)" })),
        input_hash: Type.Optional(Type.String({ description: "Input hash (AGENT_ACTION)" })),
        output_hash: Type.Optional(Type.String({ description: "Output hash (AGENT_ACTION)" })),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const apiKey = getApiKey(api);
        if (!apiKey) return jsonResult({ error: "API key required. Set apiKey in plugin config." });
        const resp = await fetch(`${base}/event`, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}` },
          body: JSON.stringify(rawParams),
        });
        if (!resp.ok) return jsonResult({ error: `${resp.status}: ${await resp.text()}` });
        return jsonResult(await resp.json());
      },
    },
    {
      name: "zap1_lifecycle",
      label: "ZAP1 Lifecycle",
      description: "Get the full lifecycle view for a participant wallet hash.",
      parameters: Type.Object({
        wallet_hash: Type.String({ description: "Participant wallet identifier" }),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const wallet = readStringParam(rawParams, "wallet_hash", { required: true });
        return jsonResult(await zap1Fetch(`${base}/lifecycle/${wallet}`));
      },
    },
    {
      name: "zap1_agent_status",
      label: "ZAP1 Agent Status",
      description: "Get attestation summary for an agent: registration, policies, actions, events.",
      parameters: Type.Object({
        agent_id: Type.Optional(Type.String({ description: "Agent ID (defaults to this agent)" })),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const agentId = readStringParam(rawParams, "agent_id", {}) || (api.config as any)?.agentId || "00zeven-alpha";
        return jsonResult(await zap1Fetch(`${base}/agent/${agentId}`));
      },
    },
    {
      name: "zap1_cohort_stats",
      label: "ZAP1 Cohort Stats",
      description: "Get mining cohort statistics: machine count, participants, volume tier, attestation stats.",
      parameters: Type.Object({}, { additionalProperties: false }),
      execute: async (_toolCallId: string, _rawParams: Record<string, unknown>) => {
        return jsonResult(await zap1Fetch(`${base}/cohort`));
      },
    },
    {
      name: "zap1_list_webhooks",
      label: "ZAP1 List Webhooks",
      description: "List registered webhooks. Requires API key.",
      parameters: Type.Object({}, { additionalProperties: false }),
      execute: async (_toolCallId: string, _rawParams: Record<string, unknown>) => {
        const apiKey = getApiKey(api);
        if (!apiKey) return jsonResult({ error: "API key required." });
        return jsonResult(await zap1Fetch(`${base}/webhooks`, {
          headers: { "Authorization": `Bearer ${apiKey}` },
        }));
      },
    },
    {
      name: "zap1_create_api_key",
      label: "ZAP1 Create API Key",
      description: "Provision a tenant API key. Admin only. Tier: builder (500 leaves/mo) or operator (unlimited).",
      parameters: Type.Object({
        name: Type.String({ description: "Key name / tenant identifier" }),
        tier: Type.String({ description: "builder or operator" }),
      }, { additionalProperties: false }),
      execute: async (_toolCallId: string, rawParams: Record<string, unknown>) => {
        const apiKey = getApiKey(api);
        if (!apiKey) return jsonResult({ error: "API key required." });
        const resp = await fetch(`${base}/admin/keys`, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}` },
          body: JSON.stringify(rawParams),
        });
        if (!resp.ok) return jsonResult({ error: `${resp.status}: ${await resp.text()}` });
        return jsonResult(await resp.json());
      },
    },
  ];
}
