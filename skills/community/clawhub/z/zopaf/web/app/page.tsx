"use client";

import { useEffect, useState } from "react";
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

  const sorted = [...frontier].sort(
    (a, b) => a.party_a_score - b.party_a_score
  );

  const fStart = sorted[0];
  const fEnd = sorted[sorted.length - 1];
  const fdx = fEnd.party_a_score - fStart.party_a_score;
  const fdy = fEnd.party_b_score - fStart.party_b_score;
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

/** Truncate a transcript message to ~2 lines */
function truncateMessage(msg: string, maxLen = 120): string {
  const clean = msg.replace(/\*\*/g, "").replace(/\n/g, " ").trim();
  if (clean.length <= maxLen) return clean;
  return clean.slice(0, maxLen).trimEnd() + "...";
}

export default function Home() {
  const router = useRouter();
  const [data, setData] = useState<DemoData | null>(null);
  const [activeMode, setActiveMode] = useState<Mode>("naive");
  const [visibleStep, setVisibleStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showInsight, setShowInsight] = useState(false);

  useEffect(() => {
    fetch("/demo-data.json")
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        setIsPlaying(true);
      });
  }, []);

  // Auto-play with loop
  useEffect(() => {
    if (!isPlaying || !data) return;

    const maxSteps = data[activeMode].round_data.length;
    if (visibleStep >= maxSteps) {
      setShowInsight(true);
      const pause = setTimeout(() => {
        setShowInsight(false);
        setVisibleStep(0);
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
      alert("Could not connect to the backend. Please try again.");
      setLoading(false);
    }
  };

  if (!data) {
    return (
      <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
        <p className="text-zinc-500">Loading...</p>
      </div>
    );
  }

  const activeResult = data[activeMode];
  const aName = data.party_a_name.split(" ")[0];
  const bName = data.party_b_name.split(" ")[0];

  const colors: Record<Mode, string> = {
    naive: "#ef4444",
    smart: "#22c55e",
    both_smart: "#3b82f6",
  };

  // Current round's transcript — only the latest message from each side
  const activeTranscriptIdx = visibleStep > 0 ? visibleStep - 1 : -1;
  const currentMsg = activeTranscriptIdx >= 0
    ? activeResult.transcript[activeTranscriptIdx]
    : null;

  const godGap = getNearestFrontierGap(
    activeResult.round_data,
    data.frontier,
    visibleStep
  );

  return (
    <div className="min-h-screen bg-white text-[#1B3A5C]">
      {/* ════════════════════════════════════════════════════════
          HERO — Light, approachable
          ════════════════════════════════════════════════════════ */}
      <div className="px-6 pt-8 pb-6">
        {/* Top bar */}
        <div className="max-w-5xl mx-auto flex items-center justify-between mb-12">
          <span className="text-lg font-bold tracking-tight text-[#1B3A5C]">
            Negotiation Map
          </span>
          <button
            onClick={handleStartCoaching}
            disabled={loading}
            className="rounded-full bg-[#D94B3E] text-white px-5 py-2 text-sm font-medium hover:bg-[#c43a2e] disabled:opacity-50 transition-colors"
          >
            {loading ? "Starting..." : "Try it yourself"}
          </button>
        </div>

        {/* Headline */}
        <div className="max-w-3xl mx-auto text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-tight text-[#1B3A5C]">
            Every negotiation leaves<br />value on the table.
          </h1>
          <p className="text-2xl md:text-3xl font-bold text-[#2D6EB5] mt-2">
            We find it.
          </p>
        </div>

        {/* Demo bridge */}
        <div className="max-w-3xl mx-auto text-center mb-4">
          <p className="text-xs text-[#7a8ea3] uppercase tracking-widest mb-3">
            See what better strategy looks like
          </p>
        </div>
        <div className="flex justify-center gap-2 mb-6">
          {(["naive", "smart", "both_smart"] as Mode[]).map((mode) => (
            <button
              key={mode}
              onClick={() => handleModeChange(mode)}
              className={`rounded-full px-4 py-1.5 text-xs font-medium transition-colors ${
                activeMode === mode
                  ? mode === "naive"
                    ? "bg-red-50 text-[#D94B3E] border border-red-200"
                    : mode === "smart"
                    ? "bg-green-50 text-green-700 border border-green-200"
                    : "bg-blue-50 text-[#2D6EB5] border border-blue-200"
                  : "text-[#7a8ea3] border border-gray-200 hover:border-gray-400"
              }`}
            >
              {mode === "naive"
                ? "No strategy"
                : mode === "smart"
                ? "One side optimized"
                : "Both optimized"}
            </button>
          ))}
        </div>

        {/* ── Compact demo: transcripts flanking the god map ── */}
        <div className="max-w-5xl mx-auto">
          {/* Current dialogue */}
          <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-start mb-4">
            <div className="text-right">
              <div className="text-xs font-semibold text-[#7a8ea3] uppercase tracking-wider mb-1">
                {aName}
              </div>
              <div
                className={`text-xs leading-relaxed transition-all duration-500 ${
                  currentMsg && currentMsg.speaker === data.party_a_name
                    ? "text-[#2D6EB5]"
                    : "text-gray-400"
                }`}
              >
                {currentMsg && currentMsg.speaker === data.party_a_name
                  ? truncateMessage(currentMsg.message)
                  : visibleStep === 0
                  ? ""
                  : (() => {
                      for (let i = activeTranscriptIdx; i >= 0; i--) {
                        if (activeResult.transcript[i].speaker === data.party_a_name) {
                          return truncateMessage(activeResult.transcript[i].message);
                        }
                      }
                      return "";
                    })()}
              </div>
            </div>

            <div className="flex flex-col items-center">
              {visibleStep > 0 && (
                <span className="text-xs text-gray-400 font-mono">
                  R{Math.ceil(visibleStep / 2)}/{Math.ceil(activeResult.round_data.length / 2)}
                </span>
              )}
            </div>

            <div>
              <div className="text-xs font-semibold text-[#7a8ea3] uppercase tracking-wider mb-1">
                {bName}
              </div>
              <div
                className={`text-xs leading-relaxed transition-all duration-500 ${
                  currentMsg && currentMsg.speaker === data.party_b_name
                    ? "text-[#2D6EB5]"
                    : "text-gray-400"
                }`}
              >
                {currentMsg && currentMsg.speaker === data.party_b_name
                  ? truncateMessage(currentMsg.message)
                  : visibleStep === 0
                  ? ""
                  : (() => {
                      for (let i = activeTranscriptIdx; i >= 0; i--) {
                        if (activeResult.transcript[i].speaker === data.party_b_name) {
                          return truncateMessage(activeResult.transcript[i].message);
                        }
                      }
                      return "";
                    })()}
              </div>
            </div>
          </div>

          {/* Three maps inline — dark containers for contrast */}
          <div className="grid grid-cols-3 gap-3">
            <div className="rounded-xl border border-gray-200 bg-[#1a1a2e] p-2">
              <NegotiationMap
                dealCloud={data.party_a_view.deal_cloud}
                frontier={data.party_a_view.frontier}
                antiFrontier={data.party_a_view.anti_frontier}
                trajectory={activeResult.trajectory_a_view}
                color={colors[activeMode]}
                visibleStep={visibleStep}
                aName={aName}
                bName={bName}
                title={`${aName}'s view`}
                compact
                batnaA={data.party_a_batna_score}
              />
            </div>

            <div className="rounded-xl border-2 border-[#F5A623]/40 bg-[#1a1a2e] p-2">
              <NegotiationMap
                dealCloud={data.deal_cloud}
                frontier={data.frontier}
                antiFrontier={data.anti_frontier}
                trajectory={activeResult.round_data}
                color={colors[activeMode]}
                visibleStep={visibleStep}
                aName={aName}
                bName={bName}
                title="Global View"
                subtitle="Both sides visible"
                compact
                batnaA={data.party_a_batna_score}
                batnaB={data.party_b_batna_score}
              />
            </div>

            <div className="rounded-xl border border-gray-200 bg-[#1a1a2e] p-2">
              <NegotiationMap
                dealCloud={data.party_b_view.deal_cloud}
                frontier={data.party_b_view.frontier}
                antiFrontier={data.party_b_view.anti_frontier}
                trajectory={activeResult.trajectory_b_view}
                color={colors[activeMode]}
                visibleStep={visibleStep}
                aName={aName}
                bName={bName}
                title={`${bName}'s view`}
                compact
                batnaB={data.party_b_batna_score}
              />
            </div>
          </div>

          {/* Value insight */}
          <div className="h-20 flex items-center justify-center">
            {showInsight && godGap && godGap.gap > 0 ? (
              <div className="animate-fade-in inline-flex items-center gap-6 rounded-xl border border-[#F5A623]/30 bg-[#FFF8ED] px-6 py-3">
                <div className="text-center">
                  <div className="text-xl font-bold text-[#1B3A5C]">{godGap.dealScore}</div>
                  <div className="text-[10px] text-[#7a8ea3]">Deal value</div>
                </div>
                <div className="text-[#F5A623] font-mono">&rarr;</div>
                <div className="text-center">
                  <div className="text-xl font-bold text-[#F5A623]">{godGap.frontierScore}</div>
                  <div className="text-[10px] text-[#7a8ea3]">Optimal deal</div>
                </div>
                <div className="border-l border-gray-200 pl-6 text-center">
                  <div className="text-xl font-bold text-[#D94B3E]">{godGap.gap}</div>
                  <div className="text-[10px] text-[#7a8ea3]">Left on table</div>
                </div>
              </div>
            ) : godGap && visibleStep > 0 ? (
              <div className="text-xs text-[#7a8ea3]">
                Deal: {godGap.dealScore} &middot; Frontier: {godGap.frontierScore}
                {godGap.gap > 0 && <span className="text-[#D94B3E] ml-2">-{godGap.gap} left</span>}
              </div>
            ) : null}
          </div>
        </div>
      </div>

      {/* ════════════════════════════════════════════════════════
          BELOW THE FOLD — light sections
          ════════════════════════════════════════════════════════ */}

      {/* What the product actually does */}
      <div className="border-t border-gray-100 bg-gray-50">
        <div className="max-w-3xl mx-auto px-6 py-20 text-center">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-[#1B3A5C] mb-4">
            Negotiation, modeled
          </h2>
          <p className="text-[#7a8ea3] text-sm uppercase tracking-widest mb-8">
            Don&apos;t head into your next negotiation flying blind
          </p>
          <p className="text-lg text-[#4a6277] leading-relaxed max-w-xl mx-auto">
            We build a mathematical model of your specific deal — mapping
            the full outcome space, identifying efficient trades, and generating
            counteroffers that move toward the optimal frontier.
          </p>
        </div>
      </div>

      {/* How it works — three steps */}
      <div className="border-t border-gray-100">
        <div className="max-w-4xl mx-auto px-6 py-20">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            <div>
              <div className="text-3xl font-bold text-gray-200 mb-2">1</div>
              <h3 className="text-[#1B3A5C] font-semibold mb-2">Map the deal</h3>
              <p className="text-[#4a6277] text-sm leading-relaxed">
                We identify all negotiable terms and build the full deal space.
                Every possible combination, scored for both sides.
              </p>
            </div>
            <div>
              <div className="text-3xl font-bold text-gray-200 mb-2">2</div>
              <h3 className="text-[#1B3A5C] font-semibold mb-2">Learn priorities</h3>
              <p className="text-[#4a6277] text-sm leading-relaxed">
                Using statistical models, we uncover what you actually value — and
                infer the other side&apos;s priorities from their counteroffers.
              </p>
            </div>
            <div>
              <div className="text-3xl font-bold text-gray-200 mb-2">3</div>
              <h3 className="text-[#1B3A5C] font-semibold mb-2">Generate better offers</h3>
              <p className="text-[#4a6277] text-sm leading-relaxed">
                Optimization models generate counteroffers that create value for
                both sides — moving toward the frontier where no better deal exists.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Two modes */}
      <div className="border-t border-gray-100 bg-gray-50">
        <div className="max-w-4xl mx-auto px-6 py-20 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
            <h3 className="text-xl font-semibold text-[#1B3A5C] mb-3">
              Practice mode
            </h3>
            <p className="text-[#4a6277] text-sm leading-relaxed">
              Prepare for your upcoming negotiation by sparring with an AI
              that plays the other side. It pushes back, makes counteroffers,
              and tests your strategy — then tells you exactly where you left
              money on the table.
            </p>
          </div>
          <div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
            <h3 className="text-xl font-semibold text-[#1B3A5C] mb-3">
              Live coaching
            </h3>
            <p className="text-[#4a6277] text-sm leading-relaxed">
              In an active negotiation? Share what&apos;s happening and get
              instant guidance: what to counter with, which terms to trade,
              and when to walk away.
            </p>
          </div>
        </div>
      </div>

      {/* Bottom CTA */}
      <div className="border-t border-gray-100">
        <div className="max-w-2xl mx-auto text-center px-6 py-20">
          <h2 className="text-3xl font-bold text-[#1B3A5C] mb-3">
            Run your negotiation through the engine
          </h2>
          <p className="text-[#7a8ea3] text-sm mb-8">
            Built on negotiation frameworks from Harvard Business School.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={handleStartCoaching}
              disabled={loading}
              className="rounded-full bg-[#D94B3E] text-white px-8 py-4 text-lg font-medium hover:bg-[#c43a2e] disabled:opacity-50 transition-colors"
            >
              {loading ? "Starting..." : "Start coaching session"}
            </button>
            <a
              href="/demo"
              className="rounded-full border border-gray-300 text-[#1B3A5C] px-8 py-4 text-lg font-medium hover:bg-gray-50 transition-colors text-center"
            >
              Watch full simulation
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
