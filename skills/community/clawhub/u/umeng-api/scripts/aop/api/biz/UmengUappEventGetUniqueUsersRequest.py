# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappEventGetUniqueUsersRequest(BaseApi):
    """获取自定义事件的独立用户数统计数据（按设备device统计 "data":[{"data":[123],"dates":["2018-01-01"]}）

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.event.getUniqueUsers&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appkey = None
        self.startDate = None
        self.endDate = None
        self.eventName = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.event.getUniqueUsers'

    def get_required_params(self):
        return ['appkey', 'startDate', 'endDate', 'eventName']

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
