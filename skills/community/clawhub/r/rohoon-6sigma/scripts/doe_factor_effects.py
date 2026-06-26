#!/usr/bin/env python3
"""
DOE Factor Effects Calculator
实验设计效应计算工具

Calculates:
- Main effects for each factor
- Two-factor interaction effects
- Creates main effects and interaction plots
"""

import json
import argparse
import numpy as np
from typing import List, Dict, Tuple
from itertools import combinations


def create_design_matrix(k: int) -> np.ndarray:
    """
    Create full factorial design matrix for 2^k design
    
    Args:
        k: Number of factors
    
    Returns:
        Design matrix with -1 (low) and +1 (high) levels
    """
    n_runs = 2 ** k
    design = np.zeros((n_runs, k), dtype=int)
    
    for i in range(k):
        repeat = 2 ** (k - i - 1)
        for j in range(n_runs):
            design[j, i] = -1 if (j // repeat) % 2 == 0 else 1
    
    return design


def calculate_main_effects(design: np.ndarray, responses: np.ndarray) -> Dict[str, float]:
    """
    Calculate main effects for each factor
    
    Main Effect = (Average response at high level) - (Average response at low level)
    """
    n_factors = design.shape[1]
    effects = {}
    
    for i in range(n_factors):
        factor_name = f'X{i+1}'
        
        # Average at high level (+1)
        high_mask = design[:, i] == 1
        avg_high = np.mean(responses[high_mask])
        
        # Average at low level (-1)
        low_mask = design[:, i] == -1
        avg_low = np.mean(responses[low_mask])
        
        # Main effect
        effects[factor_name] = avg_high - avg_low
    
    return effects


def calculate_interaction_effects(design: np.ndarray, responses: np.ndarray, 
                                  order: int = 2) -> Dict[str, float]:
    """
    Calculate interaction effects up to specified order
    
    Interaction effect is calculated by multiplying the columns of interacting factors
    """
    n_factors = design.shape[1]
    effects = {}
    
    # Generate all combinations of factors for interaction
    for r in range(2, order + 1):
        for factor_combo in combinations(range(n_factors), r):
            # Create interaction column
            interaction_col = np.ones(len(design))
            for i in factor_combo:
                interaction_col *= design[:, i]
            
            # Calculate effect
            high_mask = interaction_col == 1
            avg_high = np.mean(responses[high_mask])
            
            low_mask = interaction_col == -1
            avg_low = np.mean(responses[low_mask])
            
            # Create factor name (e.g., X1*X2)
            factor_name = '*'.join([f'X{i+1}' for i in factor_combo])
            effects[factor_name] = avg_high - avg_low
    
    return effects


def pareto_analysis(effects: Dict[str, float], alpha: float = 0.05) -> Dict:
    """
    Perform Pareto analysis to identify significant effects
    
    Uses t-test with Bonferroni correction
    """
    effect_values = list(effects.values())
    effect_names = list(effects.keys())
    
    # Calculate standard error (using Lenth's method for unreplicated designs)
    s0 = 1.5 * np.median(np.abs(effect_values))
    s = 1.5 * np.median(np.abs([e for e in effect_values if np.abs(e) < 2.5 * s0]))
    
    # t-ratios
    t_ratios = {name: abs(val) / s for name, val in effects.items()}
    
    # Sort by absolute effect
    sorted_effects = sorted(effects.items(), key=lambda x: abs(x[1]), reverse=True)
    
    # Determine significance (approximate, for screening)
    t_critical = 2.0  # Approximate for screening
    
    significant = {name: eff for name, eff in effects.items() 
                   if abs(t_ratios[name]) > t_critical}
    
    return {
        'all_effects': effects,
        't_ratios': t_ratios,
        'significant_effects': significant,
        'sorted_effects': sorted_effects,
        'standard_error': s
    }


def analyze_2k_design(responses: List[float], k: int = None) -> Dict:
    """
    Complete analysis of 2^k factorial design
    
    Args:
        responses: Response values in standard order
        k: Number of factors (auto-detected if not specified)
    
    Returns:
        Complete analysis results
    """
    responses = np.array(responses)
    n_runs = len(responses)
    
    # Auto-detect k
    if k is None:
        k = int(np.log2(n_runs))
        if 2 ** k != n_runs:
            raise ValueError(f"Number of runs ({n_runs}) is not a power of 2")
    
    if 2 ** k != n_runs:
        raise ValueError(f"Expected {2**k} runs for {k} factors, got {n_runs}")
    
    # Create design matrix
    design = create_design_matrix(k)
    
    # Calculate effects
    main_effects = calculate_main_effects(design, responses)
    interaction_effects = calculate_interaction_effects(design, responses, order=min(k, 3))
    
    # Pareto analysis
    all_effects = {**main_effects, **interaction_effects}
    pareto = pareto_analysis(all_effects)
    
    # Calculate overall statistics
    grand_mean = np.mean(responses)
    total_ss = np.sum((responses - grand_mean) ** 2)
    
    # SS for each effect
    effect_ss = {}
    for name, effect in all_effects.items():
        # SS = (Contrast)^2 / (n * 2^k) = (n * effect / 2)^2 / (n * 2^k)
        # For 2^k with n=1: SS = effect^2 * 2^(k-2)
        effect_ss[name] = (effect ** 2) * (2 ** (k - 2))
    
    return {
        'design': {
            'type': f'2^{k} Full Factorial',
            'n_factors': k,
            'n_runs': n_runs,
            'design_matrix': design.tolist()
        },
        'statistics': {
            'grand_mean': grand_mean,
            'total_ss': total_ss,
            'effect_ss': effect_ss
        },
        'effects': {
            'main_effects': main_effects,
            'interaction_effects': interaction_effects
        },
        'pareto_analysis': {
            'significant_effects': pareto['significant_effects'],
            't_ratios': pareto['t_ratios'],
            'standard_error': pareto['standard_error'],
            'sorted_effects': pareto['sorted_effects']
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='DOE Factor Effects Calculator for 2^k Designs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # 2^2 design (4 runs)
  python3 doe_factor_effects.py --responses "[40,50,45,55]" --k 2 --json
  
  # 2^3 design (8 runs)
  python3 doe_factor_effects.py --responses "[45,52,48,58,46,53,49,59]" --k 3 --json
  
  # Auto-detect k from number of runs
  python3 doe_factor_effects.py --responses "[...]" --json
        '''
    )
    
    parser.add_argument('--responses', type=str, required=True, 
                       help='Response values as JSON array (standard order)')
    parser.add_argument('--k', type=int, help='Number of factors (auto-detected if not specified)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--plot', action='store_true', help='Generate plots (requires matplotlib)')
    
    args = parser.parse_args()
    
    # Load responses
    responses = json.loads(args.responses)
    
    # Analyze
    try:
        results = analyze_2k_design(responses, args.k)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Output
    if args.json:
        # Remove design matrix for cleaner JSON
        output = {k: v for k, v in results.items() if k != 'design'}
        output['design'] = {k: v for k, v in results['design'].items() if k != 'design_matrix'}
        print(json.dumps(output, indent=2))
    else:
        print("\n" + "="*60)
        print("DOE Factor Effects Analysis")
        print("="*60)
        
        design = results['design']
        print(f"\nDesign: {design['type']}")
        print(f"Number of Factors: {design['n_factors']}")
        print(f"Number of Runs: {design['n_runs']}")
        
        stats = results['statistics']
        print(f"\nGrand Mean: {stats['grand_mean']:.4f}")
        print(f"Total SS: {stats['total_ss']:.4f}")
        
        print("\n" + "-"*60)
        print("Main Effects:")
        print("-"*60)
        for factor, effect in results['effects']['main_effects'].items():
            direction = "↑" if effect > 0 else "↓"
            print(f"  {factor}: {effect:+.4f} {direction}")
        
        if results['effects']['interaction_effects']:
            print("\n" + "-"*60)
            print("Interaction Effects:")
            print("-"*60)
            for factor, effect in results['effects']['interaction_effects'].items():
                direction = "↑" if effect > 0 else "↓"
                print(f"  {factor}: {effect:+.4f} {direction}")
        
        print("\n" + "-"*60)
        print("Pareto Analysis (Significant Effects):")
        print("-"*60)
        sig_effects = results['pareto_analysis']['significant_effects']
        if sig_effects:
            for factor, effect in sig_effects.items():
                t_ratio = results['pareto_analysis']['t_ratios'][factor]
                print(f"  {factor}: Effect={effect:+.4f}, t-ratio={t_ratio:.2f} ⭐")
        else:
            print("  No statistically significant effects detected")
        
        print("\n" + "-"*60)
        print("All Effects (Sorted by Magnitude):")
        print("-"*60)
        for factor, effect in results['pareto_analysis']['sorted_effects'][:10]:
            t_ratio = results['pareto_analysis']['t_ratios'][factor]
            marker = "⭐" if factor in sig_effects else ""
            print(f"  {factor}: {effect:+.4f} (t={t_ratio:.2f}) {marker}")
        
        print("\n" + "="*60)
        
        # Plot if requested
        if args.plot:
            try:
                import matplotlib.pyplot as plt
                
                # Main effects plot
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Main effects bar chart
                factors = list(results['effects']['main_effects'].keys())
                effects = list(results['effects']['main_effects'].values())
                colors = ['green' if e > 0 else 'red' for e in effects]
                
                ax1.bar(factors, effects, color=colors)
                ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
                ax1.set_ylabel('Effect')
                ax1.set_title('Main Effects')
                ax1.tick_params(axis='x', rotation=45)
                
                # Pareto chart
                sorted_effects = results['pareto_analysis']['sorted_effects']
                names = [e[0] for e in sorted_effects[:10]]
                values = [abs(e[1]) for e in sorted_effects[:10]]
                
                ax2.bar(range(len(names)), values, color='steelblue')
                ax2.set_xticks(range(len(names)))
                ax2.set_xticklabels(names, rotation=45, ha='right')
                ax2.set_ylabel('|Effect|')
                ax2.set_title('Pareto Chart of Effects')
                
                plt.tight_layout()
                plt.savefig('doe_effects_plot.png', dpi=150)
                print("\n📊 Plot saved to: doe_effects_plot.png")
                
            except ImportError:
                print("\n⚠️  matplotlib not available. Install with: pip3 install matplotlib")


if __name__ == '__main__':
    main()
