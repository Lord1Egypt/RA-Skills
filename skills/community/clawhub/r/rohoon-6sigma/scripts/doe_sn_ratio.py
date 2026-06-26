#!/usr/bin/env python3
"""
Taguchi Signal-to-Noise (S/N) Ratio Calculator
田口方法信噪比计算工具

S/N Ratios:
- Larger-is-better: Maximize response
- Smaller-is-better: Minimize response
- Nominal-is-best: Target a specific value
"""

import json
import argparse
import numpy as np
from typing import List, Dict, Tuple


def sn_larger_is_better(responses: np.ndarray) -> float:
    """
    Larger-is-better S/N ratio
    望大特性 (越大越好)
    
    Formula: S/N = -10 * log10(Σ(1/y²)/n)
    
    Used for: Strength, yield, efficiency
    """
    n = len(responses)
    sum_inv_sq = np.sum(1 / (responses ** 2))
    sn = -10 * np.log10(sum_inv_sq / n)
    return sn


def sn_smaller_is_better(responses: np.ndarray) -> float:
    """
    Smaller-is-better S/N ratio
    望小特性 (越小越好)
    
    Formula: S/N = -10 * log10(Σy²/n)
    
    Used for: Defects, wear, shrinkage
    """
    n = len(responses)
    sum_sq = np.sum(responses ** 2)
    sn = -10 * np.log10(sum_sq / n)
    return sn


def sn_nominal_is_best(responses: np.ndarray, target: float = None) -> float:
    """
    Nominal-is-best S/N ratio
    望目特性 (越接近目标值越好)
    
    Formula: S/N = 10 * log10(ȳ²/s²)
    
    Used for: Dimensions, voltage, pressure
    
    Args:
        responses: Response values
        target: Target value (optional, uses mean if not specified)
    """
    mean = np.mean(responses)
    variance = np.var(responses, ddof=1)
    
    if variance == 0:
        return float('inf')  # Perfect consistency
    
    # Taguchi's nominal-is-best S/N
    sn = 10 * np.log10((mean ** 2) / variance)
    return sn


def calculate_sn_for_all_trials(data: Dict[str, List[float]], 
                                 sn_type: str, 
                                 target: float = None) -> Dict[str, float]:
    """
    Calculate S/N ratios for all trials
    
    Args:
        data: Dictionary with trial names and response arrays
        sn_type: 'larger', 'smaller', or 'nominal'
        target: Target value for nominal-is-best
    
    Returns:
        S/N ratios for each trial
    """
    sn_ratios = {}
    
    for trial_name, responses in data.items():
        responses = np.array(responses)
        
        if sn_type == 'larger':
            sn = sn_larger_is_better(responses)
        elif sn_type == 'smaller':
            sn = sn_smaller_is_better(responses)
        elif sn_type == 'nominal':
            sn = sn_nominal_is_best(responses, target)
        else:
            raise ValueError(f"Unknown S/N type: {sn_type}")
        
        sn_ratios[trial_name] = sn
    
    return sn_ratios


def analyze_orthogonal_array(trial_data: Dict, 
                              factor_settings: Dict[str, Dict],
                              sn_ratios: Dict[str, float]) -> Dict:
    """
    Analyze orthogonal array experiment results
    
    Args:
        trial_data: Original response data for each trial
        factor_settings: Factor levels for each trial
        sn_ratios: Calculated S/N ratios
    
    Returns:
        Analysis results with main effects and optimal settings
    """
    # Calculate average S/N for each factor level
    factors = list(factor_settings.keys())
    factor_effects = {}
    
    for factor in factors:
        levels = factor_settings[factor]
        level_sn = {}
        
        # Get unique levels
        unique_levels = sorted(set(levels.values()))
        
        for level in unique_levels:
            # Find trials with this factor at this level
            trials_at_level = [trial for trial, lvl in levels.items() if lvl == level]
            
            # Average S/N at this level
            avg_sn = np.mean([sn_ratios[trial] for trial in trials_at_level])
            level_sn[f'{factor}_L{level}'] = avg_sn
        
        factor_effects[factor] = level_sn
    
    # Determine optimal settings (maximize S/N)
    optimal_settings = {}
    for factor in factors:
        level_sn = {k: v for k, v in factor_effects[factor].items() if k.startswith(factor)}
        optimal_level = max(level_sn, key=level_sn.get)
        optimal_settings[factor] = optimal_level
    
    # Calculate predicted optimal S/N
    grand_avg = np.mean(list(sn_ratios.values()))
    predicted_sn = grand_avg
    for factor in factors:
        optimal_level = optimal_settings[factor]
        level_avg = factor_effects[factor][optimal_level]
        predicted_sn += (level_avg - grand_avg)
    
    return {
        'factor_effects': factor_effects,
        'optimal_settings': optimal_settings,
        'predicted_optimal_sn': predicted_sn,
        'current_best_sn': max(sn_ratios.values()),
        'current_best_trial': max(sn_ratios, key=sn_ratios.get)
    }


def main():
    parser = argparse.ArgumentParser(
        description='Taguchi Signal-to-Noise (S/N) Ratio Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Larger-is-better (e.g., strength)
  python3 doe_sn_ratio.py --responses "[45,52,48,58,46,53,49,59]" --type larger --json
  
  # Smaller-is-better (e.g., defects)
  python3 doe_sn_ratio.py --responses "[2,1,3,1,2,1,2,1]" --type smaller --json
  
  # Nominal-is-best (e.g., dimension with target 10.0)
  python3 doe_sn_ratio.py --responses "[9.8,10.2,10.1,9.9,10.0,10.1,9.9,10.0]" --type nominal --target 10.0 --json
  
  # Full orthogonal array analysis
  python3 doe_sn_ratio.py --data '{"trial1":[45,46,47],"trial2":[52,51,53],...}' --settings '{"A":{"trial1":1,"trial2":1,...},"B":{...}}' --type larger
        '''
    )
    
    parser.add_argument('--responses', type=str, help='Response values as JSON array')
    parser.add_argument('--data', type=str, help='Multiple trials data as JSON object')
    parser.add_argument('--type', choices=['larger', 'smaller', 'nominal'], 
                       required=True, help='S/N ratio type')
    parser.add_argument('--target', type=float, help='Target value for nominal-is-best')
    parser.add_argument('--settings', type=str, help='Factor settings for orthogonal array analysis')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Single trial or multiple trials
    if args.data:
        # Multiple trials (orthogonal array)
        trial_data = json.loads(args.data)
        
        # Calculate S/N for each trial
        sn_ratios = calculate_sn_for_all_trials(trial_data, args.type, args.target)
        
        # Orthogonal array analysis if settings provided
        if args.settings:
            factor_settings = json.loads(args.settings)
            analysis = analyze_orthogonal_array(trial_data, factor_settings, sn_ratios)
            
            results = {
                'sn_type': args.type,
                'target': args.target,
                'trials': list(trial_data.keys()),
                'sn_ratios': sn_ratios,
                'analysis': analysis
            }
        else:
            results = {
                'sn_type': args.type,
                'target': args.target,
                'trials': list(trial_data.keys()),
                'sn_ratios': sn_ratios
            }
    
    elif args.responses:
        # Single set of responses
        responses = np.array(json.loads(args.responses))
        
        if args.type == 'larger':
            sn = sn_larger_is_better(responses)
            formula = 'S/N = -10 * log10(Σ(1/y²)/n)'
        elif args.type == 'smaller':
            sn = sn_smaller_is_better(responses)
            formula = 'S/N = -10 * log10(Σy²/n)'
        elif args.type == 'nominal':
            sn = sn_nominal_is_best(responses, args.target)
            formula = 'S/N = 10 * log10(ȳ²/s²)'
        
        results = {
            'sn_type': args.type,
            'target': args.target,
            'n_samples': len(responses),
            'mean': float(np.mean(responses)),
            'std': float(np.std(responses, ddof=1)),
            'sn_ratio': sn,
            'formula': formula
        }
    else:
        parser.error('Must specify --responses or --data')
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*60)
        print("Taguchi Signal-to-Noise (S/N) Ratio Analysis")
        print("="*60)
        
        if 'trials' in results:
            # Multiple trials
            print(f"\nS/N Type: {results['sn_type']}")
            if results['target']:
                print(f"Target: {results['target']}")
            
            print(f"\nNumber of Trials: {len(results['trials'])}")
            
            print("\n" + "-"*60)
            print("S/N Ratios by Trial:")
            print("-"*60)
            for trial, sn in results['sn_ratios'].items():
                print(f"  {trial}: {sn:.4f} dB")
            
            if 'analysis' in results:
                analysis = results['analysis']
                
                print("\n" + "-"*60)
                print("Factor Effects (Average S/N by Level):")
                print("-"*60)
                for factor, level_sn in analysis['factor_effects'].items():
                    print(f"\n  {factor}:")
                    for level, sn in level_sn.items():
                        print(f"    {level}: {sn:.4f} dB")
                
                print("\n" + "-"*60)
                print("Optimal Settings (Maximize S/N):")
                print("-"*60)
                for factor, level in analysis['optimal_settings'].items():
                    print(f"  {factor}: {level}")
                
                print(f"\n  Current Best Trial: {analysis['current_best_trial']} ({analysis['current_best_sn']:.4f} dB)")
                print(f"  Predicted Optimal S/N: {analysis['predicted_optimal_sn']:.4f} dB")
                print(f"  Expected Improvement: {analysis['predicted_optimal_sn'] - analysis['current_best_sn']:.4f} dB")
        
        else:
            # Single trial
            print(f"\nS/N Type: {results['sn_type']}")
            if results['target']:
                print(f"Target: {results['target']}")
            
            print(f"\nSample Size: {results['n_samples']}")
            print(f"Mean: {results['mean']:.4f}")
            print(f"Std Dev: {results['std']:.4f}")
            
            print("\n" + "-"*60)
            print("S/N Ratio:")
            print("-"*60)
            print(f"  S/N = {results['sn_ratio']:.4f} dB")
            print(f"  Formula: {results['formula']}")
            
            # Interpretation
            print("\n" + "-"*60)
            print("Interpretation:")
            print("-"*60)
            if results['sn_type'] == 'larger':
                print("  Higher S/N = Better (maximize response)")
            elif results['sn_type'] == 'smaller':
                print("  Higher S/N = Better (minimize response)")
            elif results['sn_type'] == 'nominal':
                print("  Higher S/N = Better (closer to target, less variation)")
        
        print("\n" + "="*60)


if __name__ == '__main__':
    main()
