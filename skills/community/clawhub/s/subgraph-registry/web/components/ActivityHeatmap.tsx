import { Panel } from "./Panel";

export interface HeatPoint {
  hour: number;
  day_of_week: number;
  count: number;
}

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export function ActivityHeatmap({ data }: { data: HeatPoint[] }) {
  const matrix: number[][] = Array.from({ length: 7 }, () => Array(24).fill(0));
  let max = 1;
  for (const p of data) {
    const d = p.day_of_week ?? 0;
    const h = p.hour ?? 0;
    if (d >= 0 && d < 7 && h >= 0 && h < 24) {
      matrix[d][h] = p.count;
      if (p.count > max) max = p.count;
    }
  }

  return (
    <Panel title="Activity heatmap" caption="hour × day of week (UTC)">
      <div className="w-full">
        {/* Hour ruler */}
        <div className="mb-2 grid items-end gap-[3px] text-[10px] font-medium text-dim"
             style={{ gridTemplateColumns: "36px repeat(24, 1fr)" }}>
          <div />
          {Array.from({ length: 24 }, (_, h) => (
            <div key={h} className="text-center font-mono">
              {h % 3 === 0 ? h.toString().padStart(2, "0") : ""}
            </div>
          ))}
        </div>

        {/* Rows */}
        <div className="space-y-[3px]">
          {DAYS.map((label, dow) => (
            <div
              key={dow}
              className="grid items-center gap-[3px]"
              style={{ gridTemplateColumns: "36px repeat(24, 1fr)" }}
            >
              <div className="pr-1 text-right text-[11px] font-medium text-muted">{label}</div>
              {Array.from({ length: 24 }, (_, h) => {
                const v = matrix[dow][h];
                const t = max > 0 ? v / max : 0;
                const bg =
                  t === 0
                    ? "rgba(111,76,255,0.06)"
                    : `rgba(111,76,255,${(0.18 + t * 0.82).toFixed(3)})`;
                return (
                  <div
                    key={h}
                    title={`${label} ${h.toString().padStart(2, "0")}:00 UTC — ${v} payments`}
                    className="aspect-square rounded-[3px]"
                    style={{ background: bg }}
                  />
                );
              })}
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="mt-3 flex items-center justify-end gap-2 text-[10px] text-dim">
          <span>less</span>
          {[0, 0.25, 0.5, 0.75, 1].map((t, i) => (
            <span
              key={i}
              className="h-3 w-4 rounded-[2px]"
              style={{
                background:
                  t === 0
                    ? "rgba(111,76,255,0.06)"
                    : `rgba(111,76,255,${(0.18 + t * 0.82).toFixed(3)})`,
              }}
            />
          ))}
          <span>more</span>
        </div>
      </div>
    </Panel>
  );
}
