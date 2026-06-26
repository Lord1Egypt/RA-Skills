# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiEditPathDisplayNameRequest(BaseApi):
    """编辑页面路径显示名称

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.editPathDisplayName&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.dataSourceId = None
        self.displayName = None
        self.path = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.editPathDisplayName'

    def get_required_params(self):
        return ['dataSourceId', 'displayName', 'path']

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
