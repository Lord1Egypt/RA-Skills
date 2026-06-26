/**
 * SONA OpenClaw Plugin
 *
 * Exposes SONA's autonomous wallet capabilities as OpenClaw-compatible tools.
 * Any OpenClaw agent can install this skill and control SONA via natural language.
 *
 * Install: clawhub install sona
 *
 * Required env:
 *   SONA_API_URL   - SONA dashboard URL (default: http://localhost:3000)
 *   SONA_TOKEN     - JWT session token (from /api/auth/login)
 */

type OpenClawTool = {
  name: string
  description: string
  parameters: object
  execute: (
    id: string,
    params: Record<string, unknown>,
  ) => Promise<{ content: Array<{ type: "text"; text: string }> }>
}

type OpenClawAPI = {
  registerTool(tool: OpenClawTool, opts?: { optional?: boolean }): void
}

// ── Config ────────────────────────────────────────────────────────────────────

const RAW_URL = (process.env.SONA_API_URL ?? "http://localhost:3000").replace(/\/$/, "")
const TOKEN = process.env.SONA_TOKEN ?? ""

// Safety: only allow localhost URLs to prevent JWT cookie exfiltration to remote hosts
const ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "::1"]
const parsedHost = (() => {
  try { return new URL(RAW_URL).hostname } catch { return "" }
})()
const BASE = ALLOWED_HOSTS.includes(parsedHost) ? RAW_URL : (() => {
  console.error(`[SONA] SONA_API_URL points to non-local host "${parsedHost}". Refusing to send credentials to remote servers. Only localhost URLs are allowed.`)
  return "http://localhost:3000"
})()

// ── Helpers ───────────────────────────────────────────────────────────────────

function headers(withAuth = false): Record<string, string> {
  const h: Record<string, string> = { "Content-Type": "application/json" }
  if (withAuth && TOKEN) h["Cookie"] = `sona_session=${encodeURIComponent(TOKEN)}`
  return h
}

async function sonaGet(path: string, withAuth = false): Promise<unknown> {
  const res = await fetch(`${BASE}${path}`, { headers: headers(withAuth) })
  if (!res.ok) throw new Error(`SONA ${path} → HTTP ${res.status}`)
  return res.json()
}

async function sonaPost(path: string, body: unknown, withAuth = false): Promise<unknown> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: headers(withAuth),
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`SONA ${path} → HTTP ${res.status}`)
  return res.json()
}

/**
 * Consume a Server-Sent Events stream from /api/chat and return the full text.
 * The chat route streams JSON events; we collect all delta text chunks.
 */
async function consumeChatStream(message: string): Promise<string> {
  const res = await fetch(`${BASE}/api/chat`, {
    method: "POST",
    headers: headers(true),
    body: JSON.stringify({ message }),
  })

  if (!res.ok) throw new Error(`SONA /api/chat → HTTP ${res.status}`)
  if (!res.body) throw new Error("No response body from chat endpoint")

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let fullText = ""
  let buffer = ""

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })

    // Process complete SSE lines
    const lines = buffer.split("\n")
    buffer = lines.pop() ?? ""

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue
      const raw = line.slice(6).trim()
      if (raw === "[DONE]") continue
      try {
        const evt = JSON.parse(raw)
        // Anthropic streaming delta
        if (evt.type === "content_block_delta" && evt.delta?.text) {
          fullText += evt.delta.text
        }
        // OpenAI-style streaming delta
        if (evt.choices?.[0]?.delta?.content) {
          fullText += evt.choices[0].delta.content
        }
        // Plain text event
        if (typeof evt.text === "string") {
          fullText += evt.text
        }
        // Full message (non-streaming fallback)
        if (typeof evt.content === "string" && !fullText) {
          fullText = evt.content
        }
      } catch {
        // Non-JSON line — ignore
      }
    }
  }

  return fullText.trim() || "(No response text received)"
}

function ok(text: string) {
  return { content: [{ type: "text" as const, text }] }
}

function fail(e: unknown) {
  const msg = e instanceof Error ? e.message : String(e)
  return { content: [{ type: "text" as const, text: `Error: ${msg}` }] }
}

// ── Plugin registration ───────────────────────────────────────────────────────

export default function register(api: OpenClawAPI): void {
  if (!TOKEN) {
    console.warn("[SONA] SONA_TOKEN not set — state-changing tools (transfer, chat, set_mode, approve) will fail. Set SONA_TOKEN to a valid session JWT.")
  }

  // ── 1. get_wallet_status ──────────────────────────────────────────────────
  api.registerTool({
    name: "get_wallet_status",
    description:
      "Get SONA wallet balance, Solana address, agent name, operating mode, and cycle statistics.",
    parameters: { type: "object", properties: {} },
    execute: async () => {
      try {
        const d = await sonaGet("/api/status") as any
        return ok([
          "SONA Wallet Status",
          `  Agent:       ${d.agent?.name ?? "SONA Agent"}`,
          `  Mode:        ${d.agent?.mode ?? "unknown"}`,
          `  Balance:     ${d.wallet?.sol_balance?.toFixed(4) ?? "?"} SOL`,
          `  Cycles run:  ${d.agent?.cycles_run ?? 0}`,
          `  Executions:  ${d.agent?.successful_executions ?? 0}`,
          d.wallet?.sol_price_usd
            ? `  SOL price:   $${Number(d.wallet.sol_price_usd).toFixed(2)}`
            : "",
          d.last_cycle
            ? `  Last cycle:  ${d.last_cycle.started_at}`
            : "",
        ].filter(Boolean).join("\n"))
      } catch (e) { return fail(e) }
    },
  })

  // ── 2. get_sol_price ─────────────────────────────────────────────────────
  api.registerTool({
    name: "get_sol_price",
    description:
      "Get the current SOL/USD price as observed by SONA from the Pyth Hermes oracle feed.",
    parameters: { type: "object", properties: {} },
    execute: async () => {
      try {
        const d = await sonaGet("/api/status") as any
        const price = d.wallet?.sol_price_usd
        if (!price) return ok("SOL price not yet available — agent may not have run a cycle yet.")
        return ok(`SOL price: $${Number(price).toFixed(2)} USD (Pyth Hermes)`)
      } catch (e) { return fail(e) }
    },
  })

  // ── 3. get_agent_status ───────────────────────────────────────────────────
  api.registerTool({
    name: "get_agent_status",
    description:
      "Get full SONA agent status including mode, brain mode, cycle count, and last cycle details.",
    parameters: { type: "object", properties: {} },
    execute: async () => {
      try {
        const d = await sonaGet("/api/status") as any
        const lines = [
          "SONA Agent Status",
          `  Name:         ${d.agent?.name ?? "SONA Agent"}`,
          `  Mode:         ${d.agent?.mode ?? "unknown"}`,
          `  Cycles run:   ${d.agent?.cycles_run ?? 0}`,
          `  Executions:   ${d.agent?.successful_executions ?? 0}`,
        ]
        if (d.last_cycle) {
          lines.push(`  Last cycle:   ${d.last_cycle.started_at}`)
          lines.push(`  Cycle mode:   ${d.last_cycle.mode}`)
        }
        return ok(lines.join("\n"))
      } catch (e) { return fail(e) }
    },
  })

  // ── 4. set_mode ───────────────────────────────────────────────────────────
  api.registerTool({
    name: "set_mode",
    description:
      "Switch SONA's operating mode. standard = observe only. assisted = queue for human approval. god = full autonomous execution.",
    parameters: {
      type: "object",
      properties: {
        mode: {
          type: "string",
          enum: ["standard", "assisted", "god"],
          description: "The operating mode to switch to.",
        },
        acknowledgment: {
          type: "string",
          description:
            'Required when switching to god mode. Must be exactly "I UNDERSTAND".',
        },
      },
      required: ["mode"],
    },
    execute: async (_id, params) => {
      try {
        const { mode, acknowledgment } = params as { mode: string; acknowledgment?: string }
        const body: Record<string, string> = { mode }
        if (mode === "god") {
          if (acknowledgment !== "I UNDERSTAND") {
            return ok(
              'God mode requires acknowledgment="I UNDERSTAND". ' +
              "This enables full autonomous execution within Constitutional Law limits."
            )
          }
          body.acknowledgment = "I UNDERSTAND"
        }
        const res = await sonaPost("/api/mode", body, true) as any
        if (!res.success) return ok(`Failed to set mode: ${res.error ?? "unknown error"}`)
        return ok(`Mode switched to: ${res.mode}`)
      } catch (e) { return fail(e) }
    },
  })

  // ── 5. get_policy ─────────────────────────────────────────────────────────
  api.registerTool({
    name: "get_policy",
    description:
      "Get SONA's current YAML policy rules including triggers, action rules, contacts, and spend limits.",
    parameters: { type: "object", properties: {} },
    execute: async () => {
      try {
        const res = await sonaGet("/api/policy") as any
        const yaml = res.yaml ?? res.policy ?? JSON.stringify(res, null, 2)
        const limits = res.spend_limits
        const parts = ["SONA Policy"]
        if (limits) {
          parts.push(
            `  Per-action limit: ${limits.per_action_sol ?? "?"} SOL`,
            `  Per-session limit: ${limits.per_session_sol ?? "?"} SOL`,
          )
        }
        parts.push("", "Policy YAML:", yaml)
        return ok(parts.join("\n"))
      } catch (e) { return fail(e) }
    },
  })

  // ── 6. transfer_sol ───────────────────────────────────────────────────────
  api.registerTool({
    name: "transfer_sol",
    description:
      "Transfer SOL from the SONA wallet to a recipient address. " +
      "All Constitutional Laws apply: spend limits enforced in Rust, Memo receipt emitted on-chain.",
    parameters: {
      type: "object",
      properties: {
        to: {
          type: "string",
          description: "Recipient Solana address (base58) or a contact name defined in policy.yaml.",
        },
        amount_sol: {
          type: "number",
          description: "Amount of SOL to transfer (e.g. 0.1). Max 0.05 SOL per action by default.",
        },
      },
      required: ["to", "amount_sol"],
    },
    execute: async (_id, params) => {
      try {
        const { to, amount_sol } = params as { to: string; amount_sol: number }
        const message = `transfer ${amount_sol} SOL to ${to}`
        const text = await consumeChatStream(message)
        return ok(text)
      } catch (e) { return fail(e) }
    },
  })

  // ── 7. get_pending_actions ────────────────────────────────────────────────
  api.registerTool({
    name: "get_pending_actions",
    description:
      "List actions queued for human approval (assisted mode only). Returns cycle IDs and action details.",
    parameters: { type: "object", properties: {} },
    execute: async () => {
      try {
        const res = await sonaGet("/api/actions/pending", true) as any
        const actions = res.actions ?? []
        if (actions.length === 0) return ok("No pending actions. Queue is empty.")
        const lines = ["Pending Actions:"]
        for (const a of actions) {
          lines.push(
            `  [${a.cycle_id}]`,
            `    Type:    ${a.action?.action_type ?? "unknown"}`,
            `    Queued:  ${a.created_at}`,
            a.action?.params
              ? `    Params:  ${JSON.stringify(a.action.params)}`
              : "",
          )
        }
        return ok(lines.filter(Boolean).join("\n"))
      } catch (e) { return fail(e) }
    },
  }, { optional: true })

  // ── 8. approve_action ────────────────────────────────────────────────────
  api.registerTool({
    name: "approve_action",
    description:
      "Approve a pending action in assisted mode. The action will execute on the next agent cycle.",
    parameters: {
      type: "object",
      properties: {
        cycle_id: {
          type: "string",
          description: "The cycle_id of the action to approve (from get_pending_actions).",
        },
      },
      required: ["cycle_id"],
    },
    execute: async (_id, params) => {
      try {
        const { cycle_id } = params as { cycle_id: string }
        const res = await sonaPost("/api/actions/approve", { cycle_id }, true) as any
        if (!res.success) return ok(`Failed to approve: ${res.error ?? "unknown error"}`)
        return ok(`Action approved. Cycle ${cycle_id} will execute on the next agent cycle.`)
      } catch (e) { return fail(e) }
    },
  }, { optional: true })

  // ── 9. chat ───────────────────────────────────────────────────────────────
  api.registerTool({
    name: "chat",
    description:
      "Send a natural language command to SONA's AI agent. The agent will reason, plan, and execute. " +
      "Examples: 'swap 0.1 SOL to USDC', 'what is my balance?', 'set a rule to buy when SOL drops below 140'.",
    parameters: {
      type: "object",
      properties: {
        message: {
          type: "string",
          description: "The natural language command or question for SONA.",
        },
      },
      required: ["message"],
    },
    execute: async (_id, params) => {
      try {
        const { message } = params as { message: string }
        const text = await consumeChatStream(message)
        return ok(text)
      } catch (e) { return fail(e) }
    },
  })

  // ── 10. get_activity ──────────────────────────────────────────────────────
  api.registerTool({
    name: "get_activity",
    description:
      "Get a summary of recent SONA agent activity: cycles run, executions, current balance, and last known SOL price.",
    parameters: {
      type: "object",
      properties: {
        limit: {
          type: "number",
          description: "Not used — returns aggregate stats only.",
        },
      },
    },
    execute: async () => {
      try {
        const d = await sonaGet("/api/status") as any
        return ok([
          "SONA Recent Activity",
          `  Balance:       ${d.wallet?.sol_balance?.toFixed(4) ?? "?"} SOL`,
          `  SOL price:     $${Number(d.wallet?.sol_price_usd ?? 0).toFixed(2)}`,
          `  Mode:          ${d.agent?.mode ?? "unknown"}`,
          `  Cycles run:    ${d.agent?.cycles_run ?? 0}`,
          `  Executions:    ${d.agent?.successful_executions ?? 0}`,
          d.last_cycle ? `  Last cycle:    ${d.last_cycle.started_at}` : "",
        ].filter(Boolean).join("\n"))
      } catch (e) { return fail(e) }
    },
  })
}
