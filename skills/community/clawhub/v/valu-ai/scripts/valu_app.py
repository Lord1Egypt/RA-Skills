"""
ValU AI - Stock Valuation Analyzer with Industry Data
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from valu_config import get_config, get_logger
from valu_logger import get_log
from valu_pricing import UserQuotaManager
from valu_batch_compare import StockComparator, compare_stocks

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False

try:
    import baostock as bs
    BAOSTOCK_AVAILABLE = True
except ImportError:
    BAOSTOCK_AVAILABLE = False

import pandas as pd
import requests
from datetime import datetime, timedelta


class StockDataService:
    def __init__(self):
        self.config = get_config()
        self.log = get_log("DataService")
        self.baostock_available = BAOSTOCK_AVAILABLE
        self.baostock_connected = False
        if self.baostock_available:
            self._init_baostock()

    def _init_baostock(self):
        try:
            lg = bs.login()
            if lg.error_code == '0':
                self.baostock_connected = True
                self.log.info("Baostock connected")
        except Exception as e:
            self.log.error(f"Baostock init error: {e}")

    def _format_date(self, date_str: str) -> str:
        if len(date_str) == 8 and date_str.isdigit():
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        return date_str

    def _is_hk_stock(self, symbol: str) -> bool:
        """判断是否为港股"""
        s = symbol.lower().strip()
        if s.startswith('hk'):
            return True
        # 纯数字5位以0开头 -> 港股
        if s.isdigit() and len(s) == 5 and s.startswith('0'):
            return True
        return False

    def _bs_symbol(self, symbol: str) -> str:
        """将A股代码转为Baostock格式"""
        if symbol.startswith('6'):
            return f"sh.{symbol}"
        else:
            return f"sz.{symbol}"

    def _simplify_industry(self, industry_full: str) -> str:
        """简化证监会行业分类为常用行业名"""
        if not industry_full:
            return ''
        mappings = {
            '酒': '白酒',
            '饮料': '饮料',
            '货币金融服务': '银行',
            '保险': '保险',
            '房地产': '房地产',
            '电力': '电力',
            '热力': '电力',
            '黑色金属': '钢铁',
            '有色金属': '有色金属',
            '汽车制造业': '汽车',
            '航空运输': '航空',
            '水上运输': '港口航运',
            '道路运输': '物流',
            '通信': '通信',
            '软件': '软件',
            '电子信息': '科技',
            '半导体': '半导体',
            '医药': '医药',
            '医疗器械': '医疗器械',
            '化学原料': '化工',
            '化学制品': '化工',
            '石油': '石油',
            '天然气': '天然气',
            '煤炭': '煤炭',
            '零售': '零售',
            '批发': '零售',
            '餐饮': '餐饮',
            '食品': '食品',
            '纺织': '纺织',
            '服装': '服装',
            '教育': '教育',
            '传媒': '传媒',
            '娱乐': '娱乐',
            '证券': '证券',
            '计算机': '科技',
            '电子设备': '电子',
            '电器': '家电',
            '仪器仪表': '精密制造',
            '专用设备': '机械',
            '通用设备': '机械',
        }
        for keyword, simplified in mappings.items():
            if keyword in industry_full:
                return simplified
        # 去掉证监会代码前缀 (如 C15)
        clean = industry_full
        for prefix in ['C', 'D', 'G', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
            if clean.startswith(prefix) and len(clean) > 2 and clean[1].isdigit():
                clean = clean[2:]
                break
        return clean if clean else industry_full

    def get_historical_prices(self, symbol: str, days: int = 180) -> Dict[str, Any]:
        self.log.info(f"Fetching price data for {symbol}")
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        is_hk = self._is_hk_stock(symbol)

        result = {'symbol': symbol, 'data': None, 'source': None, 'success': False, 'error': None, 'is_hk': is_hk}

        # ===== 港股数据获取 =====
        if is_hk and AKSHARE_AVAILABLE:
            hk_symbol = symbol.lower().replace('hk', '').strip() or symbol
            try:
                df = ak.stock_hk_hist(symbol=hk_symbol, period='daily',
                    start_date=start_date, end_date=end_date, adjust='qfq')
                if df is not None and not df.empty:
                    # 重命名列以统一格式
                    df = df.rename(columns={
                        '日期': 'date', '开盘': 'open', '收盘': 'close',
                        '最高': 'high', '最低': 'low', '成交量': 'volume'
                    })
                    self.log.info(f"HK stock {hk_symbol}: {len(df)} records from akshare")
                    result.update({'data': df, 'source': 'akshare_hk', 'success': True})
                    return result
            except Exception as e:
                self.log.error(f"HK stock_hk_hist error: {e}")

        # ===== A股数据获取 =====
        if self.baostock_connected:
            try:
                bs_symbol = f"sh.{symbol}" if symbol.startswith('6') else f"sz.{symbol}"
                rs = bs.query_history_k_data_plus(
                    bs_symbol, "date,code,open,high,low,close,volume,amount,turn,pctChg",
                    start_date=self._format_date(start_date), end_date=self._format_date(end_date),
                    frequency="d", adjustflag="2"
                )
                if rs.error_code == '0':
                    data_list = []
                    while rs.error_code == '0' and rs.next():
                        data_list.append(rs.get_row_data())
                    if data_list:
                        df = pd.DataFrame(data_list, columns=rs.fields)
                        for col in ['open', 'high', 'low', 'close', 'volume', 'amount', 'turn', 'pctChg']:
                            if col in df.columns:
                                df[col] = pd.to_numeric(df[col], errors='coerce')
                        self.log.info(f"Baostock got {len(df)} records")
                        result.update({'data': df, 'source': 'baostock', 'success': True})
                        return result
            except Exception as e:
                self.log.error(f"Baostock error: {e}")

        if AKSHARE_AVAILABLE:
            try:
                df = ak.stock_zh_a_hist(symbol=symbol, period="daily",
                    start_date=start_date, end_date=end_date, adjust="qfq")
                if df is not None and not df.empty:
                    self.log.info(f"AKShare got {len(df)} records")
                    result.update({'data': df, 'source': 'akshare', 'success': True})
                    return result
            except Exception as e:
                self.log.error(f"AKShare error: {e}")

        result['error'] = "All data sources failed"
        return result

    def search_news(self, company_name: str) -> Dict[str, Any]:
        """Search for recent news about the company"""
        self.log.info(f"Searching news for {company_name}")

        result = {
            'news': [],
            'success': False,
            'error': None
        }

        if not company_name:
            return result

        try:
            # Try to get recent stock news from akshare
            if AKSHARE_AVAILABLE:
                try:
                    # Get stock news
                    news_df = ak.stock_news_em(symbol=company_name)
                    if news_df is not None and not news_df.empty:
                        news_list = []
                        for _, row in news_df.head(10).iterrows():
                            news_list.append({
                                'title': str(row.get('新闻标题', '')),
                                'datetime': str(row.get('发布时间', '')),
                                'source': str(row.get('文章来源', '')),
                                'url': str(row.get('新闻链接', ''))
                            })
                        result['news'] = news_list
                        self.log.info(f"Got {len(news_list)} news items")
                except Exception as e:
                    self.log.warning(f"News search failed: {e}")

            result['success'] = True

        except Exception as e:
            self.log.warning(f"News search error: {e}")
            result['error'] = str(e)

        return result

    def get_financial_data(self, symbol: str) -> Dict[str, Any]:
        """获取财务数据 - Baostock优先，AKShare补充"""
        self.log.info(f"Fetching financial data for {symbol}")
        result = {
            'symbol': symbol,
            'data': None,
            'source': None,
            'success': False,
            'error': None,
            'financial_indicator': None,
            'indicator_success': False,
            'baostock_data': None,
            'baostock_success': False
        }

        # ===== 方法1: Baostock获取5年财务数据（优先，最稳定） =====
        if self.baostock_connected:
            try:
                bs_symbol = self._bs_symbol(symbol)
                financial_rows = []

                # 获取5年财务数据
                for year in range(2020, 2025):
                    # 利润表
                    rs_profit = bs.query_profit_data(code=bs_symbol, year=year, quarter=4)
                    profit_row = None
                    while rs_profit.error_code == '0' and rs_profit.next():
                        profit_row = rs_profit.get_row_data()
                    if profit_row:
                        financial_rows.append({
                            'year': year,
                            'type': 'profit',
                            'roe': float(profit_row[3]) if profit_row[3] else None,
                            'net_profit_margin': float(profit_row[4]) if profit_row[4] else None,
                            'gross_profit_margin': float(profit_row[5]) if profit_row[5] else None,
                            'operating_revenue': float(profit_row[6]) if profit_row[6] else None,
                            'net_profit': float(profit_row[9]) if len(profit_row) > 9 and profit_row[9] else None,
                        })

                    # 成长能力
                    rs_growth = bs.query_growth_data(code=bs_symbol, year=year, quarter=4)
                    growth_row = None
                    while rs_growth.error_code == '0' and rs_growth.next():
                        growth_row = rs_growth.get_row_data()
                    if growth_row:
                        # 找到对应的year行并更新
                        for row in financial_rows:
                            if row['year'] == year and row['type'] == 'profit':
                                row['revenue_growth'] = float(growth_row[3]) if growth_row[3] else None
                                row['net_profit_growth'] = float(growth_row[4]) if growth_row[4] else None
                                row['nav_growth'] = float(growth_row[5]) if growth_row[5] else None
                                break

                if financial_rows:
                    # 构建汇总DataFrame
                    latest = financial_rows[-1] if financial_rows else {}
                    summary_data = {
                        '最新年度': latest.get('year', 'N/A'),
                        'ROE': latest.get('roe', 'N/A'),
                        '净利率': latest.get('net_profit_margin', 'N/A'),
                        '毛利率': latest.get('gross_profit_margin', 'N/A'),
                        '营收增长': latest.get('revenue_growth', 'N/A'),
                        '净利润增长': latest.get('net_profit_growth', 'N/A'),
                        '营收(亿)': round(latest.get('operating_revenue', 0) / 1e9, 2) if latest.get('operating_revenue') else 'N/A',
                        '净利润(亿)': round(latest.get('net_profit', 0) / 1e8, 2) if latest.get('net_profit') else 'N/A',
                    }
                    # 5年历史
                    history_lines = []
                    for row in financial_rows:
                        history_lines.append(f"{row['year']}: ROE={row.get('roe','N/A')}, 净利率={row.get('net_profit_margin','N/A')}, 营收增长={row.get('revenue_growth','N/A')}")

                    result['baostock_data'] = {
                        'summary': summary_data,
                        'history': financial_rows,
                        'history_text': '\n'.join(history_lines)
                    }
                    result['baostock_success'] = True
                    self.log.info(f"Baostock financial: {len(financial_rows)} years, latest ROE={latest.get('roe')}")
            except Exception as e:
                self.log.warning(f"Baostock financial failed: {e}")

        # ===== 方法2: AKShare补充（不稳定，仅作备用） =====
        if AKSHARE_AVAILABLE:
            try:
                df = ak.stock_financial_abstract(symbol=symbol)
                if df is not None and not df.empty:
                    self.log.info(f"AKShare financial abstract: {df.shape}")
                    result['data'] = df
                    result['source'] = 'akshare'
            except Exception as e:
                self.log.warning(f"AKShare financial abstract failed: {e}")

            try:
                time.sleep(1)
                df_indicator = ak.stock_financial_analysis_indicator(symbol=symbol, start_year='2022')
                if df_indicator is not None and not df_indicator.empty:
                    self.log.info(f"AKShare financial indicators: {df_indicator.shape}")
                    result['financial_indicator'] = df_indicator
                    result['indicator_success'] = True
            except Exception as e:
                self.log.warning(f"AKShare financial indicators failed: {e}")

        # ===== 判断成功 =====
        # Baostock成功就算成功，AKShare只是补充
        if result['baostock_success']:
            result['success'] = True
            result['source'] = 'baostock_primary'
        elif result['data'] is not None or result['indicator_success']:
            result['success'] = True
        else:
            result['error'] = "All financial data sources failed"

        return result

    def _get_hk_basic_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取港股基本信息（从实时行情表，2741只）"""
        if not AKSHARE_AVAILABLE:
            return None
        hk_symbol = symbol.lower().replace('hk', '').strip()
        try:
            df = ak.stock_hk_spot()
            if df is None or df.empty:
                return None
            # 用列索引避开中文乱码: 0=时间, 1=代码, 2=中文名, 3=英文名, 4=现价, 5=涨跌, 6=涨跌幅
            code_col = df.columns[1]
            name_col = df.columns[2]
            price_col = df.columns[4]
            pct_col = df.columns[6]
            row = df[df[code_col].astype(str).str.strip() == hk_symbol]
            if not row.empty:
                r = row.iloc[0]
                return {
                    'stock_code': symbol,
                    'stock_name': str(r[name_col]),
                    'industry': '港股',
                    'latest_price': str(r[price_col]) if price_col < len(df.columns) else '',
                    'pct_change': str(r[pct_col]) if pct_col < len(df.columns) else '',
                }
        except Exception as e:
            self.log.warning(f"HK spot info failed: {e}")
        return None


    def get_basic_info(self, symbol: str) -> Dict[str, Any]:
        """获取基本信息 - Baostock优先（稳定），AKShare仅补充"""
        self.log.info(f"Fetching basic info for {symbol}")
        result = {'symbol': symbol, 'data': {}, 'success': False, 'is_hk': False}

        # ===== 港股分支：保持原有逻辑（内置+AKShare） =====
        if self._is_hk_stock(symbol):
            result['is_hk'] = True
            hk_sym = symbol.lower()
            hk_builtin = {
                'hk00700': {'stock_name': '腾讯控股', 'industry': '互联网科技'},
                'hk09988': {'stock_name': '阿里巴巴', 'industry': '互联网科技'},
                'hk03690': {'stock_name': '美团-W', 'industry': '本地生活'},
                'hk01810': {'stock_name': '小米集团-W', 'industry': '消费电子'},
                'hk09618': {'stock_name': '京东集团-SW', 'industry': '电商'},
                'hk09888': {'stock_name': '百度集团-SW', 'industry': '互联网科技'},
                'hk09999': {'stock_name': '网易-S', 'industry': '互联网科技'},
                'hk09626': {'stock_name': '哔哩哔哩-W', 'industry': '视频娱乐'},
                'hk01024': {'stock_name': '快手-W', 'industry': '短视频'},
                'hk02015': {'stock_name': '理想汽车-W', 'industry': '新能源汽车'},
                'hk09868': {'stock_name': '小鹏汽车-W', 'industry': '新能源汽车'},
                'hk09866': {'stock_name': '蔚来-SW', 'industry': '新能源汽车'},
                'hk002594': {'stock_name': '比亚迪股份', 'industry': '新能源汽车'},
                'hk00939': {'stock_name': '建设银行', 'industry': '银行'},
                'hk01398': {'stock_name': '工商银行', 'industry': '银行'},
                'hk03988': {'stock_name': '中国银行', 'industry': '银行'},
                'hk03968': {'stock_name': '招商银行', 'industry': '银行'},
                'hk02318': {'stock_name': '中国平安', 'industry': '保险'},
                'hk01299': {'stock_name': '友邦保险', 'industry': '保险'},
                'hk00388': {'stock_name': '香港交易所', 'industry': '金融服务'},
                'hk00941': {'stock_name': '中国移动', 'industry': '通信'},
                'hk00728': {'stock_name': '中国电信', 'industry': '通信'},
                'hk00762': {'stock_name': '中国联通', 'industry': '通信'},
                'hk02020': {'stock_name': '安踏体育', 'industry': '体育用品'},
                'hk02319': {'stock_name': '蒙牛乳业', 'industry': '乳制品'},
                'hk00168': {'stock_name': '青岛啤酒', 'industry': '啤酒'},
                'hk09633': {'stock_name': '农夫山泉', 'industry': '饮料'},
                'hk06862': {'stock_name': '海底捞', 'industry': '餐饮'},
                'hk06969': {'stock_name': '九毛九', 'industry': '餐饮'},
                'hk09992': {'stock_name': '泡泡玛特', 'industry': '潮流玩具'},
                'hk06618': {'stock_name': '京东健康', 'industry': '医疗健康'},
                'hk1177': {'stock_name': '中国生物制药', 'industry': '生物医药'},
                'hk06160': {'stock_name': '百济神州', 'industry': '生物医药'},
                'hk02126': {'stock_name': '康方生物', 'industry': '生物医药'},
                'hk00960': {'stock_name': '龙湖集团', 'industry': '房地产'},
                'hk01109': {'stock_name': '华润置地', 'industry': '房地产'},
                'hk00883': {'stock_name': '中国海洋石油', 'industry': '石油天然气'},
                'hk00857': {'stock_name': '中国石油股份', 'industry': '石油天然气'},
                'hk00386': {'stock_name': '中国石油化工', 'industry': '石油天然气'},
                'hk02382': {'stock_name': '舜宇光学科技', 'industry': '光学镜头'},
                'hk09893': {'stock_name': '华虹半导体', 'industry': '半导体'},
                'hk01928': {'stock_name': '金沙中国', 'industry': '博彩'},
                'hk00027': {'stock_name': '银河娱乐', 'industry': '博彩'},
                'hk09961': {'stock_name': '携程集团-S', 'industry': '在线旅游'},
            }
            if hk_sym in hk_builtin:
                info = {'stock_code': symbol, **hk_builtin[hk_sym]}
                self.log.info(f"HK built-in: {info.get('stock_name')}")
                result.update({'data': info, 'success': True})
                return result
            hk_info = self._get_hk_basic_info(symbol)
            if hk_info:
                self.log.info(f"HK spot: {hk_info.get('stock_name')}")
                result.update({'data': hk_info, 'success': True})
                return result
            return result

        # ===== A股分支：Baostock优先 =====

        # 方法1: Baostock query_stock_industry（证监会行业分类，最稳定）
        industry_full = ''
        if self.baostock_connected:
            try:
                bs_sym = self._bs_symbol(symbol)
                rs_ind = bs.query_stock_industry(code=bs_sym)
                ind_rows = []
                while rs_ind.error_code == '0' and rs_ind.next():
                    ind_rows.append(rs_ind.get_row_data())
                if ind_rows and ind_rows[0]:
                    # ['2026-04-13', 'sh.600519', '贵州茅台', 'C15酒、饮料和精制茶制造业', '证监会行业分类']
                    industry_full = ind_rows[0][3] if len(ind_rows[0]) > 3 else ''
                    self.log.info(f"Baostock industry: {industry_full}")
            except Exception as e:
                self.log.warning(f"Baostock industry query failed: {e}")

        # 方法2: Baostock query_stock_basic（股票名称、上市日期）
        stock_name = ''
        listing_date = ''
        if self.baostock_connected:
            try:
                bs_sym = self._bs_symbol(symbol)
                rs_basic = bs.query_stock_basic(code=bs_sym)
                basic_rows = []
                while rs_basic.error_code == '0' and rs_basic.next():
                    basic_rows.append(rs_basic.get_row_data())
                if basic_rows and basic_rows[0]:
                    # ['sh.600519', '贵州茅台', '2001-08-27', '', '1', '1']
                    br = basic_rows[0]
                    stock_name = br[1] if len(br) > 1 else ''
                    listing_date = br[2] if len(br) > 2 else ''
                    self.log.info(f"Baostock basic: {stock_name}, {listing_date}")
            except Exception as e:
                self.log.warning(f"Baostock basic query failed: {e}")

        # 如果Baostock拿到了关键数据（名称+行业）
        if stock_name and industry_full:
            industry = self._simplify_industry(industry_full)
            info = {
                'stock_code': symbol,
                'stock_name': stock_name,
                'industry': industry,
                'industry_full': industry_full,  # 保留证监会全称
                'listing_date': listing_date,
                'data_source': 'baostock',
            }
            self.log.info(f"Baostock SUCCESS: {stock_name}, Industry: {industry}")
            result.update({'data': info, 'success': True})
            return result
        elif stock_name:
            # 有名称但行业未知
            info = {
                'stock_code': symbol,
                'stock_name': stock_name,
                'industry': '',
                'listing_date': listing_date,
                'data_source': 'baostock',
            }
            self.log.info(f"Baostock partial: name={stock_name}, industry unknown")
            result.update({'data': info, 'success': True, 'industry_missing': True})
            return result

        # 方法3: AKShare补充（不稳定，作为补充获取更多字段）
        if AKSHARE_AVAILABLE:
            for attempt in range(2):  # 只重试2次（快速失败）
                try:
                    time.sleep(2)
                    info_df = ak.stock_individual_info_em(symbol=symbol)
                    if info_df is not None and not info_df.empty:
                        info_dict = {}
                        for _, row in info_df.iterrows():
                            info_dict[row.get('item', '')] = row.get('value', '')
                        industry = info_dict.get('行业', '')
                        name = info_dict.get('股票简称', '')
                        if industry and name:
                            info = {
                                'stock_code': info_dict.get('股票代码', symbol),
                                'stock_name': name,
                                'industry': industry,
                                'total_capital': info_dict.get('总股本', ''),
                                'float_capital': info_dict.get('流通股', ''),
                                'total_market_cap': info_dict.get('总市值', ''),
                                'float_market_cap': info_dict.get('流通市值', ''),
                                'pe_ratio': info_dict.get('市盈率', ''),
                                'pb_ratio': info_dict.get('市净率', ''),
                                'latest_price': info_dict.get('最新', info_dict.get('最新价', '')),
                                'listing_date': info_dict.get('上市时间', ''),
                                'data_source': 'akshare',
                            }
                            self.log.info(f"AKShare success: {name}, Industry: {industry}")
                            result.update({'data': info, 'success': True})
                            return result
                except Exception as e:
                    self.log.warning(f"AKShare attempt {attempt+1} failed: {e}")
                    if attempt < 1:
                        time.sleep(3)

        # 方法4: 内置数据库保底（仅名称+行业）
        BUILTIN_STOCKS = {
            '600519': {'stock_name': '贵州茅台', 'industry': '白酒'},
            '000858': {'stock_name': '五粮液', 'industry': '白酒'},
            '000002': {'stock_name': '万科A', 'industry': '房地产'},
            '600036': {'stock_name': '招商银行', 'industry': '银行'},
            '601318': {'stock_name': '中国平安', 'industry': '保险'},
            '600000': {'stock_name': '浦发银行', 'industry': '银行'},
            '000001': {'stock_name': '平安银行', 'industry': '银行'},
            '601166': {'stock_name': '兴业银行', 'industry': '银行'},
            '600030': {'stock_name': '中信证券', 'industry': '证券'},
            '601888': {'stock_name': '中国中免', 'industry': '零售'},
            '300750': {'stock_name': '宁德时代', 'industry': '电池'},
            '002594': {'stock_name': '比亚迪', 'industry': '汽车'},
            '300450': {'stock_name': '先导智能', 'industry': '电池'},
            '688005': {'stock_name': '容百科技', 'industry': '电池'},
            '300014': {'stock_name': '亿纬锂能', 'industry': '电池'},
            '002129': {'stock_name': 'TCL中环', 'industry': '光伏'},
            '688122': {'stock_name': '西部超导', 'industry': '超导材料'},
            '688041': {'stock_name': '海光信息', 'industry': '半导体'},
            '688981': {'stock_name': '中芯国际', 'industry': '半导体'},
            '688256': {'stock_name': '寒武纪', 'industry': '半导体'},
            '000895': {'stock_name': '双汇发展', 'industry': '食品'},
            '600887': {'stock_name': '伊利股份', 'industry': '乳制品'},
            '000568': {'stock_name': '泸州老窖', 'industry': '白酒'},
            '002304': {'stock_name': '洋河股份', 'industry': '白酒'},
            '300760': {'stock_name': '迈瑞医疗', 'industry': '医疗器械'},
            '600276': {'stock_name': '恒瑞医药', 'industry': '化学制药'},
            '300122': {'stock_name': '智飞生物', 'industry': '生物疫苗'},
            '002415': {'stock_name': '海康威视', 'industry': '安防'},
            '002475': {'stock_name': '立讯精密', 'industry': '电子制造'},
            '600588': {'stock_name': '用友网络', 'industry': '软件'},
        }
        if symbol in BUILTIN_STOCKS:
            info = {'stock_code': symbol, 'data_source': 'builtin', **BUILTIN_STOCKS[symbol]}
            self.log.info(f"Built-in DB: {info.get('stock_name')}, Industry: {info.get('industry')}")
            result.update({'data': info, 'success': True})
            return result

        # 全部失败
        self.log.error(f"All sources failed for {symbol}")
        return result


    def close(self):
        if self.baostock_connected:
            try:
                bs.logout()
            except:
                pass


class AIAnalysisService:
    def __init__(self):
        self.config = get_config()
        self.log = get_log("AIAnalysis")
        self.ds_config = self.config.deepseek

    def call_api(self, prompt: str) -> str:
        if not self.ds_config.api_key:
            return "ERROR: API key not configured"

        headers = {"Authorization": f"Bearer {self.ds_config.api_key}", "Content-Type": "application/json"}
        data = {
            "model": self.ds_config.model,
            "messages": [
                {"role": "system", "content": "You are a professional financial analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3, "max_tokens": 4000
        }

        try:
            self.log.info("Calling AI model...")
            response = requests.post(self.ds_config.api_url, headers=headers, json=data, timeout=self.ds_config.timeout)
            response.raise_for_status()
            result = response.json()
            if "choices" in result and result["choices"]:
                self.log.info("AI analysis completed")
                return result["choices"][0]["message"]["content"]
            return "ERROR: Invalid API response"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def build_valuation_prompt(self, symbol: str, price_data: pd.DataFrame,
                               financial_data: pd.DataFrame, basic_info: dict,
                               financial_indicator: pd.DataFrame = None,
                               news_result: dict = None,
                               baostock_data: dict = None) -> str:
        company_name = basic_info.get('stock_name', 'Unknown')
        industry = basic_info.get('industry', 'Unknown')

        # Format news data
        news_section = ""
        if news_result and news_result.get('news'):
            news_items = news_result['news'][:5]  # Top 5 news
            news_lines = []
            for i, news in enumerate(news_items, 1):
                title = news.get('title', 'N/A')
                datetime_info = news.get('datetime', 'N/A')
                source = news.get('source', 'N/A')
                news_lines.append(f"{i}. **{title}** - {datetime_info} ({source})")
            if news_lines:
                news_section = "### Recent Company News\n" + "\n".join(news_lines)
        else:
            news_section = "### Recent Company News\n*(No recent news available)*"

        # Price data
        price_info = "No price data available"
        latest_price = None
        latest_date = None

        if price_data is not None and not price_data.empty:
            price_lines = []
            latest_row = price_data.iloc[-1]

            if 'close' in price_data.columns:
                latest_price = latest_row['close']
                latest_date = latest_row.get('date', latest_row.get('日期', 'Unknown'))
            elif '收盘' in price_data.columns:
                latest_price = latest_row.get('收盘')
                latest_date = latest_row.get('日期', 'Unknown')

            if 'date' in price_data.columns:
                for _, row in price_data.tail(10).iterrows():
                    price_lines.append(f"- {row['date']}: Open={row['open']:.2f}, High={row['high']:.2f}, Low={row['low']:.2f}, Close={row['close']:.2f}, Change={row.get('pctChg', 0):.2f}%")
            elif '日期' in price_data.columns:
                for _, row in price_data.tail(10).iterrows():
                    price_lines.append(f"- {row['日期']}: Close={row.get('收盘', 'N/A')}")

            if price_lines:
                price_info = f"LATEST DATA (Most Recent: {latest_date}, Price: {latest_price:.2f} CNY):\n" + "\n".join(price_lines)

        # Price metrics
        price_metrics = ""
        if price_data is not None and not price_data.empty and latest_price:
            try:
                if 'close' in price_data.columns:
                    prices = price_data['close'].dropna().astype(float)
                    if len(prices) > 0:
                        price_30d_high = prices.max()
                        price_30d_low = prices.min()
                        price_30d_avg = prices.mean()
                        price_metrics = f"""
### Key Price Metrics
- Latest Price: {latest_price:.2f} CNY ({latest_date})
- 30-Day High: {price_30d_high:.2f} CNY
- 30-Day Low: {price_30d_low:.2f} CNY
- 30-Day Average: {price_30d_avg:.2f} CNY
- Distance from High: {((latest_price - price_30d_high) / price_30d_high * 100):.2f}%
- Distance from Low: {((latest_price - price_30d_low) / price_30d_low * 100):.2f}%
"""
            except:
                pass

        # Financial summary
        financial_info = "No financial data available"
        if financial_data is not None and not financial_data.empty:
            fin_lines = []
            fin_dict = financial_data.iloc[0].to_dict() if len(financial_data) > 0 else {}
            for col, val in list(fin_dict.items())[:20]:
                if val is not None and val != '' and str(val) != 'nan':
                    fin_lines.append(f"- {col}: {val}")
            if fin_lines:
                financial_info = "\n".join(fin_lines)

        # Baostock 5-year financial data (prioritized)
        baostock_financial = ""
        if baostock_data:
            summary = baostock_data.get('summary', {})
            history_text = baostock_data.get('history_text', '')
            if summary:
                rows = []
                rows.append(f"### Baostock 5-Year Financial Data (Primary Data Source)")
                rows.append(f"| Year | ROE | Net Margin | Revenue Growth | Net Profit Growth |")
                rows.append(f"|------|-----|------------|----------------|-------------------|")
                for h in baostock_data.get('history', []):
                    rows.append(f"| {h.get('year','N/A')} | {h.get('roe','N/A')} | {h.get('net_profit_margin','N/A')} | {h.get('revenue_growth','N/A')} | {h.get('net_profit_growth','N/A')} |")
                rows.append(f"\n**Latest Year Summary** (from Baostock):")
                for k, v in summary.items():
                    if str(v) != 'N/A' and v is not None and v != '':
                        rows.append(f"- {k}: {v}")
                baostock_financial = "\n".join(rows)
                self.log.info(f"Baostock financial data added to prompt: {summary}")

        # Detailed financial indicators
        detailed_financial = ""
        if financial_indicator is not None and not financial_indicator.empty:
            indicator_lines = []
            latest = financial_indicator.iloc[0]
            key_indicators = {
                'Profitability': ['每股收益', '净资产收益率', '销售净利率', '总资产净利润率', '营业利润率', '成本费用利润率'],
                'Per Share': ['每股净资产', '每股经营性现金流', '每股资本公积金', '每股未分配利润'],
                'Growth': ['营业收入同比', '净利润同比', '净资产同比'],
                'Solvency': ['流动比率', '速动比率', '资产负债率'],
            }
            for category, metrics in key_indicators.items():
                indicator_lines.append(f"\n### {category}")
                for metric in metrics:
                    for col in financial_indicator.columns:
                        if metric in col:
                            val = latest.get(col)
                            if val is not None and str(val) != 'nan':
                                indicator_lines.append(f"- {col}: {val}")
                                break
            if indicator_lines:
                detailed_financial = "\n".join(indicator_lines)

        # Basic info
        basic_info_text = "\n".join([f"- {k}: {v}" for k, v in basic_info.items() if v and str(v) != 'nan' and str(v) != 'None'])

        template = f"""
# Damodaran Valuation Analysis Task

## Target Company
| Field | Value |
|-------|-------|
| **Company Name** | {company_name} |
| **Stock Code** | {symbol} |
| **Industry** | {industry} |
| **Analysis Date** | {datetime.now().strftime('%Y-%m-%d')} |

## CRITICAL INSTRUCTIONS - MUST FOLLOW
1. **Industry IS PROVIDED**: {industry} - This is a **{industry}** company
2. **Industry is NOT unknown** - Use "{industry}" for all analysis
3. **Use ONLY data from this prompt** - DO NOT invent prices
4. **Use actual price**: {latest_price:.2f} CNY ({latest_date}) from "Recent Price Data"
5. **Output Format**: Use Markdown tables, headers, and emphasis for professional appearance
6. **Include ALL sections** specified in the output requirements

## Company Information
{basic_info_text}

## Recent Price Data (Last 10 Trading Days)
{price_info}

{price_metrics}

## Financial Analysis
{baostock_financial if baostock_financial else ""}
### Financial Summary (AKShare)
{financial_info}

### Detailed Financial Indicators
{detailed_financial if detailed_financial else "(Detailed financial indicators data)"}

## Recent News & Developments
{news_section}

## Industry Context - CRITICAL FOR RELATIVE VALUATION
- **Industry**: {industry}
- **Use this industry for**: competitive analysis, relative valuation, peer comparison
- **Compare**: {company_name}'s PE, PB, PS against industry averages
- **Assess**: competitive position within the {industry} industry

## Analysis Task

### Step 1: Core Diagnosis
- Life cycle stage analysis within {industry} industry context
- Profitability and cash flow quality assessment
- Industry-specific risk identification
- "Valuation Dark Side" analysis

### Step 2: Valuation Model (DCF)
- Build 3-stage DCF model (Base, Bull, Bear scenarios)
- Set WACC considering {industry} industry characteristics
- Calculate valuation range

### Step 3: Relative Valuation with Industry Comparison
- **CRITICAL**: Compare PE, PB, PS against {industry} industry averages
- Identify if {company_name} is overvalued or undervalued vs peers
- Use industry benchmarks for valuation assessment

### Step 4: Sensitivity Analysis
- Analyze impact of key assumptions on valuation

### Step 5: Industry Outlook & Future Prospects
- Analyze {industry} industry development trends
- Assess company's growth potential and market opportunities
- Identify key catalysts for future value appreciation
- Include quantitative growth forecasts where applicable

## Output Requirements
Generate a professional, well-formatted Markdown valuation report:

```markdown
# {company_name} ({symbol}) 估值分析报告

> 📅 {datetime.now().strftime('%Y年%m月%d日')} | 🏭 行业：{industry}

---

## 📋 核心数据一览

| 指标 | 数值 | 行业对比 |
|------|------|----------|
| 当前股价 | {latest_price:.2f}元 | - |
| 估值区间 | XX-XX元 | - |

---

## 一、核心诊断摘要

### 1.1 公司概况
- 公司名称：{company_name}
- 所属行业：{industry}
- 股票代码：{symbol}

### 1.2 生命周期阶段
[分析内容]

### 1.3 盈利能力评估
[分析内容]

### 1.4 估值暗面分析
[分析内容]

---

## 二、情景分析与估值模型

### 2.1 估值假设表
| 情景 | WACC | 永续增长率 | 估值区间 |
|------|------|-----------|----------|
| 熊市 | X% | X% | XX-XX元 |
| 基准 | X% | X% | XX-XX元 |
| 牛市 | X% | X% | XX-XX元 |

### 2.2 DCF模型分析
[详细计算过程]

---

## 三、相对估值验证

### 3.1 估值指标对比
| 指标 | 公司值 | 行业中位数 | 偏离度 |
|------|--------|------------|--------|
| PE | XX | XX | ±X% |
| PB | XX | XX | ±X% |
| PS | XX | XX | ±X% |

### 3.2 估值结论
[综合判断]

---

## 四、前景展望与成长预期 ⭐ NEW

### 4.1 行业发展趋势
[分析{industry}行业的发展方向、市场规模、政策环境]

### 4.2 公司成长动力
[分析公司未来的增长驱动因素]
- ✅ 机遇1：...
- ✅ 机遇2：...
- ✅ 机遇3：...

### 4.3 成长风险
[可能影响成长的风险因素]
- ⚠️ 风险1：...
- ⚠️ 风险2：...

### 4.4 成长预期量化
| 指标 | 未来1年 | 未来3年 | 未来5年 |
|------|---------|---------|---------|
| 营收增长 | X% | X% | X% |
| 净利润增长 | X% | X% | X% |
| 目标市值 | XX亿 | XX亿 | XX亿 |

---

## 五、敏感性分析

### 5.1 关键变量影响
| 变量 | 变动 | 估值影响 |
|------|------|----------|
| WACC | ±1% | ±X% |
| 永续增长率 | ±0.5% | ±X% |

---

## 六、投资建议与风险提示

### 6.1 综合评级
[强烈推荐/推荐/中性/谨慎/回避]

### 6.2 核心投资逻辑
[买入/持有的主要理由]

### 6.3 主要风险提示
[投资面临的主要风险]

---

## ⚠️ 免责声明

本报告仅供参考，不构成任何投资建议。股票投资有风险，入市需谨慎。
```

## Important Notes
- {company_name} is a **{industry}** company - ALWAYS mention industry in report
- Industry is "{industry}" - NEVER say industry is unknown
- Use actual data ONLY - no invented prices or ratios
- Include the **Industry Outlook & Future Prospects** section with quantitative forecasts
- Use tables and formatting for professional appearance
- This report is for reference only, not investment advice

Please generate the complete, professionally formatted Damodaran valuation report for {company_name}({symbol}) in the {industry} industry.
"""
        return template


class ReportService:
    def __init__(self):
        self.config = get_config()
        self.log = get_log("Report")

    def save_report(self, content: str, filename: str) -> str:
        report_dir = self.config.report_dir
        report_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = report_dir / f"{filename}_{timestamp}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        self.log.info(f"Report saved: {filepath}")
        return str(filepath)

    def add_disclaimer(self, report: str) -> str:
        disclaimer = """

---

## Disclaimer

This report is for reference only and does not constitute any investment advice. Stock investing involves risks.

1. All analysis results are for reference only.
2. Past performance does not indicate future returns.
3. Valuation is based on current data and assumptions.
4. Please consult a licensed investment advisor.

(c) 2026 ValU AI Valuation Analyzer
"""
        return report + disclaimer


class ValuationService:
    def __init__(self):
        self.config = get_config()
        self.log = get_log("Valuation")
        self.data_service = StockDataService()
        self.ai_service = AIAnalysisService()
        self.report_service = ReportService()
        self.quota_manager = UserQuotaManager()

    def check_quota(self, user_id: str) -> Tuple[bool, str, Dict]:
        can_analyze, source = self.quota_manager.check_can_analyze(user_id)
        info = self.quota_manager.get_user_info(user_id)
        return can_analyze, source, info

    def use_quota(self, user_id: str, count: int = 1) -> bool:
        return self.quota_manager.use_quota(user_id, count)

    def analyze_single(self, user_id: str, symbol: str) -> Dict[str, Any]:
        self.log.info(f"Starting analysis for {symbol}, user: {user_id}")

        # First check quota
        can_analyze, source, info = self.check_quota(user_id)
        if not can_analyze:
            return {'success': False, 'error': 'Quota exceeded', 'error_code': 'QUOTA_EXCEEDED'}

        self.log.info("Fetching stock data...")
        price_result = self.data_service.get_historical_prices(symbol)
        if not price_result['success']:
            return {'success': False, 'error': 'Failed to get price data. Please try again later.', 'error_code': 'DATA_ERROR_PRICE'}

        financial_result = self.data_service.get_financial_data(symbol)
        basic_result = self.data_service.get_basic_info(symbol)

        # Strict data validation - ALL fields must be complete
        validation_errors = []
        data_status = {
            'basic_info': basic_result['success'],
            'price_data': price_result['success'],
            'financial_data': financial_result['success'] or financial_result.get('indicator_success', False),
            'industry_complete': False
        }

        # Check basic info completeness
        if not basic_result['success'] or not basic_result['data']:
            validation_errors.append('Failed to get basic info')
        else:
            basic_data = basic_result['data']
            if not basic_data.get('stock_name'):
                validation_errors.append('Stock name missing')
            if not basic_data.get('industry'):
                validation_errors.append('Industry information missing')
            elif basic_data.get('industry') in ['Unknown', 'unknown', '未知', '']:
                validation_errors.append('Industry data invalid (Unknown)')
            else:
                data_status['industry_complete'] = True

        # Check financial data
        if not financial_result['success'] and not financial_result.get('indicator_success'):
            validation_errors.append('Failed to get financial data')

        # If validation fails, return error WITHOUT counting quota
        if validation_errors:
            error_msg = 'Data temporarily unavailable. This analysis was not counted.\n\n'
            error_msg += 'Missing data:\n' + '\n'.join([f"  - {e}" for e in validation_errors])
            error_msg += '\n\nPlease try again in a few moments.'

            self.log.warning(f"Data validation failed (quota NOT charged): {validation_errors}")

            return {
                'success': False,
                'error': error_msg,
                'error_code': 'DATA_INCOMPLETE',
                'quota_charged': False,  # Important: quota not charged!
                'data_status': data_status
            }

        self.log.info("Data validation passed, building report...")

        # Search for recent news
        news_result = None
        try:
            news_result = self.data_service.search_news(basic_result['data'].get('stock_name', ''))
        except Exception as e:
            self.log.warning(f"News search failed: {e}")

        prompt = self.ai_service.build_valuation_prompt(
            symbol, price_result['data'],
            financial_result['data'] if financial_result['success'] else pd.DataFrame(),
            basic_result['data'],
            financial_result.get('financial_indicator') if financial_result.get('indicator_success') else None,
            news_result,
            baostock_data=financial_result.get('baostock_data')
        )

        self.log.info("Calling AI model...")
        report = self.ai_service.call_api(prompt)

        if report.startswith("ERROR"):
            return {'success': False, 'error': report, 'error_code': 'API_ERROR'}

        report = self.report_service.add_disclaimer(report)
        filepath = self.report_service.save_report(report, f"valuation_{symbol}")
        self.use_quota(user_id, 1)
        new_info = self.quota_manager.get_user_info(user_id)

        return {
            'success': True, 'symbol': symbol,
            'company_name': basic_result['data'].get('stock_name', 'Unknown'),
            'industry': basic_result['data'].get('industry', 'Unknown'),
            'report': report, 'report_file': filepath,
            'quota_remaining': new_info['free_quota_remaining'],
            'data_status': {'basic_info': True, 'price_data': True, 'financial_data': True}
        }

    def analyze_batch(self, user_id: str, symbols: List[str]) -> Dict[str, Any]:
        self.log.info(f"Starting batch analysis for {symbols}")
        max_stocks = self.config.batch_max_stocks
        if len(symbols) < 2:
            return {'success': False, 'error': 'At least 2 stocks required', 'error_code': 'INVALID_INPUT'}
        if len(symbols) > max_stocks:
            return {'success': False, 'error': f'Max {max_stocks} stocks allowed', 'error_code': 'INVALID_INPUT'}

        stock_results = []
        for symbol in symbols:
            price_result = self.data_service.get_historical_prices(symbol)
            basic_result = self.data_service.get_basic_info(symbol)
            stock_results.append({
                'symbol': symbol,
                'name': basic_result['data'].get('stock_name', symbol),
                'price_data': price_result['data'] if price_result['success'] else None,
                'basic_info': basic_result['data'],
                'success': price_result['success']
            })
            time.sleep(0.5)

        comparator = StockComparator()
        comparison = comparator.compare_stocks(stock_results)
        report = comparator.generate_comparison_report()
        report = self.report_service.add_disclaimer(report)
        filepath = self.report_service.save_report(report, f"batch_{'_'.join(symbols)}")

        return {
            'success': True, 'stocks': symbols,
            'stocks_analyzed': len([s for s in stock_results if s['success']]),
            'comparison': comparison, 'report': report, 'report_file': filepath
        }


class ValUApp:
    def __init__(self):
        self.config = get_config()
        self.log = get_log("App")
        self.log.info(f"Starting {self.config.app.name} v{self.config.app.version}")
        self.valuation_service = ValuationService()

    def show_banner(self):
        print(f"\n{'='*50}\n{self.config.app.name} v{self.config.app.version}\n{'='*50}\n")

    def run(self):
        self.show_banner()
        while True:
            print("\nOptions: 1.Single 2.Batch 3.Quota 4.Pricing 0.Exit")
            choice = input("Choice: ").strip()
            if choice == "1":
                user_id = input("User ID: ").strip() or "guest"
                symbol = input("Stock code: ").strip()
                if symbol:
                    result = self.valuation_service.analyze_single(user_id, symbol)
                    if result['success']:
                        print(f"\nSUCCESS! Stock: {result['symbol']} ({result.get('company_name')}, {result.get('industry')})")
                        print(f"Report: {result['report_file']}, Quota: {result['quota_remaining']}")
                    else:
                        print(f"\nFAILED: {result.get('error')}")
            elif choice == "2":
                user_id = input("User ID: ").strip() or "guest"
                symbols_input = input("Stock codes (comma separated): ").strip()
                if symbols_input:
                    symbols = [s.strip() for s in symbols_input.split(',')]
                    result = self.valuation_service.analyze_batch(user_id, symbols)
                    if result['success']:
                        print(f"\nSUCCESS! Analyzed {result['stocks_analyzed']}/{len(result['stocks'])} stocks")
            elif choice == "3":
                user_id = input("User ID: ").strip() or "guest"
                info = self.valuation_service.quota_manager.get_user_info(user_id)
                print(f"Free quota: {info['free_quota_remaining']}/{info['free_quota_total']}/week")
            elif choice == "0":
                print("Goodbye!")
                break


def main():
    try:
        app = ValUApp()
        app.run()
    except KeyboardInterrupt:
        print("\nInterrupted")
    except Exception as e:
        get_log().exception(f"Error: {e}")


if __name__ == "__main__":
    main()
