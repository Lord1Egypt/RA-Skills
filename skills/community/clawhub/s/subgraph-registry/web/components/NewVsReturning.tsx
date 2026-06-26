import { Panel } from "./Panel";

export interface NRPoint {
  week: string;
  new_agents: number;
  returning_agents: number;
}

export function NewVsReturning({ data }: { data: NRPoint[] }) {
  const W = 800;
  const H = 224;
  const PADL = 36;
  const PADR = 12;
  const PADT = 28; // room for legend
  const PADB = 28;
  const innerW = W - PADL - PADR;
  const innerH = H - PADT - PADB;

  if (!data || data.length === 0) {
    return (
      <Panel title="New vs returning agents" caption="weekly">
        <div className="flex h-56 items-center justify-center text-sm text-dim">Building cohort…</div>
      </Panel>
    );
  }

  const series = data;
  const maxY = Math.max(...series.map((d) => d.new_agents + d.returning_agents), 1);
  const bandW = innerW / series.length;
  const barW = Math.max(4, bandW * 0.6);
  const bandX = (i: number) => PADL + i * bandW;
  const yScale = (v: number) => PADT + innerH - (v / maxY) * innerH;

  const yTicks = [0, 0.5, 1].map((t) => ({ v: Math.round(t * maxY), y: yScale(t * maxY) }));

  return (
    <Panel title="New vs returning agents" caption="weekly">
      <svg viewBox={`0 0 ${W} ${H}`} className="block h-56 w-full" role="img" aria-label="New vs returning agents per week">
        {/* legend */}
        <g transform={`translate(${PADL} 12)`}>
          <circle cx={6} cy={4} r={4} fill="#00FFB2" />
          <text x={16} y={8} fill="#8D86B8" fontSize="11">first-time</text>
          <circle cx={96} cy={4} r={4} fill="#6F4CFF" />
          <text x={106} y={8} fill="#8D86B8" fontSize="11">returning</text>
        </g>

        {/* y gridlines */}
        {yTicks.map(({ y, v }, idx) => (
          <g key={idx}>
            <line x1={PADL} x2={W - PADR} y1={y} y2={y} stroke="#2A2451" strokeDasharray="2 4" strokeWidth={1} />
            <text x={PADL - 6} y={y + 4} textAnchor="end" fill="#8D86B8" fontSize="11">{v}</text>
          </g>
        ))}

        {series.map((p, i) => {
          const total = p.new_agents + p.returning_agents;
          const totalH = (total / maxY) * innerH;
          const newH = total > 0 ? (p.new_agents / total) * totalH : 0;
          const returnH = totalH - newH;
          const x = bandX(i) + (bandW - barW) / 2;
          const yTop = PADT + innerH - totalH;
          return (
            <g key={i}>
              <rect x={x} y={yTop} width={barW} height={newH} fill="#00FFB2" rx={1.5}>
                <title>{`${p.week} — first-time: ${p.new_agents}`}</title>
              </rect>
              <rect x={x} y={yTop + newH} width={barW} height={returnH} fill="#6F4CFF" rx={1.5}>
                <title>{`${p.week} — returning: ${p.returning_agents}`}</title>
              </rect>
              <text x={x + barW / 2} y={H - 8} textAnchor="middle" fill="#8D86B8" fontSize="11">
                {p.week.slice(5)}
              </text>
            </g>
          );
        })}
      </svg>
    </Panel>
  );
}
