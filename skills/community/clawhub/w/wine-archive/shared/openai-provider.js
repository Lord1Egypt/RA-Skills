async function runOpenAiPrompt(_prompt, { model } = {}) {
  throw new Error(`No non-Anthropic provider handler is configured for model ${JSON.stringify(model)}. Add your OpenAI/other provider implementation in shared/openai-provider.js.`);
}

async function runOtherProviderPrompt(prompt, options = {}) {
  return runOpenAiPrompt(prompt, options);
}

module.exports = {
  runOpenAiPrompt,
  runOtherProviderPrompt,
};
