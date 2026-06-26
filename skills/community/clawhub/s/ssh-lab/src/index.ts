// ssh-lab — public API exports
// CLI entry is cli.ts; this is the library entry for programmatic use.

export { execSsh, classifySshError, execSshWithRetry, TIMEOUT_TIERS } from './ssh/exec.js';
export { withPool } from './ssh/pool.js';
export { resolveHost, resolveHosts, discoverHosts, loadLabConfig, saveLabConfig } from './ssh/config.js';
export { defaultProbes, getProbe, gpuProbe, diskProbe, processProbe } from './probes/index.js';
export { evaluateAlerts } from './alerts/rules.js';
export { loadRules, addRule, removeRule, rulesForHost } from './alerts/state.js';
export { render, exitCode } from './output/formatter.js';

// CLI helpers
export { parseArgs, getOutputMode } from './cli.js';

// Commands
export { statusCommand } from './commands/status.js';
export { runCommand } from './commands/run.js';
export { compareCommand } from './commands/compare.js';
export { doctorCommand } from './commands/doctor.js';
export { alertListCommand, alertAddCommand, alertRemoveCommand, alertCheckCommand } from './commands/alert.js';

// Types
export type {
  HostConfig,
  SshExecResult,
  SshExecOptions,
  SshError,
  SshErrorCode,
  Probe,
  ProbeData,
  GpuProbeData,
  GpuInfo,
  GpuProcess,
  DiskProbeData,
  DiskInfo,
  ProcessProbeData,
  ProcessInfo,
  CommandResult,
  HostStatus,
  Alert,
  SshLabConfig,
  OutputMode,
  AlertRule,
  AlertRuleKind,
  AlertFiring,
  AlertCheckResult,
  HostStatusData,
  NoticeLevel,
  DoctorResult,
  DoctorCheck,
} from './types/index.js';
