import { Panel } from "./Panel";
import { fmtUSD } from "@/lib/format";

export interface CumulativePoint {
  day: string;
  cumulative_usdc: number;
  cumulative_payments?: number;
}

// Pure SVG, server-rendered — no client hydration dependency.
export function CumulativeChart({ data }: { data: CumulativePoint[] }) {
  const W = 800;
  const H = 224;
  const PADL = 44;
  const PADR = 12;
  const PADT = 12;
  const PADB = 24;
  const innerW = W - PADL - PADR;
  const innerH = H - PADT - PADB;

  if (!data || data.length === 0) {
    return (
      <Panel title="Cumulative USDC paid" caption="—">
        <div className="flex h-56 items-center justify-center text-sm text-dim">
          No data yet.
        </div>
      </Panel>
    );
  }

  const maxY = Math.max(...data.map((d) => d.cumulative_usdc), 0.0001);
  const xScale = (i: number) =>
    PADL + (data.length <= 1 ? innerW / 2 : (i / (data.length - 1)) * innerW);
  const yScale = (v: number) => PADT + innerH - (v / maxY) * innerH;

  // Line + closed area paths
  const linePath = data.map((p, i) => `${i === 0 ? "M" : "L"} ${xScale(i).toFixed(1)} ${yScale(p.cumulative_usdc).toFixed(1)}`).join(" ");
  const areaPath =
    `${linePath} L ${xScale(data.length - 1).toFixed(1)} ${(PADT + innerH).toFixed(1)} L ${xScale(0).toFixed(1)} ${(PADT + innerH).toFixed(1)} Z`;

  // Tick targets: ~4 y ticks at 25/50/75/100% and ~6 x ticks
  const yTicks = [0, 0.25, 0.5, 0.75, 1].map((t) => ({ v: t * maxY, y: yScale(t * maxY) }));
  const xTickStride = Math.max(1, Math.ceil(data.length / 6));
  const xTicks = data
    .map((p, i) => ({ p, i }))
    .filter(({ i }) => i % xTickStride === 0 || i === data.length - 1);

  return (
    <Panel title="Cumulative USDC paid" caption={`${data.length} days`}>
      <svg viewBox={`0 0 ${W} ${H}`} className="block h-56 w-full" role="img" aria-label="Cumulative USDC paid over time">
        <defs>
          <linearGradient id="gradUSDC" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6F4CFF" stopOpacity={0.6} />
            <stop offset="100%" stopColor="#6F4CFF" stopOpacity={0.02} />
          </linearGradient>
        </defs>

        {/* y gridlines */}
        {yTicks.map(({ y, v }, idx) => (
          <g key={idx}>
            <line x1={PADL} x2={W - PADR} y1={y} y2={y} stroke="#2A2451" strokeDasharray="2 4" strokeWidth={1} />
            <text x={PADL - 6} y={y + 4} textAnchor="end" fill="#8D86B8" fontSize="11">
              {v >= 1000 ? `$${(v / 1000).toFixed(0)}k` : v < 1 ? `$${v.toFixed(2)}` : `$${v.toFixed(0)}`}
            </text>
          </g>
        ))}

        {/* x ticks */}
        {xTicks.map(({ p, i }) => (
          <text key={i} x={xScale(i)} y={H - 6} textAnchor="middle" fill="#8D86B8" fontSize="11">
            {p.day.slice(5)}
          </text>
        ))}

        {/* Area fill */}
        <path d={areaPath} fill="url(#gradUSDC)" />
        {/* Line */}
        <path d={linePath} fill="none" stroke="#6F4CFF" strokeWidth={2} />

        {/* Final-point marker */}
        {data.length > 0 && (
          <>
            <circle
              cx={xScale(data.length - 1)}
              cy={yScale(data[data.length - 1].cumulative_usdc)}
              r={4}
              fill="#00FFB2"
            />
            <text
              x={xScale(data.length - 1) - 8}
              y={yScale(data[data.length - 1].cumulative_usdc) - 10}
              textAnchor="end"
              fill="#00FFB2"
              fontSize="11"
              fontWeight={600}
            >
              {fmtUSD(data[data.length - 1].cumulative_usdc, { precise: true })}
            </text>
          </>
        )}
      </svg>
    </Panel>
  );
}
