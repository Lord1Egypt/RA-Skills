const { addDays, daysBetween } = require('../utils/date');
const { AppError, EXIT_CODES } = require('../errors');

const DEFAULT_RETENTION = 0.9;
const DECAY = -0.5;
const FACTOR = Math.pow(0.9, 1 / DECAY) - 1;

// FSRS-6 default weights from the public algorithm reference.
const DEFAULT_WEIGHTS = [
  0.2120, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334,
  3.0194, 0.0010, 1.8722, 0.1666, 0.7960, 1.4835,
  0.0614, 0.2629, 1.6483, 0.6014, 1.8729,
];

const LEGACY_DAYS = {
  1: 1, 2: 1, 3: 1,
  4: 3, 5: 5, 6: 10, 7: 30,
};

const EVENT_TO_GRADE = {
  wrong: 1,
  remembered_after_hint: 2,
  correct: 3,
};

const STATUS_STABILITY_FALLBACK = {
  1: 0.5,
  2: 0.9,
  3: 1.4,
  4: 3.4,
  5: 5.6,
  6: 9.5,
  7: 16.0,
};

const STATUS_DIFFICULTY_FALLBACK = {
  1: 9.4,
  2: 8.8,
  3: 8.0,
  4: 6.0,
  5: 5.0,
  6: 4.0,
  7: 3.4,
};

function clamp(v, min, max) {
  return Math.min(max, Math.max(min, v));
}

function formatLocalDate(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function parseLocalDateParts(s) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
  if (!match) return null;
  return {
    y: Number(match[1]),
    mo: Number(match[2]),
    d: Number(match[3]),
  };
}

function parseLocalDate(s) {
  const parts = parseLocalDateParts(s);
  if (!parts) return null;
  const date = new Date(parts.y, parts.mo - 1, parts.d);
  if (
    date.getFullYear() !== parts.y
    || date.getMonth() !== parts.mo - 1
    || date.getDate() !== parts.d
  ) return null;
  return date;
}

function isValidDate(s, allowNever = false) {
  if (allowNever && s === 'never') return true;
  return !!parseLocalDate(s);
}

function computeLegacyNextReview(status, baseDate = new Date()) {
  if (status === 8) return '9999-12-31';
  const days = LEGACY_DAYS[status];
  const due = addDays(baseDate, Number.isFinite(days) ? days : 1);
  return formatLocalDate(due);
}

function nextIntervalDays(stability, desiredRetention = DEFAULT_RETENTION) {
  const dr = clamp(desiredRetention, 0.7, 0.97);
  const raw = (stability / FACTOR) * (Math.pow(dr, 1 / DECAY) - 1);
  return Math.max(1, Math.round(raw));
}

function forgettingCurve(elapsedDays, stability) {
  const s = Math.max(0.1, stability);
  const t = Math.max(0, elapsedDays);
  return Math.pow(1 + (FACTOR * t) / s, DECAY);
}

function initDifficulty(grade, weights) {
  const raw = weights[4] - Math.exp(weights[5] * (grade - 1)) + 1;
  return clamp(raw, 1, 10);
}

function computeNextDifficulty(previousDifficulty, grade, weights) {
  const delta = -weights[6] * (grade - 3);
  const adjusted = clamp(previousDifficulty + delta, 1, 10);
  const meanAnchor = initDifficulty(3, weights);
  const reverted = weights[7] * meanAnchor + (1 - weights[7]) * adjusted;
  return clamp(reverted, 1, 10);
}

function initStability(grade, weights) {
  return Math.max(0.1, weights[grade - 1] || weights[2]);
}

function nextRecallStability(stability, difficulty, retrievability, grade, weights) {
  const hardPenalty = grade === 2 ? weights[15] : 1;
  const shortTermPenalty = stability < weights[16] ? weights[16] : 1;
  const growth = Math.exp(weights[8])
    * (11 - difficulty)
    * Math.pow(stability, -weights[9])
    * (Math.exp(weights[10] * (1 - retrievability)) - 1)
    * hardPenalty
    * shortTermPenalty;
  return Math.max(0.1, stability * (1 + growth));
}

function nextForgetStability(stability, difficulty, retrievability, weights) {
  const next = weights[11]
    * Math.pow(difficulty, -weights[12])
    * (Math.pow(stability + 1, weights[13]) - 1)
    * Math.exp(weights[14] * (1 - retrievability));
  return Math.max(0.1, next);
}

function inferEventFromTransition(prevStatus, nextStatus, lastReviewed) {
  if (nextStatus === 8) {
    if (prevStatus === 7 && lastReviewed !== 'never') return 'correct';
    return 'skip';
  }
  if (lastReviewed === 'never') return 'unreviewed';
  if (typeof prevStatus !== 'number') return 'correct';
  if (nextStatus > prevStatus) return 'correct';
  if (nextStatus < prevStatus) return 'wrong';
  return 'correct';
}

function eventToGrade(event) {
  return EVENT_TO_GRADE[event] || null;
}

function normalizeState(state) {
  if (state === 'new' || state === 'learning' || state === 'review' || state === 'relearning') {
    return state;
  }
  return 'review';
}

function bootstrapSrsFromLegacy(entry, reviewDate) {
  const status = Number.isInteger(entry.status) ? entry.status : 3;
  const nextReview = parseLocalDate(entry['next-review']);
  const lastReviewedRaw = entry['last-reviewed'];
  const lastReviewed = parseLocalDate(lastReviewedRaw);

  let stability = STATUS_STABILITY_FALLBACK[status] || 1.4;
  if (nextReview && lastReviewed) {
    stability = Math.max(0.1, daysBetween(lastReviewed, nextReview));
  }

  return {
    due: nextReview ? formatLocalDate(nextReview) : computeLegacyNextReview(status, reviewDate),
    stability: Number(stability.toFixed(4)),
    difficulty: Number((STATUS_DIFFICULTY_FALLBACK[status] || 8.0).toFixed(4)),
    reps: 0,
    lapses: 0,
    state: lastReviewedRaw === 'never' ? 'new' : 'review',
    lastReview: lastReviewed ? formatLocalDate(lastReviewed) : null,
  };
}

function normalizeSrs(existingSrs, legacyEntry, reviewDate) {
  if (!legacyEntry || typeof legacyEntry !== 'object') {
    legacyEntry = {};
  }
  if (!existingSrs || typeof existingSrs !== 'object') {
    return bootstrapSrsFromLegacy(legacyEntry, reviewDate);
  }

  const legacyLastReviewed = isValidDate(legacyEntry['last-reviewed'], false)
    ? legacyEntry['last-reviewed']
    : null;
  const srsLastReviewed = isValidDate(existingSrs.last_review, false)
    ? existingSrs.last_review
    : null;
  const lastReview = legacyLastReviewed || srsLastReviewed;

  return {
    due: isValidDate(existingSrs.due) ? existingSrs.due : computeLegacyNextReview(legacyEntry.status, reviewDate),
    stability: Math.max(0.1, Number(existingSrs.stability) || STATUS_STABILITY_FALLBACK[legacyEntry.status] || 1.4),
    difficulty: clamp(Number(existingSrs.difficulty) || STATUS_DIFFICULTY_FALLBACK[legacyEntry.status] || 8.0, 1, 10),
    reps: Math.max(0, Math.floor(Number(existingSrs.reps) || 0)),
    lapses: Math.max(0, Math.floor(Number(existingSrs.lapses) || 0)),
    state: normalizeState(existingSrs.state),
    lastReview,
  };
}

function scheduleFromReview(input) {
  const {
    existingSrs,
    legacyEntry,
    reviewDateStr,
    event,
    desiredRetention = DEFAULT_RETENTION,
    weights = DEFAULT_WEIGHTS,
  } = input;

  const reviewDate = parseLocalDate(reviewDateStr);
  if (!reviewDate) {
    throw new AppError('INVALID_DATE', 'invalid review date', EXIT_CODES.INVALID_INPUT);
  }

  const card = normalizeSrs(existingSrs, legacyEntry, reviewDate);
  const grade = eventToGrade(event);
  if (!grade) {
    throw new AppError('INVALID_EVENT', `unsupported review event: ${String(event)}`, EXIT_CODES.INVALID_INPUT);
  }

  let retrievability = 1;
  if (card.lastReview) {
    const prev = parseLocalDate(card.lastReview);
    if (prev) {
      const elapsed = Math.max(0, daysBetween(prev, reviewDate));
      retrievability = forgettingCurve(elapsed, card.stability);
    }
  }

  const nextStability = card.lastReview
    ? (grade === 1
      ? nextForgetStability(card.stability, card.difficulty, retrievability, weights)
      : nextRecallStability(card.stability, card.difficulty, retrievability, grade, weights))
    : initStability(grade, weights);
  const updatedDifficulty = computeNextDifficulty(card.difficulty, grade, weights);
  const nextReps = card.reps + 1;
  const nextLapses = card.lapses + (grade === 1 ? 1 : 0);
  let nextState = card.state;

  if (grade === 1) {
    nextState = 'relearning';
  } else if (grade === 2) {
    nextState = card.state === 'review' ? 'review' : 'learning';
  } else {
    nextState = 'review';
  }

  const intervalDays = grade === 1 ? 1 : nextIntervalDays(nextStability, desiredRetention);
  const dueDate = formatLocalDate(addDays(reviewDate, intervalDays));

  return {
    nextReview: dueDate,
    srs: {
      due: dueDate,
      stability: Number(nextStability.toFixed(4)),
      difficulty: Number(updatedDifficulty.toFixed(4)),
      reps: nextReps,
      lapses: nextLapses,
      state: nextState,
    },
  };
}

function scheduleUnreviewed(status, today = new Date()) {
  return {
    nextReview: computeLegacyNextReview(status, today),
    srs: {
      due: computeLegacyNextReview(status, today),
      stability: Number((STATUS_STABILITY_FALLBACK[status] || 1.4).toFixed(4)),
      difficulty: Number((STATUS_DIFFICULTY_FALLBACK[status] || 8.0).toFixed(4)),
      reps: 0,
      lapses: 0,
      state: 'new',
    },
  };
}

function estimateRetrievability(stability, elapsedDays) {
  const s = Math.max(0.1, Number(stability) || 0.1);
  const t = Math.max(0, Number(elapsedDays) || 0);
  const r = forgettingCurve(t, s);
  return clamp(r, 0, 1);
}

function buildBackfillSrsFromLegacy(entry, opts = {}) {
  const today = opts.today instanceof Date ? opts.today : new Date();
  const status = Number.isInteger(entry && entry.status) ? entry.status : 3;
  const legacyNext = entry && isValidDate(entry['next-review']) ? entry['next-review'] : null;
  const legacyLast = entry && isValidDate(entry['last-reviewed']) ? entry['last-reviewed'] : null;
  const due = status === 8
    ? '9999-12-31'
    : (legacyNext || computeLegacyNextReview(status, today));

  if (status === 8) {
    return {
      due: '9999-12-31',
      stability: 36500,
      difficulty: 1,
      reps: legacyLast ? 1 : 0,
      lapses: 0,
      state: 'review',
    };
  }

  let stability = STATUS_STABILITY_FALLBACK[status] || 1.4;
  if (legacyNext && legacyLast) {
    const d1 = parseLocalDate(legacyLast);
    const d2 = parseLocalDate(legacyNext);
    if (d1 && d2) {
      stability = Math.max(0.1, daysBetween(d1, d2));
    }
  }

  const difficulty = STATUS_DIFFICULTY_FALLBACK[status] || 8.0;
  const hasReview = !!legacyLast;

  return {
    due,
    stability: Number(stability.toFixed(4)),
    difficulty: Number(difficulty.toFixed(4)),
    reps: hasReview ? 1 : 0,
    lapses: hasReview && status <= 3 ? 1 : 0,
    state: status === 8 ? 'review' : (entry && entry['last-reviewed'] === 'never' ? 'new' : 'review'),
  };
}

module.exports = {
  DEFAULT_RETENTION,
  formatLocalDate,
  parseLocalDateParts,
  parseLocalDate,
  isValidDate,
  computeLegacyNextReview,
  buildBackfillSrsFromLegacy,
  estimateRetrievability,
  inferEventFromTransition,
  eventToGrade,
  scheduleFromReview,
  scheduleUnreviewed,
};
