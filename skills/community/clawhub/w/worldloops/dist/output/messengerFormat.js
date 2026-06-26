"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.printMessengerOutput = printMessengerOutput;
exports.printCompactOutput = printCompactOutput;
function severityEmoji(severity) {
    switch (severity) {
        case 'critical':
            return '🔴';
        case 'high':
            return '🚨';
        case 'medium':
            return '⚠️';
        default:
            return '📋';
    }
}
function sourceLabel(source) {
    switch (source) {
        case 'gmail':
            return 'Gmail';
        case 'slack':
            return 'Slack';
        case 'calendar':
            return 'Calendar';
        case 'github':
            return 'GitHub';
        default:
            return 'Signal';
    }
}
function printMessengerOutput(data) {
    console.log('');
    console.log('🦞 WorldLoops Guard');
    console.log('');
    if (!data.ok || data.candidates.length === 0) {
        console.log('No open loops detected');
        console.log('');
        console.log('✅ Safe');
        console.log('externalWrite: false');
        console.log('No email sent. No external system changed.');
        console.log('');
        return;
    }
    const count = data.openLoopCount;
    console.log(`${count} open loop${count === 1 ? '' : 's'} detected`);
    for (const candidate of data.candidates) {
        const emoji = severityEmoji(candidate.severity);
        const sev = candidate.severity
            ? candidate.severity.charAt(0).toUpperCase() + candidate.severity.slice(1)
            : 'Unknown';
        const src = sourceLabel(candidate.source);
        const title = candidate.reason || candidate.entityType.replace(/_/g, ' ');
        console.log('');
        console.log(`${emoji} ${sev} — ${src} ${title}`);
        console.log(`State: ${candidate.currentState}`);
        if (candidate.actionHint) {
            console.log('');
            console.log('Proposal:');
            console.log(candidate.actionHint);
        }
        console.log('');
        console.log('Adjudication:');
        console.log(candidate.approvalRequired ? 'requires_approval' : 'auto_approved');
    }
    console.log('');
    console.log('Receipt:');
    if (data.proposalsAlreadyTracked > 0 && data.proposalsPersisted === 0) {
        console.log('already tracked');
    }
    else {
        console.log('local proposal recorded');
    }
    console.log('');
    console.log('✅ Safe');
    console.log('externalWrite: false');
    console.log('No email sent. No external system changed.');
    console.log('');
}
function printCompactOutput(data) {
    console.log('🦞 Agent Execution Guard');
    console.log('');
    if (!data.ok || data.candidates.length === 0) {
        console.log('No open loops detected');
        console.log('');
        console.log('✅ Safe');
        console.log('externalWrite:false');
        console.log('No email, draft, call, or external change made.');
        return;
    }
    for (const candidate of data.candidates) {
        const emoji = severityEmoji(candidate.severity);
        const sev = candidate.severity
            ? candidate.severity.charAt(0).toUpperCase() + candidate.severity.slice(1)
            : 'Unknown';
        const src = sourceLabel(candidate.source);
        const title = candidate.reason || candidate.entityType.replace(/_/g, ' ');
        console.log(`${emoji} ${sev} — ${src} ${title}`);
        console.log(`State: ${candidate.currentState}`);
        if (candidate.actionHint) {
            console.log('');
            console.log('Proposal:');
            console.log(candidate.actionHint);
        }
        console.log('');
        console.log('Adjudication:');
        console.log(candidate.approvalRequired ? 'requires_approval' : 'auto_approved');
        console.log('');
    }
    console.log('✅ Safe');
    console.log('externalWrite:false');
    console.log('No email, draft, call, or external change made.');
}
//# sourceMappingURL=messengerFormat.js.map