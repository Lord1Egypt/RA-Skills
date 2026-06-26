#!/usr/bin/env python3
"""
批量重构脚本 - 用于更新所有 Python 文件中的命名
MarketPulse Insights Refactoring Script
"""

import os
import re
from pathlib import Path

# 定义替换规则
REPLACEMENTS = {
    # 核心类名
    r'\bStockData\b': 'AssetData',
    r'\bDigital AssetFundamentals\b': 'DigitalAssetMetrics',
    r'\bEarningsSurprise\b': 'EarningsPerformance',
    r'\bFundamentals\b': 'FinancialHealth',
    r'\bAnalystSentiment\b': 'ProfessionalSentiment',
    r'\bHistoricalPatterns\b': 'HistoricalBehavior',
    r'\bMarketContext\b': 'MarketEnvironment',
    r'\bSectorComparison\b': 'IndustryPosition',
    r'\bMomentumAnalysis\b': 'PriceMomentum',
    r'\bSentimentAnalysis\b': 'MarketSentiment',
    r'\bSignal\b': 'InvestmentSignal',
    
    # 主要函数
    r'\bfetch_stock_data\b': 'retrieve_market_data',
    r'\banalyze_earnings_surprise\b': 'evaluate_earnings_performance',
    r'\banalyze_fundamentals\b': 'evaluate_financial_health',
    r'\banalyze_analyst_sentiment\b': 'evaluate_professional_sentiment',
    r'\banalyze_historical_patterns\b': 'evaluate_historical_behavior',
    r'\banalyze_market_context\b': 'assess_market_environment',
    r'\banalyze_sector_performance\b': 'assess_industry_position',
    r'\banalyze_momentum\b': 'assess_price_momentum',
    r'\banalyze_sentiment\b': 'assess_market_sentiment',
    r'\banalyze_digital asset_fundamentals\b': 'evaluate_digital_asset_metrics',
    r'\bsynthesize_signal\b': 'synthesize_investment_signal',
    r'\bformat_output_text\b': 'format_text_output',
    r'\bformat_output_json\b': 'format_json_output',
    r'\bprint_portfolio_summary\b': 'display_portfolio_summary',
    r'\bgenerate_portfolio_summary\b': 'generate_portfolio_metrics',
    r'\bcalculate_portfolio_period_return\b': 'compute_portfolio_return',
    r'\bprint_\b': 'display_',
    
    # 缓存相关
    r'\b_get_cached\b': '_retrieve_cached',
    r'\b_set_cache\b': '_store_cached',
    r'\b_SENTIMENT_CACHE\b': '_ANALYSIS_CACHE',
    
    # 资产分类
    r'\bdetect_asset_type\b': 'classify_asset',
    r'\bSUPPORTED_CRYPTOS\b': 'DIGITAL_ASSET_UNIVERSE',
    r'\bCRYPTO_CATEGORIES\b': 'ASSET_CATEGORIES',
    
    # 变量名
    r'\binfo\b': 'fundamentals',
    r'\banalyst_info\b': 'analyst_data',
    r'\basset_type\b': 'asset_class',
    r'\bmarket_cap_rank\b': 'market_cap_tier',
    r'\bcategory\b': 'sector',
    r'\bexplanation\b': 'summary',
    r'\bcaveats\b': 'risk_factors',
    r'\bsupporting_points\b': 'key_highlights',
    
    # 风险检测
    r'\bGEOPOLITICAL_RISK_MAP\b': 'GEO_POLITICAL_RISK_MAP',
    r'\bcheck_sector_geopolitical_risk\b': 'assess_geopolitical_exposure',
    
    # 新闻检测
    r'\bcheck_breaking_news\b': 'scan_breaking_news',
    
    # 情绪分析子函数
    r'\bget_fear_greed_index\b': 'fetch_fear_greed_index',
    r'\bget_short_interest\b': 'fetch_short_interest',
    r'\bget_vix_term_structure\b': 'fetch_vix_term_structure',
    r'\bget_insider_activity\b': 'fetch_insider_activity',
    r'\bget_put_call_ratio\b': 'fetch_put_call_ratio',
    
    # 其他函数
    r'\bcalculate_rsi\b': 'compute_rsi',
    r'\bget_sector_etf_ticker\b': 'map_sector_to_etf',
    r'\bensure_dirs\b': 'initialize_storage',
    r'\bload_watchlist\b': 'read_watchlist',
    r'\bsave_watchlist\b': 'write_watchlist',
    r'\bget_current_price\b': 'fetch_current_price',
    r'\badd_to_watchlist\b': 'append_to_watchlist',
    r'\bremove_from_watchlist\b': 'delete_from_watchlist',
    r'\blist_watchlist\b': 'display_watchlist',
    r'\bcheck_alerts\b': 'evaluate_alerts',
    
    # 存储路径
    r'\bWATCHLIST_DIR\b': 'WATCHLIST_PATH',
    r'\bWATCHLIST_FILE\b': 'WATCHLIST_STORAGE',
    r'\bCLAWDBOT_STATE_DIR\b': 'MARKETPULSE_DATA_DIR',
    
    # 注释和字符串中的关键词
    r'MarketPulse Insights': 'MarketPulse Insights',
    r'market analysis': 'market analysis',
    r'Equities and digital assets': 'Equities and digital assets',
    r'digital asset': 'digital asset',
    r'Digital Asset': 'Digital Asset',
}

def replace_in_file(filepath: Path, dry_run: bool = True):
    """在文件中执行替换操作"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        new_content = original_content
        replacements_made = []
        
        for pattern, replacement in REPLACEMENTS.items():
            if re.search(pattern, new_content):
                new_content = re.sub(pattern, replacement, new_content)
                replacements_made.append(f"{pattern} → {replacement}")
        
        if replacements_made and not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] Updated: {filepath}")
            print(f"   Replacements: {len(replacements_made)}")
            return True
        elif replacements_made:
            print(f"[PENDING] Would update: {filepath}")
            print(f"   Changes: {len(replacements_made)}")
            for change in replacements_made[:5]:  # Show first 5
                print(f"     - {change}")
            if len(replacements_made) > 5:
                print(f"     ... and {len(replacements_made) - 5} more")
            return True
        
        return False
        
    except Exception as e:
        print(f"[ERROR] Error processing {filepath}: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("MarketPulse Insights - Batch Refactoring Tool")
    print("=" * 70)
    print()
    
    # Get script directory
    script_dir = Path(__file__).parent
    print(f"Working directory: {script_dir}")
    print()
    
    # Find all Python files
    py_files = list(script_dir.glob("*.py"))
    print(f"Found {len(py_files)} Python files:")
    for f in py_files:
        print(f"   - {f.name}")
    print()
    
    # First run dry
    print("Scanning files that need updates...")
    print("-" * 70)
    files_to_update = []
    for py_file in py_files:
        if replace_in_file(py_file, dry_run=True):
            files_to_update.append(py_file)
    
    print()
    print("-" * 70)
    print(f"Summary: {len(files_to_update)} files need updating")
    print()
    
    # Ask to continue
    if files_to_update:
        print("WARNING: This operation will modify all files. Backup recommended!")
        print("Auto-executing in 3 seconds... Press Ctrl+C to cancel")
        import time
        time.sleep(3)
        
        print()
        print("Executing replacements...")
        print("-" * 70)
        updated_count = 0
        for py_file in files_to_update:
            if replace_in_file(py_file, dry_run=False):
                updated_count += 1
        
        print()
        print("=" * 70)
        print(f"Complete! Updated {updated_count} files")
        print("=" * 70)
    else:
        print("No files need updating")

if __name__ == "__main__":
    main()
