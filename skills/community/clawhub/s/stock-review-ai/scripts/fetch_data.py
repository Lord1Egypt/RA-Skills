import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import time
import warnings
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from utils.logger import get_logger
from config import Settings

warnings.filterwarnings('ignore')

class DataFetcher:
    """Market Data Fetcher"""
    
    def __init__(self, config: Settings):
        self.config = config
        self.logger = get_logger(__name__)
    
    def get_latest_date(self) -> str:
        """Get latest available data date"""
        today = datetime.now().strftime("%Y%m%d")

        if self.config.backtrack_days <= 0:
            return today
        
        try:
            # Try to fetch data for today
            ak.stock_lhb_detail_daily_sina(date=today)
            return today
        except Exception:
            # Backtrack to find the latest valid date
            for i in range(1, self.config.backtrack_days + 1):
                check_date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
                try:
                    time.sleep(self.config.request_delay)
                    ak.stock_lhb_detail_daily_sina(date=check_date)
                    self.logger.info(f"Found latest date: {check_date} (backtracked {i} days)")
                    return check_date
                except Exception:
                    continue
            
            # default to today if no valid date found
            self.logger.warning(f"No valid data found, using today: {today}")
            return today
    
    def fetch_all(self, date: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get all market data for the specified date, with caching and retry logic
        
        Returns:
            A dictionary containing all the dataframes and summary statistics
        """
        self.logger.info(f"Fetching market data for {date}")
        
        save_dir = self.config.data_dir / date
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # check cache
        # if not force_refresh:
        #     cached_data = self._load_cached_data(date, save_dir)
        #     if cached_data is not None:
        #         self.logger.info(f"Using cached data for {date}")
        #         return cached_data
        
        # get data
        data = {}
        
        # 1. index data
        data['index'] = self._fetch_index(date, save_dir)
        
        # 2. limit up/down and special treatment stocks
        data['zt'], data['dt'], data['zb'] = self._fetch_zt_dt(date, save_dir)
        
        # 3. all stocks data and summary statistics
        data['all_stocks'], data['up_count'], data['down_count'], _ = self._fetch_all_stocks(date, save_dir)
        
        # 4. top amount stocks
        data['top_amount'] = self._fetch_top_amount(data['all_stocks'], date, save_dir)
        
        # 5. concept板块
        data['concept'] = self._fetch_concept(date, save_dir)
        
        # 6. concept cons, only for top 5 concepts
        data['concept_cons'] = self._fetch_concept_cons(data['concept'], date, save_dir)
        
        # 7. lhb data
        data['lhb'] = self._fetch_lhb(date, save_dir)
        
        # 8. Watchlist
        data['watchlist1'], data['watchlist2'] = self._create_watchlist(data, date, save_dir)
        
        self.logger.info(f"Data fetching completed for {date}")
        return data
    
    def _load_cached_data(self, date: str, save_dir: Path) -> Optional[Dict]:
        """Load cached data if all key files exist, otherwise return None"""
        required_files = [
            f"index_{date}.csv",
            f"A_stock_{date}.csv",
            f"zt_pool_{date}.csv",
            f"dt_pool_{date}.csv",
            f"zb_pool_{date}.csv",
            f"lhb_{date}.csv",
            f"top_amount_stocks_{date}.csv"
        ]
        
        for file in required_files:
            if not (save_dir / file).exists():
                return None
        
        return {'cached': True, 'date': date}
    
    def _fetch_index(self, date: str, save_dir: Path) -> pd.DataFrame:
        """Get index data"""
        file_path = save_dir / f"index_{date}.csv"
        
        if file_path.exists():
            return pd.read_csv(file_path, dtype={'代码': str})
        
        try:
            index_df = ak.stock_zh_index_spot_sina()
            target_indices = ["sh000001", "sz399001"]
            result = index_df[index_df['代码'].isin(target_indices)].copy()
            
            # calculate total amount for the two indices
            result['成交额'] = pd.to_numeric(result['成交额'])
            total_amount = result['成交额'].sum()
            
            # add summary row
            summary_row = {
                '代码': 'Total',
                '名称': '沪深总成交额',
                '最新价': None,
                '成交额': total_amount,
                '涨跌幅': None
            }
            
            result = pd.concat([result, pd.DataFrame([summary_row])], ignore_index=True)
            result['成交额(亿元)'] = result['成交额'].apply(self._format_value)
            result.insert(0, '序号', range(1, len(result) + 1))
            
            result.to_csv(file_path, index=False, encoding="utf-8-sig")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to fetch index data: {e}")
            return pd.DataFrame()
    
    def _fetch_zt_dt(self, date: str, save_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Get limit up/down and special treatment stocks"""
        zt_path = save_dir / f"zt_pool_{date}.csv"
        dt_path = save_dir / f"dt_pool_{date}.csv"
        zb_path = save_dir / f"zb_pool_{date}.csv"
        
        if all(p.exists() for p in [zt_path, dt_path, zb_path]):
            return (
                pd.read_csv(zt_path),
                pd.read_csv(dt_path),
                pd.read_csv(zb_path)
            )
        
        try:
            zt_df = ak.stock_zt_pool_em(date=date)
            time.sleep(self.config.request_delay)
            dt_df = ak.stock_zt_pool_dtgc_em(date=date)
            time.sleep(self.config.request_delay)
            zb_df = ak.stock_zt_pool_zbgc_em(date=date)
            
            # format values
            for df in [zt_df, dt_df, zb_df]:
                if '成交额' in df.columns:
                    df['成交额'] = df['成交额'].apply(self._format_value)
                if '流通市值' in df.columns:
                    df['流通市值'] = df['流通市值'].apply(self._format_value)
                if '总市值' in df.columns:
                    df['总市值'] = df['总市值'].apply(self._format_value)
            
            # save
            zt_df.to_csv(zt_path, index=False, encoding="utf-8-sig")
            dt_df.to_csv(dt_path, index=False, encoding="utf-8-sig")
            zb_df.to_csv(zb_path, index=False, encoding="utf-8-sig")
            
            return zt_df, dt_df, zb_df
            
        except Exception as e:
            self.logger.error(f"Failed to fetch ZT/DT data: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    def _fetch_all_stocks(self, date: str, save_dir: Path, max_retries: int = 3) -> Tuple[pd.DataFrame, int, int, int]:
        """Get all stocks data and calculate summary statistics (up/down/flat count)"""
        file_path = save_dir / f"A_stock_{date}.csv"
        
        if file_path.exists():
            df = pd.read_csv(file_path)
        else:
            success = False
            for i in range(max_retries):
                try:
                    if i % 2 == 0:
                        df = ak.stock_zh_a_spot_em()
                    else:
                        df = ak.stock_zh_a_spot()
                    
                    if df is not None and not df.empty:
                        df.to_csv(file_path, index=False, encoding="utf-8-sig")
                        success = True
                        break
                except Exception as e:
                    self.logger.warning(f"Attempt {i+1} failed: {e}")
                    time.sleep(5)
            
            if not success:
                return pd.DataFrame(), 0, 0, 0
        
        # calculate up/down/flat count
        df['涨跌'] = df['涨跌幅'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
        up_count = df[df['涨跌'] == 1].shape[0]
        down_count = df[df['涨跌'] == -1].shape[0]
        flat_count = df[df['涨跌'] == 0].shape[0]
        
        return df, up_count, down_count, flat_count
    
    def _fetch_top_amount(self, all_stocks_df: pd.DataFrame, date: str, save_dir: Path) -> pd.DataFrame:
        """Get top 20 stocks by amount"""
        file_path = save_dir / f"top_amount_stocks_{date}.csv"
        
        if file_path.exists():
            return pd.read_csv(file_path)
        
        try:
            top_df = all_stocks_df.sort_values(by='成交额', ascending=False).head(20).copy()
            top_df['成交额(亿元)'] = top_df['成交额'].apply(self._format_value)
            top_df = top_df[['代码', '名称', '最新价', '涨跌幅', '成交额(亿元)']]
            top_df.insert(0, '序号', range(1, len(top_df) + 1))
            
            top_df.to_csv(file_path, index=False, encoding="utf-8-sig")
            return top_df
            
        except Exception as e:
            self.logger.error(f"Failed to fetch top amount stocks: {e}")
            return pd.DataFrame()
    
    def _fetch_concept(self, date: str, save_dir: Path, top_n: int = 5) -> pd.DataFrame:
        """Get concept data"""
        file_path = save_dir / f"concept_summary_{date}.csv"
        
        if file_path.exists():
            return pd.read_csv(file_path)
        
        try:
            concept_df = ak.stock_board_concept_name_em()
            concept_df['总市值'] = concept_df['总市值'].apply(self._format_value)
            concept_df = concept_df.head(top_n).copy()
            
            concept_df.to_csv(file_path, index=False, encoding="utf-8-sig")
            return concept_df
            
        except Exception as e:
            self.logger.error(f"Failed to fetch concept data: {e}")
            return pd.DataFrame()
    
    def _fetch_concept_cons(self, concept_df: pd.DataFrame, date: str, save_dir: Path) -> list:
        """Get concept cons data for top concepts"""
        if concept_df.empty:
            return []
        
        cons_list = []
        for idx, row in concept_df.iterrows():
            file_path = save_dir / f"concept_cons_{idx}_{date}.csv"
            
            if file_path.exists():
                cons_df = pd.read_csv(file_path)
            else:
                try:
                    cons_df = ak.stock_board_concept_cons_em(symbol=row['板块名称'])
                    cons_df.sort_values(by='涨跌幅', ascending=False, inplace=True)
                    cons_df['成交额'] = cons_df['成交额'].apply(self._format_value)
                    cons_df['所属板块'] = row['板块名称']
                    cons_df = cons_df.head(15).copy()
                    
                    cons_df.to_csv(file_path, index=False, encoding="utf-8-sig")
                    time.sleep(self.config.request_delay)
                    
                except Exception as e:
                    self.logger.error(f"Failed to fetch concept cons for {row['板块名称']}: {e}")
                    continue
            
            cons_list.append(cons_df)
        
        return cons_list
    
    def _fetch_lhb(self, date: str, save_dir: Path) -> pd.DataFrame:
        """Get LHB data"""
        file_path = save_dir / f"lhb_{date}.csv"
        
        if file_path.exists():
            return pd.read_csv(file_path)
        
        try:
            lhb_df = ak.stock_lhb_detail_daily_sina(date=date)
            
            # filter ST stocks
            col_name = '名称' if '名称' in lhb_df.columns else '股票名称'
            lhb_df = lhb_df[~lhb_df[col_name].str.contains('ST', case=False, na=False)].copy()
            lhb_df.drop_duplicates(subset=[col_name], inplace=True)
            lhb_df.reset_index(drop=True, inplace=True)
            if '序号' not in lhb_df.columns:
                lhb_df.insert(0, '序号', range(1, len(lhb_df) + 1))
            else:
                self.logger.debug("'序号' column already exists, skipping insertion")
            
            lhb_df.to_csv(file_path, index=False, encoding="utf-8-sig")
            return lhb_df
            
        except Exception as e:
            self.logger.error(f"Failed to fetch LHB data: {e}")
            return pd.DataFrame()
    
    def _create_watchlist(self, data: Dict, date: str, save_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Create watchlist"""
        file_path1 = save_dir / f"watchlist1_{date}.csv"
        file_path2 = save_dir / f"watchlist2_{date}.csv"
        
        if file_path1.exists() and file_path2.exists():
            return pd.read_csv(file_path1), pd.read_csv(file_path2)
        
        top_amount = data.get('top_amount', pd.DataFrame())
        zt_df = data.get('zt', pd.DataFrame())
        zb_df = data.get('zb', pd.DataFrame())
        dt_df = data.get('dt', pd.DataFrame())
        lhb_df = data.get('lhb', pd.DataFrame())
        concept_cons = data.get('concept_cons', [])
        
        if top_amount.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        # Top 5 concept members
        top_members = set()
        for df in concept_cons[:5]:
            if not df.empty:
                name_col = '名称' if '名称' in df.columns else '股票名称'
                top_members.update(df[name_col].tolist())
        
        # names in zt/dt/zb/lhb and top concept members
        zt_names = set(zt_df['名称']) if not zt_df.empty else set()
        zb_names = set(zb_df['名称']) if not zb_df.empty else set()
        dt_names = set(dt_df['名称']) if not dt_df.empty else set()
        lhb_names = set(lhb_df['名称']) if not lhb_df.empty and '名称' in lhb_df.columns else set()
        
        # Watchlist1
        w1_mask = (
            top_amount['名称'].isin(zt_names) |
            top_amount['名称'].isin(dt_names) |
            top_amount['名称'].isin(zb_names) |
            top_amount['名称'].isin(lhb_names) |
            top_amount['名称'].isin(top_members)
        )
        w1_df = top_amount[w1_mask].copy()
        
        # Watchlist2
        combined = pd.concat([zt_df, zb_df], ignore_index=True, sort=False)
        if not combined.empty:
            w2_df = combined[combined['名称'].isin(top_members)].copy()
            if '连板数' in w2_df.columns:
                w2_df['连板数'] = w2_df['连板数'].fillna(0)
        else:
            w2_df = pd.DataFrame()
        
        # save
        w1_df.to_csv(file_path1, index=False, encoding="utf-8-sig")
        w2_df.to_csv(file_path2, index=False, encoding="utf-8-sig")
        
        return w1_df, w2_df
    
    def _format_value(self, value) -> str:
        """Format value to string with unit"""
        if pd.isna(value):
            return value
        try:
            num = float(value)
            if num >= 1e8:
                return f"{num / 1e8:.2f} 亿"
            elif num >= 1e4:
                return f"{num / 1e4:.2f} 万"
            else:
                return f"{num:.2f}"
        except:
            return str(value)