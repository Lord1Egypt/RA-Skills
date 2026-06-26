const { AppError, EXIT_CODES } = require('../errors');
const { buildQuestionPlan } = require('./question-plan');
const { stageWord } = require('./stage-word');
const { validateNewWords } = require('./validate-new-words');

function validateNextQuestionInput(input) {
  if (input.validate && (input.mode !== 'learn' || input.itemType !== 'pending')) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      '--validate only supports --mode learn --item-type pending',
      EXIT_CODES.INVALID_INPUT,
    );
  }

  if (input.itemType === 'pending') {
    if (input.status !== null) {
      throw new AppError(
        'INVALID_ARGUMENTS',
        'pending item-type must not provide --status',
        EXIT_CODES.INVALID_INPUT,
      );
    }
    if (input.mode !== 'learn') {
      throw new AppError(
        'INVALID_ARGUMENTS',
        'pending item-type only supports --mode learn',
        EXIT_CODES.INVALID_INPUT,
      );
    }
    if (!input.difficultyLevel) {
      throw new AppError(
        'INVALID_ARGUMENTS',
        'learn pending question requires --difficulty-level',
        EXIT_CODES.INVALID_INPUT,
      );
    }
    return;
  }

  if (!Number.isInteger(input.status)) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      'due item-type requires --status',
      EXIT_CODES.INVALID_INPUT,
    );
  }

  if (input.difficultyLevel !== null) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      'due item-type must not provide --difficulty-level',
      EXIT_CODES.INVALID_INPUT,
    );
  }
}

function buildWordRejectedError(word, reason) {
  return new AppError(
    'WORD_REJECTED',
    `word "${word}" rejected: ${reason}`,
    EXIT_CODES.BUSINESS_RULE,
    { reason },
  );
}

function buildNextQuestion({ repo, input }) {
  validateNextQuestionInput(input);

  let stage = null;

  if (input.validate) {
    const validation = validateNewWords({
      repo,
      wordsRaw: input.word,
    });
    if (validation.available_count !== 1) {
      const reason = validation.rejected[0] ? validation.rejected[0].reason : 'rejected';
      throw buildWordRejectedError(input.word, reason);
    }

    stage = stageWord({
      repo,
      input: {
        word: input.word,
        opIdArg: null,
      },
    });
  }

  const question = buildQuestionPlan({
    mode: input.mode,
    itemType: input.itemType,
    word: input.word,
    status: input.status,
    difficultyLevel: input.difficultyLevel,
    lastType: input.lastType,
    today: input.today,
    compact: true,
  });

  return {
    word: input.word,
    item_type: input.itemType,
    status: input.status,
    stage,
    question,
  };
}

module.exports = {
  buildNextQuestion,
  buildWordRejectedError,
  validateNextQuestionInput,
};
