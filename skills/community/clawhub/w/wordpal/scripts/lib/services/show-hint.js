const crypto = require('crypto');

function showHint({ repo, input }) {
  repo.deleteExpiredHintTokens();
  const token = crypto.randomBytes(12).toString('hex');
  const now = new Date().toISOString();
  repo.insertHintToken({ token, word: input.word, createdAt: now });
  return {
    hint_token: token,
    word: input.word,
    created_at: now,
  };
}

module.exports = { showHint };
