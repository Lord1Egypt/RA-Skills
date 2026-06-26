/**
 * Trello Planner v1.0.8
 *
 * Security model:
 * - Credentials injected via runtime params.auth
 * - No direct environment variable access
 * - Requests restricted to Trello API
 * - No credential logging or persistence
 */

const TRELLO_API_BASE = "https://api.trello.com/1";
const TRELLO_DOMAIN = "api.trello.com";

/**
 * Ensure requests only target Trello
 */
function assertTrelloDomain(url) {
  const parsed = new URL(url);
  if (parsed.hostname !== TRELLO_DOMAIN) {
    throw new Error("Blocked request to non-Trello domain");
  }
}

/**
 * Trello API request wrapper
 */
async function trelloFetch(path, auth, params = {}) {

  if (!auth?.apiKey || !auth?.token) {
    throw new Error("Missing Trello credentials");
  }

  const url = new URL(`${TRELLO_API_BASE}${path}`);

  url.searchParams.set("key", auth.apiKey);
  url.searchParams.set("token", auth.token);

  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, v);
  }

  assertTrelloDomain(url);

  const res = await fetch(url.toString());

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  return res.json();
}

/**
 * Main skill
 */
async function trelloPlanner(params = {}) {

  const auth = params.auth;

  if (!auth?.apiKey || !auth?.token) {
    return {
      status: "error",
      error_type: "auth",
      message: "Missing Trello credentials. Configure TRELLO_API_KEY and TRELLO_TOKEN."
    };
  }

  try {

    const boards = await trelloFetch(
      "/members/me/boards",
      auth,
      { fields: "name,id" }
    );

    const targetId = params.board_id || boards?.[0]?.id;

    if (!targetId) {
      return {
        status: "success",
        data: {
          boards_available: boards.length,
          message: "Available boards: " + boards.map(b => b.name).join(", ")
        }
      };
    }

    const cards = await trelloFetch(
      `/boards/${targetId}/cards`,
      auth,
      { fields: "name,due,idList,closed" }
    );

    const openCards = cards.filter(c => !c.closed);

    const overdue = openCards.filter(
      c => c.due && new Date(c.due) < new Date()
    );

    const insights = overdue.length
      ? [`Priority: "${overdue[0].name.substring(0, 50)}..." (overdue)`]
      : ["Board healthy"];

    const healthScore =
      overdue.length / Math.max(openCards.length, 1) < 0.15
        ? "Healthy"
        : overdue.length === 0
        ? "Perfect"
        : "Needs attention";

    return {
      status: "success",
      data: {
        board_target: boards.find(b => b.id === targetId)?.name,
        cards_open: openCards.length,
        cards_total: cards.length,
        overdue_count: overdue.length,
        planner_insights: insights,
        health_score: healthScore
      },
      metadata: {
        version: "1.3.0",
        auth_source: "runtime_params",
        api_domain: "api.trello.com",
        endpoints_used: 2
      }
    };

  } catch (error) {

    const msg = error?.message || "unknown_error";

    const code =
      msg.includes("401")
        ? "auth_invalid"
        : msg.includes("429")
        ? "rate_limited"
        : "network";

    return {
      status: "error",
      error_type: code,
      message: `Trello ${code}: ${msg}`
    };
  }
}

module.exports = { trelloPlanner };
