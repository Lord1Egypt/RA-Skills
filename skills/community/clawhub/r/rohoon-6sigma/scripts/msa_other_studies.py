#!/usr/bin/env python3
"""
MSA Other Studies Tool
Supports: Bias, Linearity, Stability studies
Based on AIAG MSA Manual 4th Edition

Usage:
    python3 msa_other_studies.py --study-type bias --data "10.1,10.15,..." --reference 10.0 --tolerance 0.5 --json
    python3 msa_other_studies.py --study-type linearity --data "[...]" --references "[10,20,30,40,50]" --json
"""

import argparse
import json
import sys
import numpy as np
from scipy import stats
from typing import Dict, Any, List


def parse_data(data_str: str) -> List[float]:
    """Parse input data string"""
    try:
        data = json.loads(data_str)
        if isinstance(data, list):
            return [float(x) for x in data]
    except:
        pass
    
    try:
        return [float(x.strip()) for x in data_str.split(',')]
    except:
        raise ValueError("Cannot parse data")


def calculate_bias(
    data: List[float],
    reference: float,
    tolerance: float = None
) -> Dict[str, Any]:
    """
    Calculate bias study
    
    Returns:
        Dictionary with bias, t-statistic, p-value, and evaluation
    """
    data_array = np.array(data)
    n = len(data_array)
    mean = np.mean(data_array)
    std = np.std(data_array, ddof=1)
    
    # Calculate bias
    bias = mean - reference
    
    # Calculate t-statistic
    se = std / np.sqrt(n)  # Standard error
    t_stat = bias / se if se > 0 else 0
    
    # Calculate p-value (two-tailed)
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
    
    # Calculate confidence interval (95%)
    t_critical = stats.t.ppf(0.975, df=n-1)
    ci_lower = bias - t_critical * se
    ci_upper = bias + t_critical * se
    
    # Calculate bias percentage
    if tolerance:
        bias_percent = (abs(bias) / tolerance) * 100
    else:
        bias_percent = (abs(bias) / abs(reference)) * 100
    
    # Evaluation
    is_significant = bool(p_value < 0.05)
    if bias_percent < 5:
        rating = 'excellent'
    elif bias_percent < 10:
        rating = 'acceptable'
    elif bias_percent < 30:
        rating = 'marginal'
    else:
        rating = 'unacceptable'
    
    result = {
        'study_type': 'bias',
        'n_measurements': int(n),
        'reference_value': float(reference),
        'mean': float(mean),
        'std': float(std),
        'bias': float(bias),
        'bias_percent': float(bias_percent),
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'is_significant': is_significant,
        'rating': rating,
        'acceptable': bool(bias_percent < 10 and not is_significant),
    }
    
    if tolerance:
        result['tolerance'] = float(tolerance)
    
    return result


def calculate_linearity(
    data: List[float],
    references: List[float],
    tolerance: float = None
) -> Dict[str, Any]:
    """
    Calculate linearity study
    
    Returns:
        Dictionary with slope, intercept, R², linearity, and evaluation
    """
    data_array = np.array(data)
    ref_array = np.array(references)
    
    # Check if we have multiple measurements per reference
    n_refs = len(ref_array)
    n_meas = len(data_array)
    
    if n_meas % n_refs == 0:
        # Multiple measurements per reference - calculate means
        n_per_ref = n_meas // n_refs
        means = [np.mean(data_array[i*n_per_ref:(i+1)*n_per_ref]) for i in range(n_refs)]
        means = np.array(means)
    else:
        # One measurement per reference
        means = data_array
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(ref_array, means)
    r_squared = r_value ** 2
    
    # Calculate linearity
    linearity = abs(slope) * (max(ref_array) - min(ref_array))
    
    if tolerance:
        linearity_percent = (linearity / tolerance) * 100
    else:
        linearity_percent = (linearity / (max(ref_array) - min(ref_array))) * 100
    
    # Calculate bias at each reference
    biases = means - (slope * ref_array + intercept)
    avg_bias = np.mean(biases)
    
    # Evaluation
    is_linear = r_squared >= 0.95 and linearity_percent < 10
    if linearity_percent < 5:
        rating = 'excellent'
    elif linearity_percent < 10:
        rating = 'acceptable'
    elif linearity_percent < 30:
        rating = 'marginal'
    else:
        rating = 'unacceptable'
    
    result = {
        'study_type': 'linearity',
        'n_references': int(n_refs),
        'n_measurements': int(n_meas),
        'slope': float(slope),
        'intercept': float(intercept),
        'r_squared': float(r_squared),
        'p_value_slope': float(p_value),
        'linearity': float(linearity),
        'linearity_percent': float(linearity_percent),
        'avg_bias': float(avg_bias),
        'is_linear': bool(is_linear),
        'rating': rating,
        'acceptable': is_linear,
    }
    
    if tolerance:
        result['tolerance'] = float(tolerance)
    
    return result


def calculate_stability(
    data: List[float],
    reference: float = None,
    times: List[str] = None
) -> Dict[str, Any]:
    """
    Calculate stability study using control chart method
    
    Returns:
        Dictionary with mean, std, control limits, and stability evaluation
    """
    data_array = np.array(data)
    n = len(data_array)
    mean = np.mean(data_array)
    std = np.std(data_array, ddof=1)
    
    # Calculate control limits (I-MR chart method)
    # Moving range
    mr = np.abs(np.diff(data_array))
    mr_bar = np.mean(mr)
    
    # Control limits for I chart
    d2 = 1.128  # For n=2 (moving range)
    sigma_est = mr_bar / d2
    ucl = mean + 3 * sigma_est
    lcl = mean - 3 * sigma_est
    
    # Check for out-of-control points
    ooc_points = []
    for i, val in enumerate(data_array):
        if val > ucl or val < lcl:
            ooc_points.append(i)
    
    # Check for trends (7 points in a row on same side of center)
    has_trend = False
    for i in range(n - 7):
        segment = data_array[i:i+7]
        if all(x > mean for x in segment) or all(x < mean for x in segment):
            has_trend = True
            break
    
    # Calculate drift (if reference provided)
    if reference:
        drift = mean - reference
        drift_percent = (abs(drift) / abs(reference)) * 100
    else:
        drift = 0
        drift_percent = 0
    
    # Evaluation
    is_stable = len(ooc_points) == 0 and not has_trend
    if is_stable and drift_percent < 1:
        rating = 'excellent'
    elif is_stable and drift_percent < 5:
        rating = 'acceptable'
    elif drift_percent < 10:
        rating = 'marginal'
    else:
        rating = 'unacceptable'
    
    result = {
        'study_type': 'stability',
        'n_measurements': int(n),
        'mean': float(mean),
        'std': float(std),
        'ucl': float(ucl),
        'lcl': float(lcl),
        'sigma_est': float(sigma_est),
        'ooc_points': ooc_points,
        'has_trend': bool(has_trend),
        'drift': float(drift),
        'drift_percent': float(drift_percent),
        'is_stable': bool(is_stable),
        'rating': rating,
        'acceptable': is_stable and drift_percent < 10,
    }
    
    if reference:
        result['reference_value'] = float(reference)
    if times:
        result['time_points'] = times
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='MSA Other Studies (Bias, Linearity, Stability)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Bias study
  python3 msa_other_studies.py --study-type bias --data "10.1,10.15,10.12,..." --reference 10.0 --tolerance 0.5 --json
  
  # Linearity study (5 parts, 3 measurements each)
  python3 msa_other_studies.py --study-type linearity --data "[...15 values...]" --references "[10,20,30,40,50]" --tolerance 1.0 --json
  
  # Stability study
  python3 msa_other_studies.py --study-type stability --data "10.1,10.12,10.09,..." --reference 10.0 --json
        '''
    )
    
    parser.add_argument('--study-type', '-s', type=str, required=True,
                       choices=['bias', 'linearity', 'stability'],
                       help='Type of MSA study')
    parser.add_argument('--data', '-d', type=str, required=True,
                       help='Measurement data (JSON array or comma-separated)')
    parser.add_argument('--reference', '-r', type=float, default=None,
                       help='Reference value (for bias/stability)')
    parser.add_argument('--references', '-R', type=str, default=None,
                       help='Reference values for linearity study (JSON array)')
    parser.add_argument('--tolerance', '-T', type=float, default=None,
                       help='Tolerance (USL-LSL)')
    parser.add_argument('--times', '-t', type=str, default=None,
                       help='Time points (comma-separated, for stability)')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        # Parse data
        data = parse_data(args.data)
        
        if len(data) < 2:
            raise ValueError("At least 2 data points required")
        
        # Perform study based on type
        if args.study_type == 'bias':
            if not args.reference:
                raise ValueError("Reference value required for bias study")
            result = calculate_bias(data, args.reference, args.tolerance)
            
        elif args.study_type == 'linearity':
            if not args.references:
                raise ValueError("Reference values required for linearity study")
            references = parse_data(args.references)
            result = calculate_linearity(data, references, args.tolerance)
            
        elif args.study_type == 'stability':
            times = None
            if args.times:
                times = [t.strip() for t in args.times.split(',')]
            result = calculate_stability(data, args.reference, times)
        
        # Output
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print(f"MSA {args.study_type.title()} Study Results")
            print("=" * 60)
            
            if args.study_type == 'bias':
                print(f"Reference Value: {result['reference_value']}")
                print(f"Measurements: {result['n_measurements']}")
                print(f"Mean: {result['mean']:.4f}")
                print(f"Bias: {result['bias']:.4f} ({result['bias_percent']:.1f}%)")
                print(f"t-statistic: {result['t_statistic']:.3f}")
                print(f"p-value: {result['p_value']:.4f}")
                print(f"95% CI: [{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]")
                print(f"Significant: {'Yes ⚠️' if result['is_significant'] else 'No ✅'}")
                print(f"Rating: {result['rating']}")
                
            elif args.study_type == 'linearity':
                print(f"References: {result['n_references']}")
                print(f"Measurements: {result['n_measurements']}")
                print(f"Slope: {result['slope']:.4f}")
                print(f"Intercept: {result['intercept']:.4f}")
                print(f"R²: {result['r_squared']:.4f}")
                print(f"Linearity: {result['linearity']:.4f} ({result['linearity_percent']:.1f}%)")
                print(f"Linear: {'Yes ✅' if result['is_linear'] else 'No ⚠️'}")
                print(f"Rating: {result['rating']}")
                
            elif args.study_type == 'stability':
                print(f"Measurements: {result['n_measurements']}")
                print(f"Mean: {result['mean']:.4f}")
                print(f"Std Dev: {result['std']:.4f}")
                print(f"UCL: {result['ucl']:.4f}")
                print(f"LCL: {result['lcl']:.4f}")
                print(f"Out-of-Control Points: {len(result['ooc_points'])}")
                print(f"Trend Detected: {'Yes ⚠️' if result['has_trend'] else 'No ✅'}")
                print(f"Drift: {result['drift']:.4f} ({result['drift_percent']:.1f}%)")
                print(f"Stable: {'Yes ✅' if result['is_stable'] else 'No ⚠️'}")
                print(f"Rating: {result['rating']}")
            
            print(f"Acceptable: {'Yes ✅' if result['acceptable'] else 'No ❌'}")
            print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
