const { AppError, EXIT_CODES } = require('../errors');
const { STATUS_EMOJI } = require('./update-word');

function buildEventCounts(events) {
  const counts = {
    correct: 0,
    wrong: 0,
    remembered_after_hint: 0,
    skip: 0,
    unreviewed: 0,
  };

  for (const event of events) {
    if (Object.prototype.hasOwnProperty.call(counts, event.event)) {
      counts[event.event] += 1;
    }
  }

  return counts;
}

function compareWordSummary(a, b) {
  if (a.next_review && b.next_review && a.next_review !== b.next_review) {
    return a.next_review < b.next_review ? -1 : 1;
  }
  if (a.next_review && !b.next_review) return -1;
  if (!a.next_review && b.next_review) return 1;
  return a.word.localeCompare(b.word);
}

function summarizeWords(events, repo) {
  const latestEventByWord = new Map();
  for (const event of events) {
    latestEventByWord.set(event.word, event);
  }

  const wordList = [...latestEventByWord.keys()];
  const snapshots = repo.getWordsByList(wordList);
  const snapshotMap = new Map(snapshots.map((s) => [s.word, s]));

  const words = [];
  for (const [word, latestEvent] of latestEventByWord.entries()) {
    const snapshot = snapshotMap.get(word);
    if (!snapshot) continue;

    words.push({
      word,
      event: latestEvent.event,
      previous_status: latestEvent.previousStatus,
      next_status: latestEvent.nextStatus,
      current_status: snapshot.status,
      status_emoji: STATUS_EMOJI[snapshot.status] || null,
      first_learned: snapshot.firstLearned,
      last_reviewed: snapshot.lastReviewed,
      next_review: snapshot.nextReview,
      mastered_date: snapshot.masteredDate,
    });
  }

  return words.sort(compareWordSummary);
}

function summarizeNextReview(words) {
  const nextReviewWords = words.filter((word) => word.next_review);
  if (nextReviewWords.length === 0) {
    return {
      earliest: null,
      latest: null,
      scheduled_count: 0,
    };
  }

  return {
    earliest: nextReviewWords[0].next_review,
    latest: nextReviewWords[nextReviewWords.length - 1].next_review,
    scheduled_count: nextReviewWords.length,
  };
}

function buildSessionSummary({ repo, mode, opIds, today, topRisk = 5 }) {
  const events = repo.listEventsByOpIds(opIds);
  if (events.length === 0) {
    throw new AppError(
      'SESSION_NOT_FOUND',
      'No updater events found for the provided op-ids',
      EXIT_CODES.BUSINESS_RULE,
    );
  }

  const words = summarizeWords(events, repo);
  const eventCounts = buildEventCounts(events);
  const newWordsCount = words.filter((word) => word.first_learned === today).length;
  const reviewWordsCount = Math.max(0, words.length - newWordsCount);
  const upgradedWords = words.filter((word) => {
    const previous = Number.isInteger(word.previous_status) ? word.previous_status : 3;
    return previous < 4 && word.current_status >= 4 && word.current_status <= 7;
  });
  const masteredWords = words.filter((word) => word.current_status === 8).map((word) => word.word);
  const riskWords = words
    .filter((word) => word.current_status === 1 || word.current_status === 2)
    .slice(0, topRisk)
    .map((word) => ({
      word: word.word,
      status: word.current_status,
      status_emoji: word.status_emoji,
    }));

  return {
    total_words: words.length,
    event_counts: eventCounts,
    new_words_count: newWordsCount,
    review_words_count: reviewWordsCount,
    upgraded_words: upgradedWords.map((word) => ({
      word: word.word,
      status: word.current_status,
      status_emoji: word.status_emoji,
    })),
    mastered_words: masteredWords,
    risk_words: riskWords,
    next_review: summarizeNextReview(words),
    remaining_due_count: repo.countDueWords(today),
    words,
  };
}

module.exports = {
  buildEventCounts,
  buildSessionSummary,
  summarizeNextReview,
  summarizeWords,
};
