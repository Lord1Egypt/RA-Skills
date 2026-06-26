#!/usr/bin/env python3
"""
Process Capability Calculator
Based on AIAG-VDA SPC Manual (Geometric Method)

Usage:
    python3 calculate_capability.py --data "10.1,10.2,10.15,..." --usl 10.5 --lsl 9.5 --json
    python3 calculate_capability.py --data "..." --usl 10.5 --json
"""

import argparse
import json
import sys
import numpy as np
from scipy import stats
from typing import Dict, Any


def parse_data(data_str: str) -> np.ndarray:
    """Parse input data string"""
    try:
        data = json.loads(data_str)
        if isinstance(data, list):
            return np.array([float(x) for x in data])
    except:
        pass
    
    try:
        return np.array([float(x.strip()) for x in data_str.split(',')])
    except:
        raise ValueError("Cannot parse data")


def calculate_capability_indices(
    data: np.ndarray,
    usl: float = None,
    lsl: float = None,
    target: float = None
) -> Dict[str, Any]:
    """
    Calculate process capability indices using geometric method (AIAG-VDA)
    
    Returns:
        Dictionary with Cp, Cpk, Pp, Ppk, and evaluation
    """
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    result = {
        'n': int(n),
        'mean': float(mean),
        'std': float(std),
        'min': float(np.min(data)),
        'max': float(np.max(data)),
    }
    
    # Calculate indices if specifications provided
    if usl is not None and lsl is not None:
        # Cp - Potential capability
        cp = (usl - lsl) / (6 * std)
        result['cp'] = float(cp)
        
        # Cpk - Actual capability
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        cpk = min(cpu, cpl)
        result['cpu'] = float(cpu)
        result['cpl'] = float(cpl)
        result['cpk'] = float(cpk)
        
        # Pp - Performance (same as Cp for sample)
        result['pp'] = float(cp)
        
        # Ppk - Performance index
        result['ppk'] = float(cpk)
        
        # Evaluation
        if cpk >= 2.0:
            rating = 'Six Sigma'
            action = 'Maintain, can relax control'
        elif cpk >= 1.67:
            rating = 'Excellent'
            action = 'Maintain current state'
        elif cpk >= 1.33:
            rating = 'Good'
            action = 'Maintain, continuous improvement'
        elif cpk >= 1.0:
            rating = 'Marginal'
            action = 'Need improvement plan'
        else:
            rating = 'Insufficient'
            action = 'Must improve, 100% inspection'
        
        result['rating'] = rating
        result['action'] = action
        result['acceptable'] = bool(cpk >= 1.33)
        
        # Add specifications
        result['usl'] = float(usl)
        result['lsl'] = float(lsl)
        if target:
            result['target'] = float(target)
    
    elif usl is not None:
        # Only upper specification
        cpu = (usl - mean) / (3 * std)
        result['cpu'] = float(cpu)
        result['cpk'] = float(cpu)
        result['usl'] = float(usl)
        
    elif lsl is not None:
        # Only lower specification
        cpl = (mean - lsl) / (3 * std)
        result['cpl'] = float(cpl)
        result['cpk'] = float(cpl)
        result['lsl'] = float(lsl)
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Process Capability Calculator (AIAG-VDA Geometric Method)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Two-sided specification
  python3 calculate_capability.py --data "10.1,10.2,10.15,..." --usl 10.5 --lsl 9.5 --json
  
  # Only upper specification
  python3 calculate_capability.py --data "..." --usl 10.5 --json
  
  # With target value
  python3 calculate_capability.py --data "..." --usl 10.5 --lsl 9.5 --target 10.0 --json
        '''
    )
    
    parser.add_argument('--data', '-d', type=str, required=True,
                       help='Measurement data (comma-separated or JSON array)')
    parser.add_argument('--usl', '-u', type=float, default=None,
                       help='Upper Specification Limit')
    parser.add_argument('--lsl', '-l', type=float, default=None,
                       help='Lower Specification Limit')
    parser.add_argument('--target', '-t', type=float, default=None,
                       help='Target value')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        # Parse data
        data = parse_data(args.data)
        
        if len(data) < 2:
            raise ValueError("At least 2 data points required")
        
        # Calculate capability
        result = calculate_capability_indices(
            data,
            usl=args.usl,
            lsl=args.lsl,
            target=args.target
        )
        
        # Output
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("Process Capability Analysis Results")
            print("=" * 60)
            print(f"Sample size: {result['n']}")
            print(f"Mean: {result['mean']:.4f}")
            print(f"Std Dev: {result['std']:.4f}")
            print(f"Min: {result['min']:.4f}")
            print(f"Max: {result['max']:.4f}")
            print()
            
            if 'cpk' in result:
                print("Capability Indices:")
                if 'cp' in result:
                    print(f"  Cp:  {result['cp']:.4f}")
                print(f"  Cpk: {result['cpk']:.4f}")
                if 'cpu' in result:
                    print(f"  CPU: {result['cpu']:.4f}")
                if 'cpl' in result:
                    print(f"  CPL: {result['cpl']:.4f}")
                print()
                print(f"Rating: {result['rating']}")
                print(f"Action: {result['action']}")
                print(f"Acceptable: {'Yes ✅' if result['acceptable'] else 'No ❌'}")
            
            print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
