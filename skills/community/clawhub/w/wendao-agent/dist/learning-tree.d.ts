import type { ActionLog } from "./types.js";
export declare class LearningTree {
    private leaves;
    private persistPath;
    /** SDK-07: 可选持久化路径 */
    constructor(persistPath?: string);
    /** 添加一条行为日志到 Merkle Tree */
    addEntry(log: ActionLog): void;
    /** 获取 Merkle Root */
    getRoot(): `0x${string}`;
    /** 获取叶子数量 */
    getLeafCount(): number;
    /** 将 Merkle Root 写入链上 NFA 合约 */
    updateOnChain(walletClient: {
        writeContract: (args: any) => Promise<string>;
    }, nfaAddress: string, tokenId: number): Promise<string>;
    /** SDK-07: 从磁盘加载叶子 */
    private _loadFromDisk;
    /** SDK-07: 保存叶子到磁盘 */
    private _saveToDisk;
}
//# sourceMappingURL=learning-tree.d.ts.map