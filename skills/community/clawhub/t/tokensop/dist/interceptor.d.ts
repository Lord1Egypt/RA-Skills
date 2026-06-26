/**
 * Interceptor — the main hook that fires on every intent.
 *
 * Flow:
 * 1. User issues an intent (e.g., "login to GitHub")
 * 2. Query local store first (skip LLM, save tokens)
 * 3. If local miss → query ClawMind Cloud
 * 4. If cloud hit → execute the Lobster workflow directly
 * 5. If cloud miss → passthrough to normal OpenClaw flow
 * 6. On success → save to local store + contribute to cloud
 * 7. On failure → report failure for circuit breaker tracking
 */
import type { OpenClawContext } from "./types.js";
export declare function interceptIntent(ctx: OpenClawContext): Promise<void>;
/**
 * Hook: called when a session completes successfully.
 * Compiles the session trace into a Lobster workflow and:
 * 1. Saves to local store (for faster retrieval next time)
 * 2. Contributes to cloud (for sharing with other nodes)
 */
export declare function onSessionComplete(ctx: OpenClawContext): Promise<void>;
