# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappEventParamGetValueDurationListRequest(BaseApi):
    """根据自定义事件参数值，获取使用时长

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.event.param.getValueDurationList&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appkey = None
        self.startDate = None
        self.endDate = None
        self.eventName = None
        self.eventParamName = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.event.param.getValueDurationList'

    def get_required_params(self):
        return ['appkey', 'startDate', 'endDate', 'eventName', 'eventParamName']

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
