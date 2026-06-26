"""
Research Method Advisor
研究方法决策助手

根据研究问题、数据类型和设计，推荐合适的统计检验方法，
并提示前提假设、参数/非参数备选方案。

适用于实验心理学、社会科学等定量研究。
"""

from typing import Dict, List, Optional


class StatTestAdvisor:
    """统计检验选择顾问"""

    # ============ 决策引擎：选择统计检验 ============

    def recommend_test(self,
                      goal: str,
                      dv_type: str,
                      n_groups: Optional[int] = None,
                      design: Optional[str] = None,
                      n_factors: int = 1,
                      iv_type: Optional[str] = None,
                      assumptions_met: bool = True) -> Dict:
        """
        根据研究特征推荐统计检验

        参数:
        -----
        goal : str
            研究目的: 'compare'(比较差异) / 'relationship'(检验关系) / 'predict'(预测)
        dv_type : str
            因变量类型: 'continuous'(连续) / 'categorical'(分类) / 'ordinal'(有序)
        n_groups : int, 可选
            分组/水平数量 (比较差异时需要)
        design : str, 可选
            实验设计: 'independent'(被试间/独立) / 'paired'(被试内/配对)
        n_factors : int
            自变量(因素)数量，默认1
        iv_type : str, 可选
            自变量类型(检验关系时): 'continuous' / 'categorical'
        assumptions_met : bool
            是否满足参数检验假设(正态性、方差齐性等)，默认 True

        返回:
        -----
        dict : 推荐的检验方法及说明
        """
        goal = goal.lower()

        if goal == "compare":
            return self._recommend_comparison(
                dv_type, n_groups, design, n_factors, assumptions_met)
        elif goal == "relationship":
            return self._recommend_relationship(dv_type, iv_type, assumptions_met)
        elif goal == "predict":
            return self._recommend_prediction(dv_type)
        else:
            return {"错误": f"未知的研究目的: {goal}，应为 compare/relationship/predict"}

    # ============ 比较差异 ============

    def _recommend_comparison(self, dv_type, n_groups, design,
                             n_factors, assumptions_met) -> Dict:
        """推荐组间/组内比较的检验"""

        # 分类因变量 → 卡方
        if dv_type == "categorical":
            return {
                "推荐检验": "卡方检验 (Chi-square test)",
                "适用": "比较分类因变量在不同组的分布",
                "前提假设": ["每个单元格期望频数 ≥ 5", "观测相互独立"],
                "小样本备选": "Fisher 精确检验 (当期望频数 < 5)",
                "Python函数": "scipy.stats.chi2_contingency()",
            }

        # 多因素 → 多因素方差分析
        if n_factors >= 2:
            return {
                "推荐检验": f"{n_factors}因素方差分析 ({n_factors}-way ANOVA)",
                "适用": f"检验 {n_factors} 个自变量的主效应及交互作用",
                "前提假设": ["因变量近似正态", "方差齐性", "观测独立"],
                "非参数备选": "对齐秩变换 ANOVA (ART) 或稳健方法",
                "后续分析": "若交互显著，做简单效应分析；主效应显著做事后比较",
                "Python函数": "statsmodels.formula.api.ols() + anova_lm() / pingouin.anova()",
            }

        # 单因素
        if n_groups is None:
            return {"提示": "比较差异时请提供 n_groups (分组数量)"}

        if n_groups == 1:
            if assumptions_met:
                return {
                    "推荐检验": "单样本 t 检验 (One-sample t-test)",
                    "适用": "样本均值与已知/理论值比较",
                    "前提假设": ["数据近似正态", "观测独立"],
                    "非参数备选": "Wilcoxon 符号秩检验",
                    "Python函数": "scipy.stats.ttest_1samp()",
                }
            else:
                return {
                    "推荐检验": "Wilcoxon 符号秩检验 (单样本)",
                    "适用": "不满足正态假设时的单样本中位数检验",
                    "Python函数": "scipy.stats.wilcoxon()",
                }

        elif n_groups == 2:
            if design == "paired":
                if assumptions_met:
                    return {
                        "推荐检验": "配对样本 t 检验 (Paired t-test)",
                        "适用": "同一被试两个条件/时间点的比较 (被试内)",
                        "前提假设": ["差值近似正态", "配对观测"],
                        "非参数备选": "Wilcoxon 符号秩检验",
                        "效应量": "Cohen's d (配对)",
                        "Python函数": "scipy.stats.ttest_rel()",
                    }
                else:
                    return {
                        "推荐检验": "Wilcoxon 符号秩检验 (Wilcoxon signed-rank)",
                        "适用": "配对设计，不满足正态假设",
                        "Python函数": "scipy.stats.wilcoxon()",
                    }
            else:  # independent
                if assumptions_met:
                    return {
                        "推荐检验": "独立样本 t 检验 (Independent t-test)",
                        "适用": "两个独立组的均值比较 (被试间)",
                        "前提假设": ["各组近似正态", "方差齐性(否则用Welch)", "观测独立"],
                        "非参数备选": "Mann-Whitney U 检验",
                        "效应量": "Cohen's d",
                        "Python函数": "scipy.stats.ttest_ind() (方差不齐设 equal_var=False)",
                    }
                else:
                    return {
                        "推荐检验": "Mann-Whitney U 检验 (Mann-Whitney U)",
                        "适用": "两个独立组，不满足正态假设",
                        "Python函数": "scipy.stats.mannwhitneyu()",
                    }

        else:  # n_groups >= 3
            if design == "paired":
                if assumptions_met:
                    return {
                        "推荐检验": "重复测量方差分析 (Repeated-measures ANOVA)",
                        "适用": "同一被试三个及以上条件/时间点 (被试内)",
                        "前提假设": ["近似正态", "球形性假设(Mauchly检验)"],
                        "非参数备选": "Friedman 检验",
                        "后续分析": "事后成对比较 (含多重比较校正)",
                        "Python函数": "pingouin.rm_anova() / statsmodels AnovaRM",
                    }
                else:
                    return {
                        "推荐检验": "Friedman 检验 (Friedman test)",
                        "适用": "重复测量，三组及以上，不满足正态假设",
                        "Python函数": "scipy.stats.friedmanchisquare()",
                    }
            else:  # independent
                if assumptions_met:
                    return {
                        "推荐检验": "单因素方差分析 (One-way ANOVA)",
                        "适用": "三个及以上独立组的均值比较 (被试间)",
                        "前提假设": ["各组近似正态", "方差齐性", "观测独立"],
                        "非参数备选": "Kruskal-Wallis 检验",
                        "后续分析": "事后比较 (Tukey HSD / Bonferroni)",
                        "效应量": "η² (eta-squared)",
                        "Python函数": "scipy.stats.f_oneway() / pingouin.anova()",
                    }
                else:
                    return {
                        "推荐检验": "Kruskal-Wallis 检验 (Kruskal-Wallis)",
                        "适用": "三组及以上独立组，不满足正态假设",
                        "后续分析": "Dunn 检验事后比较",
                        "Python函数": "scipy.stats.kruskal()",
                    }

    # ============ 检验关系 ============

    def _recommend_relationship(self, dv_type, iv_type, assumptions_met) -> Dict:
        """推荐相关/关联检验"""

        # 两个分类变量
        if dv_type == "categorical" and iv_type == "categorical":
            return {
                "推荐检验": "卡方独立性检验 (Chi-square test of independence)",
                "适用": "检验两个分类变量是否相关",
                "效应量": "Cramér's V / φ系数",
                "Python函数": "scipy.stats.chi2_contingency()",
            }

        # 有序变量
        if dv_type == "ordinal" or iv_type == "ordinal":
            return {
                "推荐检验": "Spearman 等级相关 (Spearman's rho)",
                "适用": "至少一个变量为有序，或不满足线性/正态假设",
                "Python函数": "scipy.stats.spearmanr()",
            }

        # 两个连续变量
        if assumptions_met:
            return {
                "推荐检验": "Pearson 相关 (Pearson's r)",
                "适用": "两个连续变量的线性相关",
                "前提假设": ["双变量正态", "线性关系", "无极端离群值"],
                "非参数备选": "Spearman 等级相关",
                "Python函数": "scipy.stats.pearsonr()",
            }
        else:
            return {
                "推荐检验": "Spearman 等级相关 (Spearman's rho)",
                "适用": "不满足正态/线性假设的相关分析",
                "Python函数": "scipy.stats.spearmanr()",
            }

    # ============ 预测 ============

    def _recommend_prediction(self, dv_type) -> Dict:
        """推荐回归/预测模型"""

        if dv_type == "continuous":
            return {
                "推荐方法": "线性回归 (Linear regression)",
                "适用": "用一个或多个自变量预测连续因变量",
                "前提假设": ["线性", "残差正态", "同方差", "无多重共线性", "残差独立"],
                "扩展": "多个自变量用多元线性回归；非线性关系考虑多项式回归",
                "Python函数": "statsmodels.formula.api.ols() / sklearn LinearRegression",
            }
        elif dv_type == "categorical":
            return {
                "推荐方法": "逻辑回归 (Logistic regression)",
                "适用": "预测二分类/多分类因变量",
                "前提假设": ["观测独立", "自变量与logit线性", "无严重多重共线性"],
                "扩展": "多分类用多项逻辑回归 (multinomial)",
                "Python函数": "statsmodels Logit / sklearn LogisticRegression",
            }
        else:
            return {
                "推荐方法": "有序逻辑回归 (Ordinal logistic regression)",
                "适用": "预测有序因变量",
                "Python函数": "statsmodels OrderedModel / mord",
            }

    # ============ 样本量 / 统计功效 ============

    # Cohen 效应量基准 (小/中/大)
    EFFECT_SIZE_BENCHMARKS = {
        "t_test": {"小": 0.2, "中": 0.5, "大": 0.8, "指标": "Cohen's d"},
        "anova": {"小": 0.1, "中": 0.25, "大": 0.4, "指标": "Cohen's f"},
        "correlation": {"小": 0.1, "中": 0.3, "大": 0.5, "指标": "r"},
        "chi_square": {"小": 0.1, "中": 0.3, "大": 0.5, "指标": "Cohen's w"},
        "regression": {"小": 0.02, "中": 0.15, "大": 0.35, "指标": "f²"},
    }

    def recommend_sample_size(self, test_type: str,
                            effect_size: Optional[float] = None,
                            effect_level: str = "中",
                            alpha: float = 0.05,
                            power: float = 0.8) -> Dict:
        """
        样本量与功效分析建议

        参数:
        -----
        test_type : str
            't_test_independent' / 't_test_paired' / 'anova' /
            'correlation' / 'chi_square' / 'regression'
        effect_size : float, 可选
            预期效应量，不填则用 effect_level 对应的基准值
        effect_level : str
            效应量水平: '小' / '中' / '大' (默认中等)
        alpha : float
            显著性水平 (默认 0.05)
        power : float
            期望统计功效 (默认 0.8)

        返回:
        -----
        dict : 估算样本量及建议
        """
        import math

        # 标准正态分位数 (近似)
        z_table = {0.05: 1.96, 0.01: 2.576, 0.10: 1.645}
        power_table = {0.8: 0.842, 0.9: 1.282, 0.95: 1.645}
        z_alpha = z_table.get(alpha, 1.96)
        z_beta = power_table.get(power, 0.842)

        # 确定效应量
        base_type = "t_test" if "t_test" in test_type else test_type
        benchmark = self.EFFECT_SIZE_BENCHMARKS.get(base_type, {})
        if effect_size is None:
            effect_size = benchmark.get(effect_level, 0.5)

        result = {
            "检验类型": test_type,
            "效应量指标": benchmark.get("指标", ""),
            "采用效应量": f"{effect_size} ({effect_level}效应)",
            "alpha": alpha,
            "目标功效": power,
        }

        # 估算样本量 (近似公式，供规划参考)
        if "t_test" in test_type:
            if "independent" in test_type:
                n_per_group = 2 * ((z_alpha + z_beta) / effect_size) ** 2
                result["每组样本量"] = int(math.ceil(n_per_group))
                result["总样本量"] = int(math.ceil(n_per_group * 2))
            else:  # paired
                n = ((z_alpha + z_beta) / effect_size) ** 2
                result["所需样本量"] = int(math.ceil(n))
        elif test_type == "correlation":
            # Fisher z 变换近似
            z_r = 0.5 * math.log((1 + effect_size) / (1 - effect_size))
            n = ((z_alpha + z_beta) / z_r) ** 2 + 3
            result["所需样本量"] = int(math.ceil(n))
        elif test_type == "anova":
            # 基于 Cohen's f 的粗略估算
            n_per_group = ((z_alpha + z_beta) / effect_size) ** 2 / 2 + 5
            result["每组样本量(粗估)"] = int(math.ceil(n_per_group))
            result["提示"] = "ANOVA 精确样本量依赖组数，建议用专门工具核算"
        else:
            result["提示"] = "该检验建议用专门工具精确计算样本量"

        result["重要说明"] = (
            "以上为基于正态近似的规划估算，仅供初步参考。"
            "正式研究请用 G*Power、pingouin.power_* 或 statsmodels.stats.power 精确计算。"
        )
        result["推荐工具"] = "G*Power (免费) / pingouin / statsmodels.stats.power"
        return result

    # ============ 信度与效度分析 ============

    def recommend_psychometric(self, need: str = "both",
                             scale_type: str = "continuous") -> Dict:
        """
        量表信度与效度分析方法推荐

        参数:
        -----
        need : str
            分析需求: 'reliability'(信度) / 'validity'(效度) /
            'both'(两者) / 'development'(量表开发全流程)
        scale_type : str
            量表类型: 'continuous'(连续/Likert) / 'dichotomous'(二分)
        """
        reliability = {
            "内部一致性信度": {
                "方法": "Cronbach's α (连续/Likert) 或 KR-20 (二分题)",
                "标准": "α ≥ 0.7 可接受，≥ 0.8 良好；维度题目 ≥ 0.6",
                "Python函数": "pingouin.cronbach_alpha()",
            },
            "组合信度": {
                "方法": "组合信度 CR (基于因子载荷)",
                "标准": "CR ≥ 0.7",
                "说明": "验证性因子分析后计算，比 α 更稳健",
            },
            "重测信度": {
                "方法": "两次施测的相关 (Pearson r 或 ICC)",
                "标准": "r ≥ 0.7，间隔 2-4 周",
                "Python函数": "pingouin.intraclass_corr()",
            },
            "评分者信度": {
                "方法": "ICC 组内相关 / Kappa 系数 (分类评分)",
                "Python函数": "pingouin.intraclass_corr() / sklearn cohen_kappa_score()",
            },
        }

        validity = {
            "内容效度": {
                "方法": "专家评定，计算内容效度比 CVR / 内容效度指数 CVI",
                "说明": "题目编制阶段，请领域专家评判题目代表性",
            },
            "结构效度-探索": {
                "方法": "探索性因子分析 EFA",
                "前提": "KMO ≥ 0.6，Bartlett 球形检验显著",
                "用途": "量表开发初期，探索潜在因子结构",
                "Python函数": "factor_analyzer.FactorAnalyzer",
            },
            "结构效度-验证": {
                "方法": "验证性因子分析 CFA",
                "拟合指标": "χ²/df < 3，CFI/TLI > 0.9，RMSEA < 0.08，SRMR < 0.08",
                "用途": "验证已有因子结构假设",
                "Python函数": "semopy (Python) 或 lavaan (R)",
            },
            "聚合效度": {
                "方法": "平均方差抽取量 AVE",
                "标准": "AVE ≥ 0.5，且 CR > AVE",
            },
            "区分效度": {
                "方法": "AVE 平方根 > 因子间相关 (Fornell-Larcker) 或 HTMT < 0.85",
            },
            "效标效度": {
                "方法": "与效标变量的相关 (同时效度/预测效度)",
            },
        }

        result = {"分析需求": need, "量表类型": scale_type}

        if need in ("reliability", "both", "development"):
            result["信度分析"] = reliability
        if need in ("validity", "both", "development"):
            result["效度分析"] = validity

        if need == "development":
            result["量表开发推荐流程"] = [
                "1. 文献回顾 + 专家评定 → 内容效度 (CVI)",
                "2. 预试样本 → 项目分析 (区分度、题总相关)",
                "3. 样本1 → 探索性因子分析 EFA 确定结构",
                "4. 样本2 → 验证性因子分析 CFA 验证结构",
                "5. 计算 Cronbach's α / CR → 信度",
                "6. 计算 AVE + HTMT → 聚合与区分效度",
                "7. 与效标相关 → 效标效度",
            ]
            result["样本量建议"] = "EFA/CFA 建议每题 5-10 人，总样本 ≥ 200"

        return result

    # ============ 中介与调节效应 ============

    def recommend_mediation_moderation(self, model_type: str) -> Dict:
        """
        中介/调节效应模型分析方法推荐

        参数:
        -----
        model_type : str
            'mediation'(中介) / 'moderation'(调节) /
            'moderated_mediation'(有调节的中介) /
            'mediated_moderation'(有中介的调节)
        """
        models = {
            "mediation": {
                "模型": "中介效应 (X → M → Y)",
                "推荐方法": "Bootstrap 法估计间接效应的置信区间",
                "PROCESS模型": "Model 4",
                "判断标准": "间接效应 a×b 的 Bootstrap 95% CI 不含 0 即显著",
                "不推荐": "Baron & Kenny 逐步法 (检验力低，已过时)；Sobel 检验 (假设正态，偏保守)",
                "Bootstrap次数": "建议 5000 次",
                "Python工具": "pingouin.mediation_analysis() (自带 Bootstrap)",
                "效应分解": "总效应 = 直接效应 c' + 间接效应 a×b",
            },
            "moderation": {
                "模型": "调节效应 (X × W → Y)",
                "推荐方法": "层级回归 + 交互项 (自变量与调节变量先中心化)",
                "PROCESS模型": "Model 1",
                "关键步骤": [
                    "1. 中心化或标准化 X 和 W (减少多重共线性)",
                    "2. 构造乘积项 X×W",
                    "3. 回归: Y = b0 + b1·X + b2·W + b3·(X×W)",
                    "4. b3 显著则存在调节效应",
                ],
                "后续分析": "简单斜率分析 (simple slopes) + Johnson-Neyman 区间",
                "可视化": "绘制不同调节变量水平 (±1SD) 下的回归线",
                "Python工具": "statsmodels OLS + 手动构造交互项",
            },
            "moderated_mediation": {
                "模型": "有调节的中介 (中介路径受调节变量影响)",
                "推荐方法": "Bootstrap + 被调节的中介指数 (index of moderated mediation)",
                "PROCESS模型": "Model 7 (调节a路径) / 14 (调节b路径) / 58 / 59 等",
                "判断标准": "被调节的中介指数的 Bootstrap CI 不含 0",
                "说明": "需明确调节变量作用于哪条路径 (a路径、b路径或两者)",
                "Python工具": "建议用 R lavaan / Mplus 或 SPSS PROCESS",
            },
            "mediated_moderation": {
                "模型": "有中介的调节 (调节效应通过中介传递)",
                "推荐方法": "结合调节与中介分析框架",
                "说明": "理论上较少用，多数情境可重构为有调节的中介",
                "Python工具": "结构方程模型 (semopy / lavaan)",
            },
        }

        result = models.get(model_type)
        if result is None:
            return {
                "错误": f"未知模型类型: {model_type}",
                "可选": "mediation / moderation / moderated_mediation / mediated_moderation",
            }

        result["通用提示"] = (
            "中介/调节分析需有理论依据支撑因果方向；"
            "横断面数据的中介推断需谨慎，纵向设计更有说服力。"
        )
        return result

    # ============ 交互式问答 ============

    def interactive_guide(self) -> Dict:
        """
        交互式引导 (命令行问答)
        逐步提问后给出推荐
        """
        print("=" * 50)
        print("  研究方法决策助手 - 交互式引导")
        print("=" * 50)

        print("\n[1] 你的研究目的是什么？")
        print("  1) 比较组间/条件差异")
        print("  2) 检验变量间关系")
        print("  3) 用变量预测结果")
        goal_map = {"1": "compare", "2": "relationship", "3": "predict"}
        goal = goal_map.get(input("请输入 (1/2/3): ").strip(), "compare")

        print("\n[2] 因变量(结果变量)是什么类型？")
        print("  1) 连续变量 (如反应时、得分)")
        print("  2) 分类变量 (如是/否、类别)")
        print("  3) 有序变量 (如等级、Likert量表)")
        dv_map = {"1": "continuous", "2": "categorical", "3": "ordinal"}
        dv_type = dv_map.get(input("请输入 (1/2/3): ").strip(), "continuous")

        kwargs = {"goal": goal, "dv_type": dv_type}

        if goal == "compare":
            n_groups = int(input("\n[3] 有几个组/条件？(输入数字): ").strip() or "2")
            kwargs["n_groups"] = n_groups
            if n_groups >= 2:
                print("\n[4] 实验设计？")
                print("  1) 被试间/独立 (不同被试)")
                print("  2) 被试内/配对 (同一被试)")
                design_map = {"1": "independent", "2": "paired"}
                kwargs["design"] = design_map.get(input("请输入 (1/2): ").strip(), "independent")
            n_factors = int(input("\n[5] 有几个自变量(因素)？(输入数字): ").strip() or "1")
            kwargs["n_factors"] = n_factors
            assume = input("\n[6] 数据是否满足正态性/方差齐性假设？(y/n): ").strip().lower()
            kwargs["assumptions_met"] = assume != "n"

        elif goal == "relationship":
            print("\n[3] 另一个变量(自变量)是什么类型？")
            print("  1) 连续  2) 分类  3) 有序")
            iv_map = {"1": "continuous", "2": "categorical", "3": "ordinal"}
            kwargs["iv_type"] = iv_map.get(input("请输入 (1/2/3): ").strip(), "continuous")
            assume = input("\n[4] 满足正态性/线性假设？(y/n): ").strip().lower()
            kwargs["assumptions_met"] = assume != "n"

        result = self.recommend_test(**kwargs)
        print("\n" + "=" * 50)
        print("  推荐结果")
        print("=" * 50)
        for key, value in result.items():
            if isinstance(value, list):
                print(f"\n{key}:")
                for v in value:
                    print(f"  • {v}")
            else:
                print(f"\n{key}: {value}")
        return result


# ============ 使用示例 ============

if __name__ == "__main__":
    advisor = StatTestAdvisor()

    # 示例1: 两组独立样本，连续因变量 (如凝视线索的两种条件)
    print("=== 示例1: 两组独立，连续因变量 ===")
    r1 = advisor.recommend_test(
        goal="compare", dv_type="continuous",
        n_groups=2, design="independent"
    )
    print(f"推荐: {r1['推荐检验']}\n")

    # 示例2: 2x2 被试内设计 (如情绪×同余性)
    print("=== 示例2: 双因素方差分析 ===")
    r2 = advisor.recommend_test(
        goal="compare", dv_type="continuous",
        n_groups=4, design="paired", n_factors=2
    )
    print(f"推荐: {r2['推荐检验']}\n")

    # 示例3: 检验两个连续变量关系
    print("=== 示例3: 相关分析 ===")
    r3 = advisor.recommend_test(
        goal="relationship", dv_type="continuous", iv_type="continuous"
    )
    print(f"推荐: {r3['推荐检验']}\n")

    # 示例4: 不满足正态假设的两组比较
    print("=== 示例4: 非参数检验 ===")
    r4 = advisor.recommend_test(
        goal="compare", dv_type="continuous",
        n_groups=2, design="independent", assumptions_met=False
    )
    print(f"推荐: {r4['推荐检验']}")
