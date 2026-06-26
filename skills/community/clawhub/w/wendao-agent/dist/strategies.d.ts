/** 内置策略 — aggressive / defensive / balanced */
import type { CustomStrategy } from "./types.js";
/** 激进策略：优先 PK，高频战斗 */
export declare const aggressiveStrategy: CustomStrategy;
/** 防守策略：重闭关质押，稳健成长 */
export declare const defensiveStrategy: CustomStrategy;
/** 均衡策略：平衡修炼和 PK */
export declare const balancedStrategy: CustomStrategy;
export declare function getStrategy(name: string): CustomStrategy;
//# sourceMappingURL=strategies.d.ts.map