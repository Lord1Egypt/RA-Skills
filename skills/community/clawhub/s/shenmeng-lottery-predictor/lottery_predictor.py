#!/usr/bin/env python3
"""
彩票预测分析工具 - 核心模块
支持：排列三、排列五、大乐透、双色球、七星彩、足彩14场

⚠️ 免责声明：本工具仅供娱乐学习，不构成投注建议
彩票开奖是独立随机事件，历史数据不具备预测能力
"""

import json
import random
from collections import Counter
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import os


class LotteryPredictor:
    """彩票预测分析器"""
    
    def __init__(self, data_dir: str = None):
        """
        初始化预测器
        
        Args:
            data_dir: 数据文件目录，默认为当前目录下的data文件夹
        """
        if data_dir is None:
            self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        else:
            self.data_dir = data_dir
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 缓存数据
        self._cache = {}
    
    # ==================== 排列三 ====================
    
    def analyze_pl3(self, history_data: List[List[int]] = None) -> Dict:
        """
        分析排列三
        
        Args:
            history_data: 历史开奖数据，每个元素是3个数字的列表
            
        Returns:
            分析结果字典
        """
        if history_data is None:
            history_data = self._load_mock_data('pl3')
        
        # 统计各位数字频率
        positions = [[], [], []]  # 百位、十位、个位
        for draw in history_data:
            for i, num in enumerate(draw):
                positions[i].append(num)
        
        # 冷热号分析
        all_numbers = [n for draw in history_data for n in draw]
        hot_cold = self._calc_hot_cold(all_numbers, 0, 9)
        
        # 各位冷热号
        pos_analysis = []
        for i, pos_nums in enumerate(positions):
            pos_hot_cold = self._calc_hot_cold(pos_nums, 0, 9)
            pos_analysis.append({
                'position': ['百位', '十位', '个位'][i],
                'hot': pos_hot_cold['hot'],
                'cold': pos_hot_cold['cold'],
                'missing': self._calc_missing(pos_nums, 0, 9, 30)
            })
        
        # 和值分析
        sums = [sum(draw) for draw in history_data]
        sum_analysis = {
            'recent_avg': sum(sums[-10:]) / 10,
            'recent_range': (min(sums[-10:]), max(sums[-10:])),
            'theoretical_avg': 13.5,  # (0+9)/2 * 3 = 13.5
            'trend': 'up' if sums[-1] > sum(sums[-5:]) / 5 else 'down'
        }
        
        # 生成推荐
        recommendation = self._generate_pl3_recommendation(pos_analysis, hot_cold)
        
        return {
            'lottery_type': '排列三',
            'hot_numbers': hot_cold['hot'],
            'cold_numbers': hot_cold['cold'],
            'position_analysis': pos_analysis,
            'sum_analysis': sum_analysis,
            'recommendation': recommendation,
            'disclaimer': '随机推荐，仅供娱乐'
        }
    
    def _generate_pl3_recommendation(self, pos_analysis: List[Dict], hot_cold: Dict) -> List[List[int]]:
        """生成排列三推荐号码"""
        recommendations = []
        
        for _ in range(5):  # 生成5组推荐
            pick = []
            for pos in pos_analysis:
                # 70%概率选热号，20%温号，10%冷号
                r = random.random()
                if r < 0.7 and pos['hot']:
                    pick.append(random.choice(pos['hot']))
                elif r < 0.9:
                    # 从非热非冷中选
                    warm = [n for n in range(10) if n not in pos['hot'] and n not in pos['cold']]
                    pick.append(random.choice(warm) if warm else random.randint(0, 9))
                else:
                    pick.append(random.choice(pos['cold']) if pos['cold'] else random.randint(0, 9))
            
            if pick not in recommendations:
                recommendations.append(pick)
        
        return recommendations
    
    # ==================== 排列五 ====================
    
    def analyze_pl5(self, history_data: List[List[int]] = None) -> Dict:
        """分析排列五"""
        if history_data is None:
            history_data = self._load_mock_data('pl5')
        
        positions = [[], [], [], [], []]
        for draw in history_data:
            for i, num in enumerate(draw):
                positions[i].append(num)
        
        all_numbers = [n for draw in history_data for n in draw]
        hot_cold = self._calc_hot_cold(all_numbers, 0, 9)
        
        # 跨度分析(最大-最小)
        spans = [max(draw) - min(draw) for draw in history_data]
        span_analysis = {
            'recent_avg': sum(spans[-10:]) / 10,
            'max_span': max(spans[-30:]),
            'min_span': min(spans[-30:])
        }
        
        # 生成推荐
        recommendations = []
        for _ in range(3):
            pick = []
            for pos_nums in positions:
                pos_hot_cold = self._calc_hot_cold(pos_nums, 0, 9)
                if random.random() < 0.6 and pos_hot_cold['hot']:
                    pick.append(random.choice(pos_hot_cold['hot']))
                else:
                    pick.append(random.randint(0, 9))
            recommendations.append(pick)
        
        return {
            'lottery_type': '排列五',
            'hot_numbers': hot_cold['hot'],
            'cold_numbers': hot_cold['cold'],
            'span_analysis': span_analysis,
            'recommendation': recommendations,
            'disclaimer': '随机推荐，仅供娱乐'
        }
    
    # ==================== 大乐透 ====================
    
    def analyze_dlt(self, history_data: List[Dict] = None) -> Dict:
        """
        分析大乐透
        
        history_data格式: [{'front': [1,5,10,15,20], 'back': [3,7]}, ...]
        """
        if history_data is None:
            history_data = self._load_mock_data('dlt')
        
        # 前区分析
        front_numbers = [n for draw in history_data for n in draw['front']]
        front_hot_cold = self._calc_hot_cold(front_numbers, 1, 35)
        
        # 后区分析
        back_numbers = [n for draw in history_data for n in draw['back']]
        back_hot_cold = self._calc_hot_cold(back_numbers, 1, 12)
        
        # 区间分析 (1-12, 13-24, 25-35)
        zone_distribution = []
        for draw in history_data[-10:]:
            zones = [0, 0, 0]  # 一区、二区、三区
            for n in draw['front']:
                if n <= 12:
                    zones[0] += 1
                elif n <= 24:
                    zones[1] += 1
                else:
                    zones[2] += 1
            zone_distribution.append(zones)
        
        # 奇偶比分析
        odd_even_ratios = []
        for draw in history_data[-10:]:
            odd = sum(1 for n in draw['front'] if n % 2 == 1)
            odd_even_ratios.append(f"{odd}:{5-odd}")
        
        # 生成推荐
        recommendations = []
        for _ in range(3):
            # 前区：热号为主
            front_pick = []
            available = list(range(1, 36))
            
            # 60%选热号
            for _ in range(5):
                if random.random() < 0.6 and front_hot_cold['hot']:
                    valid_hot = [n for n in front_hot_cold['hot'] if n in available]
                    if valid_hot:
                        num = random.choice(valid_hot)
                        front_pick.append(num)
                        available.remove(num)
                        continue
                
                num = random.choice(available)
                front_pick.append(num)
                available.remove(num)
            
            # 后区
            back_pick = []
            available_back = list(range(1, 13))
            for _ in range(2):
                if random.random() < 0.6 and back_hot_cold['hot']:
                    valid_hot = [n for n in back_hot_cold['hot'] if n in available_back]
                    if valid_hot:
                        num = random.choice(valid_hot)
                        back_pick.append(num)
                        available_back.remove(num)
                        continue
                
                num = random.choice(available_back)
                back_pick.append(num)
                available_back.remove(num)
            
            recommendations.append({
                'front': sorted(front_pick),
                'back': sorted(back_pick)
            })
        
        return {
            'lottery_type': '大乐透',
            'front_hot': front_hot_cold['hot'][:5],
            'front_cold': front_hot_cold['cold'][:5],
            'back_hot': back_hot_cold['hot'][:3],
            'back_cold': back_hot_cold['cold'][:3],
            'zone_distribution': zone_distribution[-5:],
            'odd_even_trend': odd_even_ratios[-5:],
            'recommendation': recommendations,
            'disclaimer': '随机推荐，仅供娱乐'
        }
    
    # ==================== 双色球 ====================
    
    def analyze_ssq(self, history_data: List[Dict] = None) -> Dict:
        """
        分析双色球
        
        history_data格式: [{'red': [1,5,10,15,20,25], 'blue': 7}, ...]
        """
        if history_data is None:
            history_data = self._load_mock_data('ssq')
        
        # 红球分析
        red_numbers = [n for draw in history_data for n in draw['red']]
        red_hot_cold = self._calc_hot_cold(red_numbers, 1, 33)
        
        # 蓝球分析
        blue_numbers = [draw['blue'] for draw in history_data]
        blue_hot_cold = self._calc_hot_cold(blue_numbers, 1, 16)
        
        # 三区分布 (1-11, 12-22, 23-33)
        zone_distribution = []
        for draw in history_data[-10:]:
            zones = [0, 0, 0]
            for n in draw['red']:
                if n <= 11:
                    zones[0] += 1
                elif n <= 22:
                    zones[1] += 1
                else:
                    zones[2] += 1
            zone_distribution.append(zones)
        
        # 生成推荐
        recommendations = []
        for _ in range(3):
            red_pick = []
            available = list(range(1, 34))
            
            for _ in range(6):
                if random.random() < 0.6 and red_hot_cold['hot']:
                    valid_hot = [n for n in red_hot_cold['hot'] if n in available]
                    if valid_hot:
                        num = random.choice(valid_hot)
                        red_pick.append(num)
                        available.remove(num)
                        continue
                
                num = random.choice(available)
                red_pick.append(num)
                available.remove(num)
            
            # 蓝球
            if random.random() < 0.6 and blue_hot_cold['hot']:
                blue_pick = random.choice(blue_hot_cold['hot'])
            else:
                blue_pick = random.randint(1, 16)
            
            recommendations.append({
                'red': sorted(red_pick),
                'blue': blue_pick
            })
        
        return {
            'lottery_type': '双色球',
            'red_hot': red_hot_cold['hot'][:6],
            'red_cold': red_hot_cold['cold'][:6],
            'blue_hot': blue_hot_cold['hot'][:3],
            'blue_cold': blue_hot_cold['cold'][:3],
            'zone_distribution': zone_distribution[-5:],
            'recommendation': recommendations,
            'disclaimer': '随机推荐，仅供娱乐'
        }
    
    # ==================== 七星彩 ====================
    
    def analyze_qxc(self, history_data: List[List[int]] = None) -> Dict:
        """分析七星彩"""
        if history_data is None:
            history_data = self._load_mock_data('qxc')
        
        # 各位分析
        positions = [[] for _ in range(7)]
        for draw in history_data:
            for i, num in enumerate(draw):
                positions[i].append(num)
        
        all_numbers = [n for draw in history_data for n in draw]
        hot_cold = self._calc_hot_cold(all_numbers, 0, 9)
        
        # 和值分析
        sums = [sum(draw) for draw in history_data]
        
        # 生成推荐
        recommendations = []
        for _ in range(3):
            pick = []
            for pos_nums in positions:
                pos_hot_cold = self._calc_hot_cold(pos_nums, 0, 9)
                if random.random() < 0.6 and pos_hot_cold['hot']:
                    pick.append(random.choice(pos_hot_cold['hot']))
                else:
                    pick.append(random.randint(0, 9))
            recommendations.append(pick)
        
        return {
            'lottery_type': '七星彩',
            'hot_numbers': hot_cold['hot'],
            'cold_numbers': hot_cold['cold'],
            'sum_trend': {
                'recent_avg': sum(sums[-10:]) / 10,
                'trend': 'up' if sums[-1] > sums[-2] else 'down'
            },
            'recommendation': recommendations,
            'disclaimer': '随机推荐，仅供娱乐'
        }
    
    # ==================== 足彩14场 ====================
    
    def analyze_zc14(self, matches: List[Dict] = None) -> Dict:
        """
        分析足彩14场
        
        matches格式: [
            {
                'home': '阿森纳',
                'away': '切尔西',
                'home_odds': 1.80,
                'draw_odds': 3.40,
                'away_odds': 4.50,
                'home_form': ['W', 'W', 'D', 'L', 'W'],
                'away_form': ['L', 'D', 'W', 'W', 'L']
            },
            ...
        ]
        """
        if matches is None:
            matches = self._load_mock_data('zc14')
        
        predictions = []
        
        for i, match in enumerate(matches, 1):
            # 赔率转概率
            total_prob = 1/match['home_odds'] + 1/match['draw_odds'] + 1/match['away_odds']
            home_prob = (1/match['home_odds']) / total_prob
            draw_prob = (1/match['draw_odds']) / total_prob
            away_prob = (1/match['away_odds']) / total_prob
            
            # 近期战绩评分
            home_score = self._calc_form_score(match.get('home_form', []))
            away_score = self._calc_form_score(match.get('away_form', []))
            
            # 综合分析
            if home_prob > 0.55 and home_score > away_score:
                prediction = '3'  # 主胜
                confidence = '高'
            elif away_prob > 0.30 and away_score > home_score + 3:
                prediction = '0'  # 客胜
                confidence = '中'
            elif draw_prob > 0.25:
                prediction = '1'  # 平局
                confidence = '中'
            else:
                prediction = '3/1'  # 双选
                confidence = '低'
            
            predictions.append({
                'match_no': i,
                'home': match['home'],
                'away': match['away'],
                'odds': f"{match['home_odds']}/{match['draw_odds']}/{match['away_odds']}",
                'prediction': prediction,
                'confidence': confidence,
                'reason': f"主胜概率{home_prob:.1%}, 主队状态{home_score}, 客队状态{away_score}"
            })
        
        return {
            'lottery_type': '足彩14场',
            'predictions': predictions,
            'summary': {
                'high_confidence': sum(1 for p in predictions if p['confidence'] == '高'),
                'medium_confidence': sum(1 for p in predictions if p['confidence'] == '中'),
                'low_confidence': sum(1 for p in predictions if p['confidence'] == '低'),
                'double_selections': sum(1 for p in predictions if '/' in p['prediction'])
            },
            'disclaimer': '基于赔率分析，仅供参考'
        }
    
    def _calc_form_score(self, form: List[str]) -> int:
        """计算近期战绩得分"""
        score_map = {'W': 3, 'D': 1, 'L': 0}
        return sum(score_map.get(r, 0) for r in form[-5:])
    
    # ==================== 通用工具方法 ====================
    
    def _calc_hot_cold(self, numbers: List[int], min_num: int, max_num: int) -> Dict:
        """计算冷热号"""
        if not numbers:
            return {'hot': [], 'cold': [], 'warm': []}
        
        counter = Counter(numbers)
        avg_freq = sum(counter.values()) / (max_num - min_num + 1)
        
        hot = [n for n in range(min_num, max_num + 1) 
               if counter[n] > avg_freq * 1.5]
        cold = [n for n in range(min_num, max_num + 1) 
                if counter[n] < avg_freq * 0.5]
        warm = [n for n in range(min_num, max_num + 1) 
                if n not in hot and n not in cold]
        
        # 按频率排序
        hot.sort(key=lambda x: counter[x], reverse=True)
        cold.sort(key=lambda x: counter[x])
        
        return {'hot': hot, 'cold': cold, 'warm': warm, 'frequencies': dict(counter)}
    
    def _calc_missing(self, numbers: List[int], min_num: int, max_num: int, window: int = 30) -> Dict:
        """计算遗漏值"""
        missing = {}
        recent = numbers[-window:] if len(numbers) > window else numbers
        
        for num in range(min_num, max_num + 1):
            # 从最近往前找
            found = False
            for i, n in enumerate(reversed(recent)):
                if n == num:
                    missing[num] = i
                    found = True
                    break
            if not found:
                missing[num] = len(recent)
        
        return missing
    
    def _load_mock_data(self, lottery_type: str) -> List:
        """加载模拟数据（实际使用时应从API获取）"""
        # 这里返回模拟数据，实际实现中应该从数据源获取
        mock_data = {
            'pl3': [[random.randint(0, 9) for _ in range(3)] for _ in range(100)],
            'pl5': [[random.randint(0, 9) for _ in range(5)] for _ in range(100)],
            'qxc': [[random.randint(0, 9) for _ in range(7)] for _ in range(100)],
        }
        
        # 大乐透模拟数据
        dlt_data = []
        for _ in range(100):
            front = random.sample(range(1, 36), 5)
            back = random.sample(range(1, 13), 2)
            dlt_data.append({'front': sorted(front), 'back': sorted(back)})
        mock_data['dlt'] = dlt_data
        
        # 双色球模拟数据
        ssq_data = []
        for _ in range(100):
            red = random.sample(range(1, 34), 6)
            blue = random.randint(1, 16)
            ssq_data.append({'red': sorted(red), 'blue': blue})
        mock_data['ssq'] = ssq_data
        
        # 足彩14场模拟数据
        teams = ['阿森纳', '切尔西', '曼联', '利物浦', '曼城', '热刺', '皇马', '巴萨', 
                 '马竞', '拜仁', '多特', '尤文', '国米', '米兰', '巴黎', '里昂']
        zc14_data = []
        for _ in range(14):
            home, away = random.sample(teams, 2)
            zc14_data.append({
                'home': home,
                'away': away,
                'home_odds': round(random.uniform(1.5, 3.0), 2),
                'draw_odds': round(random.uniform(3.0, 4.0), 2),
                'away_odds': round(random.uniform(2.5, 5.0), 2),
                'home_form': random.choices(['W', 'D', 'L'], k=5),
                'away_form': random.choices(['W', 'D', 'L'], k=5)
            })
        mock_data['zc14'] = zc14_data
        
        return mock_data.get(lottery_type, [])


# ==================== CLI 入口 ====================

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='彩票预测分析工具')
    parser.add_argument('type', choices=['pl3', 'pl5', 'dlt', 'ssq', 'qxc', 'zc14'],
                       help='彩票类型')
    parser.add_argument('--analyze', action='store_true', help='执行分析')
    parser.add_argument('--recommend', action='store_true', help='生成推荐')
    
    args = parser.parse_args()
    
    predictor = LotteryPredictor()
    
    # 映射类型到分析方法
    method_map = {
        'pl3': predictor.analyze_pl3,
        'pl5': predictor.analyze_pl5,
        'dlt': predictor.analyze_dlt,
        'ssq': predictor.analyze_ssq,
        'qxc': predictor.analyze_qxc,
        'zc14': predictor.analyze_zc14
    }
    
    result = method_map[args.type]()
    
    # 打印结果
    print(f"\n{'='*60}")
    print(f"🎲 {result['lottery_type']} 分析报告")
    print(f"{'='*60}")
    
    if 'hot_numbers' in result:
        print(f"\n🔥 热号: {result['hot_numbers'][:5]}")
    if 'cold_numbers' in result:
        print(f"❄️  冷号: {result['cold_numbers'][:5]}")
    
    if 'recommendation' in result:
        print(f"\n🎯 推荐号码:")
        for i, rec in enumerate(result['recommendation'], 1):
            if isinstance(rec, dict):
                if 'front' in rec:
                    print(f"   推荐{i}: 前区{rec['front']} + 后区{rec['back']}")
                elif 'red' in rec:
                    print(f"   推荐{i}: 红球{rec['red']} + 蓝球{rec['blue']}")
            else:
                print(f"   推荐{i}: {rec}")
    
    print(f"\n⚠️  {result['disclaimer']}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
