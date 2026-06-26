# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengApptrackGetMyEventDataRequest(BaseApi):
    """根据用户输入的计划id或者监测单元id返回用户自定义事件数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.apptrack&n=umeng.apptrack.getMyEventData&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.planId = None
        self.unitId = None
        self.queryDate = None

    def get_api_uri(self):
        return '1/com.umeng.apptrack/umeng.apptrack.getMyEventData'

    def get_required_params(self):
        return ['planId', 'queryDate']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return False

    def is_inner_api(self):
        return False
