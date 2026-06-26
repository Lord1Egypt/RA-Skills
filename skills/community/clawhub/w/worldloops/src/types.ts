export type SignalSource =
  | 'slack'
  | 'gmail'
  | 'calendar'
  | 'github'
  | 'manual';

export interface Signal {
  source: SignalSource;
  text: string;
  url?: string;
  createdAt?: string;
}

export interface OpenLoop {
  source: SignalSource;
  text: string;
  reason: string;
}

export interface ProposalCandidate {
  idempotencyKey: string;
  entityType: string;
  source: SignalSource;
  currentState: string;
  proposedState: string;
  reason: string;
  approvalRequired: boolean;
  actionHint: string;
  severity?: MinSeverity;
}

export interface WorldLoopsBriefResponse {
  ok: boolean;
  mode?: string;
  source?: string;
  brief?: string;
  openLoops?: OpenLoop[];
  proposalCandidates?: ProposalCandidate[];
  metadata?: Record<string, unknown>;
  safety: {
    externalWrite: false;
    note?: string;
  };
  error?: {
    code: string;
    message: string;
  };
}

// Notification preference types

export type MinSeverity = 'low' | 'medium' | 'high' | 'critical';

export interface NotificationPrefs {
  dailyBrief: {
    enabled: boolean;
    time: string;
    timezone: string;
    channel?: string;
    minimumSeverity?: MinSeverity;
    sources?: string[];
  };
  proactiveDiscovery: {
    enabled: boolean;
    scanIntervalMinutes: number;
    minSeverity: MinSeverity;
  };
  quietHours: {
    enabled: boolean;
    start: string;
    end: string;
  };
  eventAlerts: {
    enabled: boolean;
    rules: string[];
  };
  channels: {
    cli: boolean;
  };
}

export interface NotificationState {
  suppressedKeys: string[];
  lastBriefAt?: string;
  lastDiscoveryAt?: string;
}
