# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappGetNewUsersByChannelOrVersionRequest(BaseApi):
    """根据渠道或版本条件，获取指定App某个时间范围内的新增用户数

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getNewUsersByChannelOrVersion&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appkey = None
        self.startDate = None
        self.endDate = None
        self.periodType = None
        self.channels = None
        self.versions = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.getNewUsersByChannelOrVersion'

    def get_required_params(self):
        return ['appkey', 'startDate', 'endDate', 'periodType']

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
