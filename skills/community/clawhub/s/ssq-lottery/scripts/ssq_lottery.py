#!/usr/bin/env python3
"""
双色球开奖结果查询脚本 (多数据源版)
支持多个数据源自动切换，优先官方渠道，提升获取稳定性

数据源优先级:
1. http://kaijiang.zhcw.com/zhcw/html/ssq/list.html  (中国福彩网 - 官方)
2. http://m.zhcw.com/ssq/  (福彩网手机版 - 官方备用)
3. https://zx.500.com/ssq/  (500 彩票网 - 第三方，新地址)
4. https://lottery.sina.com.cn/ssq/  (新浪彩票 - 第三方)

Usage: python ssq_lottery.py [期号]
Example: 
    python ssq_lottery.py           # 查询最新一期
    python ssq_lottery.py 2026025   # 查询指定期号
"""

import sys
import urllib.request
import urllib.error
import re
from html import unescape


# 数据源配置 (按优先级排序)
DATA_SOURCES = [
    {
        'name': '中国福彩网',
        'url_list': 'http://kaijiang.zhcw.com/zhcw/html/ssq/list.html',
        'url_issue': 'http://kaijiang.zhcw.com/zhcw/html/ssq/{issue}.html',
        'priority': 'official',
        'timeout': 15,
    },
    {
        'name': '福彩网手机版',
        'url_list': 'http://m.zhcw.com/ssq/',
        'url_issue': 'http://m.zhcw.com/ssq/{issue}.html',
        'priority': 'official_backup',
        'timeout': 15,
    },
    {
        'name': '500 彩票网',
        'url_list': 'https://zx.500.com/ssq/',
        'url_issue': 'https://zx.500.com/ssq/',  # 新地址不支持按期号查询，返回列表页
        'priority': 'third_party',
        'timeout': 10,
    },
    {
        'name': '新浪彩票',
        'url_list': 'https://lottery.sina.com.cn/ssq/',
        'url_issue': 'https://lottery.sina.com.cn/ssq/{issue}/',
        'priority': 'third_party',
        'timeout': 10,
    },
]

# HTTP 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'close',
}


def fetch_lottery_page(url: str, timeout: int = 15) -> str:
    """获取彩票网页面内容"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # 尝试检测编码
            content_type = response.headers.get('Content-Type', '')
            charset = 'utf-8'
            if 'charset=' in content_type:
                charset = content_type.split('charset=')[-1].split(';')[0].strip()
            
            raw_html = response.read()
            try:
                html = raw_html.decode(charset)
            except (UnicodeDecodeError, LookupError):
                # 编码检测失败时尝试 utf-8 或 gb2312
                try:
                    html = raw_html.decode('utf-8')
                except:
                    try:
                        html = raw_html.decode('gb2312')
                    except:
                        html = raw_html.decode('utf-8', errors='ignore')
            
            if '404' in html or '无法访问' in html or '页面不存在' in html:
                return f"ERROR:页面不存在 (404)"
            return html
    except urllib.error.HTTPError as e:
        return f"ERROR:HTTP {e.code}"
    except urllib.error.URLError as e:
        return f"ERROR:网络错误 - {e.reason}"
    except Exception as e:
        return f"ERROR:{type(e).__name__} - {str(e)}"


def parse_zhcw(html: str) -> dict:
    """解析中国福彩网数据"""
    result = {'issue': '', 'date': '', 'red_balls': [], 'blue_ball': '', 'prize_pool': '', 'source': '中国福彩网'}
    html = unescape(html)
    
    # 期号
    match = re.search(r'第\s*(\d{7,8})\s*期', html)
    if match:
        result['issue'] = match.group(1)
    
    # 日期
    match = re.search(r'(\d{4}) 年 (\d{1,2}) 月 (\d{1,2}) 日', html)
    if match:
        result['date'] = f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
    else:
        match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
        if match:
            result['date'] = match.group(1)
    
    # 红球
    red_matches = re.findall(r'class="[^"]*ball_red[^"]*"[^>]*>\s*(\d{2})\s*<', html, re.IGNORECASE)
    if not red_matches:
        red_matches = re.findall(r'<td[^>]*>\s*(\d{2})\s*</td>', html)[:6]
    result['red_balls'] = sorted(set(red_matches), key=lambda x: int(x))[:6] if red_matches else []
    
    # 蓝球
    blue_match = re.search(r'class="[^"]*ball_blue[^"]*"[^>]*>\s*(\d{2})\s*<', html, re.IGNORECASE)
    if not blue_match:
        blue_match = re.search(r'<td[^>]*>\s*(\d{2})\s*</td>', html)
        if blue_match:
            all_balls = re.findall(r'<td[^>]*>\s*(\d{2})\s*</td>', html)
            if len(all_balls) >= 7:
                blue_match = type('obj', (object,), {'group': lambda x: all_balls[6]})()
    if blue_match:
        result['blue_ball'] = blue_match.group(1).zfill(2)
    
    # 奖池
    pool_match = re.search(r'奖池.*?(\d[,\d\.]+)\s*亿元', html, re.IGNORECASE)
    if pool_match:
        result['prize_pool'] = pool_match.group(1) + '亿元'
    
    return result


def parse_500(html: str) -> dict:
    """
    解析 500 彩票网数据 (新地址：zx.500.com)
    
    新页面结构:
    - 红球：<li class="redball">XX</li>
    - 蓝球：<li class="blueball">XX</li>
    - 期号：从开奖链接提取 (如 /ssq/n_dt/kj/20260226_699541.shtml)
    """
    result = {'issue': '', 'date': '', 'red_balls': [], 'blue_ball': '', 'prize_pool': '', 'source': '500 彩票网'}
    html = unescape(html)
    
    # 移除 HTML 注释干扰
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 期号：从开奖链接提取 (最新一期的链接)
    # 格式：/ssq/n_dt/kj/20260226_699541.shtml
    # 找所有期号，取第一个（最新）
    matches = re.findall(r'/ssq/n_dt/kj/(\d{8})_\d+\.shtml', html)
    if matches:
        # 取最大的期号（最新一期）
        result['issue'] = max(matches)
    
    # 日期
    match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
    if match:
        result['date'] = match.group(1)
    
    # 红球：<li class="redball">XX</li>
    red_matches = re.findall(r'class="redball">(\d{2})<', html)
    if red_matches:
        result['red_balls'] = red_matches[:6]
    
    # 蓝球：<li class="blueball">XX</li>
    blue_matches = re.findall(r'class="blueball">(\d{2})<', html)
    if blue_matches:
        result['blue_ball'] = blue_matches[0].zfill(2)
    
    # 如果上面的方法失败，回退到旧格式
    if not result['red_balls'] or not result['blue_ball']:
        combo_match = re.search(r'(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})', html)
        if combo_match:
            result['red_balls'] = list(combo_match.groups()[:6])
            result['blue_ball'] = combo_match.group(7).zfill(2) if len(combo_match.groups()) > 6 else ''
    
    return result


def parse_sina(html: str) -> dict:
    """解析新浪彩票数据"""
    result = {'issue': '', 'date': '', 'red_balls': [], 'blue_ball': '', 'prize_pool': '', 'source': '新浪彩票'}
    html = unescape(html)
    
    # 期号
    match = re.search(r'第\s*(\d{7,8})\s*期', html)
    if match:
        result['issue'] = match.group(1)
    
    # 日期
    match = re.search(r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})', html)
    if match:
        result['date'] = match.group(1).replace('年', '-').replace('月', '-').replace('日', '')
    
    # 号码
    numbers = re.findall(r'\b(\d{2})\b', html)
    if len(numbers) >= 7:
        result['red_balls'] = sorted(set(numbers[:6]), key=lambda x: int(x))
        result['blue_ball'] = numbers[6].zfill(2)
    
    return result


def parse_draw(html: str, source_name: str) -> dict:
    """根据数据源选择解析器"""
    if 'zhcw' in source_name.lower() or '福彩' in source_name:
        return parse_zhcw(html)
    elif '500' in source_name:
        return parse_500(html)
    elif 'sina' in source_name or '新浪' in source_name:
        return parse_sina(html)
    else:
        # 通用解析
        return parse_zhcw(html)


def try_data_sources(issue: str = None) -> tuple:
    """按优先级尝试所有数据源"""
    for source in DATA_SOURCES:
        if issue:
            url = source['url_issue'].format(issue=issue)
        else:
            url = source['url_list']
        
        print(f"  尝试 {source['name']}...", file=sys.stderr)
        
        html = fetch_lottery_page(url, source['timeout'])
        
        if not html.startswith("ERROR:"):
            draw = parse_draw(html, source['name'])
            
            # 验证数据完整性
            if draw['issue'] or (len(draw['red_balls']) >= 6 and draw['blue_ball']):
                return (True, draw)
        
        print(f"  ❌ {source['name']} 失败", file=sys.stderr)
    
    return (False, {'error': '所有数据源都无法获取数据'})


def format_draw(draw: dict) -> str:
    """格式化单期开奖信息"""
    lines = []
    
    if draw.get('issue'):
        lines.append(f"🎱 双色球第 {draw['issue']} 期")
    
    if draw.get('date'):
        lines.append(f"📅 开奖日期：{draw['date']}")
    
    if draw.get('red_balls') and len(draw['red_balls']) >= 6:
        red_str = ' '.join(draw['red_balls'][:6])
        lines.append(f"🔴 红球：{red_str}")
    elif draw.get('red_balls'):
        lines.append(f"🔴 红球：{' '.join(draw['red_balls'])} (数据不完整)")
    
    if draw.get('blue_ball'):
        lines.append(f"🔵 蓝球：{draw['blue_ball']}")
    
    if draw.get('prize_pool'):
        lines.append(f"💰 奖池：{draw['prize_pool']}")
    
    # 数据来源
    if draw.get('source'):
        source_type = "官方" if draw['source'] in ['中国福彩网', '福彩网手机版'] else "第三方"
        lines.append(f"📊 数据来源：{draw['source']} ({source_type})")
    
    # 检查数据完整性
    if not draw.get('red_balls') or len(draw['red_balls']) < 6 or not draw.get('blue_ball'):
        lines.append("")
        lines.append("⚠️ 提示：数据可能不完整，建议访问官网核实")
        lines.append("   http://kaijiang.zhcw.com/zhcw/html/ssq/list.html")
    
    # 中奖规则说明
    if draw.get('red_balls') and len(draw['red_balls']) >= 6 and draw.get('blue_ball'):
        lines.append("")
        lines.append("📋 中奖规则：")
        lines.append("   一等奖：6 红 + 1 蓝｜二等奖：6 红 + 0 蓝")
        lines.append("   三等奖：5 红 + 1 蓝｜四等奖：5 红/4 红 +1 蓝")
        lines.append("   五等奖：4 红/3 红 +1 蓝｜六等奖：2 红/1 红/0 红 +1 蓝")
        
        # 第三方数据源提示
        if draw.get('source') not in ['中国福彩网', '福彩网手机版']:
            lines.append("")
            lines.append("⚠️ 提示：第三方数据仅供参考，请以官网为准")
    
    return '\n'.join(lines)


def main():
    print("=" * 50, file=sys.stderr)
    print("双色球开奖结果查询 (多数据源版)", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    # 确定查询模式
    if len(sys.argv) >= 2:
        issue = sys.argv[1]
        print(f"\n查询期号：{issue}", file=sys.stderr)
    else:
        issue = None
        print("\n查询最新开奖...", file=sys.stderr)
    
    print("\n数据源优先级:", file=sys.stderr)
    for i, source in enumerate(DATA_SOURCES, 1):
        print(f"  {i}. {source['name']} ({source['priority']})", file=sys.stderr)
    print(file=sys.stderr)
    
    # 尝试所有数据源
    success, draw = try_data_sources(issue)
    
    print(file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    print(file=sys.stderr)
    
    # 输出结果
    if success:
        output = format_draw(draw)
        print(output)
    else:
        print("❌ 暂时无法获取开奖数据")
        print()
        print("可能原因：")
        print("  1. 网络连接问题")
        print("  2. 所有数据源暂时不可用")
        print("  3. 非开奖时间 (开奖日：周二、四、日)")
        print()
        print("建议访问官网查询：")
        print("  http://kaijiang.zhcw.com/zhcw/html/ssq/list.html")
        sys.exit(1)


if __name__ == '__main__':
    main()
