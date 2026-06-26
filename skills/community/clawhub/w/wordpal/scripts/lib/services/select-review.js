const { estimateRetrievability, parseLocalDate } = require('../core/fsrs-scheduler');
const { daysBetween } = require('../utils/date');

function pickSrsView(srs) {
  if (!srs || typeof srs !== 'object') return null;
  return {
    due: srs.due ?? null,
    stability: srs.stability ?? null,
    difficulty: srs.difficulty ?? null,
    reps: srs.reps ?? null,
    lapses: srs.lapses ?? null,
    state: srs.state ?? null,
  };
}

function summarizeDiagnostics(entry, today) {
  const todayDate = parseLocalDate(today);
  const dueDate = parseLocalDate(entry.nextReview);
  let overdueDays = null;
  if (todayDate && dueDate) {
    overdueDays = Math.max(0, daysBetween(dueDate, todayDate));
  }

  let retrievability = null;
  if (entry.srs && typeof entry.srs === 'object') {
    const stability = Number(entry.srs.stability);
    const lastReview = parseLocalDate(entry.lastReviewed);
    if (Number.isFinite(stability) && stability > 0 && todayDate && lastReview) {
      const elapsed = Math.max(0, daysBetween(lastReview, todayDate));
      retrievability = Number(estimateRetrievability(stability, elapsed).toFixed(4));
    }
  }

  return {
    has_srs: !!(entry.srs && typeof entry.srs === 'object'),
    srs_due_matches_next_review: !!(
      entry.srs
      && entry.srs.due
      && entry.nextReview
      && entry.srs.due === entry.nextReview
    ),
    overdue_days: overdueDays,
    estimated_retrievability: retrievability,
  };
}

function toReviewItem(entry, today, diagnostics) {
  const item = {
    word: entry.word,
    status: entry.status,
    first_learned: entry.firstLearned,
    last_reviewed: entry.lastReviewed,
    next_review: entry.nextReview,
  };

  if (diagnostics) {
    item.srs = pickSrsView(entry.srs);
    item.diagnostics = summarizeDiagnostics(entry, today);
  }

  return item;
}

function buildSelectReview({ repo, today, diagnostics = false }) {
  return {
    items: repo.listDueWords(today).map((entry) => toReviewItem(entry, today, diagnostics)),
  };
}

module.exports = {
  buildSelectReview,
  pickSrsView,
  summarizeDiagnostics,
};
