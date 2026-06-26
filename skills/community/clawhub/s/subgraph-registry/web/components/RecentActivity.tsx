import { AgentAvatar } from "./AgentAvatar";
import { Panel } from "./Panel";
import { fmtUSD, shortAddr, timeAgo } from "@/lib/format";
import { fixScan8004Url } from "@/lib/scan8004";

export interface PaymentRow {
  wallet: string;
  amount_usdc: number;
  block_time: string;
  tx_hash: string;
  agent_name?: string | null;
}

export function RecentActivity({
  rows,
  identityByWallet,
}: {
  rows: PaymentRow[];
  identityByWallet: Map<string, { name: string; link: string }>;
}) {
  if (!rows || rows.length === 0) {
    return (
      <Panel title="Recent activity" caption="waiting…">
        <div className="py-12 text-center text-sm text-dim">No payments yet.</div>
      </Panel>
    );
  }
  return (
    <Panel title="Recent activity" caption={`${rows.length} latest`}>
      <ul className="max-h-[520px] space-y-1 overflow-y-auto pr-1">
        {rows.map((r, idx) => {
          const id = identityByWallet.get(r.wallet?.toLowerCase?.() ?? "");
          const fresh = Date.now() - Date.parse(r.block_time) < 60_000;
          return (
            <li
              key={`${r.tx_hash}-${idx}`}
              className={`group flex items-center gap-3 rounded-lg px-2 py-1.5 text-sm transition hover:bg-panelHover ${
                fresh ? "animate-row_in" : ""
              }`}
            >
              <span className="w-16 shrink-0 font-mono text-[11px] text-dim">
                {timeAgo(r.block_time)}
              </span>
              <AgentAvatar wallet={r.wallet} size={20} />
              <div className="min-w-0 flex-1 truncate">
                {id ? (
                  <a
                    href={fixScan8004Url(id.link)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-ink hover:text-accent"
                  >
                    {id.name}
                  </a>
                ) : (
                  <span className="font-mono text-muted">{shortAddr(r.wallet)}</span>
                )}
              </div>
              <a
                href={`https://basescan.org/tx/${r.tx_hash}`}
                target="_blank"
                rel="noopener noreferrer"
                className="font-mono text-sm tabular-nums text-success hover:text-ink"
                title={r.tx_hash}
              >
                {fmtUSD(r.amount_usdc, { precise: true })}
              </a>
            </li>
          );
        })}
      </ul>
    </Panel>
  );
}
