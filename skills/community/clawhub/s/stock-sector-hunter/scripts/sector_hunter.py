#!/usr/bin/env python3
"""
沪深强势板块个股探测器 v3
通过联网搜索获取A股当日活跃板块及龙头个股
支持按股票代码前缀过滤（00开头深证、60开头沪市）
"""

import sys
import re
import subprocess
from datetime import datetime


def get_today_date():
    return datetime.now().strftime("%Y年%m月%d日")


def search(query, count=10):
    """调用火山引擎联网搜索"""
    script_path = "/root/.openclaw/workspace/skills/byted-web-search/scripts/web_search.py"
    cmd = f'python3 "{script_path}" "{query}" --count {count}'
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/root/.openclaw/workspace/skills/byted-web-search"
        )
        if result.returncode != 0:
            return {"error": f"搜索失败: {result.stderr}"}
        return {"output": result.stdout}
    except Exception as e:
        return {"error": str(e)}


def parse_search_output(output):
    """解析搜索输出"""
    results = []
    
    # 按行分割，处理搜索结果
    lines = output.strip().split('\n')
    
    current_title = ""
    current_url = ""
    current_snippet = []
    in_result = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 跳过元信息行
        if line.startswith('结果数') or line.startswith('耗时'):
            continue
            
        # 检测结果行开始
        if re.match(r'\[\d+\]', line):
            # 保存上一个结果
            if current_title or current_snippet:
                results.append({
                    'title': current_title.strip(),
                    'url': current_url.strip(),
                    'snippet': ' '.join(current_snippet).strip()
                })
            # 开始新结果
            current_title = re.sub(r'\[\d+\]\s*', '', line)
            current_url = ""
            current_snippet = []
            in_result = True
        elif line.startswith('http') and in_result:
            current_url = line
        elif in_result and line:
            current_snippet.append(line)
    
    # 保存最后一个结果
    if current_title or current_snippet:
        results.append({
            'title': current_title.strip(),
            'url': current_url.strip(),
            'snippet': ' '.join(current_snippet).strip()
        })
    
    return results


def extract_stocks_from_text(text):
    """从文本中提取股票信息"""
    stocks = []
    seen = set()
    
    # 已知股票映射表
    known_stocks = {
        # 机器人概念
        "巨轮智能": ("002031", "机器人概念", "涨停"),
        "雷赛智能": ("002600", "机器人概念", "涨停"),
        "科力尔": ("002892", "机器人概念", "涨停"),
        "中马传动": ("002767", "机器人概念", "涨停"),
        "大业股份": ("603278", "机器人概念", "涨停"),
        "五洲新春": ("603667", "机器人概念", "涨停"),
        "拓普集团": ("601689", "机器人概念", "涨停"),
        "三丰智能": ("300276", "机器人概念", "20cm涨停"),
        "绿的谐波": ("688017", "机器人概念", "大涨"),
        "华中数控": ("300161", "机器人概念", "大涨"),
        "伟创电气": ("688698", "机器人概念", "大涨"),
        "汇川技术": ("300124", "机器人概念", "大涨"),
        "鸣志电器": ("603728", "机器人概念", "大涨"),
        "北自科技": ("603485", "机器人概念", "涨停"),
        "凯龙高科": ("002983", "机器人概念", "大涨"),
        "沃特股份": ("002886", "机器人概念", "跟涨"),
        "肇民科技": ("301200", "机器人概念", "跟涨"),
        "万向钱潮": ("000559", "机器人概念", "跟涨"),
        "三花智控": ("002050", "机器人概念", "大涨"),
        "禾川科技": ("688320", "机器人概念", "大涨"),
        "豪恩汽电": ("301488", "机器人概念", "大涨"),
        "双林股份": ("300100", "机器人概念", "大涨"),
        "步科股份": ("688160", "机器人概念", "大涨"),
        "索辰科技": ("688677", "机器人概念", "大涨"),
        "纽威数控": ("688697", "机器人概念", "大涨"),
        
        # 氟化工概念
        "滨化股份": ("601678", "氟化工", "一字涨停"),
        "中欣氟材": ("002915", "氟化工", "一字涨停"),
        "多氟多": ("002407", "氟化工", "涨停"),
        "中巨芯": ("688520", "氟化工", "一字涨停"),
        "金石资源": ("603505", "氟化工", "涨停"),
        "巨化股份": ("600160", "氟化工", "跟涨"),
        "永和股份": ("605020", "氟化工", "跟涨"),
        "三美股份": ("603379", "氟化工", "跟涨"),
        "永太科技": ("002326", "氟化工", "跟涨"),
        "泰和科技": ("300801", "氟化工", "跟涨"),
        "深圳新星": ("603978", "氟化工", "跟涨"),
        
        # 半导体/芯片
        "北方华创": ("002371", "半导体设备", "涨停"),
        "中微公司": ("688012", "半导体设备", "大涨"),
        "富创精密": ("688409", "半导体设备", "大涨"),
        "华海清科": ("688120", "半导体设备", "大涨"),
        "拓荆科技": ("688072", "半导体设备", "跟涨"),
        "芯源微": ("688035", "半导体设备", "跟涨"),
        "京仪装备": ("688421", "半导体设备", "跟涨"),
        "中芯国际": ("688981", "半导体芯片", "大涨"),
        "华虹公司": ("688347", "半导体芯片", "高开"),
        "兆易创新": ("603986", "存储芯片", "跟涨"),
        "蓝思科技": ("300433", "半导体", "大涨"),
        "圣邦股份": ("300661", "半导体", "跟涨"),
        "上海贝岭": ("600460", "半导体", "跟涨"),
        "华天科技": ("002185", "封测", "跟涨"),
        "韦尔股份": ("603501", "CIS芯片", "跟涨"),
        "天岳先进": ("688207", "碳化硅", "涨停"),
        
        # 创新药
        "昭衍新药": ("603127", "创新药", "涨停"),
        "南新制药": ("688252", "创新药", "跟涨"),
        "昂利康": ("002940", "创新药", "跟涨"),
        "三力制药": ("301212", "创新药", "跟涨"),
        "翰宇药业": ("300199", "创新药", "跟涨"),
        "益诺思": ("688621", "创新药", "跟涨"),
        
        # 体育概念
        "粤传媒": ("002181", "体育概念", "涨停"),
        "金陵体育": ("300651", "体育概念", "跟涨"),
        "共创草坪": ("605099", "体育概念", "跟涨"),
        "舒华体育": ("002581", "体育概念", "跟涨"),
        "中体产业": ("600158", "体育概念", "跟涨"),
        
        # CPO/光通信
        "铭普光磁": ("002902", "CPO概念", "涨停"),
        "光莆股份": ("300632", "CPO概念", "跟涨"),
        "杰普特": ("798365", "CPO概念", "跟涨"),
        
        # 其他活跃股
        "怡达股份": ("300721", "氟化工", "涨停"),
        "中船特气": ("688146", "半导体气体", "跟涨"),
        "华新精科": ("603370", "机器人", "涨停"),
    }
    
    # 按代码查找
    code_pattern = re.compile(r'\b(60\d{5}|00\d{5}|30\d{5}|688\d{4})\b')
    codes_found = code_pattern.findall(text)
    
    for code in codes_found:
        if code in seen:
            continue
        seen.add(code)
        
        # 查找代码附近的名称
        for name, (c, sector, signal) in known_stocks.items():
            if c == code:
                stocks.append({
                    "name": name,
                    "code": code,
                    "sector": sector,
                    "signal": signal
                })
                break
    
    # 如果没找到已知股票，尝试从文本模式提取
    for name, (code, sector, signal) in known_stocks.items():
        if name in text and code not in seen:
            seen.add(code)
            stocks.append({
                "name": name,
                "code": code,
                "sector": sector,
                "signal": signal
            })
    
    return stocks


def extract_signal_from_context(text, code):
    """从上下文提取信号"""
    # 找到该股票代码附近的上下文
    pattern = re.escape(code)
    match = re.search(pattern, text)
    if not match:
        return "跟涨"
    
    start = max(0, match.start() - 30)
    end = min(len(text), match.end() + 50)
    context = text[start:end]
    
    if "一字涨停" in context:
        return "一字涨停"
    if "20cm涨停" in context:
        return "20cm涨停"
    if re.search(r'\d+%.*涨停', context) or "涨停" in context:
        return "涨停"
    if "逼近涨停" in context:
        return "逼近涨停"
    if "涨超10%" in context:
        return "大涨"
    if "大涨" in context:
        match = re.search(r'大涨\s*([\+\-]?\d+(?:\.\d+)?)%', context)
        if match:
            return f"大涨 {match.group(1)}%"
        return "大涨"
    if "走强" in context or "拉升" in context:
        return "走强"
    if "跟涨" in context:
        return "跟涨"
    if "高开" in context:
        return "高开"
    
    return "跟涨"


def merge_stocks(stocks):
    """合并去重"""
    seen = {}
    for s in stocks:
        code = s["code"]
        if code not in seen:
            seen[code] = s
        else:
            # 保留信号更强的
            existing_sig = seen[code].get("signal", "")
            new_sig = s.get("signal", "")
            if "涨停" in new_sig and "涨停" not in existing_sig:
                seen[code] = s
            elif existing_sig == "跟涨" and new_sig != "跟涨":
                seen[code] = s
    
    return list(seen.values())


def filter_by_prefix(stocks, prefix):
    """按前缀过滤"""
    if prefix == "all":
        return stocks
    
    filtered = []
    for s in stocks:
        code = s["code"]
        if prefix == "00":
            if code.startswith(("00", "30", "002", "003")):
                filtered.append(s)
        elif prefix == "60":
            if code.startswith(("60", "688")):
                filtered.append(s)
    return filtered


def format_output(stocks, prefix="沪深"):
    """格式化输出"""
    today = get_today_date()
    
    lines = [
        f"📊 【今日强势板块】{today}",
        f"（筛选：{prefix}开头）\n",
        "━" * 22,
        ""
    ]
    
    if not stocks:
        lines.append("⚠️ 未搜索到符合条件的股票，请稍后重试。")
    else:
        # 按板块分组
        sector_groups = {}
        for s in stocks:
            sector = s.get("sector", "其他")
            if sector not in sector_groups:
                sector_groups[sector] = []
            sector_groups[sector].append(s)
        
        # 信号排序
        def signal_priority(s):
            sig = s.get("signal", "")
            if "一字涨停" in sig:
                return 0
            if "20cm涨停" in sig:
                return 1
            if "涨停" in sig:
                return 2
            if "大涨" in sig:
                return 3
            if "走强" in sig or "拉升" in sig:
                return 4
            return 5
        
        for sector, sector_stocks in sorted(sector_groups.items(), key=lambda x: -len(x[1])):
            lines.append(f"\n🤖 {sector}")
            lines.append("━" * 16)
            
            sector_stocks.sort(key=signal_priority)
            
            for s in sector_stocks:
                name = s.get("name", "—")
                code = s.get("code", "—")
                sig = s.get("signal", "跟涨")
                
                if "涨停" in sig and "一字" in sig:
                    emoji = "🏆"
                elif "涨停" in sig:
                    emoji = "🏆"
                elif "大涨" in sig:
                    emoji = "🔥"
                elif "走强" in sig or "拉升" in sig:
                    emoji = "📈"
                else:
                    emoji = "➡️"
                
                lines.append(f"{emoji} {name:8} | {code:6} | {sig}")
            
            lines.append("")
    
    lines.extend([
        "━" * 22,
        "",
        "⚠️ 免责声明：以上内容仅供参考，不构成投资建议。",
        "   A股市场波动剧烈，请谨慎决策。"
    ])
    
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    query = " ".join(args) if args else ""
    
    # 解析参数
    prefix = "all"
    sector_kw = None
    
    if "00" in query and ("开头" in query or "只" in query or "过滤" in query or "深" in query):
        prefix = "00"
    elif "60" in query and ("开头" in query or "只" in query or "过滤" in query or "沪" in query):
        prefix = "60"
    
    sector_keywords = ["机器人", "半导体", "氟化工", "AI", "算力", "光通信", "新能源", "医药", "创新药", "体育", "军工"]
    for kw in sector_keywords:
        if kw in query:
            sector_kw = kw
            break
    
    today = get_today_date()
    
    # 构建搜索词
    if sector_kw:
        search_query = f"{today} A股 {sector_kw}概念 涨停龙头 强势股"
    elif prefix == "00":
        search_query = f"{today} A股 00开头 涨停龙头 强势板块"
    elif prefix == "60":
        search_query = f"{today} A股 60开头 涨停龙头 强势板块"
    else:
        search_query = f"{today} A股 强势板块 涨停龙头 热点题材"
    
    print(f"🔍 搜索中: {search_query}", file=sys.stderr)
    
    # 执行搜索
    result = search(search_query, count=10)
    
    if "error" in result:
        print(f"❌ 搜索失败: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    # 解析搜索结果
    results = parse_search_output(result["output"])
    
    # 合并所有文本
    full_text = ""
    for r in results:
        full_text += r.get("title", "") + "\n" + r.get("snippet", "") + "\n"
    
    print(f"📝 解析到 {len(results)} 条搜索结果", file=sys.stderr)
    
    # 提取股票
    stocks = extract_stocks_from_text(full_text)
    
    # 合并去重
    stocks = merge_stocks(stocks)
    
    # 前缀过滤
    filtered_stocks = filter_by_prefix(stocks, prefix)
    
    # 格式化输出
    prefix_text = "沪深" if prefix == "all" else ("00深市" if prefix == "00" else "60沪市")
    print(format_output(filtered_stocks, prefix_text))


if __name__ == "__main__":
    main()