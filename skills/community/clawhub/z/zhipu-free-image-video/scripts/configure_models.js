#!/usr/bin/env node
const { readJsonArg, print, getImageModels, getVideoModels } = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  const imageModel = input.default_image_model || 'cogview-3-flash';
  const videoModel = input.default_video_model || 'cogvideox-flash';

  if (!getImageModels().includes(imageModel)) {
    throw new Error(`unsupported default_image_model: ${imageModel}`);
  }
  if (!getVideoModels().includes(videoModel)) {
    throw new Error(`unsupported default_video_model: ${videoModel}`);
  }

  print({
    success: true,
    action: 'configure_models',
    default_image_model: imageModel,
    default_video_model: videoModel,
    note: 'This script validates preferred defaults for the current task. Persist them in your environment or workflow if needed.',
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
