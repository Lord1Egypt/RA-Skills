/**
 * useGameLoop — Browser game loop via requestAnimationFrame
 */
import { useCallback, useEffect, useRef, useState } from 'react';

export interface UseGameLoopOptions {
  /** Called on every frame with (deltaTime, elapsedTime) in ms */
  onFrame: (deltaTime: number, elapsedTime: number) => void;
  /** Max delta clamp in ms (default 100) */
  maxDeltaTime?: number;
}

export interface UseGameLoopReturn {
  start: () => void;
  stop: () => void;
  isRunning: boolean;
}

export function useGameLoop({ onFrame, maxDeltaTime = 100 }: UseGameLoopOptions): UseGameLoopReturn {
  const [isRunning, setIsRunning] = useState(false);

  // Stale-closure-safe refs
  const callbackRef = useRef(onFrame);
  useEffect(() => { callbackRef.current = onFrame; }, [onFrame]);

  const isRunningRef = useRef(isRunning);
  useEffect(() => { isRunningRef.current = isRunning; }, [isRunning]);

  const rafRef = useRef<number | null>(null);
  const lastTimestampRef = useRef<number | null>(null);
  const elapsedTimeRef = useRef(0);

  const tick = useCallback((timestamp: number) => {
    if (!isRunningRef.current) return;

    if (lastTimestampRef.current !== null) {
      let delta = timestamp - lastTimestampRef.current;
      if (delta > maxDeltaTime) delta = maxDeltaTime;
      elapsedTimeRef.current += delta;
      try {
        callbackRef.current(delta, elapsedTimeRef.current);
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error('useGameLoop callback error:', err);
      }
    }

    lastTimestampRef.current = timestamp;
    rafRef.current = requestAnimationFrame(tick);
  }, [maxDeltaTime]);

  const start = useCallback(() => {
    if (isRunningRef.current) return;
    setIsRunning(true);
    lastTimestampRef.current = null; // skip stale timestamp
    rafRef.current = requestAnimationFrame(tick);
  }, [tick]);

  const stop = useCallback(() => {
    if (!isRunningRef.current) return;
    setIsRunning(false);
    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (rafRef.current !== null) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
      }
    };
  }, []);

  return { start, stop, isRunning };
}
