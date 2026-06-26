// Probe registry — all built-in probes

export { gpuProbe } from './gpu.js';
export { diskProbe } from './disk.js';
export { processProbe } from './process.js';

import { gpuProbe } from './gpu.js';
import { diskProbe } from './disk.js';
import { processProbe } from './process.js';
import type { Probe } from '../types/index.js';

/** All built-in probes, in execution order */
export const defaultProbes: Probe[] = [gpuProbe, diskProbe, processProbe];

/** Get probe by name */
export function getProbe(name: string): Probe | undefined {
  return defaultProbes.find((p) => p.name === name);
}
