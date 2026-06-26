/**
 * mirror.ts — Shadow trading script for Degen Claw Arena agent
 * Position-first reconciliation: Arena always matches Shekel on every run.
 *
 * Fixes applied (v1.6.0):
 * - Bug 1: Removed hardcoded fallback balances (1057/640) — now exits on failure
 * - Bug 2: Arena balance pulled from perp.accountValue, not spot.balances
 * - Bug 3: Side mismatch detected — close+reopen if Shekel long but Arena short (or vice versa)
 * - Bug 5: Added triggerPx to ShekelOrder interface
 * - Bug 6: Removed unused state (lastTradeId/lastOrderIds) — clean slate
 * - Added: Retry on Shekel API cold-start (1 retry with 5s delay)
 * - Added: Shekel skill version check on startup
 *
 * Usage: npx tsx scripts/mirror.ts
 * Cron:  * /5 * * * * cd ~/dgclaw-skill && npx tsx scripts/mirror.ts >> ~/mirror.log 2>&1
 */

import { execSync } from "child_process";
import * as fs from "fs";
import * as path from "path";
import * as https from "https";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ─── Load .env ────────────────────────────────────────────────────────────────
const envPath = path.join(__dirname, "../.env");
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, "utf8");
  for (const line of envContent.split("\n")) {
    const [key, ...val] = line.split("=");
    if (key && val.length && !process.env[key.trim()]) {
      process.env[key.trim()] = val.join("=").trim();
    }
  }
}

const SHEKEL_KEY = process.env.SHEKEL_API_KEY;
if (!SHEKEL_KEY) {
  console.error("ERROR: SHEKEL_API_KEY not set in .env");
  process.exit(1);
}

const KNOWN_VERSION_FILE = path.join(__dirname, "../.mirror-version");

// ─── Types ────────────────────────────────────────────────────────────────────
interface ShekelPosition {
  coin: string;
  szi: string;        // positive = long, negative = short
  entryPx: string;
  leverage: { value: number };
}

interface ShekelOrder {
  coin: string;
  side: string;
  limitPx: string;
  triggerPx?: string;  // Bug 5 fix: declared
  sz: string;
  oid: number;
  reduceOnly: boolean;
  triggerCondition?: string;
  orderType?: string;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function log(msg: string) {
  console.log(`[${new Date().toISOString()}] ${msg}`);
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Shekel API with 1 retry on failure (handles Render cold-starts)
async function shekelGet(apiPath: string, retry = true): Promise<any> {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: "shekel-skill-backend.onrender.com",
      path: apiPath,
      method: "GET",
      headers: { Authorization: `Bearer ${SHEKEL_KEY}` },
      timeout: 15000,
    };
    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", async () => {
        // Bug 3 fix: treat 5xx as retryable, 4xx as fatal
        const status = res.statusCode || 0;
        if (status >= 500 && retry) {
          log(`API ${status} on ${apiPath} — retrying in 5s`);
          await sleep(5000);
          return resolve(shekelGet(apiPath, false));
        }
        if (status >= 400) {
          return reject(new Error(`API ${status} on ${apiPath}: ${data.slice(0, 100)}`));
        }
        try {
          resolve(JSON.parse(data));
        } catch {
          if (retry) {
            log(`API parse error on ${apiPath} — retrying in 5s`);
            await sleep(5000);
            resolve(shekelGet(apiPath, false));
          } else {
            reject(new Error(`Parse error: ${data.slice(0, 100)}`));
          }
        }
      });
    });
    req.on("error", async (err) => {
      if (retry) {
        log(`API error on ${apiPath} — retrying in 5s: ${err.message}`);
        await sleep(5000);
        resolve(shekelGet(apiPath, false));
      } else {
        reject(err);
      }
    });
    req.on("timeout", () => {
      req.destroy();
      reject(new Error(`Timeout on ${apiPath}`));
    });
    req.end();
  });
}

// ─── Forum config ─────────────────────────────────────────────────────────────
const ARENA_AGENT_ID = process.env.DGCLAW_AGENT_ID;
const SIGNALS_THREAD_ID = process.env.DGCLAW_SIGNALS_THREAD_ID;

if (!ARENA_AGENT_ID || !SIGNALS_THREAD_ID) {
  log("WARNING: DGCLAW_AGENT_ID or DGCLAW_SIGNALS_THREAD_ID not set — forum signal posting disabled.");
  log("Run: ./dgclaw.sh forums to find your agent ID and signals thread ID, then add to .env");
}

function postSignal(title: string, content: string): void {
  if (!ARENA_AGENT_ID || !SIGNALS_THREAD_ID) {
    log(`Signal post skipped (DGCLAW_AGENT_ID/DGCLAW_SIGNALS_THREAD_ID not set): ${title}`);
    return;
  }
  try {
    const cmd = `bash ${__dirname}/../scripts/dgclaw.sh create-post ${ARENA_AGENT_ID} ${SIGNALS_THREAD_ID} "${title.replace(/"/g, "'")}" "${content.replace(/"/g, "'")}"`;
    log(`Posting signal: ${title}`);
    execSync(cmd, { cwd: path.join(__dirname, ".."), encoding: "utf8", timeout: 15000 });
    log(`Signal posted ✅`);
  } catch (e: any) {
    log(`Signal post error (non-fatal): ${e.message?.split("\n")[0]}`);
  }
}

async function fetchLatestReasoning(pair: string, action: string): Promise<string> {
  try {
    // Filter by exact ticker — ensures VVV reasoning only comes from VVV logs
    // action filter further narrows to entry signals (not WAITs)
    const actionFilter = action === "CLOSE" ? "" : `&action=${action}`;
    const logs = await shekelGet(`/agent/llm-logs?ticker=${pair}&executed=true&limit=5${actionFilter}`);
    const recent = (logs.logs || []).find((l: any) =>
      l.ticker?.toUpperCase() === pair.toUpperCase() &&
      l.action?.toUpperCase() !== "WAIT" &&
      l.reasoning
    );
    if (recent?.reasoning) {
      log(`Found reasoning for ${pair} (action: ${recent.action}, executed: ${recent.executed})`);
      return recent.reasoning.slice(0, 1200) + (recent.reasoning.length > 1200 ? "..." : "");
    }
    // Fallback: any recent log for this exact ticker
    const fallback = (logs.logs || []).find((l: any) =>
      l.ticker?.toUpperCase() === pair.toUpperCase() && l.reasoning
    );
    if (fallback?.reasoning) {
      return fallback.reasoning.slice(0, 1200) + (fallback.reasoning.length > 1200 ? "..." : "");
    }
  } catch (e: any) {
    log(`Reasoning fetch error for ${pair}: ${e.message}`);
  }
  return `${action} ${pair} — automated signal from Shekel agent.`;
}

function runTrade(args: string): string {
  const cmd = `npx tsx ${__dirname}/trade.ts ${args}`;
  log(`Executing: ${cmd}`);
  try {
    const out = execSync(cmd, { cwd: path.join(__dirname, ".."), encoding: "utf8" });
    log(`Result: ${out.trim()}`);
    return out;
  } catch (e: any) {
    log(`Error: ${e.message?.split("\n")[0]}`);
    return "";
  }
}

// Returns null for unsupported HIP-3 pairs (xyz:*)
function normalizePair(coin: string): string | null {
  if (!coin) return null;
  if (coin.includes(":")) return null; // HIP-3 — skip silently
  return coin.toUpperCase();
}

function scaleSize(mainNotionalUsd: number, mainBalance: number, arenaBalance: number): number {
  const ratio = arenaBalance / mainBalance;
  const scaled = mainNotionalUsd * ratio;
  return Math.max(10, Math.round(scaled * 100) / 100);
}

// ─── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  log("=== Mirror run started ===");

  // ── Version check (warn if Shekel API spec changed) ─────────────────────
  // Bug 2 fix: compare against stored version, warn if different
  try {
    const versionData = await shekelGet("/skill/version");
    const currentVersion = versionData.version;
    const knownVersion = fs.existsSync(KNOWN_VERSION_FILE)
      ? fs.readFileSync(KNOWN_VERSION_FILE, "utf8").trim() : null;
    if (knownVersion && knownVersion !== currentVersion) {
      log(`⚠️ WARNING: Shekel skill version changed (${knownVersion} → ${currentVersion}). API may have changed — check for mirror issues.`);
    }
    fs.writeFileSync(KNOWN_VERSION_FILE, currentVersion);
    log(`Shekel skill version: ${currentVersion}`);
  } catch { /* non-fatal */ }

  // ── Step 1: Fetch Shekel state ───────────────────────────────────────────
  let mainBalance: number | null = null;
  let mainPositions: ShekelPosition[] = [];
  let mainOrders: ShekelOrder[] = [];

  try {
    const balData = await shekelGet("/account/balances");
    mainBalance = parseFloat(balData.marginSummary?.accountValue);
    if (isNaN(mainBalance)) throw new Error("Invalid balance response");
  } catch (e: any) {
    log(`FATAL: Cannot fetch Shekel balance — ${e.message}. Skipping reconciliation.`);
    return; // Bug 1 fix: exit instead of using wrong fallback
  }

  try {
    const portfolio = await shekelGet("/account/portfolio");
    mainPositions = (portfolio.clearinghouse?.assetPositions || [])
      .map((p: any) => p.position).filter(Boolean);
    log(`Shekel positions: ${mainPositions.length} (${mainPositions.map((p: any) => p.coin).join(", ") || "none"})`);
  } catch (e: any) {
    log(`FATAL: Cannot fetch Shekel portfolio — ${e.message}. Skipping reconciliation.`);
    return;
  }

  try {
    const ordersData = await shekelGet("/account/orders");
    mainOrders = ordersData.orders || [];
    log(`Shekel orders: ${mainOrders.length}`);
  } catch (e: any) { log(`Orders fetch error: ${e.message}`); }

  // ── Step 2: Fetch Arena state ────────────────────────────────────────────
  let arenaBalance: number | null = null;
  let arenaPositions = new Map<string, { side: string; size: number }>();

  try {
    const arenaBalRaw = execSync("npx tsx scripts/trade.ts balance", {
      cwd: path.join(__dirname, ".."), encoding: "utf8"
    });
    const arenaBal = JSON.parse(arenaBalRaw);
    // Unified account: spot USDC is used for perp trading
    // Use perp accountValue if non-zero, else fall back to spot USDC (unified mode)
    const perpVal = parseFloat(arenaBal.perp?.accountValue || "0");
    const spotVal = parseFloat(arenaBal.spot?.balances?.find((b: any) => b.coin === "USDC")?.total || "0");
    arenaBalance = perpVal > 0 ? perpVal : spotVal;
    if (isNaN(arenaBalance)) throw new Error("Invalid arena balance response");
    // Bug 4 fix: zero balance during deposit propagation is normal — warn and skip, don't fatal
    if (arenaBalance <= 0) {
      log(`WARNING: Arena balance is $0 — deposit may still be propagating. Skipping reconciliation this cycle.`);
      return;
    }
    log(`Balances — Main: $${mainBalance.toFixed(2)}, Arena: $${arenaBalance.toFixed(2)}`);
  } catch (e: any) {
    log(`FATAL: Cannot fetch Arena balance — ${e.message}. Skipping reconciliation.`);
    return; // Bug 1 fix: exit instead of using wrong fallback
  }

  try {
    const arenaPosRaw = execSync("npx tsx scripts/trade.ts positions", {
      cwd: path.join(__dirname, ".."), encoding: "utf8"
    });
    if (!arenaPosRaw.includes("No open positions")) {
      const parsed = JSON.parse(arenaPosRaw);
      if (Array.isArray(parsed)) {
        for (const entry of parsed) {
          const pos = entry.position || entry;
          const coin = pos.coin || pos.symbol?.split("/")[0] || "";
          const pair = normalizePair(coin);
          if (pair) {
            const szi = parseFloat(pos.szi || pos.size || "0");
            const side = szi > 0 ? "long" : "short";
            arenaPositions.set(pair, { side, size: Math.abs(szi) });
          }
        }
      }
    }
    log(`Arena positions: ${arenaPositions.size} (${Array.from(arenaPositions.keys()).join(", ") || "none"})`);
  } catch (e: any) { log(`Arena positions error: ${e.message}`); }

  // ── Step 3: Build Shekel position map ────────────────────────────────────
  const mainPairs = new Map<string, { side: string; leverage: number; sizeUsd: number }>();
  for (const pos of mainPositions) {
    const pair = normalizePair(pos.coin);
    if (!pair) continue;
    const szi = parseFloat(pos.szi);
    const side = szi > 0 ? "long" : "short";
    const sizeUsd = Math.abs(szi) * parseFloat(pos.entryPx);
    const leverage = pos.leverage?.value || 3;
    mainPairs.set(pair, { side, leverage, sizeUsd });
  }

  // ── Step 4: Reconcile ────────────────────────────────────────────────────

  // 4a. Close Arena positions Shekel no longer has
  for (const [pair] of arenaPositions) {
    if (!mainPairs.has(pair)) {
      log(`RECONCILE: Shekel closed ${pair} → closing Arena`);
      runTrade(`close --pair ${pair}`);
      const reasoning = await fetchLatestReasoning(pair, "CLOSE");
      const closeDisclaimer = "\n\n---\n*This signal mirrors Shekel Agent trading activity. Arena position sizes may vary.*";
      postSignal(
        `Closed ${pair}`,
        `Position closed. ${reasoning}${closeDisclaimer}`
      );
    }
  }

  // 4b. Open Arena positions Shekel has but Arena doesn't
  //     Also close+reopen if sides differ (Bug 3 fix)
  for (const [pair, mainPos] of mainPairs) {
    const arenaPos = arenaPositions.get(pair);

    const needsOpen = !arenaPos;
    const sideMismatch = arenaPos && arenaPos.side !== mainPos.side; // Bug 3 fix

    if (needsOpen || sideMismatch) {
      if (sideMismatch) {
        log(`RECONCILE: Side mismatch on ${pair} (Shekel: ${mainPos.side}, Arena: ${arenaPos!.side}) → closing and reopening`);
        runTrade(`close --pair ${pair}`);
        // Fix 2: post signal for side mismatch close
        const closeReasoning = await fetchLatestReasoning(pair, "CLOSE");
        const disclaimer = "\n\n---\n*This signal mirrors Shekel Agent trading activity. Arena position sizes may vary.*";
        postSignal(`Closed ${pair} (direction change)`, `Position closed — switching from ${arenaPos!.side} to ${mainPos.side}.\n\n${closeReasoning}${disclaimer}`);
      }

      const arenaSize = scaleSize(mainPos.sizeUsd, mainBalance, arenaBalance);
      const leverage = Math.min(mainPos.leverage, 5);

      // Find SL/TP from Shekel orders (Bug 5 fix: use triggerPx)
      const pairOrders = mainOrders.filter(o => normalizePair(o.coin) === pair && o.reduceOnly);
      let slPrice: string | null = null;
      let tpPrice: string | null = null;
      for (const o of pairOrders) {
        const px = o.triggerPx || o.limitPx;
        if (mainPos.side === "long") {
          if (o.triggerCondition?.includes("below")) slPrice = px;
          if (o.triggerCondition?.includes("above")) tpPrice = px;
        } else {
          if (o.triggerCondition?.includes("above")) slPrice = px;
          if (o.triggerCondition?.includes("below")) tpPrice = px;
        }
      }

      log(`RECONCILE: Opening Arena ${pair} ${mainPos.side} $${arenaSize} ${leverage}x (SL:${slPrice ?? "none"} TP:${tpPrice ?? "none"})`);
      let cmd = `open --pair ${pair} --side ${mainPos.side} --size ${arenaSize} --leverage ${leverage}`;
      if (slPrice) cmd += ` --sl ${slPrice}`;
      if (tpPrice) cmd += ` --tp ${tpPrice}`;
      const result = runTrade(cmd);

      // Post signal to forum if trade succeeded
      if (result && !result.includes("Error")) {
        const direction = mainPos.side === "long" ? "Long" : "Short";
        // Fix 1: use entryPx directly instead of recalculating
        const entryPx = mainPositions.find(p => normalizePair(p.coin) === pair)?.entryPx ?? "?";
        const reasoning = await fetchLatestReasoning(pair, direction.toUpperCase());
        const disclaimer = "\n\n---\n*This signal mirrors Shekel Agent trading activity. Arena position sizes may vary.*";
        postSignal(
          `${direction} ${pair} @ $${entryPx}`,
          `Opened ${direction} ${pair} — SL: ${slPrice ?? "none"} | TP: ${tpPrice ?? "none"} | Lev: ${leverage}x\n\n${reasoning}${disclaimer}`
        );
      }
    }
  }

  log("=== Mirror run complete ===\n");
}

main().catch((e) => log(`Fatal error: ${e.message}`));
