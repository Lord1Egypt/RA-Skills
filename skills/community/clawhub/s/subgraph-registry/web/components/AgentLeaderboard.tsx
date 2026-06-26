import { AgentAvatar } from "./AgentAvatar";
import { Panel } from "./Panel";
import { fmtInt, shortAddr, timeAgo } from "@/lib/format";
import { fixScan8004Url } from "@/lib/scan8004";

export interface AgentRow {
  agent: string;
  wallet: string;
  payments: number;
  last_seen: string;
  registry: string;
  agent_link: string;
}

// Extract plain name from a `[name](url)` markdown wrapper (from Dune)
function extractName(agent: string): { name: string; link: string | null } {
  const m = /^\[([^\]]+)\]\(([^)]+)\)$/.exec(agent);
  if (m) return { name: m[1], link: m[2] };
  return { name: agent, link: null };
}

function platformLabel(registry: string, link: string | null): string {
  if (link && link.includes("8004scan.io")) return "ERC-8004";
  if (registry === "operator") return "operator";
  if (registry === "bazaar") return "bazaar";
  return registry;
}

export function AgentLeaderboard({ rows }: { rows: AgentRow[] }) {
  if (!rows || rows.length === 0) {
    return (
      <Panel title="Identified agents" caption="no matches yet">
        <div className="py-12 text-center text-sm text-dim">
          No agents identified yet. As new x402-capable agents pay The Graph,
          they'll appear here.
        </div>
      </Panel>
    );
  }

  const sorted = [...rows].sort((a, b) => (b.payments ?? 0) - (a.payments ?? 0));

  return (
    <Panel title="Identified agents" caption={`${rows.length} known`}>
      <ul className="max-h-[520px] space-y-1 overflow-y-auto pr-1">
        {sorted.map((r) => {
          const { name, link } = extractName(r.agent);
          const rawUrl = link ?? r.agent_link;
          // Fix the composite-id URL Dune currently emits to 8004scan's
          // real /agents/<chain>/<token> path.
          const url = fixScan8004Url(rawUrl);
          return (
            <li key={r.wallet}>
              {/* Whole row is one clickable anchor — bigger hit-area than text-only */}
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                title={`Open ${name} on 8004scan`}
                className="group flex items-center gap-3 rounded-xl border border-transparent px-2 py-2 transition hover:border-border hover:bg-panelHover"
              >
                <AgentAvatar wallet={r.wallet} />
                <div className="min-w-0 flex-1">
                  <div className="flex items-baseline gap-1.5 truncate text-sm font-medium text-ink group-hover:text-accent">
                    <span className="truncate">{name}</span>
                    <svg
                      aria-hidden
                      viewBox="0 0 12 12"
                      className="h-2.5 w-2.5 shrink-0 opacity-40 transition group-hover:opacity-100"
                    >
                      <path
                        d="M3 9.5 9 3.5M4 3h5v5"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.4"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                  <div className="flex items-center gap-2 text-[11px] text-dim">
                    <span className="font-mono">{shortAddr(r.wallet)}</span>
                    <span>·</span>
                    <span>{platformLabel(r.registry, url)}</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-mono text-sm text-ink">{fmtInt(r.payments)}</div>
                  <div className="text-[11px] text-dim">{timeAgo(r.last_seen)}</div>
                </div>
              </a>
            </li>
          );
        })}
      </ul>
    </Panel>
  );
}
