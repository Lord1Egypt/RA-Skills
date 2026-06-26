const { runLlm } = require('../shared/llm-router');

const ALLOWED_INTENTS = new Set(['remember', 'recall', 'show-wine', 'show-label', 'label', 'unknown']);

function safeParseJson(text) {
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    const match = String(text).match(/\{[\s\S]*\}/);
    if (!match) return null;
    try {
      return JSON.parse(match[0]);
    } catch {
      return null;
    }
  }
}

async function classifyWineIntentWithLlm(text, { hasImage = false, model = process.env.WINE_LLM_INTENT_MODEL || 'openai/gpt-4.1-mini', runner = runLlm } = {}) {
  const prompt = `You are classifying a wine-chat user message.
Return JSON only with this exact schema:
{"intent":"remember|recall|show-wine|show-label|label|unknown","confidence":0-1,"reason":"short string"}

Intent meanings:
- remember: user wants to save/add/update/archive a wine or tasting
- recall: user wants to retrieve information about wines or tastings
- show-wine: user wants the canonical wine entry/details for a specific wine
- show-label: user wants to see the stored label image
- label: user is primarily asking to parse/identify a label image
- unknown: none of the above

Context:
- hasImage: ${hasImage ? 'true' : 'false'}
- message: ${JSON.stringify(text || '')}

Rules:
- Prefer show-label only if user is clearly asking to see/send the label/image/photo only.
- Prefer show-wine when the user is asking to show/display a specific wine entry/details.
- Prefer recall if user is asking what they had, bought, drank, tried, or wants details/history.
- Prefer remember if user is telling the system to add/save/log/archive/update a wine or tasting.
- Prefer label when the task is label parsing/identification rather than storage or retrieval.
- If uncertain, return unknown.
- Output JSON only.`;

  const { text: response } = await runner(prompt, {
    model,
    caller: 'wine-intent-classifier',
    timeoutMs: 20000,
  });

  const parsed = safeParseJson(response);
  if (!parsed || !ALLOWED_INTENTS.has(parsed.intent)) {
    throw new Error(`Invalid LLM wine intent response: ${JSON.stringify(response)}`);
  }

  return {
    intent: parsed.intent,
    confidence: Number(parsed.confidence || 0),
    reason: String(parsed.reason || ''),
    raw: response,
  };
}

module.exports = {
  classifyWineIntentWithLlm,
};
