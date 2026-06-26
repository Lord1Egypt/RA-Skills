#!/usr/bin/env python3
"""
仙宫云 API 调用脚本

封装仙宫云开放平台的所有 API 接口，支持实例管理、私有镜像管理、账号管理等操作。

使用方法:
    python xiangongyun_api.py --action <action> [--params ...]

示例:
    python xiangongyun_api.py --action list_instances
    python xiangongyun_api.py --action get_instance --instance-id abc123
    python xiangongyun_api.py --action deploy_instance --name "my-instance" --gpu-count 1 --image "PyTorch 2.0.0"
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional
import requests
import yaml

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "config.yaml")


def load_config() -> Dict[str, Any]:
    """从 config.yaml 加载配置"""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"配置文件不存在：{CONFIG_FILE}")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# 加载配置
config = load_config()
BASE_URL = config.get("api", {}).get("base_url", "https://api.xiangongyun.com")


class XianGongYunAPI:
    """仙宫云 API 客户端"""

    def __init__(self):
        self.api_key = self._get_api_key()
        self.headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json"
        }

    def _get_api_key(self) -> str:
        """从 config.yaml 获取 API 令牌"""
        api_key = config.get("api", {}).get("access_token")
        if not api_key or api_key == "YOUR_ACCESS_TOKEN_HERE":
            raise ValueError(
                f"缺少仙宫云 API 令牌。请在 {CONFIG_FILE} 中配置有效的 access_token。"
            )
        return api_key

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """发送 HTTP 请求"""
        url = f"{BASE_URL}{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=30)
            else:
                raise ValueError(f"不支持的 HTTP 方法：{method}")

            # 检查 HTTP 状态码
            if response.status_code >= 400:
                raise Exception(
                    f"HTTP 请求失败：状态码 {response.status_code}, "
                    f"响应内容：{response.text}"
                )

            result = response.json()

            # 检查 API 响应状态
            if not result.get("success", True):
                raise Exception(
                    f"API 错误：{result.get('msg', '未知错误')} "
                    f"(code: {result.get('code', 'N/A')})"
                )

            return result

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败：{str(e)}")

    # ==================== 实例管理 API ====================

    def list_instances(self) -> Dict[str, Any]:
        """获取实例列表"""
        return self._request("GET", "/open/instances")

    def get_instance(self, instance_id: str) -> Dict[str, Any]:
        """获取单个实例信息"""
        return self._request("GET", f"/open/instance/{instance_id}")

    def list_instance_images(self, instance_id: str) -> Dict[str, Any]:
        """获取实例储存的镜像"""
        return self._request("GET", f"/open/instance/{instance_id}/images")

    def deploy_instance(
        self,
        name: str,
        gpu_count: int,
        image: str,
        data_center: Optional[str] = None,
        ssh_key: Optional[str] = None,
        password: Optional[str] = None,
        image_id: Optional[str] = None,
        image_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """部署实例"""
        data = {
            "name": name,
            "gpu_count": gpu_count,
            "image": image
        }

        if data_center:
            data["data_center"] = data_center
        if ssh_key:
            data["ssh_key"] = ssh_key
        if password:
            data["password"] = password
        if image_id:
            data["image_id"] = image_id
        if image_type:
            data["image_type"] = image_type

        return self._request("POST", "/open/instance/deploy", data=data)

    def destroy_instance(self, instance_id: str) -> Dict[str, Any]:
        """销毁实例"""
        return self._request("POST", "/open/instance/destroy", data={"id": instance_id})

    def shutdown_instance(self, instance_id: str) -> Dict[str, Any]:
        """关机保留 GPU"""
        return self._request("POST", "/open/instance/shutdown", data={"id": instance_id})

    def shutdown_release_gpu(self, instance_id: str) -> Dict[str, Any]:
        """关机释放 GPU"""
        return self._request(
            "POST", "/open/instance/shutdown_release_gpu", data={"id": instance_id}
        )

    def shutdown_destroy(self, instance_id: str) -> Dict[str, Any]:
        """关机并销毁"""
        return self._request(
            "POST", "/open/instance/shutdown_destroy", data={"id": instance_id}
        )

    def boot_instance(self, instance_id: str) -> Dict[str, Any]:
        """开机"""
        return self._request("POST", "/open/instance/boot", data={"id": instance_id})

    def save_image(self, instance_id: str, image_name: str) -> Dict[str, Any]:
        """储存镜像"""
        return self._request(
            "POST", "/open/instance/saveimage",
            data={"id": instance_id, "image_name": image_name}
        )

    def save_image_destroy(self, instance_id: str, image_name: str) -> Dict[str, Any]:
        """储存镜像并销毁"""
        return self._request(
            "POST", "/open/instance/saveimage_destroy",
            data={"id": instance_id, "image_name": image_name}
        )

    # ==================== 私有镜像 API ====================

    def list_images(self) -> Dict[str, Any]:
        """获取镜像列表"""
        return self._request("GET", "/open/images")

    def get_image(self, image_id: str) -> Dict[str, Any]:
        """获取镜像信息"""
        return self._request("GET", f"/open/image/{image_id}")

    def destroy_image(self, image_id: str) -> Dict[str, Any]:
        """销毁镜像"""
        return self._request("POST", "/open/image/destroy", data={"id": image_id})

    # ==================== 账号 API ====================

    def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        return self._request("GET", "/open/whoami")

    def get_balance(self) -> Dict[str, Any]:
        """获取账户余额"""
        return self._request("GET", "/open/balance")

    def create_recharge_order(self, amount: float, payment: str) -> Dict[str, Any]:
        """创建充值订单"""
        if payment not in ["alipay", "wechat"]:
            raise ValueError("payment 参数必须是 'alipay' 或 'wechat'")
        return self._request(
            "POST", "/open/recharge/order",
            data={"amount": amount, "payment": payment}
        )

    def query_recharge_order(self, trade_no: str) -> Dict[str, Any]:
        """查询充值订单"""
        return self._request("GET", f"/open/recharge/order/{trade_no}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="仙宫云 API 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的操作 (action):
  实例管理:
    list_instances          - 获取实例列表
    get_instance            - 获取单个实例信息 (需要 --instance-id)
    list_instance_images    - 获取实例储存的镜像 (需要 --instance-id)
    deploy_instance         - 部署实例 (需要 --name, --gpu-count, --image)
    destroy_instance        - 销毁实例 (需要 --instance-id)
    shutdown_instance       - 关机保留 GPU (需要 --instance-id)
    shutdown_release_gpu    - 关机释放 GPU (需要 --instance-id)
    shutdown_destroy        - 关机并销毁 (需要 --instance-id)
    boot_instance           - 开机 (需要 --instance-id)
    save_image              - 储存镜像 (需要 --instance-id, --image-name)
    save_image_destroy      - 储存镜像并销毁 (需要 --instance-id, --image-name)

  私有镜像:
    list_images             - 获取镜像列表
    get_image               - 获取镜像信息 (需要 --image-id)
    destroy_image           - 销毁镜像 (需要 --image-id)

  账号管理:
    get_user_info           - 获取用户信息
    get_balance             - 获取账户余额
    create_recharge_order   - 创建充值订单 (需要 --amount, --payment)
    query_recharge_order    - 查询充值订单 (需要 --trade-no)
        """
    )

    parser.add_argument("--action", required=True, help="要执行的操作")
    parser.add_argument("--instance-id", help="实例 ID")
    parser.add_argument("--image-id", help="镜像 ID")
    parser.add_argument("--name", help="实例名称")
    parser.add_argument("--gpu-count", type=int, help="GPU 数量")
    parser.add_argument("--image", help="镜像名称")
    parser.add_argument("--data-center", help="数据中心")
    parser.add_argument("--ssh-key", help="SSH 密钥")
    parser.add_argument("--password", help="密码")
    parser.add_argument("--image-name", help="镜像名称 (保存镜像时使用)")
    parser.add_argument("--amount", type=float, help="充值金额")
    parser.add_argument("--payment", help="支付方式 (alipay/wechat)")
    parser.add_argument("--trade-no", help="交易订单号")

    args = parser.parse_args()

    try:
        api = XianGongYunAPI()

        # 实例管理
        if args.action == "list_instances":
            result = api.list_instances()
        elif args.action == "get_instance":
            if not args.instance_id:
                parser.error("get_instance 需要 --instance-id 参数")
            result = api.get_instance(args.instance_id)
        elif args.action == "list_instance_images":
            if not args.instance_id:
                parser.error("list_instance_images 需要 --instance-id 参数")
            result = api.list_instance_images(args.instance_id)
        elif args.action == "deploy_instance":
            if not args.name or not args.gpu_count or not args.image:
                parser.error("deploy_instance 需要 --name, --gpu-count, --image 参数")
            result = api.deploy_instance(
                name=args.name,
                gpu_count=args.gpu_count,
                image=args.image,
                data_center=args.data_center,
                ssh_key=args.ssh_key,
                password=args.password
            )
        elif args.action == "destroy_instance":
            if not args.instance_id:
                parser.error("destroy_instance 需要 --instance-id 参数")
            result = api.destroy_instance(args.instance_id)
        elif args.action == "shutdown_instance":
            if not args.instance_id:
                parser.error("shutdown_instance 需要 --instance-id 参数")
            result = api.shutdown_instance(args.instance_id)
        elif args.action == "shutdown_release_gpu":
            if not args.instance_id:
                parser.error("shutdown_release_gpu 需要 --instance-id 参数")
            result = api.shutdown_release_gpu(args.instance_id)
        elif args.action == "shutdown_destroy":
            if not args.instance_id:
                parser.error("shutdown_destroy 需要 --instance-id 参数")
            result = api.shutdown_destroy(args.instance_id)
        elif args.action == "boot_instance":
            if not args.instance_id:
                parser.error("boot_instance 需要 --instance-id 参数")
            result = api.boot_instance(args.instance_id)
        elif args.action == "save_image":
            if not args.instance_id or not args.image_name:
                parser.error("save_image 需要 --instance-id, --image-name 参数")
            result = api.save_image(args.instance_id, args.image_name)
        elif args.action == "save_image_destroy":
            if not args.instance_id or not args.image_name:
                parser.error("save_image_destroy 需要 --instance-id, --image-name 参数")
            result = api.save_image_destroy(args.instance_id, args.image_name)

        # 私有镜像
        elif args.action == "list_images":
            result = api.list_images()
        elif args.action == "get_image":
            if not args.image_id:
                parser.error("get_image 需要 --image-id 参数")
            result = api.get_image(args.image_id)
        elif args.action == "destroy_image":
            if not args.image_id:
                parser.error("destroy_image 需要 --image-id 参数")
            result = api.destroy_image(args.image_id)

        # 账号管理
        elif args.action == "get_user_info":
            result = api.get_user_info()
        elif args.action == "get_balance":
            result = api.get_balance()
        elif args.action == "create_recharge_order":
            if not args.amount or not args.payment:
                parser.error("create_recharge_order 需要 --amount, --payment 参数")
            result = api.create_recharge_order(args.amount, args.payment)
        elif args.action == "query_recharge_order":
            if not args.trade_no:
                parser.error("query_recharge_order 需要 --trade-no 参数")
            result = api.query_recharge_order(args.trade_no)

        else:
            parser.error(f"未知的操作：{args.action}")

        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    except ValueError as e:
        print(f"参数错误：{str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"执行失败：{str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
