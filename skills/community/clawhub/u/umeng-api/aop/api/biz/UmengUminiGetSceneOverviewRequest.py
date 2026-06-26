# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiGetSceneOverviewRequest(BaseApi):
    """获取某场景值的统计数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.getSceneOverview&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.timeUnit = None
        self.fromDate = None
        self.toDate = None
        self.scene = None
        self.pageIndex = None
        self.pageSize = None
        self.dataSourceId = None
        self.indicators = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.getSceneOverview'

    def get_required_params(self):
        return ['timeUnit', 'fromDate', 'toDate', 'scene', 'dataSourceId', 'indicators']

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
