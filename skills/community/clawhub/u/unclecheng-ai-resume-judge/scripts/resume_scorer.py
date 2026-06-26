"""
AI-Resume-Judge 简历评分引擎
基于 AI 领域满分(100)与及格线(60)两份参考简历的对比分析
"""

import re
import json
from datetime import datetime
from typing import Optional

# ============================================================
# 行业等价系数表
# ============================================================
INDUSTRY_EQUIVALENCE = {
    "ai": 1.00,
    "llm": 1.00,
    "大模型": 1.00,
    "机器学习": 1.00,
    "深度学习": 1.00,
    "自动驾驶": 0.88,
    "机器人": 0.88,
    "嵌入式": 0.82,
    "金融": 0.92,
    "量化": 0.92,
    "投行": 0.88,
    "咨询": 0.80,
    "游戏": 0.82,
    "图形学": 0.82,
    "前端": 0.70,
    "移动开发": 0.70,
    "ios": 0.70,
    "android": 0.70,
    "后端": 0.72,
    "devops": 0.72,
    "云计算": 0.75,
    "数据": 0.65,
    "数据分析": 0.65,
    "bi": 0.65,
    "产品": 0.60,
    "pm": 0.60,
    "运营": 0.55,
    "市场": 0.50,
    "财务": 0.55,
    "会计": 0.50,
    "行政": 0.45,
    "人力资源": 0.45,
    "教育": 0.55,
    "医疗": 0.70,
    "建筑": 0.65,
    "设计": 0.60,
    "法律": 0.58,
    "供应链": 0.62,
    "电商": 0.68,
    "新媒体": 0.48,
    "销售": 0.45,
}

# AI领域关键词
AI_STRONG_KEYWORDS = [
    "llm", "大模型", "gpt", "transformer", "rlhf", "lora",
    "rag", "agent", "prompt", "vllm", "langchain", "autogen",
    "crewai", "harness", "dpo", "ppo", "sft",
    "agentic", "multi-agent", "模型对齐", "对齐训练",
]

AI_WEAK_KEYWORDS = [
    "nlp", "cv", "机器学习", "深度学习", "算法",
    "数据科学", "推荐系统", "知识图谱", "语音",
    "tensorflow", "pytorch", "huggingface", "bert",
    "lstm", "cnn", "gan", "diffusion",
]

# 非AI行业标识关键词（排除项目/论文中的通用词）
# 仅包含明确的职业/行业标识词，避免"基金"(项目)、"教学"(章节)等误触发
NON_AI_KEYWORDS = [
    "会计师", "注册会计师",
    "财务总监", "cfo", "投行", "券商", "银行柜员", "保险代理",
    "建筑师", "施工员", "造价员", "结构工程师", "建造师",
    "律师", "法务顾问", "合规官",
    "临床医学", "护士", "执业医师", "药剂师",
    "语文教师", "数学教师", "英语教师", "培训讲师", "课程顾问",
    "行政专员", "人力资源专员", "人力资源总监", "招聘专员", "绩效考核专员",
    "市场专员", "品牌经理", "推广", "渠道经理",
    "销售经理", "商务经理", "客户经理", "bd经理",
    "物流管理", "供应链经理", "采购专员",
    "新媒体运营", "内容编辑", "记者", "编导",
    "游戏策划", "游戏运营", "美术设计",
    "产品经理", "需求分析师",
]

# 模糊动词（扣分标记）
WEAK_VERBS = [
    "参与", "配合", "协助", "做一些", "做过", "参与过",
    "协助过", "配合完成", "参与了部分", "负责了一些",
    "做了点", "干过", "接触过",
]

# 强动词（得分标记）
STRONG_VERBS = [
    "主导", "负责", "设计", "构建", "落地", "推动",
    "独立", "从零", "搭建", "实现", "优化", "提升",
    "重构", "带领", "管理", "产出", "构建",
]

# 量化指标模式
QUANTITY_PATTERNS = [
    r"\d+%", r"\d+倍", r"\d+[千万亿]?", r"\d+万次",
    r"\d+亿", r"\d+万用户", r"\d+万token", r"\d+亿参数",
    r"¥\d+", r"\$\d+", r"QPS", r"P99", r"ms", r"TB",
    r"PB", r"GPU", r"A100", r"H100",
]


# ============================================================
# 评分引擎
# ============================================================

class ResumeScorer:
    """简历评分引擎"""

    # 维度权重配置
    DIMENSIONS = {
        "basic_info": {"name": "基本信息完整性", "max": 15},
        "quantification": {"name": "成就量化程度", "max": 25},
        "tech_depth": {"name": "技术深度与广度", "max": 20},
        "experience": {"name": "工作经历质量", "max": 20},
        "education": {"name": "教育背景", "max": 8},
        "brand": {"name": "个人品牌/影响力", "max": 7},
        "expression": {"name": "表达能力", "max": 5},
    }

    def __init__(self):
        self.text = ""
        self.industry = "unknown"
        self.is_ai_field = True
        self.dimension_scores = {}

    # ----------------------------------------------------------
    # 公开API
    # ----------------------------------------------------------

    def score(self, text: str) -> dict:
        """
        主评分入口
        Returns: 完整评分报告字典
        """
        self.text = text
        self._detect_field()
        self._score_all_dimensions()
        report = self._generate_report()
        return report

    def detect_field(self, text: str) -> tuple[bool, str]:
        """检测简历领域，返回(is_ai_field, industry)"""
        self.text = text
        self._detect_field()
        return self.is_ai_field, self.industry

    # ----------------------------------------------------------
    # 内部评分逻辑
    # ----------------------------------------------------------

    def _detect_field(self):
        """检测简历所属行业与是否属于AI领域"""
        text_lower = self.text.lower()

        # 检查是否是非AI行业（仅精准匹配职业/岗位标识）
        for kw in NON_AI_KEYWORDS:
            if kw.lower() in text_lower:
                self.is_ai_field = False
                self.industry = kw
                return

        # AI领域强关键词
        strong_count = sum(1 for kw in AI_STRONG_KEYWORDS if kw.lower() in text_lower)
        # AI领域弱关键词
        weak_count = sum(1 for kw in AI_WEAK_KEYWORDS if kw.lower() in text_lower)

        if strong_count >= 2 or weak_count >= 4:
            self.is_ai_field = True
            self.industry = "AI / 大模型"
        else:
            self.is_ai_field = False
            self.industry = self._infer_industry(text_lower)

    def _infer_industry(self, text_lower: str) -> str:
        """从文本推断行业（排除章节标题关键词）"""
        # 排除常见章节标题词
        skip_phrases = [
            "教育背景", "教学", "培训", "课程",
            "工作经验", "工作经历", "工作背景",
            "专业技能", "个人简介", "项目经验", "项目经历",
            "量化", "数量化", "数学",
        ]
        for phrase in skip_phrases:
            text_lower = text_lower.replace(phrase, "")

        # 用更精确的短语匹配，避免"融资"匹配"金融"这类问题
        industry_map = [
            ("金融", ["投行", "券商", "对冲基金", "公募基金", "私募基金", "银行信贷", "证券交易"]),
            ("前端", ["前端开发", "react", "vue.js", "angular", "html5", "css3", "javascript"]),
            ("后端", ["后端开发", "java开发", "golang", "rust", "django", "springboot"]),
            ("数据", ["etl", "hive", "spark", "flink", "kafka", "数据仓库", "大数据"]),
            ("产品", ["产品经理", "PRD", "需求分析", "axure", "原型设计"]),
            ("游戏", ["unity3d", "unreal", "cocos", "游戏开发", "shader编程"]),
            ("移动", ["ios开发", "android开发", "flutter", "react native"]),
            ("DevOps", ["devops", "docker", "k8s", "jenkins", "cicd", "gitlab"]),
            ("医疗", ["医院", "临床医学", "医疗器械", "生物制药", "药企"]),
            ("建筑", ["施工", "工程造价", "BIM", "结构设计", "建筑师"]),
            ("法律", ["律师", "法务", "合规", "诉讼法"]),
            ("咨询", ["管理咨询", "战略咨询", "麦肯锡", "贝恩", "波士顿"]),
            ("电商", ["电商运营", "跨境电商", "淘宝", "京东", "拼多多商家"]),
            ("新媒体", ["短视频运营", "抖音", "小红书", "内容运营"]),
            ("物流", ["仓储", "物流配送", "供应链管理", "货运"]),
            ("销售", ["销售经理", "商务拓展", "客户经理", "渠道管理"]),
            ("市场", ["品牌营销", "市场推广", "数字营销", "营销策划"]),
        ]
        for industry, keywords in industry_map:
            for kw in keywords:
                if kw.lower() in text_lower:
                    return industry
        return "通用"

    def _score_all_dimensions(self):
        """计算所有维度得分"""
        t = self.text

        self.dimension_scores = {
            "basic_info": self._score_basic_info(t),
            "quantification": self._score_quantification(t),
            "tech_depth": self._score_tech_depth(t),
            "experience": self._score_experience(t),
            "education": self._score_education(t),
            "brand": self._score_brand(t),
            "expression": self._score_expression(t),
        }

    # ---- 维度评分具体实现 ----

    def _score_basic_info(self, t: str) -> float:
        """基本信息完整性（满分15）"""
        score = 0.0
        max_score = self.DIMENSIONS["basic_info"]["max"]

        # 邮箱 (2分)
        if re.search(r"[\w.-]+@[\w.-]+\.\w+", t):
            score += 2
        # 手机号 (2分)
        if re.search(r"\d{3}[-\s]?\d{4}[-\s]?\d{4}", t) or re.search(r"1[3-9]\d{9}", t):
            score += 2
        # GitHub (3分)
        if re.search(r"github\.com/[\w-]+", t, re.IGNORECASE):
            score += 3
        # LinkedIn (3分)
        if re.search(r"linkedin\.com/in/[\w-]+", t, re.IGNORECASE):
            score += 3
        # 所在地 (1分)
        if re.search(r"[\u4e00-\u9fa5]{2,6}[/\u5730]\s*[北京上海深圳杭州广州]", t):
            score += 1
        elif re.search(r"(北京|上海|深圳|杭州|广州|成都|武汉|南京)", t):
            score += 1
        # 简历结构完整度（求职意向/个人简介等）(4分)
        structure_score = 0
        if re.search(r"(个人简介|about|summary|overview)", t, re.IGNORECASE):
            structure_score += 1.5
        if re.search(r"(工作经验|工作经历|工作背景)", t, re.IGNORECASE):
            structure_score += 1
        if re.search(r"(教育背景|学历)", t, re.IGNORECASE):
            structure_score += 1
        if re.search(r"(技能|技术栈)", t, re.IGNORECASE):
            structure_score += 0.5
        score += structure_score

        return min(score, max_score)

    def _score_quantification(self, t: str) -> float:
        """成就量化程度（满分25）"""
        score = 0.0
        max_score = self.DIMENSIONS["quantification"]["max"]

        # 统计量化指标出现次数
        quantity_matches = sum(len(re.findall(p, t)) for p in QUANTITY_PATTERNS)
        score += min(quantity_matches * 1.5, 8)  # 最多8分

        # 强动词出现（代表主导）
        strong_verb_count = sum(len(re.findall(v, t)) for v in STRONG_VERBS)
        score += min(strong_verb_count * 1.0, 6)  # 最多6分

        # 模糊动词扣分
        weak_verb_count = sum(len(re.findall(v, t)) for v in WEAK_VERBS)
        score -= weak_verb_count * 1.5

        # 百分比/倍数/具体数字密度
        pct_lines = [line for line in t.split("\n") if re.search(r"\d+%|\d+倍|\d+万|\d+亿", line)]
        score += min(len(pct_lines) * 1.2, 6)  # 最多6分

        # 业务影响描述（有规模感）
        impact_phrases = ["日均", "每月", "每年", "覆盖", "服务", "用户量", "提升", "降低", "节省"]
        impact_count = sum(1 for p in impact_phrases if p in t)
        score += min(impact_count * 0.5, 5)  # 最多5分

        return max(0.0, min(score, max_score))

    def _score_tech_depth(self, t: str) -> float:
        """技术深度与广度（满分20）"""
        score = 0.0
        max_score = self.DIMENSIONS["tech_depth"]["max"]

        # AI领域技术栈检测
        ai_tech_count = sum(1 for kw in AI_STRONG_KEYWORDS + AI_WEAK_KEYWORDS if kw.lower() in t.lower())
        score += min(ai_tech_count * 0.8, 10)  # 最多10分

        # 前沿技术
        frontier_tech = ["llm", "agent", "rag", "rlhf", "dpo", "vllm", "langgraph", "autogen", "harness"]
        frontier_count = sum(1 for kw in frontier_tech if kw.lower() in t.lower())
        score += min(frontier_count * 1.0, 5)  # 最多5分

        # 技能是否有层次（精通/熟练/了解）
        if re.search(r"(精通|熟练|掌握|了解|master|proficient|familiar)", t, re.IGNORECASE):
            score += 3
        else:
            # 无层次描述扣分
            score -= 1

        # 技术工具覆盖度
        tools = ["docker", "k8s", "kubernetes", "terraform", "aws", "gcp", "azure", "hadoop", "spark"]
        tool_count = sum(1 for tool in tools if tool.lower() in t.lower())
        score += min(tool_count * 0.4, 2)  # 最多2分

        return max(0.0, min(score, max_score))

    def _score_experience(self, t: str) -> float:
        """工作经历质量（满分20）"""
        score = 0.0
        max_score = self.DIMENSIONS["experience"]["max"]

        # 公司名称检测（是否有知名公司）
        known_companies = [
            "google", "meta", "apple", "microsoft", "amazon", "openai", "anthropic",
            "nvidia", "intel", "tesla", "字节", "腾讯", "阿里", "百度", "华为",
            "商汤", "旷视", "依图", "寒武纪", "第四范式", "科大讯飞", "大疆",
            "蚂蚁", "京东", "美团", "拼多多", "快手", "小红书",
        ]
        company_count = sum(1 for co in known_companies if co.lower() in t.lower())
        score += min(company_count * 1.5, 5)  # 最多5分

        # 工作段数（稳定性）
        exp_sections = re.findall(r"(20\d{2}|201\d|202\d)[-–—~至].{0,30}(工程师|算法|开发|研究|设计|总监|经理|主管)", t)
        score += min(len(exp_sections) * 1.5, 4)  # 最多4分

        # 时间跨度
        years = re.findall(r"201[5-9]|202[0-9]", t)
        if len(set(years)) >= 5:
            score += 4
        elif len(set(years)) >= 3:
            score += 2
        elif len(set(years)) >= 1:
            score += 1

        # 主导动词出现次数
        lead_verbs = ["主导", "负责", "独立", "从零", "搭建", "带领"]
        lead_count = sum(len(re.findall(v, t)) for v in lead_verbs)
        score += min(lead_count * 0.8, 4)  # 最多4分

        # 职位级别（是否Senior/Lead/专家）
        if re.search(r"(senior|lead|专家|资深|负责人|主管|总监|principal)", t, re.IGNORECASE):
            score += 3

        return max(0.0, min(score, max_score))

    def _score_education(self, t: str) -> float:
        """教育背景（满分8）"""
        score = 0.0
        max_score = self.DIMENSIONS["education"]["max"]

        # 学历
        if re.search(r"(博士|phd|doctor)", t, re.IGNORECASE):
            score += 5
        elif re.search(r"(硕士|master|研究生)", t, re.IGNORECASE):
            score += 4
        elif re.search(r"(本科|bachelor|大学|职业技术学院|高等专科)", t, re.IGNORECASE):
            score += 2

        # 985/211
        if re.search(r"(985|211|top\s*30|C9|常青藤)", t, re.IGNORECASE):
            score += 2

        # GPA/排名
        if re.search(r"gpa[:\s]*[3-4]", t, re.IGNORECASE):
            score += 1

        # 论文/publication
        if re.search(r"(paper|论文|publication|arxiv|emlnlp|icml|neurips|kdd)", t, re.IGNORECASE):
            score += 1.5

        return max(0.0, min(score, max_score))

    def _score_brand(self, t: str) -> float:
        """个人品牌/影响力（满分7）"""
        score = 0.0
        max_score = self.DIMENSIONS["brand"]["max"]

        # GitHub star
        github_star = re.findall(r"⭐\s*([\d,]+)|star[s]?\s*([\d,]+)", t, re.IGNORECASE)
        if github_star:
            for match in github_star:
                num_str = match[0] or match[1]
                num = int(num_str.replace(",", ""))
                if num >= 1000:
                    score += 3
                elif num >= 100:
                    score += 2
                elif num >= 10:
                    score += 1

        # 开源项目提及
        if re.search(r"(github|开源|open.?source|contribute)", t, re.IGNORECASE):
            score += 1

        # 演讲/会议
        if re.search(r"(演讲|分享|speak|conference|顶会|大会)", t, re.IGNORECASE):
            score += 1.5

        # 博客/专栏
        if re.search(r"(博客|blog|专栏|article|medium|公众号)", t, re.IGNORECASE):
            score += 1

        # 证书
        certs = ["aws", "google", "azure", "tensorflow", "pytorch", "kubernetes"]
        cert_count = sum(1 for cert in certs if cert.lower() in t.lower())
        score += min(cert_count * 0.5, 1.5)

        return max(0.0, min(score, max_score))

    def _score_expression(self, t: str) -> float:
        """表达能力（满分5）"""
        score = 0.0
        max_score = self.DIMENSIONS["expression"]["max"]

        # 结构化程度（是否有标题层级）
        headers = len(re.findall(r"^#{1,3}\s+", t, re.MULTILINE))
        score += min(headers * 0.3, 2)

        # 是否有自我评价套话（负分）
        clichés = [
            "认真负责", "学习能力强", "能吃苦耐劳", "良好的团队合作精神",
            "吃苦耐劳", "积极乐观", "踏实肯干", "责任心强",
            "希望能在贵公司", "本人性格",
        ]
        cliché_count = sum(1 for c in clichés if c in t)
        if cliché_count >= 2:
            score -= 2
        elif cliché_count == 1:
            score -= 1

        # 格式规范（无乱码、无缺失section）
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        if len(lines) < 10:
            score -= 1
        if re.search(r"^\|.*\|$", t):  # 有表格
            score += 1

        return max(0.0, min(score, max_score))

    # ----------------------------------------------------------
    # 报告生成
    # ----------------------------------------------------------

    def _generate_report(self) -> dict:
        """生成结构化报告"""
        total = sum(self.dimension_scores.values())

        # 跨行业换算
        if not self.is_ai_field:
            equiv = self._cross_industry_equivalent(total)
        else:
            equiv = {"is_ai": True, "industry": "AI / 大模型", "coefficient": 1.0, "equivalent_score": round(total)}

        # 评级
        rating = self._get_rating(total)

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_ai_field": self.is_ai_field,
            "detected_industry": self.industry,
            "raw_score": round(total, 1),
            "dimensions": {
                dim_id: {
                    "name": self.DIMENSIONS[dim_id]["name"],
                    "score": round(score, 1),
                    "max": self.DIMENSIONS[dim_id]["max"],
                    "pct": round(score / self.DIMENSIONS[dim_id]["max"] * 100),
                }
                for dim_id, score in self.dimension_scores.items()
            },
            "rating": rating,
            "cross_industry": equiv,
        }

        return report

    def _cross_industry_equivalent(self, raw_score: float) -> dict:
        """跨行业等价换算"""
        # 查找最匹配的行业
        industry_key = self.industry.lower()
        coeff = INDUSTRY_EQUIVALENCE.get(industry_key, 0.60)

        # 如果没精确匹配，从industry名称推断
        if coeff == 0.60 and self.industry == "unknown":
            # 尝试模糊匹配
            for ind, c in INDUSTRY_EQUIVALENCE.items():
                if ind in self.text.lower():
                    coeff = c
                    break

        equiv_score = round(raw_score * coeff, 1)
        return {
            "is_ai": False,
            "industry": self.industry,
            "coefficient": coeff,
            "equivalent_score": max(0.0, min(100.0, equiv_score)),
        }

    def _get_rating(self, score: float) -> str:
        """根据分数返回评级"""
        if score >= 90:
            return "S (顶尖)"
        elif score >= 80:
            return "A (优秀)"
        elif score >= 70:
            return "B (良好)"
        elif score >= 60:
            return "C (及格)"
        elif score >= 45:
            return "D (较差)"
        else:
            return "F (不及格)"

    def format_markdown(self, report: dict) -> str:
        """将报告格式化为Markdown"""
        d = report
        lines = [
            "# 📋 简历评分报告",
            "",
            f"**评分时间：** {d['timestamp']}",
            f"**简历领域：** {'✅ AI领域' if d['is_ai_field'] else f'❌ 非AI领域（{d['detected_industry']}）'}",
            f"**原始能力分：** {d['raw_score']} 分",
            "",
            "---",
            "",
            "## 📊 分项得分",
            "",
            "| 维度 | 得分 | 满分 | 得分率 | 评级 |",
            "|------|------|------|--------|------|",
        ]

        for dim_id, info in d["dimensions"].items():
            pct = info["pct"]
            if pct >= 90:
                star = "⭐⭐⭐"
            elif pct >= 70:
                star = "⭐⭐"
            elif pct >= 50:
                star = "⭐"
            else:
                star = "⚠️"
            lines.append(f"| {info['name']} | {info['score']} | {info['max']} | {pct}% | {star} |")

        total_pct = round(d["raw_score"] / 100 * 100)
        lines.extend([
            f"| **总分** | **{d['raw_score']}** | **100** | **{total_pct}%** | **{d['rating']}** |",
            "",
            "---",
        ])

        # 跨行业分析
        if not d["is_ai_field"]:
            c = d["cross_industry"]
            lines.extend([
                "## 🔄 跨行业等价分析",
                "",
                f"- **识别行业：** {c['industry']}",
                f"- **等价系数：** {c['coefficient']}",
                f"- **等价分：** {c['equivalent_score']} 分（相当于AI简历的 {d['raw_score']} 分）",
                "",
                f"> 💡 **解读：** 该简历在所属行业的能力水平，等价于一份 {c['equivalent_score']} 分的AI领域简历。",
                "",
                "---",
            ])

        # 详细点评
        lines.extend([
            "## 📝 详细点评",
            "",
        ])
        for dim_id, info in d["dimensions"].items():
            score = info["score"]
            max_s = info["max"]
            lines.append(f"**{info['name']}**（{score}/{max_s}）")
            if score / max_s >= 0.8:
                lines.append("- ✅ 表现优秀，信息充实且有深度")
            elif score / max_s >= 0.5:
                lines.append("- ⚠️ 有一定内容，但有提升空间")
            else:
                lines.append("- ❌ 缺失较多，需要重点补充")
            lines.append("")

        # 改进建议
        lines.extend([
            "## 🎯 改进建议（Top 3）",
            "",
        ])

        suggestions = self._get_suggestions(d)
        for i, s in enumerate(suggestions, 1):
            lines.append(f"{i}. {s}")

        lines.extend([
            "",
            "---",
            "",
            "> 本评分基于AI领域满分/及格线两份参考简历的对比分析，仅供参考。",
        ])

        return "\n".join(lines)

    def _get_suggestions(self, report: dict) -> list:
        """根据评分短板生成改进建议"""
        suggestions = []
        dims = report["dimensions"]

        if dims["basic_info"]["pct"] < 60:
            suggestions.append("**补充联系方式**：添加GitHub、LinkedIn等可验证的技术档案，展示真实影响力")
        if dims["quantification"]["pct"] < 60:
            suggestions.append("**量化成就**：将「参与XX项目」改为「主导XX项目，QPS提升4倍，延迟降低60%」")
        if dims["tech_depth"]["pct"] < 60:
            suggestions.append("**深化技术栈**：补充LLM全链路经验（训练→微调→推理优化→RAG→Agent）")
        if dims["experience"]["pct"] < 60:
            suggestions.append("**强化职责描述**：使用「主导/设计/落地」等强动词，避免「参与/配合」等模糊词")
        if dims["education"]["pct"] < 60:
            suggestions.append("**完善教育背景**：补充GPA、排名、论文或导师项目等学术亮点")
        if dims["brand"]["pct"] < 60:
            suggestions.append("**建立技术品牌**：在GitHub/HuggingFace发布开源项目，撰写技术博客")
        if dims["expression"]["pct"] < 50:
            suggestions.append("**去除套话**：删除「认真负责、学习能力强」等自我评价，用具体成就替代")

        if not suggestions:
            suggestions = ["✅ 简历质量已经很高，继续保持优势并针对细节优化"]
        return suggestions[:3]


# ============================================================
# 命令行入口
# ============================================================

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    if len(sys.argv) < 2:
        print("Usage: python resume_scorer.py <resume_text_or_file>")
        sys.exit(1)

    input_text = sys.argv[1]

    # 如果是文件路径，读取文件
    if "\n" not in input_text and len(input_text) < 200 and not input_text.startswith("="):
        try:
            with open(input_text, "r", encoding="utf-8") as f:
                input_text = f.read()
        except Exception:
            pass

    scorer = ResumeScorer()
    report = scorer.score(input_text)
    md_report = scorer.format_markdown(report)

    # 输出到文件（避免Windows GBK控制台编码问题）
    output_path = "C:/Users/UncleC/Desktop/AIresumejudge/.workbuddy/skill_output_test.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 评分测试输出\n\n")
        f.write(f"**测试文件：** {sys.argv[1]}\n\n")
        f.write(md_report)
        f.write("\n\n## JSON原始数据\n\n```json\n")
        f.write(json.dumps(report, ensure_ascii=False, indent=2))
        f.write("\n```\n")

    print(f"[OK] Report written to: {output_path}")
    print(f"[RAW] Total score: {report['raw_score']} / Rating: {report['rating']}")
