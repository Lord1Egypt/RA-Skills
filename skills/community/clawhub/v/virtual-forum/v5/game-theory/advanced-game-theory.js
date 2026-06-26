/**
 * 虚拟论坛 - 高级博弈论模块 v3.9
 * Advanced Game Theory Module v3.9
 * 
 * v3.8基础上新增：
 * P1: 议价博弈 (Rubinstein Bargaining) + 联盟博弈 (Shapley Value)
 * 
 * 理论依据：
 * - Rubinstein (1982) - 轮流议价模型
 * - Shapley (1953) - 联盟博弈与核心
 */

const SubagentArena = require('../subagent-arena.js');
const { DEFAULTS } = require('../shared-config.js');

// ============================================================
// 第一部分：v3.8 核心模块（信号博弈、重复博弈、信息设计）
// ============================================================

/**
 * 信号博弈基础类
 */
class SignalingGame {
    constructor() {
        this.signalCosts = {
            'strong_claim': 0.8,
            'weak_claim': 0.3,
            'evidence_backed': 0.9,
            'assertion': 0.2,
            'counterargument': 0.6,
            'concession': 0.5,
        };

        this.signalTypes = {
            'strong_claim': ['必须', '绝对', '显然', '毫无疑问', '必然'],
            'weak_claim': ['可能', '也许', '不确定', '大概'],
            'evidence_backed': ['因为', '数据', '研究', '证据', '表明', '根据'],
            'assertion': ['我认为', '我觉得', '应该', '相信'],
            'counterargument': ['但是', '然而', '不对', '反对'],
            'concession': ['同意', '有道理', '承认'],
        };
    }

    assessSignalCredibility(content, speakerType, priorBelief = 0.5) {
        if (!content) return { credible: false, confidence: 0, reason: '空发言' };

        const signalType = this._identifySignalType(content);
        const signalCost = this.signalCosts[signalType] || 0.5;
        const likelihoodRatio = this._calculateLikelihoodRatio(speakerType, signalType);
        
        const posteriorOdds = likelihoodRatio * (priorBelief / (1 - priorBelief));
        const posterior = posteriorOdds / (1 + posteriorOdds);
        const isSeparating = this._checkSeparatingEquilibrium(signalCost, speakerType);
        const signalInfo = this._calculateMutualInformation(signalType, speakerType);

        return {
            signalType,
            signalCost,
            prior: priorBelief,
            posterior,
            likelihoodRatio,
            isSeparating,
            signalInfo,
            credible: posterior > priorBelief && signalCost > 0.4,
            confidence: Math.abs(posterior - priorBelief) + signalCost,
            reason: this._generateCredibilityReason(signalType, signalCost, isSeparating, posterior),
        };
    }

    _identifySignalType(content) {
        for (const [type, keywords] of Object.entries(this.signalTypes)) {
            if (keywords.some(kw => content.includes(kw))) {
                return type;
            }
        }
        return 'assertion';
    }

    _calculateLikelihoodRatio(speakerType, signalType) {
        const probs = {
            expert: { strong_claim: 0.8, weak_claim: 0.3, evidence_backed: 0.9, assertion: 0.4, counterargument: 0.7, concession: 0.5 },
            layman: { strong_claim: 0.3, weak_claim: 0.7, evidence_backed: 0.2, assertion: 0.6, counterargument: 0.3, concession: 0.6 },
            strategic: { strong_claim: 0.6, weak_claim: 0.5, evidence_backed: 0.3, assertion: 0.8, counterargument: 0.6, concession: 0.7 },
        };

        const pSignalGivenType = probs[speakerType]?.[signalType] || 0.5;
        const pSignalGivenNotType = 0.3;
        return pSignalGivenType / pSignalGivenNotType;
    }

    _checkSeparatingEquilibrium(signalCost, speakerType) {
        if (speakerType === 'expert' && signalCost >= 0.7) return true;
        if (speakerType === 'layman' && signalCost <= 0.3) return false;
        return signalCost > 0.5;
    }

    _calculateMutualInformation(signalType, speakerType) {
        const typeMatchScore = { expert: 1.0, layman: 0.5, strategic: 0.7 };
        const cost = this.signalCosts[signalType] || 0.5;
        return cost * (typeMatchScore[speakerType] || 0.5);
    }

    _generateCredibilityReason(signalType, signalCost, isSeparating, posterior) {
        if (isSeparating && signalCost > 0.6) {
            return `分离均衡信号：${signalType}，后验=${posterior.toFixed(2)}`;
        } else if (posterior > 0.6) {
            return `高可信信号：后验=${posterior.toFixed(2)}`;
        } else if (posterior < 0.4) {
            return `低可信信号：后验=${posterior.toFixed(2)}`;
        }
        return `中等可信：需要更多信号验证`;
    }
}


/**
 * 合作追踪器
 */
class CooperationTracker {
    constructor() {
        this.history = [];
        this.punishmentPhase = {};
        this.cooperationCount = {};
        this.defectionCount = {};
    }

    recordAction(player, action, cooperated) {
        this.history.push({ player, action, cooperated, round: this.history.length + 1 });
        
        if (!this.cooperationCount[player]) this.cooperationCount[player] = 0;
        if (!this.defectionCount[player]) this.defectionCount[player] = 0;
        
        if (cooperated) this.cooperationCount[player]++;
        else this.defectionCount[player]++;
    }

    getCooperationRate(player = null) {
        if (player) {
            const total = this.cooperationCount[player] + this.defectionCount[player];
            return total > 0 ? this.cooperationCount[player] / total : 0;
        }
        
        const allCooperations = Object.values(this.cooperationCount).reduce((a, b) => a + b, 0);
        const allDefections = Object.values(this.defectionCount).reduce((a, b) => a + b, 0);
        const total = allCooperations + allDefections;
        return total > 0 ? allCooperations / total : 0;
    }

    isInPunishment(player) {
        return this.punishmentPhase[player] || false;
    }

    startPunishment(player) {
        this.punishmentPhase[player] = true;
    }

    maybeEndPunishment(player, otherPlayer) {
        const myLastAction = this.history.filter(h => h.player === player).pop();
        const otherLastAction = this.history.filter(h => h.player === otherPlayer).pop();
        
        if (myLastAction?.cooperated && otherLastAction?.cooperated) {
            this.punishmentPhase[player] = false;
            return true;
        }
        return false;
    }

    getSummary() {
        return {
            totalRounds: this.history.length,
            overallCooperationRate: this.getCooperationRate(),
            players: Object.keys(this.cooperationCount).map(p => ({
                name: p,
                cooperationRate: this.getCooperationRate(p),
                inPunishment: this.isInPunishment(p),
            })),
        };
    }
}


/**
 * 重复博弈引擎
 */
class RepeatedGameEngine {
    constructor(discountFactor = 0.9) {
        this.discountFactor = discountFactor;
        this.cooperationTracker = new CooperationTracker();
        this.strategies = {
            GRIM_TRIGGER: 'grim',
            TIT_FOR_TAT: 'tft',
            GENEROUS_TFT: 'gtft',
            SUSPICIOUS_TFT: 'stft',
        };
    }

    getStrategicAdvice(player, opponent, strategyType = 'tft') {
        const history = this._getPlayerHistory(player, opponent);
        const opponentLastAction = this._getOpponentLastAction(opponent);
        
        let recommendedAction;
        let reason;
        
        switch (strategyType) {
            case 'grim':
                recommendedAction = this._grimTriggerDecision(history, opponentLastAction);
                reason = '冷酷策略：一但背叛，永远惩罚';
                break;
            case 'tft':
                recommendedAction = this._titForTatDecision(opponentLastAction);
                reason = '针锋相对：合作取决于对手上一轮';
                break;
            case 'gtft':
                recommendedAction = this._generousTFTDecision(opponentLastAction);
                reason = '宽容针锋相对：偶尔原谅背叛';
                break;
            case 'stft':
                recommendedAction = this._suspiciousTFTDecision(opponentLastAction, history);
                reason = '怀疑性针锋相对：需要两次合作才原谅';
                break;
            default:
                recommendedAction = 'cooperate';
                reason = '默认合作';
        }

        if (this.cooperationTracker.isInPunishment(player)) {
            recommendedAction = 'defect';
            reason += ' | 处于惩罚阶段';
        }

        return {
            recommendedAction,
            reason,
            strategyType,
            discountFactor: this.discountFactor,
            cooperationRate: this.cooperationTracker.getCooperationRate(player),
        };
    }

    _grimTriggerDecision(history, opponentLastAction) {
        // [P0 FIX] grim trigger：正确逻辑是检查opponent是否背叛
        // 一旦opponent背叛，就永远惩罚（defect）
        // history参数保留用于未来扩展（如追踪背叛次数）
        if (opponentLastAction === null) return 'cooperate';  // 第一轮默认合作
        return opponentLastAction ? 'cooperate' : 'defect';
    }

    _titForTatDecision(opponentLastAction) {
        if (opponentLastAction === null) return 'cooperate';
        return opponentLastAction ? 'cooperate' : 'defect';
    }

    _generousTFTDecision(opponentLastAction) {
        if (opponentLastAction === null) return 'cooperate';
        return opponentLastAction ? 'cooperate' : (Math.random() < 0.1 ? 'cooperate' : 'defect');
    }

    _suspiciousTFTDecision(opponentLastAction, history) {
        const recentCooperations = history.slice(-2).filter(h => h.cooperated).length;
        return recentCooperations >= 2 ? 'cooperate' : 'defect';
    }

    _getPlayerHistory(player, opponent) {
        return this.cooperationTracker.history.filter(h => h.player === player);
    }

    _getOpponentLastAction(opponent) {
        const last = this.cooperationTracker.history.filter(h => h.player === opponent).pop();
        return last ? last.cooperated : null;
    }

    calculateTemptationThreshold() {
        return 1 / (1 - this.discountFactor);
    }

    isInCooperationZone() {
        return this.cooperationTracker.getCooperationRate() > 0.6;
    }

    isInConflictZone() {
        return this.cooperationTracker.getCooperationRate() < 0.3;
    }

    getPhaseAnalysis() {
        const rate = this.cooperationTracker.getCooperationRate();
        
        if (rate > 0.7) {
            return { phase: 'COOPERATION', description: '已进入合作阶段', stability: '高', risk: '低' };
        } else if (rate > 0.4) {
            return { phase: 'TRANSITION', description: '处于过渡阶段', stability: '中', risk: '中' };
        } else if (rate > 0.0) {
            return { phase: 'CONFLICT', description: '处于冲突阶段', stability: '低', risk: '高' };
        }
        
        return { phase: 'UNKNOWN', description: '暂无足够历史数据', stability: '未知', risk: '未知' };
    }

    recordRound(player, action, cooperated) {
        this.cooperationTracker.recordAction(player, action, cooperated);
    }
}


/**
 * 信息设计器
 */
class InformationDesigner {
    constructor() {
        this.disclosureModes = {
            FULL: 'full',
            STRATEGIC: 'strategic',
            CONDITIONAL: 'conditional',
        };
    }

    suggestDisclosure(topic, participantStates, currentBeliefs = {}) {
        const overconfident = participantStates.filter(s => s.confidence > 0.8);
        const uncertain = participantStates.filter(s => s.confidence < 0.4);

        const diagnosis = this._diagnoseInformationProblem(participantStates, currentBeliefs);
        const recommendation = this._generateRecommendation(diagnosis, overconfident, uncertain);

        return {
            mode: recommendation.mode,
            diagnosis,
            content: recommendation.content,
            expectedImpact: recommendation.expectedImpact,
            rationale: recommendation.rationale,
        };
    }

    _diagnoseInformationProblem(participantStates, currentBeliefs) {
        const problems = [];

        const overconfident = participantStates.filter(s => s.confidence > 0.8);
        if (overconfident.length > participantStates.length / 2) {
            problems.push('OVERCONFIDENT_DOMINANT');
        }

        const beliefVariance = this._calculateBeliefVariance(currentBeliefs);
        if (beliefVariance > 0.3) {
            problems.push('BELIEF_DIVERGENCE');
        }

        const infoHaves = participantStates.filter(s => s.hasEvidence);
        const infoHaveNots = participantStates.filter(s => !s.hasEvidence);
        if (infoHaves.length > 0 && infoHaveNots.length > 0) {
            problems.push('INFORMATION_ASYMMETRY');
        }

        return problems.length > 0 ? problems : ['BALANCED'];
    }

    _calculateBeliefVariance(beliefs) {
        if (Object.keys(beliefs).length < 2) return 0;
        
        const values = Object.values(beliefs);
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length;
        return variance;
    }

    _generateRecommendation(diagnosis, overconfident, uncertain) {
        if (diagnosis.includes('OVERCONFIDENT_DOMINANT')) {
            return {
                mode: this.disclosureModes.STRATEGIC,
                content: '提供反事实证据和反对观点',
                expectedImpact: '降低过度自信，促进实质性讨论',
                rationale: '多数人过度自信时，策略性披露反对方观点可以平衡讨论',
            };
        }

        if (diagnosis.includes('BELIEF_DIVERGENCE')) {
            return {
                mode: this.disclosureModes.STRATEGIC,
                content: '提供"共同知识"和事实基础',
                expectedImpact: '减少信念分歧，促进共识',
                rationale: '信念分歧大时，聚焦共同事实可以降低对立',
            };
        }

        if (diagnosis.includes('INFORMATION_ASYMMETRY')) {
            return {
                mode: this.disclosureModes.CONDITIONAL,
                content: '要求信息优势方披露来源，允许追问',
                expectedImpact: '减少信息不对称，提高论据质量',
                rationale: '信息不对称会破坏讨论公平性',
            };
        }

        return {
            mode: this.disclosureModes.FULL,
            content: '全面披露所有相关信息',
            expectedImpact: '维持现状，促进开放讨论',
            rationale: '当前状态平衡，无需干预',
        };
    }

    optimalSignalDesign(targetAction, priorBelief, payoffFunction) {
        const possibleSignals = ['strong_positive', 'weak_positive', 'neutral', 'weak_negative', 'strong_negative'];
        let bestSignal = 'neutral';
        let bestUtility = -Infinity;

        for (const signal of possibleSignals) {
            const posterior = this._updateBeliefGivenSignal(priorBelief, signal);
            const expectedUtility = payoffFunction(posterior, targetAction);
            
            if (expectedUtility > bestUtility) {
                bestUtility = expectedUtility;
                bestSignal = signal;
            }
        }

        return {
            recommendedSignal: bestSignal,
            expectedUtility: bestUtility,
            posteriorBelief: this._updateBeliefGivenSignal(priorBelief, bestSignal),
        };
    }

    _updateBeliefGivenSignal(prior, signal) {
        const signalStrengths = {
            'strong_positive': 0.8, 'weak_positive': 0.6, 'neutral': 0.5,
            'weak_negative': 0.4, 'strong_negative': 0.2,
        };
        
        const strength = signalStrengths[signal] || 0.5;
        return (prior + strength) / 2;
    }
}


// ============================================================
// 第二部分：P1 新增 - 议价博弈 (Bargaining Games)
// Rubinstein (1982) - 轮流议价模型
// ============================================================

/**
 * 议价博弈引擎
 * 
 * 核心问题：
 * - 蛋糕如何分配？
 * - 谁先出价？
 * - 耐心程度（折扣因子）如何影响结果？
 * 
 * Rubinstein均衡：
 * - 每人获得 = (1 - δ₂) / (1 - δ₁δ₂) 当1先出价
 * - 每人获得 = δ₁(1 - δ₂) / (1 - δ₁δ₂) 当2先出价
 */
class BargainingGame {
    constructor() {
        this.rounds = [];
        this.currentRound = 0;
        this.currentOffer = null;
        this.offerHistory = [];
    }

    /**
     * 计算Rubinstein均衡份额
     * 
     * @param {number} delta1 - 玩家1的折扣因子 (0 < δ ≤ 1)
     * @param {number} delta2 - 玩家2的折扣因子 (0 < δ ≤ 1)
     * @param {string} firstMover - 谁先出价: 'player1' | 'player2'
     * @returns {object} 均衡份额
     */
    calculateEquilibrium(delta1, delta2, firstMover = 'player1') {
        // 均衡条件：δ₂/(1-δ₁δ₂) vs δ₁/(1-δ₁δ₂)
        // 总蛋糕 = 1
        
        // [P0 FIX] 防止除零
        const denominator = 1 - delta1 * delta2;
        if (Math.abs(denominator) < 1e-9) {
            // δ₁=1 且 δ₂=1 时，双方平分
            return {
                player1: { share: 0.5, sharePercent: '50.0%' },
                player2: { share: 0.5, sharePercent: '50.0%' },
                firstMover,
                firstMoverAdvantage: '0.000',
                total: 1,
                equilibrium: 'Rubinstein (degenerate)',
                note: 'δ₁=δ₂=1时无时间成本，平分收益',
            };
        }
        
        let p1Share, p2Share;
        
        if (firstMover === 'player1') {
            // 玩家1先出价，获得更多
            p1Share = (1 - delta2) / denominator;
            p2Share = delta2 * (1 - delta1) / denominator;
        } else {
            // 玩家2先出价，获得更多
            p1Share = delta1 * (1 - delta2) / denominator;
            p2Share = (1 - delta1) / denominator;
        }

        // 计算先手优势
        const firstMoverAdvantage = Math.abs(p1Share - p2Share);

        return {
            player1: { share: p1Share, sharePercent: (p1Share * 100).toFixed(1) + '%' },
            player2: { share: p2Share, sharePercent: (p2Share * 100).toFixed(1) + '%' },
            firstMover,
            firstMoverAdvantage: firstMoverAdvantage.toFixed(3),
            total: p1Share + p2Share,
            equilibrium: 'Rubinstein',
        };
    }

    /**
     * 计算均衡（给定贴现因子）
     */
    calculateEquilibriumShares(delta1, delta2) {
        // [P0 FIX] 防止除零
        const denominator = 1 - delta1 * delta2;
        if (Math.abs(denominator) < 1e-9) {
            return {
                p1IfFirst: { share: 0.5, percent: '50.0%' },
                p2IfFirst: { share: 0.5, percent: '50.0%' },
                note: 'δ₁=δ₂=1时无时间成本，平分收益',
            };
        }

        // 玩家1的份额（当玩家1先出价时）
        const p1First = (1 - delta2) / denominator;
        
        // 玩家2的份额（当玩家2先出价时）
        const p2First = (1 - delta1) / denominator;
        
        return {
            p1IfFirst: { share: p1First, percent: (p1First * 100).toFixed(1) + '%' },
            p2IfFirst: { share: p2First, percent: (p2First * 100).toFixed(1) + '%' },
        };
    }

    /**
     * 生成出价建议
     * 
     * @param {string} player - 出价者
     * @param {number} myDelta - 出价者的折扣因子
     * @param {number} opponentDelta - 对手的折扣因子
     * @param {number} currentValue - 当前议题总价值
     * @param {number} roundNumber - 当前轮次
     */
    generateOffer(player, myDelta, opponentDelta, currentValue = 100, roundNumber = 1) {
        // 计算理论均衡份额
        const equilibrium = this.calculateEquilibrium(myDelta, opponentDelta);
        
        // 当前轮次的贴现值
        const discountedValue = currentValue * Math.pow(myDelta, roundNumber - 1);
        
        // 考虑对手的保留价值
        const myMinAccept = currentValue * 0.1;  // 最低接受阈值
        const oppMinAccept = currentValue * 0.1;
        
        // 生成出价
        // 理想出价：接近对手的均衡份额，但稍微让步以促进达成
        const idealOffer = equilibrium.player2.share * 0.9;  // 给对手留点余地
        
        const offer = {
            player,
            round: roundNumber,
            rawValue: currentValue,
            discountedValue: discountedValue.toFixed(2),
            suggestedShare: idealOffer.toFixed(3),
            suggestedAmount: (idealOffer * discountedValue).toFixed(2),
            minAcceptable: myMinAccept,
            equilibriumAnalysis: {
                ifIFirst: equilibrium.player1.sharePercent,
                ifOppFirst: equilibrium.player2.sharePercent,
            },
            strategy: this._getOfferStrategy(roundNumber, myDelta, opponentDelta),
        };

        this.currentOffer = offer;
        this.offerHistory.push(offer);
        return offer;
    }

    /**
     * 获取出价策略描述
     */
    _getOfferStrategy(round, myDelta, oppDelta) {
        const deltaRatio = myDelta / oppDelta;
        
        if (round === 1 && deltaRatio > 1) {
            return '激进先手：利用耐心优势争取更大份额';
        } else if (round === 1 && deltaRatio < 1) {
            return '保守先手：接受较少的均衡份额，快速达成';
        } else if (deltaRatio > 1.2) {
            return '耐心优势：可以等更久，拖时间有利';
        } else if (deltaRatio < 0.8) {
            return '耐心劣势：尽快达成，否则损失增加';
        }
        return '对等博弈：份额取决于谁先出价';
    }

    /**
     * 评估是否接受当前出价
     * 
     * @param {string} player - 被评估的玩家
     * @param {number} offeredShare - 收到的份额 (0-1)
     * @param {number} myDelta - 我的折扣因子
     * @param {number} opponentDelta - 对手的折扣因子
     * @param {number} roundNumber - 当前轮次
     */
    evaluateOffer(player, offeredShare, myDelta, opponentDelta, roundNumber) {
        // [P1 FIX] 更正的接受/拒绝逻辑
        // 接受：立即获得 offeredShare
        // 拒绝：进入下一轮，我的份额会被贴现
        // 下一轮我能获得的 ≈ 均衡份额 × δ（贴现）
        
        const currentValueIfAccept = offeredShare;
        
        // [P0 FIX] 防止除零
        const denominator = 1 - myDelta * opponentDelta;
        let futureValueIfReject;
        
        if (Math.abs(denominator) < 1e-9 || myDelta >= 1) {
            // 无贴现成本时，下一轮价值和当前一样
            futureValueIfReject = offeredShare;
        } else {
            // Rubinstein均衡下，下一轮我能获得的（贴现后）
            // 对方会出接近均衡的价格，我的份额 = δ × myEquilibriumShare
            const myEquilibriumShare = (1 - opponentDelta) / denominator;
            futureValueIfReject = myEquilibriumShare * myDelta;
        }
        
        // 是否接受？
        const shouldAccept = currentValueIfAccept >= futureValueIfReject - 0.01; // 容忍误差
        
        // 接受率（基于确定性等价）
        const acceptProbability = currentValueIfAccept >= futureValueIfReject ? 0.9 : 0.3;

        return {
            player,
            offeredShare,
            currentValueIfAccept: currentValueIfAccept.toFixed(3),
            futureValueIfReject: futureValueIfReject.toFixed(3),
            shouldAccept,
            acceptProbability: (acceptProbability * 100).toFixed(0) + '%',
            rationale: shouldAccept 
                ? `接受：当前${(currentValueIfAccept*100).toFixed(1)}% ≥ 未来${(futureValueIfReject*100).toFixed(1)}%`
                : `拒绝：当前${(currentValueIfAccept*100).toFixed(1)}% < 未来${(futureValueIfReject*100).toFixed(1)}%，等待更优报价`,
            breakdown: {
                currentRound: roundNumber,
                myDiscount: myDelta,
                oppDiscount: opponentDelta,
                nextRoundShare: (futureValueIfReject).toFixed(3),
            },
        };
    }

    /**
     * 计算接受概率（基于期望效用）
     */
    _calculateAcceptanceProbability(valueIfAccept, valueIfReject) {
        // 使用确定性等价
        // 风险中性：直接比较
        if (valueIfAccept >= valueIfReject) {
            return 0.9;  // 高概率接受
        } else {
            return 0.3;  // 低概率接受
        }
    }

    /**
     * 获取议价阶段分析
     */
    getBargainingPhase() {
        if (this.offerHistory.length === 0) {
            return { phase: 'INITIAL', description: '尚未开始', urgency: '低' };
        }
        
        const lastOffer = this.offerHistory[this.offerHistory.length - 1];
        const round = lastOffer.round;
        
        if (round <= 2) {
            return { phase: 'EARLY', description: '早期议价，份额弹性大', urgency: '中' };
        } else if (round <= 5) {
            return { phase: 'MIDDLE', description: '中期博弈，关注耐心程度', urgency: '中高' };
        } else {
            return { phase: 'LATE', description: '后期接近deadline，达成压力增大', urgency: '高' };
        }
    }

    /**
     * 生成议价报告
     * [P2 FIX] 使用通用玩家名称而非硬编码 P1/P2
     */
    generateBargainingReport(delta1, delta2, player1Name = '玩家1', player2Name = '玩家2') {
        const equilibrium = this.calculateEquilibrium(delta1, delta2);
        const phase = this.getBargainingPhase();

        let report = '🤝 议价博弈分析\n';
        report += '═══════════════════════════════════\n';
        report += `均衡类型: ${equilibrium.equilibrium}\n`;
        report += `先手方: ${equilibrium.firstMover}\n`;
        report += `先手优势: ${equilibrium.firstMoverAdvantage}\n\n`;

        report += 'Rubinstein均衡份额:\n';
        report += `  ${player1Name}先出价: ${player1Name}=${equilibrium.player1.sharePercent}, ${player2Name}=${equilibrium.player2.sharePercent}\n`;
        report += `  ${player2Name}先出价: ${player1Name}=${(1 - equilibrium.player2.share).toFixed(1)}%, ${player2Name}=${equilibrium.player2.sharePercent}\n\n`;

        report += '当前阶段:\n';
        report += `  ${phase.phase}: ${phase.description}\n`;
        report += `  紧迫度: ${phase.urgency}\n\n`;

        report += '出价历史:\n';
        for (const offer of this.offerHistory) {
            report += `  R${offer.round}: ${offer.player} 出价 ${offer.suggestedAmount}\n`;
        }

        return report;
    }
}


// ============================================================
// 第三部分：P1 新增 - 联盟博弈 (Coalitional Games)
// Shapley (1953) - 联盟博弈与核心
// ============================================================

/**
 * 联盟博弈引擎
 * 
 * 核心问题：
 * - 在多人讨论中，谁和谁结盟？
 * - 联盟收益如何分配才公平？
 * - 联盟是否会崩溃？
 * 
 * 解决方案：Shapley值
 * - 每个玩家的贡献 = 所有联盟中该玩家的边际贡献的平均值
 */
class CoalitionGame {
    constructor() {
        this.players = [];
        this.coalitionHistory = [];
        this.valueFunction = null;
    }

    /**
     * 初始化联盟博弈
     * 
     * @param {array} players - 玩家列表
     * @param {function} valueFunction - 联盟价值函数 v(S) → number
     * 
     * 示例：
     * valueFunction = (S) => {
     *   if (S.length === 0) return 0;
     *   if (S.length === 1) return 1;
     *   if (S.length === 2) return 3;
     *   if (S.length === 3) return 5;
     *   return 5;
     * }
     */
    init(players, valueFunction) {
        this.players = players;
        this.valueFunction = valueFunction;
    }

    /**
     * 计算Shapley值
     * 
     * φ_i(v) = Σ_{S ⊆ N\\{i}} [|S|! (n-|S|-1)! / n!] × [v(S ∪ {i}) - v(S)]
     * 
     * @returns {object} 每个玩家的Shapley值
     */
    calculateShapleyValues() {
        const n = this.players.length;
        const shapleyValues = {};

        for (const player of this.players) {
            let totalContribution = 0;
            
            // 遍历所有不包含该玩家的联盟S
            const otherPlayers = this.players.filter(p => p !== player);
            const allSubsets = this._generateSubsets(otherPlayers);
            
            for (const S of allSubsets) {
                const sSize = S.length;
                
                // 边际贡献：[v(S ∪ {i}) - v(S)]
                const valueWith = this.valueFunction([...S, player]);
                const valueWithout = this.valueFunction(S);
                const marginalContribution = valueWith - valueWithout;
                
                // 加权系数：|S|! (n-|S|-1)! / n!
                const weight = this._calculateWeight(sSize, n);
                
                totalContribution += weight * marginalContribution;
            }
            
            shapleyValues[player] = totalContribution;
        }

        return {
            shapleyValues,
            totalValue: Object.values(shapleyValues).reduce((a, b) => a + b, 0),
            distribution: this._normalizeDistribution(shapleyValues),
        };
    }

    /**
     * 生成所有子集
     */
    _generateSubsets(players) {
        const subsets = [];
        const n = players.length;
        
        // 使用二进制表示生成所有子集
        for (let mask = 0; mask < (1 << n); mask++) {
            const subset = [];
            for (let i = 0; i < n; i++) {
                if (mask & (1 << i)) {
                    subset.push(players[i]);
                }
            }
            subsets.push(subset);
        }
        
        return subsets;
    }

    /**
     * 计算Shapley权重
     */
    _calculateWeight(sSize, n) {
        // |S|! (n-|S|-1)! / n!
        const sFactorial = this._factorial(sSize);
        const remainingFactorial = this._factorial(n - sSize - 1);
        const nFactorial = this._factorial(n);
        
        return (sFactorial * remainingFactorial) / nFactorial;
    }

    /**
     * 阶乘（溢出保护）
     * [P0 FIX] 对于n>20使用对数计算，避免溢出
     */
    _factorial(n) {
        if (n <= 1) return 1;
        // [P0 FIX] n! 在 n>20 时超过 Number.MAX_SAFE_INTEGER
        if (n > 20) {
            // 使用对数：log(n!) = Σ log(i)
            let logSum = 0;
            for (let i = 2; i <= n; i++) {
                logSum += Math.log(i);
            }
            return Math.exp(logSum);
        }
        let result = 1;
        for (let i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    /**
     * 标准化分配（确保总和=1）
     */
    _normalizeDistribution(shapleyValues) {
        const total = Object.values(shapleyValues).reduce((a, b) => a + b, 0);
        const distribution = {};
        
        for (const [player, value] of Object.entries(shapleyValues)) {
            distribution[player] = {
                value,
                percent: total !== 0 ? ((value / total) * 100).toFixed(1) + '%' : '0%',
            };
        }
        
        return distribution;
    }

    /**
     * 计算所有可能的联盟及其价值
     */
    calculateAllCoalitions() {
        const allCoalitions = [];
        const subsets = this._generateSubsets(this.players);
        
        for (const subset of subsets) {
            if (subset.length === 0) continue;
            
            const value = this.valueFunction(subset);
            const players = subset.join(' + ');
            
            allCoalitions.push({
                coalition: players,
                size: subset.length,
                value,
                valuePerPlayer: (value / subset.length).toFixed(2),
            });
        }
        
        // 按价值排序
        return allCoalitions.sort((a, b) => b.value - a.value);
    }

    /**
     * 检测稳定联盟（核心检测）
     * 
     * 核心(Core)条件：
     * 对于每个联盟S：Σ_{i∈S} φ_i ≥ v(S)
     * 即：分配给每个联盟的价值不小于该联盟单独能获得的价值
     */
    checkCoreStability(shapleyValues) {
        const coalitions = this.calculateAllCoalitions();
        const violations = [];
        
        for (const coalition of coalitions) {
            if (coalition.size < 2) continue;  // 单人联盟总是稳定的
            
            // 计算该联盟中玩家获得的Shapley值总和
            const coalitionPlayers = coalition.coalition.split(' + ');
            const allocatedValue = coalitionPlayers.reduce(
                (sum, p) => sum + (shapleyValues[p] || 0), 0
            );
            
            // 检验：分配值 ≥ 联盟单独价值
            if (allocatedValue < coalition.value) {
                violations.push({
                    coalition: coalition.coalition,
                    allocated: allocatedValue.toFixed(3),
                    standalone: coalition.value.toFixed(3),
                    deficit: (coalition.value - allocatedValue).toFixed(3),
                });
            }
        }
        
        return {
            isStable: violations.length === 0,
            violations,
            stabilityScore: violations.length === 0 ? 100 : Math.max(0, 100 - violations.length * 20),
        };
    }

    /**
     * 预测最优联盟结构
     * 
     * 使用贪婪算法找最大价值联盟
     */
    predictOptimalCoalition() {
        const allCoalitions = this.calculateAllCoalitions();
        
        // 找最大价值联盟
        const maxValueCoalition = allCoalitions[0];
        
        // 计算联盟内各玩家的Shapley值占比
        const coalitionPlayers = maxValueCoalition.coalition.split(' + ');
        const coalitionShapley = {};
        let totalShapleyInCoalition = 0;
        
        for (const player of coalitionPlayers) {
            coalitionShapley[player] = this._calculateIndividualShapley(player);
            totalShapleyInCoalition += coalitionShapley[player];
        }

        // 检查是否有人想跳槽
        const incentivesToDefect = this._checkIncentivesToDefect(
            coalitionPlayers, coalitionShapley
        );

        return {
            optimalCoalition: maxValueCoalition.coalition,
            totalValue: maxValueCoalition.value,
            valuePerPlayer: maxValueCoalition.valuePerPlayer,
            shapleyDistribution: coalitionShapley,
            incentivesToDefect,
            recommendation: this._generateCoalitionRecommendation(
                maxValueCoalition, incentivesToDefect
            ),
        };
    }

    /**
     * 计算单个玩家的Shapley值
     */
    _calculateIndividualShapley(player) {
        const otherPlayers = this.players.filter(p => p !== player);
        const allSubsets = this._generateSubsets(otherPlayers);
        
        let total = 0;
        const n = this.players.length;
        
        for (const S of allSubsets) {
            const sSize = S.length;
            const marginal = this.valueFunction([...S, player]) - this.valueFunction(S);
            const weight = this._calculateWeight(sSize, n);
            total += weight * marginal;
        }
        
        return total;
    }

    /**
     * 检查跳槽动机
     */
    _checkIncentivesToDefect(coalitionPlayers, shapleyDistribution) {
        const incentives = [];
        
        for (const player of coalitionPlayers) {
            // 如果离开，联盟剩余玩家的价值
            const remainingPlayers = coalitionPlayers.filter(p => p !== player);
            const remainingValue = remainingPlayers.length > 0 
                ? this.valueFunction(remainingPlayers) 
                : 0;
            
            // 留在联盟中获得的Shapley值
            const currentShare = shapleyDistribution[player];
            
            // 单飞的价值
            const soloValue = this.valueFunction([player]);
            
            if (soloValue > currentShare) {
                incentives.push({
                    player,
                    currentShare: currentShare.toFixed(3),
                    soloValue: soloValue.toFixed(3),
                    gainIfLeave: (soloValue - currentShare).toFixed(3),
                    incentive: 'HIGH',
                });
            } else if (remainingValue > currentShare * (remainingPlayers.length + 1)) {
                incentives.push({
                    player,
                    currentShare: currentShare.toFixed(3),
                    remainingValue: remainingValue.toFixed(3),
                    incentive: 'MEDIUM',
                });
            } else {
                incentives.push({
                    player,
                    currentShare: currentShare.toFixed(3),
                    soloValue: soloValue.toFixed(3),
                    incentive: 'LOW',
                });
            }
        }
        
        return incentives;
    }

    /**
     * 生成联盟建议
     */
    _generateCoalitionRecommendation(coalition, incentivesToDefect) {
        const highIncentive = incentivesToDefect.filter(i => i.incentive === 'HIGH');
        
        if (highIncentive.length === 0) {
            return '联盟稳定：所有成员无强烈跳槽动机';
        } else if (highIncentive.length === 1) {
            return `潜在不稳定：${highIncentive[0].player} 可能有跳槽动机`;
        } else {
            return `联盟高度不稳定：${highIncentive.map(i => i.player).join(', ')} 都有跳槽动机`;
        }
    }

    /**
     * 记录联盟形成
     */
    recordCoalition(players, formed = true) {
        this.coalitionHistory.push({
            players,
            formed,
            round: this.coalitionHistory.length + 1,
            timestamp: Date.now(),
        });
    }

    /**
     * 生成联盟博弈报告
     */
    generateCoalitionReport() {
        const shapley = this.calculateShapleyValues();
        const allCoalitions = this.calculateAllCoalitions();
        const stability = this.checkCoreStability(shapley.shapleyValues);
        const prediction = this.predictOptimalCoalition();

        let report = '🛡 联盟博弈分析\n';
        report += '═══════════════════════════════════\n\n';

        report += 'Shapley值分配:\n';
        for (const [player, data] of Object.entries(shapley.distribution)) {
            report += `  ${player}: ${data.percent} (价值=${data.value.toFixed(3)})\n`;
        }
        report += `  总计: ${shapley.totalValue.toFixed(3)}\n\n`;

        report += '联盟稳定性 (Core检测):\n';
        report += `  稳定: ${stability.isStable ? '是 ✅' : '否 ❌'}\n`;
        report += `  稳定评分: ${stability.stabilityScore}/100\n`;
        if (stability.violations.length > 0) {
            report += '  违反项:\n';
            for (const v of stability.violations) {
                report += `    ${v.coalition}: 分配${v.allocated} < 独立价值${v.standalone}\n`;
            }
        }
        report += '\n';

        report += '最优联盟预测:\n';
        report += `  联盟: ${prediction.optimalCoalition}\n`;
        report += `  价值: ${prediction.totalValue}\n`;
        report += `  建议: ${prediction.recommendation}\n\n`;

        report += '联盟历史:\n';
        for (const c of this.coalitionHistory) {
            report += `  R${c.round}: ${c.players.join(' + ')} (${c.formed ? '形成' : '解散'})\n`;
        }

        return report;
    }
}


// ============================================================
// 第四部分：整合竞技场
// ============================================================

class AdvancedGameTheoryArena extends SubagentArena {
    constructor(skillsDir = null) {
        super(skillsDir);
        
        this.signalingGame = new SignalingGame();
        this.repeatedGame = new RepeatedGameEngine();
        this.informationDesigner = new InformationDesigner();
        this.bargainingGame = new BargainingGame();
        this.coalitionGame = new CoalitionGame();
        
        this.gameState = null;
        this.argumentPool = [];
    }

    async initArenaWithAdvancedGameTheory(config) {
        await super.initArena(config);

        const {
            topic,
            participants,
            discountFactors = {},
            signals = {},
            coalitionValues = null,
        } = config;

        this.gameState = {
            topic,
            round: 0,
            participants: participants.map(p => ({
                name: p.name,
                skillName: p.skillName,
                discountFactor: discountFactors[p.name] || 0.9,
                speakerType: signals[p.name] || 'strategic',
                confidence: 0.5,
                hasEvidence: false,
                beliefs: {},
            })),
        };

        // 初始化联盟博弈
        if (coalitionValues && typeof coalitionValues === 'function') {
            const playerNames = participants.map(p => p.name);
            this.coalitionGame.init(playerNames, coalitionValues);
        }

        console.log('🎲 高级博弈论参数已初始化:');
        console.log(`  主题: ${topic}`);
        console.log(`  参与者: ${participants.map(p => p.name).join(', ')}`);
        console.log(`  模块: 信号博弈 | 重复博弈 | 信息设计 | 议价博弈 | 联盟博弈`);

        return this.arena;
    }

    assessArgumentCredibility(speakerName, content) {
        const participant = this.gameState.participants.find(p => p.name === speakerName);
        if (!participant) return null;

        const prior = participant.beliefs[speakerName] || 0.5;
        const assessment = this.signalingGame.assessSignalCredibility(
            content,
            participant.speakerType,
            prior
        );

        participant.beliefs[speakerName] = assessment.posterior;
        participant.confidence = assessment.confidence;
        participant.hasEvidence = assessment.signalType.includes('evidence');

        return assessment;
    }

    getStrategicAdvice(playerName, opponentName) {
        return this.repeatedGame.getStrategicAdvice(playerName, opponentName);
    }

    suggestInformationDisclosure() {
        const states = this.gameState.participants.map(p => ({
            name: p.name,
            confidence: p.confidence,
            hasEvidence: p.hasEvidence,
        }));

        const beliefs = {};
        this.gameState.participants.forEach(p => {
            beliefs[p.name] = p.confidence;
        });

        return this.informationDesigner.suggestDisclosure(
            this.gameState.topic,
            states,
            beliefs
        );
    }

    /**
     * 议价博弈分析
     */
    analyzeBargaining(player1Delta, player2Delta, firstMover = 'player1') {
        return this.bargainingGame.calculateEquilibrium(player1Delta, player2Delta, firstMover);
    }

    /**
     * 生成出价建议
     */
    generateOffer(player, myDelta, opponentDelta, currentValue = 100) {
        return this.bargainingGame.generateOffer(
            player,
            myDelta,
            opponentDelta,
            currentValue,
            this.gameState?.round || 1
        );
    }

    /**
     * 评估是否接受出价
     */
    evaluateBargainingOffer(player, offeredShare, myDelta, opponentDelta) {
        return this.bargainingGame.evaluateOffer(
            player, offeredShare, myDelta, opponentDelta,
            this.gameState?.round || 1
        );
    }

    /**
     * 联盟博弈分析
     */
    analyzeCoalition() {
        if (!this.coalitionGame.valueFunction) {
            return { error: '联盟价值函数未设置' };
        }
        return {
            shapley: this.coalitionGame.calculateShapleyValues(),
            stability: this.coalitionGame.checkCoreStability(
                this.coalitionGame.calculateShapleyValues().shapleyValues
            ),
            optimal: this.coalitionGame.predictOptimalCoalition(),
        };
    }

    /**
     * 设置联盟价值函数
     */
    setCoalitionValueFunction(valueFunction) {
        if (this.coalitionGame.players.length === 0) {
            const playerNames = this.gameState?.participants.map(p => p.name) || [];
            this.coalitionGame.init(playerNames, valueFunction);
        } else {
            this.coalitionGame.valueFunction = valueFunction;
        }
    }

    recordRound(roundData) {
        this.gameState.round++;
        const { speaker, content, action, cooperated } = roundData;

        this.repeatedGame.recordRound(speaker, action, cooperated);

        const credibility = this.assessArgumentCredibility(speaker, content);

        this.argumentPool.push({
            round: this.gameState.round,
            speaker,
            content,
            credibility,
            action,
            cooperated,
        });
    }

    generateAdvancedGameTheoryReport() {
        if (!this.gameState) return '高级博弈论状态未初始化';

        let report = '🎲 高级博弈论分析报告 v3.9\n';
        report += '═══════════════════════════════════════════\n\n';

        // 1. 信号博弈分析
        report += '📡 信号博弈分析:\n';
        report += '───────────────────────────────────────────\n';
        const credibleArgs = this.argumentPool.filter(a => a.credibility?. credible);
        const incredibleArgs = this.argumentPool.filter(a => a.credibility && !a.credibility.credible);
        
        report += `  总发言数: ${this.argumentPool.length}\n`;
        report += `  高可信信号: ${credibleArgs.length}\n`;
        report += `  低可信信号: ${incredibleArgs.length}\n`;
        if (credibleArgs.length > 0) {
            const avgCredibility = credibleArgs.reduce((a, b) => a + b.credibility.confidence, 0) / credibleArgs.length;
            report += `  平均可信度: ${avgCredibility.toFixed(2)}\n`;
        }
        report += '\n';

        // 2. 重复博弈/合作动态
        report += '🤝 合作动态分析:\n';
        report += '───────────────────────────────────────────\n';
        const phaseAnalysis = this.repeatedGame.getPhaseAnalysis();
        report += `  当前阶段: ${phaseAnalysis.phase}\n`;
        report += `  描述: ${phaseAnalysis.description}\n`;
        report += `  稳定性: ${phaseAnalysis.stability}\n`;
        report += `  风险: ${phaseAnalysis.risk}\n`;
        report += `  全局合作率: ${(this.repeatedGame.cooperationTracker.getCooperationRate() * 100).toFixed(0)}%\n\n`;

        // 3. 信息设计建议
        report += '📢 信息披露建议:\n';
        report += '───────────────────────────────────────────\n';
        const disclosure = this.suggestInformationDisclosure();
        report += `  建议模式: ${disclosure.mode}\n`;
        report += `  内容: ${disclosure.content}\n`;
        report += `  预期影响: ${disclosure.expectedImpact}\n\n`;

        // 4. 议价博弈分析
        report += '💰 议价博弈分析:\n';
        report += '───────────────────────────────────────────\n';
        const bargainingPhase = this.bargainingGame.getBargainingPhase();
        report += `  当前阶段: ${bargainingPhase.phase}\n`;
        report += `  紧迫度: ${bargainingPhase.urgency}\n`;
        if (this.gameState.participants.length === 2) {
            const [p1, p2] = this.gameState.participants;
            const eq = this.bargainingGame.calculateEquilibrium(p1.discountFactor, p2.discountFactor);
            report += `  Rubinstein均衡: P1先=${eq.player1.sharePercent}, P2先=${eq.player2.sharePercent}\n`;
        }
        report += '\n';

        // 5. 联盟博弈分析
        report += '🛡 联盟博弈分析:\n';
        report += '───────────────────────────────────────────\n';
        if (this.coalitionGame.valueFunction) {
            const coalitionAnalysis = this.analyzeCoalition();
            if (!coalitionAnalysis.error) {
                report += `  Shapley总分配: ${coalitionAnalysis.shapley.totalValue.toFixed(3)}\n`;
                report += `  核心稳定: ${coalitionAnalysis.stability.isStable ? '是 ✅' : '否 ❌'}\n`;
                report += `  最优联盟: ${coalitionAnalysis.optimal.optimalCoalition}\n`;
            }
        } else {
            report += '  (联盟价值函数未设置)\n';
        }
        report += '\n';

        // 6. 各参与者状态
        report += '👤 参与者状态:\n';
        report += '───────────────────────────────────────────\n';
        for (const p of this.gameState.participants) {
            const advice = this.getStrategicAdvice(p.name, this.gameState.participants.find(op => op.name !== p.name)?.name);
            report += `  【${p.name}】\n`;
            report += `    类型: ${p.speakerType}\n`;
            report += `    置信度: ${(p.confidence * 100).toFixed(0)}%\n`;
            report += `    折扣因子: ${p.discountFactor}\n`;
            report += `    策略建议: ${advice.reason}\n`;
            report += `    合作率: ${(this.repeatedGame.cooperationTracker.getCooperationRate(p.name) * 100).toFixed(0)}%\n`;
        }

        return report;
    }

    getSummaryScore() {
        const signalScore = this.argumentPool.length > 0
            ? (this.argumentPool.filter(a => a.credibility?. credible).length / this.argumentPool.length) * 100
            : 50;

        const cooperationRate = this.repeatedGame.cooperationTracker.getCooperationRate() * 100;
        const phaseAnalysis = this.repeatedGame.getPhaseAnalysis();

        return {
            signalQuality: signalScore.toFixed(0),
            cooperationLevel: cooperationRate.toFixed(0),
            discussionPhase: phaseAnalysis.phase,
            overallHealth: this._calculateOverallHealth(signalScore, cooperationRate),
        };
    }

    _calculateOverallHealth(signalScore, cooperationRate) {
        return ((signalScore * 0.4) + (cooperationRate * 0.6)).toFixed(0);
    }
}


module.exports = {
    SignalingGame,
    CooperationTracker,
    RepeatedGameEngine,
    InformationDesigner,
    BargainingGame,
    CoalitionGame,
    AdvancedGameTheoryArena,
};