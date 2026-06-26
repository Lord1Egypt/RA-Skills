#!/usr/bin/env python3
"""
优化后的需求分类引擎
基于需求类型驱动的智能识别系统
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class RequirementClassifier:
    """需求分类器 - 多级智能识别"""
    
    def __init__(self):
        # 一级分类模式
        self.primary_patterns = {
            "技术开发": {
                "keywords": ["开发", "编写", "实现", "构建", "创建", "制作", "编程", "代码"],
                "context_words": ["系统", "应用", "软件", "网站", "App", "程序", "工具", "脚本"],
                "weight": 1.0
            },
            "内容创作": {
                "keywords": ["设计", "撰写", "创作", "制作", "文案", "内容", "写作"],
                "context_words": ["海报", "传单", "广告", "文章", "视频", "图片", "PPT", "文档"],
                "weight": 1.0
            },
            "数据分析": {
                "keywords": ["分析", "统计", "报表", "可视化", "挖掘", "预测", "建模"],
                "context_words": ["数据", "图表", "指标", "趋势", "报告", "仪表盘", "大屏"],
                "weight": 1.0
            },
            "业务流程": {
                "keywords": ["流程", "工作流", "审批", "自动化", "集成", "对接"],
                "context_words": ["业务", "操作", "步骤", "节点", "流转", "同步", "协调"],
                "weight": 1.0
            },
            "问题解决": {
                "keywords": ["解决", "修复", "优化", "排查", "调试", "处理"],
                "context_words": ["问题", "故障", "错误", "Bug", "异常", "崩溃", "卡顿"],
                "weight": 1.0
            },
            "咨询服务": {
                "keywords": ["咨询", "建议", "方案", "选型", "评估", "规划", "设计"],
                "context_words": ["架构", "技术", "系统", "方案", "策略", "路线图"],
                "weight": 1.0
            }
        }
        
        # 二级分类模式（更具体的场景）
        self.secondary_patterns = {
            # 技术开发子类
            "Web应用开发": ["网页", "网站", "Web", "前端", "后端", "全栈", "浏览器", "在线"],
            "移动应用开发": ["App", "移动", "手机", "iOS", "Android", "小程序", "H5"],
            "桌面软件开发": ["桌面", "Windows", "macOS", "Linux", "客户端", "安装包"],
            "API接口开发": ["API", "接口", "服务", "REST", "GraphQL", "微服务"],
            "数据库设计": ["数据库", "表", "字段", "SQL", "NoSQL", "存储", "查询"],
            
            # 内容创作子类
            "营销文案": ["营销", "促销", "广告", "推广", "宣传", "品牌", "销售"],
            "技术文档": ["文档", "说明", "手册", "指南", "教程", "API文档", "帮助"],
            "视觉设计": ["设计", "视觉", "UI", "UX", "界面", "图标", "配色", "布局"],
            "视频制作": ["视频", "剪辑", "制作", "动画", "特效", "配音", "字幕"],
            "演示文稿": ["PPT", "演示", "幻灯片", "汇报", "展示", "演讲"],
            
            # 数据分析子类
            "业务报表": ["报表", "报告", "统计", "汇总", "日报", "周报", "月报"],
            "数据可视化": ["可视化", "图表", "仪表盘", "大屏", "图形", "趋势图"],
            "用户行为分析": ["用户", "行为", "留存", "转化", "活跃", "漏斗", "路径"],
            "销售数据分析": ["销售", "订单", "收入", "客户", "产品", "渠道", "区域"],
            "预测建模": ["预测", "模型", "算法", "机器学习", "AI", "智能", "推荐"],
            
            # 业务流程子类
            "审批流程": ["审批", "审核", "批准", "同意", "拒绝", "签字", "盖章"],
            "工作流设计": ["工作流", "流程", "节点", "流转", "任务", "分配", "跟踪"],
            "系统集成": ["集成", "对接", "同步", "接口", "API对接", "数据交换"],
            "自动化流程": ["自动化", "机器人", "RPA", "脚本", "定时", "触发"],
            
            # 问题解决子类
            "性能优化": ["性能", "速度", "响应", "延迟", "卡顿", "慢", "优化"],
            "故障排查": ["故障", "错误", "异常", "崩溃", "无法", "不行", "问题"],
            "安全加固": ["安全", "漏洞", "攻击", "防护", "加密", "权限", "认证"],
            "兼容性修复": ["兼容", "适配", "浏览器", "设备", "版本", "系统"],
            
            # 咨询服务子类
            "技术选型": ["选型", "技术", "框架", "工具", "平台", "方案", "比较"],
            "架构设计": ["架构", "设计", "系统", "模块", "组件", "服务", "部署"],
            "项目规划": ["规划", "计划", "时间", "资源", "预算", "里程碑", "路线图"],
            "风险评估": ["风险", "评估", "安全", "合规", "法律", "政策", "标准"]
        }
        
        # 行业背景识别
        self.industry_patterns = {
            "电商": ["商品", "订单", "支付", "购物车", "库存", "物流", "促销", "客户"],
            "教育": ["课程", "学生", "教师", "学习", "考试", "成绩", "教学", "培训"],
            "医疗": ["患者", "病历", "诊断", "药品", "预约", "医生", "医院", "健康"],
            "金融": ["账户", "交易", "支付", "风控", "投资", "理财", "贷款", "保险"],
            "制造": ["生产", "设备", "质量", "工艺", "供应链", "库存", "工厂", "产品"],
            "社交": ["用户", "好友", "消息", "社区", "分享", "评论", "点赞", "关注"],
            "游戏": ["游戏", "玩家", "关卡", "道具", "积分", "排名", "竞技", "娱乐"],
            "政务": ["政务", "政府", "审批", "办事", "服务", "政策", "法规", "公开"]
        }
        
        # 紧急程度识别
        self.urgency_patterns = {
            "紧急": ["尽快", "马上", "立即", "今天", "现在", "紧急", "迫切", "急需"],
            "重要": ["重要", "关键", "核心", "必须", "必要", "优先", "主要", "重点"],
            "常规": ["常规", "普通", "一般", "日常", "计划内", "标准", "正常"],
            "优化": ["优化", "改进", "提升", "增强", "完善", "美化", "优化"]
        }
        
        # 复杂度识别规则
        self.complexity_rules = [
            (5, "简单"),      # 少于5个词
            (15, "中等"),     # 5-15个词
            (float('inf'), "复杂")  # 多于15个词
        ]
        
    def classify(self, text: str, history: List[str] = None) -> Dict:
        """执行完整的需求分类"""
        text_lower = text.lower()
        
        # 1. 一级分类识别
        primary_result = self._classify_primary(text_lower)
        
        # 2. 二级分类识别
        secondary_result = self._classify_secondary(text_lower, primary_result["category"])
        
        # 3. 行业背景识别
        industry_result = self._classify_industry(text_lower)
        
        # 4. 紧急程度识别
        urgency_result = self._classify_urgency(text_lower)
        
        # 5. 复杂度评估
        complexity_result = self._assess_complexity(text)
        
        # 6. 用户习惯分析（如果有历史）
        user_pattern = self._analyze_user_pattern(history) if history else None
        
        # 综合结果
        result = {
            "text": text,
            "classification": {
                "primary": primary_result,
                "secondary": secondary_result
            },
            "context": {
                "industry": industry_result,
                "urgency": urgency_result,
                "complexity": complexity_result
            },
            "user_pattern": user_pattern,
            "confidence": self._calculate_confidence(primary_result, secondary_result),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _classify_primary(self, text: str) -> Dict:
        """一级分类识别"""
        scores = {}
        matched_keywords = {}
        
        for category, patterns in self.primary_patterns.items():
            keyword_score = 0
            context_score = 0
            matched = []
            
            # 关键词匹配
            for keyword in patterns["keywords"]:
                if keyword in text:
                    keyword_score += 1
                    matched.append(keyword)
            
            # 上下文词匹配
            for context_word in patterns["context_words"]:
                if context_word in text:
                    context_score += 0.5
                    matched.append(context_word)
            
            # 计算总分
            total_score = (keyword_score + context_score) * patterns["weight"]
            if total_score > 0:
                scores[category] = total_score
                matched_keywords[category] = matched
        
        if scores:
            # 找到最高分
            best_category = max(scores, key=scores.get)
            best_score = scores[best_category]
            
            # 计算置信度
            total_possible = len(self.primary_patterns[best_category]["keywords"]) + \
                           len(self.primary_patterns[best_category]["context_words"]) * 0.5
            confidence = best_score / total_possible if total_possible > 0 else 0
            
            return {
                "category": best_category,
                "score": best_score,
                "confidence": min(confidence, 1.0),
                "matched_keywords": matched_keywords.get(best_category, []),
                "all_scores": scores
            }
        
        # 默认分类
        return {
            "category": "技术开发",
            "score": 0.1,
            "confidence": 0.1,
            "matched_keywords": [],
            "all_scores": {}
        }
    
    def _classify_secondary(self, text: str, primary_category: str) -> Dict:
        """二级分类识别"""
        # 根据一级分类筛选相关二级分类
        related_secondary = {}
        
        # 简单的映射关系
        primary_to_secondary = {
            "技术开发": ["Web应用开发", "移动应用开发", "桌面软件开发", "API接口开发", "数据库设计"],
            "内容创作": ["营销文案", "技术文档", "视觉设计", "视频制作", "演示文稿"],
            "数据分析": ["业务报表", "数据可视化", "用户行为分析", "销售数据分析", "预测建模"],
            "业务流程": ["审批流程", "工作流设计", "系统集成", "自动化流程"],
            "问题解决": ["性能优化", "故障排查", "安全加固", "兼容性修复"],
            "咨询服务": ["技术选型", "架构设计", "项目规划", "风险评估"]
        }
        
        candidate_categories = primary_to_secondary.get(primary_category, [])
        
        scores = {}
        for category in candidate_categories:
            if category in self.secondary_patterns:
                keywords = self.secondary_patterns[category]
                score = sum(1 for kw in keywords if kw in text)
                if score > 0:
                    scores[category] = score
        
        if scores:
            best_category = max(scores, key=scores.get)
            best_score = scores[best_category]
            
            # 计算置信度
            total_keywords = len(self.secondary_patterns[best_category])
            confidence = best_score / total_keywords if total_keywords > 0 else 0
            
            return {
                "category": best_category,
                "score": best_score,
                "confidence": min(confidence, 1.0),
                "matched_keywords": [kw for kw in self.secondary_patterns[best_category] if kw in text],
                "all_scores": scores
            }
        
        # 返回通用二级分类
        return {
            "category": f"{primary_category}通用",
            "score": 0.1,
            "confidence": 0.1,
            "matched_keywords": [],
            "all_scores": {}
        }
    
    def _classify_industry(self, text: str) -> Dict:
        """行业背景识别"""
        scores = {}
        for industry, keywords in self.industry_patterns.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[industry] = score
        
        if scores:
            best_industry = max(scores, key=scores.get)
            best_score = scores[best_industry]
            
            confidence = best_score / len(self.industry_patterns[best_industry])
            
            return {
                "industry": best_industry,
                "score": best_score,
                "confidence": min(confidence, 1.0),
                "matched_keywords": [kw for kw in self.industry_patterns[best_industry] if kw in text]
            }
        
        return {
            "industry": "通用",
            "score": 0,
            "confidence": 0,
            "matched_keywords": []
        }
    
    def _classify_urgency(self, text: str) -> Dict:
        """紧急程度识别"""
        for level, keywords in self.urgency_patterns.items():
            if any(kw in text for kw in keywords):
                matched = [kw for kw in keywords if kw in text]
                return {
                    "level": level,
                    "matched_keywords": matched,
                    "confidence": len(matched) / len(keywords) if keywords else 0
                }
        
        return {
            "level": "常规",
            "matched_keywords": [],
            "confidence": 0.5
        }
    
    def _assess_complexity(self, text: str) -> Dict:
        """复杂度评估"""
        # 基于词数
        word_count = len(text.split())
        
        # 基于句子结构
        sentence_count = len(re.split(r'[。！？!?.]', text))
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # 基于特殊字符
        special_chars = len(re.findall(r'[，、；:;]', text))
        
        # 综合评估
        complexity_score = (
            min(word_count / 50, 1.0) * 0.4 +  # 词数权重40%
            min(avg_words_per_sentence / 20, 1.0) * 0.3 +  # 句子复杂度30%
            min(special_chars / 10, 1.0) * 0.3  # 结构复杂度30%
        )
        
        # 确定复杂度等级
        if complexity_score < 0.3:
            level = "简单"
        elif complexity_score < 0.7:
            level = "中等"
        else:
            level = "复杂"
        
        return {
            "level": level,
            "score": complexity_score,
            "metrics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_words_per_sentence": avg_words_per_sentence,
                "special_chars": special_chars
            }
        }
    
    def _analyze_user_pattern(self, history: List[str]) -> Dict:
        """分析用户历史模式"""
        if not history:
            return None
        
        # 统计历史需求类型
        type_counts = {}
        total_requests = len(history)
        
        for req in history[:10]:  # 只分析最近10条
            req_lower = req.lower()
            for category, patterns in self.primary_patterns.items():
                if any(kw in req_lower for kw in patterns["keywords"] + patterns["context_words"]):
                    type_counts[category] = type_counts.get(category, 0) + 1
                    break
        
        # 计算偏好
        preferences = {}
        if type_counts:
            for category, count in type_counts.items():
                preferences[category] = count / total_requests
        
        return {
            "total_requests_analyzed": min(len(history), 10),
            "type_distribution": type_counts,
            "preferences": preferences,
            "most_common_type": max(type_counts, key=type_counts.get) if type_counts else None
        }
    
    def _calculate_confidence(self, primary_result: Dict, secondary_result: Dict) -> float:
        """计算总体置信度"""
        primary_confidence = primary_result.get("confidence", 0)
        secondary_confidence = secondary_result.get("confidence", 0)
        
        # 加权计算：一级分类权重70%，二级分类权重30%
        total_confidence = primary_confidence * 0.7 + secondary_confidence * 0.3
        
        return min(total_confidence, 1.0)
    
    def generate_classification_report(self, classification_result: Dict) -> str:
        """生成分类报告"""
        report = []
        report.append("=" * 60)
        report.append("需求分类分析报告")
        report.append("=" * 60)
        report.append(f"原始需求: {classification_result['text']}")
        report.append("")
        
        # 分类结果
        primary = classification_result['classification']['primary']
        secondary = classification_result['classification']['secondary']
        
        report.append("📊 分类结果:")
        report.append(f"  一级分类: {primary['category']} (置信度: {primary['confidence']:.1%})")
        report.append(f"  二级分类: {secondary['category']} (置信度: {secondary['confidence']:.1%})")
        report.append(f"  总体置信度: {classification_result['confidence']:.1%}")
        report.append("")
        
        # 上下文信息
        context = classification_result['context']
        report.append("📝 上下文分析:")
        report.append(f"  行业背景: {context['industry']['industry']} (置信度: {context['industry']['confidence']:.1%})")
        report.append(f"  紧急程度: {context['urgency']['level']} (置信度: {context['urgency']['confidence']:.1%})")
        report.append(f"  复杂程度: {context['complexity']['level']} (分数: {context['complexity']['score']:.2f})")
        report.append("")
        
        # 用户模式（如果有）
        if classification_result.get('user_pattern'):
            user_pattern = classification_result['user_pattern']
            report.append("👤 用户模式分析:")
            report.append(f"  分析历史请求数: {user_pattern['total_requests_analyzed']}")
            report.append(f"  最常见需求类型: {user_pattern['most_common_type']}")
            report.append("  类型分布:")
            for req_type, count in user_pattern['type_distribution'].items():
                percentage = user_pattern['preferences'][req_type] * 100
                report.append(f"    - {req_type}: {count}次 ({percentage:.1f}%)")
            report.append("")
        
        # 建议
        report.append("💡 建议:")
        primary_type = primary['category']
        
        suggestions = {
            "技术开发": "建议明确技术栈、功能需求和性能指标",
            "内容创作": "建议明确目标受众、核心信息和视觉风格",
            "数据分析": "建议明确数据来源、分析目标和关键指标",
            "业务流程": "建议明确流程步骤、参与角色和业务规则",
            "问题解决": "建议明确问题现象、影响范围和期望解决方案",
            "咨询服务": "建议明确咨询背景、具体需求和约束条件"
        }
        
        report.append(f"  {suggestions.get(primary_type, '建议详细描述具体需求')}")
        
        # 根据紧急程度和复杂度给出额外建议
        if context['urgency']['level'] == '紧急':
            report.append("  ⚠️ 此需求标记为紧急，建议优先处理")
        if context['complexity']['level'] == '复杂':
            report.append("  🔍 此需求复杂度较高，建议分阶段实施")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# 测试函数
def test_classifier():
    """测试分类器"""
    classifier = RequirementClassifier()
    
    test_cases = [
        "请为我设计一个蛋糕促销的海报",
        "开发一个在线商城系统",
        "分析上个月的销售数据并生成报表",
        "优化网站加载速度，现在太慢了",
        "咨询一下应该选择哪个前端框架",
        "设计一个用户注册登录的流程",
        "帮我写一篇关于人工智能的技术文章",
        "排查数据库连接失败的问题"
    ]
    
    print("🧪 分类器测试开始")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {test_case}")
        print("-" * 40)
        
        result = classifier.classify(test_case)
        report = classifier.generate_classification_report(result)
        print(report)
    
    print("\n" + "=" * 60)
    print("✅ 分类器测试完成")


if __name__ == "__main__":
    test_classifier()