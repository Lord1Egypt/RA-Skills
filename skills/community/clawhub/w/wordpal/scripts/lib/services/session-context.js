const fs = require('fs');
const path = require('path');

const { parseLocalDate } = require('../core/fsrs-scheduler');
const { addDays, toIsoDate } = require('../utils/date');
const { DEFAULT_PROFILE } = require('./user-profile');
const { buildLearnerMemory } = require('./learner-memory');


function extractPoints(raw, limit = 3) {
  const lines = raw.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const out = [];

  for (const line of lines) {
    if (line.startsWith('#')) continue;
    const cleaned = line
      .replace(/^[-*]\s+/, '')
      .replace(/^\d+\.\s+/, '')
      .trim();
    if (!cleaned || cleaned.length < 4) continue;
    out.push(cleaned.slice(0, 120));
    if (out.length >= limit) break;
  }

  return out;
}

function buildMemoryDigest(todayStr, memoryDir) {
  const today = parseLocalDate(todayStr);
  if (!today) return [];

  const out = [];
  for (let i = 0; i < 3; i += 1) {
    const date = addDays(today, -i);
    const dateStr = toIsoDate(date);
    const file = path.join(memoryDir, `${dateStr}.md`);
    if (!fs.existsSync(file)) continue;
    let raw;
    try {
      raw = fs.readFileSync(file, 'utf8');
    } catch (_) {
      continue;
    }
    const points = extractPoints(raw, 3);
    if (points.length === 0) continue;
    out.push({ date: dateStr, points });
  }

  return out;
}

function toLearnQueuePreview(items) {
  return items.map((item) => ({
    item_type: item.itemType,
    word: item.word,
    status: item.status ?? null,
    first_learned: item.firstLearned ?? null,
    last_reviewed: item.lastReviewed,
    next_review: item.nextReview ?? null,
  }));
}

function buildSessionContext({ repo, today, mode, memoryDir, maxDue, maxPending }) {
  const dbEntry = repo.getUserProfile();
  const profileExists = !!dbEntry;
  const profile = dbEntry ?? { ...DEFAULT_PROFILE };
  const queueLimit = mode === 'learn'
    ? Math.max(profile.dailyTarget, 1)
    : Math.max(profile.dailyTarget, maxDue, maxPending, 1);
  const pendingPreview = mode === 'learn' ? repo.listPendingWordsLimited(queueLimit) : [];
  const duePreview = mode === 'learn'
    ? repo.listDueWordsLimited(today, queueLimit)
    : [];
  const statusCounts = repo.countWordsByStatus();
  const activeCount = [1, 2, 3, 4, 5, 6, 7].reduce((sum, s) => sum + (statusCounts[s] || 0), 0);
  const masteredCount = statusCounts[8] || 0;
  const todayReviewedCount = repo.countDistinctReviewedWordsOn(today);
  const memoryDigest = buildMemoryDigest(today, memoryDir);
  const pendingCount = repo.countPendingWords();
  const dueCount = repo.countDueWords(today);

  const data = {
    profile_exists: profileExists,
    profile: {
      learning_goal: profile.learningGoal,
      difficulty_level: profile.difficultyLevel,
      daily_target: profile.dailyTarget,
    },
    progress: {
      today_reviewed_count: todayReviewedCount,
      active_count: activeCount,
      mastered_count: masteredCount,
      pending_count: pendingCount,
    },
    memory_digest: memoryDigest,
    learner_memory: buildLearnerMemory({
      repo,
      today,
      memoryDigest,
    }),
  };

  if (mode === 'learn') {
    const queue = [
      ...pendingPreview.map((item) => ({
        itemType: 'pending',
        word: item.word,
        status: null,
        firstLearned: null,
        lastReviewed: 'never',
        nextReview: null,
        createdAt: item.createdAt,
      })),
      ...duePreview.map((item) => ({
        itemType: 'due',
        word: item.word,
        status: item.status,
        firstLearned: item.firstLearned,
        lastReviewed: item.lastReviewed,
        nextReview: item.nextReview,
      })),
    ].slice(0, profile.dailyTarget);
    const pendingUsed = queue.filter((item) => item.itemType === 'pending').length;
    const dueUsed = queue.length - pendingUsed;

    data.learn = {
      queue_counts: {
        daily_target: profile.dailyTarget,
        queue_total: queue.length,
        pending_total: pendingCount,
        due_total: dueCount,
        pending_used: pendingUsed,
        due_used: dueUsed,
        need_new_words: Math.max(0, profile.dailyTarget - queue.length),
      },
      queue_preview: toLearnQueuePreview(queue),
    };
  }

  return data;
}

module.exports = {
  buildMemoryDigest,
  buildSessionContext,
  extractPoints,
};
