# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappGetTodayDataRequest(BaseApi):
    """获取指定App今日的统计数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getTodayData&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appkey = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.getTodayData'

    def get_required_params(self):
        return ['appkey']

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
