#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场监测 CLI 工具 - Tushare 版本
支持概念板块与龙虎榜数据监测
"""

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None
import time
from datetime import datetime
import os
import sys
import argparse
from typing import Optional


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='市场实时监测工具 - 基于 Tushare 数据接口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 单次查询，显示 Top 10
  %(prog)s --once --token YOUR_TOKEN

  # 查询龙虎榜（Tushare doc_id=106）
  %(prog)s --once --data-source lhb --trade-date 20260213

  # 查询某只股票当日龙虎榜
  %(prog)s --once --data-source lhb --trade-date 20260213 --ts-code 002219.SZ

  # 持续监测，每 5 分钟刷新
  %(prog)s --token YOUR_TOKEN -i 300 -t 3

  # 短线模式
  %(prog)s --token YOUR_TOKEN --preset scalper

  # 设置环境变量避免每次输入 token
  export TUSHARE_TOKEN=YOUR_TOKEN
  %(prog)s --once
        """
    )

    # Tushare 配置
    parser.add_argument(
        '--token',
        type=str,
        help='Tushare API Token（也可通过环境变量 TUSHARE_TOKEN 设置）'
    )

    parser.add_argument(
        '--data-source',
        choices=['sector', 'lhb'],
        default='sector',
        help='数据源：sector（概念板块，默认）或 lhb（龙虎榜每日明细）'
    )

    parser.add_argument(
        '--trade-date',
        type=str,
        metavar='YYYYMMDD',
        help='交易日期（例如 20260213）。lhb 模式建议显式指定'
    )

    parser.add_argument(
        '--ts-code',
        type=str,
        help='股票 TS 代码（如 002219.SZ），仅 lhb 模式生效'
    )

    # 运行模式
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--once',
        action='store_true',
        help='单次运行模式（仅查询一次）'
    )
    mode_group.add_argument(
        '--watch', '-w',
        action='store_true',
        help='持续监测模式（默认）'
    )

    # 监测参数
    parser.add_argument(
        '--threshold', '-t',
        type=float,
        default=3.0,
        metavar='N',
        help='涨幅阈值（百分比），默认 3.0%%'
    )

    parser.add_argument(
        '--top', '-n',
        type=int,
        default=10,
        metavar='N',
        help='显示排行榜前 N 名，默认 10'
    )

    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=300,
        metavar='SEC',
        help='轮询间隔（秒），默认 300（5分钟）'
    )

    # 显示选项
    parser.add_argument(
        '--no-score',
        action='store_true',
        help='不显示综合评分榜'
    )

    parser.add_argument(
        '--no-rank',
        action='store_true',
        help='不显示涨幅排行榜'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='静默模式，仅显示超过阈值的板块'
    )

    parser.add_argument(
        '--no-clear',
        action='store_true',
        help='不清屏，保留历史输出'
    )

    # 输出格式
    parser.add_argument(
        '--format', '-f',
        choices=['table', 'simple', 'json'],
        default='table',
        help='输出格式：table（表格）、simple（简洁）、json（JSON）'
    )

    parser.add_argument(
        '--export',
        metavar='FILE',
        help='导出数据到 CSV 文件'
    )

    # 预设模式
    parser.add_argument(
        '--preset',
        choices=['scalper', 'swing', 'casual'],
        help='预设模式：scalper（短线）、swing（中线）、casual（长线）'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0 (Tushare)'
    )

    return parser.parse_args()


def apply_preset(args):
    """应用预设配置"""
    presets = {
        'scalper': {'interval': 60, 'threshold': 2.0, 'top': 15},
        'swing': {'interval': 300, 'threshold': 3.0, 'top': 10},
        'casual': {'interval': 900, 'threshold': 5.0, 'top': 8}
    }

    if args.preset and args.preset in presets:
        preset = presets[args.preset]
        if not args.quiet:
            print(f"📦 应用预设: {args.preset}")
            print(f"   间隔={preset['interval']}秒, 阈值={preset['threshold']}%, Top={preset['top']}\n")
        args.interval = preset['interval']
        args.threshold = preset['threshold']
        args.top = preset['top']

    return args


class SectorMonitor:
    """概念板块监测器"""

    def __init__(self, token, threshold=3.0, top_n=10, interval=300,
                 show_score=True, show_rank=True, quiet=False,
                 clear_screen=True, output_format='table',
                 data_source='sector', trade_date=None, ts_code=None):
        """初始化监测器"""
        if pd is None:
            print("❌ 未安装 pandas 依赖")
            print("💡 请先安装: pip install pandas")
            sys.exit(1)

        self.threshold = threshold
        self.top_n = top_n
        self.interval = interval
        self.show_score = show_score
        self.show_rank = show_rank
        self.quiet = quiet
        self.clear_screen = clear_screen
        self.output_format = output_format
        self.data_source = data_source
        self.trade_date = trade_date
        self.ts_code = ts_code
        self.last_alert_time = {}
        self.alert_cooldown = 600

        # 初始化 Tushare
        try:
            import tushare as ts
            ts.set_token(token)
            self.pro = ts.pro_api()
            if not self.quiet:
                print("✅ Tushare API 初始化成功")
        except ModuleNotFoundError:
            print("❌ 未安装 tushare 依赖")
            print("💡 请先安装: pip install tushare")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Tushare API 初始化失败: {e}")
            print("💡 请检查 Token 是否正确")
            sys.exit(1)

    def fetch_sector_data(self):
        """
        获取概念板块数据

        Tushare 提供的接口：
        - concept: 概念板块列表
        - concept_detail: 概念成分股
        - ths_daily: 同花顺概念和行业指数行情
        """
        try:
            # 获取当前交易日期
            trade_date = datetime.now().strftime('%Y%m%d')

            # 方法1: 使用 ths_daily 获取同花顺概念指数行情
            # 注意：这个接口需要一定的积分权限
            df = self.pro.ths_daily(
                trade_date=trade_date,
                fields='ts_code,name,close,pct_chg,amount,total_mv'
            )

            if df is not None and not df.empty:
                # 只保留概念板块（以 885 开头）
                df = df[df['ts_code'].str.startswith('885')]

                # 重命名列以匹配原有逻辑
                df = df.rename(columns={
                    'name': '板块名称',
                    'close': '最新价',
                    'pct_chg': '涨跌幅',
                    'amount': '成交额',
                    'total_mv': '总市值'
                })

                # 成交额单位转换（万元 -> 元）
                df['成交额'] = df['成交额'] * 10000

                # 获取每个板块的成分股信息（用于计算上涨比例等）
                df = self.enrich_sector_data(df)

                # 计算综合评分
                df = self.calculate_composite_score(df)

                return df
            else:
                if not self.quiet:
                    print("⚠️  未能获取到板块数据（可能是非交易日或权限不足）")
                return None

        except Exception as e:
            print(f"❌ 获取数据失败: {e}")
            print("💡 提示：")
            print("   1. 检查是否在交易时间")
            print("   2. ths_daily 接口需要一定积分权限")
            print("   3. 可尝试使用 concept 接口获取概念板块列表")
            return None

    def fetch_lhb_data(self):
        """
        获取龙虎榜每日明细（doc_id=106）
        接口：top_list
        """
        try:
            trade_date = self.trade_date or datetime.now().strftime('%Y%m%d')
            params = {
                'trade_date': trade_date,
                'fields': (
                    'trade_date,ts_code,name,close,pct_change,turnover_rate,amount,'
                    'l_sell,l_buy,l_amount,net_amount,net_rate,amount_rate,float_values,reason'
                )
            }
            if self.ts_code:
                params['ts_code'] = self.ts_code

            df = self.pro.top_list(**params)

            if df is None or df.empty:
                if not self.quiet:
                    print(f"⚠️  {trade_date} 未查询到龙虎榜数据（可能是非交易日或无上榜数据）")
                return None

            df = df.rename(columns={
                'trade_date': '交易日期',
                'ts_code': '代码',
                'name': '股票名称',
                'close': '收盘价',
                'pct_change': '涨跌幅',
                'turnover_rate': '换手率',
                'amount': '总成交额',
                'l_sell': '龙虎榜卖出额',
                'l_buy': '龙虎榜买入额',
                'l_amount': '龙虎榜成交额',
                'net_amount': '龙虎榜净买入额',
                'net_rate': '净买额占比',
                'amount_rate': '龙虎榜成交额占比',
                'float_values': '当日流通市值',
                'reason': '上榜理由'
            })

            # 过滤 ST 类股票（ST / *ST / S*ST / SST）
            name_series = df['股票名称'].fillna('').astype(str).str.upper()
            st_mask = name_series.str.startswith(('ST', '*ST', 'S*ST', 'SST'))
            df = df[~st_mask].copy()

            if df.empty:
                if not self.quiet:
                    print(f"⚠️  {trade_date} 龙虎榜数据仅包含 ST 类股票，过滤后为空")
                return None

            df = self.calculate_lhb_score(df)
            return df
        except Exception as e:
            print(f"❌ 获取龙虎榜数据失败: {e}")
            print("💡 提示：")
            print("   1. top_list 接口需至少 2000 积分权限")
            print("   2. 请确认 trade_date 为交易日（格式 YYYYMMDD）")
            print("   3. 接口文档: https://tushare.pro/document/2?doc_id=106")
            return None

    def fetch_data(self):
        """按数据源分派数据获取"""
        if self.data_source == 'lhb':
            return self.fetch_lhb_data()
        return self.fetch_sector_data()

    def enrich_sector_data(self, df):
        """
        丰富板块数据（获取成分股信息）
        由于 Tushare 获取成分股需要多次请求，这里简化处理
        """
        # 添加默认值（实际使用时可以通过 concept_detail 接口获取详细信息）
        df['上涨家数'] = 0
        df['下跌家数'] = 0
        df['领涨股票'] = '-'
        df['领涨股票涨跌幅'] = 0.0
        df['换手率'] = 0.0
        df['上涨比例'] = 50.0  # 默认50%

        # 注：如果需要详细的成分股信息，可以遍历每个板块调用 concept_detail
        # 但这会大大增加 API 调用次数，需要权衡

        return df

    def calculate_lhb_score(self, df):
        """计算龙虎榜综合评分"""
        df['涨幅得分'] = self.normalize_score(df['涨跌幅'])
        df['净买入得分'] = self.normalize_score(df['龙虎榜净买入额'])
        df['净买占比得分'] = self.normalize_score(df['净买额占比'])
        df['综合评分'] = (
            df['涨幅得分'] * 0.4 +
            df['净买入得分'] * 0.4 +
            df['净买占比得分'] * 0.2
        )
        return df

    def calculate_composite_score(self, df):
        """计算综合评分"""
        df['涨幅得分'] = self.normalize_score(df['涨跌幅'])
        df['成交额得分'] = self.normalize_score(df['成交额'])
        df['市值得分'] = self.normalize_score(df['总市值'])

        # 综合评分（因为缺少上涨比例等数据，调整权重）
        df['综合评分'] = (
                df['涨幅得分'] * 0.5 +
                df['成交额得分'] * 0.3 +
                df['市值得分'] * 0.2
        )

        return df

    @staticmethod
    def normalize_score(series):
        """将数据标准化到 0-100 分"""
        if series.max() == series.min():
            return pd.Series([50] * len(series), index=series.index)
        return ((series - series.min()) / (series.max() - series.min())) * 100

    def analyze_top_items(self, df):
        """分析排名前列数据"""
        top_by_change = df.nlargest(self.top_n, '涨跌幅')
        top_by_score = df.nlargest(self.top_n, '综合评分') if '综合评分' in df.columns else pd.DataFrame()
        return top_by_change, top_by_score

    def check_threshold_alerts(self, df):
        """检查是否有板块触发阈值提醒"""
        current_time = time.time()
        alerts = []

        alert_df = df[df['涨跌幅'] >= self.threshold].copy()

        name_col = '板块名称' if self.data_source == 'sector' else '股票名称'
        for _, row in alert_df.iterrows():
            item_name = row[name_col]

            if item_name in self.last_alert_time:
                if current_time - self.last_alert_time[item_name] < self.alert_cooldown:
                    continue

            self.last_alert_time[item_name] = current_time
            alerts.append(row)

        return alerts

    def format_sector_simple(self, row, index=None):
        """简洁格式输出"""
        rank = f"[{index}] " if index is not None else ""
        return f"{rank}{row['板块名称']}: {row['涨跌幅']:.2f}% | 成交: {row['成交额'] / 1e8:.1f}亿 | 评分: {row['综合评分']:.1f}"

    def format_sector_table(self, row, index=None):
        """表格格式输出"""
        rank = f"[{index}] " if index is not None else ""
        info = f"""
{rank}📊 {row['板块名称']}
  ├─ 涨跌幅: {row['涨跌幅']:.2f}%
  ├─ 最新价: {row['最新价']:.2f}
  ├─ 成交额: {row['成交额'] / 1e8:.2f} 亿元
  ├─ 总市值: {row['总市值'] / 1e8:.2f} 亿元
  └─ 综合评分: {row['综合评分']:.1f}/100
"""
        return info

    def format_lhb_simple(self, row, index=None):
        """龙虎榜简洁格式输出"""
        rank = f"[{index}] " if index is not None else ""
        return (
            f"{rank}{row['股票名称']}({row['代码']}): {row['涨跌幅']:.2f}% | "
            f"净买入: {row['龙虎榜净买入额'] / 1e8:.2f}亿 | 评分: {row['综合评分']:.1f}"
        )

    def format_lhb_table(self, row, index=None):
        """龙虎榜表格格式输出"""
        rank = f"[{index}] " if index is not None else ""
        info = f"""
{rank}📌 {row['股票名称']} ({row['代码']})
  ├─ 涨跌幅: {row['涨跌幅']:.2f}%
  ├─ 收盘价: {row['收盘价']:.2f}
  ├─ 龙虎榜净买入: {row['龙虎榜净买入额'] / 1e8:.2f} 亿元
  ├─ 龙虎榜成交额: {row['龙虎榜成交额'] / 1e8:.2f} 亿元
  ├─ 净买额占比: {row['净买额占比']:.2f}%
  ├─ 上榜理由: {row['上榜理由']}
  └─ 综合评分: {row['综合评分']:.1f}/100
"""
        return info

    def format_sector_info(self, row, index=None):
        """根据输出格式选择"""
        if self.data_source == 'lhb':
            return self.format_lhb_simple(row, index) if self.output_format == 'simple' else self.format_lhb_table(row, index)
        return self.format_sector_simple(row, index) if self.output_format == 'simple' else self.format_sector_table(row, index)

    def export_to_csv(self, df, filename):
        """导出数据到 CSV"""
        try:
            df_export = df.copy()
            df_export['更新时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if self.data_source == 'lhb':
                columns = ['更新时间', '交易日期', '代码', '股票名称', '涨跌幅', '收盘价',
                           '龙虎榜净买入额', '龙虎榜成交额', '净买额占比', '上榜理由', '综合评分']
            else:
                columns = ['更新时间', '板块名称', '涨跌幅', '最新价', '成交额', '总市值', '综合评分']
            df_export = df_export[columns]

            header = not os.path.exists(filename)
            df_export.to_csv(filename, mode='a', index=False, header=header, encoding='utf-8-sig')

            if not self.quiet:
                print(f"✅ 数据已导出到: {filename}")
        except Exception as e:
            print(f"❌ 导出失败: {e}")

    def print_report(self, df, export_file: Optional[str] = None):
        """打印监测报告"""
        if self.clear_screen and not self.quiet:
            os.system('clear' if os.name == 'posix' else 'cls')

        # JSON 格式输出
        if self.output_format == 'json':
            import json
            top_by_change, top_by_score = self.analyze_top_items(df)
            alerts = self.check_threshold_alerts(df)

            output = {
                'update_time': datetime.now().isoformat(),
                'data_source': self.data_source,
                'threshold': self.threshold,
                'alerts': [item.to_dict() for item in alerts] if len(alerts) > 0 else [],
                'top_by_change': top_by_change.head(self.top_n).to_dict('records'),
                'top_by_score': top_by_score.head(self.top_n).to_dict('records') if self.show_score else []
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
            return

        # 普通格式输出
        if not self.quiet:
            print("=" * 80)
            title = "📈 概念板块实时监测 (Tushare)" if self.data_source == 'sector' else "📌 龙虎榜每日明细监测 (Tushare)"
            print(title)
            print(f"⏰ 更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🔔 阈值: {self.threshold}%  |  🔄 间隔: {self.interval}秒  |  Top: {self.top_n}")
            print("=" * 80)

        # 阈值提醒
        alerts = self.check_threshold_alerts(df)
        if alerts:
            print(f"\n🚨 【涨幅预警】{len(alerts)} 个板块涨幅超过 {self.threshold}%:")
            print("-" * 80)
            for alert in alerts:
                print(self.format_sector_info(alert))

        if not self.quiet:
            # 涨幅榜
            if self.show_rank:
                top_by_change, _ = self.analyze_top_items(df)
                print(f"\n🏆 【涨幅榜 Top {self.top_n}】")
                print("-" * 80)
                for idx, (_, row) in enumerate(top_by_change.iterrows(), 1):
                    print(self.format_sector_info(row, idx))

            # 综合评分榜
            if self.show_score:
                _, top_by_score = self.analyze_top_items(df)
                print(f"\n⭐ 【综合评分 Top {self.top_n}】")
                print("-" * 80)
                for idx, (_, row) in enumerate(top_by_score.iterrows(), 1):
                    print(self.format_sector_info(row, idx))

            # 统计信息
            rising_count = len(df[df['涨跌幅'] > 0])
            falling_count = len(df[df['涨跌幅'] < 0])
            total_count = len(df)

            print("\n" + "=" * 80)
            print(f"📊 市场: 上涨 {rising_count} | 下跌 {falling_count} | 总计 {total_count}")
            if not self.quiet:
                print(f"💡 下次更新: {self.interval}秒后 (按 Ctrl+C 停止)")
            print("=" * 80)

        # 导出数据
        if export_file:
            self.export_to_csv(df, export_file)

    def run_once(self, export_file: Optional[str] = None):
        """运行一次监测"""
        if not self.quiet:
            if self.data_source == 'lhb':
                date_tip = self.trade_date or datetime.now().strftime('%Y%m%d')
                print(f"🔍 正在获取龙虎榜数据（交易日 {date_tip}）...")
            else:
                print("🔍 正在获取板块数据...")

        df = self.fetch_data()

        if df is not None:
            self.print_report(df, export_file)
            return True
        return False

    def run_continuous(self, export_file: Optional[str] = None):
        """持续监测模式"""
        print(f"🚀 启动持续监测模式")
        print(f"⚙️  配置: 阈值={self.threshold}%, 间隔={self.interval}秒, Top={self.top_n}")
        print(f"💡 按 Ctrl+C 停止\n")

        try:
            while True:
                success = self.run_once(export_file)

                if success:
                    time.sleep(self.interval)
                else:
                    print(f"⏳ 30秒后重试...")
                    time.sleep(30)

        except KeyboardInterrupt:
            print("\n\n👋 监测已停止")
            sys.exit(0)


def main():
    """主函数"""
    args = parse_arguments()

    # 获取 Token
    token = args.token or os.environ.get('TUSHARE_TOKEN')

    if not token:
        print("❌ 错误: 未提供 Tushare Token")
        print("\n使用方法:")
        print("  1. 命令行参数: --token YOUR_TOKEN")
        print("  2. 环境变量: export TUSHARE_TOKEN=YOUR_TOKEN")
        print("\n💡 获取 Token: https://tushare.pro/register")
        sys.exit(1)

    # 应用预设
    args = apply_preset(args)

    # 创建监测器
    monitor = SectorMonitor(
        token=token,
        threshold=args.threshold,
        top_n=args.top,
        interval=args.interval,
        show_score=not args.no_score,
        show_rank=not args.no_rank,
        quiet=args.quiet,
        clear_screen=not args.no_clear,
        output_format=args.format,
        data_source=args.data_source,
        trade_date=args.trade_date,
        ts_code=args.ts_code
    )

    # 运行模式
    if args.once:
        monitor.run_once(export_file=args.export)
    else:
        monitor.run_continuous(export_file=args.export)


if __name__ == "__main__":
    main()
