import { readFileSync } from "node:fs";

const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");

function assertContains(needle, label) {
  if (!server.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assertBefore(first, second, label) {
  const firstIndex = server.indexOf(first);
  const secondIndex = firstIndex === -1 ? -1 : server.indexOf(second, firstIndex + first.length);
  if (firstIndex === -1 || secondIndex === -1 || firstIndex >= secondIndex) {
    throw new Error(`${label} expected "${first}" before "${second}"`);
  }
}

assertContains("const codexWebClients = new Map(); // `${agentId}:${threadId}` -> Set<ws>", "thread-keyed web client sets");
assertContains("const codexE2eeSessionRoutes = new Map(); // `${agentId}:${e2eeSession}` -> { threadId, webKey, ws }", "e2ee session route map");
assertContains("function registerCodexE2eeSessionRoute(agentId, e2eeSession, threadId, ws)", "route registration helper");
assertContains("codexE2eeSessionRoutes.set(codexRelayKey(agentId, e2eeSession), { threadId, webKey, ws });", "route map stores e2ee session to thread");
assertContains("function addCodexWebClient(webKey, ws)", "web client set add helper");
assertContains("function removeCodexWebClient(webKey, ws)", "web client set remove helper");
assertContains("function openCodexWebClientsForKey(webKey)", "web client set read helper");
assertContains("function resolveCodexWebClientsForDaemonFrame(agentId, routeId)", "daemon route resolver");
assertContains("const routed = codexE2eeSessionRoutes.get(codexRelayKey(agentId, routeId));", "daemon route lookup uses e2ee session map");
assertContains("if (routed && routed.ws && routed.ws.readyState === routed.ws.OPEN) return [routed.ws];", "daemon route resolves to active owner socket");
assertContains("return openCodexWebClientsForKey(codexRelayKey(agentId, routeId));", "daemon route keeps direct thread fallback");
assertContains("const targets = resolveCodexWebClientsForDaemonFrame(identity.agentId, sessionId);", "daemon frames use route resolver");
assertContains("for (const target of targets) {", "daemon frames send to every resolved target");
assertContains("if (isCodexE2eeEnvelope(envelope) && envelope.session) {", "web e2ee messages are detected");
assertContains("envelope.route_thread_id = threadId;", "relay injects ticket-bound thread into e2ee hello");
assertContains("text = JSON.stringify(envelope);", "relay forwards the route-bound e2ee hello");
assertContains("registerCodexE2eeSessionRoute(identity.agentId, envelope.session, threadId, ws);", "web e2ee session is registered");
assertContains("const clientCount = addCodexWebClient(webKey, ws);", "new web connections are added without replacing existing clients");
assertContains("removeCodexWebClient(webKey, ws);", "close cleanup removes only the closing socket");
assertContains("removeCodexE2eeRoutesForWeb(identity.agentId, threadId, ws);", "close cleanup");
assertContains("if (route.webKey === webKey && (!ws || route.ws === ws)) {", "cleanup only removes routes owned by the closing socket");
assertBefore(
  "envelope.route_thread_id = threadId;",
  "daemonWs.send(text);",
  "web route thread is injected before forwarding to daemon",
);
assertBefore(
  "registerCodexE2eeSessionRoute(identity.agentId, envelope.session, threadId, ws);",
  "daemonWs.send(text);",
  "web session route registered before forwarding to daemon",
);
if (server.includes("const previous = codexWebClients.get(key);")) {
  throw new Error("web client replacement lookup is still present");
}
if (server.includes("codexWebClients.set(key, ws);")) {
  throw new Error("web client singleton set is still present");
}

const OPEN = 1;
const agentId = "parker-smoke-test";
const threadId = "thread-123";
const e2eeSession = "e2ee-random-session-456";
if (e2eeSession === threadId) {
  throw new Error("test setup must use a random E2EE session distinct from threadId");
}

const modelWebClients = new Map();
const modelRoutes = new Map();
const webSocketA = { readyState: OPEN, OPEN };
const webSocketB = { readyState: OPEN, OPEN };
const webSocketC = { readyState: OPEN, OPEN };
const webKey = `${agentId}:${threadId}`;

function modelAddWebClient(ws) {
  let clients = modelWebClients.get(webKey);
  if (!clients) {
    clients = new Set();
    modelWebClients.set(webKey, clients);
  }
  clients.add(ws);
}

function modelRegister(session, ws) {
  modelRoutes.set(`${agentId}:${session}`, { webKey, ws });
}

function modelResolve(routeId) {
  const route = modelRoutes.get(`${agentId}:${routeId}`);
  if (route && route.ws.readyState === route.ws.OPEN) return [route.ws];
  const clients = modelWebClients.get(`${agentId}:${routeId}`) || new Set();
  return [...clients].filter((webWs) => webWs.readyState === webWs.OPEN);
}

function modelRemoveOwnedRoutes(ws) {
  for (const [routeKey, route] of modelRoutes) {
    if (route.webKey === webKey && route.ws === ws) modelRoutes.delete(routeKey);
  }
}

function modelRemoveWebClient(ws) {
  const clients = modelWebClients.get(webKey);
  if (!clients) return;
  clients.delete(ws);
  if (clients.size === 0) modelWebClients.delete(webKey);
}

modelAddWebClient(webSocketA);
modelAddWebClient(webSocketB);
modelRegister(e2eeSession, webSocketA);
if (modelResolve(e2eeSession)[0] !== webSocketA) {
  throw new Error("random E2EE session did not route to the owning thread web socket");
}
const threadTargets = modelResolve(threadId);
if (threadTargets.length !== 2 || !threadTargets.includes(webSocketA) || !threadTargets.includes(webSocketB)) {
  throw new Error("direct thread fallback did not broadcast to every thread web socket");
}

modelRemoveOwnedRoutes(webSocketA);
modelRemoveWebClient(webSocketA);
modelAddWebClient(webSocketC);
modelRegister(e2eeSession, webSocketC);
modelRemoveOwnedRoutes(webSocketA);
if (modelResolve(e2eeSession)[0] !== webSocketC) {
  throw new Error("old socket cleanup removed or stole the replacement E2EE route");
}
const remainingThreadTargets = modelResolve(threadId);
if (remainingThreadTargets.length !== 2 || !remainingThreadTargets.includes(webSocketB) || !remainingThreadTargets.includes(webSocketC)) {
  throw new Error("closing one web socket removed another browser client");
}

console.log("crc e2ee session route checks passed");
