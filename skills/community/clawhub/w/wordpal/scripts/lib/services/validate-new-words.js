const { AppError, EXIT_CODES } = require('../errors');
const { normalizeWord, isSafeWord } = require('../core/input-guard');

function splitWords(raw) {
  return String(raw || '')
    .split(',')
    .map((word) => normalizeWord(word))
    .filter(Boolean);
}

function validateNewWords({ repo, wordsRaw }) {
  const words = splitWords(wordsRaw);
  if (words.length === 0) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      'No valid words parsed from --words',
      EXIT_CODES.INVALID_INPUT,
    );
  }

  const seen = new Set();
  const available = [];
  const rejected = [];

  for (const word of words) {
    if (seen.has(word)) {
      rejected.push({ word, reason: 'duplicate_in_input' });
      continue;
    }
    seen.add(word);

    if (!isSafeWord(word)) {
      rejected.push({ word, reason: 'unsafe_word' });
      continue;
    }

    const existing = repo.wordExists(word);
    if (existing) {
      rejected.push({ word, reason: existing.status === 8 ? 'exists_mastered' : 'exists_active' });
      continue;
    }

    if (repo.getPendingWord(word)) {
      rejected.push({ word, reason: 'exists_pending' });
      continue;
    }

    available.push(word);
  }

  return {
    input_count: words.length,
    available_count: available.length,
    rejected_count: rejected.length,
    available,
    rejected,
  };
}

module.exports = {
  splitWords,
  validateNewWords,
};
