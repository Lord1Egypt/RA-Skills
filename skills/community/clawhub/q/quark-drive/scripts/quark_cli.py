#!/usr/bin/env python3
"""
夸克网盘 CLI 工具
支持：扫码登录、文件列表、搜索、上传、下载、删除、清空
"""

import argparse
import json
import os
import sys
import time
import uuid
import hashlib
import re
import mimetypes
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode

try:
    import httpx
except ImportError:
    print("请安装 httpx: pip install httpx")
    sys.exit(1)

# ============================================================
# 常量定义
# ============================================================

PAN_DOMAIN = "https://pan.quark.cn"
DRIVE_DOMAIN = "https://drive-pc.quark.cn"
DRIVE_H_DOMAIN = "https://drive-h.quark.cn"
UOP_DOMAIN = "https://uop.quark.cn"

# API 端点
API_ENDPOINTS = {
    # 用户信息
    "user_info": "/account/info",
    "member_info": "/1/clouddrive/member",
    
    # 扫码登录
    "qr_token": "/cas/ajax/getTokenForQrcodeLogin",
    "qr_check": "/cas/ajax/getServiceTicketByQrcodeToken",
    
    # 文件操作
    "file_sort": "/1/clouddrive/file/sort",
    "file_create": "/1/clouddrive/file",
    "file_delete": "/1/clouddrive/file/delete",
    "file_move": "/1/clouddrive/file/move",
    "file_copy": "/1/clouddrive/file/copy",
    "file_rename": "/1/clouddrive/file/rename",
    "file_search": "/1/clouddrive/file/search",
    
    # 文件上传
    "upload_pre": "/1/clouddrive/file/upload/pre",
    "upload_hash": "/1/clouddrive/file/update/hash",
    "upload_auth": "/1/clouddrive/file/upload/auth",
    "upload_finish": "/1/clouddrive/file/upload/finish",
    
    # 文件下载
    "download": "/1/clouddrive/file/download",
    
    # 分享操作
    "share": "/1/clouddrive/share",
    "share_password": "/1/clouddrive/share/password",
    "share_list": "/1/clouddrive/share/list",
}

# ============================================================
# Cookie 配置管理
# ============================================================

class CookieManager:
    """Cookie 管理器"""
    
    CONFIG_DIR = Path.home() / ".hermes" / "skills" / "cloud-drive" / "quark"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    @classmethod
    def get_cookie(cls) -> Optional[str]:
        """获取 Cookie，优先级：环境变量 > 配置文件"""
        # 1. 环境变量
        cookie = os.environ.get("QUARK_COOKIE")
        if cookie:
            return cookie
        
        # 2. 配置文件
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get("cookie")
            except:
                pass
        
        return None
    
    @classmethod
    def save_cookie(cls, cookie: str) -> None:
        """保存 Cookie 到配置文件"""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        config = {}
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            except:
                pass
        
        config["cookie"] = cookie
        config["updated_at"] = int(time.time())
        
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def clear_cookie(cls) -> None:
        """清除 Cookie"""
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                config.pop("cookie", None)
                with open(cls.CONFIG_FILE, 'w') as f:
                    json.dump(config, f, indent=2)
            except:
                pass

# ============================================================
# 夸克网盘客户端
# ============================================================

class QuarkClient:
    """夸克网盘客户端"""
    
    def __init__(self, cookie: Optional[str] = None):
        self.cookie = cookie or CookieManager.get_cookie()
        if not self.cookie:
            raise ValueError("未配置 Cookie，请先运行 login 命令或设置 QUARK_COOKIE 环境变量")
        
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (iPod; U; CPU iPhone OS 3_3 like Mac OS X) AppleWebKit/534.37.3",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/json",
                "Origin": "https://pan.quark.cn",
                "Referer": "https://pan.quark.cn/",
            }
        )
        self._set_cookies()
    
    def _set_cookies(self):
        """设置 Cookie"""
        for part in self.cookie.split(";"):
            part = part.strip()
            if "=" in part:
                name, value = part.split("=", 1)
                self.client.cookies.set(name.strip(), value.strip(), domain=".quark.cn")
    
    def _get_full_url(self, domain: str, path: str, params: Optional[Dict] = None) -> str:
        """构造完整 URL"""
        url = f"{domain}{path}"
        # 总是添加公共参数
        default_params = {
            "pr": "ucpro",
            "fr": "pc",
            "uc_param_str": "",
        }
        if params:
            default_params.update(params)
        return url, default_params
    
    def _request(self, method: str, domain: str, path: str, 
                 params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict:
        """发送请求"""
        url, params = self._get_full_url(domain, path, params)
        
        try:
            if method.upper() == "GET":
                response = self.client.get(url, params=params)
            elif method.upper() == "POST":
                response = self.client.post(url, params=params, json=json_data)
            else:
                raise ValueError(f"不支持的请求方法: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP 错误: {e.response.status_code}")
            raise
        except Exception as e:
            print(f"请求失败: {e}")
            raise
    
    # --------------------------------------------------------
    # 用户信息
    # --------------------------------------------------------
    
    def get_user_info(self) -> Dict:
        """获取用户信息"""
        return self._request("GET", PAN_DOMAIN, API_ENDPOINTS["user_info"])
    
    def get_member_info(self) -> Dict:
        """获取会员信息"""
        return self._request("GET", DRIVE_DOMAIN, API_ENDPOINTS["member_info"])
    
    # --------------------------------------------------------
    # 文件操作
    # --------------------------------------------------------
    
    def list_files(self, folder_id: str = "0", page: int = 1, size: int = 50, 
                   sort: str = "file_name:asc") -> Dict:
        """列出文件"""
        params = {
            "pdir_fid": folder_id,
            "_page": str(page),
            "_size": str(size),
            "_sort": sort,
            "_fetch_total": "1",
        }
        return self._request("GET", DRIVE_DOMAIN, API_ENDPOINTS["file_sort"], params)
    
    def search_files(self, keyword: str, page: int = 1, size: int = 50) -> Dict:
        """搜索文件"""
        params = {
            "q": keyword,
            "_page": str(page),
            "_size": str(size),
            "_fetch_total": "1",
            "_sort": "file_name:asc",
            "_is_hl": "1",
        }
        return self._request("GET", DRIVE_DOMAIN, API_ENDPOINTS["file_search"], params)
    
    def create_folder(self, folder_name: str, parent_id: str = "0") -> Dict:
        """创建文件夹"""
        json_data = {
            "dir_init_lock": False,
            "dir_path": "",
            "file_name": folder_name,
            "pdir_fid": parent_id,
        }
        return self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["file_create"], json_data=json_data)
    
    def delete_files(self, file_ids: List[str], action_type: int = 2) -> Dict:
        """删除文件"""
        json_data = {
            "action_type": action_type,
            "filelist": file_ids,
            "exclude_fids": [],
        }
        return self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["file_delete"], json_data=json_data)
    
    def move_files(self, file_ids: List[str], target_folder_id: str) -> Dict:
        """移动文件"""
        json_data = {
            "action_type": 1,
            "to_pdir_fid": target_folder_id,
            "filelist": file_ids,
            "exclude_fids": [],
        }
        return self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["file_move"], json_data=json_data)
    
    def copy_files(self, file_ids: List[str], target_folder_id: str) -> Dict:
        """复制文件"""
        json_data = {
            "action_type": 1,
            "to_pdir_fid": target_folder_id,
            "filelist": file_ids,
            "exclude_fids": [],
        }
        return self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["file_copy"], json_data=json_data)
    
    def rename_file(self, file_id: str, new_name: str) -> Dict:
        """重命名文件"""
        json_data = {
            "fid": file_id,
            "file_name": new_name,
        }
        return self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["file_rename"], json_data=json_data)
    
    # --------------------------------------------------------
    # 文件上传
    # --------------------------------------------------------
    
    def upload_file(self, local_path: str, remote_path: str) -> Dict:
        """上传文件"""
        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"文件不存在: {local_path}")
        
        file_size = local_path.stat().st_size
        file_name = local_path.name
        
        # 解析远程路径
        remote_dir = str(Path(remote_path).parent)
        remote_name = Path(remote_path).name
        
        # 获取目标文件夹 ID
        target_fid = self._resolve_path(remote_dir)
        
        # 1. 上传预请求
        md5_str, sha1_str = self._calculate_md5(local_path), self._calculate_sha1(local_path)
        now_ms = int(time.time() * 1000)
        mime_type = mimetypes.guess_type(str(local_path))[0] or "application/octet-stream"
        pre_data = {
            "ccp_hash_update": True,
            "dir_name": "",
            "file_name": remote_name,
            "format_type": mime_type,
            "l_created_at": now_ms,
            "l_updated_at": now_ms,
            "pdir_fid": target_fid,
            "size": file_size,
        }
        pre_result = self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["upload_pre"], json_data=pre_data)
        
        if pre_result.get("status") != 200:
            raise Exception(f"上传预请求失败: {pre_result}")
        
        # 2. 更新哈希
        hash_result = self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["upload_hash"],
            json_data={"md5": md5_str, "sha1": sha1_str, "task_id": pre_result["data"]["task_id"]})
        if hash_result.get("data", {}).get("finish"):
            print("文件已存在（秒传）")
            return hash_result
        
        # 3. 上传文件到 COS
        upload_info = pre_result["data"]
        upload_info["metadata"] = pre_result.get("metadata", {})
        self._upload_to_cos(local_path, upload_info)
        
        return {"status": 200, "message": "上传成功"}
    
    def _calculate_md5(self, file_path: Path) -> str:
        """计算文件 MD5"""
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def _calculate_sha1(self, file_path: Path) -> str:
        """计算文件 SHA1"""
        sha1 = hashlib.sha1()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha1.update(chunk)
        return sha1.hexdigest()
    
    def _upload_to_cos(self, local_path: Path, upload_info: Dict) -> None:
        """上传文件到 COS（阿里云 PDS 分片上传）"""
        import math
        from datetime import datetime, timezone

        file_size = local_path.stat().st_size
        mime_type = mimetypes.guess_type(str(local_path))[0] or "application/octet-stream"
        bucket = upload_info["bucket"]
        obj_key = upload_info["obj_key"]
        upload_id = upload_info["upload_id"]
        auth_info = upload_info["auth_info"]
        callback = upload_info["callback"]
        task_id = upload_info["task_id"]
        part_size = upload_info.get("metadata", {}).get("part_size", 4194304)

        base = upload_info["upload_url"].replace("http://", "").replace("https://", "")
        oss_base = f"https://{bucket}.{base}/{obj_key}"
        total_parts = math.ceil(file_size / part_size)

        etag_list = []
        with open(local_path, "rb") as f:
            for pn in range(1, total_parts + 1):
                part_data = f.read(part_size)
                ts = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
                meta_str = f"PUT\n\n{mime_type}\n{ts}\nx-oss-date:{ts}\nx-oss-user-agent:aliyun-sdk-js/6.6.1\n/{bucket}/{obj_key}?partNumber={pn}&uploadId={upload_id}"

                a_resp = self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["upload_auth"],
                    json_data={"auth_info": auth_info, "auth_meta": meta_str, "task_id": task_id})
                ak = a_resp["data"]["auth_key"]

                url = f"{oss_base}?partNumber={pn}&uploadId={upload_id}"
                r = httpx.put(url, content=part_data, headers={
                    "Authorization": ak, "Content-Type": mime_type,
                    "Referer": "https://pan.quark.cn/",
                    "x-oss-date": ts,
                    "x-oss-user-agent": "aliyun-sdk-js/6.6.1",
                }, timeout=120)
                r.raise_for_status()
                etag_list.append(r.headers.get("ETag", "").strip('"'))
                print(f"  ✅ Part {pn}/{total_parts} ({pn*100//total_parts}%)")

        # Commit
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<CompleteMultipartUpload>\n'
        for i, e in enumerate(etag_list, 1):
            xml += f'<Part><PartNumber>{i}</PartNumber><ETag>{e}</ETag></Part>\n'
        xml += '</CompleteMultipartUpload>'

        cmd5 = base64.b64encode(hashlib.md5(xml.encode()).digest()).decode()
        cb64 = base64.b64encode(json.dumps(callback).encode()).decode()
        cts = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        cmeta = f"POST\n{cmd5}\napplication/xml\n{cts}\nx-oss-callback:{cb64}\nx-oss-date:{cts}\nx-oss-user-agent:aliyun-sdk-js/6.6.1\n/{bucket}/{obj_key}?uploadId={upload_id}"

        ca = self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["upload_auth"],
            json_data={"auth_info": auth_info, "auth_meta": cmeta, "task_id": task_id})
        cak = ca["data"]["auth_key"]

        r = httpx.post(f"{oss_base}?uploadId={upload_id}", content=xml.encode(), headers={
            "Authorization": cak, "Content-MD5": cmd5, "Content-Type": "application/xml",
            "Referer": "https://pan.quark.cn/", "x-oss-callback": cb64,
            "x-oss-date": cts, "x-oss-user-agent": "aliyun-sdk-js/6.6.1",
        }, timeout=60)
        r.raise_for_status()
    
    def _resolve_path(self, path: str) -> str:
        """解析路径到文件夹 ID"""
        if path == "/" or path == "":
            return "0"
        
        # 逐级解析
        parts = [p for p in path.split("/") if p]
        current_id = "0"
        
        for part in parts:
            result = self.list_files(current_id, size=100)
            found = False
            
            for item in result.get("data", {}).get("list", []):
                if item.get("file_name") == part and item.get("file_type") == 0:  # 0 = 文件夹
                    current_id = item["fid"]
                    found = True
                    break
            
            if not found:
                raise FileNotFoundError(f"路径不存在: {path}")
        
        return current_id
    
    # --------------------------------------------------------
    # 文件下载
    # --------------------------------------------------------
    
    def get_download_url(self, file_id: str) -> str:
        """获取下载链接"""
        json_data = {"fids": [file_id]}
        result = self._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["download"], json_data=json_data)
        
        if result.get("status") != 200:
            raise Exception(f"获取下载链接失败: {result}")
        
        return result["data"][0]["download_url"]
    
    def download_file(self, file_id: str, save_path: str) -> str:
        """下载文件"""
        url = self.get_download_url(file_id)
        
        response = self.client.get(url, follow_redirects=True)
        response.raise_for_status()
        
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        return save_path

# ============================================================
# 扫码登录
# ============================================================

class QRLogin:
    """扫码登录"""
    
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
        )
    
    def get_qr_token(self) -> tuple:
        """获取二维码 token"""
        request_id = str(uuid.uuid4())
        
        params = {
            "client_id": "532",
            "v": "1.2",
            "request_id": request_id,
        }
        
        response = self.client.get(f"{UOP_DOMAIN}/cas/ajax/getTokenForQrcodeLogin", params=params)
        data = response.json()
        
        if data.get("status") != 2000000:
            raise Exception(f"获取二维码失败: {data}")
        
        token = data["data"]["members"]["token"]
        qr_url = self._build_qr_url(token)
        
        return token, qr_url
    
    def _build_qr_url(self, token: str) -> str:
        """构造二维码 URL"""
        base_url = "https://su.quark.cn/4_eMHBJ"
        params = {
            "token": token,
            "client_id": "532",
            "ssb": "weblogin",
            "uc_param_str": "",
            "uc_biz_str": "S:custom|OPT:SAREA@0|OPT:IMMERSIVE@1|OPT:BACK_BTN_STYLE@0",
        }
        return f"{base_url}?{urlencode(params)}"
    
    def check_login_status(self, qr_token: str) -> Optional[Dict]:
        """检查登录状态"""
        request_id = str(uuid.uuid4())
        
        params = {
            "client_id": "532",
            "v": "1.2",
            "token": qr_token,
            "request_id": request_id,
        }
        
        response = self.client.get(f"{UOP_DOMAIN}/cas/ajax/getServiceTicketByQrcodeToken", params=params)
        data = response.json()
        
        # 检查是否登录成功
        if (data.get("status") == 2000000 and 
            data.get("message") == "ok" and
            data.get("data", {}).get("members", {}).get("service_ticket")):
            return data
        
        return None
    
    def wait_for_login(self, qr_token: str) -> bool:
        """等待用户扫码登录"""
        start_time = time.time()
        check_count = 0
        
        print("\n" + "="*50)
        print("请使用夸克 APP 扫描上方二维码登录")
        print("="*50)
        print(f"等待扫码中... (超时时间: {self.timeout}秒)")
        print("按 Ctrl+C 取消\n")
        
        try:
            while time.time() - start_time < self.timeout:
                check_count += 1
                elapsed = int(time.time() - start_time)
                remaining = self.timeout - elapsed
                
                # 显示进度
                minutes = remaining // 60
                seconds = remaining % 60
                sys.stdout.write(f"\r⏰ 剩余时间: {minutes:02d}:{seconds:02d} | 检查次数: {check_count}")
                sys.stdout.flush()
                
                result = self.check_login_status(qr_token)
                
                if result:
                    print("\n\n✅ 登录成功！")
                    
                    # 获取 service ticket
                    service_ticket = result["data"]["members"]["service_ticket"]
                    
                    # 使用 service ticket 获取 cookie
                    cookie = self._get_cookie_by_ticket(service_ticket)
                    return cookie
                
                time.sleep(2)
            
            print("\n\n❌ 登录超时，请重新尝试")
            return None
            
        except KeyboardInterrupt:
            print("\n\n❌ 已取消登录")
            return None
    
    def _get_cookie_by_ticket(self, service_ticket: str) -> str:
        """使用 service ticket 获取 Cookie"""
        # 访问用户信息 API 获取 cookie
        response = self.client.get(
            f"{PAN_DOMAIN}/account/info",
            params={"st": service_ticket, "lw": "scan"}
        )
        
        # 提取 cookie
        cookies = []
        for cookie in self.client.cookies.jar:
            if cookie.domain and "quark.cn" in cookie.domain:
                cookies.append(f"{cookie.name}={cookie.value}")
        
        return "; ".join(cookies)
    
    def login(self) -> Optional[str]:
        """执行扫码登录"""
        print("\n🚀 夸克网盘扫码登录")
        print("="*50)
        
        try:
            # 1. 获取二维码
            print("正在获取二维码...")
            qr_token, qr_url = self.get_qr_token()
            
            # 2. 显示二维码
            print(f"\n二维码链接: {qr_url}\n")
            
            # 尝试显示 ASCII 二维码
            try:
                import qrcode
                qr = qrcode.QRCode(version=1, box_size=1, border=1)
                qr.add_data(qr_url)
                qr.make(fit=True)
                qr.print_ascii(invert=True)
            except ImportError:
                print("提示: 安装 qrcode 库可显示 ASCII 二维码: pip install qrcode[pil]")
            
            # 3. 等待扫码
            cookie = self.wait_for_login(qr_token)
            
            if cookie:
                # 保存 cookie
                CookieManager.save_cookie(cookie)
                print("\n✅ Cookie 已保存")
            
            return cookie
            
        except Exception as e:
            print(f"\n❌ 登录失败: {e}")
            return None

# ============================================================
# CLI 命令
# ============================================================

def cmd_login(args):
    """登录命令"""
    login = QRLogin(timeout=args.timeout)
    cookie = login.login()
    if cookie:
        print("\n登录成功！可以开始使用夸克网盘了。")
    else:
        print("\n登录失败，请重试。")

def cmd_user(args):
    """用户信息命令"""
    try:
        client = QuarkClient()
        result = client.get_user_info()
        
        if result.get("status") == 200:
            data = result["data"]
            print("\n" + "="*50)
            print("👤 用户信息")
            print("="*50)
            print(f"昵称: {data.get('nickname', 'N/A')}")
            print(f"用户ID: {data.get('uid', 'N/A')}")
            
            # 会员信息
            try:
                member = client.get_member_info()
                if member.get("status") == 200:
                    member_data = member["data"]
                    total = member_data.get("total_capacity", 0)
                    used = member_data.get("use_capacity", 0)
                    free = total - used
                    
                    print(f"会员类型: {member_data.get('member_type', 'N/A')}")
                    print(f"总容量: {total / (1024**3):.2f} GB")
                    print(f"已使用: {used / (1024**3):.2f} GB")
                    print(f"剩余: {free / (1024**3):.2f} GB")
            except:
                pass
            
            print("="*50)
        else:
            print(f"获取用户信息失败: {result}")
    except Exception as e:
        print(f"错误: {e}")
        print("请先运行 login 命令登录")

def cmd_list(args):
    """列出文件命令"""
    try:
        client = QuarkClient()
        
        # 解析路径
        path = args.path.strip("/")
        if not path:
            folder_id = "0"
        else:
            folder_id = client._resolve_path(path)
        
        result = client.list_files(
            folder_id=folder_id,
            page=args.page,
            size=args.size
        )
        
        if result.get("status") == 200:
            data = result["data"]
            files = data.get("list", [])
            total = data.get("total", 0)
            
            print("\n" + "="*60)
            print(f"📂 目录: /{path}")
            print(f"📊 共 {total} 个项目")
            print("="*60)
            
            if not files:
                print("  (空目录)")
            else:
                for item in files:
                    file_type = "📁" if item.get("file_type") == 0 else "📄"
                    name = item.get("file_name", "N/A")
                    size = item.get("size", 0)
                    
                    if item.get("file_type") == 0:
                        print(f"  {file_type} {name}/")
                    else:
                        size_str = _format_size(size)
                        print(f"  {file_type} {name} ({size_str})")
            
            print("="*60)
        else:
            print(f"获取文件列表失败: {result}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_search(args):
    """搜索文件命令"""
    try:
        client = QuarkClient()
        
        result = client.search_files(
            keyword=args.keyword,
            page=args.page,
            size=args.size
        )
        
        if result.get("status") == 200:
            data = result["data"]
            files = data.get("list", [])
            total = data.get("total", 0)
            
            print("\n" + "="*60)
            print(f"🔍 搜索: {args.keyword}")
            print(f"📊 找到 {total} 个结果")
            print("="*60)
            
            if not files:
                print("  (无结果)")
            else:
                for item in files:
                    file_type = "📁" if item.get("file_type") == 0 else "📄"
                    name = item.get("file_name", "N/A")
                    size = item.get("size", 0)
                    
                    if item.get("file_type") == 0:
                        print(f"  {file_type} {name}/")
                    else:
                        size_str = _format_size(size)
                        print(f"  {file_type} {name} ({size_str})")
            
            print("="*60)
        else:
            print(f"搜索失败: {result}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_upload(args):
    """上传文件命令"""
    try:
        client = QuarkClient()
        
        local_path = args.local_path
        remote_path = args.remote_path
        
        if not os.path.exists(local_path):
            print(f"❌ 本地文件不存在: {local_path}")
            return
        
        print(f"\n📤 上传文件: {local_path}")
        print(f"   目标路径: {remote_path}")
        print("上传中...")
        
        result = client.upload_file(local_path, remote_path)
        
        if result.get("status") == 200:
            print("✅ 上传成功！")
        else:
            print(f"❌ 上传失败: {result}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_download(args):
    """下载文件命令"""
    try:
        client = QuarkClient()
        
        remote_path = args.remote_path.strip("/")
        local_path = args.local_path
        
        # 解析远程路径
        parts = remote_path.split("/")
        file_name = parts[-1]
        folder_path = "/".join(parts[:-1])
        
        if folder_path:
            folder_id = client._resolve_path(folder_path)
        else:
            folder_id = "0"
        
        # 搜索文件
        result = client.list_files(folder_id=folder_id, size=100)
        file_id = None
        
        for item in result.get("data", {}).get("list", []):
            if item.get("file_name") == file_name:
                file_id = item["fid"]
                break
        
        if not file_id:
            print(f"❌ 文件不存在: {remote_path}")
            return
        
        print(f"\n📥 下载文件: {remote_path}")
        print(f"   保存到: {local_path}")
        print("下载中...")
        
        client.download_file(file_id, local_path)
        
        print("✅ 下载成功！")
    except Exception as e:
        print(f"错误: {e}")

def cmd_delete(args):
    """删除文件命令"""
    try:
        client = QuarkClient()
        
        path = args.path.strip("/")
        if not path:
            print("❌ 请指定要删除的文件路径")
            return
        
        # 解析路径
        parts = path.split("/")
        file_name = parts[-1]
        folder_path = "/".join(parts[:-1])
        
        if folder_path:
            folder_id = client._resolve_path(folder_path)
        else:
            folder_id = "0"
        
        # 搜索文件
        result = client.list_files(folder_id=folder_id, size=100)
        file_id = None
        
        for item in result.get("data", {}).get("list", []):
            if item.get("file_name") == file_name:
                file_id = item["fid"]
                break
        
        if not file_id:
            print(f"❌ 文件不存在: {path}")
            return
        
        # 确认删除
        if not args.yes:
            confirm = input(f"确定要删除 {path} 吗？(y/N): ")
            if confirm.lower() != "y":
                print("已取消")
                return
        
        print(f"\n🗑️  删除文件: {path}")
        
        result = client.delete_files([file_id])
        
        if result.get("status") == 200:
            print("✅ 删除成功！")
        else:
            print(f"❌ 删除失败: {result}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_clear(args):
    """清空目录命令"""
    try:
        client = QuarkClient()
        
        path = args.path.strip("/")
        if not path:
            folder_id = "0"
        else:
            folder_id = client._resolve_path(path)
        
        # 列出所有文件
        result = client.list_files(folder_id=folder_id, size=1000)
        files = result.get("data", {}).get("list", [])
        
        if not files:
            print(f"✅ 目录已是空的: /{path}")
            return
        
        print(f"\n⚠️  即将清空目录: /{path}")
        print(f"   包含 {len(files)} 个项目")
        
        # 确认清空
        if not args.yes:
            confirm = input("确定要清空吗？此操作不可恢复！(y/N): ")
            if confirm.lower() != "y":
                print("已取消")
                return
        
        # 删除所有文件
        file_ids = [item["fid"] for item in files]
        
        print("清空中...")
        result = client.delete_files(file_ids)
        
        if result.get("status") == 200:
            print(f"✅ 已清空 {len(files)} 个项目")
        else:
            print(f"❌ 清空失败: {result}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_mkdir(args):
    """创建文件夹命令"""
    try:
        client = QuarkClient()
        
        folder_name = args.name
        parent_path = args.parent.strip("/") if args.parent else ""
        
        if parent_path:
            parent_id = client._resolve_path(parent_path)
        else:
            parent_id = "0"
        
        print(f"\n📁 创建文件夹: {folder_name}")
        
        result = client.create_folder(folder_name, parent_id)
        
        if result.get("status") == 200:
            print("✅ 创建成功！")
        else:
            print(f"❌ 创建失败: {result}")
    except Exception as e:
        print(f"错误: {e}")

def cmd_config(args):
    """配置命令"""
    if args.cookie:
        CookieManager.save_cookie(args.cookie)
        print("✅ Cookie 已保存")
    elif args.clear:
        CookieManager.clear_cookie()
        print("✅ Cookie 已清除")
    else:
        cookie = CookieManager.get_cookie()
        if cookie:
            print(f"当前 Cookie: {cookie[:20]}...")
        else:
            print("未配置 Cookie")

def _format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

# ============================================================
# 分享命令
# ============================================================

# 过期时间映射
EXPIRED_TYPES = {
    "1d": 1,   # 1天
    "7d": 2,   # 7天
    "30d": 3,  # 30天
    "permanent": 4,  # 永久
    "永不过期": 4,
    "1天": 1,
    "7天": 2,
    "30天": 3,
}

# 分享URL解析正则
SHARE_URL_PATTERN = re.compile(r'https?://pan\.quark\.cn/s/([a-zA-Z0-9]+)')
PASSCODE_PATTERN = re.compile(r'(?:提取码|密码)[：:\s]*([a-zA-Z0-9]+)')

def parse_share_url(text: str) -> tuple:
    """解析夸克分享链接，返回 (share_id, passcode)"""
    m = SHARE_URL_PATTERN.search(text)
    if not m:
        raise ValueError(f"无法解析分享链接: {text}")
    share_id = m.group(1)
    
    passcode = None
    m2 = PASSCODE_PATTERN.search(text)
    if m2:
        passcode = m2.group(1)
    return share_id, passcode


def cmd_share(args):
    """分享文件/文件夹"""
    try:
        client = QuarkClient()
        
        # 解析路径获取 fid
        path = args.path.strip("/")
        if not path:
            folder_id = "0"
        else:
            # 尝试查找文件或文件夹
            parts = path.split("/")
            current_id = "0"
            
            for i, part in enumerate(parts):
                result = client.list_files(current_id, size=100)
                found = False
                is_last = (i == len(parts) - 1)
                
                for item in result.get("data", {}).get("list", []):
                    if item.get("file_name") == part:
                        if is_last or item.get("file_type") == 0:  # 最后一级或文件夹
                            current_id = item["fid"]
                            found = True
                            break
                
                if not found:
                    raise FileNotFoundError(f"路径不存在: {args.path}")
            
            folder_id = current_id
        
        # 获取文件名作为分享标题
        title = args.title or path.split("/")[-1] or "分享"
        
        # 解析过期时间
        expired_type = EXPIRED_TYPES.get(args.expire, 2)  # 默认7天
        
        # 创建分享
        json_data = {
            "fid_list": [folder_id],
            "title": title,
            "url_type": 2 if args.passcode else 1,  # 有密码时用类型2
            "expired_type": expired_type,
        }
        
        # 添加密码
        if args.passcode:
            json_data["passcode"] = args.passcode
        
        result = client._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["share"], json_data=json_data)
        
        if result.get("status") == 200:
            share_data = result.get("data", {})
            # share_id 可能在多层嵌套中
            share_id = share_data.get("share_id")
            if not share_id:
                task_resp = share_data.get("task_resp", {})
                share_id = task_resp.get("data", {}).get("share_id")
            
            if share_id:
                # 查询分享详情（含口令）
                pwd_result = client._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["share_password"], 
                    json_data={"share_id": share_id})
                
                if pwd_result.get("status") == 200:
                    pwd_data = pwd_result.get("data", {})
                    share_url = pwd_data.get("share_url", "")
                    pwd_id = pwd_data.get("pwd_id", "")
                    passcode = pwd_data.get("passcode", "")
                    
                    print("\n" + "="*50)
                    print("🔗 分享创建成功")
                    print("="*50)
                    print(f"📁 分享名称: {title}")
                    print(f"⏰ 有效期: {args.expire}")
                    if share_url:
                        print(f"🔗 分享链接: {share_url}")
                    if passcode:
                        print(f"🔑 提取码: {passcode}")
                    if pwd_id:
                        print(f"🆔 分享ID: {pwd_id}")
                    print("="*50)
                else:
                    print(f"⚠️ 获取分享详情失败: {pwd_result}")
            else:
                print(f"⚠️ 未获取到 share_id: {share_data}")
        else:
            print(f"❌ 分享失败: {result}")
            
    except Exception as e:
        print(f"错误: {e}")
        print("请先运行 login 命令登录")

def cmd_share_list(args):
    """列出我的分享"""
    try:
        client = QuarkClient()
        
        params = {
            "_page": str(args.page),
            "_size": str(args.size),
            "_fetch_total": "1",
        }
        
        result = client._request("GET", DRIVE_DOMAIN, API_ENDPOINTS["share_list"], params=params)
        
        if result.get("status") == 200:
            data = result.get("data", {})
            shares = data.get("list", [])
            total = data.get("total", 0)
            
            print("\n" + "="*60)
            print(f"🔗 我的分享 (共 {total} 个)")
            print("="*60)
            
            if not shares:
                print("  暂无分享")
            else:
                for share in shares:
                    title = share.get("title", "未知")
                    share_id = share.get("share_id", "")
                    url = share.get("share_url", "")
                    status = "✅ 有效" if share.get("status") == 1 else "❌ 已失效"
                    expired = share.get("expired_type", 0)
                    expire_str = {1: "1天", 2: "7天", 3: "30天", 4: "永久"}.get(expired, "未知")
                    
                    print(f"\n  📄 {title}")
                    print(f"     状态: {status}")
                    print(f"     有效期: {expire_str}")
                    if url:
                        print(f"     链接: {url}")
                    print(f"     ID: {share_id}")
            
            print("\n" + "="*60)
        else:
            print(f"❌ 获取分享列表失败: {result}")
            
    except Exception as e:
        print(f"错误: {e}")
        print("请先运行 login 命令登录")

def cmd_share_cancel(args):
    """取消分享"""
    try:
        client = QuarkClient()
        
        # 如果提供的是链接，提取 share_id
        share_id = args.share_id
        if "quark.cn" in share_id:
            # 尝试从链接提取
            import re
            match = re.search(r'/s/(\w+)', share_id)
            if match:
                share_id = match.group(1)
        
        # 取消分享
        json_data = {
            "share_id": share_id,
            "action": "cancel",
        }
        
        result = client._request("POST", DRIVE_DOMAIN, f"/1/clouddrive/share/{share_id}/cancel", 
            json_data=json_data)
        
        if result.get("status") == 200:
            print(f"✅ 分享已取消: {share_id}")
        else:
            print(f"❌ 取消分享失败: {result}")
            
    except Exception as e:
        print(f"错误: {e}")
        print("请先运行 login 命令登录")

def cmd_share_save(args):
    """转存他人分享到我的网盘"""
    try:
        client = QuarkClient()
        
        # 解析分享链接
        share_id, parsed_pass = parse_share_url(args.share)
        passcode = args.passcode or parsed_pass
        
        # 获取分享token
        token_data = {
            "pwd_id": share_id,
            "passcode": passcode or "",
            "support_visit_limit_private_share": True,
        }
        
        token_result = client._request("POST", DRIVE_DOMAIN, 
            "/1/clouddrive/share/sharepage/token",
            json_data=token_data)
        
        if token_result.get("status") != 200:
            print(f"❌ 获取分享token失败: {token_result}")
            return
        
        stoken = token_result.get("data", {}).get("stoken")
        if not stoken:
            print(f"❌ token缺失: {token_result}")
            return
        
        # 获取分享详情
        detail_params = {
            "pwd_id": share_id,
            "stoken": stoken,
            "pdir_fid": "0",
            "force": "0",
            "_page": "1",
            "_size": "200",
            "_fetch_share": "1",
        }
        
        detail_result = client._request("GET", DRIVE_DOMAIN, 
            "/1/clouddrive/share/sharepage/detail",
            params=detail_params)
        
        # 目标目录
        target_dir = args.to or "/转存文件"
        
        # 确保目标目录存在
        target_fid = client._resolve_path(target_dir) if target_dir != "/" else "0"
        
        # 转存
        save_data = {
            "fid_list": [],
            "fid_token_list": [],
            "to_pdir_fid": target_fid,
            "pwd_id": share_id,
            "stoken": stoken,
            "pdir_fid": "0",
            "pdir_save_all": True,
            "exclude_fids": [],
            "scene": "link",
        }
        
        save_result = client._request("POST", DRIVE_DOMAIN, 
            "/1/clouddrive/share/sharepage/save",
            json_data=save_data)
        
        if save_result.get("status") == 200:
            print(f"\n{'='*50}")
            print("✅ 转存成功")
            print(f"{'='*50}")
            print(f"📁 保存到: {target_dir}")
            
            # 显示分享详情
            if detail_result.get("status") == 200:
                detail_data = detail_result.get("data", {})
                share_info = detail_data.get("share", {})
                file_list = detail_data.get("list", [])
                
                if share_info:
                    print(f"📄 分享标题: {share_info.get('title', '未知')}")
                if file_list:
                    print(f"📊 文件数量: {len(file_list)} 个")
            
            print(f"{'='*50}")
        else:
            print(f"❌ 转存失败: {save_result}")
            
    except ValueError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"错误: {e}")
        print("请先运行 login 命令登录")

# ============================================================
# 批量上传命令
# ============================================================

def cmd_batch_upload(args):
    """批量上传目录到夸克网盘"""
    try:
        import math
        from datetime import datetime, timezone
        
        client = QuarkClient()
        local_dir = Path(args.local_dir)
        
        if not local_dir.exists():
            print(f"❌ 本地目录不存在: {local_dir}")
            return
        
        # 远程目标目录
        remote_base = args.remote_dir or f"/备份/{datetime.now().strftime('%Y%m%d')}"
        
        print(f"\n📤 批量上传")
        print(f"   本地目录: {local_dir}")
        print(f"   远程目录: {remote_base}")
        
        # 收集文件（跳过指定目录和文件）
        skip_patterns = args.skip.split(",") if args.skip else [
            "__pycache__", ".pyc", "node_modules", ".git", "cache", ".bak"
        ]
        
        files = []
        for root, dirs, filenames in os.walk(local_dir):
            # 跳过指定目录
            dirs[:] = [d for d in dirs if not any(p in d for p in skip_patterns)]
            
            for fname in filenames:
                if any(p in fname for p in skip_patterns):
                    continue
                
                fp = Path(root) / fname
                sz = fp.stat().st_size
                
                # 跳过大文件（默认10MB限制）
                if args.max_size and sz > args.max_size * 1024 * 1024:
                    continue
                
                rel = fp.relative_to(local_dir)
                files.append((fp, rel, sz))
        
        if not files:
            print("📁 目录为空或无需上传的文件")
            return
        
        print(f"📊 找到 {len(files)} 个文件")
        
        # 确保远程目录存在
        remote_fid = "0"
        for part in remote_base.strip("/").split("/"):
            # 查找或创建文件夹
            result = client.list_files(remote_fid, size=200)
            found = False
            for item in result.get("data", {}).get("list", []):
                if item.get("file_name") == part and item.get("file_type") == 0:
                    remote_fid = item["fid"]
                    found = True
                    break
            
            if not found:
                result = client.create_folder(part, remote_fid)
                remote_fid = result.get("data", {}).get("fid")
                if not remote_fid:
                    print(f"❌ 创建目录失败: {part}")
                    return
        
        # 上传文件
        success_count = 0
        fail_count = 0
        skip_count = 0
        
        for i, (fp, rel, sz) in enumerate(files, 1):
            try:
                # 创建子目录
                parent_rel = str(rel.parent)
                if parent_rel != ".":
                    parent_fid = remote_fid
                    for sub_part in parent_rel.split("/"):
                        if not sub_part:
                            continue
                        result = client.list_files(parent_fid, size=200)
                        found = False
                        for item in result.get("data", {}).get("list", []):
                            if item.get("file_name") == sub_part and item.get("file_type") == 0:
                                parent_fid = item["fid"]
                                found = True
                                break
                        if not found:
                            result = client.create_folder(sub_part, parent_fid)
                            parent_fid = result.get("data", {}).get("fid")
                            if not parent_fid:
                                skip_count += 1
                                break
                else:
                    parent_fid = remote_fid
                
                if not parent_fid:
                    skip_count += 1
                    continue
                
                # 上传文件
                file_size = fp.stat().st_size
                md5_str, sha1_str = _calculate_md5(fp), _calculate_sha1(fp)
                mime_type = mimetypes.guess_type(str(fp))[0] or "application/octet-stream"
                now_ms = int(time.time() * 1000)
                
                pre_data = {
                    "ccp_hash_update": True,
                    "dir_name": "",
                    "file_name": fp.name,
                    "format_type": mime_type,
                    "l_created_at": now_ms,
                    "l_updated_at": now_ms,
                    "pdir_fid": parent_fid,
                    "size": file_size,
                }
                
                pre_result = client._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["upload_pre"], json_data=pre_data)
                
                if pre_result.get("status") != 200:
                    fail_count += 1
                    print(f"  ❌ [{i}/{len(files)}] {rel} - 预请求失败")
                    continue
                
                # 哈希检查（秒传）
                hash_result = client._request("POST", DRIVE_DOMAIN, API_ENDPOINTS["upload_hash"],
                    json_data={"md5": md5_str, "sha1": sha1_str, "task_id": pre_result["data"]["task_id"]})
                
                if hash_result.get("data", {}).get("finish"):
                    success_count += 1
                    print(f"  ⚡ [{i}/{len(files)}] {rel} (秒传)")
                    continue
                
                # COS上传
                upload_info = pre_result["data"]
                upload_info["metadata"] = pre_result.get("metadata", {})
                _upload_to_cos(client, fp, upload_info)
                
                success_count += 1
                if i % 10 == 0 or i == len(files):
                    print(f"  📊 进度: {i}/{len(files)} (✓={success_count} ✗={fail_count} ⊘={skip_count})")
                
                # 避免请求过快
                if i % 20 == 0:
                    time.sleep(1)
                    
            except Exception as e:
                fail_count += 1
                print(f"  ❌ [{i}/{len(files)}] {rel} - {e}")
        
        print(f"\n{'='*50}")
        print(f"📊 上传完成！✓成功={success_count}  ✗失败={fail_count}  ⊘跳过={skip_count}")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"错误: {e}")
        print("请先运行 login 命令登录")

# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="夸克网盘 CLI 工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # login 命令
    login_parser = subparsers.add_parser("login", help="扫码登录")
    login_parser.add_argument("--timeout", type=int, default=300, help="超时时间（秒）")
    
    # user 命令
    subparsers.add_parser("user", help="查看用户信息")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出文件")
    list_parser.add_argument("path", nargs="?", default="/", help="目录路径")
    list_parser.add_argument("--page", type=int, default=1, help="页码")
    list_parser.add_argument("--size", type=int, default=50, help="每页数量")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索文件")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--page", type=int, default=1, help="页码")
    search_parser.add_argument("--size", type=int, default=50, help="每页数量")
    
    # upload 命令
    upload_parser = subparsers.add_parser("upload", help="上传文件")
    upload_parser.add_argument("local_path", help="本地文件路径")
    upload_parser.add_argument("remote_path", help="远程文件路径")
    
    # download 命令
    download_parser = subparsers.add_parser("download", help="下载文件")
    download_parser.add_argument("remote_path", help="远程文件路径")
    download_parser.add_argument("local_path", help="本地保存路径")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除文件")
    delete_parser.add_argument("path", help="文件路径")
    delete_parser.add_argument("-y", "--yes", action="store_true", help="跳过确认")
    
    # clear 命令
    clear_parser = subparsers.add_parser("clear", help="清空目录")
    clear_parser.add_argument("path", nargs="?", default="/", help="目录路径")
    clear_parser.add_argument("-y", "--yes", action="store_true", help="跳过确认")
    
    # mkdir 命令
    mkdir_parser = subparsers.add_parser("mkdir", help="创建文件夹")
    mkdir_parser.add_argument("name", help="文件夹名称")
    mkdir_parser.add_argument("--parent", help="父目录路径")
    
    # config 命令
    config_parser = subparsers.add_parser("config", help="配置")
    config_parser.add_argument("--cookie", help="设置 Cookie")
    config_parser.add_argument("--clear", action="store_true", help="清除 Cookie")
    
    # share 命令
    share_parser = subparsers.add_parser("share", help="分享文件/文件夹")
    share_parser.add_argument("path", help="要分享的文件或文件夹路径")
    share_parser.add_argument("--title", help="分享标题（默认使用文件名）")
    share_parser.add_argument("--expire", default="7d", 
        choices=["1d", "7d", "30d", "permanent", "1天", "7天", "30天", "永不过期"],
        help="有效期: 1d/7d/30d/permanent (默认7天)")
    share_parser.add_argument("--passcode", help="提取码（可选，不填则无密码）")
    
    
    # share-list 命令
    share_list_parser = subparsers.add_parser("share-list", help="列出我的分享")
    share_list_parser.add_argument("--page", type=int, default=1, help="页码")
    share_list_parser.add_argument("--size", type=int, default=20, help="每页数量")
    
    # share-cancel 命令
    share_cancel_parser = subparsers.add_parser("share-cancel", help="取消分享")
    share_cancel_parser.add_argument("share_id", help="分享ID或链接")
    
    # share-save 命令
    share_save_parser = subparsers.add_parser("share-save", help="转存他人分享")
    share_save_parser.add_argument("share", help="分享链接或包含链接的文本")
    share_save_parser.add_argument("--passcode", help="提取码（可选，会自动从文本解析）")
    share_save_parser.add_argument("--to", help="保存到的目录（默认/转存文件）")
    
    # batch-upload 命令
    batch_upload_parser = subparsers.add_parser("batch-upload", help="批量上传目录")
    batch_upload_parser.add_argument("local_dir", help="本地目录路径")
    batch_upload_parser.add_argument("--remote-dir", help="远程目标目录（默认/备份/日期）")
    batch_upload_parser.add_argument("--skip", help="跳过的模式，逗号分隔")
    batch_upload_parser.add_argument("--max-size", type=int, default=10, help="最大文件大小(MB)，默认10")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    commands = {
        "login": cmd_login,
        "user": cmd_user,
        "list": cmd_list,
        "search": cmd_search,
        "upload": cmd_upload,
        "download": cmd_download,
        "delete": cmd_delete,
        "clear": cmd_clear,
        "mkdir": cmd_mkdir,
        "config": cmd_config,
        "share": cmd_share,
        "share-list": cmd_share_list,
        "share-cancel": cmd_share_cancel,
        "share-save": cmd_share_save,
        "batch-upload": cmd_batch_upload,
    }
    
    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
