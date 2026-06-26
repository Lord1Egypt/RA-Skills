import type { LogFormat, LogLevel, Logger } from './types';
export declare const sol: (lamports: number) => string;
export declare const bpsToPercent: (bps: number) => string;
export declare const withTimeout: <T>(promise: Promise<T>, label: string) => Promise<T>;
export declare const withRetry: <T>(fn: () => Promise<T>, label: string, attempts?: number, onRetry?: () => void) => Promise<T>;
export declare const createLogger: (minLevel: LogLevel, format?: LogFormat) => Logger;
//# sourceMappingURL=utils.d.ts.map