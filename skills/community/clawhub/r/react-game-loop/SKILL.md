---
name: react-hooks-game-loop
description: Create custom React hooks in TypeScript for game loops and animations. Use when the user asks for a React hook, requestAnimationFrame integration, game loop pattern, or delta-time handling. Handles stale-closure safety, unmount cleanup, error resilience, and configurable parameters.
---

# React Game Loop Hooks

Production-ready custom React hooks for game loops and animations using `requestAnimationFrame`.

## Installation

Copy the hook file into your project:

```bash
# From your skill directory
cp <skill-dir>/assets/hooks/useGameLoop.ts src/hooks/
```

> `<skill-dir>` resolves to your OpenClaw skill installation directory.

## Dependencies

- **React** >= 16.8 (hooks support)
- **TypeScript** >= 4.0 (for type safety)
- **react-dom** >= 16.8 (for `requestAnimationFrame` types in browser environment)

This is a browser-only hook — it requires `requestAnimationFrame`, which is not available in Node.js or SSR environments.

## API Reference

### `useGameLoop(options)`

```ts
import { useGameLoop } from './hooks/useGameLoop';
```

**Parameters:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `onFrame` | `(deltaTime: number, elapsedTime: number) => void` | — | Called every frame with delta (ms) and elapsed time (ms). **Required.** |
| `maxDeltaTime` | `number` | `100` | Maximum delta clamp in ms. Prevents huge jumps after tab-switch or lag. |

**Returns:**

| Field | Type | Description |
|-------|------|-------------|
| `start` | `() => void` | Start the game loop |
| `stop` | `() => void` | Stop the game loop |
| `isRunning` | `boolean` | Current loop state |

## Patterns

### Stale-closure safety

Use `useRef` for callbacks/state read inside async/closure contexts (e.g. `requestAnimationFrame`, `setInterval`, event listeners). Always sync ref in `useEffect`.

```ts
const cbRef = useRef(onFrame);
useEffect(() => { cbRef.current = onFrame; }, [onFrame]);
```

### Cleanup on unmount

Always return cleanup from `useEffect`. For RAF/intervals, store handle in ref and cancel on unmount.

```ts
useEffect(() => {
  const id = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(id);
}, []);
```

### Error resilience

Wrap user callbacks in `try/catch` so errors don't break internal loop state.

```ts
try {
  callbackRef.current(delta, elapsed);
} catch (err) {
  console.error('hook callback error:', err);
}
```

### Delta-time clamping

For game loops, clamp `deltaTime` to avoid huge jumps after tab-switch or lag spikes.

```ts
const delta = Math.min(rawDelta, maxDeltaTime);
```

## Example

See `assets/examples/GameTimer.tsx` for a complete usage example showing elapsed time and FPS display.

## Reference

- `assets/hooks/useGameLoop.ts` — requestAnimationFrame-based game loop with start/stop/isRunning controls, deltaTime clamping, and error resilience
- `assets/examples/GameTimer.tsx` — basic usage example