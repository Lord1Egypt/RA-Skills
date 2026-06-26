#!/usr/bin/env python3
"""
彩票预测自动进化系统
基于实际开奖结果持续优化预测模型

⚠️ 免责声明：彩票是独立随机事件，进化系统仅优化统计方法，不能保证预测准确率
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class LotteryEvolution:
    """彩票预测模型自动进化系统"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        else:
            self.data_dir = data_dir
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 进化配置文件
        self.config_file = os.path.join(self.data_dir, 'evolution_config.json')
        self.history_file = os.path.join(self.data_dir, 'prediction_history.json')
        
        # 加载配置
        self.config = self._load_config()
        self.history = self._load_history()
    
    def _load_config(self) -> Dict:
        """加载进化配置"""
        default_config = {
            'version': '1.0.0',
            'last_updated': datetime.now().isoformat(),
            'lottery_types': {
                'pl3': {
                    'hot_weight': 0.6,      # 热号选择权重
                    'cold_weight': 0.1,     # 冷号选择权重
                    'warm_weight': 0.3,     # 温号选择权重
                    'missing_threshold': 2.0, # 遗漏值阈值
                    'position_weight': 0.7,   # 定位分析权重
                    'sum_weight': 0.3,        # 和值分析权重
                    'performance': {
                        'total_predictions': 0,
                        'exact_matches': 0,    # 直选命中
                        'group_matches': 0,    # 组选命中
                        'digit_matches': 0     # 位数命中
                    }
                },
                'pl5': {
                    'hot_weight': 0.6,
                    'cold_weight': 0.1,
                    'warm_weight': 0.3,
                    'missing_threshold': 2.0,
                    'performance': {
                        'total_predictions': 0,
                        'exact_matches': 0,
                        'digit_matches': 0
                    }
                },
                'dlt': {
                    'hot_weight': 0.6,
                    'cold_weight': 0.15,
                    'warm_weight': 0.25,
                    'zone_balance_weight': 0.3,  # 区间平衡权重
                    'odd_even_weight': 0.2,      # 奇偶比权重
                    'performance': {
                        'total_predictions': 0,
                        'front_5_hits': 0,    # 前区全中
                        'front_4_hits': 0,    # 前区4中
                        'front_3_hits': 0,    # 前区3中
                        'back_2_hits': 0,     # 后区全中
                        'back_1_hits': 0      # 后区1中
                    }
                },
                'ssq': {
                    'hot_weight': 0.6,
                    'cold_weight': 0.15,
                    'warm_weight': 0.25,
                    'zone_balance_weight': 0.3,
                    'performance': {
                        'total_predictions': 0,
                        'red_6_hits': 0,
                        'red_5_hits': 0,
                        'red_4_hits': 0,
                        'blue_hits': 0
                    }
                },
                'qxc': {
                    'hot_weight': 0.6,
                    'cold_weight': 0.1,
                    'warm_weight': 0.3,
                    'performance': {
                        'total_predictions': 0,
                        'exact_matches': 0,
                        'digit_matches': 0
                    }
                },
                'zc14': {
                    'odds_weight': 0.5,       # 赔率权重
                    'form_weight': 0.3,       # 战绩权重
                    'home_advantage': 0.2,    # 主场优势
                    'performance': {
                        'total_predictions': 0,
                        'exact_14_hits': 0,   # 14场全中
                        '13_hits': 0,
                        '12_hits': 0,
                        'avg_correct': 0      # 平均正确场数
                    }
                }
            },
            'evolution_rules': {
                'adjustment_rate': 0.05,      # 每次调整幅度
                'min_weight': 0.05,           # 最小权重
                'max_weight': 0.9,            # 最大权重
                'window_size': 20,            # 评估窗口大小
                'improvement_threshold': 0.02 # 改进阈值
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # 合并默认配置和加载的配置
                    self._merge_config(default_config, loaded)
                    return loaded
            except:
                pass
        
        return default_config
    
    def _merge_config(self, default: Dict, loaded: Dict):
        """合并配置，确保新字段存在"""
        for key, value in default.items():
            if key not in loaded:
                loaded[key] = value
            elif isinstance(value, dict) and isinstance(loaded.get(key), dict):
                self._merge_config(value, loaded[key])
    
    def _load_history(self) -> List[Dict]:
        """加载预测历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_config(self):
        """保存配置"""
        self.config['last_updated'] = datetime.now().isoformat()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def save_history(self):
        """保存历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def record_prediction(self, lottery_type: str, prediction: List, 
                         actual: List = None, date: str = None):
        """
        记录一次预测
        
        Args:
            lottery_type: 彩票类型
            prediction: 推荐的号码
            actual: 实际开奖号码（如有）
            date: 日期
        """
        record = {
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'lottery_type': lottery_type,
            'prediction': prediction,
            'actual': actual,
            'timestamp': datetime.now().isoformat()
        }
        
        self.history.append(record)
        
        # 只保留最近200条记录
        if len(self.history) > 200:
            self.history = self.history[-200:]
        
        self.save_history()
        
        # 如果有实际开奖结果，评估并进化
        if actual:
            self.evaluate_and_evolve(lottery_type, prediction, actual)
    
    def evaluate_and_evolve(self, lottery_type: str, prediction: List, actual: List):
        """
        评估预测结果并进化模型
        
        Args:
            lottery_type: 彩票类型
            prediction: 预测号码
            actual: 实际开奖号码
        """
        lt_config = self.config['lottery_types'].get(lottery_type)
        if not lt_config:
            return
        
        # 计算命中情况
        hits = self._calculate_hits(lottery_type, prediction, actual)
        
        # 更新性能统计
        perf = lt_config['performance']
        perf['total_predictions'] = perf.get('total_predictions', 0) + 1
        
        for key, value in hits.items():
            if key in perf:
                perf[key] = perf.get(key, 0) + value
        
        # 触发进化
        self._evolve_model(lottery_type, hits)
        
        # 保存配置
        self.save_config()
    
    def _calculate_hits(self, lottery_type: str, prediction: List, actual: List) -> Dict:
        """计算命中情况"""
        hits = {}
        
        if lottery_type in ['pl3', 'pl5', 'qxc']:
            # 数字型彩票
            exact_match = prediction == actual
            digit_matches = sum(1 for p, a in zip(prediction, actual) if p == a)
            
            hits['exact_matches'] = 1 if exact_match else 0
            hits['digit_matches'] = digit_matches
            
            # 排列三组选
            if lottery_type == 'pl3':
                hits['group_matches'] = 1 if sorted(prediction) == sorted(actual) else 0
        
        elif lottery_type == 'dlt':
            # 大乐透
            pred_front = set(prediction['front'])
            pred_back = set(prediction['back'])
            actual_front = set(actual['front'])
            actual_back = set(actual['back'])
            
            front_hits = len(pred_front & actual_front)
            back_hits = len(pred_back & actual_back)
            
            hits['front_5_hits'] = 1 if front_hits == 5 else 0
            hits['front_4_hits'] = 1 if front_hits == 4 else 0
            hits['front_3_hits'] = 1 if front_hits == 3 else 0
            hits['back_2_hits'] = 1 if back_hits == 2 else 0
            hits['back_1_hits'] = 1 if back_hits == 1 else 0
        
        elif lottery_type == 'ssq':
            # 双色球
            pred_red = set(prediction['red'])
            pred_blue = prediction['blue']
            actual_red = set(actual['red'])
            actual_blue = actual['blue']
            
            red_hits = len(pred_red & actual_red)
            blue_hit = 1 if pred_blue == actual_blue else 0
            
            hits['red_6_hits'] = 1 if red_hits == 6 else 0
            hits['red_5_hits'] = 1 if red_hits == 5 else 0
            hits['red_4_hits'] = 1 if red_hits == 4 else 0
            hits['blue_hits'] = blue_hit
        
        elif lottery_type == 'zc14':
            # 足彩14场
            correct = sum(1 for p, a in zip(prediction, actual) if p == a)
            hits['exact_14_hits'] = 1 if correct == 14 else 0
            hits['13_hits'] = 1 if correct == 13 else 0
            hits['12_hits'] = 1 if correct == 12 else 0
            
            # 更新平均正确场数
            perf = self.config['lottery_types']['zc14']['performance']
            total = perf.get('total_predictions', 1)
            current_avg = perf.get('avg_correct', 0)
            hits['avg_correct'] = (current_avg * (total - 1) + correct) / total
        
        return hits
    
    def _evolve_model(self, lottery_type: str, hits: Dict):
        """
        根据命中情况进化模型参数
        
        进化策略：
        1. 如果热号策略效果好，增加热号权重
        2. 如果遗漏值策略效果好，调整遗漏阈值
        3. 如果定位分析效果好，增加定位权重
        """
        lt_config = self.config['lottery_types'][lottery_type]
        rules = self.config['evolution_rules']
        adjustment = rules['adjustment_rate']
        
        perf = lt_config['performance']
        total = perf.get('total_predictions', 1)
        
        # 计算近期表现（最近20期）
        recent_history = [h for h in self.history 
                         if h['lottery_type'] == lottery_type 
                         and h.get('actual')][-20:]
        
        if len(recent_history) < 5:
            return  # 数据不足，不进化
        
        # 计算命中率趋势
        recent_exact = sum(1 for h in recent_history 
                          if self._is_exact_match(lottery_type, h['prediction'], h['actual']))
        recent_rate = recent_exact / len(recent_history)
        
        # 整体命中率
        overall_exact = perf.get('exact_matches', 0)
        overall_rate = overall_exact / total if total > 0 else 0
        
        # 如果近期表现比整体好，微调参数向近期策略靠拢
        if recent_rate > overall_rate + rules['improvement_threshold']:
            # 增加热号权重（假设近期热号策略效果好）
            lt_config['hot_weight'] = min(rules['max_weight'], 
                                         lt_config['hot_weight'] + adjustment)
            lt_config['cold_weight'] = max(rules['min_weight'],
                                          lt_config['cold_weight'] - adjustment / 2)
        
        # 如果命中率低，尝试增加冷号权重（博冷策略）
        elif recent_rate < overall_rate - rules['improvement_threshold']:
            lt_config['cold_weight'] = min(0.3, lt_config['cold_weight'] + adjustment)
            lt_config['hot_weight'] = max(rules['min_weight'],
                                         lt_config['hot_weight'] - adjustment / 2)
    
    def _is_exact_match(self, lottery_type: str, prediction, actual) -> bool:
        """判断是否完全命中"""
        if lottery_type in ['pl3', 'pl5', 'qxc']:
            return prediction == actual
        elif lottery_type in ['dlt', 'ssq']:
            return (prediction.get('front') == actual.get('front') and
                   prediction.get('back') == actual.get('back'))
        return False
    
    def get_optimized_weights(self, lottery_type: str) -> Dict:
        """
        获取优化后的权重参数
        
        Returns:
            当前最优权重配置
        """
        lt_config = self.config['lottery_types'].get(lottery_type, {})
        
        return {
            'hot_weight': lt_config.get('hot_weight', 0.6),
            'cold_weight': lt_config.get('cold_weight', 0.1),
            'warm_weight': lt_config.get('warm_weight', 0.3),
            'missing_threshold': lt_config.get('missing_threshold', 2.0),
            'zone_balance_weight': lt_config.get('zone_balance_weight', 0.3),
            'odd_even_weight': lt_config.get('odd_even_weight', 0.2)
        }
    
    def generate_evolution_report(self, lottery_type: str = None) -> str:
        """
        生成进化报告
        
        Args:
            lottery_type: 指定彩票类型，None则生成所有类型报告
            
        Returns:
            报告文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append("🧬 彩票预测模型自动进化报告")
        lines.append("=" * 60)
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        types_to_report = [lottery_type] if lottery_type else list(self.config['lottery_types'].keys())
        
        for lt in types_to_report:
            lt_config = self.config['lottery_types'].get(lt)
            if not lt_config:
                continue
            
            perf = lt_config.get('performance', {})
            total = perf.get('total_predictions', 0)
            
            if total == 0:
                continue
            
            lines.append(f"\n📊 {self._get_lottery_name(lt)}")
            lines.append("-" * 40)
            
            # 当前权重
            lines.append(f"\n🎚️  当前优化权重:")
            lines.append(f"   热号权重: {lt_config.get('hot_weight', 0.6):.2f}")
            lines.append(f"   冷号权重: {lt_config.get('cold_weight', 0.1):.2f}")
            lines.append(f"   温号权重: {lt_config.get('warm_weight', 0.3):.2f}")
            
            if 'missing_threshold' in lt_config:
                lines.append(f"   遗漏阈值: {lt_config['missing_threshold']:.2f}")
            
            # 性能统计
            lines.append(f"\n📈 性能统计:")
            lines.append(f"   总预测次数: {total}")
            
            if 'exact_matches' in perf:
                rate = perf['exact_matches'] / total * 100
                lines.append(f"   直选命中: {perf['exact_matches']} 次 ({rate:.2f}%)")
            
            if 'group_matches' in perf:
                rate = perf['group_matches'] / total * 100
                lines.append(f"   组选命中: {perf['group_matches']} 次 ({rate:.2f}%)")
            
            if 'digit_matches' in perf:
                avg_digits = perf['digit_matches'] / total
                lines.append(f"   平均位数命中: {avg_digits:.2f}")
            
            if 'front_5_hits' in perf:
                lines.append(f"   前区5中: {perf['front_5_hits']} 次")
                lines.append(f"   后区2中: {perf['back_2_hits']} 次")
            
            if 'avg_correct' in perf:
                lines.append(f"   平均正确场数: {perf['avg_correct']:.2f}/14")
        
        lines.append("\n" + "=" * 60)
        lines.append("⚠️  注意: 以上数据仅反映历史表现，不能预测未来结果")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _get_lottery_name(self, code: str) -> str:
        """获取彩票名称"""
        names = {
            'pl3': '排列三',
            'pl5': '排列五',
            'dlt': '大乐透',
            'ssq': '双色球',
            'qxc': '七星彩',
            'zc14': '足彩14场'
        }
        return names.get(code, code)


# ==================== CLI 入口 ====================

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='彩票预测自动进化系统')
    parser.add_argument('--report', action='store_true', help='生成进化报告')
    parser.add_argument('--type', type=str, choices=['pl3', 'pl5', 'dlt', 'ssq', 'qxc', 'zc14'],
                       help='指定彩票类型')
    parser.add_argument('--record', action='store_true', help='记录一次预测')
    parser.add_argument('--prediction', type=str, help='预测号码 (JSON格式)')
    parser.add_argument('--actual', type=str, help='实际开奖号码 (JSON格式)')
    
    args = parser.parse_args()
    
    evolution = LotteryEvolution()
    
    if args.report:
        report = evolution.generate_evolution_report(args.type)
        print(report)
    
    elif args.record and args.prediction:
        import json as json_mod
        prediction = json_mod.loads(args.prediction)
        actual = json_mod.loads(args.actual) if args.actual else None
        
        evolution.record_prediction(args.type, prediction, actual)
        print(f"✅ 已记录 {args.type} 的预测")
        
        if actual:
            print("🧬 已触发模型进化")
    
    else:
        print("=" * 60)
        print("🧬 彩票预测自动进化系统")
        print("=" * 60)
        print("\n用法:")
        print("  python3 lottery_evolution.py --report")
        print("  python3 lottery_evolution.py --report --type pl3")
        print("  python3 lottery_evolution.py --record --type pl3 \\")
        print("      --prediction '[4,5,6]' --actual '[4,5,9]'")
        print("\n功能:")
        print("  • 记录每次预测和实际开奖")
        print("  • 自动分析命中情况")
        print("  • 动态调整模型权重")
        print("  • 生成进化报告")
        print("\n⚠️  彩票是随机事件，进化仅优化统计方法")
        print("=" * 60)


if __name__ == '__main__':
    main()
