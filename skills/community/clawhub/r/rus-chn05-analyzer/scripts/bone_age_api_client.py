#!/usr/bin/env python3
"""
慧龄云®中华05骨龄检测 API 客户端
对接慧龄云®骨龄人工智能检测系统（host: www.pipitu.net）

两种调用路径：
  路径A（轻量，推荐）：注册→登录→上传→cosBoneAgeOnLineByThirdPartner（仅骨龄识别）
  路径B（完整）：注册→登录→上传→predictHeightByBoneAge（骨龄+身高预测）

⚠️ 关键源码验证结论：
  1. appid 是请求体可选参数（用于消息推送），不需要从登录结果中获取
  2. signForBAImageUploadEasy 只需要 fileName，uuid 从登录态自动获取
  3. 轻量路径返回字段名是 bam/fname（非 bam05/fileName）
  4. 第三方接口需要"第三方"Shiro角色，无条件扣次数
  5. 推理服务器参数名为 filename（小写n），Java后端自动转换

用法：
  # 轻量路径（仅骨龄识别）
  python bone_age_api_client.py --host https://www.pipitu.net --username user --password-hash xxx --image bone.jpg --sex M

  # 完整路径（骨龄+身高预测）
  python bone_age_api_client.py --host https://www.pipitu.net --username user --password-hash xxx --image bone.jpg --sex M --age 10.5 --height 140 --weight 35 --father-height 175 --mother-height 162 --phone 13800000000 --full

  # 仅登录测试
  python bone_age_api_client.py --host https://www.pipitu.net --username user --password-hash xxx --login-only

  # 查询历史报告
  python bone_age_api_client.py --host https://www.pipitu.net --username user --password-hash xxx --history
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


class BoneAgeAPIClient:
    """慧龄云®骨龄检测系统 API 客户端"""

    def __init__(self, host: str):
        self.host = host.rstrip("/")
        self.token = None
        self.user = None
        self.tid = self._generate_tid()
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=utf-8"})

    @staticmethod
    def _generate_tid() -> str:
        """生成终端唯一标识"""
        return f"TID-{uuid.uuid4().hex[:16].upper()}"

    @staticmethod
    def sha256(text: str) -> str:
        """SHA256加密"""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _url(self, path: str) -> str:
        """拼接完整URL"""
        return f"{self.host}{path}"

    def _auth_header(self) -> dict:
        """
        构造鉴权Header。
        ⚠️ 源码验证（StatelessAuthFilter.java + Constants.java）：
        Header名是 "token"，值直接是JWT字符串，不加 "Bearer " 前缀。
        即 req.getHeader("token") — PARAM_DIGEST = "token"
        """
        if not self.token:
            raise ValueError("未登录，请先调用 login()")
        return {"token": self.token}  # ⚠️ 不是 Authorization: Bearer

    # ==================== Step 1：终端注册激活 ====================
    def register(self) -> dict:
        """终端注册激活"""
        resp = self.session.post(
            self._url("/v1/baClient/tidRegister"),
            json={"tid": self.tid}
        )
        result = resp.json()
        if result.get("ret"):
            print(f"[OK] 终端注册成功：TID={self.tid}")
        else:
            print(f"[FAIL] 终端注册失败：{result.get('msg')}")
        return result

    # ==================== Step 2：密码登录（获取TOKEN）====================
    def login(self, username: str, password_hash: str) -> dict:
        """
        密码登录，获取TOKEN和用户信息。
        ⚠️ appid 不从登录结果中获取——它是请求体可选参数，仅在需要微信消息推送时传递。
        """
        resp = self.session.post(
            self._url("/auth/local/login"),
            json={"username": username, "password": password_hash}
        )
        result = resp.json()
        if result.get("ret"):
            data = result.get("data", {})
            self.token = data.get("token")
            self.user = data.get("user")
            expire = data.get("expireTime", 0)
            # ⚠️ 源码验证：Header名是"token"，直接写JWT值，不加"Bearer "前缀
            self.session.headers.update({"token": self.token})
            print(f"[OK] 登录成功，TOKEN有效期：{expire}秒")
            if self.user:
                print(f"   user.id={self.user.get('id')}")
                print(f"   user.enable(VIP)={self.user.get('enable')}")
                print(f"   user.counts(剩余次数)={self.user.get('counts')}")
        else:
            print(f"[FAIL] 登录失败：{result.get('msg')}")
        return result

    # ==================== Step 3：获取图片上传预签名URL ====================
    def get_upload_url(self, file_name: str) -> dict:
        """
        获取图片上传预签名URL。
        ⚠️ 源码验证：仅需 fileName 参数，uuid 从 Shiro 登录态自动获取。
        COS key 格式：{preDir}{uuid}/{fileName}，预签名有效期30分钟。
        """
        resp = self.session.post(
            self._url("/service/signForBAImageUploadEasy"),
            json={"fileName": file_name},
            headers=self._auth_header()
        )
        result = resp.json()
        if result.get("ret"):
            signed_url = result.get("data", {}).get("signedUrl", "")
            print(f"[OK] 获取预签名URL成功")
        else:
            print(f"[FAIL] 获取预签名URL失败：{result.get('msg')}")
        return result

    # ==================== Step 4：上传图片 ====================
    def upload_image(self, signed_url: str, file_path: str) -> bool:
        """通过预签名URL上传图片"""
        with open(file_path, "rb") as f:
            resp = requests.put(signed_url, data=f.read())
        if resp.status_code == 200:
            print(f"[OK] 图片上传成功：{file_path}")
            return True
        else:
            print(f"[FAIL] 图片上传失败：HTTP {resp.status_code}")
            return False

    # ==================== 路径A：轻量路径 — 仅AI骨龄识别（推荐）====================
    def bone_age_detect(
        self,
        file_name: str,
        sex: str,
        use_third_party: bool = True
    ) -> dict:
        """
        路径A：仅AI骨龄识别。

        ⚠️ 关键源码验证：
        - 第三方接口：/bmd/v2/cosBoneAgeOnLineByThirdPartner（需要"第三方"角色，无条件扣次数）
        - 内部接口：/bmd/v2/cosBoneAgeOnLine（非会员1次/周期限频，会员无限）
        - 推理服务器参数：Java后端将 fileName 转为 filename（小写n），并自动附带 uuid 和 vip
        - 返回字段名：bam（骨龄）、fname（文件名），不是 bam05/fileName
        - 会员返回浮点 scores + 浮点 sms（插值法），非会员返回整数 sms + RUSCHNTables 重算 scores
        """
        if use_third_party:
            endpoint = "/bmd/v2/cosBoneAgeOnLineByThirdPartner"
        else:
            endpoint = "/bmd/v2/cosBoneAgeOnLine"

        params = {
            "fileName": file_name,
            "sex": sex.upper()
        }

        resp = self.session.post(
            self._url(endpoint),
            json=params,
            headers=self._auth_header()
        )
        result = resp.json()
        if result.get("ret"):
            data = result.get("data", {})
            bam = data.get("bam")      # ⚠️ 字段名是 bam，不是 bam05
            sms = data.get("sms")
            fname = data.get("fname")  # ⚠️ 字段名是 fname
            stages = data.get("stages")
            print(f"[OK] 骨龄识别成功：骨龄={bam}岁，SMS={sms}")
            print(f"   标注图文件名：{fname}")
            print(f"   骨骺等级：{stages}")
        else:
            print(f"[FAIL] 骨龄识别失败：{result.get('msg')}")
        return result

    # ==================== 路径B：完整路径 — AI骨龄+身高预测 ====================
    def bone_age_assessment(
        self,
        sex: str,
        age: float,
        height: float,
        weight: float,
        father_height: float,
        mother_height: float,
        phone: str,
        file_name: str,
        name: str = "匿名",
        has_m: str = None,
        moon_age: float = None,
        order_no: str = None,
        is_white_man: bool = False,
        appid: str = None,
        use_v2: bool = True
    ) -> dict:
        """
        路径B：AI骨龄推算+身高预测。

        ⚠️ 关键源码验证：
        - appid 是请求体可选参数（用于微信消息推送），不需要提前配置
        - AI推算用 detectedImgName（不是 fileName）
        - 非会员3次/分钟限频
        - 非会员counts=0时返回模糊结果（身高末位*替换）
        - 返回字段名是 bam05（此路径）而非 bam（路径A）
        """
        version = "v2" if use_v2 else "v1"
        endpoint = f"/bmd/{version}/predictHeightByBoneAge"

        params = {
            "sex": sex.upper(),
            "age": age,
            "height": height,
            "weight": weight,
            "name": name,
            "fatherHeight": father_height,
            "motherHeight": mother_height,
            "telephone": phone,
            "detectedImgName": file_name,  # ⚠️ AI推算用 detectedImgName
            "isWhiteMan": is_white_man
        }

        # appid 为可选参数，仅用于微信消息推送
        if appid:
            params["appid"] = appid

        # 女性初潮信息
        if sex.upper() == "F":
            params["hasM"] = has_m or "no"
            if has_m == "yes" and moon_age:
                params["moonAge"] = moon_age

        if order_no:
            params["orderNo"] = order_no

        resp = self.session.post(
            self._url(endpoint),
            json=params,
            headers=self._auth_header()
        )
        result = resp.json()
        if result.get("ret"):
            data = result.get("data", {})
            bam05 = data.get("bam05")
            sms = data.get("sms", "")
            print(f"[OK] 骨龄推算成功：骨龄={bam05}岁，SMS={sms}")
        else:
            print(f"[FAIL] 骨龄推算失败：{result.get('msg')}")
        return result

    # ==================== 人工修改等级后重新推算 ====================
    def bone_age_assessment_manual(
        self,
        sex: str,
        age: float,
        height: float,
        weight: float,
        father_height: float,
        mother_height: float,
        phone: str,
        file_name: str,
        stages: list,
        sms: str,
        rp_img: str = "",
        name: str = "匿名",
        has_m: str = None,
        moon_age: float = None,
        order_no: str = None,
        appid: str = None
    ) -> dict:
        """人工修改等级后重新推算"""
        params = {
            "sex": sex.upper(),
            "age": age,
            "height": height,
            "weight": weight,
            "name": name,
            "fatherHeight": father_height,
            "motherHeight": mother_height,
            "telephone": phone,
            "userId": self.user.get("id") if self.user else "",
            "selectedFileName": file_name,  # ⚠️ 人工修改用 selectedFileName
            "stages": stages,
            "sms": sms,
            "rpImg": rp_img
        }

        # appid 为可选参数
        if appid:
            params["appid"] = appid

        if sex.upper() == "F":
            params["hasM"] = has_m or "no"
            if has_m == "yes" and moon_age:
                params["moonAge"] = moon_age

        if order_no:
            params["orderNo"] = order_no

        resp = self.session.post(
            self._url("/bmd/v2/predictHeightFromWebBySms"),
            json=params,
            headers=self._auth_header()
        )
        return resp.json()

    # ==================== 历史报告查询 ====================
    def get_history_reports(self, limit: int = 10, skip: int = 0, sort: str = "desc") -> dict:
        """查询历史报告"""
        resp = self.session.post(
            self._url("/service/serviceLogs/getHistoryReports"),
            json={"limit": limit, "skip": skip, "sort": sort},
            headers=self._auth_header()
        )
        return resp.json()

    # ==================== 完整流程（路径A：仅骨龄识别）====================
    def full_detect(
        self,
        username: str,
        password_hash: str,
        image_path: str,
        sex: str
    ) -> dict:
        """
        完整骨龄识别流程（路径A）：注册→登录→上传→骨龄识别
        """
        # Step 1: 注册
        reg_result = self.register()
        if not reg_result.get("ret"):
            pass  # 可能已注册，继续

        # Step 2: 登录
        login_result = self.login(username, password_hash)
        if not login_result.get("ret"):
            return {"error": "登录失败", "detail": login_result}

        # Step 3: 获取上传URL
        file_name = os.path.basename(image_path)
        upload_result = self.get_upload_url(file_name)
        if not upload_result.get("ret"):
            return {"error": "获取上传URL失败", "detail": upload_result}

        signed_url = upload_result.get("data", {}).get("signedUrl", "")

        # Step 4: 上传图片
        if not self.upload_image(signed_url, image_path):
            return {"error": "图片上传失败"}

        # Step 5: AI骨龄识别（路径A，第三方接口）
        detect_result = self.bone_age_detect(file_name=file_name, sex=sex)

        return detect_result

    # ==================== 完整流程（路径B：骨龄+身高预测）====================
    def full_assessment(
        self,
        username: str,
        password_hash: str,
        image_path: str,
        sex: str,
        age: float,
        height: float,
        weight: float,
        father_height: float,
        mother_height: float,
        phone: str,
        name: str = "匿名",
        has_m: str = None,
        moon_age: float = None,
        appid: str = None
    ) -> dict:
        """
        完整骨龄评估流程（路径B）：注册→登录→上传→骨龄+身高预测
        """
        # Step 1: 注册
        reg_result = self.register()
        if not reg_result.get("ret"):
            pass

        # Step 2: 登录
        login_result = self.login(username, password_hash)
        if not login_result.get("ret"):
            return {"error": "登录失败", "detail": login_result}

        # Step 3: 获取上传URL
        file_name = os.path.basename(image_path)
        upload_result = self.get_upload_url(file_name)
        if not upload_result.get("ret"):
            return {"error": "获取上传URL失败", "detail": upload_result}

        signed_url = upload_result.get("data", {}).get("signedUrl", "")

        # Step 4: 上传图片
        if not self.upload_image(signed_url, image_path):
            return {"error": "图片上传失败"}

        # Step 5: AI骨龄推算+身高预测（路径B）
        assess_result = self.bone_age_assessment(
            sex=sex, age=age, height=height, weight=weight,
            father_height=father_height, mother_height=mother_height,
            phone=phone, file_name=file_name, name=name,
            has_m=has_m, moon_age=moon_age, appid=appid
        )

        return assess_result


def main():
    parser = argparse.ArgumentParser(description="慧龄云®中华05骨龄检测 API 客户端")
    parser.add_argument("--host", required=True, help="慧龄云®API服务器地址，如 https://www.pipitu.net")
    parser.add_argument("--username", required=True, help="登录账号")
    parser.add_argument("--password-hash", required=True, help="SHA256加密后的密码")
    parser.add_argument("--image", help="X光片图片路径")
    parser.add_argument("--sex", choices=["M", "F"], help="性别：M男/F女")
    parser.add_argument("--age", type=float, help="年龄（岁），路径B必填")
    parser.add_argument("--height", type=float, help="身高（cm），路径B必填")
    parser.add_argument("--weight", type=float, help="体重（kg），路径B必填")
    parser.add_argument("--father-height", type=float, help="父亲身高（cm），路径B必填")
    parser.add_argument("--mother-height", type=float, help="母亲身高（cm），路径B必填")
    parser.add_argument("--phone", help="手机号码，路径B必填")
    parser.add_argument("--name", default="匿名", help="患者姓名")
    parser.add_argument("--has-m", choices=["yes", "no"], help="是否有初潮（女性必填）")
    parser.add_argument("--moon-age", type=float, help="初潮年龄")
    parser.add_argument("--appid", help="微信小程序appid（可选，用于消息推送）")
    parser.add_argument("--full", action="store_true", help="使用完整路径B（骨龄+身高预测），默认为路径A（仅骨龄识别）")
    parser.add_argument("--login-only", action="store_true", help="仅测试登录")
    parser.add_argument("--history", action="store_true", help="查询历史报告")

    args = parser.parse_args()
    client = BoneAgeAPIClient(host=args.host)

    if args.login_only:
        client.register()
        result = client.login(args.username, args.password_hash)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 历史报告查询
    if args.history:
        client.register()
        client.login(args.username, args.password_hash)
        result = client.get_history_reports()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 需要图片和性别
    if not args.image or not args.sex:
        print("错误：骨龄检测需要 --image（X光片路径）和 --sex（性别）参数", file=sys.stderr)
        sys.exit(1)

    if args.full:
        # 路径B：完整评估（骨龄+身高预测）
        missing = []
        for field, label in [
            ("age", "年龄"),
            ("height", "身高"),
            ("weight", "体重"),
            ("father_height", "父亲身高"),
            ("mother_height", "母亲身高"),
            ("phone", "手机号码"),
        ]:
            if not getattr(args, field, None):
                missing.append(label)
        if missing:
            print(f"错误：完整路径缺少必要参数：{', '.join(missing)}", file=sys.stderr)
            sys.exit(1)

        result = client.full_assessment(
            username=args.username,
            password_hash=args.password_hash,
            image_path=args.image,
            sex=args.sex,
            age=args.age,
            height=args.height,
            weight=args.weight,
            father_height=args.father_height,
            mother_height=args.mother_height,
            phone=args.phone,
            name=args.name,
            has_m=args.has_m,
            moon_age=args.moon_age,
            appid=args.appid
        )
    else:
        # 路径A：仅骨龄识别（默认）
        result = client.full_detect(
            username=args.username,
            password_hash=args.password_hash,
            image_path=args.image,
            sex=args.sex
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
