#!/usr/bin/env python3
# 运行方式：python3 scripts/umeng.py <command> [参数]
# -*- coding: utf-8 -*-
"""
友盟+ App 分析 CLI 工具

从环境变量读取认证信息：
  UMENG_API_KEY      - 友盟 Open API apiKey
  UMENG_API_SECURITY - 友盟 Open API apiSecurity

用法示例：
  python umeng.py get-all-app-data
  python umeng.py get-app-count
  python umeng.py get-app-list
  python umeng.py get-new-users --appkey 123456 --start-date 2024-01-01 --end-date 2024-01-31
  python umeng.py get-daily-data --appkey 123456 --date 2024-01-31
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 将 sdk 目录加入 Python 路径
SKILL_DIR = Path(__file__).resolve().parent.parent
SDK_DIR = SKILL_DIR / 'sdk'
sys.path.insert(0, str(SDK_DIR))

import aop
import aop.api.biz

# 初始化 SDK
UMENG_SERVER = 'gateway.open.umeng.com'
API_KEY = os.environ.get('UMENG_API_KEY')
API_SECURITY = os.environ.get('UMENG_API_SECURITY')

if not API_KEY or not API_SECURITY:
    print('错误：缺少环境变量 UMENG_API_KEY 或 UMENG_API_SECURITY', file=sys.stderr)
    sys.exit(1)

aop.set_default_server(UMENG_SERVER)
aop.set_default_appinfo(int(API_KEY), API_SECURITY)


def call_api(req):
    """执行 API 调用并输出结果"""
    try:
        resp = req.get_response()
        print(json.dumps(resp, ensure_ascii=False, indent=2))
    except aop.ApiError as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except aop.AopError as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


# ─── 全部应用 ────────────────────────────────────────────

def cmd_get_all_app_data(args):
    """获取所有 App 昨日和今日的基础统计数据"""
    from aop.api.biz.UmengUappGetAllAppDataRequest import UmengUappGetAllAppDataRequest
    call_api(UmengUappGetAllAppDataRequest())


def cmd_get_app_count(args):
    """获取当前用户所有 App 的数量"""
    from aop.api.biz.UmengUappGetAppCountRequest import UmengUappGetAppCountRequest
    call_api(UmengUappGetAppCountRequest())


def cmd_get_app_list(args):
    """获取当前用户的所有 App 列表"""
    from aop.api.biz.UmengUappGetAppListRequest import UmengUappGetAppListRequest
    req = UmengUappGetAppListRequest()
    if args.page:
        req.page = args.page
    if args.per_page:
        req.perPage = args.per_page
    if args.access_token:
        req.accessToken = args.access_token
    call_api(req)


# ─── 单个应用 ────────────────────────────────────────────

def cmd_get_new_accounts(args):
    """获取新增账号（仅游戏类型 App）"""
    from aop.api.biz.UmengUappGetNewAccountsRequest import UmengUappGetNewAccountsRequest
    req = UmengUappGetNewAccountsRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    if args.period_type:
        req.periodType = args.period_type
    if args.channel:
        req.channel = args.channel
    call_api(req)


def cmd_get_active_accounts(args):
    """获取活跃账号（仅游戏类型 App）"""
    from aop.api.biz.UmengUappGetActiveAccountsRequest import UmengUappGetActiveAccountsRequest
    req = UmengUappGetActiveAccountsRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    if args.period_type:
        req.periodType = args.period_type
    if args.channel:
        req.channel = args.channel
    call_api(req)


def cmd_create_event(args):
    """创建自定义事件"""
    from aop.api.biz.UmengUappEventCreateRequest import UmengUappEventCreateRequest
    req = UmengUappEventCreateRequest()
    req.appkey = args.appkey
    req.eventName = args.event_name
    req.eventDisplayName = args.event_display_name
    if args.event_type:
        req.eventType = args.event_type
    call_api(req)


def cmd_get_launches_by_channel_or_version(args):
    """根据渠道或版本条件获取 App 启动次数"""
    from aop.api.biz.UmengUappGetLaunchesByChannelOrVersionRequest import UmengUappGetLaunchesByChannelOrVersionRequest
    req = UmengUappGetLaunchesByChannelOrVersionRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.periodType = args.period_type
    if args.channels:
        req.channels = args.channels
    if args.versions:
        req.versions = args.versions
    call_api(req)


def cmd_get_active_users_by_channel_or_version(args):
    """根据渠道或版本条件获取 App 活跃用户数"""
    from aop.api.biz.UmengUappGetActiveUsersByChannelOrVersionRequest import UmengUappGetActiveUsersByChannelOrVersionRequest
    req = UmengUappGetActiveUsersByChannelOrVersionRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.periodType = args.period_type
    if args.channels:
        req.channels = args.channels
    if args.versions:
        req.versions = args.versions
    call_api(req)


def cmd_get_new_users_by_channel_or_version(args):
    """根据渠道或版本条件获取 App 新增用户数"""
    from aop.api.biz.UmengUappGetNewUsersByChannelOrVersionRequest import UmengUappGetNewUsersByChannelOrVersionRequest
    req = UmengUappGetNewUsersByChannelOrVersionRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.periodType = args.period_type
    if args.channels:
        req.channels = args.channels
    if args.versions:
        req.versions = args.versions
    call_api(req)


def cmd_get_event_param_value_duration_list(args):
    """获取事件参数值时长列表"""
    from aop.api.biz.UmengUappEventParamGetValueDurationListRequest import UmengUappEventParamGetValueDurationListRequest
    req = UmengUappEventParamGetValueDurationListRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.eventName = args.event_name
    req.eventParamName = args.event_param_name
    call_api(req)


def cmd_get_today_yesterday_data(args):
    """获取 App 今天与昨天的统计数据"""
    from aop.api.biz.UmengUappGetTodayYesterdayDataRequest import UmengUappGetTodayYesterdayDataRequest
    req = UmengUappGetTodayYesterdayDataRequest()
    req.appkey = args.appkey
    call_api(req)


def cmd_get_yesterday_data(args):
    """获取 App 昨天统计数据"""
    from aop.api.biz.UmengUappGetYesterdayDataRequest import UmengUappGetYesterdayDataRequest
    req = UmengUappGetYesterdayDataRequest()
    req.appkey = args.appkey
    call_api(req)


def cmd_get_today_data(args):
    """获取 App 今天统计数据"""
    from aop.api.biz.UmengUappGetTodayDataRequest import UmengUappGetTodayDataRequest
    req = UmengUappGetTodayDataRequest()
    req.appkey = args.appkey
    call_api(req)


def cmd_get_event_unique_users(args):
    """获取自定义事件的独立用户数"""
    from aop.api.biz.UmengUappEventGetUniqueUsersRequest import UmengUappEventGetUniqueUsersRequest
    req = UmengUappEventGetUniqueUsersRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.eventName = args.event_name
    call_api(req)


def cmd_get_channel_data(args):
    """获取渠道维度统计数据"""
    from aop.api.biz.UmengUappGetChannelDataRequest import UmengUappGetChannelDataRequest
    req = UmengUappGetChannelDataRequest()
    req.appkey = args.appkey
    req.date = args.date
    if args.page:
        req.page = args.page
    if args.per_page:
        req.perPage = args.per_page
    call_api(req)


def cmd_get_version_data(args):
    """获取版本维度统计数据"""
    from aop.api.biz.UmengUappGetVersionDataRequest import UmengUappGetVersionDataRequest
    req = UmengUappGetVersionDataRequest()
    req.appkey = args.appkey
    req.date = args.date
    call_api(req)


def cmd_get_event_param_data(args):
    """获取事件参数值统计数据"""
    from aop.api.biz.UmengUappEventParamGetDataRequest import UmengUappEventParamGetDataRequest
    req = UmengUappEventParamGetDataRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.eventName = args.event_name
    req.eventParamName = args.event_param_name
    req.paramValueName = args.param_value_name
    call_api(req)


def cmd_get_event_param_value_list(args):
    """获取事件参数值列表"""
    from aop.api.biz.UmengUappEventParamGetValueListRequest import UmengUappEventParamGetValueListRequest
    req = UmengUappEventParamGetValueListRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.eventName = args.event_name
    req.eventParamName = args.event_param_name
    call_api(req)


def cmd_get_event_data(args):
    """获取事件统计数据"""
    from aop.api.biz.UmengUappEventGetDataRequest import UmengUappEventGetDataRequest
    req = UmengUappEventGetDataRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.eventName = args.event_name
    call_api(req)


def cmd_get_event_param_list(args):
    """获取事件参数列表"""
    from aop.api.biz.UmengUappEventParamListRequest import UmengUappEventParamListRequest
    req = UmengUappEventParamListRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    req.eventId = args.event_id
    call_api(req)


def cmd_get_event_list(args):
    """获取事件列表"""
    from aop.api.biz.UmengUappEventListRequest import UmengUappEventListRequest
    req = UmengUappEventListRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    if args.page:
        req.page = args.page
    if args.per_page:
        req.perPage = args.per_page
    if args.version:
        req.version = args.version
    call_api(req)


def cmd_get_retentions(args):
    """获取 App 新增用户留存率"""
    from aop.api.biz.UmengUappGetRetentionsRequest import UmengUappGetRetentionsRequest
    req = UmengUappGetRetentionsRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    if args.period_type:
        req.periodType = args.period_type
    if args.channel:
        req.channel = args.channel
    if args.version:
        req.version = args.version
    if args.type:
        req.type = args.type
    call_api(req)


def cmd_get_durations(args):
    """获取 App 使用时长"""
    from aop.api.biz.UmengUappGetDurationsRequest import UmengUappGetDurationsRequest
    req = UmengUappGetDurationsRequest()
    req.appkey = args.appkey
    req.date = args.date
    if args.stat_type:
        req.statType = args.stat_type
    if args.channel:
        req.channel = args.channel
    if args.version:
        req.version = args.version
    call_api(req)


def cmd_get_launches(args):
    """获取 App 启动次数"""
    from aop.api.biz.UmengUappGetLaunchesRequest import UmengUappGetLaunchesRequest
    req = UmengUappGetLaunchesRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    if args.period_type:
        req.periodType = args.period_type
    call_api(req)


def cmd_get_active_users(args):
    """获取 App 活跃用户数"""
    from aop.api.biz.UmengUappGetActiveUsersRequest import UmengUappGetActiveUsersRequest
    req = UmengUappGetActiveUsersRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    if args.period_type:
        req.periodType = args.period_type
    call_api(req)


def cmd_get_new_users(args):
    """获取 App 新增用户数"""
    from aop.api.biz.UmengUappGetNewUsersRequest import UmengUappGetNewUsersRequest
    req = UmengUappGetNewUsersRequest()
    req.appkey = args.appkey
    req.startDate = args.start_date
    req.endDate = args.end_date
    if args.period_type:
        req.periodType = args.period_type
    call_api(req)


def cmd_get_daily_data(args):
    """获取 App 统计数据（指定日期）"""
    from aop.api.biz.UmengUappGetDailyDataRequest import UmengUappGetDailyDataRequest
    req = UmengUappGetDailyDataRequest()
    req.appkey = args.appkey
    req.date = args.date
    if args.version:
        req.version = args.version
    if args.channel:
        req.channel = args.channel
    call_api(req)


# ─── 参数解析 ────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        description='友盟+ App 分析 CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest='command', required=True)

    # 通用参数组
    def add_appkey(p):
        p.add_argument('--appkey', required=True, help='App 的 appkey')

    def add_date_range(p, required=True):
        p.add_argument('--start-date', required=required, help='开始日期 YYYY-MM-DD')
        p.add_argument('--end-date', required=required, help='结束日期 YYYY-MM-DD')

    def add_period_type(p):
        p.add_argument('--period-type', help='统计周期类型：daily/weekly/monthly')

    def add_channel(p):
        p.add_argument('--channel', help='渠道名称')

    def add_version(p):
        p.add_argument('--version', help='版本号')

    def add_page(p):
        p.add_argument('--page', type=int, help='页码')
        p.add_argument('--per-page', type=int, dest='per_page', help='每页条数')

    def add_event_name(p):
        p.add_argument('--event-name', required=True, help='事件标识名称')

    def add_event_param(p):
        p.add_argument('--event-param-name', required=True, help='事件参数名称')

    # ── 全部应用 ──
    sub.add_parser('get-all-app-data', help='获取所有 App 统计数据')
    sub.add_parser('get-app-count', help='获取 App 数量')
    p = sub.add_parser('get-app-list', help='获取 App 列表')
    add_page(p)
    p.add_argument('--access-token', dest='access_token', help='access_token')

    # ── 单个应用 ──
    p = sub.add_parser('get-new-accounts', help='获取新增账号（仅游戏）')
    add_appkey(p); add_date_range(p); add_period_type(p); add_channel(p)

    p = sub.add_parser('get-active-accounts', help='获取活跃账号（仅游戏）')
    add_appkey(p); add_date_range(p); add_period_type(p); add_channel(p)

    p = sub.add_parser('create-event', help='创建自定义事件')
    add_appkey(p)
    p.add_argument('--event-name', required=True, help='事件标识名')
    p.add_argument('--event-display-name', required=True, dest='event_display_name', help='事件展示名称')
    p.add_argument('--event-type', dest='event_type', help='事件类型')

    p = sub.add_parser('get-launches-by-channel-or-version', help='按渠道或版本获取启动次数')
    add_appkey(p); add_date_range(p)
    p.add_argument('--period-type', required=True, help='统计周期 daily/weekly/monthly')
    p.add_argument('--channels', help='渠道列表（逗号分隔）')
    p.add_argument('--versions', help='版本列表（逗号分隔）')

    p = sub.add_parser('get-active-users-by-channel-or-version', help='按渠道或版本获取活跃用户数')
    add_appkey(p); add_date_range(p)
    p.add_argument('--period-type', required=True, help='统计周期 daily/weekly/monthly')
    p.add_argument('--channels', help='渠道列表（逗号分隔）')
    p.add_argument('--versions', help='版本列表（逗号分隔）')

    p = sub.add_parser('get-new-users-by-channel-or-version', help='按渠道或版本获取新增用户数')
    add_appkey(p); add_date_range(p)
    p.add_argument('--period-type', required=True, help='统计周期 daily/weekly/monthly')
    p.add_argument('--channels', help='渠道列表（逗号分隔）')
    p.add_argument('--versions', help='版本列表（逗号分隔）')

    p = sub.add_parser('get-event-param-value-duration-list', help='获取事件参数值时长列表')
    add_appkey(p); add_date_range(p); add_event_name(p); add_event_param(p)

    p = sub.add_parser('get-today-yesterday-data', help='获取 App 今天与昨天统计数据')
    add_appkey(p)

    p = sub.add_parser('get-yesterday-data', help='获取 App 昨天统计数据')
    add_appkey(p)

    p = sub.add_parser('get-today-data', help='获取 App 今天统计数据')
    add_appkey(p)

    p = sub.add_parser('get-event-unique-users', help='获取自定义事件独立用户数')
    add_appkey(p); add_date_range(p); add_event_name(p)

    p = sub.add_parser('get-channel-data', help='获取渠道维度统计数据')
    add_appkey(p)
    p.add_argument('--date', required=True, help='日期 YYYY-MM-DD')
    add_page(p)

    p = sub.add_parser('get-version-data', help='获取版本维度统计数据')
    add_appkey(p)
    p.add_argument('--date', required=True, help='日期 YYYY-MM-DD')

    p = sub.add_parser('get-event-param-data', help='获取事件参数值统计数据')
    add_appkey(p); add_date_range(p); add_event_name(p); add_event_param(p)
    p.add_argument('--param-value-name', required=True, dest='param_value_name', help='参数值名称')

    p = sub.add_parser('get-event-param-value-list', help='获取事件参数值列表')
    add_appkey(p); add_date_range(p); add_event_name(p); add_event_param(p)

    p = sub.add_parser('get-event-data', help='获取事件统计数据')
    add_appkey(p); add_date_range(p); add_event_name(p)

    p = sub.add_parser('get-event-param-list', help='获取事件参数列表')
    add_appkey(p); add_date_range(p)
    p.add_argument('--event-id', required=True, dest='event_id', help='事件 ID')

    p = sub.add_parser('get-event-list', help='获取事件列表')
    add_appkey(p); add_date_range(p); add_page(p); add_version(p)

    p = sub.add_parser('get-retentions', help='获取 App 新增用户留存率')
    add_appkey(p); add_date_range(p); add_period_type(p); add_channel(p); add_version(p)
    p.add_argument('--type', help='留存类型')

    p = sub.add_parser('get-durations', help='获取 App 使用时长')
    add_appkey(p)
    p.add_argument('--date', required=True, help='日期 YYYY-MM-DD')
    p.add_argument('--stat-type', dest='stat_type', help='统计类型')
    add_channel(p); add_version(p)

    p = sub.add_parser('get-launches', help='获取 App 启动次数')
    add_appkey(p); add_date_range(p); add_period_type(p)

    p = sub.add_parser('get-active-users', help='获取 App 活跃用户数')
    add_appkey(p); add_date_range(p); add_period_type(p)

    p = sub.add_parser('get-new-users', help='获取 App 新增用户数')
    add_appkey(p); add_date_range(p); add_period_type(p)

    p = sub.add_parser('get-daily-data', help='获取 App 统计数据（指定日期）')
    add_appkey(p)
    p.add_argument('--date', required=True, help='日期 YYYY-MM-DD')
    add_version(p); add_channel(p)

    return parser


COMMAND_MAP = {
    'get-all-app-data': cmd_get_all_app_data,
    'get-app-count': cmd_get_app_count,
    'get-app-list': cmd_get_app_list,
    'get-new-accounts': cmd_get_new_accounts,
    'get-active-accounts': cmd_get_active_accounts,
    'create-event': cmd_create_event,
    'get-launches-by-channel-or-version': cmd_get_launches_by_channel_or_version,
    'get-active-users-by-channel-or-version': cmd_get_active_users_by_channel_or_version,
    'get-new-users-by-channel-or-version': cmd_get_new_users_by_channel_or_version,
    'get-event-param-value-duration-list': cmd_get_event_param_value_duration_list,
    'get-today-yesterday-data': cmd_get_today_yesterday_data,
    'get-yesterday-data': cmd_get_yesterday_data,
    'get-today-data': cmd_get_today_data,
    'get-event-unique-users': cmd_get_event_unique_users,
    'get-channel-data': cmd_get_channel_data,
    'get-version-data': cmd_get_version_data,
    'get-event-param-data': cmd_get_event_param_data,
    'get-event-param-value-list': cmd_get_event_param_value_list,
    'get-event-data': cmd_get_event_data,
    'get-event-param-list': cmd_get_event_param_list,
    'get-event-list': cmd_get_event_list,
    'get-retentions': cmd_get_retentions,
    'get-durations': cmd_get_durations,
    'get-launches': cmd_get_launches,
    'get-active-users': cmd_get_active_users,
    'get-new-users': cmd_get_new_users,
    'get-daily-data': cmd_get_daily_data,
}

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    COMMAND_MAP[args.command](args)
