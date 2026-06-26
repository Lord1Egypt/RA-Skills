const OpenAI = require('openai');

const MODEL = process.env.OPENAI_MODEL || 'gpt-4.1-mini';

const SCORE_SYSTEM_PROMPT = [
  'You are a network relevance scoring assistant.',
  'Given a user query and connection data, return ONLY JSON.',
  'Output schema:',
  '{ "results": [{ "id": "string", "relevanceScore": 0, "reason": "string" }] }',
  'Rules:',
  '- relevanceScore must be an integer 0 to 100.',
  '- reason must be one short sentence.',
  '- Include every connection id exactly once.',
].join('\n');

const ACTION_SYSTEM_PROMPT = [
  'You generate two concise relationship-building actions for one professional contact.',
  'Return ONLY JSON with schema:',
  '{ "actions": ["action one", "action two"] }',
  'Actions should be short, practical, and specific to the person role/tags.',
].join('\n');

function getOpenAIClient() {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new Error('OPENAI_API_KEY is required in environment variables.');
  }

  return new OpenAI({ apiKey });
}

function safeJsonParse(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

async function scoreConnections(query, connections) {
  if (!Array.isArray(connections) || connections.length === 0) {
    return [];
  }

  const client = getOpenAIClient();

  const userPrompt = JSON.stringify(
    {
      query,
      connections: connections.map((connection) => ({
        id: connection.id,
        name: connection.name,
        role: connection.role,
        company: connection.company,
        location: connection.location,
        platforms: connection.platforms,
        tags: connection.tags,
        notes: connection.notes,
        lastInteraction: connection.lastInteraction,
      })),
    },
    null,
    2
  );

  const completion = await client.chat.completions.create({
    model: MODEL,
    temperature: 0.2,
    messages: [
      { role: 'system', content: SCORE_SYSTEM_PROMPT },
      { role: 'user', content: userPrompt },
    ],
    response_format: { type: 'json_object' },
  });

  const text = completion.choices?.[0]?.message?.content || '{}';
  const parsed = safeJsonParse(text);
  const scored = Array.isArray(parsed?.results) ? parsed.results : [];

  const byId = new Map(connections.map((connection) => [connection.id, connection]));

  return scored
    .map((item) => {
      const original = byId.get(item.id);
      if (!original) {
        return null;
      }

      const score = Number.isFinite(item.relevanceScore)
        ? Math.max(0, Math.min(100, Math.round(item.relevanceScore)))
        : 0;

      return {
        ...original,
        relevanceScore: score,
        reason: typeof item.reason === 'string' ? item.reason : 'Potentially relevant connection.',
      };
    })
    .filter(Boolean)
    .sort((a, b) => b.relevanceScore - a.relevanceScore);
}

async function suggestActions(connection) {
  const client = getOpenAIClient();

  const completion = await client.chat.completions.create({
    model: MODEL,
    temperature: 0.4,
    messages: [
      { role: 'system', content: ACTION_SYSTEM_PROMPT },
      {
        role: 'user',
        content: JSON.stringify(
          {
            name: connection.name,
            role: connection.role,
            company: connection.company,
            tags: connection.tags,
            notes: connection.notes,
          },
          null,
          2
        ),
      },
    ],
    response_format: { type: 'json_object' },
  });

  const text = completion.choices?.[0]?.message?.content || '{}';
  const parsed = safeJsonParse(text);
  const actions = Array.isArray(parsed?.actions) ? parsed.actions : [];

  return actions
    .filter((item) => typeof item === 'string' && item.trim().length > 0)
    .slice(0, 2);
}

module.exports = {
  scoreConnections,
  suggestActions,
};
