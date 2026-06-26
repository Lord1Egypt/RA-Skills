# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiGetChannelOverviewRequest(BaseApi):
    """获取某推广渠道的统计数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.getChannelOverview&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.fromDate = None
        self.toDate = None
        self.channel = None
        self.timeUnit = None
        self.dataSourceId = None
        self.indicators = None
        self.pageIndex = None
        self.pageSize = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.getChannelOverview'

    def get_required_params(self):
        return ['fromDate', 'toDate', 'channel', 'timeUnit', 'dataSourceId', 'indicators']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def is_inner_api(self):
        return False
