/**
 * Scope Isolation - AGENT/USER/TEAM/GLOBAL四级隔离
 * Filter memories by scope level + team namespace isolation
 *
 * Team isolation model:
 * - Each team has its own memory namespace prefixed with `team:{team_id}:`
 * - TEAM-scope memories belong to a specific team (stored with team_id)
 * - Cross-team (shared) memories use explicit GLOBAL scope
 * - USER and AGENT scopes are personal to a user/agent and never cross-team
 */

export const SCOPE_LEVELS = ['AGENT', 'USER', 'TEAM', 'GLOBAL'];
export const SCOPE_HIERARCHY = { AGENT: 0, USER: 1, TEAM: 2, GLOBAL: 3 };

// ============ Team Namespace Registry ============

/** @type {Map<string, { name: string, created_at: number, memoryCount: number }>} */
const teamRegistry = new Map();

/** Current active team context (thread-local via global) */
const TEAM_CONTEXT = {
  current: null, // team_id or null for no-team
};

// ============ Agent Context (for AGENT-scope isolation) ============

/** Current active agent context */
const AGENT_CONTEXT = {
  current: null, // agent_id string or null
};

/**
 * Set current agent context for memory operations
 * Call this at the start of each agent session
 * @param {string|null} agentId
 */
export function setCurrentAgentId(agentId) {
  AGENT_CONTEXT.current = agentId || null;
}

/**
 * Get current agent context
 * @returns {string|null}
 */
export function getCurrentAgentId() {
  return AGENT_CONTEXT.current;
}

/**
 * Switch agent context (returns previous)
 * @param {string|null} agentId
 * @returns {string|null} previous agent_id
 */
export function switchAgentId(agentId) {
  const prev = AGENT_CONTEXT.current;
  AGENT_CONTEXT.current = agentId || null;
  return prev;
}

/**
 * Normalize a scope string to SCOPE_LEVELS
 * @param {string} scope
 * @returns {string}
 */
export function normalizeScope(scope) {
  if (!scope) return 'GLOBAL';
  const upper = scope.toUpperCase();
  return SCOPE_LEVELS.includes(upper) ? upper : 'GLOBAL';
}

/**
 * Get effective scope for a scope string
 * @param {string} scope
 * @returns {string}
 */
export function getEffectiveScope(scope) {
  return normalizeScope(scope);
}

/**
 * Filter memories by scope level (with agent_id isolation for AGENT scope)
 * 
 * Scope hierarchy: AGENT(0) < USER(1) < TEAM(2) < GLOBAL(3)
 * Standard rule: memory.scope >= target.scope (more specific can see broader)
 * 
 * AGENT scope EXCEPTION: agent_id isolation - AGENT scope returns ONLY
 * memories belonging to the current agent, regardless of hierarchy.
 * This ensures agent memories are completely private.
 * 
 * @param {Array} memories
 * @param {string} scope
 * @returns {Array}
 */
export function filterByScope(memories, scope) {
  const target = normalizeScope(scope);
  const targetLevel = SCOPE_HIERARCHY[target];
  const currentAgentId = AGENT_CONTEXT.current;
  
  // AGENT scope: strict agent_id isolation - only return current agent's memories
  // This is the key difference from other scopes - AGENT memories are completely private
  if (target === 'AGENT') {
    return memories.filter(m => {
      const mScope = normalizeScope(m.scope || 'GLOBAL');
      if (mScope !== 'AGENT') return false;
      // Same agent check
      if (currentAgentId && m.agent_id && m.agent_id !== currentAgentId) {
        return false;
      }
      return true;
    });
  }
  
  // Non-AGENT scopes: standard hierarchy (memory >= target means memory is same-or-broader)
  return memories.filter(m => {
    const mScope = normalizeScope(m.scope || 'GLOBAL');
    const mLevel = SCOPE_HIERARCHY[mScope];
    return mLevel >= targetLevel;
  });
}

/**
 * Check if a memory matches a scope
 * @param {object} memory
 * @param {string} scope
 * @returns {boolean}
 */
export function matchesScope(memory, scope) {
  const target = normalizeScope(scope);
  const mScope = normalizeScope(memory.scope || 'GLOBAL');
  
  // AGENT scope: also check agent_id isolation
  if (mScope === 'AGENT' && target === 'AGENT') {
    const currentAgentId = getCurrentAgentId();
    if (currentAgentId && memory.agent_id && memory.agent_id !== currentAgentId) {
      return false; // different agent, can't see each other's AGENT memories
    }
  }
  
  return SCOPE_HIERARCHY[mScope] >= SCOPE_HIERARCHY[target];
}

// ============ Team Namespace Functions ============

/**
 * Create a new team namespace
 * @param {string} teamId  - Unique team identifier (e.g. 'engineering', 'product-team-a')
 * @param {string} name    - Human-readable team name
 * @returns {{ teamId: string, name: string, created_at: number }}
 */
export function createTeamNamespace(teamId, name = '') {
  const id = teamId.replace(/[^a-zA-Z0-9_-]/g, '_').toLowerCase();
  const now = Date.now();
  teamRegistry.set(id, {
    name: name || id,
    created_at: now,
    memoryCount: 0,
  });
  return { teamId: id, name: name || id, created_at: now };
}

/**
 * Delete a team namespace (archives memories)
 * @param {string} teamId
 * @returns {boolean}
 */
export function deleteTeamNamespace(teamId) {
  return teamRegistry.delete(teamId);
}

/**
 * List all registered teams
 * @returns {Array<{ teamId: string, name: string, created_at: number }>}
 */
export function listTeams() {
  return Array.from(teamRegistry.entries()).map(([id, info]) => ({
    teamId: id,
    name: info.name,
    created_at: info.created_at,
  }));
}

/**
 * Set current team context for memory operations
 * @param {string|null} teamId  - team_id or null to clear
 */
export function setCurrentTeam(teamId) {
  TEAM_CONTEXT.current = teamId || null;
}

/**
 * Get current team context
 * @returns {string|null}
 */
export function getCurrentTeam() {
  return TEAM_CONTEXT.current;
}

/**
 * Switch to a different team context (returns previous)
 * @param {string|null} teamId
 * @returns {string|null} previous team_id
 */
export function switchTeam(teamId) {
  const prev = TEAM_CONTEXT.current;
  TEAM_CONTEXT.current = teamId || null;
  return prev;
}

/**
 * Get the team prefix for memory IDs
 * @param {string|null} teamId
 * @returns {string}
 */
export function getTeamPrefix(teamId) {
  if (!teamId) return '';
  return `team:${teamId}:`;
}

/**
 * Check if a memory belongs to a specific team
 * @param {object} memory
 * @param {string} teamId
 * @returns {boolean}
 */
export function memoryBelongsToTeam(memory, teamId) {
  if (!teamId) return false;
  // TEAM-scope memories store team_id explicitly
  if (memory.team_id && memory.team_id === teamId) return true;
  // Also check id prefix for backward compat
  const prefix = getTeamPrefix(teamId);
  return memory.id && memory.id.startsWith(prefix);
}

/**
 * Filter memories for the current team context + agent context
 * TEAM-scope: only memories belonging to current team
 * USER-scope: personal memories (no team filter)
 * AGENT-scope: only memories belonging to current agent_id
 * GLOBAL-scope: all memories
 * @param {Array} memories
 * @param {string} scope
 * @returns {Array}
 */
export function filterByTeamAndScope(memories, scope = 'TEAM') {
  const teamId = TEAM_CONTEXT.current;
  const agentId = AGENT_CONTEXT.current;

  // GLOBAL: no team/agent filtering needed
  if (scope === 'GLOBAL') {
    return memories;
  }

  return memories.filter(m => {
    const mScope = normalizeScope(m.scope || 'GLOBAL');

    // For TEAM scope: only return memories that belong to current team
    if (mScope === 'TEAM') {
      if (!teamId) return false; // No team context, can't see TEAM memories
      return memoryBelongsToTeam(m, teamId);
    }

    // AGENT scope: strict agent_id isolation - never visible to non-AGENT scopes
    if (mScope === 'AGENT') {
      if (scope === 'AGENT') {
        if (!agentId) return false;
        if (m.agent_id && m.agent_id !== agentId) return false;
        return true;
      }
      return false; // AGENT memories are NEVER visible to USER/TEAM/GLOBAL
    }

    // USER scope: no agent filtering (personal, not tied to specific agent)
    if (mScope === 'USER') {
      return true;
    }

    // Fallback: no filtering
    return true;
  });
}

/**
 * List memories for a specific team (ignores current context)
 * @param {Array} memories
 * @param {string} teamId
 * @returns {Array}
 */
export function listTeamMemories(memories, teamId) {
  if (!teamId) return [];
  return memories.filter(m => memoryBelongsToTeam(m, teamId));
}

/**
 * Get memory namespace key for storage
 * @param {string|null} teamId
 * @returns {string}
 */
export function getMemoryNamespace(teamId) {
  return teamId ? `team:${teamId}` : 'default';
}

/**
 * Tag a memory object with team context before storage
 * @param {object} memory
 * @param {string|null} teamId
 * @returns {object} memory with team_id set
 */
export function tagWithTeam(memory, teamId) {
  if (!teamId) return memory;
  return {
    ...memory,
    team_id: teamId,
    id: (memory.id && !memory.id.startsWith('team:'))
      ? `team:${teamId}:${memory.id}`
      : memory.id,
  };
}

/**
 * Extract team_id from a memory id prefix
 * @param {string} id
 * @returns {string|null}
 */
export function extractTeamFromId(id) {
  const match = id.match(/^team:([^:]+):/);
  return match ? match[1] : null;
}

export default {
  SCOPE_LEVELS,
  SCOPE_HIERARCHY,
  normalizeScope,
  getEffectiveScope,
  filterByScope,
  matchesScope,
  createTeamNamespace,
  deleteTeamNamespace,
  listTeams,
  setCurrentTeam,
  getCurrentTeam,
  switchTeam,
  getTeamPrefix,
  memoryBelongsToTeam,
  filterByTeamAndScope,
  listTeamMemories,
  getMemoryNamespace,
  tagWithTeam,
  extractTeamFromId,
  setCurrentAgentId,
  getCurrentAgentId,
  switchAgentId,
};

// Helper: returns scope order for sorting (lower = more specific)
export function getScopeOrder(scope) {
  return SCOPE_HIERARCHY[normalizeScope(scope)] ?? 999;
}
