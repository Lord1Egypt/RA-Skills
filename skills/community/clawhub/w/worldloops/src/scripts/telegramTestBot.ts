import * as https from 'node:https';
import * as fs from 'node:fs';
import * as path from 'node:path';
import { spawnSync } from 'node:child_process';
import { loadObservations, runIntake } from '../openclawIntake';
import type {
  IntakeSummary,
  AdjudicationResult,
  OpenClawObservation,
  SuppressionReason,
} from '../openclawIntake';
import { loadOpenLoopStates } from '../storage/openLoopStates';
import type { OpenLoopState } from '../types/openLoopState';

const OPENCLAW_INBOX = path.join(process.env.HOME ?? '', '.openclaw/workspace/.worldloops/inbox');

const DEMO_FIXTURE_PATH = 'scripts/fixtures/openclaw-signal-intake/demo-observations.json';
const INTERPRETED_OBSERVATIONS = '.worldloops/inbox/openclaw-observations.json';
const MAX_LENGTH = 4096;
const TRUNCATION_SUFFIX = '\n… truncated for Telegram test output';

function loadToken(): string {
  if (process.env.TELEGRAM_BOT_TOKEN) {
    return process.env.TELEGRAM_BOT_TOKEN.trim();
  }
  const envFile = path.join(process.env.HOME ?? '', '.claude', 'channels', 'telegram', '.env');
  if (fs.existsSync(envFile)) {
    const content = fs.readFileSync(envFile, 'utf8');
    const match = /^TELEGRAM_BOT_TOKEN\s*=\s*(.+)$/m.exec(content);
    if (match) return match[1].trim();
  }
  throw new Error(
    'TELEGRAM_BOT_TOKEN not found. Set env var or add to ~/.claude/channels/telegram/.env'
  );
}

function telegramRequest(
  token: string,
  method: string,
  body: Record<string, unknown>,
  timeoutMs = 10000
): Promise<Record<string, unknown>> {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = https.request(
      {
        hostname: 'api.telegram.org',
        path: `/bot${token}/${method}`,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data),
        },
      },
      (res) => {
        let raw = '';
        res.on('data', (chunk: Buffer) => { raw += chunk; });
        res.on('end', () => {
          try {
            resolve(JSON.parse(raw) as Record<string, unknown>);
          } catch {
            reject(new Error(`JSON parse error: ${raw.slice(0, 200)}`));
          }
        });
      }
    );
    req.setTimeout(timeoutMs, () => {
      req.destroy(new Error(`Request timeout after ${timeoutMs}ms`));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function telegramGet(
  token: string,
  method: string,
  params: Record<string, unknown>,
  timeoutMs = 10000
): Promise<Record<string, unknown>> {
  return new Promise((resolve, reject) => {
    const query = Object.entries(params)
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
      .join('&');
    const req = https.request(
      {
        hostname: 'api.telegram.org',
        path: `/bot${token}/${method}${query ? '?' + query : ''}`,
        method: 'GET',
      },
      (res) => {
        let raw = '';
        res.on('data', (chunk: Buffer) => { raw += chunk; });
        res.on('end', () => {
          try {
            resolve(JSON.parse(raw) as Record<string, unknown>);
          } catch {
            reject(new Error(`JSON parse error: ${raw.slice(0, 200)}`));
          }
        });
      }
    );
    req.setTimeout(timeoutMs, () => {
      req.destroy(new Error(`Request timeout after ${timeoutMs}ms`));
    });
    req.on('error', reject);
    req.end();
  });
}

async function sendMessage(token: string, chatId: number, text: string): Promise<void> {
  await telegramRequest(token, 'sendMessage', { chat_id: chatId, text });
}

function truncate(text: string): string {
  if (text.length <= MAX_LENGTH) return text;
  const cutoff = MAX_LENGTH - TRUNCATION_SUFFIX.length;
  return text.slice(0, cutoff) + TRUNCATION_SUFFIX;
}

// Split a long brief into Telegram-sized messages at line boundaries, so the
// full brief — including the ✅ Safe footer — is always delivered rather than
// truncated mid-section.
function splitMessage(text: string, max = 4000): string[] {
  if (text.length <= max) return [text];
  const chunks: string[] = [];
  let current = '';
  for (const line of text.split('\n')) {
    if (current && current.length + 1 + line.length > max) {
      chunks.push(current);
      current = line;
    } else {
      current = current ? `${current}\n${line}` : line;
    }
  }
  if (current) chunks.push(current);
  return chunks;
}

async function sendBrief(token: string, chatId: number, text: string): Promise<void> {
  for (const chunk of splitMessage(text)) {
    await sendMessage(token, chatId, chunk);
  }
}

function srcEmoji(source: string): string {
  if (source === 'gmail' || source === 'email') return '📧';
  if (source === 'calendar') return '🗓️';
  if (source === 'slack') return '💬';
  return '📌';
}

function evField(ev: Record<string, unknown>, key: string): string {
  return typeof ev[key] === 'string' ? (ev[key] as string) : '';
}

function shortActor(actor: string | null | undefined): string {
  if (!actor) return '';
  const m = /^(.+?)\s*<[^>]+>$/.exec(actor);
  return m ? m[1].trim() : actor;
}

function fmtDue(dueAt: string | undefined): string {
  if (!dueAt) return '';
  const m = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::\d+)?([+-]\d{2}:\d{2}|Z)?/.exec(dueAt);
  if (!m) return dueAt;
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const month = months[parseInt(m[2]) - 1];
  const day = parseInt(m[3]);
  const h = parseInt(m[4]);
  const min = m[5];
  const ampm = h >= 12 ? 'PM' : 'AM';
  const h12 = h === 0 ? 12 : h > 12 ? h - 12 : h;
  const tzMap: Record<string, string> = { '+09:00': 'KST', '-07:00': 'PDT', '-08:00': 'PST', 'Z': 'UTC' };
  const tz = m[6] ? (tzMap[m[6]] ?? m[6]) : '';
  return `${month} ${day}, ${h12}:${min} ${ampm}${tz ? ' ' + tz : ''}`;
}

function actionFromText(text: string): string {
  const parts = text.split('. ');
  const triggers = ['must ', 'need to ', 'needs to ', 'required', 'confirm ', 'check ', 'attend ', 'decide ', 'submit ', 'delegate ', 'file '];
  for (const s of parts) {
    if (triggers.some(t => s.toLowerCase().includes(t))) {
      return s.replace(/^Josh (must|needs? to|should) /i, '').trim().slice(0, 120);
    }
  }
  return '';
}

// ── Language ───────────────────────────────────────────────────────────────
// The brief is a presentation surface. We detect the target language from the
// user's Telegram message and translate section/field labels and concise
// synthesized text only — never the raw observed private text.

type Lang = 'en' | 'ko';

function detectLang(text: string): Lang {
  if (/[가-힣]/.test(text)) return 'ko';
  if (/show in korean/i.test(text)) return 'ko';
  return 'en';
}

interface FieldLabels {
  from: string; subject: string; event: string; when: string;
  location: string; why: string; evidence: string; action: string;
  adjudication: string; channel: string;
}

interface Labels {
  lang: Lang;
  briefTitle: string;
  modeLine: (mode: string) => string;
  secNew: string; secTracked: string; secAging: string; secClosed: string;
  secReview: string; secContext: string; secSuppressed: string; secSafe: string;
  none: string;
  attend: string;
  openForDays: (n: number) => string;
  transitionLine: (from: string, to: string) => string;
  closedSuffix: string;
  escalatedSuffix: string;
  needsReviewSuffix: string;
  lowConfidence: string;
  dueLabel: (d: string) => string;
  safetyLine1: string;
  safetyLine2: string;
  suppPromo: string;
  suppNegative: string;
  field: FieldLabels;
  pReading: string;
  pLoaded: (n: number) => string;
  pAdjudicating: string;
  pFound: (
    total: number,
    opened: number,
    tracked: number,
    ctx: number,
    suppressed: number
  ) => string;
}

const EN_LABELS: Labels = {
  lang: 'en',
  briefTitle: '🛡️ WorldLoops Brief',
  modeLine: (m) => `mode: ${m}`,
  secNew: '🧭 New open loops',
  secTracked: '🔁 Already tracked open loops',
  secAging: '⏳ Aging open loops',
  secClosed: '✅ Closed since last brief',
  secReview: '⚠️ Needs review / Escalated',
  secContext: '📎 Context',
  secSuppressed: '🧹 Suppressed',
  secSafe: '✅ Safe',
  none: 'None.',
  attend: 'Attend',
  openForDays: (n) => `open for ${n} day${n === 1 ? '' : 's'}`,
  transitionLine: (f, t) => `  Transition: ${f} → ${t}`,
  closedSuffix: 'completed',
  escalatedSuffix: 'escalated',
  needsReviewSuffix: 'needs confirmation',
  lowConfidence: 'low confidence',
  dueLabel: (d) => `, due ${d}`,
  safetyLine1: 'externalWrite:false',
  safetyLine2: 'No email, draft, calendar event, Slack message, or external change made.',
  suppPromo: 'promotional / no action',
  suppNegative: 'no action required',
  field: {
    from: 'From', subject: 'Subject', event: 'Event', when: 'When',
    location: 'Location', why: 'Why', evidence: 'Evidence', action: 'Action',
    adjudication: 'Adjudication', channel: 'Channel',
  },
  pReading: 'Reading interpreted OpenClaw observations…',
  pLoaded: (n) => `Loaded ${n} interpreted candidate${n === 1 ? '' : 's'}.`,
  pAdjudicating: 'WorldLoops is adjudicating candidates…',
  pFound: (total, opened, tracked, ctx, sup) =>
    `WorldLoops adjudicated ${total} candidate${total === 1 ? '' : 's'}:\n` +
    `${opened} newly opened, ${tracked} already tracked, ${ctx} context, ${sup} suppressed.`,
};

const KO_LABELS: Labels = {
  lang: 'ko',
  briefTitle: '🛡️ WorldLoops 브리프',
  modeLine: (m) => `mode: ${m}`,
  secNew: '🧭 새로 열린 루프',
  secTracked: '🔁 이미 추적 중인 루프',
  secAging: '⏳ 오래 열려 있는 루프',
  secClosed: '✅ 지난 브리프 이후 닫힌 루프',
  secReview: '⚠️ 확인 필요 / 에스컬레이션',
  secContext: '📎 참고 컨텍스트',
  secSuppressed: '🧹 억제된 노이즈',
  secSafe: '✅ 안전 경계',
  none: '없음.',
  attend: '참석',
  openForDays: (n) => `${n}일째 열려 있음`,
  transitionLine: (f, t) => `  전환: ${f} → ${t}`,
  closedSuffix: '완료됨',
  escalatedSuffix: '에스컬레이션됨',
  needsReviewSuffix: '확인 필요',
  lowConfidence: '낮은 신뢰도',
  dueLabel: (d) => `, 마감 ${d}`,
  safetyLine1: 'externalWrite:false',
  safetyLine2: '이메일, 초안, 캘린더 일정, Slack 메시지 또는 외부 시스템을 변경하지 않았습니다.',
  suppPromo: '홍보성 / 조치 불필요',
  suppNegative: '조치 불필요',
  field: {
    from: '보낸 사람', subject: '제목', event: '일정', when: '시간',
    location: '장소', why: '이유', evidence: '근거', action: '다음 행동',
    adjudication: '판정', channel: '채널',
  },
  pReading: 'OpenClaw 해석 관측을 읽는 중입니다…',
  pLoaded: (n) => `해석된 후보 ${n}개를 불러왔습니다.`,
  pAdjudicating: 'WorldLoops가 후보를 판정하는 중입니다…',
  pFound: (total, opened, tracked, ctx, sup) =>
    `WorldLoops가 후보 ${total}개를 판정했습니다:\n` +
    `새로 열림 ${opened}개, 이미 추적 중 ${tracked}개, 컨텍스트 ${ctx}개, 억제 ${sup}개.`,
};

function getLabels(lang: Lang): Labels {
  return lang === 'ko' ? KO_LABELS : EN_LABELS;
}

// ── Stateful brief UX ────────────────────────────────────────────────────────
// WorldLoops tracks open-loop lifecycle state over time — it is not a snapshot
// summary bot. The brief persists the timestamp of the last brief so it can
// report which loops closed since the user last looked.

interface TelegramBriefState {
  lastBriefAt: string;
  safety: { externalWrite: false };
}

function getBriefStatePath(): string {
  const dir = process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
  return path.join(dir, 'telegram_brief_state.json');
}

function loadLastBriefAt(): string | null {
  const p = getBriefStatePath();
  if (!fs.existsSync(p)) return null;
  try {
    const parsed = JSON.parse(fs.readFileSync(p, 'utf8')) as Partial<TelegramBriefState>;
    return typeof parsed.lastBriefAt === 'string' ? parsed.lastBriefAt : null;
  } catch {
    return null;
  }
}

function saveLastBriefAt(at: string): void {
  const p = getBriefStatePath();
  const dir = path.dirname(p);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const state: TelegramBriefState = { lastBriefAt: at, safety: { externalWrite: false } };
  fs.writeFileSync(p, JSON.stringify(state, null, 2) + '\n', 'utf8');
}

// ── Lifecycle helpers ────────────────────────────────────────────────────────

function fmtDateShort(iso: string | null | undefined, lang: Lang): string {
  if (!iso) return '';
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
  if (!m) return '';
  const mon = parseInt(m[2], 10);
  const day = parseInt(m[3], 10);
  if (lang === 'ko') return `${mon}월 ${day}일`;
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return `${months[mon - 1]} ${day}`;
}

// Calendar-day difference (UTC). Returns -1 for an unparseable timestamp so it
// can be filtered out — we never invent an age we cannot derive.
function dayDiff(fromISO: string, now: Date): number {
  const d = new Date(fromISO);
  if (isNaN(d.getTime())) return -1;
  const a = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());
  const b = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  return Math.floor((b - a) / 86_400_000);
}

// Earliest reliable timestamp for "how long this loop has been open".
function loopFirstSeen(loop: OpenLoopState): string | null {
  const sig = loop.sourceSignals.find(s => typeof s.createdAt === 'string');
  if (sig?.createdAt) return sig.createdAt;
  if (loop.history[0]?.at) return loop.history[0].at;
  return loop.lastObservedAt ?? null;
}

interface AgingItem { loop: OpenLoopState; age: number }

function buildAgingItems(loops: OpenLoopState[], now: Date): AgingItem[] {
  const items: AgingItem[] = [];
  for (const loop of loops) {
    // Only loops that are genuinely still open and unattended. Escalated loops
    // surface in the review section; snoozed loops were deliberately deferred.
    if (loop.status !== 'todo' && loop.status !== 'doing') continue;
    const seen = loopFirstSeen(loop);
    if (!seen) continue;
    const age = dayDiff(seen, now);
    if (age >= 2) items.push({ loop, age });
  }
  return items.sort((a, b) => b.age - a.age);
}

interface ClosedItem { loop: OpenLoopState; from: string; to: string }

// Loops transitioned to done since the previous brief — or, per the spec,
// "or recently": closures within a short recent window stay visible even if a
// brief was already shown after them. The open-loop history entry is the
// transition receipt; if no such receipt exists, the loop is not shown.
const RECENT_CLOSE_WINDOW_MS = 3 * 86_400_000;

function buildClosedItems(
  loops: OpenLoopState[],
  lastBriefAt: string | null,
  now: Date
): ClosedItem[] {
  const recentMs = now.getTime() - RECENT_CLOSE_WINDOW_MS;
  const lastMs = lastBriefAt ? new Date(lastBriefAt).getTime() : NaN;
  const threshold = isNaN(lastMs) ? recentMs : Math.min(lastMs, recentMs);
  const items: ClosedItem[] = [];
  for (const loop of loops) {
    if (loop.status !== 'done') continue;
    const closeEntry = [...loop.history].reverse().find(h => h.to === 'done');
    if (!closeEntry) continue;
    const at = new Date(closeEntry.at).getTime();
    if (isNaN(at) || at <= threshold) continue;
    items.push({ loop, from: closeEntry.from ?? 'open', to: closeEntry.to });
  }
  return items;
}

function buildReviewLines(
  needsReview: AdjudicationResult[],
  loops: OpenLoopState[],
  L: Labels
): string[] {
  const lines: string[] = [];
  for (const r of needsReview) {
    const reason = r.suppressionReason === 'weak_evidence' ? ` (${L.lowConfidence})` : '';
    lines.push(`- ${r.observation.title} — ${L.needsReviewSuffix}${reason}`);
  }
  for (const loop of loops) {
    if (loop.status !== 'escalated') continue;
    const due = loop.dueAt ? L.dueLabel(fmtDateShort(loop.dueAt, L.lang)) : '';
    lines.push(`- ${loop.title} — ${L.escalatedSuffix}${due}`);
  }
  return lines;
}

function suppressionReasonLabel(reason: SuppressionReason | undefined, L: Labels): string {
  if (reason === 'promotional_or_informational') return L.suppPromo;
  if (reason === 'negative_intent_no_action') return L.suppNegative;
  if (reason === 'weak_evidence') return L.lowConfidence;
  return reason ?? (L.lang === 'ko' ? '억제됨' : 'suppressed');
}

function contextReason(obs: OpenClawObservation): string {
  const rc = obs.relatedContext;
  if (rc && typeof rc.note === 'string') {
    return rc.note.split('. ')[0].trim().slice(0, 80);
  }
  return '';
}

function buildLoopEntry(r: AdjudicationResult, adjLabel: string, L: Labels): string {
  const obs = r.observation;
  const ev = obs.evidence;
  const F = L.field;
  const emoji = srcEmoji(obs.source);
  const srcLabel = obs.source.charAt(0).toUpperCase() + obs.source.slice(1);
  const lines: string[] = [`${emoji} ${srcLabel} — ${obs.title}`];

  if (obs.source === 'gmail' || obs.source === 'email') {
    const from = shortActor(obs.actor);
    if (from) lines.push(`${F.from}: ${from}`);
    const subj = evField(ev, 'subject') || evField(ev, 'title');
    if (subj && subj !== obs.title) lines.push(`${F.subject}: ${subj}`);
    lines.push(`${F.why}: ${obs.text.split('. ')[0].slice(0, 130)}`);
    const snippet = evField(ev, 'snippet');
    if (snippet) lines.push(`${F.evidence}: ${snippet.slice(0, 100)}`);
    const action = actionFromText(obs.text);
    if (action) lines.push(`${F.action}: ${action}`);
  } else if (obs.source === 'calendar') {
    const evTitle = evField(ev, 'title');
    if (evTitle && evTitle !== obs.title) lines.push(`${F.event}: ${evTitle}`);
    const when = fmtDue(obs.dueAt) || evField(ev, 'start');
    if (when) lines.push(`${F.when}: ${when}`);
    const loc = evField(ev, 'location');
    if (loc) lines.push(`${F.location}: ${loc}`);
    lines.push(`${F.why}: ${obs.text.split('. ')[0].slice(0, 130)}`);
    const action = actionFromText(obs.text);
    lines.push(`${F.action}: ${action || L.attend}`);
  } else if (obs.source === 'slack') {
    const from = shortActor(obs.actor);
    if (from) lines.push(`${F.from}: ${from}`);
    const channel = evField(ev, 'channel');
    if (channel) lines.push(`${F.channel}: #${channel}`);
    lines.push(`${F.why}: ${obs.text.split('. ')[0].slice(0, 130)}`);
    const snippet = evField(ev, 'snippet') || evField(ev, 'message') || evField(ev, 'text');
    if (snippet) lines.push(`${F.evidence}: "${snippet.slice(0, 100)}"`);
    const action = actionFromText(obs.text);
    if (action) lines.push(`${F.action}: ${action}`);
  }

  lines.push(`${F.adjudication}: ${adjLabel}`);
  return lines.join('\n');
}

function buildContextEntry(r: AdjudicationResult): string {
  const obs = r.observation;
  const ev = obs.evidence;
  const emoji = srcEmoji(obs.source);
  const reason = contextReason(obs);
  let label: string;
  if (obs.source === 'gmail' || obs.source === 'email') {
    label = evField(ev, 'subject') || evField(ev, 'title') || obs.title;
  } else if (obs.source === 'calendar') {
    const evTitle = evField(ev, 'title') || obs.title;
    const when = fmtDue(obs.dueAt);
    label = `${evTitle}${when ? ` — ${when}` : ''}`;
  } else {
    // Slack and other sources: use the synthesized title — avoids surfacing
    // raw Slack user/channel IDs that live only in the evidence payload.
    label = obs.title;
  }
  return `${emoji} ${label}${reason ? ` — ${reason}` : ''}`;
}

function buildBriefOutput(
  summary: IntakeSummary,
  mode: string,
  L: Labels,
  loops: OpenLoopState[],
  lastBriefAt: string | null,
  now: Date
): string {
  const lines: string[] = [];
  lines.push(L.briefTitle);
  lines.push(L.modeLine(mode));

  const newLoops = summary.results.filter(r => r.verdict === 'accepted');
  const alreadyTracked = summary.results.filter(
    r => r.verdict === 'suppressed' &&
         r.suppressionReason === 'duplicate_signal' &&
         r.observation.observationIntent === 'new_loop'
  );
  const needsReview = summary.results.filter(r => r.verdict === 'needs_review');
  const contextItems = summary.results.filter(r => r.verdict === 'attached_context');
  const suppressedNoise = summary.results.filter(
    r => r.verdict === 'suppressed' && r.suppressionReason !== 'duplicate_signal'
  );

  // 1. 🧭 New open loops — observations accepted in this run. Omitted entirely
  // when nothing was newly opened, rather than shown as an empty "None."
  if (newLoops.length > 0) {
    lines.push('');
    lines.push(L.secNew);
    for (const r of newLoops) {
      lines.push('');
      lines.push(buildLoopEntry(r, 'new_loop', L));
    }
  }

  // 2. 🔁 Already tracked open loops — new_loop observations suppressed as
  // idempotent duplicates because the loop already exists in state. They stay
  // visible: WorldLoops knows the loop, it is not re-creating it.
  if (alreadyTracked.length > 0) {
    lines.push('');
    lines.push(L.secTracked);
    for (const r of alreadyTracked) {
      lines.push('');
      lines.push(buildLoopEntry(r, 'already_tracked', L));
    }
  }

  // 3. ⏳ Aging open loops — open 2+ days, by a real timestamp only.
  const aging = buildAgingItems(loops, now);
  if (aging.length > 0) {
    lines.push('');
    lines.push(L.secAging);
    for (const a of aging) {
      lines.push(`- ${a.loop.title} — ${L.openForDays(a.age)}`);
    }
  }

  // 4. ✅ Closed since last brief — backed by open-loop transition history.
  const closed = buildClosedItems(loops, lastBriefAt, now);
  if (closed.length > 0) {
    lines.push('');
    lines.push(L.secClosed);
    for (const c of closed) {
      lines.push(`- ${c.loop.title} — ${L.closedSuffix}`);
      lines.push(L.transitionLine(c.from, c.to));
    }
  }

  // 5. ⚠️ Needs review / Escalated — confirmation, low confidence, escalation.
  const reviewLines = buildReviewLines(needsReview, loops, L);
  if (reviewLines.length > 0) {
    lines.push('');
    lines.push(L.secReview);
    lines.push(...reviewLines);
  }

  // 6. 📎 Context — related_context and evidence items.
  if (contextItems.length > 0) {
    lines.push('');
    lines.push(L.secContext);
    for (const r of contextItems) {
      lines.push(`  ${buildContextEntry(r)}`);
    }
  }

  // 7. 🧹 Suppressed — noise and no-action items, kept compact.
  if (suppressedNoise.length > 0) {
    lines.push('');
    lines.push(L.secSuppressed);
    for (const r of suppressedNoise) {
      lines.push(`  - ${r.observation.title} — ${suppressionReasonLabel(r.suppressionReason, L)}`);
    }
  }

  // 8. ✅ Safe — externalWrite:false is always shown.
  lines.push('');
  lines.push(L.secSafe);
  lines.push(L.safetyLine1);
  lines.push(L.safetyLine2);

  return lines.join('\n');
}

async function handleBriefWithProgress(
  token: string,
  chatId: number,
  filePath: string,
  mode: string,
  L: Labels
): Promise<void> {
  await sendMessage(token, chatId, `${L.pReading}\nexternalWrite:false`);

  let observations;
  try {
    observations = loadObservations(filePath);
  } catch (err) {
    await sendMessage(token, chatId,
      `Error loading observations: ${String(err)}\nexternalWrite:false`
    );
    return;
  }

  await sendMessage(token, chatId, `${L.pLoaded(observations.length)}\nexternalWrite:false`);
  await sendMessage(token, chatId, `${L.pAdjudicating}\nexternalWrite:false`);

  let summary;
  try {
    summary = runIntake(observations);
  } catch (err) {
    await sendMessage(token, chatId,
      `Error running intake: ${String(err)}\nexternalWrite:false`
    );
    return;
  }

  // Adjudication breakdown — "already tracked" (idempotent new_loop duplicates)
  // is reported separately from true noise suppression.
  const trackedCount = summary.results.filter(
    r => r.verdict === 'suppressed' &&
         r.suppressionReason === 'duplicate_signal' &&
         r.observation.observationIntent === 'new_loop'
  ).length;
  const noiseSuppressedCount = summary.results.filter(
    r => r.verdict === 'suppressed' && r.suppressionReason !== 'duplicate_signal'
  ).length;
  await sendMessage(token, chatId,
    `${L.pFound(summary.total, summary.accepted, trackedCount, summary.attached_context, noiseSuppressedCount)}\n` +
    'externalWrite:false'
  );

  // Stateful brief: read full loop state and the previous brief timestamp,
  // render, then record this brief so the next one knows what closed.
  const loops = loadOpenLoopStates();
  const lastBriefAt = loadLastBriefAt();
  const now = new Date();
  await sendBrief(token, chatId, buildBriefOutput(summary, mode, L, loops, lastBriefAt, now));
  saveLastBriefAt(now.toISOString());
}

async function handleBriefCommand(token: string, chatId: number, L: Labels): Promise<void> {
  const filePath = path.resolve(process.cwd(), INTERPRETED_OBSERVATIONS);

  if (!fs.existsSync(filePath)) {
    await sendMessage(token, chatId, [
      'No interpreted OpenClaw observations found yet.',
      'Ask OpenClaw to observe first, then write surfaced candidates to .worldloops/inbox/openclaw-observations.json.',
      '',
      'To test with demo data: /demo',
      'To run raw inbox diagnostic (not recommended for user brief): /live',
      '',
      'externalWrite:false',
    ].join('\n'));
    return;
  }

  await handleBriefWithProgress(token, chatId, filePath, 'interpreted-observations', L);
}

async function handleDemoCommand(token: string, chatId: number, L: Labels): Promise<void> {
  const filePath = path.resolve(process.cwd(), DEMO_FIXTURE_PATH);

  if (!fs.existsSync(filePath)) {
    await sendMessage(token, chatId, [
      'Demo fixture not found.',
      `Expected: ${DEMO_FIXTURE_PATH}`,
      'externalWrite:false',
    ].join('\n'));
    return;
  }

  await handleBriefWithProgress(token, chatId, filePath, 'demo-fixture', L);
}

function runLiveDiagnostic(): string {
  try {
    const result = spawnSync(
      'node',
      ['dist/scripts/guardDaily.js', '--inbox', OPENCLAW_INBOX],
      { encoding: 'utf8', timeout: 30000, cwd: process.cwd() }
    );
    if (result.error) {
      return `Error running live diagnostic: ${result.error.message}`;
    }
    const output = ((result.stdout ?? '') + (result.stderr ?? '')).trim();
    return truncate(output || 'No output from live diagnostic.');
  } catch (err) {
    return `Error running live diagnostic: ${String(err)}`;
  }
}

function runSource(): string {
  const cwd = process.cwd();

  const interpretedAbs = path.resolve(cwd, INTERPRETED_OBSERVATIONS);
  const interpretedExists = fs.existsSync(interpretedAbs);

  const liveFiles = ['openclaw-gmail-live.json', 'openclaw-calendar-live.json', 'openclaw-slack-live.json'];
  const liveStatuses = liveFiles.map(f => {
    const exists = fs.existsSync(path.join(OPENCLAW_INBOX, f));
    return `  ${f}  ${exists ? 'exists' : 'not found'}`;
  });

  const demoAbs = path.resolve(cwd, DEMO_FIXTURE_PATH);
  const demoExists = fs.existsSync(demoAbs);

  const lines: string[] = [
    'WorldLoops input source check',
    '',
    'Interpreted observations (/brief):',
    `  ${INTERPRETED_OBSERVATIONS}  ${interpretedExists ? 'exists' : 'not found'}`,
    '  Written by OpenClaw after its observation pass.',
    '',
    'Raw live inbox diagnostic (/live):',
    `  ${OPENCLAW_INBOX}`,
    ...liveStatuses,
    '',
    'Demo fixture (/demo):',
    `  ${DEMO_FIXTURE_PATH}  ${demoExists ? 'exists' : 'not found'}`,
    '',
    'externalWrite:false',
  ];

  return lines.join('\n');
}

const BRIEF_TRIGGERS = [
  '/brief',
  '/worldloops',
  '오늘 내가 할 일이 뭐야',
  '뭐 빠진 거 없어',
  '어제 열린 루프 중 닫힌 거 있어',
];

function isBriefRequest(text: string): boolean {
  const lower = text.toLowerCase().trim();
  return BRIEF_TRIGGERS.some(t => lower.startsWith(t.toLowerCase()));
}

async function handleUpdate(token: string, update: Record<string, unknown>): Promise<void> {
  const message = update.message as Record<string, unknown> | undefined;
  if (!message) return;

  const chatId = (message.chat as Record<string, unknown> | undefined)?.id as number | undefined;
  const text = message.text as string | undefined;

  if (!chatId || !text) return;

  const trimmed = text.trim();
  // Language is detected from the user's own message — Korean text, or an
  // explicit "Show in Korean" / "우리말로 보여줘" request, renders in Korean.
  const labels = getLabels(detectLang(trimmed));

  if (trimmed === '/start') {
    await sendMessage(
      token,
      chatId,
      'WorldLoops Telegram demo wrapper is running.\nSend /help to see available commands.'
    );
    return;
  }

  if (trimmed === '/help') {
    await sendMessage(token, chatId, [
      'WorldLoops Telegram demo wrapper',
      '',
      'Commands:',
      '/status — bot version and status',
      '/source — show all three input paths and their status',
      '/brief — adjudicate OpenClaw interpreted observations',
      '/worldloops — same as /brief',
      '/demo — adjudicate demo fixture',
      '/live — raw inbox diagnostic, not recommended for user-facing brief',
      '',
      'externalWrite:false',
    ].join('\n'));
    return;
  }

  if (trimmed === '/status') {
    let version = 'unknown';
    try {
      const pkg = JSON.parse(
        fs.readFileSync(path.resolve(process.cwd(), 'package.json'), 'utf8')
      ) as { version?: string };
      version = pkg.version ?? 'unknown';
    } catch {
      // leave as unknown
    }
    await sendMessage(token, chatId, [
      'WorldLoops Telegram test bot: running',
      `version: ${version}`,
      'externalWrite:false',
    ].join('\n'));
    return;
  }

  if (trimmed === '/source') {
    await sendMessage(token, chatId, runSource());
    return;
  }

  if (trimmed === '/reset-demo') {
    await sendMessage(token, chatId, [
      '/reset-demo: not implemented',
      '',
      '.worldloops/ contains real user state (open loops, proposals, receipts).',
      'Deleting from this directory without isolated demo state is unsafe.',
      '',
      'To clear the demo inbox manually:',
      '  rm .worldloops/inbox/openclaw-observations.json',
      '',
      'externalWrite:false',
    ].join('\n'));
    return;
  }

  if (trimmed === '/demo') {
    await handleDemoCommand(token, chatId, labels);
    return;
  }

  if (trimmed === '/live') {
    await sendMessage(token, chatId, [
      'Raw diagnostic mode — this reads shallow live handoff payloads and may include noise.',
      'For user-facing quality, use interpreted OpenClaw observations with /brief.',
      '',
      'externalWrite:false',
    ].join('\n'));
    await sendMessage(token, chatId, runLiveDiagnostic());
    return;
  }

  if (isBriefRequest(trimmed) || !trimmed.startsWith('/')) {
    await handleBriefCommand(token, chatId, labels);
    return;
  }

  await sendMessage(
    token,
    chatId,
    "Unknown command. Send /help for available commands."
  );
}

interface TelegramUpdate {
  update_id: number;
  [key: string]: unknown;
}

interface GetUpdatesResponse {
  ok: boolean;
  result?: TelegramUpdate[];
  error_code?: number;
  description?: string;
}

async function poll(
  token: string,
  offset: number
): Promise<{ updates: TelegramUpdate[]; nextOffset: number }> {
  // timeout=30 → 35s socket timeout to give Telegram time to respond
  const response = (await telegramGet(
    token,
    'getUpdates',
    { offset, timeout: 30, allowed_updates: 'message' },
    35000
  )) as unknown as GetUpdatesResponse;

  if (!response.ok) {
    if (response.error_code === 409) {
      throw new Error(
        'Polling conflict (409): another bot process is already polling this token. Stop it first.'
      );
    }
    throw new Error(`getUpdates failed [${response.error_code ?? '?'}]: ${response.description ?? JSON.stringify(response)}`);
  }

  const updates = response.result ?? [];
  const nextOffset =
    updates.length > 0 ? updates[updates.length - 1].update_id + 1 : offset;

  return { updates, nextOffset };
}

async function main(): Promise<void> {
  let token: string;
  try {
    token = loadToken();
  } catch (err) {
    process.stderr.write(`Error: ${String(err)}\n`);
    process.exit(1);
  }

  console.log('WorldLoops Telegram demo wrapper starting...');
  console.log('Polling for messages. Send /help to your bot for available commands.');
  console.log('Press Ctrl+C to stop.\n');

  let offset = 0;

  for (;;) {
    try {
      const { updates, nextOffset } = await poll(token, offset);
      offset = nextOffset;
      for (const update of updates) {
        try {
          await handleUpdate(token, update as Record<string, unknown>);
        } catch (err) {
          process.stderr.write(`Error handling update ${update.update_id}: ${String(err)}\n`);
        }
      }
    } catch (err) {
      const msg = String(err);
      if (msg.includes('409')) {
        process.stderr.write(`Fatal: ${msg}\n`);
        process.exit(1);
      }
      process.stderr.write(`Polling error (retrying in 5s): ${msg}\n`);
      await new Promise<void>(r => setTimeout(r, 5000));
    }
  }
}

main();
