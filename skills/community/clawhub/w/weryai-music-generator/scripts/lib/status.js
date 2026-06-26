import { executeStatus } from '../vendor/weryai-core/status.js';

export function execute(input, ctx) {
  return executeStatus(input, ctx, {
    outputKey: 'audios',
    outputLabel: 'audio',
    allowBatch: false,
  });
}
