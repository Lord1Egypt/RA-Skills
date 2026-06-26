#!/usr/bin/env node
const { readJsonArg, postJson, print } = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.prompt) throw new Error('prompt is required');

  const payload = {
    model: input.model || 'cogvideox-flash',
    prompt: input.prompt,
    ...(input.image_url ? { image_url: input.image_url } : {}),
    ...(input.quality ? { quality: input.quality } : {}),
    ...(input.size ? { size: input.size } : {}),
    ...(input.fps ? { fps: input.fps } : {}),
    ...(input.duration ? { duration: input.duration } : {}),
    ...(input.with_audio !== undefined ? { with_audio: input.with_audio } : {}),
    ...(input.watermark_enabled !== undefined ? { watermark_enabled: input.watermark_enabled } : {}),
  };

  const data = await postJson('/paas/v4/videos/generations', payload);
  print({ success: true, action: 'generate_video', model: payload.model, prompt: input.prompt, data });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
