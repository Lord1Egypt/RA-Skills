// Data flow: sends the project-scoped EdgeCloud API key (x-api-key) and tool arguments to the
// official Theta hosted MCP endpoint only. Only the listed read tools and four GPU write tools are
// sent; writes need confirm:true (and dry-run off), and creation needs a verified price cap.
import { ThetaConfig } from '../config.js';
import { fromHttpError, fromTransportError, sanitizeHttpErrorMessage } from '../errors.js';
import { assertApproved, snapshotBody } from '../approval.js';

// Official hosted MCP server, discovered from
// https://www.thetaedgecloud.com/.well-known/mcp/server-card.json (server 1.0.0, protocol 2025-06-18).
// It is the only public contract for GPU resource discovery, deployment events/logs and
// detailed billing; the underlying REST paths are not published. Stateless JSON-RPC
// tools/call over streamable HTTP is accepted without an initialize handshake.
export const THETA_MCP_ENDPOINT = 'https://controller.thetaedgecloud.com/mcp';

let requestSeq = 0;

function projectKey(cfg: ThetaConfig): string {
  if (!cfg.edgecloudApiKey) throw new Error('THETA_EC_API_KEY missing (project-scoped EdgeCloud API key)');
  return cfg.edgecloudApiKey;
}

function parseRpcEnvelope(text: string, contentType: string): Record<string, unknown> {
  if (contentType.includes('text/event-stream')) {
    const data = text.split(/\r?\n/)
      .filter((line) => line.startsWith('data:'))
      .map((line) => line.slice(5).trim())
      .filter(Boolean);
    for (let i = data.length - 1; i >= 0; i -= 1) {
      const parsed = JSON.parse(data[i]) as Record<string, unknown>;
      if ('result' in parsed || 'error' in parsed) return parsed;
    }
    throw new Error('Theta MCP stream ended without a JSON-RPC result');
  }
  return JSON.parse(text) as Record<string, unknown>;
}

function decodeToolResult(name: string, result: Record<string, unknown>): unknown {
  const content = Array.isArray(result.content) ? result.content as Array<Record<string, unknown>> : [];
  const texts = content.filter((item) => item.type === 'text' && typeof item.text === 'string').map((item) => item.text as string);
  const joined = texts.join('\n');
  if (result.isError) throw new Error(`Theta MCP ${name} failed: ${sanitizeHttpErrorMessage(joined).slice(0, 300) || 'unknown error'}`);
  if (result.structuredContent !== undefined) return result.structuredContent;
  try {
    return JSON.parse(joined);
  } catch {
    return { text: joined };
  }
}

// GPU node creation must carry a positive hourly cap (sent to Theta as max_price_per_hour_usd), and
// the resource's current listed price must be known and within that cap before provisioning.
async function enforceGpuPriceCap(cfg: ThetaConfig, args: Record<string, unknown>): Promise<void> {
  const cap = Number(args.max_price_per_hour_usd);
  if (typeof args.max_price_per_hour_usd !== 'number' || !Number.isFinite(cap) || cap <= 0) {
    throw new Error('create_gpu_deployment requires max_price_per_hour_usd (a positive hourly price cap)');
  }
  if (typeof args.resource_id !== 'string' || !args.resource_id.trim()) throw new Error('create_gpu_deployment requires resource_id');
  const lookup = await callThetaMcpTool(cfg, 'get_gpu_resource', { project_id: args.project_id, resource_id: args.resource_id, region: args.region }) as
    { price_per_hour_usd?: unknown; resource?: { price_per_hour_usd?: unknown } };
  const price = lookup?.price_per_hour_usd ?? lookup?.resource?.price_per_hour_usd;
  if (typeof price !== 'number' || !Number.isFinite(price)) throw new Error(`Could not verify the listed price of ${args.resource_id}; not provisioning`);
  if (price > cap) throw new Error(`Resource ${args.resource_id} lists USD ${price}/h, above the approved cap of USD ${cap}/h`);
}

const READ_ONLY_TOOLS = new Set([
  'list_gpu_resources', 'get_gpu_resource', 'list_gpu_deployment_templates',
  'list_gpu_deployments', 'get_gpu_deployment', 'get_gpu_deployment_events',
  'get_gpu_deployment_logs', 'get_billing_balance', 'get_billing_usage',
  'list_billing_top_ups', 'get_billing_pricing'
]);

// The only write tools this skill sends. Any other non-read tool name is refused.
const MUTATING_TOOLS = new Set(['create_gpu_deployment', 'start_gpu_deployment', 'stop_gpu_deployment', 'delete_gpu_deployment']);

export async function callThetaMcpTool(cfg: ThetaConfig, name: string, rawArgs: Record<string, unknown>): Promise<unknown> {
  const args = snapshotBody(rawArgs ?? {});
  if (!READ_ONLY_TOOLS.has(name)) {
    if (!MUTATING_TOOLS.has(name)) throw new Error(`Theta MCP tool ${name} is not supported by this skill`);
    assertApproved(cfg, args.confirm, `Theta MCP ${name}`);
    if (name === 'create_gpu_deployment') await enforceGpuPriceCap(cfg, args);
  }
  requestSeq += 1;
  const body = JSON.stringify({ jsonrpc: '2.0', id: requestSeq, method: 'tools/call', params: { name, arguments: args } });
  let res: Response;
  try {
    res = await fetch(THETA_MCP_ENDPOINT, {
      method: 'POST',
      redirect: 'error',
      headers: {
        'x-api-key': projectKey(cfg),
        'content-type': 'application/json',
        accept: 'application/json, text/event-stream'
      },
      body,
      signal: AbortSignal.timeout(cfg.httpTimeoutMs)
    });
  } catch (error) {
    // Never retried: several tools provision or delete billable capacity.
    throw fromTransportError('edgecloud-mcp', THETA_MCP_ENDPOINT, error);
  }
  const text = await res.text();
  if (!res.ok) throw fromHttpError('edgecloud-mcp', THETA_MCP_ENDPOINT, res.status, text);
  const envelope = parseRpcEnvelope(text, res.headers.get('content-type') ?? '');
  if (envelope.error) {
    const err = envelope.error as { code?: number; message?: string };
    throw new Error(`Theta MCP ${name} JSON-RPC error ${err.code ?? ''}: ${sanitizeHttpErrorMessage(String(err.message ?? 'unknown')).slice(0, 300)}`);
  }
  return decodeToolResult(name, (envelope.result ?? {}) as Record<string, unknown>);
}
