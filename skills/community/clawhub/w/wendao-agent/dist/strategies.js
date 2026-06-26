const EXP_BASE = [40, 120, 350, 900, 2200, 5500, 14000, 35000];
const PK_TIERS = [1000n, 5000n, 10000n, 50000n, 100000n];
const e18 = 10n ** 18n;
function xpToNextLevel(realm, level) {
    const layer = ((level - 1) % 12) + 1;
    const pow13 = [1000, 2462, 4171, 6063, 8103, 10267, 12541, 14912, 17370, 19953, 22551, 25253];
    return BigInt(Math.floor(EXP_BASE[realm] * pow13[layer - 1] / 1000));
}
function canLevelUp(s) {
    const realmMax = (s.warrior.realm + 1) * 12;
    return s.warrior.level < realmMax && s.warrior.level < 96 && s.warrior.xp >= xpToNextLevel(s.warrior.realm, s.warrior.level);
}
function canBreakthrough(s) {
    const realmMax = (s.warrior.realm + 1) * 12;
    return s.warrior.level === realmMax && s.warrior.realm < 7;
}
function bestAffordableTier(balance) {
    for (let i = 4; i >= 0; i--) {
        if (balance >= PK_TIERS[i] * e18)
            return i;
    }
    return -1;
}
/** 激进策略：优先 PK，高频战斗 */
export const aggressiveStrategy = {
    name: "aggressive",
    shouldMeditate: (s) => !s.isMeditating && !s.isInPK && s.warrior.xp < xpToNextLevel(s.warrior.realm, s.warrior.level),
    shouldStopMeditation: (s) => s.isMeditating && s.pendingXP > 0 && (Date.now() / 1000 - s.meditationStartTime) >= 3600,
    shouldLevelUp: canLevelUp,
    shouldBreakthrough: canBreakthrough,
    shouldPK: (s) => {
        if (s.isInPK || s.isMeditating)
            return { should: false, tier: 0 };
        const tier = bestAffordableTier(s.jwBalance);
        return { should: tier >= 0, tier: Math.min(tier, 2) }; // 激进但不超仙境
    },
    distributeSP: (_s, points) => {
        // SDK-04 fix: 激进策略，防止 ceil 溢出
        if (points <= 0)
            return [0, 0, 0, 0, 0];
        const alloc = [0, 0, 0, 0, 0];
        alloc[0] = Math.floor(points * 0.4); // STR
        alloc[1] = Math.floor(points * 0.3); // AGI
        const rest = points - alloc[0] - alloc[1];
        alloc[2] = Math.floor(rest / 3); // END
        alloc[3] = Math.floor(rest / 3); // INT
        alloc[4] = rest - alloc[2] - alloc[3]; // CON (余数兜底)
        return alloc;
    },
};
/** 防守策略：重闭关质押，稳健成长 */
export const defensiveStrategy = {
    name: "defensive",
    shouldMeditate: (s) => !s.isMeditating && !s.isInPK,
    shouldStopMeditation: (s) => s.isMeditating && (Date.now() / 1000 - s.meditationStartTime) >= 28800, // 8小时才出关
    shouldLevelUp: canLevelUp,
    shouldBreakthrough: canBreakthrough,
    shouldPK: () => ({ should: false, tier: 0 }), // 不打 PK
    distributeSP: (_s, points) => {
        // SDK-04 fix: 防守策略，防止 ceil 溢出
        if (points <= 0)
            return [0, 0, 0, 0, 0];
        const alloc = [0, 0, 0, 0, 0];
        alloc[2] = Math.floor(points * 0.35); // END
        alloc[4] = Math.floor(points * 0.35); // CON
        alloc[0] = Math.floor(points * 0.1); // STR
        alloc[1] = Math.floor(points * 0.1); // AGI
        alloc[3] = points - alloc[0] - alloc[1] - alloc[2] - alloc[4]; // INT (余数兜底)
        return alloc;
    },
};
/** 均衡策略：平衡修炼和 PK */
export const balancedStrategy = {
    name: "balanced",
    shouldMeditate: (s) => !s.isMeditating && !s.isInPK,
    shouldStopMeditation: (s) => s.isMeditating && (Date.now() / 1000 - s.meditationStartTime) >= 14400, // 4小时出关
    shouldLevelUp: canLevelUp,
    shouldBreakthrough: canBreakthrough,
    shouldPK: (s) => {
        if (s.isInPK || s.isMeditating)
            return { should: false, tier: 0 };
        const tier = bestAffordableTier(s.jwBalance);
        return { should: tier >= 0, tier: Math.min(tier, 1) }; // 只打凡境/灵境
    },
    distributeSP: (_s, points) => {
        // 均衡分配
        const each = Math.floor(points / 5);
        const alloc = [each, each, each, each, 0];
        alloc[4] = points - each * 4;
        return alloc;
    },
};
export function getStrategy(name) {
    switch (name) {
        case "aggressive": return aggressiveStrategy;
        case "defensive": return defensiveStrategy;
        case "balanced": return balancedStrategy;
        default: return balancedStrategy;
    }
}
//# sourceMappingURL=strategies.js.map