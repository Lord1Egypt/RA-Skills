const {
  estimateRetrievability,
  formatLocalDate,
  parseLocalDate,
} = require('../core/fsrs-scheduler');
const { addDays, daysBetween } = require('../utils/date');

const STATUS_WEIGHT = {
  1: 5,
  2: 4,
  3: 3,
  4: 0,
  5: 0,
  6: 0,
  7: 0,
};

function round4(n) {
  return Number(Number(n).toFixed(4));
}

function dateRange(endDateStr, days) {
  const end = parseLocalDate(endDateStr);
  if (!end) return [];

  const out = [];
  for (let i = days - 1; i >= 0; i -= 1) {
    out.push(formatLocalDate(addDays(end, -i)));
  }
  return out;
}

function forwardDateRange(startDateStr, days) {
  const start = parseLocalDate(startDateStr);
  if (!start) return [];

  const out = [];
  for (let i = 0; i < days; i += 1) {
    out.push(formatLocalDate(addDays(start, i)));
  }
  return out;
}

function normalizeStatusCounts(rawCounts) {
  const counts = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
  };

  for (const [status, count] of Object.entries(rawCounts || {})) {
    if (Object.prototype.hasOwnProperty.call(counts, status)) {
      counts[status] = Number(count) || 0;
    }
  }

  return counts;
}

function computeRiskRows(candidateEntries, todayStr) {
  const today = parseLocalDate(todayStr);
  if (!today) return [];

  const rows = [];
  for (const entry of candidateEntries) {
    if (entry.lastReviewed === 'never' || !entry.nextReview) continue;
    const dueDate = parseLocalDate(entry.nextReview);
    if (!dueDate) continue;

    const overdueDays = Number.isInteger(entry.overdueDays)
      ? entry.overdueDays
      : Math.max(0, daysBetween(dueDate, today));
    const srs = entry.srs || {};
    const stability = Number.isFinite(srs.stability) ? Number(srs.stability) : null;
    const difficulty = Number.isFinite(srs.difficulty) ? Number(srs.difficulty) : null;
    const lapses = Number.isInteger(srs.lapses) ? srs.lapses : 0;
    const reps = Number.isInteger(srs.reps) ? srs.reps : 0;
    const lastReviewDate = parseLocalDate(entry.lastReviewed);
    let estimatedRetrievability = null;
    if (stability && stability > 0 && lastReviewDate) {
      const elapsed = Math.max(0, daysBetween(lastReviewDate, today));
      estimatedRetrievability = round4(estimateRetrievability(stability, elapsed));
    }

    const retrievabilityForScore = estimatedRetrievability === null ? 1 : estimatedRetrievability;
    const statusWeight = STATUS_WEIGHT[entry.status] || 0;
    const riskScore = round4(
      overdueDays * 2
      + (1 - retrievabilityForScore) * 10
      + statusWeight
      + lapses * 0.5
    );
    let riskLevel = 'low';
    if (riskScore >= 12) riskLevel = 'high';
    else if (riskScore >= 7) riskLevel = 'medium';

    rows.push({
      word: entry.word,
      status: entry.status,
      overdue_days: overdueDays,
      estimated_retrievability: estimatedRetrievability,
      lapses,
      reps,
      stability,
      difficulty,
      risk_score: riskScore,
      risk_level: riskLevel,
    });
  }

  rows.sort((a, b) => {
    if (b.risk_score !== a.risk_score) return b.risk_score - a.risk_score;
    if (b.overdue_days !== a.overdue_days) return b.overdue_days - a.overdue_days;
    if (a.status !== b.status) return a.status - b.status;
    return a.word.localeCompare(b.word);
  });

  return rows;
}

function mapCountsToDates(rows, dates) {
  const counts = Object.create(null);
  for (const date of dates) {
    counts[date] = 0;
  }
  for (const row of rows) {
    if (Object.prototype.hasOwnProperty.call(counts, row.date)) {
      counts[row.date] = Number(row.count) || 0;
    }
  }
  return dates.map((date) => ({
    date,
    count: counts[date],
  }));
}

function calcDue({ todayStr, days, todayDue, dueByDateRows, earliestDueDate }) {
  const today = parseLocalDate(todayStr);
  const horizonDates = forwardDateRange(todayStr, days);
  const nextDaysDueByDate = mapCountsToDates(dueByDateRows, horizonDates);
  const nextDaysDueTotal = nextDaysDueByDate.reduce((sum, item) => sum + item.count, 0);

  return {
    today_due: todayDue,
    next_days_due_total: nextDaysDueTotal,
    next_days_due_by_date: nextDaysDueByDate,
    earliest_due_date: earliestDueDate,
    today: today ? formatLocalDate(today) : todayStr,
  };
}

function buildNextAction({ todayDue, totalWords }) {
  if (todayDue > 0) {
    return {
      kind: 'learn_now',
      reason: 'today_due>0',
    };
  }

  if (totalWords > 0) {
    return {
      kind: 'learn_now',
      reason: 'total_words>0_and_today_due=0',
    };
  }

  return {
    kind: 'light_encouragement',
    reason: 'no_records_or_no_due',
  };
}

function buildReportStats({ repo, today, days, topRisk }) {
  const counts = normalizeStatusCounts(repo.countWordsByStatus());
  const pendingCount = repo.countPendingWords();
  const totalWords = Object.values(counts).reduce((sum, count) => sum + count, 0);
  const masteredWords = counts[8];
  const activeWords = totalWords - masteredWords;
  const horizonDates = forwardDateRange(today, days);
  const horizonEnd = horizonDates.length > 0 ? horizonDates[horizonDates.length - 1] : today;
  const todayDue = repo.countDueWords(today);
  const due = calcDue({
    todayStr: today,
    days,
    todayDue,
    dueByDateRows: repo.countDueByDateRange(today, horizonEnd),
    earliestDueDate: repo.getEarliestDueDate(),
  });
  const trendDates = dateRange(today, days);
  const trendNew = repo.countNewWordsByDates(trendDates);
  const trendReviewed = repo.countReviewedWordsByDates(trendDates);
  const riskCandidates = repo.listRiskWords(today, Math.max(topRisk * 10, 50));
  const riskRows = computeRiskRows(riskCandidates, today).slice(0, topRisk);
  const nextAction = buildNextAction({
    todayDue: due.today_due,
    totalWords,
  });

  return {
    warnings: {
      count: 0,
      samples: [],
    },
    totals: {
      total_words: totalWords,
      active_words: activeWords,
      mastered_words: masteredWords,
      pending_words: pendingCount,
      consolidating_words: counts[4] + counts[5] + counts[6] + counts[7],
      mastered_ratio: totalWords > 0 ? round4(masteredWords / totalWords) : 0,
      consolidating_ratio: totalWords > 0
        ? round4((counts[4] + counts[5] + counts[6] + counts[7]) / totalWords)
        : 0,
      status_counts: counts,
      learned_counts: {
        status_4_to_7: counts[4] + counts[5] + counts[6] + counts[7],
        status_1_to_3: counts[1] + counts[2] + counts[3],
      },
    },
    due,
    trend_7d: {
      days,
      new_words_by_date: trendNew,
      reviewed_words_by_date: trendReviewed,
      total_new_words: trendNew.reduce((sum, row) => sum + row.count, 0),
      total_reviewed_words: trendReviewed.reduce((sum, row) => sum + row.count, 0),
    },
    risk_words: riskRows,
    next_action: nextAction,
  };
}

module.exports = {
  buildNextAction,
  buildReportStats,
  calcDue,
  computeRiskRows,
  dateRange,
  forwardDateRange,
  mapCountsToDates,
  normalizeStatusCounts,
  round4,
};
