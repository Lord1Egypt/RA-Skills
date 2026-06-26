// ============================================================
// ssh-lab type definitions — zero external dependencies
// ============================================================

/** Host configuration (resolved from SSH config + custom overrides) */
export interface HostConfig {
  alias: string;
  hostname: string;
  user?: string;
  port?: number;
  identityFile?: string;
  proxyJump?: string;
  /** Where this config came from */
  source: 'ssh-config' | 'custom';
  tags: string[];
  notes?: string;
  /** Default remote working directory */
  defaultPath?: string;
}

/** Result of a single SSH command execution */
export interface SshExecResult {
  host: string;
  command: string;
  stdout: string;
  stderr: string;
  exitCode: number | null;
  durationMs: number;
  timedOut: boolean;
}

/** Options for SSH execution */
export interface SshExecOptions {
  timeoutMs?: number;
  /** Inherit stdio (for interactive / streaming) */
  inherit?: boolean;
}

// ── Probe system ──────────────────────────────────────────────

/** A single probe collects structured data from a remote host */
export interface Probe {
  name: string;
  /** Remote command to execute */
  command: string;
  /** Parse stdout into structured data */
  parse(stdout: string): ProbeData;
}

/** Union of all probe data types */
export type ProbeData = GpuProbeData | DiskProbeData | ProcessProbeData;

export interface GpuInfo {
  index: number;
  name: string;
  utilizationPct: number;
  memoryUsedMiB: number;
  memoryTotalMiB: number;
  memoryPct: number;
  temperatureC: number;
  powerW: number;
}

export interface GpuProcess {
  pid: number;
  gpuIndex: number;
  memoryMiB: number;
  name: string;
  /** Full command line if available */
  cmdline?: string;
}

export interface GpuProbeData {
  probe: 'gpu';
  available: boolean;
  driverVersion?: string;
  gpus: GpuInfo[];
  processes: GpuProcess[];
}

export interface DiskInfo {
  filesystem: string;
  size: string;
  used: string;
  available: string;
  usedPct: number;
  mountpoint: string;
}

export interface DiskProbeData {
  probe: 'disk';
  disks: DiskInfo[];
}

export interface ProcessInfo {
  pid: number;
  user: string;
  cpuPct: number;
  memPct: number;
  vsz: string;
  rss: string;
  command: string;
}

export interface ProcessProbeData {
  probe: 'process';
  processes: ProcessInfo[];
}

// ── Command results ──────────────────────────────────────────

/** Unified result wrapper for all commands */
export interface CommandResult<T = unknown> {
  ok: boolean;
  host?: string;
  command: string;
  data?: T;
  summary: string;
  raw?: string;
  error?: { code: string; message: string };
  durationMs: number;
}

/** Status data for a single host */
export interface HostStatus {
  host: HostConfig;
  gpu: GpuProbeData;
  disk: DiskProbeData;
  process: ProcessProbeData;
  alerts: Alert[];
  durationMs: number;
}

/** Simple alert from structured data */
export interface Alert {
  level: 'info' | 'warn' | 'error';
  host: string;
  message: string;
}

// ── Config ───────────────────────────────────────────────────

export interface SshLabConfig {
  version: number;
  defaults: {
    sshTimeoutMs: number;
    commandTimeoutMs: number;
    maxConcurrency: number;
    output: 'summary' | 'json' | 'raw';
  };
  hosts: Record<string, Partial<HostConfig>>;
}

export type OutputMode = 'summary' | 'json' | 'raw';

// ── Alert system ─────────────────────────────────────────────

export type NoticeLevel = 'info' | 'warning' | 'critical';

export type AlertRuleKind =
  | 'gpu_idle'
  | 'disk_full'
  | 'process_died'
  | 'ssh_unreachable'
  | 'oom_detected'
  | 'high_temp';

export interface AlertRule {
  id: string;
  kind: AlertRuleKind;
  host: string; // host alias or 'all'
  enabled: boolean;
  threshold?: number;
  processPattern?: string;
  createdAt: string;
}

export interface AlertFiring {
  ruleId: string;
  kind: AlertRuleKind;
  host: string;
  level: NoticeLevel;
  message: string;
  value?: number;
  threshold?: number;
  firedAt: string;
}

export interface AlertCheckResult {
  host: string;
  firings: AlertFiring[];
  errors: string[];
}

/**
 * Flattened host status data for alert evaluation.
 * Adapts the probe-based HostStatus into a shape alerts can work with.
 */
export interface HostStatusData {
  host: HostConfig;
  gpu: GpuInfo[];
  disk: DiskInfo[];
  processes: ProcessInfo[];
  collectorErrors: string[];
}

// ── Doctor ───────────────────────────────────────────────────

export interface DoctorCheck {
  name: string;
  status: 'pass' | 'warn' | 'fail' | 'skip';
  message: string;
  durationMs: number;
}

export interface DoctorResult {
  host: string;
  checks: DoctorCheck[];
  overallStatus: 'healthy' | 'degraded' | 'unhealthy';
}

// ── SSH error classification ─────────────────────────────────

export type SshErrorCode =
  | 'AUTH_FAILED'
  | 'HOST_UNREACHABLE'
  | 'TIMEOUT'
  | 'COMMAND_FAILED'
  | 'CONNECTION_REFUSED'
  | 'UNKNOWN';

export interface SshError {
  code: SshErrorCode;
  message: string;
  retryable: boolean;
}
