"use client";

import { useEffect, useState, useRef } from "react";
import { useAtomValue } from "jotai";
import { animationsEnabledAtom } from "@/lib/atoms";

interface AnimatedNumberProps {
  value: number;
  decimals?: number;
  duration?: number;
  className?: string;
}

export function AnimatedNumber({
  value,
  decimals = 2,
  duration = 1000,
  className,
}: AnimatedNumberProps) {
  const animationsEnabled = useAtomValue(animationsEnabledAtom);
  const [displayValue, setDisplayValue] = useState(value);
  const previousValue = useRef(value);

  useEffect(() => {
    if (!animationsEnabled) {
      setDisplayValue(value);
      previousValue.current = value;
      return;
    }

    const startValue = previousValue.current;
    const endValue = value;
    const startTime = performance.now();

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Ease out quart for smooth deceleration
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const currentValue = startValue + (endValue - startValue) * easeOutQuart;

      setDisplayValue(currentValue);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
    previousValue.current = value;
  }, [value, duration, animationsEnabled]);

  const formatted = displayValue.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });

  return (
    <span className={className}>
      {formatted.split("").map((char, i) => (
        <span
          key={`${i}-${char}`}
          className={
            char === "," || char === "." ? "text-muted-foreground" : ""
          }
        >
          {char}
        </span>
      ))}
    </span>
  );
}
