# 导入必要的模块
from datetime import datetime, timedelta, time
from typing import Optional, Callable

# 导入pandas的DataFrame
from pandas import DataFrame
# 导入迅投相关的数据接口模块
from xtquant import (
    xtdata,
    # xtdatacenter as xtdc
)
# # 导入文件锁模块
# from filelock import FileLock, Timeout

# 从vnpy框架中导入相关配置和基础类
from vnpy.trader.setting import SETTINGS
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData, TickData, HistoryRequest
from vnpy.trader.utility import ZoneInfo, get_file_path
from vnpy.trader.datafeed import BaseDatafeed

# 定义vnpy间隔到迅投间隔的映射字典
INTERVAL_VT2XT: dict[Interval, str] = {
    Interval.MINUTE: "1m",    # 分钟线映射为"1m"
    Interval.DAILY: "1d",     # 日线映射为"1d"
    Interval.TICK: "tick"     # Tick数据映射为"tick"
}

# 定义间隔调整映射，用于时间戳处理
INTERVAL_ADJUSTMENT_MAP: dict[Interval, timedelta] = {
    Interval.MINUTE: timedelta(minutes=1),  # 分钟线调整1分钟
    Interval.DAILY: timedelta()             # 日线无需调整
}

# 定义vnpy交易所到迅投交易所的映射字典
EXCHANGE_VT2XT: dict[Exchange, str] = {
    Exchange.SSE: "SH",        # 上交所
    Exchange.SZSE: "SZ",       # 深交所
    Exchange.BSE: "BJ",        # 北交所
    Exchange.SHFE: "SF",       # 上期所
    Exchange.CFFEX: "IF",      # 中金所
    Exchange.INE: "INE",       # 能源中心
    Exchange.DCE: "DF",        # 大商所
    Exchange.CZCE: "ZF",       # 郑商所
    Exchange.GFEX: "GF",       # 广期所
}

# 设置中国时区
CHINA_TZ = ZoneInfo("Asia/Shanghai")


class XtDatafeed(BaseDatafeed):
    """迅投研数据服务接口"""

    # # 定义锁文件相关属性
    # lock_filename = "xt_lock"
    # lock_filepath = get_file_path(lock_filename)

    def __init__(self):
        """初始化方法"""
        # 从全局配置中获取用户名和密码
        self.username: str = SETTINGS["datafeed.username"]
        self.password: str = SETTINGS["datafeed.password"]
        self.inited: bool = False  # 初始化标志

        # self.lock: FileLock = None  # 文件锁对象

        xtdata.enable_hello = False  # 禁用迅投的hello信息

    def init(self, output: Callable = print) -> bool:
        """初始化"""
        if self.inited:  # 如果已经初始化，直接返回True
            return True

        try:
            # 使用Token连接，无需启动客户端
            if self.username != "client":  # 如果不是默认的client用户名
                self.init_xtdc()  # 初始化迅投数据中心

            # 尝试查询合约信息，确认连接成功
            xtdata.get_instrument_detail("000001.SZ")
        except Exception as ex:
            # 输出错误信息并返回False
            output(f"迅投研数据服务初始化失败，发生异常：{ex}")
            return False

        self.inited = True  # 标记为已初始化
        return True

    # def get_lock(self) -> bool:
    #     """获取文件锁，确保单例运行"""
    #     self.lock = FileLock(self.lock_filepath)  # 创建文件锁对象
    #
    #     try:
    #         self.lock.acquire(timeout=1)  # 尝试获取锁，超时1秒
    #         return True
    #     except Timeout:
    #         return False  # 获取锁超时返回False
    #
    # def init_xtdc(self) -> None:
    #     """初始化xtdc服务进程"""
    #     if not self.get_lock():  # 尝试获取锁
    #         return
    #
    #     # 设置token
    #     xtdc.set_token(self.password)
    #
    #     # 设置连接池
    #     xtdc.set_allow_optmize_address(["115.231.218.73:55310", "115.231.218.79:55310"])
    #
    #     # 开启使用期货真实夜盘时间
    #     xtdc.set_future_realtime_mode(True)
    #
    #     # 执行初始化，但不启动默认58609端口监听
    #     xtdc.init(False)
    #
    #     # 设置监听端口58620
    #     xtdc.listen(port=58620)

    def query_bar_history(self, req: HistoryRequest, output: Callable = print) -> Optional[list[BarData]]:
        """查询K线历史数据"""
        history: list[BarData] = []  # 初始化结果列表

        if not self.inited:  # 如果未初始化
            n: bool = self.init(output)  # 尝试初始化
            if not n:
                return history  # 初始化失败返回空列表

        # 获取历史数据DataFrame
        df: DataFrame = get_history_df(req, output)
        if df.empty:  # 如果数据为空
            return history

        # 获取时间调整量
        adjustment: timedelta = INTERVAL_ADJUSTMENT_MAP[req.interval]

        # 遍历解析
        auction_bar: BarData = None

        # 遍历DataFrame的每一行
        for tp in df.itertuples():
            # 将迅投研时间戳（K线结束时点）转换为VeighNa时间戳（K线开始时点）
            dt: datetime = datetime.fromtimestamp(tp.time / 1000)
            dt = dt.replace(tzinfo=CHINA_TZ)  # 设置时区
            dt = dt - adjustment  # 根据间隔类型调整时间

            # 日线，过滤尚未走完的当日数据
            if req.interval == Interval.DAILY:
                incomplete_bar: bool = (
                    dt.date() == datetime.now().date()  # 如果是今天
                    and datetime.now().time() < time(hour=15)  # 且当前时间在15点前
                )
                if incomplete_bar:
                    continue  # 跳过未完成的日线
            # 分钟线，过滤盘前集合竞价数据（合并到开盘后第1根K线中）
            else:
                # 检查是否是集合竞价时间
                if (
                    req.exchange in (Exchange.SSE, Exchange.SZSE, Exchange.BSE, Exchange.CFFEX)
                    and dt.time() == time(hour=9, minute=29)
                ) or (
                    req.exchange in (Exchange.SHFE, Exchange.INE, Exchange.DCE, Exchange.CZCE, Exchange.GFEX)
                    and dt.time() in (time(hour=8, minute=59), time(hour=20, minute=59))
                ):
                    # 创建集合竞价Bar
                    auction_bar = BarData(
                        symbol=req.symbol,
                        exchange=req.exchange,
                        datetime=dt,
                        open_price=float(tp.open),
                        volume=float(tp.volume),
                        turnover=float(tp.amount),
                        gateway_name="XT"
                    )
                    continue  # 跳过集合竞价时间点

            # 生成K线对象
            bar: BarData = BarData(
                symbol=req.symbol,
                exchange=req.exchange,
                datetime=dt,
                interval=req.interval,
                volume=float(tp.volume),
                turnover=float(tp.amount),
                open_interest=float(tp.openInterest),
                open_price=float(tp.open),
                high_price=float(tp.high),
                low_price=float(tp.low),
                close_price=float(tp.close),
                gateway_name="XT"
            )

            # 合并集合竞价数据
            if auction_bar and auction_bar.volume:
                bar.open_price = auction_bar.open_price
                bar.volume += auction_bar.volume
                bar.turnover += auction_bar.turnover
                auction_bar = None  # 清空集合竞价Bar

            history.append(bar)  # 添加到结果列表

        return history

    def query_tick_history(self, req: HistoryRequest, output: Callable = print) -> Optional[list[TickData]]:
        """查询Tick数据"""
        history: list[TickData] = []

        if not self.inited:  # 如果未初始化
            n: bool = self.init(output)  # 尝试初始化
            if not n:
                return history  # 初始化失败返回空列表

        # 获取历史数据DataFrame
        df: DataFrame = get_history_df(req, output)
        if df.empty:  # 如果数据为空
            return history

        # 遍历DataFrame的每一行
        for tp in df.itertuples():
            # 将迅投的时间戳(毫秒)转换为datetime对象
            dt: datetime = datetime.fromtimestamp(tp.time / 1000)
            dt = dt.replace(tzinfo=CHINA_TZ)  # 设置时区

            # 创建Tick数据对象
            tick: TickData = TickData(
                symbol=req.symbol,
                exchange=req.exchange,
                datetime=dt,
                volume=float(tp.volume),
                turnover=float(tp.amount),
                open_interest=float(tp.openInt),
                open_price=float(tp.open),
                high_price=float(tp.high),
                low_price=float(tp.low),
                last_price=float(tp.lastPrice),
                pre_close=float(tp.lastClose),
                bid_price_1=float(tp.bidPrice[0]),
                ask_price_1=float(tp.askPrice[0]),
                bid_volume_1=float(tp.bidVol[0]),
                ask_volume_1=float(tp.askVol[0]),
                gateway_name="XT",
            )

            # 处理五档行情数据
            bid_price_2: float = float(tp.bidPrice[1])
            if bid_price_2:  # 如果有第二档买价
                tick.bid_price_2 = bid_price_2
                tick.bid_price_3 = float(tp.bidPrice[2])
                tick.bid_price_4 = float(tp.bidPrice[3])
                tick.bid_price_5 = float(tp.bidPrice[4])

                tick.ask_price_2 = float(tp.askPrice[1])
                tick.ask_price_3 = float(tp.askPrice[2])
                tick.ask_price_4 = float(tp.askPrice[3])
                tick.ask_price_5 = float(tp.askPrice[4])

                tick.bid_volume_2 = float(tp.bidVol[1])
                tick.bid_volume_3 = float(tp.bidVol[2])
                tick.bid_volume_4 = float(tp.bidVol[3])
                tick.bid_volume_5 = float(tp.bidVol[4])

                tick.ask_volume_2 = float(tp.askVol[1])
                tick.ask_volume_3 = float(tp.askVol[2])
                tick.ask_volume_4 = float(tp.askVol[3])
                tick.ask_volume_5 = float(tp.askVol[4])

            history.append(tick)  # 添加到结果列表

        return history


def get_history_df(req: HistoryRequest, output: Callable = print) -> DataFrame:
    """获取历史数据DataFrame"""
    symbol: str = req.symbol  # 获取合约符号
    exchange: Exchange = req.exchange  # 获取交易所
    start: datetime = req.start  # 获取开始时间
    end: datetime = req.end  # 获取结束时间
    interval: Interval = req.interval  # 获取间隔类型

    if not interval:  # 如果没有指定间隔类型
        interval = Interval.TICK  # 默认为Tick数据

    # 获取对应的迅投间隔字符串
    xt_interval: str = INTERVAL_VT2XT.get(interval, None)
    if not xt_interval:  # 如果不支持的间隔类型
        output(f"迅投研查询历史数据失败：不支持的时间周期{interval.value}")
        return DataFrame()  # 返回空DataFrame

    # 为了查询夜盘数据，结束时间加1天
    end += timedelta(1)

    # 构建迅投格式的合约代码
    xt_symbol: str = symbol + "." + EXCHANGE_VT2XT[exchange]
    # 格式化开始和结束时间字符串
    start: str = start.strftime("%Y%m%d%H%M%S")
    end: str = end.strftime("%Y%m%d%H%M%S")

    # 处理特殊情况：如果是股票且代码长度大于6位
    if exchange in (Exchange.SSE, Exchange.SZSE) and len(symbol) > 6:
        xt_symbol += "O"  # 添加后缀

    # 下载历史数据
    xtdata.download_history_data(xt_symbol, xt_interval, start, end)
    # 获取本地数据，默认使用等比前复权
    data: dict = xtdata.get_local_data(
        [], 
        [xt_symbol], 
        xt_interval, 
        start, 
        end, 
        -1, 
        "front_ratio", 
        False
    )  # 默认等比前复权

    # 返回对应合约的DataFrame
    df: DataFrame = data[xt_symbol]
    return df