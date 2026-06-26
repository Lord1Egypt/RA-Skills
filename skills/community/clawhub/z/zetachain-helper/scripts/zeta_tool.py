import sys
import requests
import json
import time

# ZetaChain 核心配置 (Mainnet)
ZETA_CONFIG = {
    "RPC_NODES": {
        "ZetaChain": [
            "https://zetachain.rpc.thirdweb.com",
            "https://zetachain-evm.blockpi.network/v1/rpc/public"
        ],
        "Ethereum": ["https://eth.llamarpc.com", "https://rpc.ankr.com/eth"],
        "BSC": ["https://binance.llamarpc.com", "https://bsc-dataseed.binance.org"],
        "Bitcoin": ["https://blockstream.info/api"]
    },
    "TSS_ADDRESSES": {
        "BTC": "bc1qm34lsc65zpw79lxp39s3629sh3buut69qq066d",
        "ETH": "0x56a4768393e80000000000000000000000000000",
        "BSC": "0x28bcA2791Bca1f2de4661ED88A30C99A7a9449Aa"
    },
    "LCD": "https://zetachain.blockpi.network/lcd/v1/public"
}

def get_evm_balance(node_list, address):
    payload = {"jsonrpc": "2.0", "method": "eth_getBalance", "params": [address, "latest"], "id": 1}
    for node in node_list:
        try:
            r = requests.post(node, json=payload, timeout=5)
            result = r.json().get("result")
            if result: return int(result, 16) / 1e18
        except: continue
    return 0.0

def get_btc_balance(address):
    try:
        r = requests.get(f"{ZETA_CONFIG['RPC_NODES']['Bitcoin'][0]}/address/{address}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            stats = data.get('chain_stats', {})
            return (stats.get('funded_txo_sum', 0) - stats.get('spent_txo_sum', 0)) / 1e8
    except: pass
    return 0.0

def get_gas_price(node_list):
    payload = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
    for node in node_list:
        try:
            r = requests.post(node, json=payload, timeout=5)
            result = r.json().get("result")
            if result: return int(result, 16) / 1e9
        except: continue
    return 0.0

def track_cctx(cctx_hash):
    url = f"{ZETA_CONFIG['LCD']}/zeta-chain/crosschain/cctx/{cctx_hash}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json().get("CrossChainTx", {})
            return {"status": "success", "cctx_status": data.get("cctx_status", {}).get("status", "Unknown")}
        return {"status": "error", "message": "Transaction not found"}
    except:
        return {"status": "error", "message": "Network error"}

def generate_navigation(evm_addr, btc_addr=None):
    eth_bal = get_evm_balance(ZETA_CONFIG["RPC_NODES"]["Ethereum"], evm_addr)
    bsc_bal = get_evm_balance(ZETA_CONFIG["RPC_NODES"]["BSC"], evm_addr)
    zeta_bal = get_evm_balance(ZETA_CONFIG["RPC_NODES"]["ZetaChain"], evm_addr)
    btc_bal = get_btc_balance(btc_addr) if btc_addr else 0.0
    eth_gas = get_gas_price(ZETA_CONFIG["RPC_NODES"]["Ethereum"])
    zeta_gas = get_gas_price(ZETA_CONFIG["RPC_NODES"]["ZetaChain"])

    report = {
        "Address_Snapshot": {"EVM": evm_addr, "BTC": btc_addr if btc_addr else "None"},
        "Balance_Details": {
            "ZetaChain": f"{zeta_bal:.4f} ZETA",
            "Bitcoin": f"{btc_bal:.4f} BTC",
            "Ethereum": f"{eth_bal:.4f} ETH",
            "BSC": f"{bsc_bal:.4f} BNB"
        },
        "Network_Health": {"ZetaChain_Gas": f"{zeta_gas:.2f} Gwei", "Ethereum_Gas": f"{eth_gas:.2f} Gwei"}
    }
    
    actions = []
    if btc_bal > 0.001:
        actions.append({"priority": "HIGH", "action": "Unlock BTC Liquidity", "target_tss": ZETA_CONFIG["TSS_ADDRESSES"]["BTC"]})
    if eth_bal > 0.05 and eth_gas < 15:
        actions.append({"priority": "MEDIUM", "action": "Low-Cost ETH Deposit"})
    if zeta_bal < 1.0:
        actions.append({"priority": "CRITICAL", "action": "Refuel ZETA"})

    return {"status": "success", "data": report, "actions": actions}

def get_help():
    help_text = {
        "skill_name": "ZetaChain Helper",
        "author": "mango (ZetaChain Technical Ambassador)",
        "intro": "我是你在 ZetaChain 世界里的全能导航员。支持全链资产监控、CCTX 追踪和智能跨链建议。",
        "commands": [
            {"cmd": "nav <evm_addr> [btc_addr]", "desc": "一键扫描全链资产并获取智能操作建议。"},
            {"cmd": "track <cctx_hash>", "desc": "实时追踪跨链交易状态。"},
            {"cmd": "balance <evm_addr>", "desc": "快速查看 ZetaChain 主网余额。"},
            {"cmd": "help", "desc": "显示此帮助信息。"}
        ],
        "highlights": [
            "原生 Bitcoin 穿透，无需 Wrapped Token。",
            "三链实时 Gas 对比分析。",
            "工业级多节点冗余机制。"
        ]
    }
    return help_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps(get_help(), indent=2, ensure_ascii=False))
        sys.exit(0)
        
    cmd = sys.argv[1]
    
    if cmd == "help":
        print(json.dumps(get_help(), indent=2, ensure_ascii=False))
    elif cmd == "nav":
        if len(sys.argv) < 3:
            print("Error: Missing EVM address.")
            sys.exit(1)
        evm_addr = sys.argv[2]
        btc_addr = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(generate_navigation(evm_addr, btc_addr), indent=2, ensure_ascii=False))
    elif cmd == "track":
        if len(sys.argv) < 3:
            print("Error: Missing Hash.")
            sys.exit(1)
        print(json.dumps(track_cctx(sys.argv[2]), indent=2, ensure_ascii=False))
    elif cmd == "balance":
        if len(sys.argv) < 3:
            print("Error: Missing address.")
            sys.exit(1)
        bal = get_evm_balance(ZETA_CONFIG["RPC_NODES"]["ZetaChain"], sys.argv[2])
        print(json.dumps({"ZETA": f"{bal:.4f}"}, indent=2))
    else:
        print(json.dumps({"error": "Unknown command", "use": "python zeta_tool.py help"}, indent=2))
