/**
 * download-ux.ts — Wrapper for heavy first-call downloads (rc.16, fixes #92).
 *
 * Wraps a download promise with:
 *   - per-attempt timeout (default 600s, override via TOTALRECLAW_ONNX_INSTALL_TIMEOUT in seconds)
 *   - 60s keep-alive log so slow-bandwidth users don't think it's frozen
 *   - 3-attempt exponential-backoff retry (per-attempt timeout grows 1x/2x/4x)
 *   - loud actionable error after exhaustion
 *
 * No third-party imports here — pure stdlib so the unit test can exercise it
 * without pulling the heavy `@huggingface/transformers` chain.
 */

const DEFAULT_DOWNLOAD_TIMEOUT_MS = 600_000;
const KEEPALIVE_INTERVAL_MS = 60_000;
const MAX_DOWNLOAD_ATTEMPTS = 3;

export function getDownloadTimeoutMs(): number {
  const raw = process.env.TOTALRECLAW_ONNX_INSTALL_TIMEOUT;
  if (!raw) return DEFAULT_DOWNLOAD_TIMEOUT_MS;
  const parsed = Number(raw);
  if (!Number.isFinite(parsed) || parsed <= 0) return DEFAULT_DOWNLOAD_TIMEOUT_MS;
  // Spec accepts seconds; convert to ms.
  return Math.floor(parsed * 1000);
}

export interface DownloadWithUXOpts {
  /** Override the per-attempt base timeout in ms (env var takes precedence by default). */
  timeoutMs?: number;
  /** Override the keep-alive cadence in ms. */
  keepaliveMs?: number;
  /** Override the max attempts. */
  maxAttempts?: number;
  /** Logger override (defaults to console.error). */
  log?: (msg: string) => void;
  /** Sleep override for tests; defaults to setTimeout. */
  sleep?: (ms: number) => Promise<void>;
}

export async function downloadWithUX<T>(
  label: string,
  download: () => Promise<T>,
  opts?: DownloadWithUXOpts,
): Promise<T> {
  const baseTimeoutMs = opts?.timeoutMs ?? getDownloadTimeoutMs();
  const keepaliveMs = opts?.keepaliveMs ?? KEEPALIVE_INTERVAL_MS;
  const maxAttempts = opts?.maxAttempts ?? MAX_DOWNLOAD_ATTEMPTS;
  const log = opts?.log ?? ((msg: string) => console.error(msg));
  const sleep = opts?.sleep ?? ((ms: number) => new Promise(r => setTimeout(r, ms)));

  let lastErr: unknown = null;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const attemptTimeoutMs = baseTimeoutMs * Math.pow(2, attempt - 1);
    const startedAt = Date.now();
    const keepaliveTimer = setInterval(() => {
      const elapsedSec = Math.floor((Date.now() - startedAt) / 1000);
      log(`[TotalReclaw] ${label}: still downloading… (${elapsedSec}s elapsed, attempt ${attempt}/${maxAttempts})`);
    }, keepaliveMs);

    try {
      const result = await Promise.race([
        download(),
        new Promise<never>((_, reject) =>
          setTimeout(
            () => reject(new Error(`Download timeout after ${Math.floor(attemptTimeoutMs / 1000)}s (attempt ${attempt}/${maxAttempts})`)),
            attemptTimeoutMs,
          ),
        ),
      ]);
      clearInterval(keepaliveTimer);
      return result;
    } catch (err) {
      clearInterval(keepaliveTimer);
      lastErr = err;
      const msg = err instanceof Error ? err.message : String(err);
      if (attempt < maxAttempts) {
        const backoffMs = Math.min(5_000 * Math.pow(2, attempt - 1), 30_000);
        log(`[TotalReclaw] ${label}: attempt ${attempt} failed (${msg}). Retrying in ${Math.floor(backoffMs / 1000)}s…`);
        await sleep(backoffMs);
      }
    }
  }

  const finalMsg = lastErr instanceof Error ? lastErr.message : String(lastErr);
  throw new Error(
    `[TotalReclaw] Embedding model download failed after ${maxAttempts} attempts (last error: ${finalMsg}). ` +
      `Check your network connection and retry: \`openclaw plugins install totalreclaw\`. ` +
      `On slow connections, set TOTALRECLAW_ONNX_INSTALL_TIMEOUT=1200 (in seconds) to extend the per-attempt timeout.`,
  );
}
