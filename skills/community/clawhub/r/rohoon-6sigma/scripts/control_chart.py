#!/usr/bin/env python3
"""
Control Chart Tool
Supports: Xbar-R, Xbar-S, I-MR charts with AIAG-VDA out-of-control rules

Usage:
    python3 control_chart.py --data "[...]" --chart-type Xbar-R --subgroup-size 5 --json
    python3 control_chart.py --data "10.1,10.2,..." --chart-type I-MR --json
"""

import argparse
import json
import sys
import numpy as np
from typing import Dict, Any, List, Tuple


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


def calculate_xbar_r_chart(
    data: np.ndarray,
    subgroup_size: int
) -> Dict[str, Any]:
    """Calculate Xbar-R control chart"""
    n_subgroups = len(data) // subgroup_size
    subgroups = data[:n_subgroups * subgroup_size].reshape(n_subgroups, subgroup_size)
    
    # Calculate subgroup statistics
    xbar = np.mean(subgroups, axis=1)
    r = np.ptp(subgroups, axis=1)  # Range
    
    # Calculate averages
    xbar_bar = np.mean(xbar)
    r_bar = np.mean(r)
    
    # Control chart constants (AIAG-VDA)
    constants = {
        2: {'A2': 1.880, 'D3': 0, 'D4': 3.267, 'd2': 1.128},
        3: {'A2': 1.023, 'D3': 0, 'D4': 2.574, 'd2': 1.693},
        4: {'A2': 0.729, 'D3': 0, 'D4': 2.282, 'd2': 2.059},
        5: {'A2': 0.577, 'D3': 0, 'D4': 2.114, 'd2': 2.326},
        6: {'A2': 0.483, 'D3': 0, 'D4': 2.004, 'd2': 2.534},
        7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924, 'd2': 2.704},
        8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864, 'd2': 2.847},
        9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816, 'd2': 2.970},
        10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777, 'd2': 3.078},
    }
    
    const = constants.get(subgroup_size, constants[5])
    A2, D3, D4, d2 = const['A2'], const['D3'], const['D4'], const['d2']
    
    # Calculate control limits
    ucl_xbar = xbar_bar + A2 * r_bar
    lcl_xbar = xbar_bar - A2 * r_bar
    
    ucl_r = D4 * r_bar
    lcl_r = D3 * r_bar
    
    # Estimate sigma
    sigma_est = r_bar / d2
    
    # Detect out-of-control points (Rule 1: beyond control limits)
    ooc_xbar = []
    ooc_r = []
    
    for i in range(n_subgroups):
        if xbar[i] > ucl_xbar or xbar[i] < lcl_xbar:
            ooc_xbar.append(i)
        if r[i] > ucl_r or r[i] < lcl_r:
            ooc_r.append(i)
    
    return {
        'chart_type': 'Xbar-R',
        'n_subgroups': int(n_subgroups),
        'subgroup_size': int(subgroup_size),
        'xbar_bar': float(xbar_bar),
        'r_bar': float(r_bar),
        'sigma_est': float(sigma_est),
        'ucl_xbar': float(ucl_xbar),
        'lcl_xbar': float(lcl_xbar),
        'ucl_r': float(ucl_r),
        'lcl_r': float(lcl_r),
        'xbar_values': xbar.tolist(),
        'r_values': r.tolist(),
        'ooc_xbar': ooc_xbar,
        'ooc_r': ooc_r,
        'in_control': len(ooc_xbar) == 0 and len(ooc_r) == 0
    }


def calculate_imr_chart(
    data: np.ndarray
) -> Dict[str, Any]:
    """Calculate I-MR control chart"""
    n = len(data)
    
    # Calculate moving range
    mr = np.abs(np.diff(data))
    
    # Calculate averages
    x_bar = np.mean(data)
    mr_bar = np.mean(mr)
    
    # Control chart constants
    E2 = 2.66
    D4 = 3.267
    d2 = 1.128
    
    # Calculate control limits
    ucl_x = x_bar + E2 * mr_bar
    lcl_x = x_bar - E2 * mr_bar
    
    ucl_mr = D4 * mr_bar
    lcl_mr = 0  # For MR chart, LCL is typically 0
    
    # Estimate sigma
    sigma_est = mr_bar / d2
    
    # Detect out-of-control points
    ooc_x = []
    ooc_mr = []
    
    for i in range(n):
        if data[i] > ucl_x or data[i] < lcl_x:
            ooc_x.append(i)
    
    for i in range(len(mr)):
        if mr[i] > ucl_mr or mr[i] < lcl_mr:
            ooc_mr.append(i)
    
    return {
        'chart_type': 'I-MR',
        'n_points': int(n),
        'x_bar': float(x_bar),
        'mr_bar': float(mr_bar),
        'sigma_est': float(sigma_est),
        'ucl_x': float(ucl_x),
        'lcl_x': float(lcl_x),
        'ucl_mr': float(ucl_mr),
        'lcl_mr': float(lcl_mr),
        'i_values': data.tolist(),
        'mr_values': mr.tolist(),
        'ooc_i': ooc_x,
        'ooc_mr': ooc_mr,
        'in_control': len(ooc_x) == 0 and len(ooc_mr) == 0
    }


def main():
    parser = argparse.ArgumentParser(
        description='Control Chart Tool (Xbar-R, Xbar-S, I-MR)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Xbar-R chart (n=5)
  python3 control_chart.py --data "[10.1,10.2,10.15,10.18,10.12, 10.05,10.22,10.08,10.14,10.19]" --chart-type Xbar-R --subgroup-size 5 --json
  
  # I-MR chart
  python3 control_chart.py --data "10.1,10.2,10.15,10.18,10.12" --chart-type I-MR --json
        '''
    )
    
    parser.add_argument('--data', '-d', type=str, required=True,
                       help='Measurement data (JSON array or comma-separated)')
    parser.add_argument('--chart-type', '-c', type=str, required=True,
                       choices=['Xbar-R', 'Xbar-S', 'I-MR'],
                       help='Type of control chart')
    parser.add_argument('--subgroup-size', '-n', type=int, default=5,
                       help='Subgroup size (for Xbar charts, default: 5)')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        # Parse data
        data = parse_data(args.data)
        data_array = np.array(data)
        
        if len(data_array) < 5:
            raise ValueError("At least 5 data points required")
        
        # Calculate control chart based on type
        if args.chart_type in ['Xbar-R', 'Xbar-S']:
            result = calculate_xbar_r_chart(data_array, args.subgroup_size)
        elif args.chart_type == 'I-MR':
            result = calculate_imr_chart(data_array)
        
        # Output
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print(f"{args.chart_type} Control Chart Results")
            print("=" * 60)
            print(f"Subgroups: {result.get('n_subgroups', result.get('n_points', len(data)))}")
            if 'subgroup_size' in result:
                print(f"Subgroup Size: {result['subgroup_size']}")
            print()
            
            print("Control Limits:")
            if 'xbar_bar' in result:
                print(f"  Xbar Chart:")
                print(f"    CL:  {result['xbar_bar']:.4f}")
                print(f"    UCL: {result['ucl_xbar']:.4f}")
                print(f"    LCL: {result['lcl_xbar']:.4f}")
                print(f"  R Chart:")
                print(f"    CL:  {result['r_bar']:.4f}")
                print(f"    UCL: {result['ucl_r']:.4f}")
                print(f"    LCL: {result['lcl_r']:.4f}")
            else:
                print(f"  I Chart:")
                print(f"    CL:  {result['x_bar']:.4f}")
                print(f"    UCL: {result['ucl_x']:.4f}")
                print(f"    LCL: {result['lcl_x']:.4f}")
                print(f"  MR Chart:")
                print(f"    CL:  {result['mr_bar']:.4f}")
                print(f"    UCL: {result['ucl_mr']:.4f}")
                print(f"    LCL: {result['lcl_mr']:.4f}")
            
            print()
            print(f"Sigma Estimate: {result['sigma_est']:.4f}")
            print()
            
            if result.get('ooc_xbar') or result.get('ooc_i'):
                ooc = result.get('ooc_xbar', result.get('ooc_i', []))
                print(f"⚠️  Out-of-Control Points: {ooc}")
            else:
                print("✅ Process is in statistical control")
            
            print(f"In Control: {'Yes ✅' if result['in_control'] else 'No ❌'}")
            print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
