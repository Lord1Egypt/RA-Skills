# /// script
# dependencies = ["requests", "pandas"]
# ///
import sys
import argparse
from utils.api_client import api_client

def render_report(data: dict):
    """Render the ScanResult as a nice Markdown report."""
    symbol = data['symbol']
    name = data['name']
    signal = data['signal']
    score = data['composite_score']
    
    # Header
    print(f"# {name} ({symbol}) 多维深度全描报告")
    print(f"\n> **综合评分**: {score} | **投资信号**: {signal}")
    print("\n---")
    
    # Dimensions
    print("## 维度分析")
    for dim, d_data in data['scores'].items():
        dim_cn = {
            "fundamental": "基本面",
            "technical": "技术面",
            "capital_flow": "资金面",
            "sentiment": "情绪面"
        }.get(dim, dim)
        
        emoji = "🟢" if d_data['score'] >= 70 else "🟡" if d_data['score'] >= 40 else "🔴"
        print(f"- {emoji} **{dim_cn} ({d_data['score']})**: {d_data['explanation']}")
    
    # Narrative
    print("\n## AI 深度解读")
    print(data['narrative'])
    
    # Risks
    if data['risk_flags']:
        print("\n## 风险提示")
        for flag in data['risk_flags']:
            print(f"- ⚠️ {flag}")
    
    print("\n---")
    print("*数据来源：Stock Advisor Pro Cloud Backend | Tushare Pro*")

def main():
    parser = argparse.ArgumentParser(description="Deep stock scan")
    parser.add_argument("symbol", help="Stock symbol (e.g. 600519)")
    args = parser.parse_args()
    
    try:
        print(f"正在分析 {args.symbol}，请稍候...")
        data = api_client.get_scan(args.symbol)
        render_report(data)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
