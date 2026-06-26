import { executeStatus } from '../vendor/weryai-core/status.js';

export function execute(input, ctx) {
  return executeStatus(input, ctx, {
    outputKey: 'images',
    outputLabel: 'image',
    allowBatch: true,
  });
}

export default execute;
