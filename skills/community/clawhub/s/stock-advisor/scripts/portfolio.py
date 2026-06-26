# /// script
# dependencies = ["requests", "pandas"]
# ///
import sys
import argparse
from utils.config import PORTFOLIO_FILE
from utils.local_store import LocalStore

store = LocalStore(PORTFOLIO_FILE)

def add_stock(symbol: str, cost: float, quantity: int):
    data = store.load()
    data[symbol] = {
        "cost": cost,
        "quantity": quantity,
        "added_at": sys.prefix # Placeholder for timestamp logic if needed
    }
    store.save(data)
    print(f"✅ 已添加持仓: {symbol} (成本: {cost}, 数量: {quantity})")

def show_portfolio():
    data = store.load()
    if not data:
        print("当前无本地持仓数据。")
        return
    
    print("# 本地持仓清单")
    print("| 股票代码 | 持仓成本 | 持仓数量 |")
    print("| --- | --- | --- |")
    for symbol, info in data.items():
        print(f"| {symbol} | {info['cost']} | {info['quantity']} |")

def remove_stock(symbol: str):
    data = store.load()
    if symbol in data:
        del data[symbol]  # pyrefly: ignore[bad-argument-count]
        store.save(data)
        print(f"✅ 已删除持仓: {symbol}")
    else:
        print(f"未找到持仓: {symbol}")

def main():
    parser = argparse.ArgumentParser(description="Portfolio Management")
    subparsers = parser.add_subparsers(dest="command")
    
    # Show
    subparsers.add_parser("show")
    
    # Add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("symbol")
    add_parser.add_argument("--cost", type=float, required=True)
    add_parser.add_argument("--quantity", type=int, required=True)
    
    # Remove
    rem_parser = subparsers.add_parser("remove")
    rem_parser.add_argument("symbol")
    
    args = parser.parse_args()
    
    if args.command == "show":
        show_portfolio()
    elif args.command == "add":
        add_stock(args.symbol, args.cost, args.quantity)
    elif args.command == "remove":
        remove_stock(args.symbol)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
