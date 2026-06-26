const { AppError, EXIT_CODES } = require('../errors');
const {
  DEFAULT_RETENTION,
  computeLegacyNextReview,
  formatLocalDate,
  isValidDate,
  parseLocalDate,
  scheduleFromReview,
  scheduleUnreviewed,
} = require('../core/fsrs-scheduler');
const {
  deriveOpId,
  resolveStatusFromEvent,
  validateEventTransition,
} = require('../core/input-guard');

const NEW_WORD_STATUS = 3;

const STATUS_EMOJI = {
  1: '❌❌❌',
  2: '❌❌',
  3: '❌',
  4: '✅',
  5: '✅✅',
  6: '✅✅✅',
  7: '✅✅✅✅',
  8: '⭐',
};

function normalizeSrsState(raw, fallback) {
  if (raw === 'new' || raw === 'learning' || raw === 'review' || raw === 'relearning') {
    return raw;
  }
  return fallback;
}

function toFixedNumber(raw, digits) {
  const n = Number(raw);
  if (!Number.isFinite(n)) return null;
  return Number(n.toFixed(digits));
}

function pickPersistedDue(entry, fallbackStatus) {
  if (entry && entry.srs && typeof entry.srs === 'object' && isValidDate(entry.srs.due, false)) {
    return entry.srs.due;
  }
  if (entry && isValidDate(entry.nextReview, false)) {
    return entry.nextReview;
  }
  return computeLegacyNextReview(fallbackStatus);
}

function buildInitialLegacyEntry(previousStatus, reviewDateStr) {
  const reviewDate = parseLocalDate(reviewDateStr) || new Date();
  const status = Number.isInteger(previousStatus) ? previousStatus : NEW_WORD_STATUS;
  return {
    status,
    'last-reviewed': 'never',
    'next-review': computeLegacyNextReview(status, reviewDate),
  };
}

function normalizePersistedSrs(rawSrs, status, due) {
  const fallbackStability = status === 8 ? 36500 : 2.3;
  const fallbackDifficulty = status === 8 ? 1 : 7.1;
  const fallbackState = status === 8 ? 'review' : 'new';
  const stability = toFixedNumber(rawSrs && rawSrs.stability, 4);
  const difficulty = toFixedNumber(rawSrs && rawSrs.difficulty, 4);
  const reps = Number.isFinite(Number(rawSrs && rawSrs.reps))
    ? Math.max(0, Math.floor(Number(rawSrs.reps)))
    : 0;
  const lapses = Number.isFinite(Number(rawSrs && rawSrs.lapses))
    ? Math.max(0, Math.floor(Number(rawSrs.lapses)))
    : 0;

  return {
    due: status === 8
      ? null
      : (isValidDate(due, false) ? due : computeLegacyNextReview(status)),
    stability: stability !== null && stability > 0 ? stability : fallbackStability,
    difficulty: difficulty !== null && difficulty >= 1 && difficulty <= 10 ? difficulty : fallbackDifficulty,
    reps,
    lapses,
    state: normalizeSrsState(rawSrs && rawSrs.state, fallbackState),
  };
}

function computeSchedule(params) {
  const {
    existing,
    previousStatus,
    status,
    reviewEvent,
    lastReviewed,
  } = params;

  let due = status === 8 ? null : computeLegacyNextReview(status);
  let rawSrs = existing && existing.srs && typeof existing.srs === 'object' ? existing.srs : null;

  if (status === 8) {
    if (reviewEvent === 'correct' && lastReviewed !== 'never') {
      const scheduled = scheduleFromReview({
        existingSrs: existing && existing.srs,
        legacyEntry: existing
          ? {
            status: existing.status,
            'last-reviewed': existing.lastReviewed,
            'next-review': pickPersistedDue(existing, previousStatus ?? 7),
          }
          : buildInitialLegacyEntry(previousStatus ?? 7, lastReviewed),
        reviewDateStr: lastReviewed,
        event: 'correct',
        desiredRetention: DEFAULT_RETENTION,
      });
      rawSrs = { ...scheduled.srs, due: null, state: 'review' };
    } else {
      rawSrs = {
        due: null,
        stability: rawSrs && Number.isFinite(rawSrs.stability) ? rawSrs.stability : 36500,
        difficulty: rawSrs && Number.isFinite(rawSrs.difficulty) ? rawSrs.difficulty : 1,
        reps: rawSrs && Number.isFinite(rawSrs.reps) ? rawSrs.reps : 0,
        lapses: rawSrs && Number.isFinite(rawSrs.lapses) ? rawSrs.lapses : 0,
        state: 'review',
      };
    }
  } else if (reviewEvent === 'unreviewed') {
    const reviewDate = parseLocalDate(lastReviewed) || new Date();
    const scheduled = scheduleUnreviewed(status, reviewDate);
    due = scheduled.nextReview;
    rawSrs = scheduled.srs;
  } else {
    const scheduled = scheduleFromReview({
      existingSrs: existing && existing.srs,
      legacyEntry: existing
        ? {
          status: existing.status,
          'last-reviewed': existing.lastReviewed,
          'next-review': pickPersistedDue(existing, existing.status),
        }
        : buildInitialLegacyEntry(previousStatus, lastReviewed),
      reviewDateStr: lastReviewed,
      event: reviewEvent,
      desiredRetention: DEFAULT_RETENTION,
    });
    due = scheduled.nextReview;
    rawSrs = scheduled.srs;
  }

  const srs = normalizePersistedSrs(rawSrs, status, due);
  return { due: srs.due, srs };
}

function toResultPayload(input) {
  const {
    result,
    word,
    status,
    previousStatus,
    firstLearned,
    lastReviewed,
    masteredDate,
    nextReview,
    reviewEvent,
    opId,
    srs,
    createdAt,
    updatedAt,
    todayCount,
  } = input;

  return {
    result,
    word,
    status,
    status_emoji: STATUS_EMOJI[status],
    today_count: todayCount ?? null,
    previous_status: previousStatus,
    first_learned: firstLearned,
    last_reviewed: lastReviewed,
    mastered_date: masteredDate,
    next_review: nextReview,
    review_event: reviewEvent,
    op_id: opId,
    retention: DEFAULT_RETENTION,
    srs: srs ? {
      due: srs.due ?? null,
      stability: srs.stability ?? null,
      difficulty: srs.difficulty ?? null,
      reps: srs.reps ?? null,
      lapses: srs.lapses ?? null,
      state: srs.state ?? null,
    } : null,
    created_at: createdAt,
    updated_at: updatedAt,
  };
}

function formatUpdateText(result) {
  if (result.result === 'idempotent') {
    return `[Idempotent] '${result.word}' already applied | op-id: ${result.op_id}`;
  }

  if (result.result === 'archived') {
    return `[Archived] '${result.word}' → ⭐ | event: ${result.review_event} | op-id: ${result.op_id}`;
  }

  return `[Success] '${result.word}' → ${result.status} (${result.status_emoji}) | event: ${result.review_event} | next-review: ${result.next_review} | retention: ${result.retention} | op-id: ${result.op_id}`;
}

function updateWord({ repo, input }) {
  const {
    word,
    statusArg,
    firstLearnedArg,
    lastReviewed,
    eventArg,
    opIdArg,
  } = input;

  const payloadInput = repo.transaction(() => {
    const existing = repo.getWord(word);
    const pending = repo.getPendingWord(word);
    const firstLearned = pending
      ? lastReviewed
      : (
        firstLearnedArg
        || (existing && isValidDate(existing.firstLearned, false) ? existing.firstLearned : lastReviewed)
        || formatLocalDate()
      );
    const previousStatus = existing && Number.isInteger(existing.status)
      ? existing.status
      : (pending ? NEW_WORD_STATUS : null);
    const reviewEvent = eventArg;
    let status = null;

    try {
      status = resolveStatusFromEvent(previousStatus, reviewEvent, NEW_WORD_STATUS);
    } catch (error) {
      throw new AppError(
        'INVALID_TRANSITION',
        `invalid event/status transition: ${error.message}`,
        EXIT_CODES.BUSINESS_RULE,
      );
    }

    if (statusArg !== null && statusArg !== status) {
      throw new AppError(
        'STATUS_MISMATCH',
        `provided --status ${statusArg} does not match computed status ${status} for event "${reviewEvent}"`,
        EXIT_CODES.BUSINESS_RULE,
      );
    }

    try {
      validateEventTransition({
        previousStatus,
        nextStatus: status,
        event: reviewEvent,
        lastReviewed,
      });
    } catch (error) {
      throw new AppError(
        'INVALID_TRANSITION',
        `invalid event/status transition: ${error.message}`,
        EXIT_CODES.BUSINESS_RULE,
      );
    }

    const computedOpId = deriveOpId(`${word}|${status}|${firstLearned}|${lastReviewed}|${reviewEvent}`);
    const opId = opIdArg || computedOpId;
    const existingEvent = repo.findEventByOpId(opId);
    if (existingEvent) {
      if (existingEvent.word !== word) {
        throw new AppError(
          'OP_ID_CONFLICT',
          `op-id "${opId}" already exists for word "${existingEvent.word}"`,
          EXIT_CODES.BUSINESS_RULE,
        );
      }
      const snapshot = repo.getWord(word) || existing;
      return {
        result: 'idempotent',
        word,
        status: snapshot ? snapshot.status : status,
        previousStatus,
        firstLearned: snapshot ? snapshot.firstLearned : firstLearned,
        lastReviewed: snapshot ? snapshot.lastReviewed : lastReviewed,
        masteredDate: snapshot ? snapshot.masteredDate : null,
        nextReview: snapshot ? snapshot.nextReview : null,
        reviewEvent,
        opId,
        srs: snapshot ? snapshot.srs : null,
        createdAt: snapshot ? snapshot.createdAt : null,
        updatedAt: snapshot ? snapshot.updatedAt : null,
      };
    }

    const { due, srs } = computeSchedule({
      existing,
      previousStatus,
      status,
      reviewEvent,
      lastReviewed,
    });
    const now = new Date().toISOString();
    const studyDate = lastReviewed;
    const masteredDate = status === 8 ? studyDate : null;
    const nextReview = status === 8 ? null : due;
    const createdAt = existing ? existing.createdAt : now;

    if (pending) {
      repo.deletePendingWord(word);
    }
    repo.saveWord({
      word,
      status,
      firstLearned,
      lastReviewed,
      nextReview,
      masteredDate,
      lastOpId: opId,
      srs,
      createdAt,
      updatedAt: now,
    });
    repo.insertEvent({
      opId,
      word,
      event: reviewEvent,
      previousStatus,
      nextStatus: status,
      studyDate,
      resultDue: nextReview,
      resultSrsState: srs.state,
      createdAt: now,
    });
    return {
      result: status === 8 ? 'archived' : 'success',
      word,
      status,
      previousStatus,
      firstLearned,
      lastReviewed,
      masteredDate,
      nextReview,
      reviewEvent,
      opId,
      srs,
      createdAt,
      updatedAt: now,
    };
  });

  return toResultPayload({
    ...payloadInput,
    todayCount: repo.countDistinctReviewedWordsOn(payloadInput.lastReviewed),
  });
}

module.exports = {
  DEFAULT_RETENTION,
  STATUS_EMOJI,
  computeSchedule,
  formatUpdateText,
  normalizePersistedSrs,
  updateWord,
};
