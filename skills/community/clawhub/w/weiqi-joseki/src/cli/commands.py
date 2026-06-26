#!/usr/bin/env python3
"""
简化版CLI - 仅支持KataGo定式库
"""

import argparse
import sys
from pathlib import Path

from ..storage import JsonStorage, DEFAULT_DB_PATH
from ..builder import KatagoJosekiBuilder, convert_to_rudl
from ..discover import discover_joseki
from ..extraction import extract_moves_all_corners, convert_to_multigogm

from ..auto import AutoState
from ..extraction.katago_downloader import download_auto


def cmd_init(args):
    """初始化空数据库"""
    storage = JsonStorage(args.db)
    storage.clear()
    print(f"✅ 已初始化空数据库: {storage.db_path}")


def _cmd_katago_auto(args):
    """自动增量构建模式（简化版）
    
    核心逻辑：
    1. 初始化AutoState（只保留配置）
    2. 调用 download_auto() 下载新日期的棋谱
    3. 调用 builder.run_auto() 完成构建流程：
       - 提取所有未提取的tar到temp
       - 实时更新CMS并保存
       - 重建定式库
    """
    
    # 1. 初始化/加载 AutoState
    state = AutoState()
    
    if not state.is_initialized() or args.force_rebuild:
        if args.force_rebuild:
            print("🔄 强制重建模式，清除现有状态...")
            state.reset()
        print("🆕 初始化自动构建配置...")
        state.init_config()
        print(f"   CMS配置: width={state.config['cms_width']}, depth={state.config['cms_depth']}")
    else:
        print(f"📋 加载现有配置")
    
    # 2. 准备缓存目录
    cache_dir = Path.home() / ".weiqi-joseki" / "katago-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. 下载新日期的棋谱（如果存在）
    print("\n📥 检查并下载新棋谱...")
    downloaded = download_auto(state, cache_dir=cache_dir)
    if downloaded:
        print(f"   ✅ 下载完成: {len(downloaded)} 个新日期")
    else:
        print("   ℹ️  没有新日期需要下载")
    
    # 4. 创建 Builder 并执行自动流程（提取、CMS、重建）
    builder = KatagoJosekiBuilder(db_path=args.db)
    
    result = builder.run_auto(state, cache_dir, limit=args.limit)
    
    if result:
        print(f"\n✅ 自动构建完成，共 {len(result)} 条定式")
        return 0
    else:
        print("\n⏭️  没有新数据，跳过")
        return 0


def _cmd_katago_custom(args):
    """自定义构建模式（原katago命令逻辑）"""
    from datetime import datetime, timedelta
    from ..extraction.katago_downloader import download_katago_games
    
    # 检查必需参数
    if not args.start_date or not args.end_date:
        print("❌ 错误: custom模式需要指定 --start-date 和 --end-date")
        return 1
    
    # 配置
    CACHE_DIR = Path.home() / ".weiqi-joseki/katago-cache"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 解析日期
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        print("❌ 错误: 日期格式应为 YYYY-MM-DD")
        sys.exit(1)
    
    if start_date > end_date:
        print("❌ 错误: 起始日期不能晚于结束日期")
        sys.exit(1)
    
    # 生成日期列表
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    
    print(f"📅 日期范围: {args.start_date} 至 {args.end_date}（共{len(dates)}天）")
    print(f"💾 缓存目录: {CACHE_DIR}")
    print(f"🗄️  数据库: {args.db}")
    print()
    
    # 下载阶段
    print(f"📥 开始下载/检查缓存...")
    
    downloaded_files, missing_dates = download_katago_games(
        start_date=args.start_date,
        end_date=args.end_date,
        cache_dir=CACHE_DIR,
        max_retries=3,
        workers=1,
        keep_cache=True,
        delay=args.delay
    )
    
    print(f"✅ 文件准备完成: {len(downloaded_files)}/{len(dates)} 个")
    if missing_dates:
        print(f"⚠️  未找到: {len(missing_dates)} 个日期")
    print()
    
    if not downloaded_files:
        print("❌ 没有可处理的文件")
        return 1
    
    # 仅下载模式
    if args.download_only:
        print("✅ 下载完成，跳过定式库构建")
        return 0
    
    # 构建定式库
    print(f"⏳ 开始构建定式库...")
    print(f"   参数: first-n={args.first_n}, min-freq={args.min_freq}, top-k={args.top_k}")
    print()
    
    builder = KatagoJosekiBuilder(args.db)
    
    joseki_list = builder.build_from_files(
        downloaded_files,
        min_freq=args.min_freq,
        top_k=args.top_k,
        first_n=args.first_n,
        distance_threshold=args.distance_threshold,
        min_moves=args.min_moves,
        max_moves=args.max_moves,
        verbose=True
    )
    
    # 保存到数据库
    print("\n🔄 保存到数据库...")
    builder.save_to_db(joseki_list, append=False)
    
    print()
    print("=" * 50)
    print(f"🎉 全部完成！共 {len(joseki_list)} 条定式")
    print("=" * 50)


def cmd_katago(args):
    """从KataGo棋谱构建定式库"""
    if args.mode == "auto":
        return _cmd_katago_auto(args)
    else:
        return _cmd_katago_custom(args)


def cmd_list(args):
    """列出定式"""
    storage = JsonStorage(args.db)
    joseki_list = storage.get_all()
    
    if not joseki_list:
        print("数据库为空")
        return
    
    # 排序
    reverse = (args.order == "desc")
    if args.sort == "freq":
        joseki_list.sort(key=lambda x: x.get("frequency", 0), reverse=reverse)
    elif args.sort == "probability":
        joseki_list.sort(key=lambda x: x.get("probability", 0), reverse=reverse)
    elif args.sort == "moves":
        joseki_list.sort(key=lambda x: x.get("moves", []), reverse=reverse)
    elif args.sort == "length":
        joseki_list.sort(key=lambda x: len(x.get("moves", [])), reverse=reverse)
    else:  # id
        joseki_list.sort(key=lambda x: x.get("id", ""), reverse=reverse)
    
    # 限制数量
    if args.limit:
        joseki_list = joseki_list[:args.limit]
    
    print(f"共 {len(storage.get_all())} 条定式")
    print()
    print(f"{'ID':<12} {'手数':>4} {'频率':>8} {'概率':>8} {'着法串'}")
    print("-" * 70)
    
    for j in joseki_list:
        jid = j.get("id", "-")
        moves = j.get("moves", [])
        freq = j.get("frequency", 0)
        prob = j.get("probability", 0.0)
        moves_str = " ".join(moves[:8])
        if len(moves) > 8:
            moves_str += "..."
        print(f"{jid:<12} {len(moves):>4} {freq:>8} {prob:>8.4%} {moves_str}")


def cmd_stats(args):
    """统计信息"""
    storage = JsonStorage(args.db)
    joseki_list = storage.get_all()
    
    if not joseki_list:
        print("数据库为空")
        return
    
    total = len(joseki_list)
    frequencies = [j.get("frequency", 0) for j in joseki_list]
    lengths = [len(j.get("moves", [])) for j in joseki_list]
    
    # 频率统计
    freq_sorted = sorted(frequencies, reverse=True)
    total_freq = sum(frequencies)
    
    # 中位数
    def median(lst):
        lst_sorted = sorted(lst)
        n = len(lst_sorted)
        if n == 0:
            return 0
        if n % 2 == 1:
            return lst_sorted[n // 2]
        return (lst_sorted[n // 2 - 1] + lst_sorted[n // 2]) // 2
    
    # 找出频率最高的定式
    max_freq_joseki = max(joseki_list, key=lambda x: x.get("frequency", 0))
    
    print("=" * 50)
    print("定式库统计")
    print("=" * 50)
    print(f"总定式数:     {total}")
    print(f"总出现次数:   {total_freq}")
    print()
    print("【频率统计】")
    print(f"  最高:       {max(frequencies)}")
    print(f"  最低:       {min(frequencies)}")
    print(f"  平均:       {total_freq / total:.1f}")
    print(f"  中位数:     {median(frequencies)}")
    print(f"  Top 10%平均: {sum(freq_sorted[:total//10]) / (total//10 or 1):.1f}")
    print()
    print("【着法长度统计】")
    print(f"  最长:       {max(lengths)} 手")
    print(f"  最短:       {min(lengths)} 手")
    print(f"  平均:       {sum(lengths) / total:.1f} 手")
    print(f"  中位数:     {median(lengths)} 手")
    print()
    print("【出现最多定式】")
    print(f"  ID:         {max_freq_joseki.get('id')}")
    print(f"  频率:       {max_freq_joseki.get('frequency', 0)}")
    print(f"  着法:       {' '.join(max_freq_joseki.get('moves', []))}")


def cmd_extract(args):
    """从SGF提取四角着法"""
    if not Path(args.input).exists():
        print(f"❌ 文件不存在: {args.input}")
        return 1
    
    sgf_data = Path(args.input).read_text(encoding='utf-8')
    
    result = extract_moves_all_corners(
        sgf_data,
        first_n=args.first_n,
        distance_threshold=args.distance_threshold
    )
    
    if not result:
        print("未提取到着法")
        return
    
    print(f"提取结果（前{args.first_n}手，距离阈值{args.distance_threshold}）:")
    print()
    
    corner_names = {'tl': '左上', 'tr': '右上', 'bl': '左下', 'br': '右下'}
    
    for corner in ['tl', 'tr', 'bl', 'br']:
        if corner not in result:
            continue
        
        moves = result[corner]
        coords = [c for _, c in moves]
        
        print(f"【{corner_names.get(corner, corner)}】{len(coords)}手")
        
        if args.verbose:
            for i, (color, coord) in enumerate(moves):
                coord_display = coord if coord != 'tt' else 'tt(脱先)'
                print(f"  {i+1:2d}. {color}[{coord_display}]")
        else:
            moves_str = " ".join(coords[:10])
            if len(coords) > 10:
                moves_str += f"... ({len(coords)}手)"
            print(f"  {moves_str}")
        print()
    
    # 可选保存MULTIGOGM
    if args.output:
        multigogm = convert_to_multigogm(result)
        Path(args.output).write_text(multigogm, encoding='utf-8')
        print(f"已保存MULTIGOGM: {args.output}")


def cmd_discover(args):
    """从SGF发现定式（支持批量目录和JSON输出）"""
    import json
    
    storage = JsonStorage(args.db)
    joseki_list = storage.get_all()
    
    if not joseki_list:
        print("❌ 数据库为空，请先使用katago命令构建定式库")
        return 1
    
    # 收集所有SGF文件
    sgf_files = []
    for path_str in args.paths:
        path = Path(path_str)
        if not path.exists():
            print(f"⚠️  路径不存在: {path_str}")
            continue
        
        if path.is_file() and path.suffix == '.sgf':
            sgf_files.append(path)
        elif path.is_dir():
            sgf_files.extend(path.glob("*.sgf"))
    
    if not sgf_files:
        print("❌ 未找到SGF文件")
        return 1
    
    # 批量处理 - 收集所有匹配结果
    all_matches = []
    for sgf_file in sgf_files:
        try:
            sgf_data = sgf_file.read_text(encoding='utf-8')
            
            # 解析SGF元数据
            from ..extraction.sgf_parser import parse_sgf
            sgf_result = parse_sgf(sgf_data)
            sgf_game_info = sgf_result.get("game_info", {})
            
            # 优先取EV，没有则取GN
            event = sgf_game_info.get("event", "")
            if not event:
                # 从原始properties获取GN
                tree = sgf_result.get("tree", {})
                props = tree.get("properties", {})
                event = props.get("GN", "")
            
            game_info = {
                "black": sgf_game_info.get("black", "未知"),
                "white": sgf_game_info.get("white", "未知"),
                "result": sgf_game_info.get("result", ""),
                "event": event,
                "date": sgf_game_info.get("date", "")
            }
            
            # 提取四角着法（用于输出）
            from ..extraction import extract_moves_all_corners, get_move_sequence
            from ..core.coords import convert_to_top_right
            from ..builder import convert_to_rudl
            corner_moves_dict = extract_moves_all_corners(
                sgf_data, first_n=args.first_n, distance_threshold=args.distance_threshold
            )
            # 准备着法串（用于输出）
            extracted_moves = {}
            for corner, moves in corner_moves_dict.items():
                coords = get_move_sequence(moves)
                
                # 检查该角9路范围内是否有棋子（转换前判断）
                from ..core.coords import has_stone_in_corner_9lu
                if not has_stone_in_corner_9lu(coords, corner):
                    continue  # 该角9路无棋子，不输出
                
                tr_coords = convert_to_top_right(coords, corner)
                extracted_moves[corner] = " ".join(tr_coords)
            
            results = discover_joseki(
                sgf_data,
                joseki_list,
                first_n=args.first_n,
                distance_threshold=args.distance_threshold
            )
            
            # 每条定式一条记录
            for corner, m in results.items():
                joseki = storage.get(m.joseki_id)
                all_matches.append({
                    "file": str(sgf_file),
                    "game_info": game_info,
                    "source_corner": m.source_corner,
                    "extracted_moves": m.moves,
                    "joseki_id": m.joseki_id,
                    "prefix": m.prefix,
                    "prefix_len": m.prefix_len,
                    "total_moves": m.total_moves,
                    "frequency": joseki.get("frequency", 0) if joseki else 0,
                    "probability": joseki.get("probability", 0.0) if joseki else 0.0
                })
        except Exception as e:
            print(f"⚠️  处理失败 {sgf_file}: {e}")
            continue
    
    if not all_matches:
        print("未发现定式")
        return
    
    # 按匹配长度从长到短排序
    all_matches.sort(key=lambda x: -x["prefix_len"])
    
    # JSON输出
    if args.json:
        output = json.dumps(all_matches, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            print(f"✅ 已保存到: {args.output}")
        else:
            print(output)
    else:
        # 文本输出
        corner_names = {'tl': '左上', 'tr': '右上', 'bl': '左下', 'br': '右下'}
        print(f"\n发现 {len(all_matches)} 个定式匹配（按匹配长度排序）：\n")
        for m in all_matches:
            print(f"📄 {m['file']}")
            print(f"  来源角: {corner_names.get(m['source_corner'], m['source_corner'])}")
            print(f"  定式ID: {m['joseki_id']}")
            print(f"  匹配: {m['prefix_len']}/{m['total_moves']}手")
            print(f"  前缀: {m['prefix']}")
            print(f"  频率: {m['frequency']}  概率: {m['probability']:.4%}")
            print()


def cmd_export(args):
    """导出定式"""
    storage = JsonStorage(args.db)
    joseki_list = storage.get_all()
    
    if not joseki_list:
        print("数据库为空")
        return
    
    # 前缀过滤
    if args.prefix:
        prefix = args.prefix.split()
        joseki_list = [j for j in joseki_list if j.get("moves", [])[:len(prefix)] == prefix]
    
    # limit 限制
    if args.limit:
        joseki_list = joseki_list[:args.limit]
    
    if args.format == "json":
        import json
        output = json.dumps(joseki_list, ensure_ascii=False, indent=2)
    elif args.format == "sgf":
        # 平面SGF格式
        lines = ["(;CA[utf-8]FF[4]AP[JosekiExport]SZ[19]GM[1]"]
        for j in joseki_list:
            moves = j.get("moves", [])
            if moves:
                lines.append(f"(;C[{j.get('id')} freq={j.get('frequency',0)}]")
                color = 'B'
                for m in moves:
                    lines.append(f";{color}[{m}]")
                    color = 'W' if color == 'B' else 'B'
                lines.append(")")
        lines.append(")")
        output = "".join(lines)
    elif args.format == "tree":
        # 树状SGF格式
        from ..matching import TrieMatcher
        matcher = TrieMatcher()
        matcher.build(joseki_list)
        prefix = args.prefix.split() if args.prefix else None
        output = matcher.export_tree(prefix=prefix, limit=args.limit or 100)
    else:
        print(f"❌ 不支持的格式: {args.format}")
        return 1
    
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"✅ 已导出到: {args.output}")
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(
        prog="weiqi-joseki",
        description="围棋定式数据库 - KataGo版"
    )
    parser.add_argument("--db", help="数据库路径", default=str(DEFAULT_DB_PATH))
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # init
    p_init = subparsers.add_parser("init", help="初始化空数据库")
    
    # katago
    p_katago = subparsers.add_parser("katago", help="从KataGo棋谱构建定式库")
    p_katago.add_argument("--mode", choices=["custom", "auto"], default="custom",
                         help="构建模式：custom=自定义构建(默认), auto=自动增量构建")
    p_katago.add_argument("--start-date", help="起始日期 (YYYY-MM-DD)，custom模式必需")
    p_katago.add_argument("--end-date", help="结束日期 (YYYY-MM-DD)，custom模式必需")
    p_katago.add_argument("--min-freq", type=int, default=10, help="最小频率")
    p_katago.add_argument("--top-k", type=int, default=100000, help="入库数量上限")
    p_katago.add_argument("--first-n", type=int, default=80, help="提取前N手")
    p_katago.add_argument("--distance-threshold", type=int, default=4, help="连通块距离阈值")
    p_katago.add_argument("--min-moves", type=int, default=4, help="最少手数")
    p_katago.add_argument("--max-moves", type=int, default=50, help="最多手数")
    p_katago.add_argument("--download-only", action="store_true", help="仅下载棋谱到缓存，不构建定式库")
    p_katago.add_argument("--delay", type=int, default=10, help="下载间隔延迟（秒），默认10秒")
    p_katago.add_argument("--force-rebuild", action="store_true", help="强制重建（仅auto模式有效）")
    p_katago.add_argument("--limit", type=int, help="限制处理的tar文件数量（仅auto模式测试用）")
    
    # list
    p_list = subparsers.add_parser("list", help="列出定式")
    p_list.add_argument("--limit", type=int, help="限制数量")
    p_list.add_argument("--sort", choices=["id", "freq", "probability", "moves", "length"], default="id", help="排序方式")
    p_list.add_argument("--order", choices=["asc", "desc"], default="asc", help="排序方向")
    
    # stats
    p_stats = subparsers.add_parser("stats", help="统计信息")
    
    # extract
    p_extract = subparsers.add_parser("extract", help="从SGF提取四角着法")
    p_extract.add_argument("input", help="SGF文件路径")
    p_extract.add_argument("--first-n", type=int, default=80, help="提取前N手")
    p_extract.add_argument("--distance-threshold", type=int, default=4, help="连通块距离阈值")
    p_extract.add_argument("--output", "-o", help="输出MULTIGOGM文件")
    p_extract.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    # discover
    p_discover = subparsers.add_parser("discover", help="从SGF发现定式")
    p_discover.add_argument("paths", nargs="+", help="SGF文件或目录路径")
    p_discover.add_argument("--first-n", type=int, default=80, help="提取前N手")
    p_discover.add_argument("--distance-threshold", type=int, default=4, help="连通块距离阈值")
    p_discover.add_argument("--json", action="store_true", help="JSON格式输出")
    p_discover.add_argument("--output", "-o", help="输出文件")
    p_discover.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    # export
    p_export = subparsers.add_parser("export", help="导出定式")
    p_export.add_argument("--format", choices=["json", "sgf", "tree"], default="tree", help="导出格式（默认: tree）")
    p_export.add_argument("--output", "-o", help="输出文件")
    p_export.add_argument("--limit", type=int, help="限制导出数量")
    p_export.add_argument("--prefix", help="指定前缀，只导出包含此前缀的定式")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    commands = {
        "init": cmd_init,
        "katago": cmd_katago,
        "list": cmd_list,
        "stats": cmd_stats,
        "extract": cmd_extract,
        "discover": cmd_discover,
        "export": cmd_export,
    }
    
    func = commands.get(args.command)
    if func:
        return func(args) or 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
