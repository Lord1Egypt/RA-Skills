from __future__ import annotations

from dataclasses import dataclass

from classifier import SituationAssessment


@dataclass
class DecisionPath:
    name: str
    summary: str
    suitable_conditions: str
    short_term_benefit: str
    short_term_risk: str
    mid_term_evolution: str
    failure_point: str


class DecisionAnalyzer:
    VARIABLE_LIBRARY: dict[str, list[tuple[str, str]]] = {
        "以弱对强": [
            ("资源", "你能否集中有限资源打到决定性节点，而不是全面摊薄。"),
            ("时间窗口", "对手是否正处在迟缓、内耗或判断失真的窗口期。"),
            ("联盟稳定性", "你是否能借外力缩小正面硬碰的差距。"),
            ("对手状态", "对手是不是过度自信、线条过长或内部松动。"),
        ],
        "内部冲突": [
            ("内部一致性", "关键执行层是否愿意跟随你的节奏。"),
            ("合法性", "你是否握有公开授权或占据规则优势。"),
            ("信息控制", "冲突是否停留在局部，还是已经扩散成全面失序。"),
            ("关键人物", "谁是真正能改变局势的中间层与节点人物。"),
        ],
        "改革推进": [
            ("执行链条", "方案再正确，也要看谁来执行、谁会拖延。"),
            ("利益补偿", "改革是否给受损方留下缓冲空间。"),
            ("时间窗口", "现在适合全面推进，还是更适合局部试点。"),
            ("合法性", "你是否拥有足够的正式授权与叙事正当性。"),
        ],
        "联盟不稳": [
            ("共同敌人", "联盟是否真的有足够强的外部压力。"),
            ("承诺机制", "是否有可验证、可兑现的利益绑定。"),
            ("退出成本", "盟友翻脸时，代价是否足够高。"),
            ("后手", "即使联盟破裂，你是否仍有独立生存方案。"),
        ],
        "守攻抉择": [
            ("基本盘", "一旦出手失败，你还能守住什么。"),
            ("节奏", "此时推进是抢先，还是过早暴露自己。"),
            ("战果可见性", "短期内是否能形成可见成果。"),
            ("补给", "资源与组织是否足以支撑中期消耗。"),
        ],
        "权力控制": [
            ("形式权威", "名义上的授权是否支持你的动作。"),
            ("实际控制", "关键岗位、信息流、资源流谁在掌握。"),
            ("继任叙事", "你要证明自己是在稳局，而不是单纯夺权。"),
            ("反制能力", "对手若提前动作，你有没有快速收口的能力。"),
        ],
        "用人换将": [
            ("人岗匹配", "现在的问题到底是人不对，还是结构不对。"),
            ("替补质量", "换下去以后是否真有更稳的人接得住。"),
            ("交接成本", "换人后组织能否承受短期磨合损失。"),
            ("信号效应", "此次换人会给组织发出什么信号。"),
        ],
    }

    PATH_LIBRARY: dict[str, list[tuple[str, str, str, str, str, str]]] = {
        "以弱对强": [
            ("暂避锋芒", "避免正面消耗，把冲突拖到对手不舒服的场景。", "你没有短期硬碰条件，但有回旋空间。", "保全基本盘，降低被一击击溃的概率。", "容易被误判为软弱，内部士气可能波动。", "若能拖到对手失误，可转入主动局。", "拖延过久却没有建立新优势。"),
            ("集中突破", "把所有有限资源砸向最关键的一点。", "你能识别决定胜负的单点，并有足够执行力。", "一旦突破成功，局面会迅速改观。", "押错点位会导致资源清空。", "突破后可能带动中立方转向。", "没有建立后续跟进，首胜后反被反扑。"),
            ("借势结盟", "通过联盟补齐你最缺的一块短板。", "存在暂时利益一致的外部伙伴。", "快速缩小资源差距。", "盟友目标不完全一致，后续容易反噬。", "如果绑定机制设计得好，能形成稳定均势。", "把命运完全押给不稳定盟友。"),
        ],
        "内部冲突": [
            ("先稳关键中层", "先稳住执行链条，再处理公开冲突。", "你的主要风险来自组织失控。", "能迅速降低执行层离心。", "短期内看起来动作不够强。", "若中层站稳，后续清理与调整成本更低。", "误把核心反对者当成可安抚对象。"),
            ("公开定规矩", "先把边界和纪律公开化，压缩模糊空间。", "你掌握规则解释权或名义授权。", "可迅速提高组织可预期性。", "过早亮牌可能刺激对手提前联手。", "若执行到位，组织会回到规则轨道。", "规则出台后执行不一致，反而损伤威信。"),
            ("分化对手", "区分强硬反对者与摇摆者，避免把所有人推到一起。", "对方内部并非铁板一块。", "有机会降低正面冲突规模。", "操作过慢会被对手识破。", "成功后可形成局部倒向。", "没有给摇摆者真实收益，分化失败。"),
        ],
        "改革推进": [
            ("试点推进", "先做一块可见样板，再扩展制度。", "时间允许局部验证，且失败成本可控。", "能用结果为改革争取支持。", "试点范围太小会被视为无关痛痒。", "试点成功后可逐步扩面。", "样板没有做成，改革叙事当场受损。"),
            ("先整执行链", "先抓考核、节奏和责任链，再上大方案。", "改革阻力主要来自执行层，而非顶层共识。", "短期能看到纪律与效率改善。", "若没有同步解释，容易被理解为单纯加压。", "执行链稳定后，制度改革落地率会提升。", "只抓执行不调激励，后续反弹集中。"),
            ("强授权直推", "拿到最高授权后集中推进核心改革。", "你已有明确背书，且窗口期很短。", "速度快，能抢在阻力组织化前完成关键步骤。", "一旦首轮受挫，反对者会迅速结盟。", "如果第一阶段成果明显，后续阻力会下降。", "高估授权强度，低估基层消化能力。"),
        ],
        "联盟不稳": [
            ("先绑定利益", "先把分配、回报和退出成本写清楚。", "联盟仍愿意合作，但信任不足。", "能降低短期背刺概率。", "谈判成本高，速度变慢。", "规则清楚后联盟更可持续。", "只签原则不做执行约束。"),
            ("留足后手", "合作但不把核心生死线全部交出去。", "盟友价值高，但不可完全信任。", "即便联盟破裂，也不至于致命。", "合作深度不足，战果可能受限。", "中期可根据局势再决定是否加码。", "过度防范导致盟友感到你不可信。"),
            ("制造共同敌压", "把联盟内部差异压到共同外部压力之下。", "外部威胁真实且双方都承受不起。", "能迅速形成协同。", "一旦外部压力下降，联盟会重新松动。", "短期效果通常最好，但耐久度有限。", "误判外部威胁强度，联盟很快失去粘性。"),
        ],
        "守攻抉择": [
            ("守住基本盘", "先确保现金流、核心团队和关键阵地不失。", "你当前最怕的是一次失败后再无翻身资本。", "降低系统性崩盘风险。", "可能错失先手。", "若敌方后劲不足，你会赢得更长窗口。", "守得太久，团队转入消极心态。"),
            ("有限出击", "只打一个能验证方向的战役，不全面铺开。", "你需要信号性胜利，但资源不足以全面推进。", "有机会打出士气与预期。", "首战选错会伤害信心。", "若打赢，可转入更积极态势。", "把试探战误做决战。"),
            ("全面推进", "趁窗口期主动扩张，试图一次改写格局。", "机会窗口短，且你已有足够准备。", "一旦成功，收益最大。", "资源链容易被拉断。", "成则重塑秩序，败则伤到根本。", "补给与组织能力跟不上前线节奏。"),
        ],
        "权力控制": [
            ("先拿中枢", "优先控制关键岗位、信息流和审批链。", "名义授权不完全可靠，实际控制更重要。", "能迅速改变真实力量对比。", "动作过早可能激化全面对抗。", "若中枢稳定，后续整编成本会下降。", "只拿位置，不拿执行人。"),
            ("借规则整权", "用制度、任命和流程重排控制权，而非直接摊牌。", "你需要保住名分与合法性。", "更容易争取中间层支持。", "推进较慢，给对手留了反制窗口。", "如果节奏稳，组织会默认新秩序。", "规则变更后没有配套执行。"),
            ("快刀定局", "在对手尚未完成组织化前，快速定局。", "窗口很短，且你已有足够把握。", "避免长期消耗。", "失败即反噬。", "成则局面清晰，败则威信受重创。", "高估支持面，低估对方反扑。"),
        ],
        "用人换将": [
            ("先调权后换人", "先削减关键岗位权限，再做正式替换。", "直接换人会引发强反弹。", "减少换人时的系统性震荡。", "短期容易形成双轨并行。", "若交接顺利，可自然完成替换。", "权责不清，形成更大内耗。"),
            ("立即换将", "用明确动作重置信号和纪律。", "问题根源确实集中在人，而非结构。", "能快速释放组织信号。", "替补若接不住，局面会更坏。", "若新负责人能力足够，可迅速止损。", "把结构问题误判为单人问题。"),
            ("保人换打法", "先不换人，先改目标、节奏和协作方式。", "当前没有更好的替补，且问题部分来自结构失配。", "避免交接成本。", "若旧问题重复，会被视为优柔寡断。", "若打法调整有效，可为后续换人与否争取时间。", "没有配套监督，打法改革流于口号。"),
        ],
    }

    def analyze(self, question: str, assessment: SituationAssessment, cases: list[dict]) -> dict:
        variables = self._select_variables(assessment.primary, cases)
        paths = self._select_paths(assessment.primary)
        principles = self._collect_principles(cases)
        return {
            "situation": assessment,
            "cases": cases,
            "variables": variables,
            "paths": paths,
            "principles": principles,
            "boundary": [
                "历史类比 != 现实预测，历史只能提供结构参照，不提供确定答案。",
                "推演 != 结果保证，现实执行中的人、制度、技术和外部环境都可能改变结果。",
                "不要照搬历史人物的做法，应只借鉴背后的结构条件、节奏与失败机制。",
            ],
            "assumptions": self._build_assumptions(question),
        }

    def _select_variables(self, primary: str, cases: list[dict]) -> list[tuple[str, str]]:
        variables = list(self.VARIABLE_LIBRARY.get(primary, self.VARIABLE_LIBRARY["守攻抉择"]))
        if any("合法性" in case["situation_tags"] for case in cases):
            variables.append(("合法性", "你是否占据规则、名分或公开授权，这会决定很多动作能否被组织接受。"))
        deduped: list[tuple[str, str]] = []
        seen_names: set[str] = set()
        for name, explanation in variables:
            if name in seen_names:
                continue
            deduped.append((name, explanation))
            seen_names.add(name)
        return deduped[:6]

    def _select_paths(self, primary: str) -> list[DecisionPath]:
        raw_paths = self.PATH_LIBRARY.get(primary, self.PATH_LIBRARY["守攻抉择"])
        return [
            DecisionPath(
                name=name,
                summary=summary,
                suitable_conditions=suitable_conditions,
                short_term_benefit=short_term_benefit,
                short_term_risk=short_term_risk,
                mid_term_evolution=mid_term_evolution,
                failure_point=failure_point,
            )
            for name, summary, suitable_conditions, short_term_benefit, short_term_risk, mid_term_evolution, failure_point in raw_paths
        ]

    def _collect_principles(self, cases: list[dict]) -> list[str]:
        principles: list[str] = []
        for case in cases:
            for principle in case["transferable_principles"]:
                if principle not in principles:
                    principles.append(principle)
        return principles[:5]

    def _build_assumptions(self, question: str) -> list[str]:
        assumptions = []
        if not any(keyword in question for keyword in ["预算", "资源", "现金流", "人手"]):
            assumptions.append("默认你当前资源不是无限的，需要在关键节点集中投入。")
        if not any(keyword in question for keyword in ["上级", "董事会", "授权", "合法"]):
            assumptions.append("默认你并没有完全不受约束的最高授权，需要考虑合法性与组织接受度。")
        if not any(keyword in question for keyword in ["盟友", "合作方", "股东", "伙伴"]):
            assumptions.append("默认外部支持并不稳定，不能把成败全部押在联盟上。")
        return assumptions
