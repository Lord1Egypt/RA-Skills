# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengApptrackGetMonitoringListRequest(BaseApi):
    """根据用户输入的计划id返回该计划id下的监测单元id

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.apptrack&n=umeng.apptrack.getMonitoringList&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.planId = None
        self.pageNum = None
        self.pageSize = None

    def get_api_uri(self):
        return '1/com.umeng.apptrack/umeng.apptrack.getMonitoringList'

    def get_required_params(self):
        return ['planId']

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
