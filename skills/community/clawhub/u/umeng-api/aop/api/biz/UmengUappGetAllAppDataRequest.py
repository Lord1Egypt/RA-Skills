# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappGetAllAppDataRequest(BaseApi):
    """获取当前用户所有App昨日和今日的基础统计数据（活跃用户数，新增用户数，启动次数，总用户数）

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getAllAppData&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.getAllAppData'

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
