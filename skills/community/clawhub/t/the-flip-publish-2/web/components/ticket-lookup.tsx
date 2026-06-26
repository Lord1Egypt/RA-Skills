"use client";

import { useState, useCallback } from "react";
import { PublicKey } from "@solana/web3.js";
import { useQuery } from "@tanstack/react-query";
import {
  fetchGameFromChain,
  fetchTicketFromChain,
  computeTicketStatus,
  flipToStr,
  type OnChainTicket,
} from "@/lib/solana";
import { PREDICTIONS_SIZE, SURVIVAL_FLIPS } from "@/lib/types";
import { cn } from "@/lib/utils";

export function TicketLookup() {
  const { data: game } = useQuery({
    queryKey: ["gameRaw"],
    queryFn: fetchGameFromChain,
    refetchInterval: 10_000,
    staleTime: 8_000,
  });

  const [walletInput, setWalletInput] = useState("");
  const [roundInput, setRoundInput] = useState("");
  const [ticket, setTicket] = useState<OnChainTicket | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searched, setSearched] = useState(false);

  const lookup = useCallback(async () => {
    const trimmed = walletInput.trim();
    if (!trimmed) return;

    setLoading(true);
    setError(null);
    setTicket(null);
    setSearched(true);

    try {
      const pubkey = new PublicKey(trimmed);
      const round = roundInput.trim()
        ? parseInt(roundInput.trim(), 10)
        : null;

      if (round !== null && !isNaN(round)) {
        const result = await fetchTicketFromChain(pubkey, round);
        setTicket(result);
        if (!result) {
          setError(`No ticket found for round #${round}`);
        }
      } else {
        // Search recent rounds
        const currentRound = game?.currentRound ?? 0;
        let found = false;
        for (let r = currentRound; r >= Math.max(0, currentRound - 50); r--) {
          const result = await fetchTicketFromChain(pubkey, r);
          if (result) {
            setTicket(result);
            found = true;
            break;
          }
        }
        if (!found) {
          setError("No ticket found for this wallet");
        }
      }
    } catch {
      setError("Invalid wallet address");
    } finally {
      setLoading(false);
    }
  }, [walletInput, roundInput, game?.currentRound]);

  const ticketStatus = ticket && game ? computeTicketStatus(game, ticket) : null;

  const statusConfig: Record<string, { label: string; color: string }> = {
    WINNER_COLLECTED: { label: "Winner (Collected)", color: "bg-emerald-500" },
    WINNER: { label: "Winner!", color: "bg-emerald-500" },
    ALL_CORRECT: { label: "All 14 Correct - Claim Now!", color: "bg-emerald-500" },
    WAITING: { label: "Waiting for Round to Flip", color: "bg-amber-500" },
    ELIMINATED: { label: "Eliminated", color: "bg-red-500" },
  };

  return (
    <section className="border-t border-border">
      <div className="max-w-3xl mx-auto px-6 py-12">
        <h2 className="text-sm font-mono text-muted-foreground uppercase tracking-wider mb-6 text-center">
          Lookup Ticket
        </h2>

        <div className="flex flex-col sm:flex-row gap-2 max-w-lg mx-auto">
          <input
            type="text"
            placeholder="Wallet address"
            value={walletInput}
            onChange={(e) => setWalletInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && lookup()}
            className="flex-1 px-4 py-2.5 bg-secondary border border-border rounded-lg text-sm font-mono text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-foreground/30 transition-colors"
          />
          <input
            type="text"
            placeholder="Round # (optional)"
            value={roundInput}
            onChange={(e) => setRoundInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && lookup()}
            className="w-full sm:w-36 px-3 py-2.5 bg-secondary border border-border rounded-lg text-sm font-mono text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-foreground/30 transition-colors"
          />
          <button
            onClick={lookup}
            disabled={loading || !walletInput.trim()}
            className="px-5 py-2.5 bg-foreground text-background font-medium rounded-lg hover:bg-foreground/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm"
          >
            {loading ? "..." : "Lookup"}
          </button>
        </div>

        {error && searched && (
          <p className="text-center text-sm text-muted-foreground mt-4">
            {error}
          </p>
        )}

        {ticket && ticketStatus && (() => {
          const cfg = statusConfig[ticketStatus.status] ?? {
            label: ticketStatus.status,
            color: "bg-muted-foreground",
          };

          return (
            <div className="mt-6 p-4 rounded-lg bg-card border border-border max-w-2xl mx-auto">
              {/* Status header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className={cn("w-2 h-2 rounded-full", cfg.color)} />
                  <span className="text-sm font-medium">{cfg.label}</span>
                </div>
                <span className="text-xs font-mono text-muted-foreground">
                  Round #{ticket.round}
                </span>
              </div>

              {/* Score */}
              {ticketStatus.flipped && (
                <div className="text-center mb-4">
                  <span className="text-3xl font-bold">{ticketStatus.score}</span>
                  <span className="text-muted-foreground">/{SURVIVAL_FLIPS} correct</span>
                </div>
              )}

              {!ticketStatus.flipped && (
                <div className="text-center mb-4">
                  <p className="text-sm text-muted-foreground">
                    Waiting for round #{ticket.round} to be flipped...
                  </p>
                  <p className="text-xs text-muted-foreground/60 mt-1">
                    All 20 coins will flip at once.
                  </p>
                </div>
              )}

              {/* Predictions vs Results — all 20 at once */}
              <div className="space-y-1.5">
                {/* Column numbers */}
                <div className="flex items-center gap-0.5">
                  <span className="w-14 shrink-0" />
                  <div className="flex gap-0.5 flex-1">
                    {ticket.predictions.map((_, i) => (
                      <div
                        key={i}
                        className={cn(
                          "flex-1 text-center text-[8px] font-mono tabular-nums",
                          i < SURVIVAL_FLIPS
                            ? "text-muted-foreground/60"
                            : "text-muted-foreground/30"
                        )}
                      >
                        {i + 1}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Your picks row */}
                <div className="flex items-center gap-0.5">
                  <span className="w-14 text-[10px] font-mono text-muted-foreground uppercase shrink-0">
                    Picks
                  </span>
                  <div className="flex gap-0.5 flex-1">
                    {ticket.predictions.map((p, i) => (
                      <div
                        key={i}
                        className={cn(
                          "flex-1 h-6 rounded-sm flex items-center justify-center text-[10px] font-bold",
                          i < SURVIVAL_FLIPS
                            ? "bg-secondary border border-border"
                            : "bg-secondary/40 border border-border/40 text-muted-foreground/50"
                        )}
                      >
                        {flipToStr(p)}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Results row */}
                <div className="flex items-center gap-0.5">
                  <span className="w-14 text-[10px] font-mono text-muted-foreground uppercase shrink-0">
                    Result
                  </span>
                  <div className="flex gap-0.5 flex-1">
                    {ticket.predictions.map((_, i) => {
                      const comp = ticketStatus.comparisons[i];
                      if (!comp) {
                        return (
                          <div
                            key={i}
                            className="flex-1 h-6 rounded-sm flex items-center justify-center text-[10px] font-bold bg-secondary/50 border border-border text-muted-foreground/40"
                          >
                            ?
                          </div>
                        );
                      }
                      const isSurvival = i < SURVIVAL_FLIPS;
                      return (
                        <div
                          key={i}
                          className={cn(
                            "flex-1 h-6 rounded-sm flex items-center justify-center text-[10px] font-bold",
                            isSurvival && comp.match && "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30",
                            isSurvival && !comp.match && "bg-red-500/20 text-red-400 border border-red-500/30",
                            !isSurvival && comp.match && "bg-emerald-500/10 text-emerald-400/50 border border-emerald-500/15",
                            !isSurvival && !comp.match && "bg-red-500/10 text-red-400/50 border border-red-500/15"
                          )}
                        >
                          {comp.actual}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Survival zone indicator */}
                <div className="flex items-center gap-0.5 mt-1">
                  <span className="w-14 shrink-0" />
                  <div className="flex gap-0.5 flex-1">
                    <div
                      className="flex items-center justify-center text-[8px] font-mono text-muted-foreground/50 border-t border-dashed border-muted-foreground/20 pt-0.5"
                      style={{ flex: SURVIVAL_FLIPS }}
                    >
                      must match (1–{SURVIVAL_FLIPS})
                    </div>
                    <div
                      className="flex items-center justify-center text-[8px] font-mono text-muted-foreground/25 border-t border-dashed border-muted-foreground/10 pt-0.5"
                      style={{ flex: PREDICTIONS_SIZE - SURVIVAL_FLIPS }}
                    >
                      extra
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })()}
      </div>
    </section>
  );
}
