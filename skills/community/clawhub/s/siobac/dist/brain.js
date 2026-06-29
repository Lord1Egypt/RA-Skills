// Agent-brain owner surface (the brain itself runs on the SERVER). Extracted from cli.ts.
import * as api from './api.js';
import { requireString, optionalString, optionalNonNegInt } from './argparse.js';
import { ok, requireBoundAgent } from './runtime.js';
// ── Agent Brain — owner surface (the brain itself runs on the SERVER) ──
// docs/agent-brain-design.md, references/brain.md. The server composes + sends
// autonomous replies and escalates owner-committing asks; this skill only lets
// the owner toggle autonomous mode (pause/go-online), read presence, and handle
// escalations (owner-channel, brain-pending/brain-resolve) plus owner-triggered
// outreach/interrupt. There is NO client tick/loop here — see brain.md.
// Go online — resume autonomous mode (the server auto-replies again) after a pause.
// Autonomous is the DEFAULT once shared, so this is only needed to undo a pause.
export async function cmdGoOnline(_flags) {
    const { auth, agentId } = await requireBoundAgent();
    const res = await api.brainGoOnline(auth.accessToken, agentId);
    ok({ status: 'ok', ...res, next_step: "Autonomous mode is ON. Tell the owner (in their language) you're online — answering their friends automatically and flagging anything that needs them. Nothing to keep alive." });
}
// Pause — switch to manual: the server stops auto-replying; messages wait for you.
export async function cmdBrainHandback(_flags) {
    const { auth, agentId } = await requireBoundAgent();
    const res = await api.brainHandback(auth.accessToken, agentId);
    ok({ status: 'ok', ...res, next_step: "Autonomous mode is now PAUSED. Tell the owner (in their language) you've stopped auto-replying and messages will wait for them; they can say 'go online' to resume. Run `go-online` when they do." });
}
// Online check: am I auto-replying (online) or paused (manual)? The SERVER is the
// responder — there's no client task to keep alive.
export async function cmdBrainStatus(_flags) {
    const { auth, agentId } = await requireBoundAgent();
    const res = await api.brainPresence(auth.accessToken, agentId);
    ok({
        status: 'ok', ...res,
        next_step: res.online
            ? 'ONLINE — the server auto-replies for this agent and escalates anything that needs the owner. Nothing to arm or keep alive.'
            : 'PAUSED (manual) — the server is NOT auto-replying; messages wait for the owner. Run `go-online` to resume autonomous replies.',
    });
}
// owner-channel: no --message → READ (the owner<->you thread); with --message →
// POST as the agent (talk back / clarify / answer / report).
export async function cmdOwnerChannel(flags) {
    const { auth, agentId } = await requireBoundAgent();
    const text = optionalString(flags, 'message');
    if (text !== undefined) {
        const res = await api.brainOwnerChannelPost(auth.accessToken, agentId, 'agent', text);
        ok({ status: 'sent', ...res, next_step: 'Posted to the owner-channel as the agent. Nothing else needed unless the owner asked a question that needs a follow-up command.' });
        return;
    }
    const since = optionalNonNegInt(flags, 'since') ?? 0;
    const res = await api.brainOwnerChannelRead(auth.accessToken, agentId, since);
    ok({
        status: 'ok', ...res,
        next_step: "This is the owner<->agent thread (server notices + your own messages), oldest→newest. Summarize anything new for the owner IN THEIR LANGUAGE — never echo the raw lines. A 🔔/🔄 notice means a reply is HELD: handle it via `brain-pending` → `brain-resolve`. To post back as the agent, run `owner-channel --message \"<text>\"`.",
    });
}
// dismiss: drop a notice from the overview (email-style inbox) — DURABLY (server
// side, so it stays gone across logins). `--seq <n>` drops ONE notice ("leave it");
// `--all` (with `--up-to <n>` = the latest notice seq) clears the whole FYI batch.
// Nothing is deleted from history — the friend/conversation is still in `conversations`.
export async function cmdDismiss(flags) {
    const { auth, agentId } = await requireBoundAgent();
    const all = flags['all'] === true || flags['all'] === 'true';
    const upTo = optionalNonNegInt(flags, 'up-to');
    const seq = optionalNonNegInt(flags, 'seq');
    if (all || upTo !== undefined) {
        // Bulk clear: advance the read-cursor to the latest seen notice seq.
        const target = upTo ?? seq;
        if (target === undefined) {
            ok({ status: 'error', error: 'dismiss --all needs --up-to <latest notice seq from check>', next_step: 'Re-run `check`, take the highest notice `seq`, then `dismiss --all --up-to <that seq>`.' });
            return;
        }
        const res = await api.dismissNotice(auth.accessToken, agentId, { up_to_seq: target });
        ok({ status: 'cleared', ...res, next_step: "Overview FYI cleared — those recaps won't re-surface, even on a fresh login. Tell the owner (in their language) it's done; the conversations themselves are still under `conversations` if they want them. Then RE-RUN `check` and re-show the overview list." });
        return;
    }
    if (seq === undefined) {
        ok({ status: 'error', error: 'dismiss needs --seq <notice seq> (one) or --all --up-to <seq> (clear all)', next_step: 'Use the notice `seq` from `check`: `dismiss --seq <n>` for one, or `dismiss --all --up-to <latest seq>` for all.' });
        return;
    }
    const res = await api.dismissNotice(auth.accessToken, agentId, { seq });
    ok({ status: 'dismissed', ...res, next_step: "That notice is dismissed — it won't show in the overview again (durable across logins). Tell the owner (in their language) you've left it; then RE-RUN `check` and re-show the remaining overview list." });
}
export async function cmdBrainPending(_flags) {
    const { auth, agentId } = await requireBoundAgent();
    const res = await api.brainPending(auth.accessToken, agentId);
    const n = Array.isArray(res.pending) ? res.pending.length : 0;
    ok({
        status: 'ok', ...res,
        next_step: n === 0
            ? 'Nothing is waiting on the owner right now. Tell them their queue is clear (in their language).'
            : `${n} reply/replies the server HELD for the owner's approval. For EACH item, tell the owner (in their language) who it's from (\`friend\`), why it needs them (\`reason\`), and the suggested reply (\`proposed_draft\`) as ONE short item with numbered options — never echo raw JSON. On their decision: approve/edit → \`brain-resolve --request-id <request_id> --action sent [--message \"<edited text>\"]\`; \"I'll handle it\" → \`--action handed_off\`; decline → \`--action declined\`.`,
    });
}
export async function cmdBrainResolve(flags) {
    const { auth, agentId } = await requireBoundAgent();
    const requestId = requireString(flags, 'request-id', 'brain-resolve');
    const action = (optionalString(flags, 'action') ?? 'sent');
    // action 'sent' DELIVERS the held reply. Pass --message to send the owner's
    // edited/approved text (sent scan-bypassed, since the owner approved it); omit
    // to send the held draft as-is. This is how an approved escalation goes out —
    // do NOT also run a separate `send` for it (that would double-send + re-scan).
    // action 'declined' now ALSO sends a brief refusal to the friend (so they aren't
    // left hanging and the "no" is on record); --message lets the owner give their own
    // decline wording, else the server sends a safe default. handed_off sends nothing.
    const message = optionalString(flags, 'message');
    const res = await api.brainResolve(auth.accessToken, agentId, requestId, action, (action === 'sent' || action === 'declined') ? message : undefined);
    // Close the loop with ONE clear status for the owner: DONE or UPDATE.
    const next_step = res.outcome === 'updated'
        ? `UPDATE — the friend said something that changed things since the owner approved, so the OLD reply was NOT sent. The hold is refreshed and still open. Tell the owner in ONE line it's an update (what changed: "${res.update?.reason ?? ''}") with the new suggestion ("${res.update?.draft ?? ''}") + numbered options. See scripts → "Escalation resolved".`
        : action === 'sent'
            ? (res.sent ? 'DONE — approved reply delivered. Tell the owner in ONE line it is sent + closed (scripts → "Escalation resolved").' : 'Resolved — no text to send.')
            : action === 'declined'
                ? 'DONE — declined, and I sent the friend a brief "no" so they are not left hanging (and the brain now sees it was declined). Tell the owner in ONE line you turned it down + let them know.'
                : `DONE — ${action}. Tell the owner in ONE line it is handled (scripts → "Escalation resolved").`;
    ok({ status: 'ok', ...res, next_step });
}
// OWNER-TRIGGERED outreach. The agent NEVER self-initiates: run this ONLY because
// the owner said so in the owner-channel ("go talk to X"). Sends an opener into an
// existing connection; after that it's a normal conversation the server handles.
// (New-connection-via-invite outreach uses `connect` + `send`.)
export async function cmdBrainOutreach(flags) {
    const { auth, agentId } = await requireBoundAgent();
    const connId = requireString(flags, 'conversation', 'brain-outreach');
    const message = requireString(flags, 'message', 'brain-outreach');
    const res = await api.postReply(auth.accessToken, agentId, connId, message);
    ok({ status: 'sent', conversation: connId, ...res, next_step: 'Owner-triggered opener sent. It is now a normal conversation the server handles; the reply shows up on `check`. Tell the owner (in their language) the message went out.' });
}
// Interrupt: the owner said "stop talking to Y". Pause the connection so the
// server leaves it alone (resume later with `resume-connection`).
export async function cmdBrainInterrupt(flags) {
    const { auth, agentId } = await requireBoundAgent();
    const connId = requireString(flags, 'conversation', 'brain-interrupt');
    await api.actOnConnection(auth.accessToken, agentId, connId, 'pause');
    ok({ status: 'paused', conversation: connId, next_step: "This one conversation is paused — the server will leave it alone until the owner says otherwise. Tell the owner (in their language) it's paused; run `resume-connection` to undo." });
}
