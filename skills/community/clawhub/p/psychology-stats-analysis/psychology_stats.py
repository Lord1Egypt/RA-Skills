"""
Psychology Statistical Analysis Module
Comprehensive statistical toolkit for psychological research
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Union, Optional
import json


class PsychologyAnalyzer:
    """Main analyzer class for psychological statistical analysis"""
    
    def __init__(self):
        self.results = {}
    
    # ============ Descriptive Statistics ============
    
    def descriptive_stats(self, data: Union[list, np.ndarray, pd.Series], 
                         by_group: Optional[str] = None,
                         decimals: int = 4) -> Dict:
        """
        Calculate comprehensive descriptive statistics
        
        Parameters:
        -----------
        data : array-like
            Input data
        by_group : str, optional
            Column name for grouping (if data is DataFrame)
        decimals : int
            Decimal places for rounding
        
        Returns:
        --------
        dict : Dictionary with statistics including mean, SD, SE, min, max, etc.
        """
        if isinstance(data, pd.DataFrame) and by_group:
            return {
                group: self._compute_descriptives(group_data, decimals)
                for group, group_data in data.groupby(by_group)[data.columns[0]]
            }
        else:
            return self._compute_descriptives(data, decimals)
    
    def _compute_descriptives(self, data: np.ndarray, decimals: int = 4) -> Dict:
        """Helper method to compute descriptive statistics"""
        data = np.array(data)
        data_clean = data[~np.isnan(data)]
        
        n = len(data_clean)
        mean = np.mean(data_clean)
        sd = np.std(data_clean, ddof=1)
        se = sd / np.sqrt(n) if n > 1 else np.nan
        
        return {
            'n': int(n),
            'mean': round(mean, decimals),
            'sd': round(sd, decimals),
            'se': round(se, decimals),
            'min': round(np.min(data_clean), decimals),
            'max': round(np.max(data_clean), decimals),
            'median': round(np.median(data_clean), decimals),
            'q1': round(np.percentile(data_clean, 25), decimals),
            'q3': round(np.percentile(data_clean, 75), decimals),
            'iqr': round(np.percentile(data_clean, 75) - np.percentile(data_clean, 25), decimals)
        }
    
    # ============ Hypothesis Testing ============
    
    def independent_t_test(self, group1: np.ndarray, group2: np.ndarray,
                          equal_var: bool = True) -> Dict:
        """
        Independent samples t-test
        
        Returns Cohen's d and statistical significance
        """
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=equal_var)
        cohens_d = self._cohens_d(group1, group2)
        
        return {
            't_statistic': round(t_stat, 4),
            'p_value': round(p_value, 4),
            'significant': p_value < 0.05,
            'cohens_d': round(cohens_d, 4),
            'effect_size_interpretation': self._interpret_cohens_d(cohens_d)
        }
    
    def paired_t_test(self, before: np.ndarray, after: np.ndarray) -> Dict:
        """Paired samples t-test"""
        t_stat, p_value = stats.ttest_rel(before, after)
        differences = np.array(after) - np.array(before)
        cohens_d = np.mean(differences) / np.std(differences, ddof=1)
        
        return {
            't_statistic': round(t_stat, 4),
            'p_value': round(p_value, 4),
            'significant': p_value < 0.05,
            'cohens_d': round(cohens_d, 4),
            'mean_difference': round(np.mean(differences), 4),
            'effect_size_interpretation': self._interpret_cohens_d(cohens_d)
        }
    
    def one_way_anova(self, *groups) -> Dict:
        """
        One-way ANOVA for multiple groups
        """
        f_stat, p_value = stats.f_oneway(*groups)
        
        # Calculate eta-squared (effect size)
        all_data = np.concatenate(groups)
        grand_mean = np.mean(all_data)
        ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
        ss_total = sum((x - grand_mean)**2 for x in all_data)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        return {
            'f_statistic': round(f_stat, 4),
            'p_value': round(p_value, 4),
            'significant': p_value < 0.05,
            'eta_squared': round(eta_squared, 4),
            'effect_size_interpretation': self._interpret_eta_squared(eta_squared),
            'num_groups': len(groups)
        }
    
    def correlation_analysis(self, x: np.ndarray, y: np.ndarray) -> Dict:
        """
        Pearson correlation analysis
        """
        r, p_value = stats.pearsonr(x, y)
        r_squared = r**2
        
        return {
            'pearson_r': round(r, 4),
            'p_value': round(p_value, 4),
            'significant': p_value < 0.05,
            'r_squared': round(r_squared, 4),
            'effect_size_interpretation': self._interpret_correlation(abs(r))
        }
    
    # ============ Effect Size Utilities ============
    
    def _cohens_d(self, group1: np.ndarray, group2: np.ndarray) -> float:
        """Calculate Cohen's d"""
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1 + n2 - 2))
        return (np.mean(group1) - np.mean(group2)) / pooled_std if pooled_std > 0 else 0
    
    def _interpret_cohens_d(self, d: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
    
    def _interpret_eta_squared(self, eta2: float) -> str:
        """Interpret eta-squared effect size"""
        if eta2 < 0.01:
            return "negligible"
        elif eta2 < 0.06:
            return "small"
        elif eta2 < 0.14:
            return "medium"
        else:
            return "large"
    
    def _interpret_correlation(self, r: float) -> str:
        """Interpret correlation strength"""
        if r < 0.1:
            return "negligible"
        elif r < 0.3:
            return "small"
        elif r < 0.5:
            return "medium"
        else:
            return "large"
    
    # ============ Power Analysis ============
    
    def power_analysis_ttest(self, effect_size: float = 0.5, 
                            alpha: float = 0.05, power: float = 0.8) -> Dict:
        """
        Estimate sample size needed for t-test
        Based on Cohen's effect size conventions
        """
        # Approximate formula for independent t-test
        # n = 2 * (z_alpha + z_beta)^2 / d^2
        from scipy.stats import norm
        z_alpha = norm.ppf(1 - alpha/2)
        z_beta = norm.ppf(power)
        n_per_group = 2 * ((z_alpha + z_beta) / effect_size) ** 2
        
        return {
            'n_per_group': int(np.ceil(n_per_group)),
            'total_n': int(np.ceil(2 * n_per_group)),
            'effect_size': effect_size,
            'alpha': alpha,
            'power': power,
            'note': 'For independent samples t-test, two-tailed'
        }
    
    # ============ Data Validation ============
    
    def check_normality(self, data: np.ndarray, test: str = 'shapiro') -> Dict:
        """
        Test for normality (Shapiro-Wilk or Kolmogorov-Smirnov)
        """
        data_clean = np.array(data)[~np.isnan(data)]
        
        if test == 'shapiro':
            stat, p_value = stats.shapiro(data_clean)
            test_name = 'Shapiro-Wilk'
        else:
            stat, p_value = stats.kstest(data_clean, 'norm', 
                                        args=(np.mean(data_clean), np.std(data_clean)))
            test_name = 'Kolmogorov-Smirnov'
        
        return {
            'test': test_name,
            'statistic': round(stat, 4),
            'p_value': round(p_value, 4),
            'normal': p_value > 0.05,
            'note': 'p > 0.05 suggests data is approximately normal'
        }
    
    def check_homogeneity_variance(self, *groups) -> Dict:
        """
        Levene's test for homogeneity of variance
        """
        stat, p_value = stats.levene(*groups)
        
        return {
            'test': 'Levene Test',
            'statistic': round(stat, 4),
            'p_value': round(p_value, 4),
            'homogeneous': p_value > 0.05,
            'note': 'p > 0.05 suggests equal variances across groups'
        }


# ============ Example Usage ============

if __name__ == "__main__":
    analyzer = PsychologyAnalyzer()
    
    # Example: gaze-cueing experiment data
    congruent_rt = [450, 460, 455, 470, 465, 458, 462, 468, 455, 460]
    incongruent_rt = [480, 495, 490, 505, 500, 492, 498, 510, 488, 502]
    
    # Descriptive statistics
    stats_result = analyzer.independent_t_test(
        np.array(congruent_rt), 
        np.array(incongruent_rt)
    )
    print("Independent t-test result:")
    print(json.dumps(stats_result, indent=2))
