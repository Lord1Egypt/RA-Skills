"""
自动生成的同花顺数据请求函数
"""

class THSProtocol:
    """同花顺数据协议"""
    
    @staticmethod
    def build_request(msg_id: int, **kwargs) -> str:
        """构建请求数据包"""
        params = [f"id={msg_id}"]
        for key, value in kwargs.items():
            if isinstance(value, list):
                params.append(f"{key}={','.join(map(str, value))}")
            else:
                params.append(f"{key}={value}")
        return "&".join(params)


    @staticmethod
    def get_分时查询(code: str, **kwargs) -> str:
        """获取分时查询
        操作: 个股-分时
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(207, **params)

    @staticmethod
    def get_ai相似个股(code: str, **kwargs) -> str:
        """获取AI相似个股
        操作: 个股-AI相似个股
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1007, **params)

    @staticmethod
    def get_个股资讯(code: str, **kwargs) -> str:
        """获取个股资讯
        操作: 个股-资讯
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1001, **params)

    @staticmethod
    def get_个股权息(code: str, **kwargs) -> str:
        """获取个股权息
        操作: 个股-K线
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(211, **params)

    @staticmethod
    def get_深市a股市场涨幅排名(code: str, **kwargs) -> str:
        """获取深市A股市场涨幅排名
        操作: 沪深-沪深A股-深市A股
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(6, **params)

    @staticmethod
    def get_键盘精灵(code: str, **kwargs) -> str:
        """获取键盘精灵
        操作: 键盘精灵中输入56
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(8, **params)

    @staticmethod
    def get_通过股票代码查询市场(code: str, **kwargs) -> str:
        """获取通过股票代码查询市场
        操作: 初始化股票预警
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(9, **params)

    @staticmethod
    def get_成交明细(code: str, **kwargs) -> str:
        """获取成交明细
        操作: 个股-涨跌停股票
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(10, **params)

    @staticmethod
    def get_请求所属行业(code: str, **kwargs) -> str:
        """获取请求所属行业
        操作: 个股-K线-区间统计
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(102, **params)

    @staticmethod
    def get_获取板块数据(code: str, **kwargs) -> str:
        """获取获取板块数据
        操作: 行情登陆
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(103, **params)

    @staticmethod
    def get_深指前置数据查询(code: str, **kwargs) -> str:
        """获取深指前置数据查询
        操作: 主页底部深指行情
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(200, **params)

    @staticmethod
    def get_创指补充数据查询(code: str, **kwargs) -> str:
        """获取创指补充数据查询
        操作: 在有创指的列表中左右拖动
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(201, **params)

    @staticmethod
    def get_5分钟涨速排名(code: str, **kwargs) -> str:
        """获取5分钟涨速排名
        操作: 个股-盯盘助手
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(202, **params)

    @staticmethod
    def get_集合竞价数据(code: str, **kwargs) -> str:
        """获取集合竞价数据
        操作: 个股-分时
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(204, **params)

    @staticmethod
    def get_个股成交明细(code: str, **kwargs) -> str:
        """获取个股成交明细
        操作: 个股-明细
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(205, **params)

    @staticmethod
    def get_个股时间轴获取(code: str, **kwargs) -> str:
        """获取个股时间轴获取
        操作: 个股-分时
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(209, **params)

    @staticmethod
    def get_个股换手率(code: str, **kwargs) -> str:
        """获取个股换手率
        操作: 个股-换手
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(212, **params)

    @staticmethod
    def get_个股历史收盘价(code: str, **kwargs) -> str:
        """获取个股历史收盘价
        操作: 个股-K线
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(213, **params)

    @staticmethod
    def get_期货数据查询(code: str, **kwargs) -> str:
        """获取期货数据查询
        操作: 扩展-期货
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(240, **params)

    @staticmethod
    def get_资讯树(code: str, **kwargs) -> str:
        """获取资讯树
        操作: 行情登陆
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1000, **params)

    @staticmethod
    def get_信息地雷(code: str, **kwargs) -> str:
        """获取信息地雷
        操作: 工具-启用信息地雷；打开个股日线
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1002, **params)

    @staticmethod
    def get_个股分时(code: str, **kwargs) -> str:
        """获取个股分时
        操作: 工具-启用信息地雷；打开个股分时
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1003, **params)

    @staticmethod
    def get_历史信息地雷(code: str, **kwargs) -> str:
        """获取历史信息地雷
        操作: 个股-日线-查看信息地雷
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1005, **params)

    @staticmethod
    def get_当日信息地雷(code: str, **kwargs) -> str:
        """获取当日信息地雷
        操作: 个股-分时-查看信息地雷
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1006, **params)

    @staticmethod
    def get_融资融券数据(code: str, **kwargs) -> str:
        """获取融资融券数据
        操作: 切换个股
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1600, **params)

    @staticmethod
    def get_深市短线精灵(code: str, **kwargs) -> str:
        """获取深市短线精灵
        操作: 个股-盯盘助手
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(1701, **params)

    @staticmethod
    def get_深证系列指数(code: str, **kwargs) -> str:
        """获取深证系列指数
        操作: 沪深指数-深证系列指数
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(7, **params)

    @staticmethod
    def get_中港股对比列表(code: str, **kwargs) -> str:
        """获取中港股对比列表
        操作: 港股-中港对比
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(101, **params)

    @staticmethod
    def get_个股分时k线(code: str, **kwargs) -> str:
        """获取个股分时K线
        操作: 个股-日线
        """
        params = {'code': code, **kwargs}
        return THSProtocol.build_request(210, **params)
