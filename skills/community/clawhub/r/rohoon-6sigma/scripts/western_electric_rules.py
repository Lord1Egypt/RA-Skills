#!/usr/bin/env python3
"""
Western Electric 7 Rules for Out-of-Control Detection
基于 Western Electric 7 判异规则的失控检测

Rules:
1. Any point beyond 3σ control limits
2. 9 consecutive points on same side of center line
3. 6 consecutive points increasing or decreasing (trend)
4. 14 consecutive points alternating up and down
5. 2 out of 3 consecutive points beyond 2σ
6. 4 out of 5 consecutive points beyond 1σ
7. 15 consecutive points within 1σ (stratification)
"""

import json
import argparse
import numpy as np
from typing import List, Dict, Tuple


class WesternElectricRules:
    """Western Electric 7 Rules Detector"""
    
    def __init__(self, data: List[float], cl: float, ucl: float, lcl: float):
        """
        Initialize the detector
        
        Args:
            data: Process data points
            cl: Center line (process mean)
            ucl: Upper control limit (3σ)
            lcl: Lower control limit (3σ)
        """
        self.data = np.array(data)
        self.cl = cl
        self.ucl = ucl
        self.lcl = lcl
        
        # Calculate sigma zones
        self.sigma = (ucl - cl) / 3
        self.uwl = cl + 2 * self.sigma  # Upper warning limit (2σ)
        self.lwl = cl - 2 * self.sigma  # Lower warning limit (2σ)
        self.uzl = cl + self.sigma      # Upper zone limit (1σ)
        self.lzl = cl - self.sigma      # Lower zone limit (1σ)
        
        self.violations = []
    
    def check_rule_1(self) -> List[int]:
        """
        Rule 1: Any point beyond 3σ control limits
        任何点超出 3σ控制限
        """
        violations = []
        for i, x in enumerate(self.data):
            if x > self.ucl or x < self.lcl:
                violations.append(i)
        return violations
    
    def check_rule_2(self) -> List[int]:
        """
        Rule 2: 9 consecutive points on same side of center line
        连续 9 点在中心线同一侧
        """
        violations = []
        consecutive_above = 0
        consecutive_below = 0
        
        for i, x in enumerate(self.data):
            if x > self.cl:
                consecutive_above += 1
                consecutive_below = 0
            elif x < self.cl:
                consecutive_below += 1
                consecutive_above = 0
            else:
                consecutive_above = 0
                consecutive_below = 0
            
            if consecutive_above >= 9 or consecutive_below >= 9:
                violations.append(i)
        
        return violations
    
    def check_rule_3(self) -> List[int]:
        """
        Rule 3: 6 consecutive points increasing or decreasing (trend)
        连续 6 点递增或递减 (趋势)
        """
        violations = []
        consecutive_increasing = 0
        consecutive_decreasing = 0
        
        for i in range(1, len(self.data)):
            if self.data[i] > self.data[i-1]:
                consecutive_increasing += 1
                consecutive_decreasing = 0
            elif self.data[i] < self.data[i-1]:
                consecutive_decreasing += 1
                consecutive_increasing = 0
            else:
                consecutive_increasing = 0
                consecutive_decreasing = 0
            
            if consecutive_increasing >= 6 or consecutive_decreasing >= 6:
                violations.append(i)
        
        return violations
    
    def check_rule_4(self) -> List[int]:
        """
        Rule 4: 14 consecutive points alternating up and down
        连续 14 点交替上下
        """
        violations = []
        consecutive_alternating = 0
        
        for i in range(2, len(self.data)):
            prev_diff = self.data[i-1] - self.data[i-2]
            curr_diff = self.data[i] - self.data[i-1]
            
            if prev_diff * curr_diff < 0:  # Alternating
                consecutive_alternating += 1
            else:
                consecutive_alternating = 0
            
            if consecutive_alternating >= 13:  # 14 points = 13 alternations
                violations.append(i)
        
        return violations
    
    def check_rule_5(self) -> List[int]:
        """
        Rule 5: 2 out of 3 consecutive points beyond 2σ
        3 点中 2 点超出 2σ
        """
        violations = []
        
        for i in range(2, len(self.data)):
            window = self.data[i-2:i+1]
            beyond_2sigma = sum(1 for x in window if x > self.uwl or x < self.lwl)
            
            if beyond_2sigma >= 2:
                violations.append(i)
        
        return violations
    
    def check_rule_6(self) -> List[int]:
        """
        Rule 6: 4 out of 5 consecutive points beyond 1σ
        5 点中 4 点超出 1σ
        """
        violations = []
        
        for i in range(4, len(self.data)):
            window = self.data[i-4:i+1]
            beyond_1sigma = sum(1 for x in window if x > self.uzl or x < self.lzl)
            
            if beyond_1sigma >= 4:
                violations.append(i)
        
        return violations
    
    def check_rule_7(self) -> List[int]:
        """
        Rule 7: 15 consecutive points within 1σ (stratification)
        连续 15 点在 1σ内 (分层)
        """
        violations = []
        consecutive_within_1sigma = 0
        
        for i, x in enumerate(self.data):
            if self.lzl <= x <= self.uzl:
                consecutive_within_1sigma += 1
            else:
                consecutive_within_1sigma = 0
            
            if consecutive_within_1sigma >= 15:
                violations.append(i)
        
        return violations
    
    def check_all_rules(self) -> Dict:
        """
        Check all 7 rules and return comprehensive results
        检查所有 7 条规则并返回综合结果
        """
        self.violations = {
            'rule_1': {
                'description': 'Any point beyond 3σ control limits (超出 3σ控制限)',
                'violations': self.check_rule_1()
            },
            'rule_2': {
                'description': '9 consecutive points on same side of CL (连续 9 点同侧)',
                'violations': self.check_rule_2()
            },
            'rule_3': {
                'description': '6 consecutive points increasing/decreasing (连续 6 点递增/递减)',
                'violations': self.check_rule_3()
            },
            'rule_4': {
                'description': '14 consecutive points alternating (连续 14 点交替)',
                'violations': self.check_rule_4()
            },
            'rule_5': {
                'description': '2 out of 3 consecutive points beyond 2σ (3 点中 2 点超 2σ)',
                'violations': self.check_rule_5()
            },
            'rule_6': {
                'description': '4 out of 5 consecutive points beyond 1σ (5 点中 4 点超 1σ)',
                'violations': self.check_rule_6()
            },
            'rule_7': {
                'description': '15 consecutive points within 1σ (连续 15 点在 1σ内)',
                'violations': self.check_rule_7()
            }
        }
        
        # Summary
        total_violations = sum(len(v['violations']) for v in self.violations.values())
        is_in_control = total_violations == 0
        
        return {
            'summary': {
                'total_points': len(self.data),
                'center_line': self.cl,
                'ucl_3sigma': self.ucl,
                'lcl_3sigma': self.lcl,
                'sigma': self.sigma,
                'is_in_control': is_in_control,
                'total_violations': total_violations
            },
            'violations': self.violations
        }


def main():
    parser = argparse.ArgumentParser(
        description='Western Electric 7 Rules for Out-of-Control Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Check process data with control limits
  python3 western_electric_rules.py --data "[10.1,10.2,10.15,...]" --cl 10.0 --ucl 10.5 --lcl 9.5
  
  # From file
  python3 western_electric_rules.py --input data.csv --cl 10.0 --ucl 10.5 --lcl 9.5 --json
        '''
    )
    
    parser.add_argument('--data', type=str, help='Process data as JSON array')
    parser.add_argument('--input', type=str, help='Input CSV file with data column')
    parser.add_argument('--cl', type=float, required=True, help='Center line (CL)')
    parser.add_argument('--ucl', type=float, required=True, help='Upper control limit (UCL)')
    parser.add_argument('--lcl', type=float, required=True, help='Lower control limit (LCL)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Load data
    if args.data:
        data = json.loads(args.data)
    elif args.input:
        import pandas as pd
        df = pd.read_csv(args.input)
        data = df['data'].tolist() if 'data' in df.columns else df.iloc[:, 0].tolist()
    else:
        parser.error('Must specify --data or --input')
    
    # Run detection
    detector = WesternElectricRules(data, args.cl, args.ucl, args.lcl)
    results = detector.check_all_rules()
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*60)
        print("Western Electric 7 Rules - Out-of-Control Detection")
        print("="*60)
        print(f"\nTotal Points: {results['summary']['total_points']}")
        print(f"Center Line (CL): {results['summary']['center_line']:.4f}")
        print(f"UCL (3σ): {results['summary']['ucl_3sigma']:.4f}")
        print(f"LCL (3σ): {results['summary']['lcl_3sigma']:.4f}")
        print(f"Sigma: {results['summary']['sigma']:.4f}")
        print(f"\nProcess Status: {'✅ IN CONTROL' if results['summary']['is_in_control'] else '❌ OUT OF CONTROL'}")
        print(f"Total Violations: {results['summary']['total_violations']}")
        
        print("\n" + "-"*60)
        print("Rule Violations:")
        print("-"*60)
        
        for rule, info in results['violations'].items():
            status = "❌" if info['violations'] else "✅"
            print(f"\n{status} {rule}: {info['description']}")
            if info['violations']:
                print(f"   Violation points: {info['violations']}")
        
        print("\n" + "="*60)


if __name__ == '__main__':
    main()
