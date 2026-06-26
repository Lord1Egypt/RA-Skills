"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import NegotiationMap from "@/components/NegotiationMap";
import { createSession } from "@/lib/api";

interface Point {
  party_a_score: number;
  party_b_score: number;
}

interface RoundPoint extends Point {
  round: number;
  speaker: string;
}

interface SimResult {
  round_data: RoundPoint[];
  trajectory_a_view: RoundPoint[];
  trajectory_b_view: RoundPoint[];
  final_scores: { party_a_score: number; party_b_score: number } | null;
  transcript: Array<{ speaker: string; message: string }>;
}

interface PerspectiveData {
  label: string;
  description: string;
  deal_cloud: Point[];
  frontier: Point[];
  anti_frontier?: Point[];
}

interface DemoData {
  case_title: string;
  party_a_name: string;
  party_b_name: string;
  party_a_batna_score: number;
  party_b_batna_score: number;
  frontier: Point[];
  anti_frontier: Point[];
  deal_cloud: Point[];
  naive: SimResult;
  smart: SimResult;
  both_smart: SimResult;
  party_a_view: PerspectiveData;
  party_b_view: PerspectiveData;
}

type Mode = "naive" | "smart" | "both_smart";

function getNearestFrontierGap(
  trajectory: RoundPoint[],
  frontier: Point[],
  visibleStep: number
): { dealScore: number; frontierScore: number; gap: number } | null {
  const visible = trajectory.slice(0, visibleStep);
  if (visible.length === 0 || frontier.length < 2) return null;

  const last = visible[visible.length - 1];
  const dealScore = last.party_a_score + last.party_b_score;
  const px = last.party_a_score;
  const py = last.party_b_score;

  // Sort frontier by party_a_score for consistent segment traversal
  const sorted = [...frontier].sort(
    (a, b) => a.party_a_score - b.party_a_score
  );

  // Frontier diagonal: first point to last point
  const fStart = sorted[0];
  const fEnd = sorted[sorted.length - 1];
  const fdx = fEnd.party_a_score - fStart.party_a_score;
  const fdy = fEnd.party_b_score - fStart.party_b_score;
  // Orthogonal to frontier diagonal
  const ox = -fdy;
  const oy = fdx;

  let nearest: Point | null = null;
  let bestT = Infinity;

  for (let i = 0; i < sorted.length - 1; i++) {
    const s1 = sorted[i];
    const s2 = sorted[i + 1];
    const sx = s2.party_a_score - s1.party_a_score;
    const sy = s2.party_b_score - s1.party_b_score;
    const denom = ox * sy - oy * sx;
    if (Math.abs(denom) < 1e-10) continue;
    const dpx = s1.party_a_score - px;
    const dpy = s1.party_b_score - py;
    const t = (dpx * sy - dpy * sx) / denom;
    const u = (dpx * oy - dpy * ox) / denom;
    if (u >= -0.01 && u <= 1.01 && t > 0 && t < bestT) {
      bestT = t;
      nearest = {
        party_a_score: Math.round(s1.party_a_score + u * sx),
        party_b_score: Math.round(s1.party_b_score + u * sy),
      };
    }
  }

  // Fallback
  if (!nearest) {
    let minDist = Infinity;
    for (const fp of sorted) {
      const dist = Math.sqrt(
        (px - fp.party_a_score) ** 2 + (py - fp.party_b_score) ** 2
      );
      if (dist < minDist) {
        minDist = dist;
        nearest = fp;
      }
    }
  }

  if (!nearest) return null;
  const frontierScore = nearest.party_a_score + nearest.party_b_score;
  return { dealScore, frontierScore, gap: frontierScore - dealScore };
}

function getJointValue(sim: SimResult): number {
  if (sim.final_scores) {
    return sim.final_scores.party_a_score + sim.final_scores.party_b_score;
  }
  const rd = sim.round_data;
  if (rd.length > 0) {
    return rd[rd.length - 1].party_a_score + rd[rd.length - 1].party_b_score;
  }
  return 0;
}

export default function DemoPage() {
  const router = useRouter();
  const [data, setData] = useState<DemoData | null>(null);
  const [activeMode, setActiveMode] = useState<Mode>("naive");
  const [visibleStep, setVisibleStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showInsight, setShowInsight] = useState(false);
  const [hasCompletedOnce, setHasCompletedOnce] = useState(false);
  const activeLineRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch("/demo-data.json")
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        // Autoplay on load
        setIsPlaying(true);
      });
  }, []);

  // Auto-play animation with loop
  useEffect(() => {
    if (!isPlaying || !data) return;

    const maxSteps = data[activeMode].round_data.length;
    if (visibleStep >= maxSteps) {
      // Animation finished — show insight, then loop
      setShowInsight(true);
      setHasCompletedOnce(true);
      const pause = setTimeout(() => {
        setShowInsight(false);
        setVisibleStep(0);
        // Small delay before restarting
        setTimeout(() => setIsPlaying(true), 500);
      }, 5000);
      setIsPlaying(false);
      return () => clearTimeout(pause);
    }

    const timer = setTimeout(() => {
      setVisibleStep((s) => s + 1);
    }, 2000);

    return () => clearTimeout(timer);
  }, [isPlaying, visibleStep, activeMode, data]);

  // Auto-scroll active transcript line into view
  useEffect(() => {
    activeLineRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
  }, [visibleStep]);

  const handleModeChange = (mode: Mode) => {
    setActiveMode(mode);
    setVisibleStep(0);
    setShowInsight(false);
    setIsPlaying(true);
  };

  const handleStartCoaching = async () => {
    setLoading(true);
    try {
      const sessionId = await createSession();
      router.push(`/chat/${sessionId}`);
    } catch {
      alert("Could not connect to the backend.");
      setLoading(false);
    }
  };

  if (!data) {
    return (
      <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
        <p className="text-zinc-500">Loading demo...</p>
      </div>
    );
  }

  const activeResult = data[activeMode];
  const aName = data.party_a_name.split(" ")[0];
  const bName = data.party_b_name.split(" ")[0];

  // Split transcript by speaker
  const transcriptA = activeResult.transcript
    .map((msg, i) => ({ ...msg, idx: i }))
    .filter((msg) => msg.speaker === data.party_a_name);
  const transcriptB = activeResult.transcript
    .map((msg, i) => ({ ...msg, idx: i }))
    .filter((msg) => msg.speaker === data.party_b_name);

  const jointValues = {
    naive: getJointValue(data.naive),
    smart: getJointValue(data.smart),
    both_smart: getJointValue(data.both_smart),
  };

  const colors: Record<Mode, string> = {
    naive: "#ef4444",
    smart: "#22c55e",
    both_smart: "#3b82f6",
  };

  // The active transcript index is visibleStep - 1 (0-based)
  const activeTranscriptIdx = visibleStep > 0 ? visibleStep - 1 : -1;

  const godGap = getNearestFrontierGap(
    activeResult.round_data,
    data.frontier,
    visibleStep
  );

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* Header */}
      <div className="border-b border-zinc-800 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div>
              <h1 className="text-sm font-semibold">Watch AI Negotiate</h1>
              <p className="text-xs text-zinc-500">{data.case_title}</p>
            </div>
            {visibleStep > 0 && (
              <span className="text-xs text-zinc-500">
                Round {visibleStep} / {activeResult.round_data.length}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            {/* Mode tabs — compact */}
            {(["naive", "smart", "both_smart"] as Mode[]).map((mode) => (
              <button
                key={mode}
                onClick={() => handleModeChange(mode)}
                className={`rounded-full px-3 py-1 text-xs transition-colors ${
                  activeMode === mode
                    ? mode === "naive"
                      ? "bg-red-500/20 text-red-400 border border-red-500/40"
                      : mode === "smart"
                      ? "bg-green-500/20 text-green-400 border border-green-500/40"
                      : "bg-blue-500/20 text-blue-400 border border-blue-500/40"
                    : "text-zinc-500 border border-zinc-800 hover:border-zinc-600"
                }`}
              >
                {mode === "naive"
                  ? "No strategy"
                  : mode === "smart"
                  ? "One side optimized"
                  : "Both optimized"}
              </button>
            ))}
            <button
              onClick={handleStartCoaching}
              disabled={loading}
              className="ml-2 rounded-full bg-white text-black px-4 py-1.5 text-xs font-medium hover:bg-zinc-200 disabled:opacity-50 transition-colors"
            >
              {loading ? "..." : "Try it yourself"}
            </button>
          </div>
        </div>
      </div>

      {/* ═══ 3-COLUMN LAYOUT: Transcript A | Maps | Transcript B ═══ */}
      <div className="grid grid-cols-[1fr_2fr_1fr] h-[calc(100vh-52px)]">
        {/* LEFT RAIL — Party A's narrative */}
        <div className="border-r border-zinc-800 overflow-y-auto p-4">
          <h3 className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-3">
            {data.party_a_name}
          </h3>
          {visibleStep === 0 && (
            <p className="text-xs text-zinc-600 italic">
              Negotiation starting...
            </p>
          )}
          {transcriptA.map((msg) => {
            const isActive = msg.idx === activeTranscriptIdx;
            const isVisible = msg.idx < visibleStep;
            if (!isVisible) return null;
            return (
              <div
                key={msg.idx}
                ref={isActive ? activeLineRef : undefined}
                className={`mb-3 rounded-lg px-3 py-2 transition-all duration-500 ${
                  isActive
                    ? "bg-blue-500/10 border border-blue-500/30"
                    : "border border-transparent"
                }`}
              >
                <div
                  className={`text-xs leading-relaxed whitespace-pre-wrap transition-colors duration-500 ${
                    isActive ? "text-blue-300" : "text-zinc-600"
                  }`}
                >
                  {msg.message}
                </div>
              </div>
            );
          })}
        </div>

        {/* CENTER RAIL — Three maps in triangle hierarchy */}
        <div className="overflow-y-auto p-4">
          {/* Top: Full Picture (god map) — centered */}
          <div className="flex justify-center mb-3">
            <div className="w-full max-w-md rounded-xl border border-amber-500/30 bg-amber-500/5 p-3">
              <NegotiationMap
                dealCloud={data.deal_cloud}
                frontier={data.frontier}
                antiFrontier={data.anti_frontier}
                trajectory={activeResult.round_data}
                color={colors[activeMode]}
                visibleStep={visibleStep}
                aName={aName}
                bName={bName}
                title="Full Picture"
                subtitle="True deal space — both sides visible"
                compact
                batnaA={data.party_a_batna_score}
                batnaB={data.party_b_batna_score}
              />
              {godGap && (
                <div className="mt-1 text-xs text-zinc-500 flex justify-between">
                  <span>
                    Deal:{" "}
                    <span className="text-zinc-300">{godGap.dealScore}</span>
                  </span>
                  <span>
                    Frontier:{" "}
                    <span className="text-amber-400">
                      {godGap.frontierScore}
                    </span>
                  </span>
                  {godGap.gap > 0 && (
                    <span className="text-red-400">
                      -{godGap.gap} left
                    </span>
                  )}
                  {godGap.gap <= 0 && (
                    <span className="text-green-400">On frontier</span>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Bottom: Party A (left) + Party B (right) */}
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/30 p-3">
              <NegotiationMap
                dealCloud={data.party_a_view.deal_cloud}
                frontier={data.party_a_view.frontier}
                antiFrontier={data.party_a_view.anti_frontier}
                trajectory={activeResult.trajectory_a_view}
                color={colors[activeMode]}
                visibleStep={visibleStep}
                aName={aName}
                bName={bName}
                title={aName}
                subtitle="Guesses their priorities"
                compact
                batnaA={data.party_a_batna_score}
              />
              {(() => {
                const gap = getNearestFrontierGap(
                  activeResult.trajectory_a_view,
                  data.party_a_view.frontier,
                  visibleStep
                );
                if (!gap) return null;
                return (
                  <div className="mt-1 text-xs text-zinc-500 flex justify-between">
                    <span>{gap.dealScore}</span>
                    <span className="text-amber-400">{gap.frontierScore}</span>
                    {gap.gap > 0 && (
                      <span className="text-red-400">-{gap.gap}</span>
                    )}
                  </div>
                );
              })()}
            </div>

            <div className="rounded-xl border border-zinc-800 bg-zinc-900/30 p-3">
              <NegotiationMap
                dealCloud={data.party_b_view.deal_cloud}
                frontier={data.party_b_view.frontier}
                antiFrontier={data.party_b_view.anti_frontier}
                trajectory={activeResult.trajectory_b_view}
                color={colors[activeMode]}
                visibleStep={visibleStep}
                aName={aName}
                bName={bName}
                title={bName}
                subtitle="Guesses their priorities"
                compact
                batnaB={data.party_b_batna_score}
              />
              {(() => {
                const gap = getNearestFrontierGap(
                  activeResult.trajectory_b_view,
                  data.party_b_view.frontier,
                  visibleStep
                );
                if (!gap) return null;
                return (
                  <div className="mt-1 text-xs text-zinc-500 flex justify-between">
                    <span>{gap.dealScore}</span>
                    <span className="text-amber-400">{gap.frontierScore}</span>
                    {gap.gap > 0 && (
                      <span className="text-red-400">-{gap.gap}</span>
                    )}
                  </div>
                );
              })()}
            </div>
          </div>

          {/* Value insight — appears when animation completes */}
          {showInsight && godGap && godGap.gap > 0 && (
            <div className="text-center mt-6 pb-2 animate-fade-in">
              <div className="inline-flex items-center gap-6 rounded-xl border border-amber-500/30 bg-amber-500/5 px-6 py-4">
                <div>
                  <div className="text-2xl font-bold text-zinc-300">{godGap.dealScore}</div>
                  <div className="text-xs text-zinc-500">Deal value</div>
                </div>
                <div className="text-amber-400 text-lg font-mono">→</div>
                <div>
                  <div className="text-2xl font-bold text-amber-400">{godGap.frontierScore}</div>
                  <div className="text-xs text-zinc-500">Optimal deal</div>
                </div>
                <div className="border-l border-zinc-700 pl-6">
                  <div className="text-2xl font-bold text-red-400">{godGap.gap}</div>
                  <div className="text-xs text-zinc-500">Points left on table</div>
                </div>
              </div>
            </div>
          )}

          {/* CTA — fades in after first loop completes */}
          {hasCompletedOnce && (
            <div className="text-center mt-4 pb-4 animate-fade-in">
              <p className="text-zinc-500 text-xs mb-3">
                The gap between the deal and the frontier is value both sides missed.
              </p>
              <button
                onClick={handleStartCoaching}
                disabled={loading}
                className="rounded-full bg-white text-black px-6 py-2 text-sm font-semibold hover:bg-zinc-200 disabled:opacity-50 transition-colors"
              >
                {loading ? "Starting..." : "Try it yourself →"}
              </button>
            </div>
          )}
        </div>

        {/* RIGHT RAIL — Party B's narrative */}
        <div className="border-l border-zinc-800 overflow-y-auto p-4">
          <h3 className="text-xs font-semibold text-zinc-400 uppercase tracking-wider mb-3">
            {data.party_b_name}
          </h3>
          {visibleStep === 0 && (
            <p className="text-xs text-zinc-600 italic">
              Negotiation starting...
            </p>
          )}
          {transcriptB.map((msg) => {
            const isActive = msg.idx === activeTranscriptIdx;
            const isVisible = msg.idx < visibleStep;
            if (!isVisible) return null;
            return (
              <div
                key={msg.idx}
                ref={isActive ? activeLineRef : undefined}
                className={`mb-3 rounded-lg px-3 py-2 transition-all duration-500 ${
                  isActive
                    ? "bg-blue-500/10 border border-blue-500/30"
                    : "border border-transparent"
                }`}
              >
                <div
                  className={`text-xs leading-relaxed whitespace-pre-wrap transition-colors duration-500 ${
                    isActive ? "text-blue-300" : "text-zinc-600"
                  }`}
                >
                  {msg.message}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
