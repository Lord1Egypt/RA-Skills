#!/usr/bin/env python3
"""
learn_api.py — 清华网络学堂 HTTP API 封装
所有数据查询通过此模块，API 优先，必要时回退 DOM。
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, json, time, base64, re
import requests
from urllib.parse import urlencode, quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import get_state_file, get_semester, get_download_dir_abs

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION_FILE = get_state_file()
DOWNLOAD_DIR = get_download_dir_abs()
LEARN_BASE = "https://learn.tsinghua.edu.cn"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": LEARN_BASE + "/",
}

AJAX_HEADERS = {
    **DEFAULT_HEADERS,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}

def escape_filename(s):
    for ch in [' ', '\t', '?', '/', "'", '"', '<', '>', '#', ';', '*', '|', '\\']:
        s = s.replace(ch, '_')
    return s


def _safe_json(r):
    try:
        return r.json()
    except Exception:
        return {}


def _get_items(data):
    if isinstance(data, dict):
        obj = data.get("object", data)
        if isinstance(obj, dict):
            return obj.get("aaData", [])
        if isinstance(obj, list):
            return obj
    elif isinstance(data, list):
        return data
    return []


class LearnAPI:
    def __init__(self, session_file=None):
        self.session_file = session_file or SESSION_FILE
        self.session = None
        self.valid = False
        self.cookies = {}
        self.xsrf_token = None
        self._semester = None  # auto-detected after reload_session
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # ====== Session 管理 ======

    def reload_session(self):
        if not os.path.exists(self.session_file):
            self.valid = False
            return False
        try:
            state = json.load(open(self.session_file, encoding='utf-8'))
        except Exception:
            self.valid = False
            return False

        jsession = state.get('learn_jsession', '')
        csrf = state.get('csrf', '')

        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        for domain in ['.tsinghua.edu.cn', 'learn.tsinghua.edu.cn', 'id.tsinghua.edu.cn']:
            self.session.cookies.set('JSESSIONID', jsession, domain=domain, path='/', secure=False)
            self.session.cookies.set('XSRF-TOKEN', csrf, domain=domain, path='/', secure=False)
        self.xsrf_token = csrf
        if csrf:
            self.session.headers.update({"X-XSRF-TOKEN": csrf})

        ok = self._check_valid()
        if ok:
            detected = self.get_current_semester()
            self._semester = detected or get_semester()
        return ok

    def _check_valid(self):
        """轻量检测 session，不依赖 semester 参数。"""
        if not self.session:
            self.valid = False
            return False
        try:
            r = self.session.get(
                f"{LEARN_BASE}/b/wlxt/kczy/zy/student/index/zyListWj?wlkcid=&size=1",
                headers={**AJAX_HEADERS, "X-XSRF-TOKEN": self.xsrf_token} if self.xsrf_token else AJAX_HEADERS,
                timeout=8
            )
            valid = r.status_code == 200 and "location.href" not in r.text[:500]
            self.valid = valid
            return valid
        except Exception:
            self.valid = False
            return False

    # ====== HTTP 工具 ======

    def _post(self, path, data=None, use_ajax=True):
        url = LEARN_BASE + path
        headers = AJAX_HEADERS if use_ajax else DEFAULT_HEADERS
        kwargs = {"headers": dict(headers)}
        if data:
            if isinstance(data, dict):
                kwargs["data"] = urlencode(data, encoding='utf-8')
                kwargs["headers"]["Content-Type"] = "application/x-www-form-urlencoded"
            else:
                kwargs["data"] = data
        r = self.session.post(url, **kwargs, timeout=15)
        return _safe_json(r)

    def _get(self, path, params=None, use_ajax=False):
        url = LEARN_BASE + path
        headers = AJAX_HEADERS if use_ajax else dict(DEFAULT_HEADERS)
        if self.xsrf_token:
            headers["X-XSRF-TOKEN"] = self.xsrf_token
        kwargs = {"headers": headers, "params": params}
        r = self.session.get(url, **kwargs, timeout=15)
        return r

    def _get_json(self, path, params=None):
        r = self._get(path, params=params, use_ajax=True)
        return _safe_json(r)

    # ====== 学期 ======

    def get_current_semester(self):
        """返回当前学期 ID 字符串，如 '2025-2026-2'。"""
        d = self._post("/b/kc/zhjw_v_code_xnxq/getCurrentAndNextSemester", use_ajax=True)
        xnxq = d.get('result', {}).get('xnxq', '') if isinstance(d, dict) else ''
        if isinstance(xnxq, list):
            return xnxq[0] if xnxq else ''
        return str(xnxq)

    def get_semesters(self):
        d = self._post("/b/wlxt/kc/v_wlkc_xs_xktjb_coassb/queryxnxq", use_ajax=True)
        return [x for x in d if x is not None] if isinstance(d, list) else []

    # ====== 课程 ======

    def get_courses(self, semester=None):
        if semester is None:
            semester = self.get_current_semester() or self._semester

        courses = []
        try:
            data = self._get_json(
                f"/b/wlxt/kc/v_wlkc_xs_xkb_kcb_extend/student/loadCourseBySemesterId/{semester}/zh_CN",
            )
            for c in data.get('resultList', []):
                c['jslx'] = '3'
                c['kcm_escaped'] = escape_filename(c.get('kcm', ''))
                courses.append(c)
        except Exception:
            pass

        try:
            data2 = self._post(f"/b/kc/v_wlkc_kcb/queryAsorCoCourseList/{semester}/0", use_ajax=True)
            for c in data2.get('resultList', []):
                c['jslx'] = '0'
                c['kcm_escaped'] = escape_filename(c.get('kcm', ''))
                courses.append(c)
        except Exception:
            pass

        return courses

    # ====== 公告 ======

    def get_announcements(self, wlkcid):
        d = self._post(
            "/b/wlxt/kcgg/wlkc_ggb/student/pageListXs",
            {"aoData": [{"name": "wlkcid", "value": wlkcid}]},
            use_ajax=True
        )
        return d.get('object', {}).get('aaData', [])

    def get_announcement_detail(self, wlkcid, ggid):
        """获取公告详细内容。内容从列表 API 中提取（ggnr base64 字段），无需额外请求。"""
        items = self.get_announcements(wlkcid)
        for a in items:
            aid = a.get("ggid") or a.get("id", "")
            if aid == ggid or aid.endswith(ggid):
                title = a.get("bt", "")
                raw = a.get("ggnr", "")
                content = ""
                if raw:
                    try:
                        decoded = base64.b64decode(raw).decode("utf-8")
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(decoded, "html.parser")
                        content = soup.get_text(strip=True)
                    except Exception:
                        content = a.get("ggnrStr", raw)
                return {"title": title, "content": content}
        return {"title": "", "content": ""}

    def mark_announcement_read(self, wlkcid, ggid):
        """标记公告已读。返回 bool。"""
        try:
            r = self.session.get(
                f"{LEARN_BASE}/f/wlxt/kcgg/wlkc_ggb/student/beforeViewXs",
                params={"wlkcid": wlkcid, "id": ggid},
                headers={"Accept": "text/html,*/*"},
                timeout=15
            )
            return r.status_code == 200
        except Exception:
            return False

    def mark_all_announcements_read(self, wlkcid):
        """批量标记所有未读公告为已读。返回 (已标记数, 总数)。"""
        items = self.get_announcements(wlkcid)
        unread = [x for x in items if x.get('sfyd') == '否']
        marked = 0
        for a in unread:
            aid = a.get('ggid') or a.get('id', '')
            if aid and self.mark_announcement_read(wlkcid, aid):
                marked += 1
        return marked, len(unread)

    # ====== 课件文件 ======

    def get_files(self, wlkcid):
        d = self._get_json(
            "/b/wlxt/kj/wlkc_kjxxb/student/kjxxbByWlkcidAndSizeForStudent",
            params={"wlkcid": wlkcid, "size": 0}
        )
        return d.get('object', [])

    def get_file_categories(self, wlkcid, type_='student'):
        d = self._get_json(
            f"/b/wlxt/kj/wlkc_kjflb/{type_}/pageList",
            params={"wlkcid": wlkcid}
        )
        return d.get('object', {}).get('rows', [])

    def download_file(self, wlkcid, wjid, type_='student', filename=None, save_dir=None):
        save_dir = save_dir or DOWNLOAD_DIR
        os.makedirs(save_dir, exist_ok=True)

        url = f"{LEARN_BASE}/b/wlxt/kj/wlkc_kjxxb/{type_}/downloadFile"
        params = {"sfgk": 0, "wjid": wjid}
        headers = dict(DEFAULT_HEADERS)
        if self.xsrf_token:
            headers["X-XSRF-TOKEN"] = self.xsrf_token

        r = self.session.get(url, params=params, headers=headers, stream=True, timeout=30)
        if r.status_code != 200:
            return None

        if filename is None:
            cd = r.headers.get('Content-Disposition', '')
            m = re.search(r'filename[^;]*=([^;]+)', cd)
            if m:
                import urllib.parse
                filename = urllib.parse.unquote(m.group(1).strip().strip('"').strip("'"))
                # 修复：服务器将 UTF-8 字节以 Latin-1 编码发送
                try:
                    fixed = filename.encode('latin-1').decode('utf-8')
                    filename = fixed
                except Exception:
                    pass
            else:
                ext = r.headers.get('Content-Type', '').split('/')[-1] or 'bin'
                filename = f"file_{wjid}.{ext}"

        filename = escape_filename(filename)
        filepath = os.path.join(save_dir, filename)

        try:
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filepath
        except Exception:
            return None

    def mark_file_read(self, wjid):
        """标记单个课件已读。"""
        try:
            r = self.session.post(
                f"{LEARN_BASE}/b/wlxt/kj/wlkc_kjfwb/student/savePlayRecord?_csrf={self.xsrf_token}",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-XSRF-TOKEN": self.xsrf_token,
                    "Referer": f"{LEARN_BASE}/f/wlxt/kj/wlkc_kjxxb/student/beforePageList",
                },
                data=f"wjid={wjid}&sfgk=0", timeout=10
            )
            return r.status_code == 200 and 'success' in r.text
        except Exception:
            return False

    def mark_all_files_read(self, wlkcid):
        """批量标记所有未读课件为已读。返回 (已标记数, 总数)。"""
        files = self.get_files(wlkcid)
        unread = [f for f in files if str(f.get('isNew', '')) == '1']
        marked = 0
        for f in unread:
            wjid = f.get('wjid', '')
            if wjid and self.mark_file_read(wjid):
                marked += 1
        return marked, len(unread)

    # ====== 作业 ======

    def get_homeworks(self, wlkcid):
        hws = []
        data = {"aoData": [{"name": "wlkcid", "value": wlkcid}]}
        for endpoint in ['zyListWj', 'zyListYjwg', 'zyListYpg']:
            try:
                d = self._post(f"/b/wlxt/kczy/zy/student/{endpoint}", data, use_ajax=True)
                hws.extend(d.get('object', {}).get('aaData', []))
            except Exception:
                continue
        return hws

    def get_homework_detail(self, wlkcid, zyid, xszyid='', type_='student'):
        """获取作业详情：标题、说明、截止日期、附件。"""
        r = self._get(
            f"/f/wlxt/kczy/zy/{type_}/viewZy",
            params={"wlkcid": wlkcid, "sfgq": "0", "zyid": zyid, "xszyid": xszyid},
            use_ajax=False
        )
        html = r.text if isinstance(r, requests.Response) else r
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        info = {"title": "", "description": "", "deadline": "", "makeup_deadline": "", "attachments": []}

        for item in soup.find_all('div', class_='list'):
            left = item.find('div', class_='left')
            right = item.find('div', class_='right')
            if not left or not right:
                continue
            key = left.get_text(strip=True)
            val = right.get_text(strip=True)
            if '标题' in key:
                info['title'] = val
            elif '说明' in key:
                info['description'] = val
            elif '截止' in key:
                info['deadline'] = val
            elif '补交' in key:
                info['makeup_deadline'] = val

        for fj in soup.find_all('div', class_='fujian'):
            left = fj.find('div', class_='left')
            links = fj.find_all('a')
            if left and links:
                key = left.get_text(strip=True)
                for link in links:
                    href = link.get('href', '')
                    name = link.get_text(strip=True)
                    if href and name and '作业' in key:
                        info['attachments'].append({'name': name, 'href': href})
        return info

    def get_homework_full_detail(self, wlkcid, zyid, xszyid='', type_='student'):
        """
        获取作业完整信息：含老师评语、得分、批改状态、提交状态。
        先试 API 解析 HTML，信息不足时返回 raw HTML 供外部解析。
        """
        r = self._get(
            f"/f/wlxt/kczy/zy/{type_}/viewZy",
            params={"wlkcid": wlkcid, "sfgq": "0", "zyid": zyid, "xszyid": xszyid},
            use_ajax=False
        )
        html = r.text if isinstance(r, requests.Response) else r
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        info = {
            "title": "", "description": "", "deadline": "", "makeup_deadline": "",
            "status": "", "score": "", "comment": "",
            "attachments": [], "raw_html_len": len(html),
        }

        for item in soup.find_all('div', class_='list'):
            left = item.find('div', class_='left')
            right = item.find('div', class_='right')
            if not left or not right:
                continue
            key = left.get_text(strip=True)
            val = right.get_text(strip=True)
            if '标题' in key:
                info['title'] = val
            elif '说明' in key:
                info['description'] = val
            elif '截止' in key:
                info['deadline'] = val
            elif '补交' in key:
                info['makeup_deadline'] = val
            elif '批语' in key or '评语' in key:
                info['comment'] = val
            elif '得分' in key:
                info['score'] = val
            elif '状态' in key or '批改' in key:
                info['status'] = val

        for fj in soup.find_all('div', class_='fujian'):
            left = fj.find('div', class_='left')
            links = fj.find_all('a')
            if left and links:
                for link in links:
                    href = link.get('href', '')
                    name = link.get_text(strip=True)
                    if href and name:
                        info['attachments'].append({'name': name, 'href': href})

        if not info['status']:
            page_text = soup.get_text()
            if '已批改' in page_text:
                info['status'] = '已批改'
            elif '已提交' in page_text:
                info['status'] = '已提交'
            elif '未提交' in page_text or '未交' in page_text:
                info['status'] = '未交'

        return info

    # ====== 讨论 ======

    def get_discussions(self, wlkcid, type_='student'):
        d = self._get_json(
            f"/b/wlxt/bbs/bbs_tltb/{type_}/kctlList",
            params={"wlkcid": wlkcid}
        )
        return d.get('object', {}).get('resultsList', [])

    def get_discussion_detail(self, wlkcid, id_, bqid, type_='student'):
        r = self._get(
            f"/f/wlxt/bbs/bbs_tltb/{type_}/viewTlById",
            params={"wlkcid": wlkcid, "id": id_, "tabbh": "2", "bqid": bqid},
            use_ajax=False
        )
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        detail = soup.find('div', class_='detail')
        return detail.get_text(strip=True) if detail else ""

    # ====== 问卷 ======

    def get_questionnaires(self, wlkcid):
        """获取课程问卷列表（未做）。"""
        d = self._get_json(
            f"/b/wlxt/kcwj/wlkc_wjb/student/pageListWks",
            params={"wlkcid": wlkcid, "size": 20}
        )
        return _get_items(d)

    def get_all_unanswered_questionnaires(self):
        """获取所有未做问卷（全局）。"""
        try:
            body = "aoData=%5B%7B%22name%22%3A%22iDisplayStart%22%2C%22value%22%3A0%7D%2C%7B%22name%22%3A%22iDisplayLength%22%2C%22value%22%3A100%7D%5D"
            r = self.session.post(
                f"{LEARN_BASE}/b/wlxt/kcwj/wlkc_wjb/student/pageListWks?_csrf={self.xsrf_token}",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-XSRF-TOKEN": self.xsrf_token,
                    "Accept": "application/json, */*",
                }, data=body, timeout=15
            )
            d = _safe_json(r)
            return _get_items(d)
        except Exception:
            return []

    # ====== 聚合查询 ======

    def get_course_detail(self, wlkcid):
        """获取课程所有信息的一站式聚合。"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        result = {}

        def fetch_announcements():
            try:
                items = self.get_announcements(wlkcid)
                return [{
                    "id": x.get("id", x.get("ggid", "")),
                    "title": x.get("bt", ""),
                    "time": x.get("fbsjStr", x.get("cjsjStr", "")),
                    "unread": x.get("sfyd") == "否",
                } for x in items]
            except Exception:
                return []

        def fetch_files():
            try:
                items = self.get_files(wlkcid)
                return [{
                    "id": x.get("wjid", ""),
                    "title": x.get("bt", ""),
                    "type": x.get("wjlx", ""),
                    "time": x.get("fssjStr", x.get("cjsjStr", "")),
                    "is_new": str(x.get("isNew", "")) == "1",
                } for x in items]
            except Exception:
                return []

        def fetch_homeworks():
            try:
                items = self.get_homeworks(wlkcid)
                return [{
                    "zyid": x.get("zyid", ""),
                    "xszyid": x.get("xszyid", ""),
                    "title": x.get("bt", ""),
                    "deadline": x.get("jzsjStr", x.get("scsjStr", "")),
                    "status": x.get("zt", ""),
                } for x in items]
            except Exception:
                return []

        def fetch_discussions():
            try:
                items = self.get_discussions(wlkcid)
                return [{
                    "id": x.get("id", ""),
                    "title": x.get("bt", ""),
                    "author": x.get("fbrxm", ""),
                    "replies": x.get("htsl", 0),
                    "time": x.get("fbsjStr", ""),
                } for x in items]
            except Exception:
                return []

        def fetch_questionnaires():
            try:
                items = self.get_questionnaires(wlkcid)
                return [{
                    "id": x.get("wjid", ""),
                    "title": x.get("bt", ""),
                    "deadline": x.get("jzsjStr", ""),
                } for x in items]
            except Exception:
                return []

        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = {
                ex.submit(fetch_announcements): "announcements",
                ex.submit(fetch_files): "files",
                ex.submit(fetch_homeworks): "homeworks",
                ex.submit(fetch_discussions): "discussions",
                ex.submit(fetch_questionnaires): "questionnaires",
            }
            for f in as_completed(futures):
                result[futures[f]] = f.result()

        return result

    # ====== 提交作业 ======

    def submit_homework(self, wlkcid, xszyid, file_path, content=""):
        """提交作业。使用 tjzy 端点提交文件 + 可选文字内容。返回 bool。"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return False

        basename = os.path.basename(file_path)
        tjzy_url = f"{LEARN_BASE}/b/wlxt/kczy/zy/student/tjzy?_csrf={self.xsrf_token}"

        with open(file_path, 'rb') as f:
            r = self.session.post(
                tjzy_url,
                data={"xszyid": xszyid, "isDeleted": "0", "zynr": content},
                files={"fileupload": (basename, f, "application/pdf")},
                headers={"X-XSRF-TOKEN": self.xsrf_token, "Referer": f"{LEARN_BASE}/f/wlxt/kczy/zy/student/tijiao?wlkcid={wlkcid}&xszyid={xszyid}"},
                timeout=30
            )
        try:
            data = r.json()
            return data.get('result') == 'success'
        except Exception:
            return False


# ====== CLI ======
if __name__ == '__main__':
    import argparse, pprint

    parser = argparse.ArgumentParser(description='清华网络学堂 API')
    parser.add_argument('--session', default=SESSION_FILE)
    parser.add_argument('--semester', default=None)
    parser.add_argument('--course', default=None, help='课名（部分匹配）')
    parser.add_argument('--action', default='courses',
                        choices=['courses', 'announcements', 'announcement-detail',
                                 'files', 'file-download',
                                 'homeworks', 'homework-detail', 'homework-full',
                                 'discussions', 'aggregated', 'questionnaires',
                                 'mark-announcement-read', 'mark-all-announcements-read',
                                 'mark-file-read', 'mark-all-files-read'])
    parser.add_argument('--id', default=None, help='条目 ID（ggid/zyid/wjid）')
    parser.add_argument('--xszyid', default=None, help='学生作业 ID')
    parser.add_argument('--out', default=None, help='输出文件路径')
    args = parser.parse_args()

    api = LearnAPI(session_file=args.session)
    if not api.reload_session():
        print("Session 无效，请先运行 login_manager.py")
        exit(1)

    courses = api.get_courses(semester=args.semester)
    if args.course:
        courses = [c for c in courses if args.course in c.get('kcm', '')]

    if args.action == 'courses':
        for c in courses:
            print(f"[{c.get('jslx')}] {c.get('kcm')} | {c.get('jsm')} | wlkcid={c.get('wlkcid')}")

    elif args.action == 'announcements':
        for c in courses:
            items = api.get_announcements(c['wlkcid'])
            print(f"\n=== {c['kcm']} 公告 ===")
            for a in items:
                print(f"  [{'未读' if a.get('sfyd')=='否' else '已读'}] {a.get('fbsjStr','')} {a.get('bt','')}")

    elif args.action == 'announcement-detail':
        for c in courses:
            items = api.get_announcements(c['wlkcid'])
            for a in items:
                aid = a.get('id', a.get('ggid', ''))
                if args.id and args.id != aid:
                    continue
                detail = api.get_announcement_detail(c['wlkcid'], aid)
                print(f"标题: {detail['title']}")
                print(f"内容: {detail['content'][:2000]}")
                print()

    elif args.action == 'files':
        for c in courses:
            items = api.get_files(c['wlkcid'])
            print(f"\n=== {c['kcm']} 课件 ===")
            for f in items:
                print(f"  [{'新' if str(f.get('isNew',''))=='1' else '旧'}] {f.get('bt','?')}.{f.get('wjlx','?')} | wjid={f.get('wjid','?')}")

    elif args.action == 'file-download':
        for c in courses:
            items = api.get_files(c['wlkcid'])
            target = [f for f in items if f.get('wjid') == args.id] if args.id else items[:1]
            for f in target:
                path = api.download_file(c['wlkcid'], f['wjid'], filename=args.out)
                print(f"下载到: {path}" if path else "下载失败")

    elif args.action == 'homeworks':
        for c in courses:
            items = api.get_homeworks(c['wlkcid'])
            print(f"\n=== {c['kcm']} 作业 ===")
            for h in items:
                print(f"  [{h.get('zt','?')}] {h.get('bt','?')} | 截止:{h.get('scsjStr','?')} | zyid={h.get('zyid','?')}")

    elif args.action == 'homework-detail' or args.action == 'homework-full':
        for c in courses:
            items = api.get_homeworks(c['wlkcid'])
            for h in items:
                if args.id and args.id != h.get('zyid', ''):
                    continue
                detail = api.get_homework_full_detail(c['wlkcid'], h['zyid'], h.get('xszyid', ''))
                print(f"\n=== {h.get('bt','?')} ===")
                for k, v in detail.items():
                    if k != 'raw_html_len':
                        print(f"  {k}: {v}")

    elif args.action == 'discussions':
        for c in courses:
            items = api.get_discussions(c['wlkcid'])
            print(f"\n=== {c['kcm']} 讨论 ===")
            for d in items:
                print(f"  [{d.get('htsl',0)}回复] {d.get('bt','?')} by {d.get('fbrxm','?')}")

    elif args.action == 'aggregated':
        for c in courses:
            detail = api.get_course_detail(c['wlkcid'])
            print(f"\n=== {c['kcm']} 汇总 ===")
            for cat, items in detail.items():
                print(f"  {cat}: {len(items)} 项")
                if items:
                    print(f"    最新: {items[0].get('title','')[:50]}{'...' if len(items[0].get('title',''))>50 else ''}")

    elif args.action == 'questionnaires':
        for c in courses:
            items = api.get_questionnaires(c['wlkcid'])
            print(f"\n=== {c['kcm']} 问卷 ===")
            for q in items:
                print(f"  {q.get('bt','?')} | 截止:{q.get('jzsjStr','?')}")

    elif args.action == 'mark-announcement-read':
        for c in courses:
            items = api.get_announcements(c['wlkcid'])
            for a in items:
                aid = a.get('id', a.get('ggid', ''))
                if args.id and args.id != aid:
                    continue
                ok = api.mark_announcement_read(c['wlkcid'], aid)
                print(f"  {'✅' if ok else '❌'} {a.get('bt','?')}")

    elif args.action == 'mark-all-announcements-read':
        for c in courses:
            marked, total = api.mark_all_announcements_read(c['wlkcid'])
            print(f"  {c['kcm']}: 标记 {marked}/{total} 项已读")

    elif args.action == 'mark-file-read':
        if args.id:
            ok = api.mark_file_read(args.id)
            print(f"{'✅' if ok else '❌'} 标记已读")

    elif args.action == 'mark-all-files-read':
        for c in courses:
            marked, total = api.mark_all_files_read(c['wlkcid'])
            print(f"  {c['kcm']}: 标记 {marked}/{total} 项已读")
