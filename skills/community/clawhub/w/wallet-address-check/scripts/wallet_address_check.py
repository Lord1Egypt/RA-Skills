import argparse, json, re, sys

B58 = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{26,35}$")
B32 = re.compile(r"^bc1[02-9ac-hj-np-z]{11,71}$")
HEX = re.compile(r"^0x[0-9a-fA-F]{40}$")

def main():
    ap = argparse.ArgumentParser(description="wallet-address-check · 链上地址格式校验（零依赖）")
    ap.add_argument("--address", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    addr = a.address.strip()
    chains, ok, notes = [], False, []
    if HEX.match(addr):
        chains.append("EVM(ETH/BSC/Polygon等)")
        if addr[2:].islower() or addr[2:].isupper():
            ok = True
        else:
            notes.append("EVM混合大小写属EIP-55校验和格式，本工具零依赖无法重算keccak，请用钱包软件复核后再转账")
    elif B32.match(addr):
        chains.append("Bitcoin(bech32/bc1)")
        ok = True
    elif B58.match(addr):
        if addr.startswith("T") and len(addr) == 34:
            chains.append("TRON(Base58)")
        else:
            chains.append("Bitcoin(Base58)等Base58系")
        ok = True
        notes.append("Base58地址未做双哈希校验和验证，大额转账请先小额试转")
    else:
        chains.append("无法识别")
        notes.append("格式不符合常见EVM/BTC系/TRON地址")
    masked = addr if len(addr) <= 12 else addr[:6] + "..." + addr[-4:]
    if a.json:
        print(json.dumps({"pass": ok, "address_masked": masked, "chains": chains, "notes": notes},
                         ensure_ascii=False, indent=2))
    else:
        print("地址：" + masked)
        print("链系：" + "、".join(chains))
        print("  判定：" + ("PASS 格式可接受" if ok else "FAIL 格式可疑，请勿直接转账"))
        for n in notes:
            print("    - " + n)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
