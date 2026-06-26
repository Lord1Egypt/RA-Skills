# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiInitMultiLevelTreeRequest(BaseApi):
    """上传层级分组结构

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.initMultiLevelTree&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.dataSourceId = None
        self.treeJson = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.initMultiLevelTree'

    def get_required_params(self):
        return ['dataSourceId', 'treeJson']

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
