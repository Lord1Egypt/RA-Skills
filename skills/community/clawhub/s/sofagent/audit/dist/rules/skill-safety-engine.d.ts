import { type SafetyHit } from './skill-safety-rules';
/**
 * 递归找出所有需扫描的文件。
 * 跳过隐藏目录和 node_modules。
 */
export declare function findFiles(target: string): string[];
/**
 * 扫描单个文件，返回命中列表。
 */
export declare function scanFile(filePath: string): SafetyHit[];
//# sourceMappingURL=skill-safety-engine.d.ts.map