#!/usr/bin/env node
const { readJsonArg, postJson, print, sleep } = require('./lib');

async function generateOne(prompt, input) {
  const payload = {
    model: input.model || 'cogview-3-flash',
    prompt,
    quality: input.quality || 'standard',
    size: input.size || '1024x1024',
    watermark_enabled: input.watermark_enabled !== undefined ? input.watermark_enabled : false,
    ...(input.user_id ? { user_id: input.user_id } : {}),
  };
  const data = await postJson('/paas/v4/images/generations', payload);
  return { prompt, success: true, data };
}

async function main() {
  const input = readJsonArg(2, 'input');
  if (!Array.isArray(input.prompts) || !input.prompts.length) {
    throw new Error('prompts is required');
  }

  const prompts = input.prompts.slice(0, 100);
  const batchSize = Math.max(1, Math.min(20, Number(input.batch_size || 4)));
  const maxConcurrent = Math.max(1, Math.min(10, Number(input.max_concurrent || 3)));
  const delay = Math.max(0, Number(input.delay_between_batches || 1000));
  const parallel = input.parallel !== false;
  const results = [];

  for (let i = 0; i < prompts.length; i += batchSize) {
    const batch = prompts.slice(i, i + batchSize);
    if (parallel) {
      for (let j = 0; j < batch.length; j += maxConcurrent) {
        const slice = batch.slice(j, j + maxConcurrent);
        const settled = await Promise.all(slice.map(async (prompt) => {
          try {
            return await generateOne(prompt, input);
          } catch (error) {
            return { prompt, success: false, error: error.message };
          }
        }));
        results.push(...settled);
      }
    } else {
      for (const prompt of batch) {
        try {
          results.push(await generateOne(prompt, input));
        } catch (error) {
          results.push({ prompt, success: false, error: error.message });
        }
      }
    }
    if (i + batchSize < prompts.length && delay > 0) {
      await sleep(delay);
    }
  }

  print({
    success: results.every((item) => item.success),
    action: 'batch_generate_images',
    total_prompts: prompts.length,
    successful_generations: results.filter((item) => item.success).length,
    failed_generations: results.filter((item) => !item.success).length,
    results,
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
