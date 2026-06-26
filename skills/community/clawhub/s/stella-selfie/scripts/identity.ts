import * as fs from "fs";
import * as path from "path";
import * as os from "os";

export interface IdentityConfig {
  avatar: string | null;
  avatarsDir: string | null;
  avatarsURLs: string[];
}

const DEFAULT_WORKSPACE = path.join(os.homedir(), ".openclaw", "workspace");

/**
 * Resolve a path from IDENTITY.md relative to the workspace root.
 * Absolute paths are returned as-is.
 */
function resolvePath(value: string, workspaceRoot: string): string {
  if (path.isAbsolute(value)) {
    return value;
  }
  return path.resolve(workspaceRoot, value);
}

/**
 * Parse a single key: value line from IDENTITY.md.
 * Supports plain `Key: value` as well as Markdown list+bold variants:
 *   - **Key:** value
 *   - **Key**: value
 *   * **Key:** value
 * Returns null if the line doesn't match.
 */
function parseLine(line: string): [string, string] | null {
  const match = line.match(
    /^(?:[-*]\s*)?(?:\*{1,2})?([A-Za-z][A-Za-z0-9_]*)\*{0,2}:\*{0,2}\s*(.+?)\s*(?:#.*)?$/
  );
  if (!match) return null;
  return [match[1], match[2]];
}

/**
 * Read and parse IDENTITY.md from the OpenClaw workspace.
 * Returns resolved absolute paths for Avatar and AvatarsDir.
 */
export function parseIdentity(
  workspaceRoot: string = DEFAULT_WORKSPACE
): IdentityConfig {
  const identityPath = path.join(workspaceRoot, "IDENTITY.md");

  if (!fs.existsSync(identityPath)) {
    throw new Error(`IDENTITY.md not found at: ${identityPath}`);
  }

  const content = fs.readFileSync(identityPath, "utf-8");
  const lines = content.split("\n");

  let avatar: string | null = null;
  let avatarsDir: string | null = null;
  let avatarsURLsRaw: string[] = [];

  for (const line of lines) {
    const parsed = parseLine(line.trim());
    if (!parsed) continue;

    const [key, value] = parsed;

    if (key === "Avatar") {
      avatar = resolvePath(value, workspaceRoot);
    } else if (key === "AvatarsDir") {
      avatarsDir = resolvePath(value, workspaceRoot);
    } else if (key === "AvatarsURLs") {
      avatarsURLsRaw = value
        .split(",")
        .map((u) => u.trim())
        .filter((u) => u.startsWith("http://") || u.startsWith("https://"));
    }
  }

  return { avatar, avatarsDir, avatarsURLs: avatarsURLsRaw };
}
