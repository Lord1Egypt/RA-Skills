#!/usr/bin/env python3
"""
第三方接入示例 — 慧龄云(R)中华05骨龄智能检测

适用场景：SaaS平台、医院信息系统、体检平台等第三方系统对接
调用路径：路径A（轻量路径 — 仅AI骨龄识别）
核心接口：/bmd/v2/cosBoneAgeOnLineByThirdPartner

前置要求：
  1. 登录账号需具备"第三方" Shiro 角色
  2. 账号 counts > 0（有剩余计算次数，每次调用扣1次）
  3. 安装依赖：pip install requests

用法：
  # 设置环境变量后直接运行
  export BONE_AGE_USERNAME=your_phone
  export BONE_AGE_PASSWORD_HASH=your_sha256_hash
  python third_party_integration.py --image bone.jpg --sex M

  # 或通过命令行参数
  python third_party_integration.py --host https://www.pipitu.net --username 13800000000 --password-hash abc123 --image bone.jpg --sex M
"""

import argparse
import hashlib
import json
import os
import sys
import uuid

try:
    import requests
except ImportError:
    print("需要安装 requests 库：pip install requests", file=sys.stderr)
    sys.exit(1)


class ThirdPartyBoneAgeClient:
    """第三方骨龄检测客户端 — 轻量路径"""

    def __init__(self, host: str):
        self.host = host.rstrip("/")
        self.token = None
        self.user = None
        self.tid = f"TID-{uuid.uuid4().hex[:16].upper()}"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=utf-8"})

    def register(self) -> bool:
        """Step 1: 终端注册激活"""
        resp = self.session.post(
            f"{self.host}/v1/baClient/tidRegister",
            json={"tid": self.tid}, timeout=15
        )
        result = resp.json()
        if result.get("ret"):
            print(f"[OK] 终端注册成功: TID={self.tid}")
            return True
        else:
            print(f"[WARN] 终端注册跳过: {result.get('msg')}")
            return False

    def login(self, username: str, password_hash: str) -> bool:
        """Step 2: 密码登录，获取TOKEN"""
        resp = self.session.post(
            f"{self.host}/auth/local/login",
            json={"username": username, "password": password_hash}, timeout=15
        )
        result = resp.json()
        if result.get("ret"):
            self.token = result["data"]["token"]
            self.user = result["data"].get("user", {})
            # ⚠️ 关键：Header名是"token"，不是"Authorization: Bearer"
            self.session.headers.update({"token": self.token})
            print(f"[OK] 登录成功")
            print(f"   VIP: {self.user.get('enable')}, 剩余次数: {self.user.get('counts')}")
            return True
        else:
            print(f"[FAIL] 登录失败: {result.get('msg')}")
            return False

    def upload_image(self, file_name: str, image_path: str) -> bool:
        """Step 3+4: 获取预签名URL并上传图片"""
        # 获取预签名URL（只需fileName，uuid从登录态自动获取）
        resp = self.session.post(
            f"{self.host}/service/signForBAImageUploadEasy",
            json={"fileName": file_name}, timeout=15
        )
        result = resp.json()
        if not result.get("ret"):
            print(f"[FAIL] 获取上传URL失败: {result.get('msg')}")
            return False

        signed_url = result["data"]["signedUrl"]

        # PUT上传图片
        with open(image_path, "rb") as f:
            put_resp = requests.put(signed_url, data=f.read(), timeout=30)

        if put_resp.status_code == 200:
            print(f"[OK] 图片上传成功: {file_name}")
            return True
        else:
            print(f"[FAIL] 图片上传失败: HTTP {put_resp.status_code}")
            return False

    def detect_bone_age(self, file_name: str, sex: str) -> dict:
        """Step 5: 第三方AI骨龄识别（无条件扣1次）"""
        resp = self.session.post(
            f"{self.host}/bmd/v2/cosBoneAgeOnLineByThirdPartner",
            json={"fileName": file_name, "sex": sex.upper()}, timeout=45
        )
        result = resp.json()
        if result.get("ret"):
            data = result["data"]
            print(f"[OK] 骨龄识别成功")
            print(f"   骨龄: {data.get('bam')} 岁")
            print(f"   SMS:  {data.get('sms')}")
            print(f"   stages: {data.get('stages')}")
            return data
        else:
            print(f"[FAIL] 骨龄识别失败: {result.get('msg')}")
            return None

    def full_flow(self, username: str, password_hash: str, image_path: str, sex: str) -> dict:
        """完整第三方接入流程：注册→登录→上传→骨龄识别"""
        # Step 1
        self.register()

        # Step 2
        if not self.login(username, password_hash):
            return None

        # Step 3+4
        file_name = os.path.basename(image_path)
        if not self.upload_image(file_name, image_path):
            return None

        # Step 5
        return self.detect_bone_age(file_name, sex)


def generate_report(data: dict, sex: str) -> str:
    """根据API返回数据生成中文诊断报告"""
    if not data:
        return "骨龄识别失败，无法生成报告"

    bam = data.get("bam", "?")
    sms = data.get("sms", "?")
    stages = data.get("stages", [])
    url = data.get("url", "")

    # 13块骨骼名称
    bone_names = [
        "桡骨", "尺骨", "掌骨I", "掌骨III", "掌骨V",
        "近节指骨I", "近节指骨III", "近节指骨V",
        "中节指骨III", "中节指骨V",
        "远节指骨I", "远节指骨III", "远节指骨V"
    ]

    report = f"""
{'='*50}
       中华05骨龄AI评估报告
{'='*50}

评估方法：中华05标准 (RUS-CHN05计分法)
性    别：{'男' if sex == 'M' else '女'}

━━━━━━━━━━ 骨龄评估 ━━━━━━━━━━

骨龄：{bam} 岁
骨成熟度评分 (SMS)：{sms} (满分1000)

━━━━━━━━━━ 骨骼发育等级 ━━━━━━━━━━
"""
    if stages and len(stages) >= 13:
        for i, name in enumerate(bone_names):
            report += f"  {name:12s}：等级 {stages[i]}\n"

    if url:
        report += f"""
━━━━━━━━━━ 标注图片 ━━━━━━━━━━
{url}
"""

    report += f"""
━━━━━━━━━━ 免责声明 ━━━━━━━━━━
本报告由AI辅助分析生成，仅供参考，不构成医疗诊断。
骨龄评估存在约+/-1岁的正常观察误差。
如有异常，请前往正规医疗机构儿科内分泌科就诊。
{'='*50}
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="第三方接入示例 — 慧龄云骨龄检测")
    parser.add_argument("--host", default=os.getenv("BONE_AGE_API_HOST", "https://www.pipitu.net"))
    parser.add_argument("--username", default=os.getenv("BONE_AGE_USERNAME"))
    parser.add_argument("--password-hash", default=os.getenv("BONE_AGE_PASSWORD_HASH"))
    parser.add_argument("--image", required=True, help="X光片图片路径")
    parser.add_argument("--sex", required=True, choices=["M", "F"], help="性别")
    args = parser.parse_args()

    if not args.username or not args.password_hash:
        print("错误：请通过 --username/--password-hash 或环境变量提供登录凭证", file=sys.stderr)
        sys.exit(1)

    client = ThirdPartyBoneAgeClient(host=args.host)
    data = client.full_flow(
        username=args.username,
        password_hash=args.password_hash,
        image_path=args.image,
        sex=args.sex
    )

    if data:
        print(generate_report(data, args.sex))


if __name__ == "__main__":
    main()
