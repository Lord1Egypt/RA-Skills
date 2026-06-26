// SECURITY MANIFEST:
//   Environment variables accessed: none
//   External endpoints called: none
//   Local files read: none
//   Local files written: none

import type { PlatformAdapter } from '../types.js';

const adapterRegistry: Record<string, () => Promise<PlatformAdapter>> = {
  'bilibili': async () => {
    const { BilibiliAdapter } = await import('./bilibili.js');
    return new BilibiliAdapter();
  },
  'tieba': async () => {
    const { TiebaAdapter } = await import('./tieba.js');
    return new TiebaAdapter();
  },
  'zhihu': async () => {
    const { ZhihuAdapter } = await import('./zhihu.js');
    return new ZhihuAdapter();
  },
  'xiaohongshu': async () => {
    const { XiaohongshuAdapter } = await import('./xiaohongshu.js');
    return new XiaohongshuAdapter();
  },
};

export async function getAdapter(platformId: string): Promise<PlatformAdapter> {
  const factory = adapterRegistry[platformId];
  if (!factory) {
    const available = Object.keys(adapterRegistry).join(', ');
    throw new Error(`Unknown platform: "${platformId}". Available: ${available}`);
  }
  return factory();
}

export function listPlatforms(): string[] {
  return Object.keys(adapterRegistry);
}

const isMainModule = process.argv[1]?.replace(/\\/g, '/').endsWith('adapters/base.ts');
if (isMainModule && process.argv[2] === 'test') {
  console.log(JSON.stringify({
    script: 'adapters/base',
    status: 'ok',
    platforms: listPlatforms(),
  }));
}
