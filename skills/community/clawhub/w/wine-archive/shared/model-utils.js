const MODEL_ALIAS_MAP = Object.freeze({
  'opus-4': 'claude-opus-4',
  'opus4': 'claude-opus-4',
  'claude-opus-4': 'claude-opus-4',
  'sonnet-4': 'claude-sonnet-4',
  'sonnet4': 'claude-sonnet-4',
  'claude-sonnet-4': 'claude-sonnet-4',
  'haiku-4': 'claude-haiku-4',
  'haiku4': 'claude-haiku-4',
  'claude-haiku-4': 'claude-haiku-4',
  'gpt-4.1': 'gpt-4.1',
  'gpt-4o': 'gpt-4o',
  'gpt-4o-mini': 'gpt-4o-mini',
});

function stripProviderPrefix(model) {
  if (!model || typeof model !== 'string') return model;
  return model.replace(/^(anthropic|openai)\//i, '');
}

function normalizeAnthropicModel(model) {
  if (!model || typeof model !== 'string') return model;
  const stripped = stripProviderPrefix(model).trim();
  const lowered = stripped.toLowerCase();
  return MODEL_ALIAS_MAP[lowered] || stripped;
}

function isAnthropicModel(model) {
  if (!model || typeof model !== 'string') return false;
  const normalized = normalizeAnthropicModel(model).toLowerCase();
  return /(claude|opus|sonnet|haiku)/i.test(normalized);
}

function detectModelProvider(model) {
  if (!model || typeof model !== 'string') return null;
  if (/^anthropic\//i.test(model) || isAnthropicModel(model)) return 'anthropic';
  if (/^openai\//i.test(model) || /\b(gpt|o1|o3|o4)\b/i.test(model)) return 'openai';
  return null;
}

module.exports = {
  MODEL_ALIAS_MAP,
  isAnthropicModel,
  normalizeAnthropicModel,
  detectModelProvider,
  stripProviderPrefix,
};
