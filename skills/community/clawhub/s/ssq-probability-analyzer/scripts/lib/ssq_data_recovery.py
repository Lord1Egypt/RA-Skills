"""
双色球数据容灾 / 恢复运维工具  (V1.7 新增)

解决"无独立备份源切换开关"短板：把多源下载做成可观测、可强制切换的运维能力。
依赖 ssq_auto 的 download_data / persist_history / validate_data / DATA_SOURCES。

用法：
  python ssq_data_recovery.py status            # 查看当前数据状态 + 最后成功源
  python ssq_data_recovery.py list              # 列出可用数据源及优先级
  python ssq_data_recovery.py force huiniao     # 强制从指定源重新下载并覆盖合并
  python ssq_data_recovery.py force 500         # 强制从500彩票网恢复
  python ssq_data_recovery.py verify            # 完整性自检（期数/格式/期号连续性）
"""
import sys
import json
import os


def _load_auto():
    import ssq_auto
    return ssq_auto


def cmd_status():
    auto = _load_auto()
    print("=" * 60)
    print("数据容灾状态")
    print("=" * 60)
    # 历史数据
    try:
        with open('ssq_history.json', 'r', encoding='utf-8') as f:
            hist = json.load(f)
        print(f"  ssq_history.json: {len(hist)} 期")
        if hist:
            print(f"    最早: {hist[0]['period']} ({hist[0].get('date','')})")
            print(f"    最新: {hist[-1]['period']} ({hist[-1].get('date','')})")
    except Exception as e:
        print(f"  ssq_history.json: 读取失败 ({e})")
    # 最后成功源
    try:
        with open('ssq_data_source.json', 'r', encoding='utf-8') as f:
            src = json.load(f)
        print(f"  最后成功源: {src.get('source')} | 期数: {src.get('count')} | 时间: {src.get('timestamp')}")
    except Exception:
        print("  最后成功源: 无记录 (ssq_data_source.json 不存在)")
    # 优先级
    print(f"  数据源优先级: {[s[0] for s in auto.DATA_SOURCES]}")


def cmd_list():
    auto = _load_auto()
    print("可用数据源（故障转移顺序）：")
    for i, (name, desc) in enumerate(auto.DATA_SOURCES, 1):
        print(f"  {i}. {name} — {desc}")


def cmd_force(source):
    auto = _load_auto()
    valid = [s[0] for s in auto.DATA_SOURCES]
    if source not in valid:
        print(f"✗ 未知数据源 '{source}'。可用: {valid}")
        return 1
    print(f"强制从数据源 '{source}' 重新下载...")
    draws = auto.download_data(force_source=source)
    if not draws:
        print("✗ 下载失败，未改动现有数据。")
        return 1
    draws = auto.persist_history(draws)
    print(f"✓ 已用 '{source}' 恢复，现存 {len(draws)} 期")
    return 0


def cmd_verify():
    auto = _load_auto()
    print("=" * 60)
    print("数据完整性自检")
    print("=" * 60)
    try:
        with open('ssq_history.json', 'r', encoding='utf-8') as f:
            hist = json.load(f)
    except Exception as e:
        print(f"✗ 无法读取 ssq_history.json: {e}")
        return 1
    issues = []
    total = len(hist)
    print(f"  总期数: {total}")
    if total < 100:
        issues.append(f"期数过少({total})")
    # 格式
    bad = 0
    for d in hist:
        if len(d.get('front', [])) != 5 or len(d.get('back', [])) != 2:
            bad += 1
        elif not all(1 <= n <= 35 for n in d['front']) or len(set(d['front'])) != 5:
            bad += 1
        elif not all(1 <= n <= 12 for n in d['back']) or len(set(d['back'])) != 2:
            bad += 1
    if bad:
        issues.append(f"格式错误 {bad} 期")
    # 连续性：正常相邻期号差1；年份跨界跳变很大(如 07153->08001, ~+848)属正常，
    # 仅当跳变在 (1, 100) 之间才视为"年内缺期"。
    gaps = []
    for i in range(1, total):
        diff = int(hist[i]['period']) - int(hist[i-1]['period'])
        if 1 < diff < 100:
            gaps.append((hist[i-1]['period'], hist[i]['period']))
    if gaps:
        issues.append(f"疑似年内缺期 {len(gaps)} 处: {gaps[:5]}")
    if issues:
        print(f"✗ 发现问题:")
        for x in issues:
            print(f"   - {x}")
        return 1
    print("✓ 完整性通过（期数/格式/连续性均正常）")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    if cmd == 'status':
        cmd_status()
    elif cmd == 'list':
        cmd_list()
    elif cmd == 'force' and len(sys.argv) > 2:
        return cmd_force(sys.argv[2])
    elif cmd == 'verify':
        return cmd_verify()
    else:
        print(__doc__)
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
