"use client";

import { useState } from "react";

interface Point {
  party_a_score: number;
  party_b_score: number;
  terms?: Record<string, string>;
}

interface RoundPoint extends Point {
  round: number;
  speaker: string;
}

interface NegotiationMapProps {
  dealCloud: Point[];
  frontier: Point[];
  antiFrontier?: Point[];
  trajectory: RoundPoint[];
  color: string;
  visibleStep: number;
  aName: string;
  bName: string;
  title?: string;
  subtitle?: string;
  compact?: boolean;
  batnaA?: number;
  batnaB?: number;
}

export default function NegotiationMap({
  dealCloud,
  frontier,
  antiFrontier,
  trajectory,
  color,
  visibleStep,
  aName,
  bName,
  title,
  subtitle,
  compact = false,
  batnaA,
  batnaB,
}: NegotiationMapProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  const W = compact ? 360 : 500;
  const H = compact ? 280 : 400;
  const PAD = compact ? 40 : 50;

  // Score ranges from deal cloud
  const allA = dealCloud.map((d) => d.party_a_score);
  const allB = dealCloud.map((d) => d.party_b_score);
  const minA = Math.min(...allA);
  const maxA = Math.max(...allA);
  const minB = Math.min(...allB);
  const maxB = Math.max(...allB);

  const scaleX = (v: number) =>
    PAD + ((v - minA) / (maxA - minA || 1)) * (W - 2 * PAD);
  const scaleY = (v: number) =>
    H - PAD - ((v - minB) / (maxB - minB || 1)) * (H - 2 * PAD);

  // Sort frontiers for line drawing
  const sortedFrontier = [...frontier].sort(
    (a, b) => a.party_a_score - b.party_a_score
  );
  const sortedAntiFrontier = antiFrontier
    ? [...antiFrontier].sort((a, b) => a.party_a_score - b.party_a_score)
    : null;

  const visibleTrajectory = trajectory.slice(0, visibleStep);

  // Compute nearest frontier point to the final visible deal
  const lastPoint = visibleTrajectory.length > 0
    ? visibleTrajectory[visibleTrajectory.length - 1]
    : null;

  let nearestFrontier: Point | null = null;
  let nearestFrontierTerms: Record<string, string> | null = null;
  let frontierGap = 0;
  if (lastPoint && sortedFrontier.length >= 2) {
    // Orthogonal projection method:
    // 1. Frontier diagonal = line from first frontier point to last
    // 2. Orthogonal to that diagonal
    // 3. Place orthogonal through the last offer point
    // 4. Extend to intersect the frontier polyline
    // 5. Intersection = the deal that proportionally splits the value-add
    const fStart = sortedFrontier[0];
    const fEnd = sortedFrontier[sortedFrontier.length - 1];
    // Frontier diagonal direction
    const fdx = fEnd.party_a_score - fStart.party_a_score;
    const fdy = fEnd.party_b_score - fStart.party_b_score;
    // Orthogonal direction (perpendicular to frontier diagonal)
    // Rotate 90°: (fdx, fdy) → (-fdy, fdx)
    const ox = -fdy;
    const oy = fdx;

    // Ray from deal point along orthogonal: P(t) = deal + t * (ox, oy)
    // Find intersection with each frontier segment
    const px = lastPoint.party_a_score;
    const py = lastPoint.party_b_score;

    let bestT = Infinity;
    for (let i = 0; i < sortedFrontier.length - 1; i++) {
      const s1 = sortedFrontier[i];
      const s2 = sortedFrontier[i + 1];
      // Segment direction
      const sx = s2.party_a_score - s1.party_a_score;
      const sy = s2.party_b_score - s1.party_b_score;
      // Solve: deal + t*(ox,oy) = s1 + u*(sx,sy)
      // ox*t - sx*u = s1.x - px
      // oy*t - sy*u = s1.y - py
      const denom = ox * sy - oy * sx;
      if (Math.abs(denom) < 1e-10) continue;
      const dpx = s1.party_a_score - px;
      const dpy = s1.party_b_score - py;
      const t = (dpx * sy - dpy * sx) / denom;
      const u = (dpx * oy - dpy * ox) / denom;
      // Valid if u in [0,1] (on segment) and t > 0 (toward frontier)
      if (u >= -0.01 && u <= 1.01 && t > 0 && t < bestT) {
        bestT = t;
        nearestFrontier = {
          party_a_score: Math.round(s1.party_a_score + u * sx),
          party_b_score: Math.round(s1.party_b_score + u * sy),
        };
        // Pick terms from the closer segment endpoint
        nearestFrontierTerms = (u <= 0.5 ? s1.terms : s2.terms) || null;
      }
    }

    // Fallback: if no intersection found (deal is beyond frontier),
    // find the closest frontier point by Euclidean distance
    if (!nearestFrontier) {
      let minDist = Infinity;
      for (const fp of sortedFrontier) {
        const dist = Math.sqrt(
          (px - fp.party_a_score) ** 2 + (py - fp.party_b_score) ** 2
        );
        if (dist < minDist) {
          minDist = dist;
          nearestFrontier = fp;
          nearestFrontierTerms = fp.terms || null;
        }
      }
    }

    if (nearestFrontier) {
      const lastJoint = lastPoint.party_a_score + lastPoint.party_b_score;
      const frontierJoint =
        nearestFrontier.party_a_score + nearestFrontier.party_b_score;
      frontierGap = frontierJoint - lastJoint;
    }
  }

  const dotR = compact ? 4 : 5;
  const activeDotR = compact ? 5.5 : 7;
  const fontSize = compact ? 8 : 9;
  const axisFont = compact ? 10 : 12;
  const frontierFont = compact ? 8 : 10;

  return (
    <div className="relative">
      {title && (
        <div className="mb-2">
          <h4 className="text-sm font-semibold text-zinc-100">{title}</h4>
          {subtitle && (
            <p className="text-xs text-zinc-500">{subtitle}</p>
          )}
        </div>
      )}
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="w-full"
        style={{ background: "transparent" }}
      >
        {/* Deal space — filled region between upper and lower frontiers */}
        {sortedFrontier.length > 1 && sortedAntiFrontier && sortedAntiFrontier.length > 1 ? (
          <polygon
            points={[
              ...sortedFrontier.map(
                (p) => `${scaleX(p.party_a_score)},${scaleY(p.party_b_score)}`
              ),
              ...[...sortedAntiFrontier].reverse().map(
                (p) => `${scaleX(p.party_a_score)},${scaleY(p.party_b_score)}`
              ),
            ].join(" ")}
            fill="#3f3f46"
            opacity={0.15}
          />
        ) : (
          /* Fallback: scattered dots if no anti-frontier data */
          dealCloud.map((d, i) => (
            <circle
              key={`cloud-${i}`}
              cx={scaleX(d.party_a_score)}
              cy={scaleY(d.party_b_score)}
              r={compact ? 1 : 1.5}
              fill="#3f3f46"
              opacity={0.3}
            />
          ))
        )}

        {/* BATNA zones — grey out non-viable regions */}
        {batnaA !== undefined && (
          <rect
            x={PAD}
            y={PAD}
            width={Math.max(0, scaleX(batnaA) - PAD)}
            height={H - 2 * PAD}
            fill="#18181b"
            opacity={0.7}
          />
        )}
        {batnaB !== undefined && (
          <rect
            x={PAD}
            y={scaleY(batnaB)}
            width={W - 2 * PAD}
            height={Math.max(0, H - PAD - scaleY(batnaB))}
            fill="#18181b"
            opacity={0.7}
          />
        )}
        {/* BATNA threshold lines */}
        {batnaA !== undefined && (
          <>
            <line
              x1={scaleX(batnaA)}
              y1={PAD}
              x2={scaleX(batnaA)}
              y2={H - PAD}
              stroke="#ef4444"
              strokeWidth={1}
              strokeDasharray="4,3"
              opacity={0.6}
            />
            {!compact && (
              <text
                x={scaleX(batnaA) + 4}
                y={PAD + 12}
                fill="#ef4444"
                fontSize={8}
                opacity={0.8}
              >
                {aName} walkaway
              </text>
            )}
          </>
        )}
        {batnaB !== undefined && (
          <>
            <line
              x1={PAD}
              y1={scaleY(batnaB)}
              x2={W - PAD}
              y2={scaleY(batnaB)}
              stroke="#ef4444"
              strokeWidth={1}
              strokeDasharray="4,3"
              opacity={0.6}
            />
            {!compact && (
              <text
                x={W - PAD - 4}
                y={scaleY(batnaB) - 4}
                fill="#ef4444"
                fontSize={8}
                opacity={0.8}
                textAnchor="end"
              >
                {bName} walkaway
              </text>
            )}
          </>
        )}

        {/* Lower frontier line */}
        {sortedAntiFrontier && sortedAntiFrontier.length > 1 && (
          <polyline
            points={sortedAntiFrontier
              .map(
                (p) =>
                  `${scaleX(p.party_a_score)},${scaleY(p.party_b_score)}`
              )
              .join(" ")}
            fill="none"
            stroke="#52525b"
            strokeWidth={compact ? 1 : 1.5}
            strokeDasharray="4,4"
            opacity={0.4}
          />
        )}

        {/* Pareto frontier line */}
        {sortedFrontier.length > 1 && (
          <>
            <polyline
              points={sortedFrontier
                .map(
                  (p) =>
                    `${scaleX(p.party_a_score)},${scaleY(p.party_b_score)}`
                )
                .join(" ")}
              fill="none"
              stroke="#fbbf24"
              strokeWidth={compact ? 1.5 : 2}
              strokeDasharray="6,3"
            />
            {!compact && (
              <text
                x={
                  scaleX(
                    sortedFrontier[sortedFrontier.length - 1]?.party_a_score ||
                      0
                  ) + 5
                }
                y={
                  scaleY(
                    sortedFrontier[sortedFrontier.length - 1]?.party_b_score ||
                      0
                  ) - 8
                }
                fill="#fbbf24"
                fontSize={frontierFont}
                fontWeight="bold"
              >
                Optimal frontier
              </text>
            )}
          </>
        )}

        {/* Trajectory path */}
        {visibleTrajectory.length > 1 && (
          <polyline
            points={visibleTrajectory
              .map(
                (p) =>
                  `${scaleX(p.party_a_score)},${scaleY(p.party_b_score)}`
              )
              .join(" ")}
            fill="none"
            stroke={color}
            strokeWidth={compact ? 1.5 : 2}
            opacity={0.6}
          />
        )}

        {/* Trajectory dots */}
        {visibleTrajectory.map((p, i) => {
          const isLast = i === visibleTrajectory.length - 1;
          return (
            <g key={`traj-${i}`}>
              <circle
                cx={scaleX(p.party_a_score)}
                cy={scaleY(p.party_b_score)}
                r={isLast ? activeDotR : dotR}
                fill={color}
                opacity={isLast ? 1 : 0.6}
                stroke={isLast ? "white" : "none"}
                strokeWidth={compact ? 1.5 : 2}
              />
              {!compact && (
                <text
                  x={scaleX(p.party_a_score) + 10}
                  y={scaleY(p.party_b_score) + 4}
                  fill="#a1a1aa"
                  fontSize={fontSize}
                >
                  R{p.round}
                </text>
              )}
            </g>
          );
        })}

        {/* Frontier gap: ghost dot + dashed line + score labels */}
        {lastPoint && nearestFrontier && frontierGap > 2 && (
          <>
            {/* Dashed line from final deal to nearest frontier point */}
            <line
              x1={scaleX(lastPoint.party_a_score)}
              y1={scaleY(lastPoint.party_b_score)}
              x2={scaleX(nearestFrontier.party_a_score)}
              y2={scaleY(nearestFrontier.party_b_score)}
              stroke="#fbbf24"
              strokeWidth={1}
              strokeDasharray="3,3"
              opacity={0.5}
            />
            {/* Ghost dot on frontier — hover for terms */}
            <circle
              cx={scaleX(nearestFrontier.party_a_score)}
              cy={scaleY(nearestFrontier.party_b_score)}
              r={compact ? 4 : 6}
              fill="none"
              stroke="#fbbf24"
              strokeWidth={1.5}
              strokeDasharray="3,2"
              opacity={0.8}
            />
            {/* Invisible larger hit area for hover */}
            <circle
              cx={scaleX(nearestFrontier.party_a_score)}
              cy={scaleY(nearestFrontier.party_b_score)}
              r={compact ? 12 : 16}
              fill="transparent"
              style={{ cursor: "pointer" }}
              onMouseEnter={() => setShowTooltip(true)}
              onMouseLeave={() => setShowTooltip(false)}
            />
            {/* Tooltip with deal terms */}
            {showTooltip && nearestFrontierTerms && (
              <foreignObject
                x={scaleX(nearestFrontier.party_a_score) - 90}
                y={scaleY(nearestFrontier.party_b_score) - (compact ? 90 : 110)}
                width={180}
                height={compact ? 80 : 100}
              >
                <div
                  style={{
                    background: "#18181b",
                    border: "1px solid #fbbf24",
                    borderRadius: 8,
                    padding: compact ? "6px 8px" : "8px 10px",
                    fontSize: compact ? 7 : 9,
                    color: "#fafafa",
                    lineHeight: 1.5,
                    pointerEvents: "none",
                  }}
                >
                  <div style={{ fontWeight: 600, color: "#fbbf24", marginBottom: 2, fontSize: compact ? 8 : 10 }}>
                    Best deal
                  </div>
                  {Object.entries(nearestFrontierTerms).map(([k, v]) => (
                    <div key={k} style={{ display: "flex", justifyContent: "space-between", gap: 4 }}>
                      <span style={{ color: "#a1a1aa" }}>{k}</span>
                      <span style={{ fontWeight: 500 }}>{v}</span>
                    </div>
                  ))}
                </div>
              </foreignObject>
            )}
            {/* Score label on the final deal */}
            <text
              x={scaleX(lastPoint.party_a_score) + (compact ? -2 : 12)}
              y={scaleY(lastPoint.party_b_score) + (compact ? -8 : -10)}
              fill="#a1a1aa"
              fontSize={compact ? 7 : 9}
              textAnchor={compact ? "middle" : "start"}
            >
              {lastPoint.party_a_score + lastPoint.party_b_score} pts
            </text>
            {/* Score label on the frontier point */}
            <text
              x={scaleX(nearestFrontier.party_a_score) + (compact ? -2 : 12)}
              y={scaleY(nearestFrontier.party_b_score) + (compact ? -8 : -10)}
              fill="#fbbf24"
              fontSize={compact ? 7 : 9}
              textAnchor={compact ? "middle" : "start"}
            >
              {nearestFrontier.party_a_score + nearestFrontier.party_b_score} pts
            </text>
            {/* Gap label at midpoint */}
            {!compact && (
              <text
                x={(scaleX(lastPoint.party_a_score) + scaleX(nearestFrontier.party_a_score)) / 2 + 8}
                y={(scaleY(lastPoint.party_b_score) + scaleY(nearestFrontier.party_b_score)) / 2}
                fill="#fbbf24"
                fontSize={8}
                opacity={0.7}
              >
                +{frontierGap} left on table
              </text>
            )}
          </>
        )}

        {/* Axes */}
        <line
          x1={PAD}
          y1={H - PAD}
          x2={W - PAD}
          y2={H - PAD}
          stroke="#52525b"
          strokeWidth={1}
        />
        <line
          x1={PAD}
          y1={PAD}
          x2={PAD}
          y2={H - PAD}
          stroke="#52525b"
          strokeWidth={1}
        />
        <text
          x={W / 2}
          y={H - (compact ? 6 : 10)}
          fill="#71717a"
          fontSize={axisFont}
          textAnchor="middle"
        >
          {aName} value
        </text>
        <text
          x={compact ? 10 : 15}
          y={H / 2}
          fill="#71717a"
          fontSize={axisFont}
          textAnchor="middle"
          transform={`rotate(-90, ${compact ? 10 : 15}, ${H / 2})`}
        >
          {bName} value
        </text>
      </svg>
    </div>
  );
}
