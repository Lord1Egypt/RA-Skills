/**
 * WenDaoAgent — NFA 自主修仙 Agent
 * BAP-578 标准 Agent Skill 实现
 */
import { createPublicClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { bsc } from "viem/chains";
import { NFA_ABI, VAULT_ABI, TOKEN_ABI } from "./abi.js";
import { getStrategy } from "./strategies.js";
import { LearningTree } from "./learning-tree.js";
export class WenDaoAgent {
    config;
    strategy;
    account;
    publicClient;
    walletClient;
    running = false;
    logs = [];
    learningTree;
    successCount = 0;
    jwt; // JWT 独立存储，不受 Object.freeze 影响
    onAction;
    onError;
    onStateUpdate;
    constructor(config) {
        // SDK-02: freeze config 防止外部修改（含私钥）
        this.config = Object.freeze({ interval: 300, ...config });
        this.jwt = config.jwt;
        this.strategy = typeof config.strategy === "string"
            ? getStrategy(config.strategy)
            : config.strategy;
        this.account = privateKeyToAccount(config.agentPrivateKey);
        this.publicClient = createPublicClient({ chain: bsc, transport: http(config.rpcUrl) });
        this.walletClient = createWalletClient({ account: this.account, chain: bsc, transport: http(config.rpcUrl) });
        // SDK-07: 用持久化路径初始化 LearningTree
        this.learningTree = new LearningTree(`.wendao-tree-${config.tokenId}.json`);
    }
    on(event, cb) {
        if (event === "action")
            this.onAction = cb;
        if (event === "error")
            this.onError = cb;
        if (event === "stateUpdate")
            this.onStateUpdate = cb;
        return this;
    }
    /** 读取链上完整状态 */
    async getState() {
        const { nfa, vault, token } = this.config.contracts;
        const tokenId = BigInt(this.config.tokenId);
        const [warrior, owner, agentWallet, medInfo, inPK, jwBal, bnbBal] = await Promise.all([
            this.publicClient.readContract({ address: nfa, abi: NFA_ABI, functionName: "getWarrior", args: [tokenId] }),
            this.publicClient.readContract({ address: nfa, abi: NFA_ABI, functionName: "ownerOf", args: [tokenId] }),
            this.publicClient.readContract({ address: nfa, abi: NFA_ABI, functionName: "getAgentWallet", args: [tokenId] }),
            this.publicClient.readContract({ address: vault, abi: VAULT_ABI, functionName: "getMeditationInfo", args: [tokenId] }),
            this.publicClient.readContract({ address: vault, abi: VAULT_ABI, functionName: "inPK", args: [tokenId] }),
            this.publicClient.readContract({ address: token, abi: TOKEN_ABI, functionName: "balanceOf", args: [this.account.address] }),
            this.publicClient.getBalance({ address: this.account.address }),
        ]);
        const w = warrior;
        const stakeInfo = await this.publicClient.readContract({
            address: vault, abi: VAULT_ABI, functionName: "getStakeInfo", args: [owner],
        });
        const EXP_BASE = [40, 120, 350, 900, 2200, 5500, 14000, 35000];
        const layer = ((w.level - 1) % 12) + 1;
        const pow13 = [1000, 2462, 4171, 6063, 8103, 10267, 12541, 14912, 17370, 19953, 22551, 25253];
        const xpNeeded = BigInt(Math.floor(EXP_BASE[w.realm] * pow13[layer - 1] / 1000));
        return {
            warrior: w,
            tokenId: this.config.tokenId,
            ownerAddress: owner,
            agentAddress: agentWallet,
            jwBalance: jwBal,
            bnbBalance: bnbBal,
            staked: stakeInfo[0],
            pendingReward: stakeInfo[1],
            isMeditating: Number(medInfo[0]) > 0,
            meditationStartTime: Number(medInfo[0]),
            pendingXP: Number(medInfo[1]),
            isInPK: inPK,
            xpToNextLevel: xpNeeded,
        };
    }
    /** 执行单次决策循环 */
    async tick() {
        const actions = [];
        try {
            const state = await this.getState();
            this.onStateUpdate?.(state);
            // 1. 升级
            if (this.strategy.shouldLevelUp(state)) {
                const log = await this.execLevelUp(state);
                actions.push(log);
            }
            // 2. SP 分配
            if (state.warrior.unspentSP > 0) {
                const log = await this.execDistributeSP(state);
                actions.push(log);
            }
            // 3. 渡劫
            if (this.strategy.shouldBreakthrough(state)) {
                const log = await this.execBreakthrough(state);
                actions.push(log);
            }
            // 4. 闭关管理
            if (this.strategy.shouldStopMeditation(state)) {
                const log = await this.execStopMeditation(state);
                actions.push(log);
            }
            if (this.strategy.shouldMeditate(state)) {
                const log = await this.execStartMeditation(state);
                actions.push(log);
            }
            // 5. PK — C-15: 如果已在 PK（上次 deposit 后 resolve 失败），先尝试恢复
            if (state.isInPK && this.config.apiUrl && this.jwt) {
                const log = await this.execPKRecover(state);
                actions.push(log);
            }
            else {
                const pkDecision = this.strategy.shouldPK(state);
                if (pkDecision.should) {
                    const log = await this.execPK(state, pkDecision.tier);
                    actions.push(log);
                }
            }
            // 6. 灵气奖励和质押奖励均需 owner 手动领取（agent 钱包无 NFA，claimSpiritReward 会被拒）
        }
        catch (err) {
            const error = err instanceof Error ? err : new Error(String(err));
            this.onError?.(error);
            actions.push({ timestamp: Date.now(), action: "error", details: error.message, success: false });
        }
        // Record successful actions in learning tree
        const prevCount = this.successCount;
        for (const a of actions) {
            if (a.success) {
                this.learningTree.addEntry(a);
                this.successCount++;
            }
        }
        // Auto-persist merkle root every 10 successful actions
        if (this.successCount >= 10 && Math.floor(this.successCount / 10) > Math.floor(prevCount / 10)) {
            try {
                await this.learningTree.updateOnChain(this.walletClient, this.config.contracts.nfa, this.config.tokenId);
            }
            catch (_e) {
                // Silently fail — merkle update is non-critical
            }
        }
        this.logs.push(...actions);
        return actions;
    }
    /** 自动获取 Agent JWT（通过签名验证身份） */
    async authenticate() {
        if (this.jwt || !this.config.apiUrl)
            return;
        try {
            const timestamp = Math.floor(Date.now() / 1000);
            const message = `wendao-agent-auth:${this.config.tokenId}:${timestamp}`;
            const signature = await this.account.signMessage({ message });
            const res = await fetch(`${this.config.apiUrl}/api/auth/agent`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ tokenId: this.config.tokenId, agentAddress: this.account.address, signature, timestamp }),
            });
            if (!res.ok)
                throw new Error(`Agent auth failed: ${res.status}`);
            const data = await res.json();
            this.jwt = data.jwt;
            console.log("🔑 Agent JWT 获取成功");
        }
        catch (e) {
            console.error("⚠️ Agent 认证失败（PK 功能不可用）:", e.message);
        }
    }
    /** 启动 Agent 循环 */
    async start() {
        this.running = true;
        console.log(`🏮 WenDao Agent 启动 | tokenId: ${this.config.tokenId} | 策略: ${this.strategy.name}`);
        console.log(`   Agent 钱包: ${this.account.address}`);
        console.log(`   间隔: ${this.config.interval}s`);
        // 启动时自动认证获取 JWT
        await this.authenticate();
        while (this.running) {
            const actions = await this.tick();
            for (const a of actions) {
                const icon = a.success ? "✅" : "❌";
                console.log(`${icon} [${new Date(a.timestamp).toLocaleTimeString()}] ${a.action}: ${a.details}`);
                this.onAction?.(a);
            }
            await new Promise(r => setTimeout(r, (this.config.interval ?? 300) * 1000));
        }
    }
    /** 停止 Agent */
    stop() {
        this.running = false;
        console.log("🛑 Agent 已停止");
    }
    /** 获取行动日志 */
    getLogs() { return [...this.logs]; }
    // ═══ 执行器 ═══
    async execLevelUp(_state) {
        try {
            const hash = await this.walletClient.writeContract({
                address: this.config.contracts.nfa, abi: NFA_ABI,
                functionName: "levelUp", args: [BigInt(this.config.tokenId)],
            });
            return { timestamp: Date.now(), action: "levelUp", details: `升级成功`, txHash: hash, success: true };
        }
        catch (e) {
            return { timestamp: Date.now(), action: "levelUp", details: `失败: ${e.message?.slice(0, 80)}`, success: false };
        }
    }
    async execDistributeSP(state) {
        try {
            const alloc = this.strategy.distributeSP(state, state.warrior.unspentSP);
            const hash = await this.walletClient.writeContract({
                address: this.config.contracts.nfa, abi: NFA_ABI,
                functionName: "distributeSP", args: [BigInt(this.config.tokenId), alloc],
            });
            return { timestamp: Date.now(), action: "distributeSP", details: `分配 ${state.warrior.unspentSP} SP: [${alloc}]`, txHash: hash, success: true };
        }
        catch (e) {
            return { timestamp: Date.now(), action: "distributeSP", details: `失败: ${e.message?.slice(0, 80)}`, success: false };
        }
    }
    async execBreakthrough(state) {
        try {
            // C-04: 先 approve 渡劫费用再 payBreakthrough
            const COSTS = [0n, 80n, 250n, 700n, 2200n, 7000n, 22000n, 70000n];
            const nextRealm = state.warrior.realm + 1;
            const cost = COSTS[nextRealm] ?? 0n;
            const e18 = 10n ** 18n;
            if (cost > 0n) {
                await this.walletClient.writeContract({
                    address: this.config.contracts.token, abi: TOKEN_ABI,
                    functionName: "approve", args: [this.config.contracts.vault, cost * e18],
                });
            }
            const hash = await this.walletClient.writeContract({
                address: this.config.contracts.vault, abi: VAULT_ABI,
                functionName: "payBreakthrough", args: [BigInt(this.config.tokenId)],
            });
            return { timestamp: Date.now(), action: "breakthrough", details: `渡劫成功`, txHash: hash, success: true };
        }
        catch (e) {
            return { timestamp: Date.now(), action: "breakthrough", details: `失败: ${e.message?.slice(0, 80)}`, success: false };
        }
    }
    async execStartMeditation(_state) {
        try {
            const hash = await this.walletClient.writeContract({
                address: this.config.contracts.vault, abi: VAULT_ABI,
                functionName: "startMeditation", args: [BigInt(this.config.tokenId)],
            });
            return { timestamp: Date.now(), action: "startMeditation", details: `开始闭关`, txHash: hash, success: true };
        }
        catch (e) {
            return { timestamp: Date.now(), action: "startMeditation", details: `失败: ${e.message?.slice(0, 80)}`, success: false };
        }
    }
    async execStopMeditation(_state) {
        try {
            const hash = await this.walletClient.writeContract({
                address: this.config.contracts.vault, abi: VAULT_ABI,
                functionName: "stopMeditation", args: [BigInt(this.config.tokenId)],
            });
            return { timestamp: Date.now(), action: "stopMeditation", details: `出关`, txHash: hash, success: true };
        }
        catch (e) {
            return { timestamp: Date.now(), action: "stopMeditation", details: `失败: ${e.message?.slice(0, 80)}`, success: false };
        }
    }
    // C-15 + SDK-03: PK 恢复 — 已 deposit 但未 resolve 时重试匹配；超时后自动 cancelPK
    async execPKRecover(_state) {
        try {
            // SDK-03: 检查是否已超过 1h 锁定期，可以 cancel
            const depositTime = await this.publicClient.readContract({
                address: this.config.contracts.vault, abi: VAULT_ABI,
                functionName: "pkDepositTime", args: [BigInt(this.config.tokenId)],
            });
            const elapsed = BigInt(Math.floor(Date.now() / 1000)) - depositTime;
            const MIN_PK_LOCK = 3600n; // 1 hour
            // 如果锁定超过 2h 且仍未匹配到对手，自动 cancel
            if (elapsed > MIN_PK_LOCK * 2n) {
                const hash = await this.walletClient.writeContract({
                    address: this.config.contracts.vault, abi: VAULT_ABI,
                    functionName: "cancelPK", args: [BigInt(this.config.tokenId)],
                });
                return { timestamp: Date.now(), action: "pk-cancel", details: `超时自动取消 PK`, txHash: hash, success: true };
            }
            if (!this.config.apiUrl || !this.jwt) {
                return { timestamp: Date.now(), action: "pk-recover", details: `无API配置，${elapsed > MIN_PK_LOCK ? "可手动 cancelPK" : "等待锁定期结束"}`, success: false };
            }
            // 读取链上实际 tier，不能写死 0
            const onChainTier = Number(await this.publicClient.readContract({
                address: this.config.contracts.vault, abi: VAULT_ABI,
                functionName: "pkTierOf", args: [BigInt(this.config.tokenId)],
            }));
            const res = await fetch(`${this.config.apiUrl}/api/battle/resolve`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${this.jwt}` },
                body: JSON.stringify({ tokenId: this.config.tokenId, tier: onChainTier }),
            });
            const result = await res.json();
            if (result.status === "waiting") {
                return { timestamp: Date.now(), action: "pk-recover", details: `继续等待对手 (${Number(elapsed) / 60 | 0}min)`, success: true };
            }
            if (result.status === "resolved" && result.signature) {
                await this.walletClient.writeContract({
                    address: this.config.contracts.vault, abi: VAULT_ABI,
                    functionName: "settlePK",
                    args: [BigInt(result.winner), BigInt(result.loser), result.tier, BigInt(result.nonce), result.signature],
                });
                return { timestamp: Date.now(), action: "pk-recover", details: `PK 恢复结算成功`, success: true };
            }
            return { timestamp: Date.now(), action: "pk-recover", details: `恢复异常: ${result.message || "unknown"}`, success: false };
        }
        catch (e) {
            return { timestamp: Date.now(), action: "pk-recover", details: `恢复失败: ${e.message?.slice(0, 80)}`, success: false };
        }
    }
    async execPK(_state, tier) {
        try {
            const PK_AMOUNTS = [1000n, 5000n, 10000n, 50000n, 100000n];
            const amount = PK_AMOUNTS[tier] * (10n ** 18n);
            // 1. Approve $JW
            await this.walletClient.writeContract({
                address: this.config.contracts.token, abi: TOKEN_ABI,
                functionName: "approve", args: [this.config.contracts.vault, amount],
            });
            // 2. DepositPK 链上锁定
            await this.walletClient.writeContract({
                address: this.config.contracts.vault, abi: VAULT_ABI,
                functionName: "depositPK", args: [BigInt(this.config.tokenId), tier],
            });
            // 3. 调后端匹配 + 战斗模拟
            if (!this.config.apiUrl || !this.jwt) {
                return { timestamp: Date.now(), action: "depositPK", details: `已锁定灵石，但无 API/JWT 配置，无法匹配`, success: true };
            }
            const resolveRes = await fetch(`${this.config.apiUrl}/api/battle/resolve`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${this.jwt}` },
                body: JSON.stringify({ tokenId: this.config.tokenId, tier }),
            });
            const battleResult = await resolveRes.json();
            if (battleResult.status === "waiting") {
                return { timestamp: Date.now(), action: "pk-waiting", details: battleResult.message || "等待对手", success: true };
            }
            if (battleResult.status !== "resolved" || !battleResult.signature) {
                return { timestamp: Date.now(), action: "pk-error", details: `匹配异常: ${battleResult.message || "unknown"}`, success: false };
            }
            // 4. SettlePK 链上结算
            const settleTx = await this.walletClient.writeContract({
                address: this.config.contracts.vault, abi: VAULT_ABI,
                functionName: "settlePK",
                args: [BigInt(battleResult.winner), BigInt(battleResult.loser), tier, BigInt(battleResult.nonce), battleResult.signature],
            });
            const won = battleResult.winner === this.config.tokenId;
            return {
                timestamp: Date.now(),
                action: won ? "pk-win" : "pk-lose",
                details: `${won ? "胜" : "负"} Tier ${tier} | ${won ? "+" : "-"}灵石`,
                txHash: settleTx,
                success: true,
            };
        }
        catch (e) {
            return { timestamp: Date.now(), action: "pk", details: `失败: ${e.message?.slice(0, 100)}`, success: false };
        }
    }
}
//# sourceMappingURL=agent.js.map