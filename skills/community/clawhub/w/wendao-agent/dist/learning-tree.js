/**
 * BAP-578 Learning Tree — 链上行为存证
 * 将 Agent 行为日志构建为 Merkle Tree，定期上链
 */
import { keccak256, encodePacked } from "viem";
import { NFA_ABI } from "./abi.js";
import { readFileSync, writeFileSync, existsSync } from "fs";
export class LearningTree {
    leaves = [];
    persistPath = null;
    /** SDK-07: 可选持久化路径 */
    constructor(persistPath) {
        if (persistPath) {
            this.persistPath = persistPath;
            this._loadFromDisk();
        }
    }
    /** 添加一条行为日志到 Merkle Tree */
    addEntry(log) {
        const leaf = keccak256(encodePacked(["uint256", "string", "string"], [BigInt(log.timestamp), log.action, log.details]));
        this.leaves.push(leaf);
        this._saveToDisk();
    }
    /** 获取 Merkle Root */
    getRoot() {
        if (this.leaves.length === 0) {
            return "0x0000000000000000000000000000000000000000000000000000000000000000";
        }
        let layer = [...this.leaves];
        while (layer.length > 1) {
            const next = [];
            for (let i = 0; i < layer.length; i += 2) {
                if (i + 1 < layer.length) {
                    // Sort pair to ensure consistent ordering
                    const [a, b] = layer[i] < layer[i + 1] ? [layer[i], layer[i + 1]] : [layer[i + 1], layer[i]];
                    next.push(keccak256(encodePacked(["bytes32", "bytes32"], [a, b])));
                }
                else {
                    // SDK-06 fix: 奇数叶子直接提升到上一层，不自身 hash（避免 root 碰撞）
                    next.push(layer[i]);
                }
            }
            layer = next;
        }
        return layer[0];
    }
    /** 获取叶子数量 */
    getLeafCount() {
        return this.leaves.length;
    }
    /** 将 Merkle Root 写入链上 NFA 合约 */
    async updateOnChain(walletClient, nfaAddress, tokenId) {
        const root = this.getRoot();
        const hash = await walletClient.writeContract({
            address: nfaAddress,
            abi: NFA_ABI,
            functionName: "updateLearningTree",
            args: [BigInt(tokenId), root],
        });
        return hash;
    }
    /** SDK-07: 从磁盘加载叶子 */
    _loadFromDisk() {
        if (!this.persistPath || !existsSync(this.persistPath))
            return;
        try {
            const data = JSON.parse(readFileSync(this.persistPath, "utf-8"));
            if (Array.isArray(data.leaves)) {
                this.leaves = data.leaves;
            }
        }
        catch {
            // 文件损坏，重置
            this.leaves = [];
        }
    }
    /** SDK-07: 保存叶子到磁盘 */
    _saveToDisk() {
        if (!this.persistPath)
            return;
        try {
            writeFileSync(this.persistPath, JSON.stringify({ leaves: this.leaves }), "utf-8");
        }
        catch {
            // 静默失败，不阻塞主流程
        }
    }
}
//# sourceMappingURL=learning-tree.js.map