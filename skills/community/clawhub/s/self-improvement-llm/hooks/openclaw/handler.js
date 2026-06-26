import { n as defaultRuntime } from "../../runtime-CChwgwyg.js";
import { t as createSubsystemLogger } from "../../subsystem-DwIxKdWw.js";
import { x as resolveAgentWorkspaceDir } from "../../agent-scope-Df_s1jDI.js";
import path from "node:path";
import fs from "node:fs";

const log = createSubsystemLogger("hooks/self-improvement");

export default async function selfImprovementHook(ctx) {
  try {
    const config = ctx.config;
    const workspaceDir = resolveAgentWorkspaceDir(config, "main");
    const trailPath = path.join(workspaceDir, "memory", ".learning-trail.json");
    const contextPath = path.join(workspaceDir, "memory", ".hook-context.txt");

    if (!fs.existsSync(trailPath)) return;

    const trail = JSON.parse(fs.readFileSync(trailPath, "utf-8"));
    const now = new Date();
    const lines = [];

    // Pending high-priority items
    const highPriority = (trail.entries || []).filter(
      (e) =>
        (e.priority === "critical" || e.priority === "high") &&
        e.status === "pending"
    );

    // Verifications due
    const dueVerifications = (trail.changes || []).filter(
      (c) => !c.verified && c.next_check && new Date(c.next_check) <= now
    );

    // Check session summary coverage
    const sessionsDir = path.join(workspaceDir, "memory", "sessions");
    const hasRecentSummary = fs.existsSync(sessionsDir) &&
      fs.readdirSync(sessionsDir).some(f => f.endsWith(".md"));

    // Pending patterns (≥2 occurrences)
    const patternGroups = {};
    for (const e of (trail.entries || [])) {
      const pk = e.pattern_key || e.pattern_key;
      if (!pk || e.status === "resolved" || e.status === "promoted") continue;
      if (!patternGroups[pk]) {
        patternGroups[pk] = { count: 0, entries: [], summary: e.summary };
      }
      patternGroups[pk].count += e.recurrence_count || 1;
      patternGroups[pk].entries.push(e);
    }

    const readyPatterns = Object.entries(patternGroups)
      .filter(([, v]) => v.count >= 2)
      .map(([pk, v]) => ({ pk, count: v.count, summary: v.summary }));

    if (highPriority.length > 0) {
      lines.push(`## ⚠️ Pending High-Priority Items (${highPriority.length})`);
      highPriority.forEach((e) =>
        lines.push(`- [${e.id}] ${e.summary}`)
      );
      lines.push("");
    }

    if (dueVerifications.length > 0) {
      lines.push(`## 🔍 Verifications Due (${dueVerifications.length})`);
      dueVerifications.forEach((c) =>
        lines.push(`- [${c.id}] ${c.change?.slice(0, 80)}`)
      );
      lines.push("");
    }

    if (readyPatterns.length > 0) {
      lines.push(`## 🚀 Patterns Ready for Promotion (${readyPatterns.length})`);
      readyPatterns.forEach((p) =>
        lines.push(`- \`${p.pk}\` (${p.count}x): ${p.summary?.slice(0, 80)}`)
      );
      lines.push("");
    }

    if (!hasRecentSummary) {
      lines.push(`## 📝 No Recent Session Summary`);
      lines.push(`- Last auto-summary may be missing. Run: python3 scripts/learn.py --cycle`);
      lines.push("");
    }

    const stats = trail.stats || {};
    lines.push(`## 📊 Stats`);
    lines.push(`- Entries: ${stats.total_entries || 0} | Changes: ${stats.total_changes || 0} | Verified: ${stats.verified_ok || 0}`);
    lines.push(`- Graph nodes: ${stats.total_nodes || 0} | Edges: ${stats.total_edges || 0}`);
    lines.push(`- Last cycle: ${trail.last_cycle || "never"}`);

    // Write context file
    fs.writeFileSync(contextPath, lines.join("\n"), "utf-8");

    if (lines.length > 1 || highPriority.length > 0 || dueVerifications.length > 0) {
      defaultRuntime.log("🧠 self-improvement: hook context written to memory/.hook-context.txt");
    }
  } catch (err) {
    log.warn(`self-improvement hook error: ${err.message}`);
  }
}
