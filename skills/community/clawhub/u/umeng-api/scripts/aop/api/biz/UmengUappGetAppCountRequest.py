# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUappGetAppCountRequest(BaseApi):
    """获取当前用户所有App的数量

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.uapp&n=umeng.uapp.getAppCount&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)

    def get_api_uri(self):
        return '1/com.umeng.uapp/umeng.uapp.getAppCount'

    def get_required_params(self):
        return []

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
