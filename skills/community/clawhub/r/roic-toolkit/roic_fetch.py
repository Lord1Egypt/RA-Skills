"""
ROIC V2.0 多市场数据获取工具 - 统一框架

支持：
  - A股：finance-data API（CAS 准则）
  - 美股：SEC EDGAR 10-K/20-F HTML 下载 + 本地解析（US GAAP / IFRS）
  - 港股：SEC EDGAR 20-F HTML 下载 + 本地解析（IFRS）

用法：
  python roic_fetch.py 600426.SH 2021-2024          # A股
  python roic_fetch.py BABA 2021-2024               # 美股/中概
  python roic_fetch.py 09988.HK 2021-2024           # 港股（也走SEC 20-F）
  python roic_fetch.py AAPL 2021-2024               # 美股

输出：
  统一 JSON 格式文件，供 roic_engine.py 计算使用
"""

import sys
import os
import json
import urllib.request
import re
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# finance-data API
API_URL = "https://www.codebuddy.cn/v2/tool/financedata"

# SEC EDGAR headers
SEC_HEADERS = {
    "User-Agent": "WorkBuddy Research Agent contact@example.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# =====================================================================
# 市场识别
# =====================================================================

def detect_market(code: str) -> str:
    """根据代码判断市场"""
    code = code.upper().strip()
    if code.endswith('.SH') or code.endswith('.SZ'):
        return 'A'
    elif code.endswith('.HK'):
        return 'HK'
    else:
        # 美股代码（字母）
        if re.match(r'^[A-Z]+$', code):
            return 'US'
        return 'UNKNOWN'


def get_sec_cik(ticker: str) -> str:
    """通过 SEC EDGAR 搜索获取 CIK 号"""
    # 常见公司的 CIK 映射
    KNOWN_CIKS = {
        'BABA': '0001577552',
        'AAPL': '0000320193',
        'GOOGL': '0001652044',
        'MSFT': '0000789019',
        'AMZN': '0001018724',
        'TSLA': '0001318605',
        'META': '0001326801',
        'NVDA': '0001045810',
        'JD': '0001549802',
        'PDD': '0001770767',
        'NTES': '0001195692',
        'TME': '0001727928',
        'BIDU': '0001329084',
        'NIO': '0001744489',
        '9988': '0001577552',  # 阿里巴巴港股
        '09988': '0001577552',
        '0700': '0001023254',  # 腾讯
        '00700': '0001023254',
    }
    
    ticker = ticker.upper().strip()
    if ticker in KNOWN_CIKS:
        return KNOWN_CIKS[ticker]
    
    # 通过 SEC search 获取
    url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={ticker}&type=10-K&dateb=&owner=include&count=1&output=atom'
    req = urllib.request.Request(url, headers={**SEC_HEADERS, 'Accept': 'application/atom+xml'})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        content = resp.read().decode('utf-8', errors='replace')
        match = re.search(r'<cik>(\d+)</cik>', content)
        if match:
            cik = match.group(1).zfill(10)
            print(f'  [SEC] Found CIK: {cik} for {ticker}')
            return cik
    except Exception as e:
        print(f'  [SEC] CIK lookup failed: {e}')
    return None


# =====================================================================
# A股数据获取
# =====================================================================

def fetch_a_share(ts_code: str, years: list) -> list:
    """通过 finance-data API 获取A股数据"""
    print(f'  [A股] 使用 finance-data API 获取 {ts_code}...')
    
    INCOME_FIELDS = [
        "revenue", "oper_cost", "biz_tax_surchg", "sell_exp", "admin_exp", "rd_exp",
        "total_profit", "income_tax", "invest_income", "ass_invest_income", "fin_exp",
    ]
    BS_FIELDS = [
        "total_hldr_eqy_inc_min_int", "st_borr", "lt_borr", "bond_payable", "notes_payable",
        "lease_liab", "money_cap", "trad_asset", "oth_eq_invest", "oth_illiq_fin_assets",
        "deriv_assets", "time_deposits", "goodwill", "lt_eqt_invest", "intang_assets",
        "fix_assets", "cipo", "right_use_asset", "invest_real_estate", "nca_within_1y",
        "oth_cur_assets", "oth_nca", "non_cur_liab_due_1y", "receiv_financing",
    ]
    
    results = []
    for y in years:
        print(f'    获取 {y} 年数据...', end=' ', flush=True)
        try:
            # 利润表
            inc_data = _call_api("income", {"ts_code": ts_code, "period": f"{y}1231", "report_type": "1"}, INCOME_FIELDS)
            if not inc_data.get('items'):
                print(f'[未发布]')
                continue
            inc = dict(zip(inc_data['fields'], inc_data['items'][0]))
            
            # 资产负债表
            bs_data = _call_api("balancesheet", {"ts_code": ts_code, "period": f"{y}1231", "report_type": "1"}, BS_FIELDS)
            if not bs_data.get('items'):
                print(f'[无资产负债表]')
                continue
            bs = dict(zip(bs_data['fields'], bs_data['items'][0]))
            
            # 组装统一格式
            record = _assemble_unified(inc, bs, y, 'A')
            results.append(record)
            print(f'[OK] NOPAT={record["nopat"]/1e8:.1f}亿')
        except Exception as e:
            print(f'[FAIL] {e}')
    
    return results


def _call_api(api_name, params, fields):
    body = {"api_name": api_name, "params": params, "fields": ",".join(fields)}
    data = json.dumps(body).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode('utf-8'))
    if result.get("code") != 0:
        raise Exception(result.get('msg', 'API error'))
    return result["data"]


def _safe_float(d, key, default=0.0):
    v = d.get(key)
    return float(v) if v is not None else default


# =====================================================================
# 美股/港股数据获取（通过 SEC EDGAR 20-F/10-K HTML）
# =====================================================================

def fetch_sec_filing(ticker: str, years: list) -> list:
    """通过 SEC EDGAR 获取美股/港股 20-F/10-K HTML 数据"""
    cik = get_sec_cik(ticker)
    if not cik:
        print(f'  [SEC] 无法获取 CIK，跳过')
        return []
    
    # 获取 filing 列表
    print(f'  [SEC] 搜索 {ticker} (CIK: {cik}) 的年报 filings...')
    filings = _get_sec_filings(cik)
    
    if not filings:
        print(f'  [SEC] 未找到年报 filings')
        return []
    
    print(f'  [SEC] 找到 {len(filings)} 个年报 filings')
    
    results = []
    for filing in filings:
        fy = filing['fy']
        if fy not in years:
            continue
        
        print(f'    FY{fy}: 下载 {filing["filename"]}...', end=' ', flush=True)
        
        # 下载 HTML
        html_path = os.path.join(DATA_DIR, f'{ticker}_FY{fy}.htm')
        if not os.path.exists(html_path):
            try:
                _download_file(filing['url'], html_path)
                print(f'[下载完成]', end=' ', flush=True)
            except Exception as e:
                print(f'[下载失败: {e}]')
                continue
        else:
            print(f'[已缓存]', end=' ', flush=True)
        
        # 解析 HTML
        try:
            record = _parse_sec_html(html_path, fy, filing.get('report_type', '20-F'))
            if record:
                results.append(record)
                print(f'[OK] Equity={record["total_equity"]/1e8:.1f}亿')
            else:
                print(f'[解析失败]')
        except Exception as e:
            print(f'[解析错误: {e}]')
        
        time.sleep(0.5)  # SEC rate limit
    
    return results


def _get_sec_filings(cik: str) -> list:
    """获取 SEC EDGAR 上的年报 filing 列表"""
    filings = []
    seen_fys = set()
    
    # 尝试 20-F 和 10-K
    for filing_type in ['20-F', '10-K']:
        url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={filing_type}&dateb=&owner=include&count=20&output=atom'
        req = urllib.request.Request(url, headers={**SEC_HEADERS, 'Accept': 'application/atom+xml'})
        try:
            resp = urllib.request.urlopen(req, timeout=15)
            content = resp.read().decode('utf-8', errors='replace')
            
            # 解析 Atom feed - entries
            entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
            for entry in entries:
                # 跳过修正文件 (20-F/A, 10-K/A)
                title_match = re.search(r'<title>(.*?)</title>', entry)
                title = title_match.group(1) if title_match else ''
                if '/A ' in title or '/A[' in title:
                    continue
                
                # 提取 index link
                link_match = re.search(r'<link[^>]*href="([^"]*)"', entry)
                if not link_match:
                    continue
                index_url = link_match.group(1)
                
                # 提取 filing date 和 accession number
                filing_date = ''
                accession = ''
                content_match = re.search(r'<content[^>]*>(.*?)</content>', entry, re.DOTALL)
                if content_match:
                    inner = content_match.group(1)
                    fd_match = re.search(r'<filing-date>(\d{4}-\d{2}-\d{2})', inner)
                    if fd_match:
                        filing_date = fd_match.group(1)
                    acc_match = re.search(r'<accession-number>([\d-]+)</accession-number>', inner)
                    if acc_match:
                        accession = acc_match.group(1)
                
                if not accession:
                    # 尝试从 index_url 中提取
                    acc_match = re.search(r'/(\d{10}-\d{2}-\d{6})/', index_url)
                    if acc_match:
                        accession = acc_match.group(1)
                
                if not accession:
                    continue
                
                # 推测财年
                fy = _guess_fy_from_filing(filing_type, filing_date, index_url)
                if fy and fy not in seen_fys:
                    seen_fys.add(fy)
                    
                    # 获取主文档文件名
                    acc_nodash = accession.replace('-', '')
                    filename = _get_filing_document(cik, accession)
                    if filename:
                        doc_url = f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_nodash}/{filename}'
                        filings.append({
                            'fy': fy,
                            'url': doc_url,
                            'filename': filename,
                            'accession': accession,
                            'report_type': filing_type,
                            'filing_date': filing_date,
                            'index_url': index_url,
                        })
                        print(f'    Found FY{fy}: {filename} (filed {filing_date})')
        except Exception as e:
            print(f'    [!] Error fetching {filing_type}: {e}')
        
        time.sleep(0.3)
    
    # 按 FY 排序
    filings.sort(key=lambda x: x['fy'])
    return filings


def _get_filing_document(cik: str, acc: str) -> str:
    """获取 SEC filing 的主文档文件名"""
    # acc format: 0000950170-24-063767
    acc_nodash = acc.replace('-', '')
    index_url = f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_nodash}/{acc_nodash}-index.htm'
    
    try:
        req = urllib.request.Request(index_url, headers=SEC_HEADERS)
        resp = urllib.request.urlopen(req, timeout=15)
        content = resp.read().decode('utf-8', errors='replace')
        
        # 查找主文档（通常是最大的 .htm 文件）
        # 优先匹配常见模式
        patterns = [
            r'href="([a-z]+-\d{8}(?:x20f|x10k)?\.htm)"',  # baba-20240331.htm
            r'href="([a-z]+-\d{4}[-x]?\d*\.htm)"',          # 其他模式
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                # 返回最长的匹配（通常是主文档）
                return max(matches, key=len)
        
        # 兜底：找最大的 .htm 文件
        htm_files = re.findall(r'href="([^"]*\.htm)"', content, re.IGNORECASE)
        if htm_files:
            # 排除 index 文件和表格文件
            candidates = [f for f in htm_files if 'index' not in f.lower() and 'dataset' not in f.lower()]
            if candidates:
                return candidates[0]
    except Exception:
        pass
    
    return None


def _guess_fy_from_filing(filing_type: str, filing_date: str, index_url: str) -> int:
    """从 filing 信息推测财年
    
    20-F（外国公司）：
      - 阿里巴巴：6月发布FY年报（如2025-06发布FY2025）
      - 一般规则：filing_year = FY（大多数4-7月发布的是当年FY）
    
    10-K（美国公司）：
      - 一般11-2月发布，FY = filing_year - 1
    """
    if not filing_date:
        return None
    
    year = int(filing_date[:4])
    month = int(filing_date[5:7])
    
    if '20-F' in filing_type:
        # 20-F: 如果4月或之后发布，FY = filing_year；否则 FY = filing_year - 1
        if month >= 4:
            return year
        else:
            return year - 1
    else:
        # 10-K: 通常在10-2月发布，FY = filing_year - 1
        if month >= 10:
            return year  # 极少数情况
        else:
            return year - 1


def _download_file(url: str, filepath: str):
    """下载文件"""
    req = urllib.request.Request(url, headers=SEC_HEADERS)
    resp = urllib.request.urlopen(req, timeout=60)
    with open(filepath, 'wb') as f:
        f.write(resp.read())


# =====================================================================
# SEC HTML 解析（通用，适用于 10-K 和 20-F）
# =====================================================================

def _parse_sec_html(html_path: str, fy: int, report_type: str) -> dict:
    """解析 SEC 10-K/20-F HTML 文件，提取财务数据"""
    with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    
    # 提取文本内容（去除HTML标签）
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    # 使用 iXBRL 数据属性提取（更精确）
    data = {}
    
    # 定义搜索模式（关键词 → 统一字段名）
    # 注意：需要处理 US GAAP 和 IFRS 两种术语
    search_patterns = [
        # 利润表
        (r'(?:Total )?revenue[s]?\s+([\d,]+)', 'revenue'),
        (r'(?:Total )?cost\s+of\s+revenue\s+([\d,]+)', 'oper_cost'),
        (r'cost\s+(?:of\s+)?(?:goods\s+and\s+services\s+sold|sales)\s+([\d,]+)', 'oper_cost'),
        (r'income\s+from\s+operations\s+([\d,]+)', 'operating_income'),
        (r'operating\s+income\s+([\d,]+)', 'operating_income'),
        (r'income\s+tax(?:\s+expense)?\s+([\d,]+)', 'income_tax'),
        (r'total\s+(?:comprehensive\s+)?income(?:\s+tax)?\s+expense\s+([\d,]+)', 'income_tax'),
        (r'share\s+of\s+(?:results\s+of\s+)?equity\s+method\s+(?:investee|investments)\s+([\d,]+)', 'equity_method_income'),
        (r'equity\s+in\s+(?:earnings|loss(?:es)?)\s+of\s+(?:affiliates|investees)\s+([\d,]+)', 'equity_method_income'),
        (r'research\s+and\s+development\s+([\d,]+)', 'rd_expense'),
        (r'selling.*?administrative\s+expenses?\s+([\d,]+)', 'sga_expense'),
        # 资产负债表
        (r'total\s+equity\s+([\d,]+)', 'total_equity'),
        (r'stockholders[\'\u2019]?\s+equity\s+([\d,]+)', 'total_equity'),
        (r'total\s+assets?\s+([\d,]+)', 'total_assets'),
        (r'total\s+liabilit(?:y|ies)\s+([\d,]+)', 'total_liabilities'),
        (r'cash\s+and\s+cash\s+equivalents?\s+([\d,]+)', 'cash'),
        (r'cash\s+and\s+bank\s+balances\s+([\d,]+)', 'cash'),
        (r'goodwill\s+([\d,]+)', 'goodwill'),
        (r'intangible\s+assets?,?\s+net\s+([\d,]+)', 'intangible_assets'),
        (r'property.*?equipment.*?net\s+([\d,]+)', 'ppe_net'),
        (r'short[\s-]term\s+borrowings?\s+([\d,]+)', 'st_borrowings'),
        (r'long[\s-]term\s+(?:borrowings?|debt)\s+([\d,]+)', 'lt_borrowings'),
        (r'lease\s+liabilit(?:y|ies)\s+([\d,]+)', 'lease_liabilities'),
        (r'investments?\s+in\s+(?:associates?|equity\s+method)\s+(?:and\s+)?(?:joint\s+)?ventures?\s+([\d,]+)', 'equity_investments'),
        (r'other\s+current\s+assets?\s+([\d,]+)', 'other_current_assets'),
        (r'other\s+non[\s-]current\s+assets?\s+([\d,]+)', 'other_noncurrent_assets'),
        (r'right[\s-]of[\s-]use\s+assets?\s+([\d,]+)', 'rou_assets'),
        (r'(?:short[\s-]term|current)\s+investments?\s+([\d,]+)', 'short_term_investments'),
        (r'restricted\s+cash\s+([\d,]+)', 'restricted_cash'),
        (r'loans?\s+and\s+other\s+borrowings?\s+([\d,]+)', 'total_borrowings'),
    ]
    
    # 执行搜索
    for pattern, field_name in search_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # 取最后一个匹配（通常是FY当前年度）
            val_str = matches[-1].replace(',', '')
            try:
                val = float(val_str)
                if field_name not in data:
                    data[field_name] = val
            except ValueError:
                pass
    
    # 如果没有找到 revenue，尝试更多模式
    if 'revenue' not in data:
        for pattern in [r'revenue\s+([\d,]+)', r'(?:net\s+)?sales\s+([\d,]+)']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                val_str = matches[-1].replace(',', '')
                try:
                    data['revenue'] = float(val_str)
                except ValueError:
                    pass
    
    if not data.get('revenue'):
        print(f'[!] 未找到营业收入数据')
        return None
    
    # 组装统一格式
    return _assemble_unified_sec(data, fy, report_type)


# =====================================================================
# 统一数据格式
# =====================================================================

def _assemble_unified(inc: dict, bs: dict, year: int, market: str) -> dict:
    """组装A股统一数据格式"""
    return {
        'year': year,
        'market': market,
        # 利润表（万元 → 元）
        'revenue': _safe_float(inc, 'revenue'),
        'oper_cost': _safe_float(inc, 'oper_cost'),
        'tax_surchg': _safe_float(inc, 'biz_tax_surchg'),
        'sell_exp': _safe_float(inc, 'sell_exp'),
        'admin_exp': _safe_float(inc, 'admin_exp'),
        'rd_expense': _safe_float(inc, 'rd_exp'),
        'sga_expense': _safe_float(inc, 'sell_exp') + _safe_float(inc, 'admin_exp'),
        'operating_income': _safe_float(inc, 'operate_profit'),
        'income_tax': _safe_float(inc, 'income_tax'),
        'equity_method_income': _safe_float(inc, 'ass_invest_income'),
        'net_income': _safe_float(inc, 'n_income'),
        # 资产负债表
        'total_equity': _safe_float(bs, 'total_hldr_eqy_inc_min_int'),
        'total_assets': 0,  # API 未获取
        'total_liabilities': 0,
        'cash': _safe_float(bs, 'money_cap'),
        'short_term_investments': 0,
        'restricted_cash': 0,
        'goodwill': _safe_float(bs, 'goodwill'),
        'intangible_assets': _safe_float(bs, 'intang_assets'),
        'ppe_net': _safe_float(bs, 'fix_assets') + _safe_float(bs, 'cipo'),
        'st_borrowings': _safe_float(bs, 'st_borr'),
        'lt_borrowings': _safe_float(bs, 'lt_borr'),
        'bonds': _safe_float(bs, 'bond_payable'),
        'notes_payable': _safe_float(bs, 'notes_payable'),
        'lease_liabilities': _safe_float(bs, 'lease_liab'),
        'ncl_due_1y': _safe_float(bs, 'non_cur_liab_due_1y'),
        'equity_investments': _safe_float(bs, 'lt_eqt_invest'),
        'other_current_assets': _safe_float(bs, 'oth_cur_assets'),
        'other_noncurrent_assets': _safe_float(bs, 'oth_nca'),
        'rou_assets': _safe_float(bs, 'right_use_asset'),
        'tradable_fin_assets': _safe_float(bs, 'trad_asset'),
        'other_equity_investments': _safe_float(bs, 'oth_eq_invest'),
        'other_illiquid_fin_assets': _safe_float(bs, 'oth_illiq_fin_assets'),
        'deriv_assets': _safe_float(bs, 'deriv_assets'),
        'time_deposits': _safe_float(bs, 'time_deposits'),
        'receiv_financing': _safe_float(bs, 'receiv_financing'),
        'invest_real_estate': _safe_float(bs, 'invest_real_estate'),
        'nca_within_1y': _safe_float(bs, 'nca_within_1y'),
        # 原始数据（用于报告展示）
        'raw_income': inc,
        'raw_bs': bs,
    }


def _assemble_unified_sec(data: dict, fy: int, report_type: str) -> dict:
    """组装SEC filing统一数据格式"""
    return {
        'year': fy,
        'market': 'US' if report_type == '10-K' else 'HK',
        'report_type': report_type,
        'currency': 'CNY',  # 默认假设CNY，后续需检测
        # 利润表
        'revenue': data.get('revenue', 0),
        'oper_cost': data.get('oper_cost', 0),
        'tax_surchg': 0,
        'sell_exp': 0,
        'admin_exp': 0,
        'rd_expense': data.get('rd_expense', 0),
        'sga_expense': data.get('sga_expense', 0),
        'operating_income': data.get('operating_income', 0),
        'income_tax': data.get('income_tax', 0),
        'equity_method_income': data.get('equity_method_income', 0),
        'net_income': data.get('net_income', 0),
        # 资产负债表
        'total_equity': data.get('total_equity', 0),
        'total_assets': data.get('total_assets', 0),
        'total_liabilities': data.get('total_liabilities', 0),
        'cash': data.get('cash', 0),
        'short_term_investments': data.get('short_term_investments', 0),
        'restricted_cash': data.get('restricted_cash', 0),
        'goodwill': data.get('goodwill', 0),
        'intangible_assets': data.get('intangible_assets', 0),
        'ppe_net': data.get('ppe_net', 0),
        'st_borrowings': data.get('st_borrowings', 0),
        'lt_borrowings': data.get('lt_borrowings', 0),
        'bonds': 0,
        'notes_payable': 0,
        'lease_liabilities': data.get('lease_liabilities', 0),
        'ncl_due_1y': 0,
        'equity_investments': data.get('equity_investments', 0),
        'other_current_assets': data.get('other_current_assets', 0),
        'other_noncurrent_assets': data.get('other_noncurrent_assets', 0),
        'rou_assets': data.get('rou_assets', 0),
        'tradable_fin_assets': 0,
        'other_equity_investments': 0,
        'other_illiquid_fin_assets': 0,
        'deriv_assets': 0,
        'time_deposits': 0,
        'receiv_financing': 0,
        'invest_real_estate': 0,
        'nca_within_1y': 0,
        # 原始数据
        'raw_extracted': data,
    }


# =====================================================================
# 主流程
# =====================================================================

DATA_DIR = 'c:/Users/Corey/WorkBuddy/Claw/data/sec_filings'

def parse_years(years_spec: str) -> list:
    if '-' in years_spec:
        parts = years_spec.split('-')
        return list(range(int(parts[0]), int(parts[1]) + 1))
    return [int(y) for y in years_spec.split()]


def main():
    if len(sys.argv) < 3:
        print("用法: python roic_fetch.py <股票代码> <年份范围>")
        print("  A股: python roic_fetch.py 600426.SH 2021-2024")
        print("  美股: python roic_fetch.py AAPL 2021-2024")
        print("  港股: python roic_fetch.py 09988.HK 2021-2024")
        sys.exit(1)
    
    code = sys.argv[1]
    years_spec = " ".join(sys.argv[2:])
    years = parse_years(years_spec)
    
    market = detect_market(code)
    print(f'[ROIC] {code} → 市场: {market}, 年份: {years[0]}-{years[-1]}')
    
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 根据市场选择获取方式
    if market == 'A':
        results = fetch_a_share(code, years)
    elif market in ('US', 'HK'):
        results = fetch_sec_filing(code, years)
    else:
        print(f'[ERROR] 无法识别市场: {code}')
        sys.exit(1)
    
    if not results:
        print(f'\n[FAIL] 未获取到任何数据')
        sys.exit(1)
    
    # 保存结果
    output_file = os.path.join(DATA_DIR, f'{code}_{years[0]}-{years[-1]}_raw.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        # 移除 raw 数据（太大了），只保留数值
        clean_results = []
        for r in results:
            clean = {k: v for k, v in r.items() if not k.startswith('raw_')}
            clean_results.append(clean)
        json.dump(clean_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f'\n[DONE] 数据已保存: {output_file}')
    print(f'  共 {len(results)} 个年度数据')
    
    # 打印摘要
    print(f'\n{"年度":<6} {"市场":<4} {"营业收入":>15} {"股东权益":>15} {"现金":>15} {"商誉":>15}')
    print('-' * 75)
    for r in results:
        rev = r['revenue']
        eq = r['total_equity']
        cash = r['cash']
        gw = r['goodwill']
        unit = '亿元' if max(abs(rev), abs(eq)) > 1e8 else '万元'
        div = 1e8 if unit == '亿元' else 1e4
        print(f'{r["year"]:<6} {r["market"]:<4} {rev/div:>13,.1f}{unit} {eq/div:>13,.1f}{unit} {cash/div:>13,.1f}{unit} {gw/div:>13,.1f}{unit}')


if __name__ == '__main__':
    main()
