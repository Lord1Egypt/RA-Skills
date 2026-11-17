import json
import os
import sys
import time
import random
import struct
import subprocess
import uuid
import zlib

import requests
import qrcode
from loguru import logger

from xhs_utils.http_util import REQUEST_TIMEOUT
from xhs_utils.xhs_util import generate_headers, generate_xs_xs_common, splice_str
from xhs_utils.common_util import generate_a1, generate_web_id

# 二维码 PNG 默认保存路径（与 cookie 同目录，便于查找/重扫）
_QR_DIR = os.path.expanduser("~/.xiaohongshu")
_QR_DEFAULT_PATH = os.path.join(_QR_DIR, "qrcode.png")


def _write_qr_png(matrix, path, scale=10):
    """把二维码矩阵写为 1-bit 黑白 PNG，仅用标准库(zlib/struct)，无需 Pillow。

    matrix: list[list[bool]]，True=暗(黑)模块（qrcode.QRCode.get_matrix() 的返回）。
    scale: 每个模块放大成 scale×scale 像素，提升物理尺寸便于扫码。"""
    h_mod = len(matrix)
    w_mod = len(matrix[0]) if h_mod else 0
    w = w_mod * scale
    h = h_mod * scale
    row_bytes = (w + 7) // 8

    raw = bytearray()
    for y in range(h):
        raw.append(0)  # PNG 行过滤器: None
        my = y // scale
        byte = 0
        bits = 0
        for x in range(w):
            mx = x // scale
            bit = 1 if matrix[my][mx] else 0  # 1=黑(暗), 0=白(亮)
            byte = (byte << 1) | bit
            bits += 1
            if bits == 8:
                raw.append(byte)
                byte = 0
                bits = 0
        if bits:
            byte <<= (8 - bits)
            raw.append(byte)

    def _chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack('>IIBBBBB', w, h, 1, 0, 0, 0, 0)  # 1-bit grayscale
    idat = zlib.compress(bytes(raw), 9)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(_chunk(b'IHDR', ihdr))
        f.write(_chunk(b'IDAT', idat))
        f.write(_chunk(b'IEND', b''))


class XHSLoginApi:
    def __init__(self):
        self.base_url = "https://edith.xiaohongshu.com"
        self.as_url = "https://as.xiaohongshu.com"
        self.home_url = 'https://www.xiaohongshu.com/explore'

    @staticmethod
    def _get_sec_headers():
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'origin': 'https://www.xiaohongshu.com',
            'referer': 'https://www.xiaohongshu.com/',
        }

    def _fetch_sec_cookies(self, cookies):
        api = '/api/sec/v1/scripting'
        data = {"callFrom": "web", "callback": "", "type": "ds", "appId": "xhs-pc-web"}

        xs, xt, xs_common = generate_xs_xs_common(cookies['a1'], api, data)
        headers = self._get_sec_headers()
        headers['x-s'] = xs
        headers['x-t'] = str(xt)
        headers['x-s-common'] = xs_common

        data_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        try:
            resp = requests.post(
                self.as_url + api,
                headers=headers, cookies=cookies,
                data=data_str.encode('utf-8'),
                timeout=REQUEST_TIMEOUT
            )
            res = resp.json()
            return res.get('data', {}).get('secPoisonId')
        except Exception as e:
            logger.debug(f'fetch sec_poison_id failed: {e}')
            return None

    def _fetch_gid(self, cookies):
        api = '/api/sec/v1/shield/webprofile'
        data = {"platform": "Windows", "sdkVersion": "4.3.5", "svn": "2", "profileData": ""}

        xs, xt, xs_common = generate_xs_xs_common(cookies['a1'], api, data)
        headers = self._get_sec_headers()
        headers['x-s'] = xs
        headers['x-t'] = str(xt)
        headers['x-s-common'] = xs_common

        data_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        try:
            resp = requests.post(
                self.as_url + api,
                headers=headers, cookies=cookies,
                data=data_str.encode('utf-8'),
                timeout=REQUEST_TIMEOUT
            )
            for key, value in resp.cookies.items():
                cookies[key] = value
            return cookies.get('gid')
        except Exception as e:
            logger.debug(f'fetch gid failed: {e}')
            return None

    def generate_init_cookies(self):
        ts = int(time.time() * 1000)
        a1 = generate_a1()
        web_id = generate_web_id(a1)
        cookies = {
            'abRequestId': str(uuid.uuid4()),
            'ets': str(ts),
            'webBuild': '6.7.4',
            'xsecappid': 'xhs-pc-web',
            'loadts': str(ts + random.randint(50, 200)),
            'a1': a1,
            'webId': web_id,
        }

        sec_poison_id = self._fetch_sec_cookies(cookies)
        if sec_poison_id:
            cookies['sec_poison_id'] = sec_poison_id

        gid = self._fetch_gid(cookies)
        if gid:
            cookies['gid'] = gid

        return cookies

    def generate_qrcode(self, cookies):
        api = '/api/sns/web/v1/login/qrcode/create'
        data = {"qr_type": 1}

        headers, data = generate_headers(cookies['a1'], api, data)
        resp = requests.post(
            self.base_url + api,
            headers=headers, cookies=cookies, data=data,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        if not res.get('success'):
            return False, res.get('msg', '未知错误'), None
        data = res.get('data') or {}
        if not all(key in data for key in ('qr_id', 'code', 'url')):
            return False, res.get('msg', '二维码响应缺少必要字段'), {'cookies': cookies, 'res_json': res}

        return True, '成功', {
            'cookies': cookies,
            'qr_id': data['qr_id'],
            'code': data['code'],
            'qr_url': data['url'],
        }

    def check_qrcode_status(self, qr_id, code, cookies):
        api = '/api/qrcode/userinfo'
        data = {"qrId": qr_id, "code": code}

        headers, data = generate_headers(cookies['a1'], api, data)
        resp = requests.post(
            self.base_url + api,
            headers=headers, cookies=cookies, data=data,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        status = (res.get('data') or {}).get('codeStatus')
        if status is None:
            return False, res.get('msg', '二维码状态响应缺少 codeStatus'), cookies

        if status == 2:
            cookies = self._login_by_qrcode_status(qr_id, code, cookies)

        status_map = {
            0: (False, '请扫描二维码'),
            1: (False, '请确认登录'),
            2: (True, '验证成功'),
            3: (False, '二维码已过期'),
        }
        success, msg = status_map.get(status, (False, f'未知状态: {status}'))
        return success, msg, cookies

    def _login_by_qrcode_status(self, qr_id, code, cookies):
        api = '/api/sns/web/v1/login/qrcode/status'
        params = {"qr_id": qr_id, "code": code}
        splice_api = splice_str(api, params)

        headers, _ = generate_headers(cookies['a1'], splice_api, method='GET')
        resp = requests.get(
            self.base_url + splice_api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        if res.get('success') and 'login_info' in res.get('data', {}):
            login_info = res['data']['login_info']
            if 'session' in login_info and 'web_session' not in cookies:
                cookies['web_session'] = login_info['session']

        return cookies

    def get_user_info(self, cookies):
        api = '/api/sns/web/v2/user/me'

        headers, _ = generate_headers(cookies['a1'], api)
        resp = requests.get(
            self.base_url + api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        return res.get('success', False), res.get('data', {}), cookies

    def send_phone_code(self, phone, cookies, zone='86'):
        api = '/api/sns/web/v2/login/send_code'
        params = {"phone": phone, "zone": zone, "type": "login"}
        splice_api = splice_str(api, params)

        headers, _ = generate_headers(cookies['a1'], splice_api)
        resp = requests.get(
            self.base_url + splice_api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        res = resp.json()
        return res.get('success', False), res.get('msg', ''), res

    def login_by_phone(self, phone, code, cookies, zone='86'):
        check_api = '/api/sns/web/v1/login/check_code'
        params = {"phone": phone, "zone": zone, "code": code}
        splice_api = splice_str(check_api, params)

        headers, _ = generate_headers(cookies['a1'], splice_api)
        resp = requests.get(
            self.base_url + splice_api,
            headers=headers, cookies=cookies,
            timeout=REQUEST_TIMEOUT
        )
        res = resp.json()
        if not res.get('success'):
            return False, res.get('msg', '验证码验证失败'), {'cookies': cookies}
        mobile_token = (res.get('data') or {}).get('mobile_token')
        if not mobile_token:
            return False, res.get('msg', '验证码响应缺少 mobile_token'), {'cookies': cookies, 'res_json': res}

        login_api = '/api/sns/web/v2/login/code'
        data = {"mobile_token": mobile_token, "zone": zone, "phone": phone}
        headers, data = generate_headers(cookies['a1'], login_api, data)
        resp = requests.post(
            self.base_url + login_api,
            headers=headers, cookies=cookies, data=data,
            timeout=REQUEST_TIMEOUT
        )
        for key, value in resp.cookies.items():
            cookies[key] = value

        res = resp.json()
        if not res.get('success'):
            return False, res.get('msg', '登录失败'), {'cookies': cookies}
        session = (res.get('data') or {}).get('session')
        if not session:
            return False, res.get('msg', '登录响应缺少 session'), {'cookies': cookies, 'res_json': res}
        cookies['web_session'] = session
        return True, '成功', {
            'cookies': cookies,
            'res_json': res,
        }

    @staticmethod
    def cookies_to_str(cookies):
        return '; '.join(f'{k}={v}' for k, v in cookies.items())

    @staticmethod
    def show_qrcode_terminal(url):
        """终端渲染二维码：用半块字符(▀▄█)把 2 个模块行压成 1 行，比 print_ascii 更接近正方形、更易扫码。

        深色终端下，暗(黑)模块留空融入背景、亮(白)模块填块，颜色虽反转但主流扫码器均支持。"""
        qr = qrcode.QRCode(box_size=1, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        matrix = qr.get_matrix()  # True=暗(黑)模块
        for y in range(0, len(matrix), 2):
            line = []
            for x in range(len(matrix[0])):
                top_dark = matrix[y][x]
                bottom_dark = y + 1 < len(matrix) and matrix[y + 1][x]
                if not top_dark and not bottom_dark:
                    line.append('█')      # 上下都亮
                elif not top_dark and bottom_dark:
                    line.append('▀')      # 仅上亮
                elif top_dark and not bottom_dark:
                    line.append('▄')      # 仅下亮
                else:
                    line.append(' ')      # 上下都暗
            print(''.join(line))

    @staticmethod
    def show_qrcode_image(url, save_path=None, open_viewer=True):
        """保存二维码为 PNG（持久化到磁盘），可选调用系统图片查看器打开。返回保存路径。

        用标准库直接编码 1-bit PNG，无需 Pillow 依赖。持久化 PNG 可重复扫码、
        在 SSH/无头环境下查看器打不开时也能凭打印的路径取用。"""
        save_path = save_path or _QR_DEFAULT_PATH
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        qr = qrcode.QRCode(box_size=1, border=4)  # border=4 是标准静区，矩阵内已含
        qr.add_data(url)
        qr.make(fit=True)
        _write_qr_png(qr.get_matrix(), save_path, scale=10)
        logger.info(f'二维码已保存为图片: {save_path}')
        if open_viewer:
            XHSLoginApi._open_file(save_path)
        return save_path

    @staticmethod
    def _open_file(path):
        """跨平台用系统默认程序打开文件（macOS=open / Linux=xdg-open / Windows=startfile）"""
        try:
            if sys.platform == 'darwin':
                subprocess.Popen(['open', path])
            elif os.name == 'nt':
                os.startfile(path)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(['xdg-open', path])
        except Exception as e:
            logger.debug(f'打开图片查看器失败（可手动打开上面的路径）: {e}')

    def qrcode_login(self, show_in_terminal=False, qr_save_path=None, open_viewer=True):
        """QR码登录。

        默认 show_in_terminal=False：保存二维码 PNG 并用系统查看器打开（最易扫码）。
        show_in_terminal=True：终端字符渲染（SSH 等无图形界面场景的兜底）。
        无论哪种模式都会打印二维码 URL，作为最终兜底（可用任意二维码生成器扫码）。"""
        logger.info('[1/4] 正在生成初始cookies...')
        cookies = self.generate_init_cookies()
        logger.info(f'{cookies}')

        logger.info('[2/4] 正在获取二维码...')
        success, msg, qr_data = self.generate_qrcode(cookies)
        if not success:
            logger.error(f'获取二维码失败: {msg}')
            return None
        cookies = qr_data['cookies']

        logger.info('请使用小红书APP扫描二维码:')
        logger.info(f'二维码URL(兜底，可复制到任意二维码生成器): {qr_data["qr_url"]}')
        if show_in_terminal:
            self.show_qrcode_terminal(qr_data['qr_url'])
        else:
            self.show_qrcode_image(qr_data['qr_url'], save_path=qr_save_path, open_viewer=open_viewer)

        logger.info('[3/4] 等待扫码...')
        while True:
            success, msg, cookies = self.check_qrcode_status(
                qr_data['qr_id'], qr_data['code'], cookies
            )
            if success:
                logger.info(msg)
                break
            if msg == '二维码已过期':
                logger.error(msg)
                return None
            time.sleep(2)

        logger.info('[4/4] 验证登录状态...')
        success, user_info, cookies = self.get_user_info(cookies)
        if success:
            logger.info(f'用户: {user_info.get("nickname", "未知")} (RedID: {user_info.get("red_id", "未知")})')
        else:
            logger.warning('获取用户信息失败，但cookies可能仍有效')

        # 防御性校验：web_session 缺失会导致后续 search/feed 报"无登录信息"
        if 'web_session' not in cookies:
            logger.error(
                '⚠️ 登录cookie缺少 web_session，search/feed 将失败。'
                '请改用 set-cookie 手动补全：python scripts/xhs.py set-cookie --cookie "a1=...; web_session=..."'
            )

        cookies_str = self.cookies_to_str(cookies)
        logger.success(f'登录成功!\ncookies:\n{cookies_str}')
        return cookies_str

    def phone_login(self):
        logger.info('[1/4] 正在生成初始cookies...')
        cookies = self.generate_init_cookies()
        logger.info(f'a1={cookies["a1"]}')

        phone = input('请输入手机号: ')
        logger.info('[2/4] 正在发送验证码...')
        success, msg, _ = self.send_phone_code(phone, cookies)
        if not success:
            logger.error(f'发送失败: {msg}')
            return None
        logger.info('验证码已发送')

        code = input('请输入验证码: ')
        logger.info('[3/4] 正在验证...')
        success, msg, result = self.login_by_phone(phone, code, cookies)
        if not success:
            logger.error(f'验证失败: {msg}')
            return None
        cookies = result['cookies']

        logger.info('[4/4] 验证登录状态...')
        success, user_info, cookies = self.get_user_info(cookies)
        if success:
            logger.info(f'用户: {user_info.get("nickname", "未知")} (RedID: {user_info.get("red_id", "未知")})')

        cookies_str = self.cookies_to_str(cookies)
        logger.success(f'登录成功!\ncookies:\n{cookies_str}')
        return cookies_str


if __name__ == '__main__':
    login_api = XHSLoginApi()
    cookies_str = login_api.qrcode_login(show_in_terminal=True)
    if cookies_str:
        print(f'登录成功! cookies: {cookies_str[:80]}...')
    else:
        print('登录失败')
