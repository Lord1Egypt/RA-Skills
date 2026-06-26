# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappCreateAppRequest(BaseApi):
    """U-App新建数据源

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.createApp&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.name = None
        self.type = None
        self.platform = None
        self.language = None
        self.firstLevel = None
        self.secondLevel = None
        self.description = None

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.createApp'

    def get_required_params(self):
        return ['name', 'type', 'platform', 'language', 'firstLevel', 'secondLevel']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def is_inner_api(self):
        return False
