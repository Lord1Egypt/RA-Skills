#!/usr/bin/env node
/**
 * Read-only discovery audit for external registries.
 * Does not call SignalLayer, wallets, facilitators' settlement endpoints or Floot.
 * No payment payloads or credentials.
 */
const payee = "0x60B3C6c053E926460D1E1053c516c859C95365e6";
const expectedMcpName = "io.github.xavierleterrible-hub/signallayer";
const expectedToolPaths = [
  "/_api/v1/agent/preflight",
  "/_api/v1/market/execution-intel",
  "/_api/v1/web/structured-extract"
];
async function jsonGet(url) {
  try {
    const response = await fetch(url, {
      headers: { Accept: "application/json" },
      signal: AbortSignal.timeout(22000),
      redirect: "manual"
    });
    if (!response.ok) return { status: response.status, ok: false, reason: "http_error" };
    const body = await response.json();
    return { status: response.status, ok: true, body };
  } catch (e) {
    return { ok: false, reason: String(e?.message || e).slice(0,200) };
  }
}

const payaiUrl = new URL("https://facilitator.payai.network/discovery/resources");
payaiUrl.searchParams.set("payTo", payee);
payaiUrl.searchParams.set("limit", "100");
const registryUrl = new URL("https://registry.modelcontextprotocol.io/v0.1/servers");
registryUrl.searchParams.set("search", expectedMcpName);
const baselineUrl = new URL("https://facilitator.payai.network/discovery/resources");
baselineUrl.searchParams.set("limit", "1");
const [payai, mcp, baseline] = await Promise.all([
  jsonGet(payaiUrl),
  jsonGet(registryUrl),
  jsonGet(baselineUrl)
]);

const clawhubUrl = "https://clawhub.ai/api/v1/skills/signallayer-preflight";
const clawhub = await jsonGet(clawhubUrl);
const report = { checkedAt: new Date().toISOString(), mode: "external-catalogs-only" };
const clawhubRecord = clawhub.ok ? (clawhub.body?.skill || clawhub.body || {}) : {};
report.clawhub = clawhub.ok ? {
  status: "responded",
  httpStatus: clawhub.status,
  slug: clawhubRecord.slug ?? null,
  displayName: clawhubRecord.displayName ?? clawhubRecord.name ?? null,
  latestVersion: clawhubRecord.latestVersion ?? clawhubRecord.latest?.version ?? null,
  statsDownloads: clawhubRecord.statsDownloads ?? clawhubRecord.stats?.downloads ?? null,
  statsSkillsShInstalls: clawhubRecord.statsSkillsShInstalls ?? null,
  statsInstallsCurrent: clawhubRecord.statsInstallsCurrent ?? null,
  statsInstallsAllTime: clawhubRecord.statsInstallsAllTime ?? null,
  note: "Downloads count archive fetches, not distinct customers or paid API calls."
} : { status: "unverified", httpStatus: clawhub.status ?? null, reason: clawhub.reason ?? null };
const baselineBody = baseline.ok ? (baseline.body ?? {}) : {};
report.payaiGlobalCatalog = baseline.ok ? {
  httpStatus: baseline.status,
  itemsInSample: Array.isArray(baselineBody.items) ? baselineBody.items.length :
    Array.isArray(baselineBody.resources) ? baselineBody.resources.length : null,
  totalAdvertised: baselineBody.pagination?.total ?? null
} : { status: "unverified", reason: baseline.reason, httpStatus: baseline.status || null };
if (payai.ok) {
  const body = payai.body ?? {};
  const items = Array.isArray(body.items) ? body.items :
    Array.isArray(body.resources) ? body.resources : [];
  const ours = items.filter(x =>
    (x.accepts ?? []).some(a => String(a.payTo||"").toLowerCase() === payee.toLowerCase())
  );
  const resources = ours.map(x => ({
    resource: typeof x.resource === "string" ? x.resource : x.resource?.url || null,
    networks: [...new Set((x.accepts ?? []).map(a => a.network).filter(Boolean))],
    pricesAtomic: [...new Set((x.accepts ?? []).map(a => String(a.amount ?? a.maxAmountRequired ?? "")).filter(Boolean))]
  }));
  const foundPaths = expectedToolPaths.filter(path => resources.some(r => r.resource?.includes(path)));
  report.payai = {
    status: "responded",
    httpStatus: payai.status,
    itemsReturned: items.length,
    totalAdvertised: body.pagination?.total ?? null,
    matchedPayee: ours.length,
    foundPaths,
    missingPaths: expectedToolPaths.filter(x => !foundPaths.includes(x)),
    resources,
    caution: "Missing a resource from this response is not proof the endpoint is unlisted: provider filtering, pagination and asynchronous Bazaar ingestion may differ."
  };
} else report.payai = { status: "unverified", reason: payai.reason, httpStatus: payai.status || null };

if (mcp.ok) {
  const body = mcp.body ?? {};
  const servers = Array.isArray(body.servers) ? body.servers : Array.isArray(body.items) ? body.items : [];
  const found = servers.filter(x => (x.server?.name ?? x.name ?? "") === expectedMcpName);
  report.officialMcpRegistry = {
    status: "responded", httpStatus: mcp.status,
    found: found.length > 0,
    entries: found.map(x => ({
      name: x.server?.name || x.name,
      version: x.server?.version || x.version || null,
      status: x._meta?.["io.modelcontextprotocol.registry/official"]?.status ?? null,
      remotes: x.server?.remotes ?? x.remotes ?? []
    })).slice(0,4),
    caution: "Version here may lag the live MCP server until a separate publisher run."
  };
} else report.officialMcpRegistry = { status: "unverified", reason: mcp.reason, httpStatus: mcp.status || null };

console.log(JSON.stringify(report, null, 2));
// A missing listing is an actionable observation, not a test failure.
