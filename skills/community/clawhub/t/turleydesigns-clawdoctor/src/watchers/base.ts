import { ClawDoctorConfig } from '../config.js';
import { insertEvent, Severity } from '../store.js';
import { nowIso } from '../utils.js';

export interface WatchResult {
  ok: boolean;
  severity: Severity;
  event_type: string;
  message: string;
  details?: Record<string, unknown>;
}

export abstract class BaseWatcher {
  abstract readonly name: string;
  abstract readonly defaultInterval: number;

  protected config: ClawDoctorConfig;

  constructor(config: ClawDoctorConfig) {
    this.config = config;
  }

  abstract check(): Promise<WatchResult[]>;

  async run(): Promise<WatchResult[]> {
    const results = await this.check();
    for (const result of results) {
      insertEvent({
        timestamp: nowIso(),
        watcher: this.name,
        severity: result.severity,
        event_type: result.event_type,
        message: result.message,
        details: result.details ? JSON.stringify(result.details) : undefined,
      });
    }
    return results;
  }

  protected ok(message: string, event_type = 'check_ok'): WatchResult {
    return { ok: true, severity: 'info', event_type, message };
  }

  protected warn(message: string, event_type: string, details?: Record<string, unknown>): WatchResult {
    return { ok: false, severity: 'warning', event_type, message, details };
  }

  protected error(message: string, event_type: string, details?: Record<string, unknown>): WatchResult {
    return { ok: false, severity: 'error', event_type, message, details };
  }

  protected critical(message: string, event_type: string, details?: Record<string, unknown>): WatchResult {
    return { ok: false, severity: 'critical', event_type, message, details };
  }
}
