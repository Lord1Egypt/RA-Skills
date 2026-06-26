declare const require: any;

const { execFileSync } = require("child_process");
const { appendFileSync, mkdirSync } = require("fs");
const path = require("path");
const processRef = require("process");

type RewriteResult = {
  rewritten: string | null;
  action: string;
};

function tryRewrite(cmd: string): RewriteResult {
  if (!cmd.trim()) return { rewritten: null, action: "skip:empty" };
  try {
    const output = execFileSync("rtk", ["rewrite", cmd], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
    const rewritten = output.trim();
    if (!rewritten) return { rewritten: null, action: "skip:no_match" };
    return { rewritten, action: "rewrite" };
  } catch (error: any) {
    if (error?.status === 1)
      return { rewritten: null, action: "skip:no_match" };
    if (error?.code === "ENOENT")
      return { rewritten: null, action: "skip:no_rtk" };
    return { rewritten: null, action: "skip:rewrite_error" };
  }
}

function getAuditPath(pluginConfig: any): string | null {
  if (pluginConfig.audit !== true) return null;
  const configuredDir =
    typeof pluginConfig.auditDir === "string"
      ? pluginConfig.auditDir.trim()
      : "";
  const envDir = processRef?.env?.RTK_AUDIT_DIR || "";
  const home = processRef?.env?.HOME || "/tmp";
  const auditDir =
    configuredDir || envDir || path.join(home, ".local", "share", "rtk");
  return path.join(auditDir, "hook-audit.log");
}

function isoTimestamp(): string {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function appendAudit(
  auditPath: string | null,
  action: string,
  original: string,
  rewritten: string = "-",
): void {
  if (!auditPath) return;
  try {
    mkdirSync(path.dirname(auditPath), { recursive: true });
    appendFileSync(
      auditPath,
      `${isoTimestamp()} | ${action} | ${original} | ${rewritten}\n`,
      "utf8",
    );
  } catch {}
}

export default function register(api: any) {
  const pluginConfig = api.config ?? {};
  const enabled = pluginConfig.enabled !== false;
  const verbose = pluginConfig.verbose === true;
  const auditPath = getAuditPath(pluginConfig);

  if (!enabled) return;

  api.on(
    "before_tool_call",
    (event: { toolName: string; params: Record<string, unknown> }) => {
      if (event.toolName !== "exec") return;

      const command = event.params?.command;
      if (typeof command !== "string") {
        appendAudit(auditPath, "skip:non_string", "-");
        return;
      }

      const result = tryRewrite(command);
      if (!result.rewritten) {
        appendAudit(auditPath, result.action, command);
        return;
      }

      const rewritten = result.rewritten;
      appendAudit(auditPath, "rewrite", command, rewritten);

      if (verbose) {
        console.log(`[rtk-rewrite] ${command} → ${rewritten}`);
      }

      return { params: { ...event.params, command: rewritten } };
    },
    { priority: 10 },
  );

  if (verbose) {
    console.log("[rtk-rewrite] Registered (delegating to `rtk rewrite`)");
    if (auditPath) {
      console.log(`[rtk-rewrite] Audit enabled: ${auditPath}`);
    }
  }
}

export { tryRewrite };
