const { AppError, EXIT_CODES } = require('../errors');
const { updateWord } = require('./update-word');

function submitAnswer({ repo, input }) {
  if (input.hintTokenArg != null) {
    const tokenRecord = repo.findHintToken(input.hintTokenArg);
    if (!tokenRecord) {
      throw new AppError(
        'HINT_TOKEN_INVALID',
        'Hint token not found or already used',
        EXIT_CODES.BUSINESS_RULE,
      );
    }
    if (tokenRecord.word !== input.word) {
      throw new AppError(
        'HINT_TOKEN_INVALID',
        'Hint token does not match the submitted word',
        EXIT_CODES.BUSINESS_RULE,
      );
    }
    const ageMs = Date.now() - new Date(tokenRecord.createdAt).getTime();
    if (ageMs > 30 * 60 * 1000) {
      repo.deleteHintToken(input.hintTokenArg);
      throw new AppError(
        'HINT_TOKEN_EXPIRED',
        'Hint token has expired. Call show-hint.js again.',
        EXIT_CODES.BUSINESS_RULE,
      );
    }
    repo.deleteHintToken(input.hintTokenArg);
  }

  const update = updateWord({
    repo,
    input: {
      word: input.word,
      statusArg: null,
      firstLearnedArg: null,
      lastReviewed: input.lastReviewed,
      eventArg: input.eventArg,
      opIdArg: input.opIdArg,
    },
  });

  return {
    result: update.result,
    word: update.word,
    status: update.status,
    status_emoji: update.status_emoji,
    today_count: update.today_count,
    previous_status: update.previous_status,
    next_review: update.next_review,
    review_event: update.review_event,
    op_id: update.op_id,
    remaining_in_queue: input.remainingCount,
  };
}

module.exports = {
  submitAnswer,
};
