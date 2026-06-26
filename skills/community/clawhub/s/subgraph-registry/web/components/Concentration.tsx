import { Panel } from "./Panel";
import { fmtInt, fmtPct } from "@/lib/format";

export interface ConcentrationRow {
  bucket: string;
  payers?: number;
  payments?: number;
  share?: number;
}

export function Concentration({ rows }: { rows: ConcentrationRow[] }) {
  if (!rows || rows.length === 0) {
    return (
      <Panel title="Concentration" caption="">
        <div className="py-12 text-center text-sm text-dim">No data.</div>
      </Panel>
    );
  }
  const max = Math.max(...rows.map((r) => Number(r.payments ?? r.share ?? 0)));
  return (
    <Panel title="Payment concentration" caption="who drives the volume">
      <ul className="space-y-2">
        {rows.map((r) => {
          const v = Number(r.payments ?? r.share ?? 0);
          const w = max > 0 ? (v / max) * 100 : 0;
          return (
            <li key={r.bucket} className="grid grid-cols-[110px_1fr_60px] items-center gap-3 text-sm">
              <span className="truncate text-muted">{r.bucket}</span>
              <span className="h-2 overflow-hidden rounded-full bg-border">
                <span
                  className="block h-full rounded-full bg-gradient-to-r from-accent to-success"
                  style={{ width: `${w}%` }}
                />
              </span>
              <span className="text-right font-mono text-xs text-ink">
                {r.share != null ? fmtPct(Number(r.share)) : fmtInt(Number(r.payments ?? 0))}
              </span>
            </li>
          );
        })}
      </ul>
    </Panel>
  );
}
