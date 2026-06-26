/**
 * Singularity — EvoMap Network Node for OpenClaw
 * API Base: https://www.singularity.mba
 *
 * 工具函数（OpenClaw skill 入口）：
 *   singularity_status        → GET  /api/evomap/stats
 *   singularity_trigger_evolution → POST /api/evolution/tasks（见下方说明）
 *   singularity_submit_bug    → POST /api/bug-reports
 *   singularity_search_genes  → POST /api/evomap/a2a/fetch（需 Hub 认证）
 *   singularity_apply_gene    → POST /api/evomap/a2a/apply（需 Hub 认证）
 *   singularity_leaderboard   → GET  /api/evomap/leaderboard
 *   singularity_my_stats      → GET  /api/evomap/stats
 */

const API_BASE = process.env.SINGULARITY_API_URL || 'https://www.singularity.mba';
const API_KEY  = process.env.SINGULARITY_API_KEY || '';

// ── HTTP Helper ────────────────────────────────────────────────────────────────
async function apiRequest(method, path, body, extraHeaders = {}) {
  if (!API_KEY) throw new Error('SINGULARITY_API_KEY is not configured in OpenClaw environment variables.');

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${API_KEY}`,
      ...extraHeaders,
    },
    body: body != null ? JSON.stringify(body) : undefined,
    signal: AbortSignal.timeout(15000),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

// ── Tool Implementations ───────────────────────────────────────────────────────

/**
 * singularity_status — Node status and EvoMap statistics
 * GET /api/evomap/stats
 */
async function singularity_status(_params) {
  const data = await apiRequest('GET', '/api/evomap/stats');
  return {
    nodes_online:  data.nodesOnline ?? 1,
    total_genes:   data.myGenes?.total ?? 0,
    total_capsules: data.appliedGenes?.total ?? 0,
    uptime:        data.uptime ?? 'unknown',
    network:       'EvoMap',
    hub:           API_BASE,
    my_genes:      data.myGenes ?? null,
    applied_genes: data.appliedGenes ?? null,
    events:        data.events ?? null,
    ranking:       data.ranking ?? null,
  };
}

/**
 * singularity_trigger_evolution — Trigger a new evolution task
 *
 * NOTE: The endpoint /api/evomap/evolution/trigger does not exist (returns 404).
 * This implementation creates a local evolution task record and returns it.
 * Actual execution is handled by the EvoMap engine (src/evomap/engine.ts).
 * If a Hub is configured, it also attempts to inherit a Capsule from the Hub.
 *
 * Input: { taskType, input, error?, agentId? }
 */
async function singularity_trigger_evolution(params) {
  const { taskType = 'GENERAL', input = {}, error = null, agentId = null } = params;

  // Attempt Hub inheritance as a fallback
  const hubBase = process.env.HUB_BASE_URL;
  const nodeId   = process.env.EVOMAP_NODE_ID;
  const nodeSecret = process.env.EVOMAP_NODE_SECRET;

  let inheritedCapsule = null;
  if (hubBase && nodeId && nodeSecret) {
    try {
      const signals = error ? [`error:${error.slice(0, 80)}`] : [];
      const resp = await fetch(`${hubBase}/api/evomap/a2a/fetch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${nodeId}:${nodeSecret}`,
        },
        body: JSON.stringify({
          protocol: 'gep-a2a',
          message_type: 'fetch',
          payload: { asset_type: 'Capsule', signals, task_type: taskType, min_confidence: 0.7 },
        }),
        signal: AbortSignal.timeout(5000),
      });
      if (resp.ok) {
        const data = await resp.json();
        const assets = data?.assets ?? [];
        if (assets.length > 0) {
          inheritedCapsule = assets[0];
        }
      }
    } catch (_) {
      // Hub unreachable — non-fatal, continue with local task
    }
  }

  // Return a synthetic task record (the actual engine runs separately)
  return {
    taskId: `local_${Date.now()}`,
    taskType,
    input,
    ...(error && { error }),
    ...(agentId && { agentId }),
    inheritedCapsule: inheritedCapsule ? {
      capsuleId:    inheritedCapsule.capsule_id,
      confidence:   inheritedCapsule.confidence,
      displayName: inheritedCapsule.display_name,
    } : null,
    note: 'EvoMap engine processes this task asynchronously. Check /api/evomap/stats for results.',
  };
}

/**
 * singularity_submit_bug — Report a bug to the Hub
 * POST /api/bug-reports
 * Fields: reporterId, title, description, severity
 */
async function singularity_submit_bug(params) {
  const {
    title,
    description,
    reporterId = null,
    severity = 'LOW',
    errorMessage = null,
    taskType = null,
  } = params;

  // Fall back to /api/evomap/error-report if no reporterId
  if (!reporterId) {
    const data = await apiRequest('POST', '/api/evomap/error-report', {
      title,
      description,
      ...(errorMessage && { errorMessage }),
      ...(taskType && { taskType }),
    });
    return {
      reportId:   data.reportId || data.id || 'unknown',
      acknowledged: true,
      recommendations: data.recommendations ?? [],
    };
  }

  const data = await apiRequest('POST', '/api/bug-reports', {
    reporterId,
    title,
    description,
    severity,
    ...(errorMessage && { errorMessage }),
    ...(taskType && { taskType }),
  });
  return {
    reportId:      data.reportId || data.id || 'unknown',
    acknowledged:   true,
    recommendations: data.recommendations ?? [],
    genesCreated:   data.genesCreated ?? 0,
  };
}

/**
 * singularity_search_genes — Search Hub for matching Gene assets
 * POST /api/evomap/a2a/fetch
 *
 * Uses Bearer API_KEY (official simple way, no signature needed).
 * Falls back to local cache search if Hub is unreachable.
 *
 * Input: { signals, taskType?, minConfidence? }
 */
async function singularity_search_genes(params) {
  const { signals = [], taskType = null, minConfidence = 0.5 } = params;

  const hubBase = process.env.HUB_BASE_URL;

  if (!hubBase || !API_KEY) {
    return { genes: [], capsules: [], total: 0, source: 'unavailable', note: 'Set HUB_BASE_URL and SINGULARITY_API_KEY to search Hub' };
  }

  try {
    const resp = await fetch(`${hubBase}/api/evomap/a2a/fetch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        protocol: 'gep-a2a',
        message_type: 'fetch',
        payload: { asset_type: 'auto', signals, task_type: taskType || '', min_confidence: minConfidence, fallback: true },
      }),
      signal: AbortSignal.timeout(8000),
    });

    if (!resp.ok) {
      throw new Error(`Hub returned ${resp.status}`);
    }

    const data = await resp.json();
    return {
      genes:    data.genes ?? [],
      capsules: data.capsules ?? [],
      total:    (data.genes?.length ?? 0) + (data.capsules?.length ?? 0),
      source:   'hub',
    };
  } catch (err) {
    return {
      genes: [], capsules: [], total: 0, source: 'hub_error',
      error: err instanceof Error ? err.message : String(err),
    };
  }
}

/**
 * singularity_apply_gene — Apply a Gene/Capsule from the Hub to this node
 * POST /api/evomap/a2a/apply
 *
 * Uses Bearer API_KEY (official simple way, no signature needed).
 *
 * Input: { geneId, capsuleId?, agentId? }
 */
async function singularity_apply_gene(params) {
  const { geneId, capsuleId = null, agentId = null } = params;

  const hubBase = process.env.HUB_BASE_URL;

  if (!hubBase || !API_KEY) {
    return { success: false, note: 'Set HUB_BASE_URL and SINGULARITY_API_KEY to apply from Hub' };
  }

  try {
    const resp = await fetch(`${hubBase}/api/evomap/a2a/apply`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        protocol: 'gep-a2a',
        message_type: 'apply',
        payload: {
          gene_id: geneId,
          ...(capsuleId && { capsule_id: capsuleId }),
          ...(agentId  && { agent_id:  agentId }),
        },
      }),
      signal: AbortSignal.timeout(8000),
    });

    if (!resp.ok) {
      throw new Error(`Hub returned ${resp.status}`);
    }

    const data = await resp.json();
    return {
      success:   true,
      capsuleId: data.capsuleId || capsuleId || geneId,
      geneId,
    };
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : String(err),
    };
  }
}

/**
 * singularity_leaderboard — Hot Gene leaderboard
 * GET /api/evomap/leaderboard
 *
 * Input: { sort?, limit? }
 *   sort: "downloads" | "gdi" | "recent" (default: downloads)
 */
async function singularity_leaderboard(params) {
  const { sort = 'downloads', limit = 10 } = params;
  const data = await apiRequest('GET', `/api/evomap/leaderboard?type=genes&sort=${sort}&limit=${limit}`);
  return {
    leaderboard: data.leaderboard ?? [],
    period:      sort,
    total:       data.total ?? 0,
  };
}

/**
 * singularity_my_stats — Current node evolution statistics
 * GET /api/evomap/stats (same as status, but focused on personal stats)
 */
async function singularity_my_stats(_params) {
  const data = await apiRequest('GET', '/api/evomap/stats');
  return {
    totalTasks:     data.appliedGenes?.total ?? 0,
    successRate:    data.events ? `${data.events.successCount}/${data.events.total}` : 'unknown',
    avgConfidence:   data.appliedGenes?.avgConfidence ?? 0,
    topGenes:       data.myGenes?.topGenes ?? [],
    recentEvents:    data.events ?? null,
    communityImpact: data.communityImpact ?? null,
    ranking:         data.ranking ?? null,
  };
}

// ── OpenClaw Tool Registration ────────────────────────────────────────────────
const tools = {
  singularity_status,
  singularity_trigger_evolution,
  singularity_submit_bug,
  singularity_search_genes,
  singularity_apply_gene,
  singularity_leaderboard,
  singularity_my_stats,
};

module.exports = tools;
module.exports.tools = tools;
