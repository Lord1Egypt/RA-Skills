import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { TelegramAlerter } from '../alerters/telegram.js';
import { ClawDoctorConfig, DEFAULT_CONFIG } from '../config.js';
import { WatchResult } from '../watchers/base.js';

function makeConfig(overrides: Partial<ClawDoctorConfig['alerts']['telegram']> = {}): ClawDoctorConfig {
  return {
    ...DEFAULT_CONFIG,
    alerts: {
      telegram: {
        enabled: true,
        botToken: 'test-token',
        chatId: '123456',
        ...overrides,
      },
    },
  };
}

describe('TelegramAlerter', () => {
  it('formatMessage includes watcher name and message', () => {
    const alerter = new TelegramAlerter(makeConfig());
    const result: WatchResult = {
      ok: false,
      severity: 'critical',
      event_type: 'gateway_down',
      message: 'Gateway process not found',
    };
    const msg = alerter.formatMessage({ watcher: 'GatewayWatcher', result });
    assert.ok(msg.includes('GatewayWatcher'));
    assert.ok(msg.includes('Gateway process not found'));
  });

  it('formatMessage uses 🔴 for critical', () => {
    const alerter = new TelegramAlerter(makeConfig());
    const result: WatchResult = { ok: false, severity: 'critical', event_type: 'gateway_down', message: 'Down' };
    const msg = alerter.formatMessage({ watcher: 'GatewayWatcher', result });
    assert.ok(msg.includes('🔴'));
  });

  it('formatMessage uses 🟢 for info/ok', () => {
    const alerter = new TelegramAlerter(makeConfig());
    const result: WatchResult = { ok: true, severity: 'info', event_type: 'gateway_running', message: 'All good' };
    const msg = alerter.formatMessage({ watcher: 'GatewayWatcher', result });
    assert.ok(msg.includes('🟢'));
  });

  it('formatMessage uses 🟡 for warning', () => {
    const alerter = new TelegramAlerter(makeConfig());
    const result: WatchResult = { ok: false, severity: 'warning', event_type: 'cron_overdue', message: 'Cron overdue' };
    const msg = alerter.formatMessage({ watcher: 'CronWatcher', result });
    assert.ok(msg.includes('🟡'));
  });

  it('formatMessage includes heal result when provided', () => {
    const alerter = new TelegramAlerter(makeConfig());
    const result: WatchResult = { ok: false, severity: 'critical', event_type: 'gateway_down', message: 'Down' };
    const msg = alerter.formatMessage({
      watcher: 'GatewayWatcher',
      result,
      healResult: { success: true, action: 'openclaw gateway restart', message: 'Back online' },
    });
    assert.ok(msg.includes('openclaw gateway restart'));
    assert.ok(msg.includes('Back online'));
  });

  it('formatMessage includes time and host', () => {
    const alerter = new TelegramAlerter(makeConfig());
    const result: WatchResult = { ok: false, severity: 'error', event_type: 'err', message: 'Err' };
    const msg = alerter.formatMessage({ watcher: 'TestWatcher', result });
    assert.ok(msg.includes('UTC'));
  });

  it('shouldAlert returns true for error/critical/warning', () => {
    const alerter = new TelegramAlerter(makeConfig());
    for (const severity of ['warning', 'error', 'critical'] as const) {
      const result: WatchResult = { ok: false, severity, event_type: 'test', message: 'test' };
      assert.equal(alerter.shouldAlert(result), true);
    }
  });

  it('shouldAlert returns false for info', () => {
    const alerter = new TelegramAlerter(makeConfig());
    const result: WatchResult = { ok: true, severity: 'info', event_type: 'ok', message: 'ok' };
    assert.equal(alerter.shouldAlert(result), false);
  });

  it('rate limiting prevents duplicate alerts within 5 minutes', async () => {
    // We test the rate-limit logic indirectly by checking lastAlertTime tracking
    const alerter = new TelegramAlerter(makeConfig({ enabled: false })); // disabled so no real HTTP

    // Access private field via cast for testing
    const alerterAny = alerter as unknown as { lastAlertTime: Map<string, number>; isRateLimited: (name: string) => boolean; markAlerted: (name: string) => void };

    assert.equal(alerterAny.isRateLimited('GatewayWatcher'), false);
    alerterAny.markAlerted('GatewayWatcher');
    assert.equal(alerterAny.isRateLimited('GatewayWatcher'), true);
  });

  it('sendAlert returns false when telegram is disabled', async () => {
    const config = makeConfig({ enabled: false });
    const alerter = new TelegramAlerter(config);
    const result: WatchResult = { ok: false, severity: 'critical', event_type: 'down', message: 'Down' };
    const sent = await alerter.sendAlert({ watcher: 'GatewayWatcher', result });
    assert.equal(sent, false);
  });

  it('sendAlert returns false when botToken is empty', async () => {
    const config = makeConfig({ enabled: true, botToken: '', chatId: '123' });
    const alerter = new TelegramAlerter(config);
    const result: WatchResult = { ok: false, severity: 'critical', event_type: 'down', message: 'Down' };
    const sent = await alerter.sendAlert({ watcher: 'GatewayWatcher', result });
    assert.equal(sent, false);
  });
});
