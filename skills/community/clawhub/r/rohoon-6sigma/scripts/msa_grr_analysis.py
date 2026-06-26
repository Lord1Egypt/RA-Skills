#!/usr/bin/env python3
"""
MSA GR&R Analysis Tool (Xbar-R Method)
Based on AIAG MSA Manual 4th Edition

Usage:
    python3 msa_grr_analysis.py --data "[...]" --parts 10 --operators 3 --trials 3 --tolerance 0.5 --json
"""

import argparse
import json
import sys
import numpy as np
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


def calculate_grr_xbar_r(
    data: List[float],
    n_parts: int,
    n_operators: int,
    n_trials: int,
    tolerance: float = None
) -> Dict[str, Any]:
    """
    Calculate GR&R using Xbar-R method
    
    Returns:
        Dictionary with EV, AV, GR&R, PV, TV, %GR&R, ndc, and evaluation
    """
    # Constants for R chart
    K1_constants = {2: 4.56, 3: 3.05, 4: 2.46, 5: 2.18, 6: 2.00, 7: 1.88, 8: 1.79, 9: 1.72, 10: 1.67}
    K2_constants = {2: 3.65, 3: 2.70, 4: 2.30, 5: 2.08, 6: 1.93, 7: 1.82, 8: 1.74, 9: 1.67, 10: 1.62}
    K3_constants = {2: 3.65, 3: 2.70, 4: 2.30, 5: 2.08, 6: 1.93, 7: 1.82, 8: 1.74, 9: 1.67, 10: 1.62}
    
    # Reshape data
    data_array = np.array(data).reshape(n_parts, n_operators, n_trials)
    
    # Calculate ranges (R) for each part-operator combination
    R = np.ptp(data_array, axis=2)  # Range across trials
    
    # Calculate average range (R_bar)
    R_bar = np.mean(R)
    
    # Calculate part averages
    part_means = np.mean(data_array, axis=(1, 2))
    
    # Calculate operator averages
    operator_means = np.mean(data_array, axis=(0, 2))
    
    # Calculate overall average
    grand_mean = np.mean(data_array)
    
    # Calculate range of operator averages
    R_op = np.max(operator_means) - np.min(operator_means)
    
    # Calculate range of part averages
    R_part = np.max(part_means) - np.min(part_means)
    
    # Get constants
    K1 = K1_constants.get(n_trials, 1.67)
    K2 = K2_constants.get(n_operators, 1.62)
    K3 = K3_constants.get(n_parts, 1.62)
    
    # Calculate variation components
    EV = R_bar * K1  # Equipment Variation (Repeatability)
    AV = np.sqrt((R_op * K2)**2 - (EV**2 / (n_parts * n_trials))) if (R_op * K2)**2 > (EV**2 / (n_parts * n_trials)) else 0  # Appraiser Variation (Reproducibility)
    PV = R_part * K3  # Part Variation
    
    # Calculate GR&R and Total Variation
    GRR = np.sqrt(EV**2 + AV**2)
    TV = np.sqrt(GRR**2 + PV**2)
    
    # Calculate percentages
    if tolerance:
        percent_ev = (EV / tolerance) * 100
        percent_av = (AV / tolerance) * 100
        percent_grr = (GRR / tolerance) * 100
        percent_pv = (PV / tolerance) * 100
    else:
        percent_ev = (EV / TV) * 100 if TV > 0 else 0
        percent_av = (AV / TV) * 100 if TV > 0 else 0
        percent_grr = (GRR / TV) * 100 if TV > 0 else 0
        percent_pv = (PV / TV) * 100 if TV > 0 else 0
    
    # Calculate ndc (Number of Distinct Categories)
    ndc = int(1.41 * (PV / GRR)) if GRR > 0 else 0
    
    # Evaluation
    if percent_grr < 10:
        acceptance = 'acceptable'
        is_acceptable = True
    elif percent_grr < 30:
        acceptance = 'conditionally_acceptable'
        is_acceptable = True
    else:
        acceptance = 'unacceptable'
        is_acceptable = False
    
    result = {
        'n_parts': n_parts,
        'n_operators': n_operators,
        'n_trials': n_trials,
        'total_measurements': len(data),
        'ev': float(EV),
        'av': float(AV),
        'grr': float(GRR),
        'pv': float(PV),
        'tv': float(TV),
        'percent_ev': float(percent_ev),
        'percent_av': float(percent_av),
        'percent_grr': float(percent_grr),
        'percent_pv': float(percent_pv),
        'ndc': ndc,
        'acceptance': acceptance,
        'is_acceptable': is_acceptable,
    }
    
    if tolerance:
        result['tolerance'] = float(tolerance)
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='MSA GR&R Analysis (Xbar-R Method)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Standard 10x3x3 study
  python3 msa_grr_analysis.py --data "[...90 values...]" --parts 10 --operators 3 --trials 3 --tolerance 0.5 --json
  
  # Without tolerance (uses total variation)
  python3 msa_grr_analysis.py --data "[...]" --parts 10 --operators 3 --trials 3 --json
        '''
    )
    
    parser.add_argument('--data', '-d', type=str, required=True,
                       help='Measurement data (JSON array or comma-separated)')
    parser.add_argument('--parts', '-p', type=int, required=True,
                       help='Number of parts')
    parser.add_argument('--operators', '-o', type=int, required=True,
                       help='Number of operators')
    parser.add_argument('--trials', '-t', type=int, required=True,
                       help='Number of trials per part-operator')
    parser.add_argument('--tolerance', '-T', type=float, default=None,
                       help='Tolerance (USL-LSL) for percent GRR calculation')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        # Parse data
        data = parse_data(args.data)
        
        # Validate data count
        expected_count = args.parts * args.operators * args.trials
        if len(data) != expected_count:
            raise ValueError(f"Expected {expected_count} data points, got {len(data)}")
        
        # Calculate GR&R
        result = calculate_grr_xbar_r(
            data,
            n_parts=args.parts,
            n_operators=args.operators,
            n_trials=args.trials,
            tolerance=args.tolerance
        )
        
        # Output
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("MSA GR&R Analysis Results (Xbar-R Method)")
            print("=" * 60)
            print(f"Parts: {result['n_parts']}, Operators: {result['n_operators']}, Trials: {result['n_trials']}")
            print(f"Total Measurements: {result['total_measurements']}")
            print()
            print("Variation Components:")
            print(f"  EV (Repeatability): {result['ev']:.4f} ({result['percent_ev']:.1f}%)")
            print(f"  AV (Reproducibility): {result['av']:.4f} ({result['percent_av']:.1f}%)")
            print(f"  GR&R: {result['grr']:.4f} ({result['percent_grr']:.1f}%)")
            print(f"  PV (Part Variation): {result['pv']:.4f} ({result['percent_pv']:.1f}%)")
            print(f"  TV (Total Variation): {result['tv']:.4f}")
            print()
            print("Evaluation:")
            print(f"  %GR&R: {result['percent_grr']:.1f}%")
            print(f"  ndc: {result['ndc']}")
            print(f"  Acceptance: {result['acceptance'].upper()}")
            print(f"  Status: {'✅ Acceptable' if result['is_acceptable'] else '❌ Unacceptable'}")
            
            if args.tolerance:
                print(f"  Tolerance: {args.tolerance}")
            
            print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
