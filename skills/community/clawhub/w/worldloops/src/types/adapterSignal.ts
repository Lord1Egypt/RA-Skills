export interface AdapterSignal {
  source: string;
  sourceType: string;
  externalWrite: false;
  text: string;
  observedAt: string;
  url?: string;
  summary?: string;
  metadata?: Record<string, unknown>;
}

export type AdapterSignalValidationResult =
  | { ok: true; signal: AdapterSignal }
  | { ok: false; errors: string[] };

/** Categorizes whether an adapter is maintained by WorldLoops or the community. */
export type AdapterStatus = 'core' | 'community' | 'experimental';
