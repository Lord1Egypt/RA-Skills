import type { AuditContext } from './rules/types';
import type { DiffFile } from './diff-parser';
export declare function makeDiffFile(path: string, lines?: string[], status?: DiffFile['status']): DiffFile;
export declare function makeCtx(diffFiles: DiffFile[], overrides?: Partial<Omit<AuditContext, 'diffFiles'>>): AuditContext;
//# sourceMappingURL=test-utils.d.ts.map