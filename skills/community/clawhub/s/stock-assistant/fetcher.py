#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股行情获取模块
支持多数据源：腾讯财经、新浪财经、东方财富（备用）
"""

import requests
import time
import json
from typing import Dict, Any, Optional, List


class StockFetcher:
    """A股行情获取器 - 腾讯接口"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://finance.qq.com/'
        }
        self.providers = [
            EastMoneyProvider(),
            TencentProvider(),
            SinaProvider(),
        ]
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        获取A股实时行情（多数据源合并）
        
        策略：东方财富（主）+ 腾讯（辅，补充盘口和资金流）
        
        Args:
            symbol: 股票代码，如 '600519' (上海) 或 '000001' (深圳)
        
        Returns:
            包含行情数据的字典
        """
        # 第一步：腾讯获取实时行情（价格/成交以腾讯为准，东方财富集合竞价数据有误差）
        result = None
        tw_provider = TencentProvider()
        try:
            result = tw_provider.fetch(symbol)
            if result and 'error' not in result:
                result['_provider'] = '腾讯'
            else:
                result = None
        except Exception:
            pass
        
        # 第二步：东方财富补充财务指标、市值、涨跌停等字段
        em_provider = EastMoneyProvider()
        try:
            em = em_provider.fetch(symbol)
            if em and 'error' not in em:
                for key in em:
                    # 东方财富只补充腾讯没有的字段，避免覆盖错误的价格数据
                    if key not in result or not result.get(key):
                        result[key] = em[key]
                if result.get('_provider') == '腾讯':
                    result['_provider'] = '腾讯+东方财富'
        except Exception:
            pass
        
        if result:
            return result
        
        # 第三步：其他数据源兜底
        for provider in [TencentProvider(), SinaProvider()]:
            if isinstance(provider, EastMoneyProvider):
                continue
            try:
                r = provider.fetch(symbol)
                if r and 'error' not in r:
                    r['_provider'] = provider.name
                    return r
            except Exception:
                continue
        
        return {'error': '所有数据源均不可用'}
    
    def format_table(self, data: Dict[str, Any], position=None) -> str:
        """格式化行情数据为飞书卡片
        
        Args:
            data: 行情数据
            position: 持仓信息 (可选)
        """
        import json
        
        if 'error' in data:
            return json.dumps({
                'config': {'wide_screen_mode': True},
                'header': {
                    'title': {'tag': 'plain_text', 'content': '❌ 获取失败'},
                    'template': 'red'
                },
                'elements': [
                    {'tag': 'div', 'text': {'tag': 'lark_md', 'content': data.get('error', '未知错误')}}
                ]
            })
        
        name = data.get('股票名称', data.get('股票代码', ''))
        code = data.get('股票代码', '')
        price = data.get('当前价格', '-')
        change = data.get('涨跌额', '0')
        pct = data.get('涨跌幅(%)', '0')
        open_price = data.get('今开价', '-')
        pre_close = data.get('昨收价', '-')
        high = data.get('最高价', '-')
        low = data.get('最低价', '-')
        volume = data.get('成交量(手)', '-')
        turnover = data.get('成交额(元)', '-')
        turnover_rate = data.get('换手率(%)', '-')
        provider = data.get('_provider', '未知')
        
        # 处理涨跌幅显示
        try:
            pct_float = float(pct)
            pct_str = f"{pct_float:+.2f}%"
            if pct_float > 0:
                change_str = f"+{change} ({pct_str}) 🔺"
            elif pct_float < 0:
                change_str = f"{change} ({pct_str}) 🔻"
            else:
                change_str = f"{change} ({pct_str})"
        except:
            pct_str = pct
            change_str = change
        
        # 格式化成交量
        try:
            vol = int(str(volume).replace(',', ''))
            if vol > 10000:
                volume_str = f"{vol/10000:.1f}万手"
            else:
                volume_str = f"{vol}手"
        except:
            volume_str = volume
        
        # 格式化成交额
        try:
            amt = float(str(turnover).replace(',', ''))
            if amt > 10000:
                turnover_str = f"{amt/10000:.1f}万"
            else:
                turnover_str = turnover
        except:
            turnover_str = turnover
        
        # 卡片颜色
        template = 'blue' if pct_float >= 0 else 'red'
        
        # 构建卡片元素
        elements = [
            {
                'tag': 'div',
                'text': {'tag': 'lark_md', 'content': f'**当前价**: {price}  |  **涨跌**: {change_str}'}
            },
            {
                'tag': 'div',
                'text': {'tag': 'lark_md', 'content': f'**今开**: {open_price}  |  **昨收**: {pre_close}'}
            },
            {
                'tag': 'div',
                'text': {'tag': 'lark_md', 'content': f'**最高**: {high}  |  **最低**: {low}'}
            },
            {
                'tag': 'div',
                'text': {'tag': 'lark_md', 'content': '---'}
            },
            {
                'tag': 'div',
                'text': {'tag': 'lark_md', 'content': f'**成交量**: {volume_str}  |  **成交额**: {turnover_str}'}
            },
            {
                'tag': 'div',
                'text': {'tag': 'lark_md', 'content': f'**换手率**: {turnover_rate}%'}
            }
        ]
        
        # 如果有持仓信息，追加持仓数据
        if position and position.quantity > 0:
            try:
                current_price = float(price)
                market_value = position.quantity * current_price
                profit = market_value - position.total_cost
                profit_pct = (profit / position.total_cost * 100) if position.total_cost > 0 else 0
                
                elements.append({'tag': 'div', 'text': {'tag': 'lark_md', 'content': '---'}})
                elements.append({
                    'tag': 'div',
                    'text': {'tag': 'lark_md', 'content': f'**持仓**: {position.quantity}股  |  **成本**: {position.avg_cost:.2f}'}
                })
                elements.append({
                    'tag': 'div',
                    'text': {'tag': 'lark_md', 'content': f'**市值**: {market_value:.2f}  |  **盈利**: {profit:+.2f} ({profit_pct:+.2f}%)'}
                })
            except:
                pass
        
        card = {
            'config': {'wide_screen_mode': True},
            'header': {
                'title': {'tag': 'plain_text', 'content': f'📊 {name} ({code})'},
                'template': template
            },
            'elements': elements
        }
        
        return json.dumps(card)

    def format_quote(self, data: Dict[str, Any]) -> str:
        """格式化行情数据为字符串（完整版）"""
        if 'error' in data:
            return f"错误: {data['error']}"

        lines = []
        lines.append("【A股行情】")
        lines.append("=" * 50)

        # 基础信息
        lines.append(f"股票: {data.get('股票名称', '')} ({data.get('股票代码', '')})")
        lines.append("")
        lines.append(f"当前价: {data.get('当前价格', '-')}")
        lines.append(f"涨跌额: {data.get('涨跌额', '-')}")
        lines.append(f"涨跌幅: {data.get('涨跌幅(%)', '-')}%")
        lines.append("")
        lines.append(f"今开: {data.get('今开价', '-')}")
        lines.append(f"昨收: {data.get('昨收价', '-')}")
        lines.append(f"最高: {data.get('最高价', '-')}")
        lines.append(f"最低: {data.get('最低价', '-')}")
        lines.append("")
        lines.append(f"成交量: {data.get('成交量(手)', '-')} 手")
        lines.append(f"成交额: {data.get('成交额(元)', '-')} 元")
        lines.append(f"换手率: {data.get('换手率(%)', '-')}%")
        lines.append("")
        lines.append(f"市盈率(动态): {data.get('市盈率(动态)', '-')}")
        lines.append(f"市净率: {data.get('市净率', '-')}")
        lines.append(f"总市值: {data.get('总市值(亿元)', '-')} 亿元")
        lines.append(f"流通市值: {data.get('流通市值(亿元)', '-')} 亿元")
        lines.append("")

        # 盘口
        lines.append("【盘口】")
        nums = ['一', '二', '三', '四', '五']
        for n in nums:
            buy_p = data.get(f'买{n}价', '-')
            buy_v = data.get(f'买{n}量(手)', '-')
            sell_p = data.get(f'卖{n}价', '-')
            sell_v = data.get(f'卖{n}量(手)', '-')
            if buy_p and buy_p != '-':
                lines.append(f"买{n}: {buy_p}({buy_v}) → 卖{n}: {sell_p}({sell_v})")

        lines.append("")
        lines.append(f"数据来源: {data.get('_provider', '未知')}")

        return "\n".join(lines)


class BaseProvider:
    """数据源基类"""
    name = "base"
    
    def fetch(self, symbol: str) -> Dict[str, Any]:
        raise NotImplementedError


class TencentProvider(BaseProvider):
    """腾讯财经"""
    name = "腾讯财经"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://finance.qq.com/'
        }
    
    def fetch(self, symbol: str) -> Dict[str, Any]:
        if symbol.startswith(('6', '5', '9')):
            market = 'sh'
        else:
            market = 'sz'
        
        full_code = f'{market}{symbol}'
        url = f'https://qt.gtimg.cn/q={full_code}'
        
        response = requests.get(url, headers=self.headers, timeout=10)
        response.encoding = 'gbk'
        content = response.text
        return self._parse(content, symbol, market)
    
    def _parse(self, content: str, symbol: str, market: str) -> Dict[str, Any]:
        search_str = f'v_{market}{symbol}="'
        idx = content.find(search_str)
        
        if idx == -1:
            return {'error': f'未获取到数据'}
        
        start = idx + len(search_str)
        end = content.find('"', start)
        
        if end == -1:
            return {'error': '数据解析失败'}
        
        data_str = content[start:end]
        
        if not data_str:
            return {'error': '股票代码不存在'}
        
        fields = data_str.split('~')
        
        def safe_float(v, default='0'):
            try:
                return str(float(v)) if v and v != '-' else default
            except:
                return default

        result = {
            '股票名称': fields[1] if len(fields) > 1 else '',
            '股票代码': fields[2] if len(fields) > 2 else symbol,
            '当前价格': fields[3] if len(fields) > 3 else '',
            '昨收价': fields[4] if len(fields) > 4 else '',
            '今开价': fields[5] if len(fields) > 5 else '',
            '成交量(手)': fields[6] if len(fields) > 6 and fields[6] else '',  # field[6]直接就是手
            '成交额(元)': str(int(float(fields[7]) * 1000)) if len(fields) > 7 and fields[7] else '',  # field[7]是仟元，×1000=元
            # 格式化显示（东方财富合并时使用同一字段名，故在此格式化）
            '成交量': f'{float(fields[6]) / 10000:.2f}万手' if len(fields) > 6 and fields[6] else '',
            '成交额': f'{float(fields[7]) * 1000 / 1e8:.2f}亿' if len(fields) > 7 and fields[7] else '',  # 仟元→元→亿
            # 昨收/今开/最高/最低 from Tencent (东方财富这几个字段在集合竞价阶段有误)
            '昨收价': fields[4] if len(fields) > 4 else '',
            '今开价': fields[5] if len(fields) > 5 else '',
            '最高价': fields[33] if len(fields) > 33 else '',
            '最低价': fields[34] if len(fields) > 34 else '',
            '涨跌额': fields[31] if len(fields) > 31 else '',
            '涨跌幅(%)': fields[32] if len(fields) > 32 else '',
            '最高价': fields[33] if len(fields) > 33 else '',
            '最低价': fields[34] if len(fields) > 34 else '',
            '换手率(%)': fields[38] if len(fields) > 38 else '',
            '市盈率(动态)': fields[52] if len(fields) > 52 else '',
            '市净率': fields[46] if len(fields) > 46 else '',
            '总市值(亿元)': fields[45] if len(fields) > 45 else '',
            '流通市值(亿元)': fields[44] if len(fields) > 44 else '',
            '涨停价': fields[47] if len(fields) > 47 else '',
            '跌停价': fields[48] if len(fields) > 48 else '',
            # 买一~买五（腾讯字段: [9,10][11,12][13,14][15,16][17,18]）
            '买一价': fields[9] if len(fields) > 9 else '',
            '买一量(手)': fields[10] if len(fields) > 10 else '',
            '买二价': fields[11] if len(fields) > 11 else '',
            '买二量(手)': fields[12] if len(fields) > 12 else '',
            '买三价': fields[13] if len(fields) > 13 else '',
            '买三量(手)': fields[14] if len(fields) > 14 else '',
            '买四价': fields[15] if len(fields) > 15 else '',
            '买四量(手)': fields[16] if len(fields) > 16 else '',
            '买五价': fields[17] if len(fields) > 17 else '',
            '买五量(手)': fields[18] if len(fields) > 18 else '',
            # 卖一~卖五（腾讯字段: [19,20][21,22][23,24][25,26][27,28]）
            '卖一价': fields[19] if len(fields) > 19 else '',
            '卖一量(手)': fields[20] if len(fields) > 20 else '',
            '卖二价': fields[21] if len(fields) > 21 else '',
            '卖二量(手)': fields[22] if len(fields) > 22 else '',
            '卖三价': fields[23] if len(fields) > 23 else '',
            '卖三量(手)': fields[24] if len(fields) > 24 else '',
            '卖四价': fields[25] if len(fields) > 25 else '',
            '卖四量(手)': fields[26] if len(fields) > 26 else '',
            '卖五价': fields[27] if len(fields) > 27 else '',
            '卖五量(手)': fields[28] if len(fields) > 28 else '',
            # 资金流
            '主力净流入': fields[72] if len(fields) > 72 else '',
            '内盘(主动卖)': fields[73] if len(fields) > 73 else '',
            '外盘(主动买)': fields[74] if len(fields) > 74 else '',
        }
        return result


class SinaProvider(BaseProvider):
    """新浪财经"""
    name = "新浪财经"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
    
    def fetch(self, symbol: str) -> Dict[str, Any]:
        if symbol.startswith(('6', '5', '9')):
            market = 'sh'
        else:
            market = 'sz'
        
        full_code = f'{market}{symbol}'
        url = f'https://hq.sinajs.cn/list=n_{full_code}'
        
        response = requests.get(url, headers=self.headers, timeout=10)
        response.encoding = 'gbk'
        content = response.text
        return self._parse(content, symbol)
    
    def _parse(self, content: str, symbol: str) -> Dict[str, Any]:
        idx = content.find('=')
        if idx == -1:
            return {'error': '未获取到数据'}
        
        data = content[idx+2:-1]
        fields = data.split(',')
        
        if len(fields) < 32:
            return {'error': '数据不完整'}
        
        try:
            current = float(fields[1])
            yesterday = float(fields[2])
            change = current - yesterday
            pct = (change / yesterday * 100) if yesterday else 0
        except:
            change = '0'
            pct = '0'
        
        return {
            '股票名称': fields[0],
            '股票代码': symbol,
            '当前价格': fields[1] if len(fields) > 1 else '',
            '昨收价': fields[2] if len(fields) > 2 else '',
            '今开价': fields[3] if len(fields) > 3 else '',
            '最高价': fields[4] if len(fields) > 4 else '',
            '最低价': fields[5] if len(fields) > 5 else '',
            '成交量(手)': str(int(float(fields[8]) / 100)) if len(fields) > 8 else '',
            '成交额(元)': fields[9] if len(fields) > 9 else '',
            '涨跌额': f'{change:.2f}',
            '涨跌幅(%)': f'{pct:.2f}',
        }


class EastMoneyProvider(BaseProvider):
    """东方财富（主数据源）"""
    name = "东方财富"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
    
    def fetch(self, symbol: str) -> Dict[str, Any]:
        # 扩展字段：行情 + 盘口(买一到买五, 卖一到卖五) + 资金流
        fields = (
            'f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f59,f60,f62,f66,f69,f72,f75,'
            'f116,f117,f162,f164,f167,f168,f169,f170,f171,f173,f177,'
            'f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,'
            'f24,f25,f26,f27,f28,f29,f30,f31,f32,f33'
        )
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={self._get_secid(symbol)}&fields={fields}'
        
        response = requests.get(url, headers=self.headers, timeout=10)
        data = response.json()
        
        return self._parse(data, symbol)
    
    def _get_secid(self, symbol: str) -> str:
        if symbol.startswith(('6', '5', '9')):
            return f'1.{symbol}'
        else:
            return f'0.{symbol}'
    
    def _parse(self, data: dict, symbol: str) -> Dict[str, Any]:
        try:
            d = data.get('data', {})
            if not d:
                return {'error': '未获取到数据'}
            
            def fmt(val, divisor=100, decimal=2):
                """格式化数值字段"""
                if val is None or val == '':
                    return ''
                try:
                    v = float(val) / divisor
                    return f'{v:.{decimal}f}' if decimal else str(int(v))
                except:
                    return str(val)
            
            def fmt_money(val):
                """格式化资金单位（元转万/亿）"""
                if val is None or val == '':
                    return ''
                try:
                    v = float(val)
                    if abs(v) >= 100000000:
                        return f'{v/100000000:.2f}亿'
                    elif abs(v) >= 10000:
                        return f'{v/10000:.2f}万'
                    return str(int(v))
                except:
                    return str(val)
            
            yesterday = float(d.get('f44', 0) or 0) / 100
            current = float(d.get('f43', 0) or 0) / 100
            open_p = float(d.get('f45', 0) or 0) / 100
            high = float(d.get('f46', 0) or 0) / 100
            # f47 不是最低价，用 min(当前, 今开, 昨收) 代替
            low = min(current, open_p, yesterday) if current else 0
            change = float(d.get('f60', 0) or 0) / 100
            pct = (change / yesterday * 100) if yesterday else 0
            
            # f48 = turnover in 分 = vol(股) × price(分)
            f48_val = d.get('f48', 0) or 0
            price_fen = float(d.get('f43', 0) or 1)
            # f117 = 流通市值 in 元
            f117_val = d.get('f117', 0) or 0
            
            result = {
                '股票代码': symbol,
                '股票名称': d.get('f58', ''),
                '当前价格': fmt(d.get('f43')),
                '昨收价': fmt(d.get('f44')),
                '今开价': fmt(d.get('f45')),
                '最高价': fmt(d.get('f46')),
                '最低价': f'{low:.2f}',
                '成交量(手)': str(int((d.get('f47') or 0) / 100)),  # f47是累计成交量(股)，/100=手
                '成交额(元)': str(int(f48_val / 100)),  # f48是累计成交额(分)，/100=元
                '涨跌额': fmt(d.get('f60')),
                '涨跌幅(%)': fmt(d.get('f170'), divisor=100, decimal=2),
                # 换手率 = f48(分) / f117(元) × 100，等价于 f48×100/f117
                '换手率(%)': f'{f48_val * 100 / f117_val:.2f}' if f117_val else '',
                '市盈率(动态)': fmt(d.get('f162'), divisor=100),
                '市净率': fmt(d.get('f167'), divisor=100),
                '总市值(亿元)': fmt(d.get('f116'), divisor=100000000, decimal=2),
                '流通市值(亿元)': fmt(d.get('f117'), divisor=100000000, decimal=2),
                # 买一~买五（按价格降序排列）
                '买一价': fmt(d.get('f14')),
                '买一量(手)': fmt(d.get('f15'), divisor=1),
                '买二价': fmt(d.get('f16')),
                '买二量(手)': fmt(d.get('f17'), divisor=1),
                '买三价': fmt(d.get('f18')),
                '买三量(手)': fmt(d.get('f19'), divisor=1),
                '买四价': fmt(d.get('f20')),
                '买四量(手)': fmt(d.get('f21'), divisor=1),
                '买五价': fmt(d.get('f22')),
                '买五量(手)': fmt(d.get('f23'), divisor=1),
                # 卖一~卖五（按价格升序排列）
                '卖一价': fmt(d.get('f24')),
                '卖一量(手)': fmt(d.get('f25'), divisor=1),
                '卖二价': fmt(d.get('f26')),
                '卖二量(手)': fmt(d.get('f27'), divisor=1),
                '卖三价': fmt(d.get('f28')),
                '卖三量(手)': fmt(d.get('f29'), divisor=1),
                '卖四价': fmt(d.get('f30')),
                '卖四量(手)': fmt(d.get('f31'), divisor=1),
                '卖五价': fmt(d.get('f32')),
                '卖五量(手)': fmt(d.get('f33'), divisor=1),
                # 资金流（东方财富 f62 等字段值过小且非元单位，参考性有限）
                # 实际资金流以腾讯数据为准（见合并阶段）
                '主力净流入': fmt_money(d.get('f62', 0) * 10000) if d.get('f62') else '',
            }
            return result
        except Exception as e:
            return {'error': str(e)}
    
    def _parse_tencent_data(self, content: str, symbol: str, market: str) -> Dict[str, Any]:
        """解析腾讯A股接口返回的数据"""
        
        search_str = f'v_{market}{symbol}="'
        idx = content.find(search_str)
        
        if idx == -1:
            return {'error': f'未获取到数据，股票代码: {symbol}'}
        
        start = idx + len(search_str)
        end = content.find('"', start)
        
        if end == -1:
            return {'error': '数据解析失败'}
        
        data_str = content[start:end]
        
        if not data_str:
            return {'error': '股票代码不存在'}
        
        fields = data_str.split('~')
        
        field_map = {
            0: '市场标识',
            1: '股票名称',
            2: '股票代码',
            3: '当前价格',
            4: '昨收价',
            5: '今开价',
            6: '成交量(手)',
            7: '成交额(元)',
            9: '买一价',
            10: '买一量(手)',
            11: '卖一价',
            12: '卖一量(手)',
            13: '买二价',
            14: '买二量(手)',
            15: '卖二价',
            16: '卖二量(手)',
            30: '日期时间',
            31: '涨跌额',
            32: '涨跌幅(%)',
            33: '最高价',
            34: '最低价',
            36: '成交量(手)',
            37: '成交额(元)',
            38: '换手率(%)',
            39: '市盈率(动态)',
            41: '市净率',
            42: '总市值(亿元)',
            43: '流通市值(亿元)',
            44: '涨停价',
            45: '跌停价',
        }
        
        result = {}
        
        for idx, name in field_map.items():
            if idx < len(fields) and fields[idx]:
                value = fields[idx]
                if value and value != '-' and value != '':
                    result[name] = value
        
        # 附加信息
        result['_股票代码'] = f'{market}{symbol}'
        result['_市场'] = 'A股'
        
        return result
    
    def format_quote(self, data: Dict[str, Any]) -> str:
        """格式化行情数据为字符串（完整版）"""
        if 'error' in data:
            return f"错误: {data['error']}"
        
        lines = []
        lines.append("【A股行情】")
        lines.append("=" * 50)
        
        # 基础信息
        lines.append(f"股票: {data.get('股票名称', '')} ({data.get('股票代码', '')})")
        lines.append(f"市场: {data.get('_市场', 'A股')}")
        lines.append("")
        
        # 价格
        lines.append("【价格】")
        lines.append(f"当前价: {data.get('当前价格', '-')}")
        lines.append(f"涨跌额: {data.get('涨跌额', '-')}")
        lines.append(f"涨跌幅: {data.get('涨跌幅(%)', '-')}%")
        lines.append("")
        
        # 开盘收盘
        lines.append("【开盘收盘】")
        lines.append(f"今开: {data.get('今开价', '-')}")
        lines.append(f"昨收: {data.get('昨收价', '-')}")
        lines.append(f"最高: {data.get('最高价', '-')}")
        lines.append(f"最低: {data.get('最低价', '-')}")
        lines.append("")
        
        # 成交
        lines.append("【成交】")
        lines.append(f"成交量: {data.get('成交量(手)', '-')} 手")
        lines.append(f"成交额: {data.get('成交额(元)', '-')} 元")
        lines.append(f"换手率: {data.get('换手率(%)', '-')}%")
        lines.append("")
        
        # 财务指标
        lines.append("【财务指标】")
        lines.append(f"市盈率(动态): {data.get('市盈率(动态)', '-')}")
        lines.append(f"市净率: {data.get('市净率', '-')}")
        lines.append(f"总市值: {data.get('总市值(亿元)', '-')} 亿元")
        lines.append(f"流通市值: {data.get('流通市值(亿元)', '-')} 亿元")
        lines.append("")
        
        # 涨跌停
        lines.append("【涨跌停】")
        lines.append(f"涨停价: {data.get('涨停价', '-')}")
        lines.append(f"跌停价: {data.get('跌停价', '-')}")
        lines.append("")
        
        # 盘口
        lines.append("【盘口】")
        for i in range(1, 6):
            buy_price = data.get(f'买{i}价', '-')
            buy_vol = data.get(f'买{i}量(手)', '-')
            sell_price = data.get(f'卖{i}价', '-')
            sell_vol = data.get(f'卖{i}量(手)', '-')
            if buy_price != '-' and sell_price != '-':
                lines.append(f"买{i}: {buy_price} ({buy_vol}) → 卖{i}: {sell_price} ({sell_vol})")
        
        lines.append("")
        lines.append(f"更新时间: {data.get('日期时间', '-')}")
        
        return "\n".join(lines)


def get_quote(symbol: str) -> Dict[str, Any]:
    """便捷函数：获取A股行情"""
    fetcher = StockFetcher()
    return fetcher.get_quote(symbol)


def send_feishu(webhook: str, message: str) -> bool:
    """发送消息到飞书
    
    支持两种方式:
    1. Webhook URL (群机器人)
    2. App ID + Secret (私聊)
    """
    import requests
    
    # 方式1: Webhook
    if webhook and webhook.startswith('http'):
        payload = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        try:
            response = requests.post(webhook, json=payload, timeout=30)
            return response.status_code == 200
        except Exception as e:
            print(f"发送失败: {e}")
            return False
    
    return False


def send_feishu_private(message: str, app_id: str = None, app_secret: str = None, receive_id: str = None, is_card: bool = False) -> bool:
    """发送私聊消息到飞书
    
    Args:
        message: 消息内容 (普通文本或卡片JSON)
        app_id: 飞书应用 App ID
        app_secret: 飞书应用 App Secret
        receive_id: 接收者 ID (open_id)
        is_card: 是否为卡片消息格式
    
    Returns:
        是否发送成功
    """
    import requests
    import json as json_mod
    
    if not app_id or not app_secret or not receive_id:
        print("缺少必要参数")
        return False
    
    try:
        # 1. 获取 access_token
        resp = requests.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', json={
            'app_id': app_id,
            'app_secret': app_secret
        }, timeout=30)
        
        if resp.json().get('code') != 0:
            print(f"获取token失败: {resp.json()}")
            return False
        
        token = resp.json()['tenant_access_token']
        
        # 2. 准备消息
        if is_card:
            # 卡片消息
            msg_type = 'interactive'
            content = message  # 已经是 JSON 字符串
        else:
            # 普通文本消息
            msg_type = 'text'
            content = json_mod.dumps({"text": message})
        
        # 3. 直接用 open_id 发送消息
        msg_resp = requests.post(f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id', headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }, json={
            'receive_id': receive_id,
            'msg_type': msg_type,
            'content': content
        }, timeout=30)
        
        result = msg_resp.json()
        if result.get('code') != 0:
            print(f"发送失败: {result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"发送失败: {e}")
        return False


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        code = sys.argv[1].strip()
    else:
        code = input('请输入股票代码: ').strip()
    
    if not code:
        print('请输入股票代码')
        sys.exit(1)
    
    fetcher = StockFetcher()
    result = fetcher.get_quote(code)
    print(fetcher.format_quote(result))
