const { isAnthropicModel, detectModelProvider } = require('./model-utils');
const { runAnthropicPrompt } = require('./anthropic-provider');
const { runOpenAiPrompt } = require('./openai-provider');

async function runLlm(prompt, { model, timeoutMs, caller, skipLog } = {}) {
  const startedAt = Date.now();
  const provider = detectModelProvider(model);

  let result;
  if (isAnthropicModel(model)) {
    result = await runAnthropicPrompt({ model, prompt, timeoutMs, caller, skipLog });
  } else if (provider === 'openai') {
    result = await runOpenAiPrompt(prompt, { model, timeoutMs, caller, skipLog });
  } else {
    throw new Error(`Unsupported model/provider: ${JSON.stringify(model)}. Supported routing currently recognizes Anthropic and OpenAI model names.`);
  }

  return {
    ...result,
    durationMs: Date.now() - startedAt,
  };
}

module.exports = {
  runLlm,
};
