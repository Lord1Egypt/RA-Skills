#!/usr/bin/env node
const { readJsonArg, postJson, print } = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.prompt) throw new Error('prompt is required');

  const payload = {
    model: input.model || 'cogview-3-flash',
    prompt: input.prompt,
    quality: input.quality || 'standard',
    size: input.size || '1024x1024',
    watermark_enabled: input.watermark_enabled !== undefined ? input.watermark_enabled : false,
    ...(input.user_id ? { user_id: input.user_id } : {}),
  };

  const data = await postJson('/paas/v4/images/generations', payload);
  print({ success: true, action: 'generate_image', model: payload.model, prompt: input.prompt, data });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
