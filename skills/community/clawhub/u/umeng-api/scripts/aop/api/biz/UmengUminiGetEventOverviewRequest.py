# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiGetEventOverviewRequest(BaseApi):
    """获取某自定义事件统计数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.getEventOverview&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.timeUnit = None
        self.fromDate = None
        self.toDate = None
        self.eventName = None
        self.dataSourceId = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.getEventOverview'

    def get_required_params(self):
        return ['timeUnit', 'fromDate', 'toDate', 'eventName', 'dataSourceId']

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
