import json
from utils import make_request

def setup_parser(subparsers):
    parser = subparsers.add_parser("locations", help="管理和查询位置")
    sub_subparsers = parser.add_subparsers(dest="subcommand", help="可用操作")
    sub_subparsers.required = True

    list_parser = sub_subparsers.add_parser("list", help="查询位置分布，不含时间信息（地点名，照片数量）")
    list_parser.add_argument("--level", choices=["city", "province", "district", "scene"], default="city", help="分组级别，默认 city, 可选值：city,province,district,scene（5A景区） 中的一个")
    list_parser.add_argument("--skip", type=int, default=0, help="跳过 N 个位置")
    list_parser.add_argument("--limit", type=int, default=100, help="限制返回 N 个位置")
    # start_date, end_date 过滤时间范围
    list_parser.add_argument("--start-date", help="可选，开始日期，格式 YYYY-MM-DD")
    list_parser.add_argument("--end-date", help="可选，结束日期，格式 YYYY-MM-DD")
    list_parser.set_defaults(func=execute_list)

    timeline_parser = sub_subparsers.add_parser("timeline", help="查询足迹时间轴列表，按时间和地点分组（开始日期，结束日期，地点名，照片数量）")
    timeline_parser.add_argument("--level", choices=["city", "province", "district", "scene"], default="city", help="分组级别，默认 city, 可选值：city,province,district,scene（5A景区） 中的一个")
    timeline_parser.add_argument("--skip", type=int, default=0, help="跳过 N 个位置")
    timeline_parser.add_argument("--limit", type=int, default=100, help="限制返回 N 个位置")
    # start_date, end_date 过滤时间范围
    timeline_parser.add_argument("--start-date", help="可选，开始日期，格式 YYYY-MM-DD")
    timeline_parser.add_argument("--end-date", help="可选，结束日期，格式 YYYY-MM-DD")
    timeline_parser.set_defaults(func=execute_timeline)

def execute_timeline(args):
    data = make_request("/locations/timeline", {"start_date": args.start_date, "end_date": args.end_date, "skip": args.skip, "limit": args.limit, "level": args.level})
    if data:
        timelines = [{
            "startDate": timeline["startDate"],
            "endDate": timeline["endDate"],
            "locationName": timeline["locationName"],
            "count": timeline["photoCount"]
        } for timeline in data["nodes"]]
        print(json.dumps(timelines, indent=2, ensure_ascii=False))
    else:
        print("未查询到位置足迹时间轴数据")

def execute_list(args):
    data = make_request("/locations", {"level": args.level, "skip": args.skip, "limit": args.limit, "start_date": args.start_date, "end_date": args.end_date})
    if data:
        # 映射字段并添加 count 字段
        locations = [{
            "name": location["name"],
            "count": location["count"]
        } for location in data]
        print(json.dumps(locations, indent=2, ensure_ascii=False))
    else:
        print("未查询到位置记录")
