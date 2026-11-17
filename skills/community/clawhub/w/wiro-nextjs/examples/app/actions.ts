// app/actions.ts
'use server';

import { runModel } from '../lib/wiro';

/** Text to speech with Eleven v4, $0.00008 per character. A server action keeps the key on the server too. */
export async function speak(text: string): Promise<{ token?: string; error?: string }> {
  if (typeof text !== 'string' || !text.trim() || text.length > 1000) {
    return { error: 'Send between 1 and 1,000 characters.' };
  }
  try {
    const token = await runModel('elevenlabs/eleven-v4', {
      prompt: text,
      voice: 'alice',
      outputFormat: 'mp3_44100_128',
    });
    return { token };
  } catch {
    return { error: 'Could not start the speech.' };
  }
}
