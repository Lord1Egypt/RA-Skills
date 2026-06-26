from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

from utils.logger import get_logger
from config import Settings

class ReportGenerator:
    """Report Generator for Stock Review"""
    
    def __init__(self, config: Settings):
        self.config = config
        self.logger = get_logger(__name__)
    
    def create_market_summary(self, market_data: Dict, date: str) -> str:
        """
        Create market summary Markdown report
        
        Args:
            market_data: market data dictionary, can include:
                - index: DataFrame of market indices
                - zt: DataFrame of 涨停个股
                - dt: DataFrame of 跌停个股
                - zb: DataFrame of 炸板个股
                - up_count: number of 上涨个股
                - down_count: number of 下跌个股
                - top_amount: DataFrame of 成交额前二十个股
                - concept: DataFrame of 概念板块
                - concept_cons: list of DataFrame of 板块成分股
                - lhb: DataFrame of 龙虎榜
                - watchlist1: DataFrame of 大额异动池
                - watchlist2: DataFrame of 风口涨停池
            date: report date in YYYYMMDD format
            
        Returns:
           conclusion of market summary in Markdown format
        """
        save_dir = self.config.data_dir / date
        file_path = save_dir / f"market_summary_{date}.md"
        
        # if file_path.exists() and not market_data.get('cached', False):
        #     with open(file_path, 'r', encoding='utf-8') as f:
        #         return f.read()
        
        index_df = market_data.get('index', pd.DataFrame())
        zt_df = market_data.get('zt', pd.DataFrame())
        dt_df = market_data.get('dt', pd.DataFrame())
        zb_df = market_data.get('zb', pd.DataFrame())
        up_count = market_data.get('up_count', 0)
        down_count = market_data.get('down_count', 0)
        top_amount = market_data.get('top_amount', pd.DataFrame())
        concept = market_data.get('concept', pd.DataFrame())
        concept_cons = market_data.get('concept_cons', [])
        lhb_df = market_data.get('lhb', pd.DataFrame())
        w1_df = market_data.get('watchlist1', pd.DataFrame())
        w2_df = market_data.get('watchlist2', pd.DataFrame())
        
        # create report content
        content = []
        content.append(f"# A股全市场复盘 {date}\n")
        
        # market snapshot
        if index_df is not None:
            if not index_df.empty:
                content.append("## 📊 市场核心快照")
                content.append(f"- **上证指数**: {index_df.iloc[0]['最新价']:.2f} ({index_df.iloc[0]['涨跌幅']:.2f}%)")
                if len(index_df) > 2:
                    content.append(f"- **全市场成交总额**: {index_df.iloc[2]['成交额(亿元)']}")
                content.append(f"- **涨跌比**: {up_count} / {down_count}")
                content.append(f"- **涨停/跌停/炸板数**: {len(zt_df)} / {len(dt_df)} / {len(zb_df)}\n")
        else:
            content.append("## 📊 市场核心快照\n暂无数据\n")
        
        # top amount stocks
        if top_amount is not None:
            if not top_amount.empty:
                content.append("## 🔍 成交额前二十个股")
                content.append(self._df_to_markdown(top_amount))
        else:
            content.append("## 🔍 成交额前二十个股\n暂无数据\n")
        
        # concept analysis
        if concept is not None:
            if not concept.empty:
                content.append("## 🏆 概念板块分析")
                content.append("**前五概念板块**（按涨幅排序）")
                content.append(self._df_to_markdown(concept))
        else:
            content.append("## 🏆 概念板块分析\n暂无数据\n")
        
        # concept constituents
        if concept_cons is not None and len(concept_cons) > 0:
            content.append("### 各板块涨幅靠前个股")
            for i, cons_df in enumerate(concept_cons[:5]):
                if not cons_df.empty:
                    board_name = cons_df['所属板块'].iloc[0] if '所属板块' in cons_df.columns else f"板块{i+1}"
                    content.append(f"**{board_name}**")
                    content.append(self._df_to_markdown(cons_df))
        else:
            content.append("### 各板块涨幅靠前个股\n暂无数据\n")
        
        # limit up/down stocks
        if zt_df is not None:
            if not zt_df.empty:
                content.append("## 💥 涨停个股")
                content.append(self._df_to_markdown(zt_df))
        else:
            content.append("## 💥 涨停个股\n暂无数据\n")
        
        if zb_df is not None:
            if not zb_df.empty:
                content.append("## 💔 炸板个股")
                content.append(self._df_to_markdown(zb_df))
        else:
            content.append("## 💔 炸板个股\n暂无数据\n")
        
        # 龙虎榜
        if lhb_df is not None:
            if not lhb_df.empty:
                content.append("## 🚀 龙虎榜")
                content.append(self._df_to_markdown(lhb_df))
        else:
            content.append("## 🚀 龙虎榜\n暂无数据\n")
        
        # Watchlist
        if w1_df is not None:
            if not w1_df.empty:
                content.append("## ⭐ 重点个股 Watchlist")
                content.append("### 大额异动池")
                content.append(self._df_to_markdown(w1_df))
        
        if w2_df is not None:
            if not w2_df.empty:
                content.append("### 风口涨停池")
                content.append(self._df_to_markdown(w2_df))
        else:
            content.append("### 风口涨停池\n暂无数据\n")
        
        content.append("\n---\n*数据来源：AKShare*")
        
        full_content = "\n\n".join(content)
        
        # save report
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        self.logger.info(f"Market summary saved to {file_path}")
        return full_content
    
    def generate_all(self, market_data: Dict, market_summary: str, ai_analysis: Optional[str], date: str) -> Dict[str, Path]:
        """
        Generate all reports and save to files
        
        Returns:
            dictionary of report paths, e.g.:
            {
                'market_summary': Path('data/20260101/market_summary_20260101.md'),
                'ai_analysis': Path('data/20260101/ai_analysis_20260101.md')
            }
        """
        save_dir = self.config.data_dir / date
        reports = {}
        
        # market summary report has been generated
        reports['market_summary'] = save_dir / f"market_summary_{date}.md"
        
        # AI analysis report
        if ai_analysis:
            ai_path = save_dir / f"ai_analysis_{date}.md"
            with open(ai_path, 'w', encoding='utf-8') as f:
                f.write(ai_analysis)
            reports['ai_analysis'] = ai_path
        
        return reports
    
    def _df_to_markdown(self, df: pd.DataFrame) -> str:
        """
        DataFrame to Markdown table, with some formatting for better display in reports
        """
        if df.empty:
            return "暂无数据"
        
        # limit column width for better display in Markdown
        display_df = df.copy()
        for col in display_df.columns:
            if display_df[col].dtype == 'object':
                display_df[col] = display_df[col].astype(str).str[:30]
        
        return display_df.to_markdown(index=False, tablefmt="pipe")