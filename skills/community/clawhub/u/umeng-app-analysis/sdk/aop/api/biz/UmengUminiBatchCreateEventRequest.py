# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiBatchCreateEventRequest(BaseApi):
    """批量创建事件

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.batchCreateEvent&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.dataSourceId = None
        self.eventList = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.batchCreateEvent'

    def get_required_params(self):
        return ['dataSourceId', 'eventList']

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
