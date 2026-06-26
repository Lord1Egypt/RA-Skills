# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappEventParamGetDataRequest(BaseApi):
    """获取自定义事件某个参数按照值维度的统计数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.event.param.getData&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appkey = None
        self.startDate = None
        self.endDate = None
        self.eventName = None
        self.eventParamName = None
        self.paramValueName = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.event.param.getData'

    def get_required_params(self):
        return ['appkey', 'startDate', 'endDate', 'eventName', 'eventParamName', 'paramValueName']

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
