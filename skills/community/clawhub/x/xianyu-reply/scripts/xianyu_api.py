"""闲鱼平台 API 接口封装"""

import time
import os
import re
import sys
import logging

import requests
from xianyu_utils import generate_sign

logger = logging.getLogger('xianyu-monitor')


class XianyuApis:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.goofish.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.goofish.com/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        })

    def clear_duplicate_cookies(self):
        """清理重复的 cookies"""
        new_jar = requests.cookies.RequestsCookieJar()
        added = set()
        cookie_list = list(self.session.cookies)
        cookie_list.reverse()
        for cookie in cookie_list:
            if cookie.name not in added:
                new_jar.set_cookie(cookie)
                added.add(cookie.name)
        self.session.cookies = new_jar

    def hasLogin(self, retry_count=0):
        """检查登录状态"""
        if retry_count >= 2:
            logger.error("登录检查失败")
            return False
        try:
            url = 'https://passport.goofish.com/newlogin/hasLogin.do'
            params = {'appName': 'xianyu', 'fromSite': '77'}
            data = {
                'hid': self.session.cookies.get('unb', ''),
                'ltl': 'true',
                'appName': 'xianyu',
                'appEntrance': 'web',
                '_csrf_token': self.session.cookies.get('XSRF-TOKEN', ''),
                'umidToken': '',
                'hsiz': self.session.cookies.get('cookie2', ''),
                'bizParams': 'taobaoBizLoginFrom=web',
                'mainPage': 'false',
                'isMobile': 'false',
                'lang': 'zh_CN',
                'returnUrl': '',
                'fromSite': '77',
                'isIframe': 'true',
                'documentReferer': 'https://www.goofish.com/',
                'defaultView': 'hasLogin',
                'umidTag': 'SERVER',
                'deviceId': self.session.cookies.get('cna', '')
            }
            response = self.session.post(url, params=params, data=data)
            res_json = response.json()
            if res_json.get('content', {}).get('success'):
                self.clear_duplicate_cookies()
                return True
            else:
                time.sleep(0.5)
                return self.hasLogin(retry_count + 1)
        except Exception as e:
            logger.error(f"Login 请求异常: {e}")
            time.sleep(0.5)
            return self.hasLogin(retry_count + 1)

    def get_token(self, device_id, retry_count=0):
        """获取 WebSocket 连接 Token"""
        if retry_count >= 2:
            logger.warning("Token 获取失败，尝试重新登录")
            if self.hasLogin():
                return self.get_token(device_id, 0)
            else:
                logger.error("Cookie 已失效，请更新 Cookie 后重启服务")
                sys.exit(1)

        params = {
            'jsv': '2.7.2',
            'appKey': '34839810',
            't': str(int(time.time()) * 1000),
            'sign': '',
            'v': '1.0',
            'type': 'originaljson',
            'accountSite': 'xianyu',
            'dataType': 'json',
            'timeout': '20000',
            'api': 'mtop.taobao.idlemessage.pc.login.token',
            'sessionOption': 'AutoLoginOnly',
            'spm_cnt': 'a21ybx.im.0.0',
        }
        data_val = '{"appKey":"444e9908a51d1cb236a27862abc769c9","deviceId":"' + device_id + '"}'
        data = {'data': data_val}

        token = self.session.cookies.get('_m_h5_tk', '').split('_')[0]
        sign = generate_sign(params['t'], token, data_val)
        params['sign'] = sign

        try:
            response = self.session.post(
                'https://h5api.m.goofish.com/h5/mtop.taobao.idlemessage.pc.login.token/1.0/',
                params=params, data=data
            )
            res_json = response.json()

            if isinstance(res_json, dict):
                ret_value = res_json.get('ret', [])
                if not any('SUCCESS::调用成功' in ret for ret in ret_value):
                    error_msg = str(ret_value)
                    if 'RGV587_ERROR' in error_msg or '被挤爆啦' in error_msg:
                        logger.error(f"触发风控: {ret_value}")
                        logger.error("请在浏览器过验证后重新获取 Cookie")
                        sys.exit(1)

                    if 'Set-Cookie' in response.headers:
                        self.clear_duplicate_cookies()
                    time.sleep(0.5)
                    return self.get_token(device_id, retry_count + 1)
                else:
                    return res_json
            else:
                return self.get_token(device_id, retry_count + 1)
        except Exception as e:
            logger.error(f"Token API 请求异常: {e}")
            time.sleep(0.5)
            return self.get_token(device_id, retry_count + 1)

    def get_item_info(self, item_id, retry_count=0):
        """获取商品信息"""
        if retry_count >= 3:
            return {"error": "获取商品信息失败"}

        params = {
            'jsv': '2.7.2',
            'appKey': '34839810',
            't': str(int(time.time()) * 1000),
            'sign': '',
            'v': '1.0',
            'type': 'originaljson',
            'accountSite': 'xianyu',
            'dataType': 'json',
            'timeout': '20000',
            'api': 'mtop.taobao.idle.pc.detail',
            'sessionOption': 'AutoLoginOnly',
            'spm_cnt': 'a21ybx.im.0.0',
        }
        data_val = '{"itemId":"' + item_id + '"}'
        data = {'data': data_val}

        token = self.session.cookies.get('_m_h5_tk', '').split('_')[0]
        sign = generate_sign(params['t'], token, data_val)
        params['sign'] = sign

        try:
            response = self.session.post(
                'https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/',
                params=params, data=data
            )
            res_json = response.json()
            if isinstance(res_json, dict):
                ret_value = res_json.get('ret', [])
                if not any('SUCCESS::调用成功' in ret for ret in ret_value):
                    if 'Set-Cookie' in response.headers:
                        self.clear_duplicate_cookies()
                    time.sleep(0.5)
                    return self.get_item_info(item_id, retry_count + 1)
                else:
                    return res_json
            else:
                return self.get_item_info(item_id, retry_count + 1)
        except Exception as e:
            logger.error(f"商品信息 API 请求异常: {e}")
            time.sleep(0.5)
            return self.get_item_info(item_id, retry_count + 1)
