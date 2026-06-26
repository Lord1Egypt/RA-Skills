#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一句话出方案 - 方案生成器CLI

根据用户输入的一句话需求，自动识别场景类型，
匹配对应模板，生成结构化的方案Markdown文档。

用法：
    python demo.py "建设智慧城市平台"
    python demo.py "新产品上市方案" --output ./output.md
    python demo.py "技术架构升级" --preview
"""

import argparse
import re
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

# 场景关键词映射表
SCENE_KEYWORDS = {
    'gov': [
        '政务', '服务大厅', '社区', '街道', '居委会', '派出所',
        '局', '委', '办', '政府', '智慧城市', '数字化转型',
        '一网通办', '一窗受理', '最多跑一次', '放管服',
        '公安', '民政', '人社', '城管', '应急', '消防',
        '教育局', '卫生局', '市场监管', '营商环境'
    ],
    'biz': [
        '营销', '推广', '运营', '上市', '融资', '商业化',
        '市场', '品牌', '用户增长', '获客', '转化',
        '产品', '策略', '方案', '活动', '策划',
        '电商', '零售', '销售', '渠道', '客户'
    ],
    'tech': [
        '系统', '平台', '架构', '技术', 'API', '中台',
        '数据', '数据库', '服务器', '云', '部署',
        '开发', '代码', '接口', 'APP', '小程序',
        '智能', 'AI', '人工智能', '算法', '模型'
    ]
}


class ScenarioDetector:
    """场景类型检测器"""
    
    def __init__(self):
        self.keyword_map = SCENE_KEYWORDS
    
    def detect(self, text: str) -> str:
        """
        根据关键词检测场景类型
        
        Args:
            text: 用户输入的文本
            
        Returns:
            场景类型：'gov', 'biz', 'tech' 或 'gov'(默认)
        """
        text_lower = text.lower()
        scores = {}
        
        for scene, keywords in self.keyword_map.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[scene] = score
        
        # 返回得分最高的场景
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        # 默认返回政务场景
        return 'gov'
    
    def get_scene_display_name(self, scene: str) -> str:
        """获取场景的中文显示名称"""
        names = {
            'gov': '🏛️ 政务方案',
            'biz': '💼 商业方案',
            'tech': '💻 技术方案'
        }
        return names.get(scene, '📋 通用方案')


class TemplateFiller:
    """模板填充器"""
    
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            # 默认从当前目录的templates子目录加载
            self.templates_dir = Path(__file__).parent / 'templates'
        else:
            self.templates_dir = Path(templates_dir)
        
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """加载所有模板文件"""
        for scene in ['gov', 'biz', 'tech']:
            template_path = self.templates_dir / f'{scene}.md'
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    self.templates[scene] = f.read()
            else:
                # 模板不存在时使用内置默认模板
                self.templates[scene] = self._get_default_template(scene)
    
    def _get_default_template(self, scene: str) -> str:
        """获取内置默认模板"""
        templates = {
            'gov': DEFAULT_GOV_TEMPLATE,
            'biz': DEFAULT_BIZ_TEMPLATE,
            'tech': DEFAULT_TECH_TEMPLATE
        }
        return templates.get(scene, DEFAULT_GOV_TEMPLATE)
    
    def get_template(self, scene: str) -> str:
        """获取指定场景的模板"""
        return self.templates.get(scene, self.templates['gov'])
    
    def extract_entities(self, text: str) -> Dict[str, str]:
        """
        从用户输入中提取实体信息
        
        Args:
            text: 用户输入的文本
            
        Returns:
            提取的实体字典
        """
        entities = {}
        current_year = datetime.now().year
        
        # 基础信息
        entities['{title}'] = self._extract_title(text)
        entities['{area}'] = self._extract_area(text)
        entities['{product_name}'] = self._extract_product_name(text)
        entities['{system_name}'] = self._extract_system_name(text)
        
        # 时间相关
        entities['{year}'] = str(current_year + 2)  # 默认2年后
        entities['{current_year}'] = str(current_year)
        
        # 政务场景默认值
        entities['{current_share}'] = '45'
        entities['{target_share}'] = '90'
        entities['{current_run}'] = '65'
        entities['{target_run}'] = '95'
        entities['{current_time}'] = '45'
        entities['{improvement}'] = '50'
        entities['{dept_count}'] = '12'
        entities['{online_rate}'] = '95'
        entities['{satisfaction}'] = '92'
        entities['{cost_saving}'] = '30'
        entities['{sensor_count}'] = '5000'
        entities['{current_discovery}'] = '30'
        entities['{target_discovery}'] = '80'
        entities['{leader}'] = '分管副区长'
        entities['{department}'] = '区政数局'
        entities['{total_budget}'] = '1200'
        entities['{phase_count}'] = '3'
        entities['{phase1_budget}'] = '300'
        entities['{phase2_budget}'] = '500'
        entities['{phase3_budget}'] = '400'
        entities['{governance_improvement}'] = '40'
        entities['{time_save}'] = '50'
        entities['{ops_cost_reduction}'] = '25'
        
        # 商业场景默认值
        entities['{market_opportunity}'] = '目标市场呈现快速增长态势，用户需求未被充分满足'
        entities['{pain_point_1}'] = '现有解决方案效率低下'
        entities['{pain_point_2}'] = '用户体验有待提升'
        entities['{pain_point_3}'] = '成本控制压力大'
        entities['{strategy}'] = '多元化发展'
        entities['{target_segment}'] = '中高端'
        entities['{new_users}'] = '10'
        entities['{arr}'] = '500'
        entities['{market_penetration}'] = '5'
        entities['{timeline}'] = '上线后12个月'
        entities['{m3_users}'] = '0.5'
        entities['{m6_users}'] = '3'
        entities['{m12_users}'] = '10'
        entities['{market_position}'] = '高品质、高性价比的差异化定位'
        entities['{diff_1_title}'] = '功能优势'
        entities['{diff_1_desc}'] = '核心功能领先竞品'
        entities['{diff_2_title}'] = '体验优势'
        entities['{diff_2_desc}'] = '用户体验更流畅'
        entities['{diff_3_title}'] = '价格优势'
        entities['{diff_3_desc}'] = '性价比更高'
        entities['{step1}'] = '市场验证'
        entities['{step1_time}'] = '第1-2月'
        entities['{step2}'] = '产品打磨'
        entities['{step2_time}'] = '第3-4月'
        entities['{step3}'] = '规模推广'
        entities['{step3_time}'] = '第5-12月'
        entities['{phase1_time}'] = '第1个月'
        entities['{pm_name}'] = '张经理'
        entities['{phase2_time}'] = '第2-4个月'
        entities['{dev_name}'] = '李工'
        entities['{phase3_time}'] = '第5-6个月'
        entities['{mkt_name}'] = '王总'
        entities['{phase4_time}'] = '第7-12个月'
        entities['{ops_name}'] = '刘总'
        entities['{pm_count}'] = '1'
        entities['{dev_count}'] = '4'
        entities['{mkt_count}'] = '2'
        entities['{ops_count}'] = '2'
        entities['{pm_salary}'] = '2'
        entities['{dev_salary}'] = '2.5'
        entities['{mkt_salary}'] = '1.5'
        entities['{ops_salary}'] = '1.5'
        entities['{months}'] = '6'
        entities['{pm_total}'] = '12'
        entities['{dev_total}'] = '60'
        entities['{mkt_total}'] = '18'
        entities['{ops_total}'] = '18'
        entities['{hr_total}'] = '108'
        entities['{ads_budget}'] = '30'
        entities['{kol_budget}'] = '20'
        entities['{event_budget}'] = '15'
        entities['{content_budget}'] = '10'
        entities['{infra_cost}'] = '5'
        entities['{third_party_cost}'] = '10'
        entities['{misc_cost}'] = '5'
        entities['{north_star_metric}'] = '日活跃用户数(DAU)'
        entities['{north_star_value}'] = '达到5万'
        entities['{metric_1}'] = '次日留存率'
        entities['{metric_1_value}'] = '≥40%'
        entities['{metric_2}'] = '付费转化率'
        entities['{metric_2_value}'] = '≥8%'
        entities['{metric_3}'] = 'NPS评分'
        entities['{metric_3_value}'] = '≥50'
        entities['{warning_1}'] = '30%'
        entities['{warning_2}'] = '5%'
        
        # 技术场景默认值
        entities['{pain_1}'] = '系统响应慢'
        entities['{impact_1}'] = '用户体验差'
        entities['{urgency_1}'] = '高'
        entities['{pain_2}'] = '数据孤岛'
        entities['{impact_2}'] = '效率低'
        entities['{urgency_2}'] = '中'
        entities['{pain_3}'] = '扩展性差'
        entities['{impact_3}'] = '成本高'
        entities['{urgency_3}'] = '低'
        entities['{user_role}'] = '运营人员'
        entities['{user_want}'] = '快速查询数据报表'
        entities['{user_benefit}'] = '提高工作效率'
        entities['{p0_1}'] = '用户登录注册'
        entities['{p0_2}'] = '核心业务功能'
        entities['{p0_3}'] = '数据展示'
        entities['{p1_1}'] = '消息通知'
        entities['{p1_2}'] = '数据导出'
        entities['{p2_1}'] = '主题定制'
        entities['{frontend_tech}'] = 'Vue3 + Element Plus'
        entities['{gateway_tech}'] = 'Kong/Nginx'
        entities['{svc1}'] = '用户服务'
        entities['{svc2}'] = '业务服务'
        entities['{svc3}'] = '数据服务'
        entities['{svc_n}'] = '……'
        entities['{db_tech}'] = 'MySQL'
        entities['{cache_tech}'] = 'Redis'
        entities['{mq_tech}'] = 'RabbitMQ/Kafka'
        entities['{frontend_reason}'] = '生态成熟，学习成本低'
        entities['{backend_tech}'] = 'Spring Boot'
        entities['{backend_reason}'] = '社区活跃，稳定性好'
        entities['{db_reason}'] = '适合OLTP场景'
        entities['{cache_reason}'] = '高性能缓存'
        entities['{mq_reason}'] = '解耦异步通信'
        entities['{container_tech}'] = 'Docker + K8s'
        entities['{container_reason}'] = '容器化部署'
        entities['{cicd_tech}'] = 'Jenkins/GitLab CI'
        entities['{cicd_reason}'] = '自动化构建部署'
        entities['{ha_1}'] = '多副本部署'
        entities['{ha_2}'] = '自动故障转移'
        entities['{ha_3}'] = '熔断降级'
        entities['{module_1}'] = '用户模块'
        entities['{module_1_features}'] = '注册、登录、权限'
        entities['{module_1_priority}'] = '0'
        entities['{module_1_effort}'] = '20'
        entities['{module_1_desc}'] = '提供用户全生命周期管理'
        entities['{module_2}'] = '业务模块'
        entities['{module_2_features}'] = '核心业务逻辑'
        entities['{module_2_priority}'] = '0'
        entities['{module_2_effort}'] = '50'
        entities['{module_2_desc}'] = '实现核心业务功能'
        entities['{module_3}'] = '数据模块'
        entities['{module_3_features}'] = '数据采集、分析、报表'
        entities['{module_3_priority}'] = '1'
        entities['{module_3_effort}'] = '30'
        entities['{module_3_desc}'] = '提供数据分析能力'
        entities['{module_4}'] = '系统模块'
        entities['{module_4_features}'] = '配置、监控、日志'
        entities['{module_4_priority}'] = '1'
        entities['{module_4_effort}'] = '15'
        entities['{total_effort}'] = '115'
        entities['{phase1_time}'] = '2周'
        entities['{phase2_time}'] = '1周'
        entities['{phase3_time}'] = '6周'
        entities['{phase4_time}'] = '2周'
        entities['{phase5_time}'] = '1周'
        entities['{risk_1}'] = '技术难度超预期'
        entities['{risk_1_prob}'] = '中'
        entities['{risk_1_impact}'] = '中'
        entities['{risk_1_mitigation}'] = '预留buffer，增加专家评审'
        entities['{risk_2}'] = '需求变更频繁'
        entities['{risk_2_prob}'] = '高'
        entities['{risk_2_impact}'] = '高'
        entities['{risk_2_mitigation}'] = '敏捷迭代，控制变更'
        entities['{risk_3}'] = '人员流动'
        entities['{risk_3_prob}'] = '低'
        entities['{risk_3_impact}'] = '中'
        entities['{risk_3_mitigation}'] = '文档沉淀，知识共享'
        entities['{pm_count}'] = '1'
        entities['{pm_months}'] = '3'
        entities['{pm_rate}'] = '2'
        entities['{pm_cost}'] = '6'
        entities['{techlead_count}'] = '1'
        entities['{techlead_months}'] = '3'
        entities['{techlead_rate}'] = '3'
        entities['{techlead_cost}'] = '9'
        entities['{backend_count}'] = '3'
        entities['{backend_months}'] = '3'
        entities['{backend_rate}'] = '2.5'
        entities['{backend_cost}'] = '22.5'
        entities['{frontend_count}'] = '2'
        entities['{frontend_months}'] = '2'
        entities['{frontend_rate}'] = '2'
        entities['{frontend_cost}'] = '8'
        entities['{qa_count}'] = '2'
        entities['{qa_months}'] = '2'
        entities['{qa_rate}'] = '1.5'
        entities['{qa_cost}'] = '6'
        entities['{hr_total}'] = '51.5'
        entities['{server_spec}'] = '8核16G'
        entities['{server_count}'] = '4'
        entities['{server_price}'] = '2000'
        entities['{server_cost}'] = '8000'
        entities['{db_spec}'] = '16核32G'
        entities['{db_count}'] = '2'
        entities['{db_price}'] = '5000'
        entities['{db_cost}'] = '10000'
        entities['{bandwidth}'] = '100'
        entities['{bandwidth_count}'] = '1'
        entities['{bandwidth_price}'] = '5000'
        entities['{bandwidth_cost}'] = '5000'
        entities['{third_party}'] = '短信/推送等'
        entities['{third_party_cost}'] = '3000'
        entities['{infra_year_cost}'] = '27.6'
        entities['{third_party_year_cost}'] = '3.6'
        entities['{misc_cost}'] = '2'
        entities['{total_cost}'] = '84.7'
        
        return entities
    
    def _extract_title(self, text: str) -> str:
        """提取方案标题"""
        # 移除常见前缀和后缀
        text = re.sub(r'^(帮我)?(写|做|搞|出)(一个?|份)?', '', text)
        text = re.sub(r'(方案|计划|思路)$', '', text)
        text = text.strip() or '通用'
        # 返回干净的中文标题
        return text
    
    def _extract_area(self, text: str) -> str:
        """提取区域名称"""
        # 简单匹配XX区/县/市
        match = re.search(r'([\u4e00-\u9fa5]{2,6}(?:区|县|市))', text)
        return match.group(1) if match else '本区'
    
    def _extract_product_name(self, text: str) -> str:
        """提取产品名称（保留，用作title）"""
        return self._extract_title(text)
    
    def _extract_system_name(self, text: str) -> str:
        """提取系统名称（保留，用作title）"""
        return self._extract_title(text)
    
    def fill(self, template: str, entities: Dict[str, str]) -> str:
        """
        填充模板
        
        Args:
            template: 模板字符串
            entities: 实体字典
            
        Returns:
            填充后的文本
        """
        result = template
        for key, value in entities.items():
            result = result.replace(key, value)
        
        # 清理未替换的占位符
        result = re.sub(r'\{[^}]+\}', '', result)
        
        # 清理多余的空行
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result


class SchemeGenerator:
    """方案生成器主类"""
    
    def __init__(self, templates_dir: str = None):
        self.detector = ScenarioDetector()
        self.filler = TemplateFiller(templates_dir)
    
    def generate(self, requirement: str, output_path: str = None, preview: bool = False) -> str:
        """
        根据需求生成方案
        
        Args:
            requirement: 用户输入的一句话需求
            output_path: 输出文件路径，None则不保存
            preview: 是否仅预览模式
            
        Returns:
            生成的方案文档
        """
        # 1. 检测场景类型
        scene = self.detector.detect(requirement)
        scene_display = self.detector.get_scene_display_name(scene)
        
        print(f"🔍 检测到场景: {scene_display}")
        
        # 2. 获取模板
        template = self.filler.get_template(scene)
        
        # 3. 提取实体
        entities = self.filler.extract_entities(requirement)
        
        # 4. 填充模板
        document = self.filler.fill(template, entities)
        
        # 5. 添加元信息
        header = f"> 由 [一句话出方案] CLI 生成 | 场景: {scene_display} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        document = header + document
        
        # 6. 输出
        if preview:
            print("\n" + "="*60)
            print("📋 方案预览")
            print("="*60 + "\n")
        
        print(document)
        
        if preview:
            print("\n" + "="*60)
        
        # 7. 保存文件
        if output_path and not preview:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(document)
            print(f"\n✅ 方案已保存至: {output_file.absolute()}")
        
        return document


# 内置默认模板（当模板文件不存在时使用）

DEFAULT_GOV_TEMPLATE = """# 【{title}智慧城市平台建设方案】

## 一、背景

根据《"十四五"数字政府建设规划》和省、市关于加快推进新型智慧城市建设的工作部署，当前{area}存在"数据孤岛"、服务响应慢、群众办事跑腿多等问题。为提升治理效能和群众获得感，拟建设统一智慧城市平台，实现"一网统管、一网通办"。

### 现状分析
- **数据分散**：各部门系统独立运行，数据标准不统一，共享困难
- **服务割裂**：群众办事需跑多个部门，流程繁琐，体验差
- **响应滞后**：问题发现依赖人工上报，缺乏主动预警能力

## 二、目标

到{year}年底，实现以下目标：

| 指标 | 当前值 | 目标值 |
|-----|-------|-------|
| 平台覆盖率 | - | 100% |
| 跨部门数据共享率 | {current_share}% | {target_share}% |
| "最多跑一次"比例 | {current_run}% | {target_run}% |
| 平均办事时长 | {current_time}分钟 | 缩短{improvement}% |

## 三、重点任务

### （一）建设城市运行管理中心
- **措施**：整合{dept_count}个部门数据，建立统一指挥调度平台
- **预期**：实现城市事件发现-派发-处置闭环，响应时长缩短60%

### （二）打造"一网通办"服务端
- **措施**：升级区级政务服务平台，新增AI智能客服和自动审批功能
- **预期**：高频事项网办率达到{online_rate}%，群众满意度提升至{satisfaction}分

### （三）构建数据中台
- **措施**：打通水电气、交通、舆情等公共数据，建立标准化的数据治理体系
- **预期**：数据共享时效从T+1提升至实时，节约数据对接成本{cost_saving}%

### （四）部署智能感知网络
- **措施**：在重点区域布设{sensor_count}个物联网传感器，实现环境、设施实时监测
- **预期**：问题主动发现率从{current_discovery}%提升至{target_discovery}%

## 四、保障措施

### 组织保障
成立智慧城市建设领导小组，{leader}任组长，{department}牵头实施，各部门明确联络员。

### 资金保障
总投资{total_budget}万元，分{phase_count}期建设：
- 一期：{phase1_budget}万元（基础设施）
- 二期：{phase2_budget}万元（平台开发）
- 三期：{phase3_budget}万元（智能应用）

### 考核机制
纳入部门绩效考核，实行季度通报、年度评估，与绩效奖金挂钩。

## 五、预期成效

### 直接成效
- 城市治理效率提升{governance_improvement}%
- 群众办事时间节省{time_save}%
- 数据运维成本降低{ops_cost_reduction}%

### 间接效益
- 为数字经济发展奠定数据基础
- 吸引优质企业入驻
- 推动产业升级，提升区域竞争力
"""

DEFAULT_BIZ_TEMPLATE = """# 【{product_name}产品上市方案】

## 一、项目背景

### 市场机会
{market_opportunity}

### 用户痛点
- **痛点1**：{pain_point_1}
- **痛点2**：{pain_point_2}
- **痛点3**：{pain_point_3}

### 战略匹配度
本产品契合公司"{strategy}"战略，有助于拓展{target_segment}市场，完善产品矩阵。

## 二、核心目标

采用SMART原则设定目标：

| 维度 | 指标 | 数值 |
|-----|------|------|
| 用户获取 | 新增用户数 | {new_users}万 |
| 收入 | ARR（年度经常性收入） | {arr}万元 |
| 市场份额 | 目标市场渗透率 | {market_penetration}% |
| 时间 | 达成周期 | {timeline} |

**阶段性目标**：
- M3（第一阶段）：完成MVP发布，获取{m3_users}万种子用户
- M6（第二阶段）：达到{m6_users}万用户，验证PMF
- M12（第三阶段）：实现{m12_users}万用户，商业模式跑通

## 三、核心策略

### 市场定位
{market_position}

### 差异化优势
1. **{diff_1_title}**：{diff_1_desc}
2. **{diff_2_title}**：{diff_2_desc}
3. **{diff_3_title}**：{diff_3_desc}

### 切入路径
```
第1步：{step1}（{step1_time}）
    ↓
第2步：{step2}（{step2_time}）
    ↓
第3步：{step3}（{step3_time}）
```

## 四、执行计划

### 里程碑计划

| 阶段 | 时间 | 关键交付物 | 责任人 |
|-----|------|-----------|--------|
| 准备期 | {phase1_time} | 市场调研、需求确认、产品设计 | {pm_name} |
| 开发期 | {phase2_time} | MVP开发、内测、Bug修复 | {dev_name} |
| 上市期 | {phase3_time} | 公测、正式发布、KOL合作 | {mkt_name} |
| 成长期 | {phase4_time} | 迭代优化、用户运营、收入增长 | {ops_name} |

### 资源投入
- 产品团队：{pm_count}人
- 开发团队：{dev_count}人
- 市场团队：{mkt_count}人
- 运营团队：{ops_count}人

## 五、资源需求

### 预算汇总
| 类别 | 金额 |
|-----|------|
| 人力成本 | {hr_total}万元 |
| 市场推广 | {ads_budget}万元 |
| 基础设施 | {infra_cost}万元/年 |
| 其他杂费 | {misc_cost}万元 |
| **合计** | **{total_budget}万元** |

## 六、成功指标

### 北极星指标
**{north_star_metric}**：{north_star_value}

### 辅助指标
| 指标 | 目标值 |
|-----|-------|
| {metric_1} | {metric_1_value} |
| {metric_2} | {metric_2_value} |
| {metric_3} | {metric_3_value} |
"""

DEFAULT_TECH_TEMPLATE = """# 【{system_name}系统/平台建设方案】

## 一、需求分析

### 现状痛点
| 痛点 | 影响 | 紧急度 |
|-----|------|-------|
| {pain_1} | {impact_1} | {urgency_1} |
| {pain_2} | {impact_2} | {urgency_2} |
| {pain_3} | {impact_3} | {urgency_3} |

### 用户故事
```
作为 {user_role}
我想要 {user_want}
以便 {user_benefit}
```

### 功能需求
**P0（必须）**：
1. {p0_1}
2. {p0_2}
3. {p0_3}

**P1（重要）**：
1. {p1_1}
2. {p1_2}

**P2（优化）**：
1. {p2_1}

## 二、技术选型

### 架构设计
```
┌─────────────────────────────────────────────┐
│                   前端层                     │
│  {frontend_tech}                            │
├─────────────────────────────────────────────┤
│                   API网关                    │
│  {gateway_tech}                             │
├──────────┬──────────┬──────────┬────────────┤
│  服务1   │  服务2   │  服务3   │  服务N     │
│ {svc1}   │ {svc2}   │ {svc3}   │ {svc_n}    │
├──────────┴──────────┴──────────┴────────────┤
│                   数据层                    │
│  {db_tech} + {cache_tech} + {mq_tech}       │
└─────────────────────────────────────────────┘
```

### 技术栈选型

| 层级 | 技术方案 | 选型理由 |
|-----|---------|---------|
| 前端 | {frontend_tech} | {frontend_reason} |
| 后端 | {backend_tech} | {backend_reason} |
| 数据库 | {db_tech} | {db_reason} |
| 缓存 | {cache_tech} | {cache_reason} |
| 消息队列 | {mq_tech} | {mq_reason} |
| 容器化 | {container_tech} | {container_reason} |

### 高可用设计
- {ha_1}
- {ha_2}
- {ha_3}

## 三、建设内容

### 功能模块分解

| 模块 | 功能点 | 优先级 | 工作量 |
|-----|-------|-------|-------|
| {module_1} | {module_1_features} | P{module_1_priority} | {module_1_effort}人天 |
| {module_2} | {module_2_features} | P{module_2_priority} | {module_2_effort}人天 |
| {module_3} | {module_3_features} | P{module_3_priority} | {module_3_effort}人天 |
| {module_4} | {module_4_features} | P{module_4_priority} | {module_4_effort}人天 |

**总工作量**：约{total_effort}人天

## 四、实施路径

| 阶段 | 时间 | 里程碑 |
|-----|------|-------|
| 需求分析 | {phase1_time} | 需求评审通过 |
| 架构设计 | {phase2_time} | 架构评审通过 |
| 迭代开发 | {phase3_time} | 测试通过 |
| 集成测试 | {phase4_time} | 全量测试通过 |
| 上线部署 | {phase5_time} | 生产环境可用 |

## 五、风险与对策

| 风险 | 概率 | 影响 | 对策 |
|-----|------|------|------|
| {risk_1} | {risk_1_prob} | {risk_1_impact} | {risk_1_mitigation} |
| {risk_2} | {risk_2_prob} | {risk_2_impact} | {risk_2_mitigation} |
| {risk_3} | {risk_3_prob} | {risk_3_impact} | {risk_3_mitigation} |

## 六、资源评估

### 人力成本
| 角色 | 人数 | 周期 | 单价 | 小计 |
|-----|------|------|------|------|
| 项目经理 | {pm_count} | {pm_months}月 | {pm_rate}万/月 | {pm_cost}万 |
| 技术经理 | {techlead_count} | {techlead_months}月 | {techlead_rate}万/月 | {techlead_cost}万 |
| 后端开发 | {backend_count} | {backend_months}月 | {backend_rate}万/月 | {backend_cost}万 |
| 前端开发 | {frontend_count} | {frontend_months}月 | {frontend_rate}万/月 | {frontend_cost}万 |
| 测试工程师 | {qa_count} | {qa_months}月 | {qa_rate}万/月 | {qa_cost}万 |

**人力成本合计**：{hr_total}万元

### 年度总成本
| 成本项 | 金额 |
|-------|------|
| 人力成本 | {hr_total}万元 |
| 基础设施 | {infra_year_cost}万元 |
| 第三方服务 | {third_party_year_cost}万元 |
| 其他杂费 | {misc_cost}万元 |
| **合计** | **{total_cost}万元/年** |
"""


def main():
    """CLI入口函数"""
    parser = argparse.ArgumentParser(
        prog='一句话出方案',
        description='根据一句话需求，自动生成完整方案文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  %(prog)s "建设智慧城市平台"
  %(prog)s "新产品上市方案" --output ./output.md
  %(prog)s "技术架构升级" --preview

场景自动识别：
  - 包含"政务、服务大厅、街道、局委办"等 → 政务方案
  - 包含"营销、推广、运营、上市"等 → 商业方案
  - 包含"系统、平台、架构、技术"等 → 技术方案
        """
    )
    
    parser.add_argument(
        'requirement',
        nargs='?',
        help='一句话需求描述，如：建设智慧城市平台'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径（默认输出到stdout）'
    )
    
    parser.add_argument(
        '-p', '--preview',
        action='store_true',
        help='预览模式：只显示不保存'
    )
    
    parser.add_argument(
        '-t', '--templates',
        help='模板目录路径（默认使用内置模板）'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s v1.1.0'
    )
    
    args = parser.parse_args()
    
    # 如果没有输入需求，显示帮助并退出
    if not args.requirement:
        parser.print_help()
        print("\n💡 或者直接输入需求：")
        print("  python demo.py \"建设智慧城市平台\"")
        sys.exit(0)
    
    # 验证输入
    if len(args.requirement.strip()) < 2:
        print("❌ 需求描述太短了，请提供更具体的信息", file=sys.stderr)
        sys.exit(1)
    
    try:
        # 创建生成器
        generator = SchemeGenerator(templates_dir=args.templates)
        
        # 生成方案
        generator.generate(
            requirement=args.requirement,
            output_path=args.output,
            preview=args.preview
        )
        
    except FileNotFoundError as e:
        print(f"❌ 模板文件未找到: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
