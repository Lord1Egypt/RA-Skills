"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCapabilityBoundary = getCapabilityBoundary;
const allowed = [
    {
        name: 'readSignals',
        allowed: true,
        boundary: 'read_only',
        reason: 'WorldLoops may read provided input signals.',
    },
    {
        name: 'generateBrief',
        allowed: true,
        boundary: 'read_only',
        reason: 'WorldLoops may generate a brief from observed signals.',
    },
    {
        name: 'generateProposalCandidates',
        allowed: true,
        boundary: 'read_only',
        reason: 'WorldLoops may propose candidate transitions for review.',
    },
    {
        name: 'persistTransitionReceipt',
        allowed: true,
        boundary: 'local_commit',
        reason: 'WorldLoops may persist local audit receipts.',
    },
    {
        name: 'persistLocalOpenLoopState',
        allowed: true,
        boundary: 'local_commit',
        reason: 'WorldLoops may persist local open-loop state.',
    },
    {
        name: 'transitionLocalOpenLoopState',
        allowed: true,
        boundary: 'local_commit',
        reason: 'WorldLoops may transition local open-loop state.',
    },
];
const denied = [
    {
        name: 'sendEmail',
        allowed: false,
        boundary: 'external_write',
        reason: 'Sending email would modify an external system.',
    },
    {
        name: 'createEmailDraft',
        allowed: false,
        boundary: 'external_write',
        reason: 'Creating drafts would write to Gmail or another mail system.',
    },
    {
        name: 'sendSlackMessage',
        allowed: false,
        boundary: 'external_write',
        reason: 'Sending Slack messages would modify an external system.',
    },
    {
        name: 'createCalendarEvent',
        allowed: false,
        boundary: 'external_write',
        reason: 'Creating calendar events would modify an external system.',
    },
    {
        name: 'modifyGitHub',
        allowed: false,
        boundary: 'external_write',
        reason: 'Modifying GitHub issues, PRs, or repos would write externally.',
    },
    {
        name: 'writeExternalSystem',
        allowed: false,
        boundary: 'external_write',
        reason: 'External writes are outside the public WorldLoops skill boundary.',
    },
];
function getCapabilityBoundary() {
    return {
        externalWrite: false,
        mode: 'safe_by_default',
        allowed,
        denied,
    };
}
//# sourceMappingURL=capabilityBoundary.js.map