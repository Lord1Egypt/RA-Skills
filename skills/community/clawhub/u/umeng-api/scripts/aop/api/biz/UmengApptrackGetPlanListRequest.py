# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengApptrackGetPlanListRequest(BaseApi):
    """根据用户id获得用户计划列表

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.apptrack&n=umeng.apptrack.getPlanList&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appKey = None
        self.pageNum = None
        self.pageSize = None

    def get_api_uri(self):
        return '1/com.umeng.apptrack/umeng.apptrack.getPlanList'

    def get_required_params(self):
        return []

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
