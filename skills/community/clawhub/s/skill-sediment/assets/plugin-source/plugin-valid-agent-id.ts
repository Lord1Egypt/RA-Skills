/**
 * Shared parsing for `plugins.entries.<pluginId>.config.validAgentId` (string only).
 * Used by workspace extensions that gate behavior by resolved agent id.
 */

/**
 * - absent → null (all agents)
 * - `"*"` → null (all agents)
 * - `""` → [] (no agents)
 * - `"id1,id2"` → trimmed ids
 * - any comma token `*` with others → null (wildcard wins)
 */
export function resolveValidAgentAllowlistFromConfig(
  pluginConfig: Record<string, unknown> | undefined,
): string[] | null {
  const raw = pluginConfig?.validAgentId;
  if (raw === undefined) {
    return null;
  }
  if (typeof raw !== "string") {
    return null;
  }
  const trimmed = raw.trim();
  if (trimmed === "") {
    return [];
  }
  if (trimmed === "*") {
    return null;
  }
  const ids = trimmed
    .split(",")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
  if (ids.length === 0) {
    return [];
  }
  if (ids.some((id) => id === "*")) {
    return null;
  }
  return ids;
}

export function pluginAppliesToAgent(
  agentId: string | undefined,
  allowlist: string[] | null,
): boolean {
  if (allowlist === null) {
    return true;
  }
  if (allowlist.length === 0) {
    return false;
  }
  if (!agentId) {
    return false;
  }
  return allowlist.includes(agentId);
}
