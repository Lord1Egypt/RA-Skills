#!/usr/bin/env python3
"""
Pooled Standard Deviation Calculator
合并标准差计算工具

Supports three sigma estimation methods:
1. Range method (R̄/d₂) - for small samples (n≤10)
2. Standard deviation method (s̄/c₄) - for medium samples (10<n≤25)
3. Pooled standard deviation (s_p) - for large samples (n>25)
"""

import json
import argparse
import numpy as np
from typing import List, Dict, Tuple


# Control chart coefficients
COEFFICIENTS = {
    2: {'d2': 1.128, 'c4': 0.7979, 'A2': 1.880, 'D3': 0.000, 'D4': 3.267},
    3: {'d2': 1.693, 'c4': 0.8862, 'A2': 1.023, 'D3': 0.000, 'D4': 2.574},
    4: {'d2': 2.059, 'c4': 0.9213, 'A2': 0.729, 'D3': 0.000, 'D4': 2.282},
    5: {'d2': 2.326, 'c4': 0.9400, 'A2': 0.577, 'D3': 0.000, 'D4': 2.114},
    6: {'d2': 2.534, 'c4': 0.9515, 'A2': 0.483, 'D3': 0.000, 'D4': 2.004},
    7: {'d2': 2.704, 'c4': 0.9594, 'A2': 0.419, 'D3': 0.076, 'D4': 1.924},
    8: {'d2': 2.847, 'c4': 0.9650, 'A2': 0.373, 'D3': 0.136, 'D4': 1.864},
    9: {'d2': 2.970, 'c4': 0.9693, 'A2': 0.337, 'D3': 0.184, 'D4': 1.816},
    10: {'d2': 3.078, 'c4': 0.9727, 'A2': 0.308, 'D3': 0.223, 'D4': 1.777},
    11: {'d2': 3.173, 'c4': 0.9754, 'A2': 0.285, 'D3': 0.256, 'D4': 1.744},
    12: {'d2': 3.258, 'c4': 0.9776, 'A2': 0.266, 'D3': 0.283, 'D4': 1.717},
    13: {'d2': 3.336, 'c4': 0.9794, 'A2': 0.249, 'D3': 0.307, 'D4': 1.693},
    14: {'d2': 3.407, 'c4': 0.9810, 'A2': 0.235, 'D3': 0.328, 'D4': 1.672},
    15: {'d2': 3.472, 'c4': 0.9823, 'A2': 0.223, 'D3': 0.347, 'D4': 1.653},
    16: {'d2': 3.532, 'c4': 0.9835, 'A2': 0.212, 'D3': 0.363, 'D4': 1.637},
    17: {'d2': 3.588, 'c4': 0.9845, 'A2': 0.203, 'D3': 0.378, 'D4': 1.622},
    18: {'d2': 3.640, 'c4': 0.9854, 'A2': 0.194, 'D3': 0.391, 'D4': 1.608},
    19: {'d2': 3.689, 'c4': 0.9862, 'A2': 0.187, 'D3': 0.403, 'D4': 1.597},
    20: {'d2': 3.735, 'c4': 0.9869, 'A2': 0.180, 'D3': 0.415, 'D4': 1.585},
    21: {'d2': 3.778, 'c4': 0.9876, 'A2': 0.173, 'D3': 0.425, 'D4': 1.575},
    22: {'d2': 3.819, 'c4': 0.9882, 'A2': 0.167, 'D3': 0.434, 'D4': 1.566},
    23: {'d2': 3.858, 'c4': 0.9887, 'A2': 0.162, 'D3': 0.443, 'D4': 1.557},
    24: {'d2': 3.895, 'c4': 0.9892, 'A2': 0.157, 'D3': 0.451, 'D4': 1.548},
    25: {'d2': 3.931, 'c4': 0.9896, 'A2': 0.153, 'D3': 0.459, 'D4': 1.541},
}


def get_coefficient(n: int, coeff: str) -> float:
    """Get control chart coefficient for sample size n"""
    if n < 2 or n > 25:
        raise ValueError(f"Sample size n={n} out of range (2-25)")
    return COEFFICIENTS[n][coeff]


def range_method(subgroups: List[List[float]]) -> Dict:
    """
    Sigma estimation using Range method (R̄/d₂)
    Recommended for small samples (n≤10)
    """
    n = len(subgroups[0])  # Subgroup size
    k = len(subgroups)     # Number of subgroups
    
    # Calculate ranges
    ranges = [max(sg) - min(sg) for sg in subgroups]
    R_bar = np.mean(ranges)
    
    # Get d₂ coefficient
    d2 = get_coefficient(n, 'd2')
    sigma_hat = R_bar / d2
    
    # Calculate process mean
    x_double_bar = np.mean([np.mean(sg) for sg in subgroups])
    
    return {
        'method': 'Range (R̄/d₂)',
        'recommended_for': 'Small samples (n≤10)',
        'subgroup_size': n,
        'num_subgroups': k,
        'R_bar': R_bar,
        'd2': d2,
        'sigma_hat': sigma_hat,
        'process_mean': x_double_bar
    }


def std_dev_method(subgroups: List[List[float]]) -> Dict:
    """
    Sigma estimation using Standard Deviation method (s̄/c₄)
    Recommended for medium samples (10<n≤25)
    """
    n = len(subgroups[0])  # Subgroup size
    k = len(subgroups)     # Number of subgroups
    
    # Calculate standard deviations
    std_devs = [np.std(sg, ddof=1) for sg in subgroups]
    s_bar = np.mean(std_devs)
    
    # Get c₄ coefficient
    c4 = get_coefficient(n, 'c4')
    sigma_hat = s_bar / c4
    
    # Calculate process mean
    x_double_bar = np.mean([np.mean(sg) for sg in subgroups])
    
    return {
        'method': 'Standard Deviation (s̄/c₄)',
        'recommended_for': 'Medium samples (10<n≤25)',
        'subgroup_size': n,
        'num_subgroups': k,
        's_bar': s_bar,
        'c4': c4,
        'sigma_hat': sigma_hat,
        'process_mean': x_double_bar
    }


def pooled_std_method(subgroups: List[List[float]]) -> Dict:
    """
    Sigma estimation using Pooled Standard Deviation (s_p)
    Recommended for large samples (n>25) or unequal subgroup sizes
    """
    k = len(subgroups)     # Number of subgroups
    
    # Calculate pooled standard deviation
    sum_variances = sum((len(sg) - 1) * np.var(sg, ddof=1) for sg in subgroups)
    sum_df = sum(len(sg) - 1 for sg in subgroups)
    
    s_pooled = np.sqrt(sum_variances / sum_df)
    
    # Calculate process mean (weighted average)
    total_n = sum(len(sg) for sg in subgroups)
    x_double_bar = sum(np.sum(sg) for sg in subgroups) / total_n
    
    # Average subgroup size
    n_avg = total_n / k
    
    return {
        'method': 'Pooled Standard Deviation (s_p)',
        'recommended_for': 'Large samples (n>25) or unequal subgroup sizes',
        'subgroup_size': f'{n_avg:.2f} (average)',
        'num_subgroups': k,
        'total_samples': total_n,
        'degrees_of_freedom': sum_df,
        's_pooled': s_pooled,
        'sigma_hat': s_pooled,
        'process_mean': x_double_bar
    }


def compare_methods(subgroups: List[List[float]]) -> Dict:
    """
    Compare all three sigma estimation methods
    """
    n = len(subgroups[0])
    
    results = {
        'subgroup_size': n,
        'num_subgroups': len(subgroups),
        'methods': {}
    }
    
    # Range method
    if n <= 10:
        results['methods']['range'] = range_method(subgroups)
    else:
        results['methods']['range'] = {'note': 'Not recommended for n>10'}
    
    # Std dev method
    if 2 < n <= 25:
        results['methods']['std_dev'] = std_dev_method(subgroups)
    else:
        results['methods']['std_dev'] = {'note': 'Not recommended for n>25 or n≤2'}
    
    # Pooled method (always applicable)
    results['methods']['pooled'] = pooled_std_method(subgroups)
    
    # Recommendation
    if n <= 10:
        results['recommendation'] = 'Range method (R̄/d₂) - Simple and effective for small samples'
    elif n <= 25:
        results['recommendation'] = 'Standard deviation method (s̄/c₄) - More accurate for medium samples'
    else:
        results['recommendation'] = 'Pooled standard deviation (s_p) - Best for large samples'
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Sigma Estimation Methods Comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # From JSON data
  python3 pooled_std.py --data "[[10.1,10.2,10.15],[10.05,10.22,10.08],...]" --json
  
  # From CSV file (each row is a subgroup)
  python3 pooled_std.py --input subgroups.csv --json
  
  # Compare all methods
  python3 pooled_std.py --data "[[...],[...],...]" --compare --json
        '''
    )
    
    parser.add_argument('--data', type=str, help='Subgroup data as JSON array of arrays')
    parser.add_argument('--input', type=str, help='Input CSV file (each row is a subgroup)')
    parser.add_argument('--method', choices=['range', 'std_dev', 'pooled', 'all'], 
                       default='all', help='Sigma estimation method')
    parser.add_argument('--compare', action='store_true', help='Compare all methods')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Load data
    if args.data:
        subgroups = json.loads(args.data)
    elif args.input:
        import pandas as pd
        df = pd.read_csv(args.input)
        subgroups = df.values.tolist()
    else:
        parser.error('Must specify --data or --input')
    
    # Validate subgroups
    if not subgroups or len(subgroups) < 2:
        parser.error('Need at least 2 subgroups')
    
    # Run analysis
    if args.compare or args.method == 'all':
        results = compare_methods(subgroups)
    elif args.method == 'range':
        results = range_method(subgroups)
    elif args.method == 'std_dev':
        results = std_dev_method(subgroups)
    elif args.method == 'pooled':
        results = pooled_std_method(subgroups)
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*60)
        print("Sigma Estimation Methods")
        print("="*60)
        
        if 'recommendation' in results:
            print(f"\nSubgroup Size: {results['subgroup_size']}")
            print(f"Number of Subgroups: {results['num_subgroups']}")
            print(f"\n💡 Recommendation: {results['recommendation']}")
            
            print("\n" + "-"*60)
            print("Method Comparison:")
            print("-"*60)
            
            for method_name, method_result in results['methods'].items():
                if 'note' in method_result:
                    print(f"\n{method_name.upper()}: {method_result['note']}")
                else:
                    print(f"\n{method_name.upper()}:")
                    print(f"  Method: {method_result['method']}")
                    print(f"  σ̂ = {method_result['sigma_hat']:.6f}")
                    print(f"  Process Mean = {method_result['process_mean']:.6f}")
        else:
            print(f"\nMethod: {results['method']}")
            print(f"Recommended for: {results['recommended_for']}")
            print(f"\nResults:")
            print(f"  σ̂ (Sigma Estimate) = {results['sigma_hat']:.6f}")
            print(f"  Process Mean = {results['process_mean']:.6f}")
            
            if 'd2' in results:
                print(f"  R̄ = {results['R_bar']:.6f}")
                print(f"  d₂ = {results['d2']:.4f}")
                print(f"  Formula: σ̂ = R̄/d₂ = {results['R_bar']:.6f}/{results['d2']:.4f} = {results['sigma_hat']:.6f}")
            
            if 'c4' in results:
                print(f"  s̄ = {results['s_bar']:.6f}")
                print(f"  c₄ = {results['c4']:.4f}")
                print(f"  Formula: σ̂ = s̄/c₄ = {results['s_bar']:.6f}/{results['c4']:.4f} = {results['sigma_hat']:.6f}")
        
        print("\n" + "="*60)


if __name__ == '__main__':
    main()
