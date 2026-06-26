import pandas as pd
import sys
import os

class TestEffortEstimator:
    def __init__(self):
        self.complexity_standards = {
            'simple': {
                'design_range': (0.20, 0.30),
                'first_run_range': (0.15, 0.20),
                'retest_ratio': (0.40, 0.67),
                'regression_ratio': (0.50, 0.67)
            },
            'medium': {
                'design_range': (0.35, 0.40),
                'first_run_range': (0.25, 0.30),
                'retest_ratio': (0.33, 0.40),
                'regression_ratio': (0.48, 0.50)
            },
            'complex': {
                'design_range': (0.50, 0.50),
                'first_run_range': (0.30, 0.40),
                'retest_ratio': (0.33, 0.38),
                'regression_ratio': (0.50, 0.50)
            }
        }
    
    def classify_complexity(self, feature_description):
        keywords_simple = ['列表', '展示', '导航', '跳转', '简单', '修改名称', '保存', '状态显示']
        keywords_complex = ['绑定', '预绑定', '在线', '离线', '批量', '权限', '升级', '重启', '解绑', '强制', '用户管理', '筛选', '详情']
        
        simple_count = sum(1 for keyword in keywords_simple if keyword in feature_description)
        complex_count = sum(1 for keyword in keywords_complex if keyword in feature_description)
        
        if simple_count >= 2 or '简单' in feature_description:
            return 'simple'
        elif complex_count >= 2 or ('绑定' in feature_description and '预绑定' in feature_description) or '批量' in feature_description:
            return 'complex'
        else:
            return 'medium'
    
    def estimate_time(self, complexity, time_type):
        standards = self.complexity_standards[complexity]
        
        if time_type == 'design':
            return standards['design_range'][1]
        elif time_type == 'first_run':
            return standards['first_run_range'][1]
        elif time_type == 'retest':
            return standards['retest_ratio'][1]
        elif time_type == 'regression':
            return standards['regression_ratio'][1]
        else:
            return 0.10
    
    def calculate_times(self, complexity, design_time, first_run_time):
        standards = self.complexity_standards[complexity]
        
        retest_ratio = standards['retest_ratio'][1]
        regression_ratio = standards['regression_ratio'][1]
        
        retest_time = round(first_run_time * retest_ratio, 2)
        regression_time = round(first_run_time * regression_ratio, 2)
        
        retest_time = max(retest_time, 0.10)
        regression_time = max(regression_time, 0.10)
        
        return design_time, first_run_time, retest_time, regression_time
    
    def generate_rationale(self, complexity, design_time, first_run_time, retest_time, regression_time, feature_description):
        standards = self.complexity_standards[complexity]
        
        complexity_desc = {
            'simple': '简单功能：测试入口和点击跳转，操作步骤少，数据准备简单',
            'medium': '中等功能：数据展示和功能跳转，包含多个子功能，需要准备测试数据',
            'complex': '复杂功能：在线/预绑定两种模式，交互流程复杂，需要准备多种测试数据'
        }
        
        retest_ratio = standards['retest_ratio'][1]
        regression_ratio = standards['regression_ratio'][1]
        
        retest_calc = round(first_run_time * retest_ratio, 2)
        regression_calc = round(first_run_time * regression_ratio, 2)
        
        rationale = f"{complexity_desc[complexity]}，用例设计{design_time}，首轮执行{first_run_time}，复测按{int(retest_ratio*100)}%计算{retest_calc}四舍五入{retest_time}，回归按{int(regression_ratio*100)}%计算{regression_calc}"
        
        return rationale
    
    def process_requirements(self, requirements_data):
        results = []
        
        for req in requirements_data:
            title = req.get('title', '')
            story = req.get('story', '')
            
            complexity = self.classify_complexity(story)
            
            design_time = self.estimate_time(complexity, 'design')
            first_run_time = self.estimate_time(complexity, 'first_run')
            
            design_time, first_run_time, retest_time, regression_time = self.calculate_times(
                complexity, design_time, first_run_time
            )
            
            rationale = self.generate_rationale(
                complexity, design_time, first_run_time, 
                retest_time, regression_time, story
            )
            
            results.append({
                '需求标题': title,
                '需求点/故事': story,
                '用例设计时间': design_time,
                '首轮执行时间': first_run_time,
                '复测时间': retest_time,
                '回归时间': regression_time,
                '评估依据': rationale
            })
        
        return results
    
    def export_to_excel(self, results, output_file='测试人力评估.xlsx'):
        df = pd.DataFrame(results)
        df.to_excel(output_file, index=False)
        print(f"Excel文件已生成: {output_file}")
        
        total_design = sum(r['用例设计时间'] for r in results)
        total_first_run = sum(r['首轮执行时间'] for r in results)
        total_retest = sum(r['复测时间'] for r in results)
        total_regression = sum(r['回归时间'] for r in results)
        total = total_design + total_first_run + total_retest + total_regression
        
        print(f"\n总计:")
        print(f"用例设计: {total_design:.2f}人/日")
        print(f"首轮执行: {total_first_run:.2f}人/日")
        print(f"复测: {total_retest:.2f}人/日")
        print(f"回归: {total_regression:.2f}人/日")
        print(f"总计: {total:.2f}人/日")

def main():
    estimator = TestEffortEstimator()
    
    sample_requirements = [
        {
            'title': '网关列表',
            'story': '工作台进入设备--网关，进入网关列表，展示网关icon、状态(在/离线)、名称，卡片点击可以进入网关详情'
        },
        {
            'title': '设备详情',
            'story': '基本信息、关联设备、设备记录、用户管理，信息展示、关联设备的设备卡片也支持点击跳转、设备记录分操作记录和异常记录支持事件类型筛选及时间筛选，用户管理可以编辑用户设备权限'
        },
        {
            'title': '添加设备',
            'story': '区分在线绑定和预绑定，离线设备预绑定，状态为待激活'
        },
        {
            'title': '网关重启',
            'story': '需要等待，观察关联子设备的状态'
        },
        {
            'title': '子设备绑定',
            'story': '在线、离线预绑定'
        },
        {
            'title': '设备名称修改',
            'story': '修改名称保存'
        },
        {
            'title': '解绑+强制解绑',
            'story': '设备解绑和强制解绑功能'
        },
        {
            'title': 'OTA升级',
            'story': '单个设备OTA升级'
        },
        {
            'title': '批量OTA升级',
            'story': '批量OTA升级功能'
        },
        {
            'title': '用户管理',
            'story': '用户管理功能'
        },
        {
            'title': '用户管理-设置权限',
            'story': '用户权限设置功能'
        }
    ]
    
    results = estimator.process_requirements(sample_requirements)
    estimator.export_to_excel(results)

if __name__ == '__main__':
    main()
