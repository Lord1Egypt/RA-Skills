// Workspace auto-setup.
//
// On first load after install, appends the heartbeat consolidation check
// to the workspace HEARTBEAT.md. Skills are served from the extension dir
// via the manifest's "skills" field. Agents are injected via extraSystemPrompt.
// No workspace file copying needed — everything lives in the extension dir.
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

function resolveOpenclawHome(): string {
  return process.env.OPENCLAW_HOME || path.join(os.homedir(), ".openclaw");
}

/**
 * Strip all existing reflexio heartbeat blocks from content.
 * Splits by double-newline into paragraphs and drops any containing the tool name.
 */
function stripReflexioHeartbeatBlocks(content: string): string {
  const paragraphs = content.split(/\n\n+/);
  const cleaned = paragraphs.filter(
    (p) => !p.includes("reflexio_consolidation_check") && !p.includes("Reflexio Consolidation Check")
  );
  return cleaned.join("\n\n").trim();
}

/**
 * Append HEARTBEAT.md content to the workspace. Idempotent — strips all
 * existing reflexio blocks first, then appends one canonical block.
 *
 * @param pluginDir - The plugin's install directory (import.meta.dirname)
 */
export function setupWorkspaceResources(pluginDir: string): void {
  const workspace = path.join(resolveOpenclawHome(), "workspace");

  const heartbeatSrc = path.join(pluginDir, "HEARTBEAT.md");
  const heartbeatDest = path.join(workspace, "HEARTBEAT.md");
  if (!fs.existsSync(heartbeatSrc)) return;

  const heartbeatContent = fs.readFileSync(heartbeatSrc, "utf8");

  let existing = "";
  try {
    existing = fs.readFileSync(heartbeatDest, "utf8");
  } catch {
    // file doesn't exist yet
  }

  // Always strip existing reflexio blocks (handles duplicates from prior installs),
  // then append one canonical block
  const cleaned = stripReflexioHeartbeatBlocks(existing);
  const final = cleaned + (cleaned ? "\n\n" : "") + heartbeatContent;
  fs.mkdirSync(workspace, { recursive: true });
  fs.writeFileSync(heartbeatDest, final, "utf8");
}
