const { parseLocalDate } = require('../core/fsrs-scheduler');
const { addDays, toIsoDate } = require('../utils/date');

const FREQUENT_ERROR_LIMIT = 8;
const RECENTLY_CONFUSED_LIMIT = 6;

function compareDateDesc(a, b) {
  if (a === b) return 0;
  if (!a || a === 'never') return 1;
  if (!b || b === 'never') return -1;
  return a < b ? 1 : -1;
}

function compareFrequentErrorWords(a, b) {
  if (a.wrong_count_30d !== b.wrong_count_30d) {
    return b.wrong_count_30d - a.wrong_count_30d;
  }
  if (a.remembered_after_hint_count_30d !== b.remembered_after_hint_count_30d) {
    return b.remembered_after_hint_count_30d - a.remembered_after_hint_count_30d;
  }
  const aStatus = Number.isInteger(a.current_status) ? a.current_status : Number.MAX_SAFE_INTEGER;
  const bStatus = Number.isInteger(b.current_status) ? b.current_status : Number.MAX_SAFE_INTEGER;
  if (aStatus !== bStatus) {
    return aStatus - bStatus;
  }
  const dateCmp = compareDateDesc(a.last_reviewed, b.last_reviewed);
  if (dateCmp !== 0) return dateCmp;
  return a.word.localeCompare(b.word);
}

function compareRecentlyConfusedWords(a, b) {
  if (a.problematic_events_14d !== b.problematic_events_14d) {
    return b.problematic_events_14d - a.problematic_events_14d;
  }
  const aStatus = Number.isInteger(a.current_status) ? a.current_status : Number.MAX_SAFE_INTEGER;
  const bStatus = Number.isInteger(b.current_status) ? b.current_status : Number.MAX_SAFE_INTEGER;
  if (aStatus !== bStatus) {
    return aStatus - bStatus;
  }
  const dateCmp = compareDateDesc(a.last_reviewed, b.last_reviewed);
  if (dateCmp !== 0) return dateCmp;
  return a.word.localeCompare(b.word);
}

function deriveDateWindow(todayStr, days) {
  const today = parseLocalDate(todayStr);
  if (!today) {
    return { startDate: todayStr, endDate: todayStr };
  }
  return {
    startDate: toIsoDate(addDays(today, -(days - 1))),
    endDate: todayStr,
  };
}

function buildFrequentErrorWords(repo, todayStr) {
  const { startDate, endDate } = deriveDateWindow(todayStr, 30);
  return repo.listProblemWordsByDateRange(startDate, endDate)
    .map((item) => ({
      word: item.word,
      wrong_count_30d: item.wrongCount,
      remembered_after_hint_count_30d: item.rememberedAfterHintCount,
      current_status: item.currentStatus,
      last_reviewed: item.lastReviewed,
    }))
    .filter((item) => item.wrong_count_30d > 0 || item.remembered_after_hint_count_30d > 0)
    .sort(compareFrequentErrorWords)
    .slice(0, FREQUENT_ERROR_LIMIT);
}

function buildRecentlyConfusedWords(repo, todayStr) {
  const { startDate, endDate } = deriveDateWindow(todayStr, 14);
  return repo.listProblemWordsByDateRange(startDate, endDate)
    .map((item) => ({
      word: item.word,
      problematic_events_14d: item.problematicCount,
      current_status: item.currentStatus,
      last_reviewed: item.lastReviewed,
    }))
    .filter((item) => item.problematic_events_14d >= 2)
    .sort(compareRecentlyConfusedWords)
    .slice(0, RECENTLY_CONFUSED_LIMIT);
}

function buildLearnerMemory({ repo, today, memoryDigest }) {
  return {
    generated_on: today,
    learning_performance: {
      frequent_error_words: buildFrequentErrorWords(repo, today),
      recently_confused_words: buildRecentlyConfusedWords(repo, today),
    },
    personal_context: {
      recent_context_digest: Array.isArray(memoryDigest)
        ? memoryDigest.map((entry) => ({
          date: entry.date,
          points: Array.isArray(entry.points) ? entry.points.slice() : [],
        }))
        : [],
    },
  };
}

module.exports = {
  buildFrequentErrorWords,
  buildLearnerMemory,
  buildRecentlyConfusedWords,
  deriveDateWindow,
};
