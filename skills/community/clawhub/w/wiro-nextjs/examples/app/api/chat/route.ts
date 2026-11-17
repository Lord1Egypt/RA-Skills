// app/api/chat/route.ts
import { createWiro } from '@wiro-ai/wiro-llm';
import { convertToModelMessages, streamText, type UIMessage } from 'ai';

export const maxDuration = 60;

export async function POST(request: Request) {
  const { messages } = (await request.json()) as { messages: UIMessage[] };
  const { WIRO_API_KEY, WIRO_API_SECRET } = process.env;
  // The gateway takes the key, or KEY:SECRET for a Signature project. No nonce or signature here.
  const wiro = createWiro({ apiKey: WIRO_API_SECRET ? `${WIRO_API_KEY}:${WIRO_API_SECRET}` : WIRO_API_KEY });

  const result = streamText({
    model: wiro('openai/gpt-5-4-nano'), // any chat model id from GET https://llm.wiro.ai/v1/models
    messages: await convertToModelMessages(messages.slice(-20)),
    maxOutputTokens: 1024, // reasoning tokens count too, so keep this at 512 or more
    abortSignal: request.signal,
  });

  return result.toUIMessageStreamResponse({
    // Every step reports what it cost, in USD.
    messageMetadata: ({ part }) =>
      part.type === 'finish-step' ? { cost: Number(part.providerMetadata?.wiro?.cost ?? 0) } : undefined,
  });
}
