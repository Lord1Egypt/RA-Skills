const crypto = require('crypto');

const { AppError, EXIT_CODES } = require('../errors');
const { DIFFICULTY_LEVELS } = require('./user-profile');

const WORD_CARD_DISPLAY_FIELDS = ['单词', '音标', '词性', '中文释义'];
const ALL_QUESTION_TYPES = [
  'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9',
  'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17',
];
const LEARN_PENDING_POOLS = {
  I: ['Q1', 'Q2', 'Q3'],
  II: ['Q1', 'Q2', 'Q3', 'Q4'],
  III: ['Q2', 'Q3', 'Q4', 'Q5', 'Q9'],
  IV: ['Q3', 'Q4', 'Q5', 'Q6', 'Q9', 'Q10'],
  V: ['Q4', 'Q5', 'Q6', 'Q9', 'Q10'],
};

const REVIEW_BANDS = [
  { key: 'status_1_2', statuses: [1, 2], types: ['Q1', 'Q3', 'Q6', 'Q7', 'Q8', 'Q11', 'Q12'], fallbackKeys: ['status_3'] },
  { key: 'status_3', statuses: [3], types: ['Q3', 'Q6', 'Q11', 'Q12', 'Q13', 'Q14'], fallbackKeys: ['status_1_2', 'status_4_7'] },
  { key: 'status_4_7', statuses: [4, 5, 6, 7], types: ['Q9', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17'], fallbackKeys: ['status_3'] },
];

const QUESTION_TYPE_DETAILS = {
  Q1: {
    name: '单词释义选择',
    description: '直接从四个选项里选出目标词的意思。',
  },
  Q2: {
    name: '词卡同义词识别',
    description: '先看词卡，再从四个简单词里选出和目标词同义的一项。',
  },
  Q3: {
    name: '英文语境猜义',
    description: '先看一句英文语境，再猜目标词的大意。',
  },
  Q4: {
    name: '场景选义',
    description: '先看词卡，再判断目标词是否适合给定场景。',
  },
  Q5: {
    name: '固定搭配入门',
    description: '先看词卡，再从多个搭配里选出最自然的一项。',
  },
  Q6: {
    name: '语义线索选词',
    description: '根据同义、反义或概念线索，从四个选项中选出目标词。',
  },
  Q7: {
    name: '用法判断',
    description: '判断目标词当前用法是否正确，并简要说明原因。',
  },
  Q8: {
    name: '固定搭配选择',
    description: '在多个搭配里选出最自然的目标词用法。',
  },
  Q9: {
    name: '场景造句复现',
    description: '根据场景提示，用目标词写一句原创英文句子。',
  },
  Q10: {
    name: '场景翻译',
    description: '先看词卡信息，再把中文场景翻成包含目标词的英文句子。',
  },
  Q11: {
    name: '英文填空（带提示）',
    description: '根据英文句子上下文和首字母+词长提示，把目标词填进空格。',
  },
  Q12: {
    name: '三线索猜词',
    description: '根据三条递进线索（第三条为首字母+词长）猜出目标词。',
  },
  Q13: {
    name: '单词纠错',
    description: '找出句中被替换为形近/音近但不同义的错误词，给出正确的目标词。',
  },
  Q14: {
    name: '词汇升级替换',
    description: '把基础表达替换成更准确的目标词表达（带首字母+词长提示）。',
  },
  Q15: {
    name: '中文句子回忆单词',
    description: '根据中文句子线索和首字母+词长提示，回答目标词。',
  },
  Q16: {
    name: '中文释义拼写',
    description: '根据中文释义，完整拼出目标词。',
  },
  Q17: {
    name: '场景造句（无词卡）',
    description: '根据场景提示，不看词卡，用目标词写一句原创英文句子。',
  },
};

const QUESTION_TYPE_CONSTRAINTS = {
  Q1: {
    group: 'learn',
    prompt_style: 'direct_meaning_multiple_choice',
    reveal_word_card: false,
    answer_expectation: 'choose_the_correct_meaning_from_four_options',
    notes: [
      'ask exactly one multiple-choice question with four options',
      'do not reveal extra hints beyond the word itself before the user answers',
      'options should be short meanings rather than full example sentences',
      'correct answer position must vary across questions; do not always place it in option A',
    ],
  },
  Q2: {
    group: 'learn',
    prompt_style: 'word_card_then_synonym_choice',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'choose_the_matching_simple_synonym_from_four_options',
    notes: [
      'show the word card before asking',
      'the four options should be simple and common English words or short phrases',
      'only one option should match the target meaning closely',
    ],
  },
  Q3: {
    group: 'learn',
    prompt_style: 'english_context_guess_meaning',
    reveal_word_card: false,
    answer_expectation: 'guess_meaning_from_context',
    notes: [
      'use one English sentence with the target word bolded',
      'do not reveal Chinese meaning before the user answers',
      'prefer scenarios from memory_digest, then fallback to learning_goal',
      'the sentence must not contain Chinese or direct definitions of the target word',
      'the sentence difficulty should match the user learning_goal level',
    ],
  },
  Q4: {
    group: 'learn',
    prompt_style: 'word_card_then_usage_fit',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'judge_if_the_word_fits_the_scene_with_a_brief_reason',
    notes: [
      'show the word card before asking',
      'the scene must be a short, concrete English sentence',
      'the user answer should stay brief: fit or not fit plus a short reason',
    ],
  },
  Q5: {
    group: 'learn',
    prompt_style: 'word_card_then_collocation_choice',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'pick_best_beginner_friendly_collocation',
    notes: [
      'show the word card before asking',
      'keep distractors plausible but easier than review-mode collocation questions',
      'focus on one common collocation pattern only',
    ],
  },
  Q6: {
    group: 'learn',
    prompt_style: 'semantic_clue_multiple_choice',
    reveal_word_card: false,
    answer_expectation: 'choose_the_target_word_from_four_options',
    notes: [
      'do not show the word card',
      'present a synonym, antonym, or conceptual clue, then provide four word options',
      'only one option should be the target word; distractors should be plausible but clearly different in meaning',
      'correct answer position must vary across questions; do not always place it in option A',
      'do not include the target word or its direct morphological variants in the clue text itself',
    ],
  },
  Q7: {
    group: 'learn',
    prompt_style: 'usage_judgment',
    reveal_word_card: false,
    answer_expectation: 'judge_correctness_and_explain',
    notes: [
      'the target word appears in the sentence; do not show a separate word card',
      'keep true/false cases balanced over time',
    ],
  },
  Q8: {
    group: 'learn',
    prompt_style: 'collocation_choice',
    reveal_word_card: false,
    answer_expectation: 'pick_best_collocation_and_explain_briefly',
    notes: [
      'the target word appears in the question; do not show a separate word card',
      'wrong options should prefer common Chinglish phrasing',
    ],
  },
  Q9: {
    group: 'learn',
    prompt_style: 'scene_based_sentence_writing',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'write_one_original_sentence_with_target_word',
    notes: [
      'show the word card before asking; this task tests usage and production, not recall of the word itself',
      'the scene must relate to the learner profile (learning_goal and personal_context); do not use generic or random scenes',
      'feedback order should be strengths first, then corrections',
    ],
  },
  Q10: {
    group: 'learn',
    prompt_style: 'word_card_then_translate',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'translate_one_chinese_scene_into_full_english_sentence',
    notes: [
      'do not use fill-in-the-blank',
      'focus on target-word placement and grammar',
    ],
  },
  Q11: {
    group: 'learn',
    prompt_style: 'english_cloze_with_hint',
    reveal_word_card: false,
    answer_expectation: 'fill_the_target_word_into_the_blank',
    notes: [
      'do not show the word card; revealing it would expose the answer',
      'show a hint line after the blank sentence: first letter + word length (e.g. "提示：a_______ (7 letters)")',
      'context must be inferable from the sentence',
      'the blank must replace the target word exactly; do not blank out a different word',
      'surrounding context plus the first-letter hint must make the target word uniquely inferable',
    ],
  },
  Q12: {
    group: 'learn',
    prompt_style: 'triple_clue_word_guess',
    reveal_word_card: false,
    answer_expectation: 'guess_the_word_from_three_clues',
    notes: [
      'do not show the word card; the goal is unaided recall of the target word',
      'present exactly three clues at once in a single turn; do not use multi-turn interaction',
      'clue 1: broad category or domain hint',
      'clue 2: more specific semantic or usage hint that narrows down the answer',
      'clue 3: first letter + word length (e.g. "首字母 a，共 7 个字母")',
      'never reveal the word itself or its Chinese meaning as a clue',
    ],
  },
  Q13: {
    group: 'learn',
    prompt_style: 'lookalike_word_correction',
    reveal_word_card: false,
    answer_expectation: 'identify_the_wrong_word_and_give_the_correct_one',
    notes: [
      'do not show the word card',
      'replace the target word in the sentence with a visually or phonetically similar but different-meaning word (e.g. inference → infertile, complement → compliment)',
      'the rest of the sentence must be correct; only the swapped word is wrong',
      'the impostor word should look or sound plausible in the sentence at first glance',
      'the user must identify which word is wrong and provide the correct target word',
    ],
  },
  Q14: {
    group: 'learn',
    prompt_style: 'vocabulary_upgrade_with_hint',
    reveal_word_card: false,
    answer_expectation: 'replace_basic_word_with_target_word',
    notes: [
      'do not show the word card; the goal is to recall the target word from context',
      'show a hint line after the sentence: first letter + word length (e.g. "提示：a_______ (7 letters)")',
      'reasonable synonyms can be accepted if they stay close to the target intent',
      'the basic expression should use a simpler synonym, not an unrelated word',
      'context must make the upgrade clearly beneficial, not just optional',
    ],
  },
  Q15: {
    group: 'learn',
    prompt_style: 'chinese_sentence_to_single_word_with_hint',
    reveal_word_card: false,
    answer_expectation: 'reply_with_target_word_only',
    notes: [
      'do not show the word card; the goal is recall of the target word with minimal assistance',
      'do not provide answer options',
      'show a hint line after the sentence: first letter + word length (e.g. "提示：a_______ (7 letters)")',
      'the Chinese sentence must uniquely point to the target word; avoid sentences where multiple English words could fit',
    ],
  },
  Q16: {
    group: 'learn',
    prompt_style: 'definition_to_spelling',
    reveal_word_card: false,
    answer_expectation: 'spell_the_target_word',
    notes: [
      'do not show the word card; the goal is unaided recall and correct spelling',
      'Chinese clue should uniquely identify the word',
      'give only the Chinese definition, no extra English hints or context',
    ],
  },
  Q17: {
    group: 'learn',
    prompt_style: 'scene_based_sentence_writing_no_card',
    reveal_word_card: false,
    answer_expectation: 'write_one_original_sentence_with_target_word',
    notes: [
      'do not show the word card; the user must recall meaning and usage from memory',
      'provide only the target word and a scene description',
      'the scene must relate to the learner profile (learning_goal and personal_context); do not use generic or random scenes',
      'feedback order should be strengths first, then corrections',
    ],
  },
};

function stableIndex(parts, length) {
  const hash = crypto.createHash('sha256').update(parts.join('|')).digest('hex');
  return Number.parseInt(hash.slice(0, 8), 16) % length;
}

function pickStableType(types, parts) {
  if (!Array.isArray(types) || types.length === 0) {
    throw new AppError(
      'NO_AVAILABLE_TYPES',
      'no available question types to choose from',
      EXIT_CODES.BUSINESS_RULE,
    );
  }
  return types[stableIndex(parts, types.length)];
}

function excludeLastType(types, lastType, options = {}) {
  const { preserveSingle = false } = options;
  if (!lastType) {
    return types.slice();
  }
  if (types.length <= 1 && preserveSingle) {
    return types.slice();
  }
  const filtered = types.filter((type) => type !== lastType);
  if (filtered.length > 0) return filtered;
  return preserveSingle ? types.slice() : [];
}

function getReviewBand(status, bands = REVIEW_BANDS) {
  return bands.find((band) => band.statuses.includes(status)) || null;
}

function getBandByKey(key, bands = REVIEW_BANDS) {
  return bands.find((band) => band.key === key) || null;
}

function resolveLearnPendingTypes(difficultyLevel, lastType) {
  const pool = LEARN_PENDING_POOLS[difficultyLevel];
  if (!pool) {
    throw new AppError(
      'INVALID_DIFFICULTY_LEVEL',
      `unsupported difficulty level: ${String(difficultyLevel)}`,
      EXIT_CODES.BUSINESS_RULE,
    );
  }

  return {
    allowedTypes: excludeLastType(pool, lastType, { preserveSingle: true }),
    selectionReason: `learn_pending_${difficultyLevel}`,
    usedFallback: false,
  };
}

function resolveReviewTypes(status, lastType, bands = REVIEW_BANDS) {
  const primaryBand = getReviewBand(status, bands);
  if (!primaryBand) {
    throw new AppError(
      'INVALID_STATUS',
      `status ${String(status)} cannot be used for review question planning`,
      EXIT_CODES.INVALID_INPUT,
    );
  }

  const primaryTypes = excludeLastType(primaryBand.types, lastType);
  if (primaryTypes.length > 0) {
    return {
      allowedTypes: primaryTypes,
      selectionReason: primaryBand.key,
      usedFallback: false,
    };
  }

  for (const fallbackKey of primaryBand.fallbackKeys) {
    const fallbackBand = getBandByKey(fallbackKey, bands);
    if (!fallbackBand) continue;
    const fallbackTypes = excludeLastType(fallbackBand.types, lastType);
    if (fallbackTypes.length > 0) {
      return {
        allowedTypes: fallbackTypes,
        selectionReason: `${primaryBand.key}_fallback_${fallbackBand.key}`,
        usedFallback: true,
      };
    }
  }

  throw new AppError(
    'NO_AVAILABLE_TYPES',
    `no review question types available for status ${String(status)}`,
    EXIT_CODES.BUSINESS_RULE,
  );
}

function toCompactQuestionPlan(plan) {
  return {
    question_type: plan.question_type,
    question_type_name: plan.question_type_name,
    constraints: {
      group: plan.constraints.group,
      reveal_word_card: !!plan.constraints.reveal_word_card,
      word_card_fields: Array.isArray(plan.constraints.word_card_fields)
        ? plan.constraints.word_card_fields.slice()
        : null,
    },
  };
}

function buildQuestionPlan(input) {
  const {
    mode,
    itemType,
    word,
    status,
    difficultyLevel,
    lastType,
    today,
    compact = false,
    reviewBands = REVIEW_BANDS,
  } = input;

  if (itemType === 'pending' && status !== null) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      'pending item-type must not provide --status',
      EXIT_CODES.INVALID_INPUT,
    );
  }

  let resolution = null;
  let seedParts = null;

  if (mode === 'learn' && itemType === 'pending') {
    if (!DIFFICULTY_LEVELS.includes(difficultyLevel)) {
      throw new AppError(
        'INVALID_ARGUMENTS',
        'pending learn question planning requires --difficulty-level',
        EXIT_CODES.INVALID_INPUT,
      );
    }
    resolution = resolveLearnPendingTypes(difficultyLevel, lastType);
    seedParts = [mode, itemType, word, difficultyLevel, lastType || '', today];
  } else {
    if (!Number.isInteger(status)) {
      throw new AppError(
        'INVALID_ARGUMENTS',
        'due/review question planning requires --status',
        EXIT_CODES.INVALID_INPUT,
      );
    }
    resolution = resolveReviewTypes(status, lastType, reviewBands);
    seedParts = [mode, itemType, word, String(status), lastType || '', today];
  }

  const questionType = pickStableType(resolution.allowedTypes, seedParts);
  const questionTypeDetails = QUESTION_TYPE_DETAILS[questionType];

  const plan = {
    question_type: questionType,
    question_type_name: questionTypeDetails.name,
    question_type_description: questionTypeDetails.description,
    allowed_types: resolution.allowedTypes,
    selection_reason: resolution.selectionReason,
    used_fallback: resolution.usedFallback,
    constraints: {
      ...QUESTION_TYPE_CONSTRAINTS[questionType],
    },
  };

  return compact ? toCompactQuestionPlan(plan) : plan;
}

module.exports = {
  ALL_QUESTION_TYPES,
  LEARN_PENDING_POOLS,
  QUESTION_TYPE_CONSTRAINTS,
  QUESTION_TYPE_DETAILS,
  REVIEW_BANDS,
  WORD_CARD_DISPLAY_FIELDS,
  buildQuestionPlan,
  excludeLastType,
  getReviewBand,
  pickStableType,
  resolveLearnPendingTypes,
  resolveReviewTypes,
  stableIndex,
  toCompactQuestionPlan,
};
