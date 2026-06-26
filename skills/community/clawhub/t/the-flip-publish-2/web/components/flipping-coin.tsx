"use client";

import { useEffect, useRef, useState } from "react";
import { useGameState } from "@/lib/hooks/use-game-state";

export function FlippingCoin() {
  const { data } = useGameState();
  const [isFlipping, setIsFlipping] = useState(false);
  const [displayResult, setDisplayResult] = useState<"H" | "T">("H");
  const prevFlipRef = useRef(0);
  const idleTimerRef = useRef<ReturnType<typeof setTimeout>>();

  const currentRound = data?.currentRound ?? 0;

  // When a new round is detected, animate
  useEffect(() => {
    if (currentRound > 0 && currentRound !== prevFlipRef.current) {
      setIsFlipping(true);
      const timeout = setTimeout(() => {
        setDisplayResult(Math.random() > 0.5 ? "T" : "H");
        setIsFlipping(false);
      }, 1000);
      prevFlipRef.current = currentRound;
      return () => clearTimeout(timeout);
    }
    prevFlipRef.current = currentRound;
  }, [currentRound]);

  // Idle: when no flips are happening, do a random decorative flip every 3-6s
  useEffect(() => {
    if (isFlipping) return;

    const scheduleIdle = () => {
      const delay = 3000 + Math.random() * 3000;
      idleTimerRef.current = setTimeout(() => {
        setIsFlipping(true);
        setTimeout(() => {
          setDisplayResult(Math.random() > 0.5 ? "H" : "T");
          setIsFlipping(false);
          scheduleIdle();
        }, 1000);
      }, delay);
    };

    scheduleIdle();
    return () => {
      if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
    };
  }, [isFlipping]);

  return (
    <div className="relative" style={{ perspective: "1000px" }}>
      {/* Glow behind coin */}
      <div className="absolute inset-0 bg-foreground/10 blur-[60px] rounded-full scale-150" />

      {/* The coin */}
      <div
        className="relative w-32 h-32 md:w-40 md:h-40"
        style={{
          transformStyle: "preserve-3d",
          animation: isFlipping
            ? "coinFlip 1s ease-in-out"
            : "coinFloat 4s ease-in-out infinite",
        }}
      >
        {/* Heads side */}
        <div
          className="absolute inset-0 rounded-full border-4 border-foreground/20 bg-gradient-to-br from-foreground/10 to-foreground/5 flex items-center justify-center"
          style={{
            backfaceVisibility: "hidden",
            transform:
              displayResult === "H" ? "rotateY(0deg)" : "rotateY(180deg)",
          }}
        >
          <span className="text-5xl md:text-6xl font-bold text-foreground/80 select-none">
            H
          </span>
        </div>

        {/* Tails side */}
        <div
          className="absolute inset-0 rounded-full border-4 border-foreground/20 bg-gradient-to-br from-foreground/10 to-foreground/5 flex items-center justify-center"
          style={{
            backfaceVisibility: "hidden",
            transform:
              displayResult === "T" ? "rotateY(0deg)" : "rotateY(180deg)",
          }}
        >
          <span className="text-5xl md:text-6xl font-bold text-foreground/80 select-none">
            T
          </span>
        </div>
      </div>

      <style jsx>{`
        @keyframes coinFlip {
          0% {
            transform: rotateY(0deg) rotateX(0deg);
          }
          50% {
            transform: rotateY(900deg) rotateX(20deg) scale(1.1);
          }
          100% {
            transform: rotateY(1800deg) rotateX(0deg);
          }
        }

        @keyframes coinFloat {
          0%,
          100% {
            transform: translateY(0px) rotateY(0deg);
          }
          50% {
            transform: translateY(-10px) rotateY(10deg);
          }
        }
      `}</style>
    </div>
  );
}
