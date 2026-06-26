export type CapabilityName = 'readSignals' | 'generateBrief' | 'generateProposalCandidates' | 'persistTransitionReceipt' | 'persistLocalOpenLoopState' | 'transitionLocalOpenLoopState' | 'sendEmail' | 'createEmailDraft' | 'sendSlackMessage' | 'createCalendarEvent' | 'modifyGitHub' | 'writeExternalSystem';
export interface CapabilityRule {
    name: CapabilityName;
    allowed: boolean;
    boundary: 'read_only' | 'local_commit' | 'external_write';
    reason: string;
}
export interface CapabilityBoundary {
    externalWrite: false;
    mode: 'safe_by_default';
    allowed: CapabilityRule[];
    denied: CapabilityRule[];
}
