export type BoundaryCrossed = 'read_only' | 'local_commit' | 'external_write';

export interface TransitionReceiptRedactions {
  applied: boolean;
  fields: string[];
}

export interface TransitionReceipt {
  id: string;
  createdAt: string;
  proposalId: string | null;
  sourceSignalsObserved: string[];
  normalizedResponsibility: string | null;
  proposedTransition: {
    currentState: string;
    proposedState: string;
  } | null;
  reason: string | null;
  adjudicationResult: string | null;
  boundaryCrossed: BoundaryCrossed;
  externalWrite: false;
  actor: string | null;
  decision: string | null;
  unresolvedState: string | null;
  redactions: TransitionReceiptRedactions;
}
