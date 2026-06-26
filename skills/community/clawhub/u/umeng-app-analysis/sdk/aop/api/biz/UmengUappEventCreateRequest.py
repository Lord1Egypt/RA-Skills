# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappEventCreateRequest(BaseApi):
    """创建自定义事件

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.event.create&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appkey = None
        self.eventName = None
        self.eventDisplayName = None
        self.eventType = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.event.create'

    def get_required_params(self):
        return ['appkey', 'eventName', 'eventDisplayName']

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
