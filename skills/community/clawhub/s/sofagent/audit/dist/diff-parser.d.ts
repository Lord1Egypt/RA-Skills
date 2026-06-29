export interface DiffFile {
    path: string;
    status: 'added' | 'modified' | 'deleted' | 'renamed';
    oldPath?: string;
    lines: string[];
}
/**
 * git diff --numstat 输出的单条记录
 * 格式：<added_lines>\t<deleted_lines>\t<file_path>
 */
export interface NumstatEntry {
    path: string;
    addedLines: number;
    deletedLines: number;
}
/**
 * 解析 git diff 指定范围的文件变更
 */
export declare function parseDiff(range: string): DiffFile[];
/**
 * 获取 diff 中新增的行（以 + 开头）
 */
export declare function getAddedLines(diffFile: DiffFile): string[];
/**
 * 获取 diff 中删除的行（以 - 开头）
 */
export declare function getRemovedLines(diffFile: DiffFile): string[];
/**
 * 解析 git diff --numstat 输出
 * 格式示例：
 *   10\t5\tsrc/index.ts
 *   0\t20\tsrc/legacy.ts
 *   200\t0\tsrc/new-file.ts
 * 第一列：添加行数，第二列：删除行数（- 表示二进制），第三列：文件路径
 */
export declare function parseNumstat(numstatOutput: string): NumstatEntry[];
//# sourceMappingURL=diff-parser.d.ts.map