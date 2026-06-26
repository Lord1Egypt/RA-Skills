#!/usr/bin/env python3
"""
DOE Full Factorial Design Tool
2^k full factorial designs with analysis

Usage:
    python3 doe_full_factorial.py --factors 2 --responses "[40,50,45,55]" --analyze
    python3 doe_full_factorial.py --factors 3 --responses "[45,52,48,58,46,53,49,59]" --seed 42
"""

import argparse
import json
import sys
import numpy as np
from scipy import stats
from itertools import product
from typing import List, Dict, Any


def generate_full_factorial(k: int) -> np.ndarray:
    """Generate 2^k full factorial design matrix"""
    levels = [-1, 1]
    design = np.array(list(product(levels, repeat=k)))
    return design


def calculate_effects(
    design: np.ndarray,
    responses: np.ndarray
) -> Dict[str, float]:
    """Calculate main effects and interactions"""
    n = len(responses)
    k = design.shape[1]
    
    effects = {}
    
    # Main effects
    for i in range(k):
        factor_name = f"A{i+1}"
        contrast = np.sum(design[:, i] * responses)
        effect = (2 / n) * contrast
        effects[factor_name] = float(effect)
    
    # Two-factor interactions
    if k >= 2:
        for i in range(k):
            for j in range(i+1, k):
                interaction = design[:, i] * design[:, j]
                factor_name = f"A{i+1}A{j+1}"
                contrast = np.sum(interaction * responses)
                effect = (2 / n) * contrast
                effects[factor_name] = float(effect)
    
    return effects


def calculate_anova(
    design: np.ndarray,
    responses: np.ndarray
) -> Dict[str, Any]:
    """Perform ANOVA analysis"""
    n = len(responses)
    k = design.shape[1]
    
    # Total sum of squares
    ss_total = np.sum((responses - np.mean(responses))**2)
    
    # Calculate sum of squares for each effect
    effects = calculate_effects(design, responses)
    ss_effects = {}
    for name, effect in effects.items():
        ss_effects[name] = (n / 4) * effect**2
    
    # Error (residual)
    ss_model = sum(ss_effects.values())
    ss_error = ss_total - ss_model
    df_error = n - 1 - len(effects)
    
    # Mean squares
    ms_effects = {name: ss for name, ss in ss_effects.items()}
    ms_error = ss_error / df_error if df_error > 0 else 0
    
    # F-values and p-values
    results = {}
    for name, ms in ms_effects.items():
        f_val = ms / ms_error if ms_error > 0 else 0
        p_val = 1 - stats.f.cdf(f_val, 1, df_error) if df_error > 0 else 1
        results[name] = {
            'effect': effects[name],
            'ss': ss_effects[name],
            'ms': ms,
            'f': f_val,
            'p': p_val,
            'significant': p_val < 0.05
        }
    
    return {
        'effects': results,
        'ss_total': ss_total,
        'ss_error': ss_error,
        'df_error': df_error,
        'ms_error': ms_error
    }


def main():
    parser = argparse.ArgumentParser(
        description='DOE Full Factorial Design (2^k)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # 2^2 factorial design
  python3 doe_full_factorial.py --factors 2 --responses "[40,50,45,55]" --analyze
  
  # 2^3 factorial design
  python3 doe_full_factorial.py --factors 3 --responses "[45,52,48,58,46,53,49,59]" --seed 42
        '''
    )
    
    parser.add_argument('--factors', '-k', type=int, required=True,
                       help='Number of factors (2-8)')
    parser.add_argument('--responses', '-y', type=str, required=True,
                       help='Response values (JSON array or comma-separated)')
    parser.add_argument('--factor-names', '-n', type=str, default=None,
                       help='Factor names (comma-separated)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for randomization')
    parser.add_argument('--analyze', '-a', action='store_true',
                       help='Perform ANOVA analysis')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        # Validate factors
        if args.factors < 1 or args.factors > 8:
            raise ValueError("Number of factors must be 1-8")
        
        # Parse responses
        try:
            responses = np.array(json.loads(args.responses))
        except:
            responses = np.array([float(x.strip()) for x in args.responses.split(',')])
        
        # Validate response count
        n_expected = 2 ** args.factors
        if len(responses) != n_expected:
            raise ValueError(f"Expected {n_expected} responses for {args.factors} factors, got {len(responses)}")
        
        # Generate design
        design = generate_full_factorial(args.factors)
        
        # Get factor names
        if args.factor_names:
            factor_names = [f.strip() for f in args.factor_names.split(',')]
        else:
            factor_names = [f"A{i+1}" for i in range(args.factors)]
        
        # Calculate effects
        effects = calculate_effects(design, responses)
        
        # Output
        if args.json:
            result = {
                'design_type': f'2^{args.factors} Full Factorial',
                'n_factors': args.factors,
                'n_runs': len(responses),
                'factor_names': factor_names,
                'effects': effects
            }
            
            if args.analyze:
                anova = calculate_anova(design, responses)
                result['anova'] = anova
            
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print(f"2^{args.factors} Full Factorial Design")
            print("=" * 60)
            print(f"Factors: {args.factors}")
            print(f"Runs: {len(responses)}")
            print()
            
            print("Design Matrix:")
            print("-" * 60)
            header = "\t".join(["Run"] + factor_names + ["Response"])
            print(header)
            for i in range(len(responses)):
                row = "\t".join([str(i+1)] + [str(design[i,j]) for j in range(args.factors)] + [str(responses[i])])
                print(row)
            print()
            
            print("Effects Analysis:")
            print("-" * 60)
            print(f"{'Effect':<15} {'Value':>12} {'Significance':>15}")
            print("-" * 60)
            
            for name, effect in effects.items():
                sig = "**" if abs(effect) > np.std(responses) * 0.5 else ""
                print(f"{name:<15} {effect:>12.4f} {sig:>15}")
            
            if args.analyze:
                print()
                print("ANOVA Results:")
                print("-" * 60)
                anova = calculate_anova(design, responses)
                
                print(f"{'Source':<15} {'Effect':>10} {'SS':>10} {'F':>10} {'p-value':>10}")
                print("-" * 60)
                for name, result in anova['effects'].items():
                    sig = "**" if result['significant'] else ""
                    print(f"{name:<15} {result['effect']:>10.4f} {result['ss']:>10.4f} {result['f']:>10.2f} {result['p']:>10.4f} {sig}")
            
            print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
