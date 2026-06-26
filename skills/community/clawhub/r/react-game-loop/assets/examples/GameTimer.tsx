import React, { useState, useCallback } from 'react';
import { useGameLoop } from '../hooks/useGameLoop';

export default function GameTimer() {
  const [elapsed, setElapsed] = useState(0);
  const [fps, setFps] = useState(0);

  const onFrame = useCallback((delta: number, total: number) => {
    setElapsed(total);
    setFps(Math.round(1000 / delta));
  }, []);

  const { start, stop, isRunning } = useGameLoop({ onFrame, maxDeltaTime: 100 });

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 24 }}>
      <h1>⏱ Game Timer</h1>
      <p>Elapsed: {(elapsed / 1000).toFixed(2)} s</p>
      <p>FPS: {fps}</p>
      <button onClick={start} disabled={isRunning}>Start</button>
      <button onClick={stop} disabled={!isRunning}>Stop</button>
    </div>
  );
}
