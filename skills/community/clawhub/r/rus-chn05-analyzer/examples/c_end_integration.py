#!/usr/bin/env python3
"""
C端接入示例 — 慧龄云(R)中华05骨龄智能检测

适用场景：面向家长的骨龄评估App、小程序、Web应用
调用路径：路径B（完整路径 — AI骨龄+身高预测）
核心流程：先调 cosBoneAgeOnLine(AI识别) → 再调 predictHeightByBoneAge(身高预测)

前置要求：
  1. 登录账号（普通用户即可，非会员有限频，VIP无限频）
  2. 安装依赖：pip install requests

限频说明：
  - 非会员：cosBoneAgeOnLine 1次/30分钟，predictHeightByBoneAge 3次/30分钟
  - VIP会员：无限频，精度更高（线性插值法）

用法：
  python c_end_integration.py \\
    --image bone.jpg --sex M --age 10.5 --height 140 \\
    --father-height 175 --mother-height 163 --phone 13800000000
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


class CEndBoneAgeClient:
    """C端骨龄检测客户端 — 完整路径"""

    def __init__(self, host: str):
        self.host = host.rstrip("/")
        self.token = None
        self.user = None
        self.tid = f"TID-{uuid.uuid4().hex[:16].upper()}"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=utf-8"})

    def login(self, username: str, password_hash: str) -> bool:
        """密码登录"""
        resp = self.session.post(
            f"{self.host}/auth/local/login",
            json={"username": username, "password": password_hash}, timeout=15
        )
        result = resp.json()
        if result.get("ret"):
            self.token = result["data"]["token"]
            self.user = result["data"].get("user", {})
            # ⚠️ Header名是"token"，不是"Authorization: Bearer"
            self.session.headers.update({"token": self.token})
            is_vip = self.user.get("enable", False)
            counts = self.user.get("counts", 0)
            print(f"[OK] 登录成功 | VIP: {is_vip} | 剩余次数: {counts}")
            return True
        else:
            print(f"[FAIL] 登录失败: {result.get('msg')}")
            return False

    def upload_image(self, file_name: str, image_path: str) -> bool:
        """获取预签名URL并上传图片"""
        resp = self.session.post(
            f"{self.host}/service/signForBAImageUploadEasy",
            json={"fileName": file_name}, timeout=15
        )
        result = resp.json()
        if not result.get("ret"):
            print(f"[FAIL] 获取上传URL失败: {result.get('msg')}")
            return False

        signed_url = result["data"]["signedUrl"]
        with open(image_path, "rb") as f:
            put_resp = requests.put(signed_url, data=f.read(), timeout=30)
        if put_resp.status_code == 200:
            print(f"[OK] 图片上传成功")
            return True
        else:
            print(f"[FAIL] 上传失败: HTTP {put_resp.status_code}")
            return False

    def ai_detect_bone_age(self, file_name: str, sex: str) -> dict:
        """Step A: AI骨龄识别（内部接口，非会员有限频但免费）"""
        resp = self.session.post(
            f"{self.host}/bmd/v2/cosBoneAgeOnLine",
            json={"fileName": file_name, "sex": sex.upper()}, timeout=45
        )
        result = resp.json()
        if result.get("ret"):
            data = result["data"]
            print(f"[OK] AI骨龄识别: {data.get('bam')}岁, SMS={data.get('sms')}")
            return data
        else:
            print(f"[FAIL] AI识别失败: {result.get('msg')}")
            return None

    def predict_height(
        self, file_name: str, sex: str, age: float, height: float,
        father_height: float, mother_height: float, phone: str,
        stages: list = None, scores: list = None, sms: float = None,
        name: str = "匿名", has_m: str = None, moon_age: float = None
    ) -> dict:
        """Step B: 完整身高预测"""
        params = {
            "fileName": file_name,
            "sex": sex.upper(),
            "age": age,
            "height": height,
            "fatherHeight": father_height,
            "motherHeight": mother_height,
            "telephone": phone,
            "name": name,
        }

        # 如果已有AI识别结果，直传stages/scores/sms（VIP使用插值法精度更高）
        if stages:
            params["stages"] = stages
        if scores:
            params["scores"] = scores
        if sms:
            params["sms"] = sms

        # 女性初潮信息
        if sex.upper() == "F":
            params["hasM"] = has_m or "no"
            if has_m == "yes" and moon_age:
                params["moonAge"] = moon_age

        resp = self.session.post(
            f"{self.host}/bmd/v2/predictHeightByBoneAge",
            json=params, timeout=30
        )
        result = resp.json()
        if result.get("ret"):
            data = result["data"]
            print(f"[OK] 身高预测完成")
            return data
        else:
            print(f"[FAIL] 身高预测失败: {result.get('msg')}")
            return None

    def full_flow(
        self, username: str, password_hash: str, image_path: str,
        sex: str, age: float, height: float,
        father_height: float, mother_height: float, phone: str,
        name: str = "匿名", has_m: str = None, moon_age: float = None
    ) -> dict:
        """C端完整流程：登录→上传→AI识别→身高预测"""
        # Step 1: 登录
        if not self.login(username, password_hash):
            return None

        # Step 2: 上传
        file_name = os.path.basename(image_path)
        if not self.upload_image(file_name, image_path):
            return None

        # Step 3: AI骨龄识别
        ai_result = self.ai_detect_bone_age(file_name, sex)
        if not ai_result:
            return None

        stages = ai_result.get("stages")
        scores = ai_result.get("scores")
        sms = ai_result.get("sms")

        # Step 4: 身高预测（使用AI识别到的stages）
        height_result = self.predict_height(
            file_name=file_name, sex=sex, age=age, height=height,
            father_height=father_height, mother_height=mother_height,
            phone=phone, stages=stages, scores=scores, sms=sms,
            name=name, has_m=has_m, moon_age=moon_age
        )

        return {
            "ai_result": ai_result,
            "height_result": height_result
        }


def generate_full_report(ai_data: dict, height_data: dict, age: float, sex: str) -> str:
    """生成C端完整诊断报告"""
    if not ai_data:
        return "AI骨龄识别失败"

    bam = ai_data.get("bam", "?")
    sms = ai_data.get("sms", "?")
    stages = ai_data.get("stages", [])
    bone_diff = round(bam - age, 2) if isinstance(bam, (int, float)) else "?"

    # 骨龄差值解读
    if isinstance(bone_diff, (int, float)):
        if bone_diff > 2:
            status = "明显超前"
        elif bone_diff > 1:
            status = "偏快"
        elif bone_diff > -1:
            status = "正常"
        elif bone_diff > -2:
            status = "偏慢"
        else:
            status = "明显落后"
    else:
        status = "无法判断"

    bone_names = [
        "桡骨", "尺骨", "掌骨I", "掌骨III", "掌骨V",
        "近节指骨I", "近节指骨III", "近节指骨V",
        "中节指骨III", "中节指骨V",
        "远节指骨I", "远节指骨III", "远节指骨V"
    ]

    report = f"""
{'='*55}
         中华05骨龄AI评估报告（完整版）
{'='*55}

评估方法：中华05标准 (RUS-CHN05计分法)
性    别：{'男' if sex == 'M' else '女'}
实际年龄：{age} 岁

━━━━━━━━━━━━ 骨龄评估 ━━━━━━━━━━━━

骨龄：{bam} 岁
骨龄差值：{bone_diff} 岁 → 发育状态：{status}
骨成熟度评分 (SMS)：{sms} (满分1000)

━━━━━━━━━━━━ 骨骼发育等级 ━━━━━━━━━━━━
"""
    if stages and len(stages) >= 13:
        for i, name in enumerate(bone_names):
            report += f"  {name:12s}：等级 {stages[i]}\n"

    # 身高预测部分
    if height_data:
        cmhc = height_data.get("preHeightCMHC", "?")
        fphc = height_data.get("preHeightFPHC", "?")
        chn05 = height_data.get("preHeightCHN05", "?")
        bcpe_ba = height_data.get("predictBCPEByBoneAge", "?")
        bcpe_age = height_data.get("predictBCPEByAge", "?")
        percents = height_data.get("percentsCHN05", "?")
        order_no = height_data.get("orderNo", "")

        report += f"""
━━━━━━━━━━━━ 身高预测 ━━━━━━━━━━━━

遗传靶身高（CMH-C法）：{cmhc} cm
遗传靶身高（FPH-C法）：{fphc} cm
中华05预测成年身高：   {chn05} cm
按骨龄预测身高（BCPE）：{bcpe_ba} cm
按年龄预测身高（BCPE）：{bcpe_age} cm
骨龄百分位：           {percents}%
"""
        if order_no:
            report += f"""
━━━━━━━━━━━━ 在线报告 ━━━━━━━━━━━━
https://www.pipitu.net/RUSCHNAIReport.html?orderNo={order_no}
"""

    report += f"""
━━━━━━━━━━━━ 温馨提示 ━━━━━━━━━━━━
- 骨龄评估误差约+/-1岁，属正常范围
- 如骨龄异常，建议至儿科内分泌科就诊
- 本报告不可作为法律或医疗鉴定依据

⚠️ 免责声明：本报告由AI辅助分析生成，仅供参考，
不构成医疗诊断。如有疑问，请咨询专业医师。
{'='*55}
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="C端接入示例 — 慧龄云骨龄检测（完整路径）")
    parser.add_argument("--host", default=os.getenv("BONE_AGE_API_HOST", "https://www.pipitu.net"))
    parser.add_argument("--username", default=os.getenv("BONE_AGE_USERNAME"))
    parser.add_argument("--password-hash", default=os.getenv("BONE_AGE_PASSWORD_HASH"))
    parser.add_argument("--image", required=True, help="X光片图片路径")
    parser.add_argument("--sex", required=True, choices=["M", "F"], help="性别")
    parser.add_argument("--age", required=True, type=float, help="年龄（岁）")
    parser.add_argument("--height", required=True, type=float, help="当前身高（cm）")
    parser.add_argument("--father-height", required=True, type=float, help="父亲身高（cm）")
    parser.add_argument("--mother-height", required=True, type=float, help="母亲身高（cm）")
    parser.add_argument("--phone", required=True, help="手机号码")
    parser.add_argument("--name", default="匿名", help="患者姓名")
    parser.add_argument("--has-m", choices=["yes", "no"], help="是否有初潮（女性必填）")
    parser.add_argument("--moon-age", type=float, help="初潮年龄")
    args = parser.parse_args()

    if not args.username or not args.password_hash:
        print("错误：请通过 --username/--password-hash 或环境变量提供登录凭证", file=sys.stderr)
        sys.exit(1)

    client = CEndBoneAgeClient(host=args.host)
    result = client.full_flow(
        username=args.username,
        password_hash=args.password_hash,
        image_path=args.image,
        sex=args.sex,
        age=args.age,
        height=args.height,
        father_height=args.father_height,
        mother_height=args.mother_height,
        phone=args.phone,
        name=args.name,
        has_m=args.has_m,
        moon_age=args.moon_age
    )

    if result:
        print(generate_full_report(
            ai_data=result["ai_result"],
            height_data=result.get("height_result"),
            age=args.age,
            sex=args.sex
        ))


if __name__ == "__main__":
    main()
