import { BaseWatcher, WatchResult } from './base.js';
import { runShell } from '../utils.js';

export class GatewayWatcher extends BaseWatcher {
  readonly name = 'GatewayWatcher';
  readonly defaultInterval = 30;

  async check(): Promise<WatchResult[]> {
    // Check openclaw gateway status directly
    const status = runShell('openclaw gateway status 2>/dev/null');
    if (status.ok && /running|active|started/i.test(status.stdout)) {
      return [this.ok('Gateway running', 'gateway_running')];
    }

    // Fallback: check systemd service
    const systemctl = runShell('systemctl is-active openclaw-gateway 2>/dev/null');
    if (systemctl.ok && systemctl.stdout.trim() === 'active') {
      return [this.ok('Gateway systemd service active', 'gateway_running')];
    }

    // Fallback: check if any openclaw gateway process exists
    // Use more specific match to avoid matching unrelated openclaw processes
    const pgrep = runShell('pgrep -f "openclaw.*gateway" 2>/dev/null');
    if (pgrep.ok && pgrep.stdout.trim().length > 0) {
      const pid = pgrep.stdout.trim().split('\n')[0]; // Just show first PID
      return [this.ok(`Gateway process running (PID: ${pid})`, 'gateway_running')];
    }

    return [
      this.critical(
        'Gateway process not found',
        'gateway_down',
        { statusOutput: status.stdout?.substring(0, 200), statusErr: status.stderr?.substring(0, 200) }
      ),
    ];
  }
}
