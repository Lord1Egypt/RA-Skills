import type { OpenLoopStatus } from './openLoopState';

export type StuckLoopReason =
  | 'todo_timeout'
  | 'doing_timeout'
  | 'snooze_expired'
  | 'high_or_critical_overdue'
  | 'none';

export interface StuckLoopPolicyConfig {
  todoTimeoutHours: number;
  doingTimeoutHours: number;
}

export interface StuckLoopEvaluation {
  shouldTransition: boolean;
  from: OpenLoopStatus;
  to: OpenLoopStatus;
  reason: StuckLoopReason;
  note: string;
  safety: {
    externalWrite: false;
  };
}
