# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappEventParamListRequest(BaseApi):
    """获取自定义事件的参数列表

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.event.param.list&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.startDate = None
        self.endDate = None
        self.eventId = None
        self.appkey = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.event.param.list'

    def get_required_params(self):
        return ['startDate', 'endDate', 'eventId', 'appkey']

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
