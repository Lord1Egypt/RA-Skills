# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiCreateMiniAppRequest(BaseApi):
    """新建小程序数据源

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.createMiniApp&v=1&cat=default

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
        self.miniAppId = None
        self.miniAppSecret = None
        self.miniPublicKey = None
        self.miniPrivateKey = None
        self.integrationType = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.createMiniApp'

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
