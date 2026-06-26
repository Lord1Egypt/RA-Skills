from xtquant import xtdata

from .xt_gateway import *


class XtGateway(XtGateway):
    def __init__(self, event_engine: EventEngine, gateway_name: str) -> None:
        """构造函数"""
        # 不调用父类XtGateway的__init__
        # super().__init__(event_engine, gateway_name)
        # 直接调用祖父类 BaseGateway 的 __init__
        BaseGateway.__init__(self, event_engine, gateway_name)

        # 初始化行情和交易API
        self.md_api: "XtMdApi" = XtMdApi(self)
        self.td_api: "XtTdApi" = XtTdApi(self)

        self.trading: bool = False  # 是否交易模式
        self.orders: dict[str, OrderData] = {}  # 委托订单字典

        self.thread: Thread = None  # 连接线程


class XtMdApi(XtMdApi):
    def __init__(self, gateway: XtGateway) -> None:
        super().__init__(gateway)
        self.code_list = []

    # 方法覆写
    def onMarketData(self, data: dict) -> None:
        """行情推送回调（来自 subscribe_quote 的订阅）"""
        for xt_symbol, d in data.items():
            # 解析合约代码和交易所
            symbol, xt_exchange = xt_symbol.split(".")
            exchange = EXCHANGE_XT2VT[xt_exchange]

            # 创建Tick数据对象
            tick: TickData = TickData(
                symbol=symbol,
                exchange=exchange,
                datetime=generate_datetime(d["time"]),  # 生成时间
                volume=d["volume"],  # 成交量
                turnover=d["amount"],  # 成交额
                open_interest=d["openInt"],  # 持仓量
                gateway_name=self.gateway_name
            )

            # 获取合约信息
            contract = symbol_contract_map[tick.vt_symbol]
            tick.name = contract.name  # 合约名称

            # 设置买卖盘数据
            bp_data: list = d["bidPrice"]
            ap_data: list = d["askPrice"]
            bv_data: list = d["bidVol"]
            av_data: list = d["askVol"]

            # 设置五档行情
            tick.bid_price_1 = round_to(bp_data[0], contract.pricetick)
            tick.bid_price_2 = round_to(bp_data[1], contract.pricetick)
            tick.bid_price_3 = round_to(bp_data[2], contract.pricetick)
            tick.bid_price_4 = round_to(bp_data[3], contract.pricetick)
            tick.bid_price_5 = round_to(bp_data[4], contract.pricetick)

            tick.ask_price_1 = round_to(ap_data[0], contract.pricetick)
            tick.ask_price_2 = round_to(ap_data[1], contract.pricetick)
            tick.ask_price_3 = round_to(ap_data[2], contract.pricetick)
            tick.ask_price_4 = round_to(ap_data[3], contract.pricetick)
            tick.ask_price_5 = round_to(ap_data[4], contract.pricetick)

            tick.bid_volume_1 = bv_data[0]
            tick.bid_volume_2 = bv_data[1]
            tick.bid_volume_3 = bv_data[2]
            tick.bid_volume_4 = bv_data[3]
            tick.bid_volume_5 = bv_data[4]

            tick.ask_volume_1 = av_data[0]
            tick.ask_volume_2 = av_data[1]
            tick.ask_volume_3 = av_data[2]
            tick.ask_volume_4 = av_data[3]
            tick.ask_volume_5 = av_data[4]

            # 设置其他行情数据
            tick.last_price = round_to(d["lastPrice"], contract.pricetick)
            tick.open_price = round_to(d["open"], contract.pricetick)
            tick.high_price = round_to(d["high"], contract.pricetick)
            tick.low_price = round_to(d["low"], contract.pricetick)
            tick.pre_close = round_to(d["lastClose"], contract.pricetick)

            # 设置涨跌停价
            if tick.vt_symbol in symbol_limit_map:
                tick.limit_up, tick.limit_down = symbol_limit_map[tick.vt_symbol]

            # 推送Tick数据
            self.gateway.on_tick(tick)

    # 方法覆写
    def query_contracts(self) -> None:
        """查询合约信息"""
        super().query_contracts()
        self.auto_subscribe()  # 自动订阅全市场

    # 方法覆写
    def subscribe(self, req: SubscribeRequest) -> None:
        pass

    def auto_subscribe(self) -> None:
        """自动订阅"""
        # 添加反向映射：字符串交易所名称 → Exchange 枚举
        EXCHANGE_STR2VT = {exchange.name: exchange for exchange in Exchange}

        for vt_symbol, d in symbol_contract_map.items():
            # 解析合约代码和交易所
            symbol, vt_exchange_str = vt_symbol.split(".")
            vt_exchange = EXCHANGE_STR2VT[vt_exchange_str]  # 将字符串转换为 Exchange 枚举
            exchange = EXCHANGE_VT2XT[vt_exchange]  # 获取迅投交易所代码
            self.code_list.append(symbol + '.' + exchange)

        swq = xtdata.subscribe_whole_quote(code_list=self.code_list, callback=self.onMarketData)
        if swq > 0:
            self.gateway.write_log("自动订阅成功")
        elif swq == -1:
            self.gateway.write_log("自动订阅失败")
