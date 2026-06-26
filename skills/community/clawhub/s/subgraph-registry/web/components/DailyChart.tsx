import { Panel } from "./Panel";

export interface DailyPoint {
  day: string;
  payments: number;
  ma7?: number;
}

function withMA7(data: DailyPoint[]): DailyPoint[] {
  return data.map((p, i) => {
    const window = data.slice(Math.max(0, i - 6), i + 1);
    const avg = window.reduce((s, x) => s + (x.payments || 0), 0) / window.length;
    return { ...p, ma7: avg };
  });
}

export function DailyChart({ data }: { data: DailyPoint[] }) {
  const W = 800;
  const H = 224;
  const PADL = 36;
  const PADR = 12;
  const PADT = 12;
  const PADB = 24;
  const innerW = W - PADL - PADR;
  const innerH = H - PADT - PADB;

  if (!data || data.length === 0) {
    return (
      <Panel title="Daily payments" caption="bars + 7-day MA">
        <div className="flex h-56 items-center justify-center text-sm text-dim">No data yet.</div>
      </Panel>
    );
  }

  const series = withMA7(data);
  const maxY = Math.max(...series.map((d) => d.payments), 1);

  const bandW = innerW / series.length;
  const barW = Math.max(2, bandW * 0.72);
  const bandX = (i: number) => PADL + i * bandW;
  const yScale = (v: number) => PADT + innerH - (v / maxY) * innerH;

  const maPath = series
    .map((p, i) => `${i === 0 ? "M" : "L"} ${(bandX(i) + bandW / 2).toFixed(1)} ${yScale(p.ma7 || 0).toFixed(1)}`)
    .join(" ");

  const yTicks = [0, 0.5, 1].map((t) => ({ v: Math.round(t * maxY), y: yScale(t * maxY) }));
  const xTickStride = Math.max(1, Math.ceil(series.length / 6));
  const xTicks = series.map((p, i) => ({ p, i })).filter(({ i }) => i % xTickStride === 0 || i === series.length - 1);

  return (
    <Panel title="Daily payments" caption="bars + 7-day MA">
      <svg viewBox={`0 0 ${W} ${H}`} className="block h-56 w-full" role="img" aria-label="Daily payment counts">
        {/* y gridlines */}
        {yTicks.map(({ y, v }, idx) => (
          <g key={idx}>
            <line x1={PADL} x2={W - PADR} y1={y} y2={y} stroke="#2A2451" strokeDasharray="2 4" strokeWidth={1} />
            <text x={PADL - 6} y={y + 4} textAnchor="end" fill="#8D86B8" fontSize="11">
              {v}
            </text>
          </g>
        ))}

        {/* bars */}
        {series.map((p, i) => {
          const barH = (p.payments / maxY) * innerH;
          const isLast = i === series.length - 1;
          return (
            <rect
              key={i}
              x={bandX(i) + (bandW - barW) / 2}
              y={PADT + innerH - barH}
              width={barW}
              height={Math.max(0, barH)}
              fill={isLast ? "#00FFB2" : "#6F4CFF"}
              opacity={0.78}
              rx={1.5}
            >
              <title>{`${p.day} — ${p.payments} payments`}</title>
            </rect>
          );
        })}

        {/* 7d MA line */}
        <path d={maPath} fill="none" stroke="#FFB547" strokeWidth={2} />

        {/* x ticks */}
        {xTicks.map(({ p, i }) => (
          <text
            key={i}
            x={bandX(i) + bandW / 2}
            y={H - 6}
            textAnchor="middle"
            fill="#8D86B8"
            fontSize="11"
          >
            {p.day.slice(5)}
          </text>
        ))}
      </svg>
    </Panel>
  );
}
