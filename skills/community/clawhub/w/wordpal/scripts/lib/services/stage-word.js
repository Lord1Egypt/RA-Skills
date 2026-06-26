const { AppError, EXIT_CODES } = require('../errors');
const { deriveOpId } = require('../core/input-guard');

function toResultPayload(input) {
  const {
    result,
    word,
    opId,
    createdAt,
  } = input;

  return {
    result,
    word,
    op_id: opId,
    created_at: createdAt,
  };
}

function formatStageText(result) {
  if (result.result === 'idempotent') {
    return `[Idempotent] '${result.word}' already pending | op-id: ${result.op_id}`;
  }

  return `[Staged] '${result.word}' pending | op-id: ${result.op_id}`;
}

function stageWord({ repo, input }) {
  const {
    word,
    opIdArg,
  } = input;

  return repo.transaction(() => {
    const existing = repo.wordExists(word);
    if (existing) {
      throw new AppError(
        'WORD_EXISTS',
        `word "${word}" already exists in ${existing.status === 8 ? 'mastered' : 'active'} storage`,
        EXIT_CODES.BUSINESS_RULE,
      );
    }

    const pending = repo.getPendingWord(word);
    if (pending) {
      return toResultPayload({
        result: 'idempotent',
        word,
        opId: pending.lastOpId,
        createdAt: pending.createdAt,
      });
    }

    const createdAt = new Date().toISOString();
    const opId = opIdArg || deriveOpId(`${word}|stage`);
    const inserted = repo.stagePendingWord({
      word,
      createdAt,
      lastOpId: opId,
    });

    if (!inserted) {
      return toResultPayload({
        result: 'idempotent',
        word,
        opId,
        createdAt,
      });
    }

    return toResultPayload({
      result: 'staged',
      word,
      opId,
      createdAt,
    });
  });
}

module.exports = {
  formatStageText,
  stageWord,
};
