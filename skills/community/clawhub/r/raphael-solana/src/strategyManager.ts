import fs from "fs";
import path from "path";
import os from "os";
import type {
  StrategyStatus,
  PolymarketWeatherConfig,
  PolymarketWeatherReading,
  XConfig,
  XStrategyConfig,
} from "./types.ts";
import { runPolymarketWeatherArbTick } from "./polymarketWeatherArb.ts";
import { createXStrategy } from "./xStrategy.ts";

const RAPHAEL_DATA_DIR =
  process.env["RAPHAEL_DATA_DIR"] ?? path.join(os.homedir(), ".raphael");

try { fs.mkdirSync(RAPHAEL_DATA_DIR, { recursive: true }); } catch {}

export const STATUS_FILE = path.join(RAPHAEL_DATA_DIR, "scanner-status.json");
export const PID_FILE    = path.join(RAPHAEL_DATA_DIR, "weather-arb.pid");

// ── Helpers ───────────────────────────────────────────────────────────────────

const atomicWriteJSON = (filePath: string, data: unknown): void => {
  const tmp = filePath + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2));
  fs.renameSync(tmp, filePath);
};

const isPidAlive = (pid: number): boolean => {
  try { process.kill(pid, 0); return true; } catch { return false; }
};

const isDaemonRunning = (): boolean => {
  try {
    if (!fs.existsSync(PID_FILE)) return false;
    const pid = parseInt(fs.readFileSync(PID_FILE, "utf-8").trim(), 10);
    return !isNaN(pid) && isPidAlive(pid);
  } catch { return false; }
};

// ── Strategy Manager ──────────────────────────────────────────────────────────

export const createStrategyManager = () => {
  let weatherArbIntervalId: NodeJS.Timeout | null = null;
  let weatherArbConfig: PolymarketWeatherConfig | null = null;
  let weatherArbLastReadings: PolymarketWeatherReading[] = [];
  let weatherArbLastCheckAt: string | null = null;
  let isOwnerProcess = false;

  const xStrategy = createXStrategy();

  const buildLiveStatus = (): StrategyStatus => {
    const xs = xStrategy.getState();
    return {
      pumpfun: { running: false, lastGraduations: 0, lastCheckAt: null },
      weather_arb: {
        running: weatherArbIntervalId !== null,
        lastCheckAt: weatherArbLastCheckAt,
        cities: weatherArbConfig?.cities ?? [],
        lastReadings: weatherArbLastReadings,
      },
      x_strategy: {
        running: xs.running,
        lastCheckAt: xs.lastCheckAt,
        tweetsThisHour: xs.tweetsThisHour,
        lastTweetId: xs.lastTweetId,
      },
    };
  };

  const saveStatusToDisk = () => {
    try { atomicWriteJSON(STATUS_FILE, buildLiveStatus()); } catch (e) {
      console.error(`[strategyManager] Failed to write status file: ${e}`);
    }
  };

  const writePidFile = () => {
    try { fs.writeFileSync(PID_FILE, String(process.pid)); } catch (e) {
      console.error(`[strategyManager] Failed to write PID file: ${e}`);
    }
  };

  const cleanupPidFile = () => { try { fs.unlinkSync(PID_FILE); } catch {} };

  const getStatus = (
    forceLive = false,
  ): StrategyStatus & { _stale?: boolean; _source?: string } => {
    if (forceLive || isOwnerProcess) return { ...buildLiveStatus(), _source: "live" };

    if (fs.existsSync(STATUS_FILE)) {
      try {
        const fileData = JSON.parse(fs.readFileSync(STATUS_FILE, "utf-8")) as StrategyStatus;
        const ageMs = Date.now() - fs.statSync(STATUS_FILE).mtimeMs;

        if (fileData.weather_arb.running && !isDaemonRunning()) {
          console.warn("[strategyManager] Status file says RUNNING but daemon PID is dead. Cleaning up.");
          try { fs.unlinkSync(STATUS_FILE); } catch {}
          try { fs.unlinkSync(PID_FILE); } catch {}
          return { ...buildLiveStatus(), _source: "dead_daemon_cleanup" };
        }

        return { ...fileData, _stale: ageMs > 10 * 60 * 1000, _source: "file" };
      } catch { /* corrupted file */ }
    }

    return { ...buildLiveStatus(), _source: "default" };
  };

  const startWeatherArb = (config: PolymarketWeatherConfig) => {
    isOwnerProcess = true;
    weatherArbConfig = config;

    const onReading = (readings: PolymarketWeatherReading[]) => {
      weatherArbLastReadings = readings;
      weatherArbLastCheckAt = new Date().toISOString();
      saveStatusToDisk();
    };

    writePidFile();
    saveStatusToDisk();
    runPolymarketWeatherArbTick(config, onReading).catch(console.error);

    weatherArbIntervalId = setInterval(
      () => runPolymarketWeatherArbTick(config, onReading).catch(console.error),
      (config.intervalSeconds || 120) * 1000,
    );

    const cleanup = () => {
      if (weatherArbIntervalId) { clearInterval(weatherArbIntervalId); weatherArbIntervalId = null; }
      saveStatusToDisk();
      cleanupPidFile();
    };

    process.on("SIGTERM", () => { cleanup(); process.exit(0); });
    process.on("SIGINT",  () => { cleanup(); process.exit(0); });
    process.on("exit", cleanup);
  };

  const stopWeatherArb = () => {
    if (weatherArbIntervalId) {
      clearInterval(weatherArbIntervalId);
      weatherArbIntervalId = null;
      saveStatusToDisk();
      cleanupPidFile();
    }
  };

  const startXStrategy = (xConfig: XConfig, strategyConfig: XStrategyConfig) => {
    isOwnerProcess = true;
    xStrategy.start(xConfig, strategyConfig);
    saveStatusToDisk();
  };

  const stopXStrategy = () => {
    xStrategy.stop();
    saveStatusToDisk();
  };

  const notifyXTrade = (xConfig: XConfig, strategyConfig: XStrategyConfig, summary: string) => {
    xStrategy.onTrade(xConfig, strategyConfig, summary);
  };

  return { startWeatherArb, stopWeatherArb, startXStrategy, stopXStrategy, notifyXTrade, getStatus, STATUS_FILE, PID_FILE };
};

export const strategyManager = createStrategyManager();
