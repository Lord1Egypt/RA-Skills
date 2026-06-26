"use client";

import { useGameState } from "@/lib/hooks/use-game-state";

const CONTRACT_URL =
  "https://explorer.solana.com/address/7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX?cluster=devnet";

export function Footer() {
  const { data } = useGameState();
  const currentRound = data?.currentRound ?? 0;

  return (
    <footer className="border-t border-border">
      <div className="max-w-3xl mx-auto px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="font-bold tracking-tight">THE FLIP</span>
          <span className="text-[10px] text-muted-foreground font-mono uppercase tracking-wider">
            Round #{currentRound} &middot; Solana Devnet
          </span>
        </div>

        <a
          href={CONTRACT_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-muted-foreground hover:text-foreground transition-colors font-mono"
        >
          View Contract
        </a>
      </div>
    </footer>
  );
}
