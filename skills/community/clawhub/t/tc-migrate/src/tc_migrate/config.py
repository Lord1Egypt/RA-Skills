"""配置文件管理 — YAML 读写 + Pydantic 校验（多 VPC + CCN 云联网，支持跨地域）"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import ValidationError

from .models import DEFAULT_TAGS, MigrateConfig

# 默认配置文件名
DEFAULT_CONFIG_NAME = "tc-migrate.yaml"
DEFAULT_ACCOUNT_NAME = "account.yaml"


# ─────────────────────────── account.yaml 支持 ───────────────────────────

def find_account_file(account_path: Optional[str] = None) -> Optional[Path]:
    """
    查找 account.yaml 路径，优先级：
    1. 显式指定的路径
    2. 环境变量 TC_MIGRATE_ACCOUNT
    3. 当前目录下的 account.yaml
    返回 None 表示未找到（不报错，因为 account.yaml 是可选的）
    """
    if account_path:
        p = Path(account_path)
        if not p.exists():
            raise FileNotFoundError(f"账号文件不存在: {p}")
        return p

    env_path = os.environ.get("TC_MIGRATE_ACCOUNT")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    local = Path.cwd() / DEFAULT_ACCOUNT_NAME
    if local.exists():
        return local

    return None


def load_account_file(account_path: Optional[str] = None) -> Optional[dict]:
    """
    加载 account.yaml 文件，返回字典。

    account.yaml 格式示例：
    ```yaml
    account_a:
      secret_id: AKIDxxx
      secret_key: xxx
      region: ap-beijing
    account_b:
      secret_id: AKIDyyy
      secret_key: yyy
      region: ap-guangzhou
    ```
    """
    path = find_account_file(account_path)
    if path is None:
        return None

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ValueError(f"账号文件格式错误，应为 YAML 字典: {path}")

    return raw


def merge_account_into_config(config_dict: dict, account: dict) -> dict:
    """
    将 account.yaml 中的信息合并到配置字典中。
    account.yaml 的信息只在对应字段为空/占位符时才填入，不会覆盖已有值。

    account.yaml 可提供以下字段（均可选）：
    - account_a.secret_id / secret_key / uin
    - account_b.secret_id / secret_key / uin
    - account_a.region → 填入 config 的 region_a
    - account_b.region → 填入 config 的 region_b
    """
    for label in ("account_a", "account_b"):
        src = account.get(label, {})
        if not src:
            continue
        dst = config_dict.setdefault(label, {})
        # 合并 secret_id / secret_key / uin
        for field in ("secret_id", "secret_key", "uin"):
            src_val = src.get(field, "")
            dst_val = dst.get(field, "")
            if src_val and _is_placeholder(dst_val):
                dst[field] = src_val

    # 合并 region
    for label, region_key in [("account_a", "region_a"), ("account_b", "region_b")]:
        src = account.get(label, {})
        region_val = src.get("region", "")
        if region_val and not config_dict.get(region_key):
            config_dict[region_key] = region_val

    # 合并 target_cidr_block（account.yaml 中的值优先级低于 tc-migrate.yaml）
    acct_target_cidr = account.get("target_cidr_block")
    if acct_target_cidr and not config_dict.get("target_cidr_block"):
        config_dict["target_cidr_block"] = acct_target_cidr

    return config_dict


def get_account_credentials(account_path: Optional[str] = None) -> Optional[dict]:
    """
    从 account.yaml 提取密钥和地域信息，供 config auto 等命令使用。
    返回格式：
    {
      "secret_id_a": "...", "secret_key_a": "...", "region_a": "...",
      "secret_id_b": "...", "secret_key_b": "...", "region_b": "...",
    }
    """
    acct = load_account_file(account_path)
    if acct is None:
        return None

    result = {}
    for label, suffix in [("account_a", "a"), ("account_b", "b")]:
        src = acct.get(label, {})
        if src.get("secret_id"):
            result[f"secret_id_{suffix}"] = src["secret_id"]
        if src.get("secret_key"):
            result[f"secret_key_{suffix}"] = src["secret_key"]
        if src.get("region"):
            result[f"region_{suffix}"] = src["region"]

    # 提取 target_cidr_block
    if acct.get("target_cidr_block"):
        result["target_cidr_block"] = acct["target_cidr_block"]

    return result if result else None


def _is_placeholder(val: str) -> bool:
    """判断一个值是否为空或占位符"""
    if not val:
        return True
    placeholders = ("AKIDx", "AKIDy", "xxxxx", "yyyyy", "<", "PLACEHOLDER", "CHANGE_ME")
    return any(val.startswith(p) for p in placeholders)


def generate_example_account(output_path: str | Path) -> Path:
    """生成示例 account.yaml 文件"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write("# ============================================================\n")
        f.write("# account.yaml — 腾讯云账号密钥文件（敏感信息，请勿提交到 Git）\n")
        f.write("# ============================================================\n")
        f.write("# 此文件独立于 tc-migrate.yaml，存放密钥和地域信息。\n")
        f.write("# CLI 命令会自动从此文件读取密钥，无需在命令行中传入。\n")
        f.write("# \n")
        f.write("# 使用方式：\n")
        f.write("#   1. 编辑此文件，填入真实密钥\n")
        f.write("#   2. 运行 tc-migrate config auto（自动读取 account.yaml）\n")
        f.write("#   3. 或通过 --account-file 指定路径\n")
        f.write("#\n")
        f.write("# 🎯 目标网段自动拆分：\n")
        f.write("#   设置 target_cidr_block 后，程序会自动从该大网段中\n")
        f.write("#   按源端 VPC 大小拆分出等大子网段分配给目标端\n")
        f.write("#   不设置则使用各 VPC 配置中的 account_b_vpc_cidr\n")
        f.write("# ============================================================\n\n")

        yaml.dump(
            {
                "account_a": {
                    "secret_id": "AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "region": "ap-beijing",
                },
                "account_b": {
                    "secret_id": "AKIDyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
                    "secret_key": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
                    "region": "ap-guangzhou",
                },
                "target_cidr_block": "10.0.0.0/8",
            },
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    return path


# ─────────────────────────── tc-migrate.yaml ───────────────────────────

def find_config(config_path: Optional[str] = None) -> Path:
    """
    查找配置文件路径，优先级：
    1. 显式指定的路径
    2. 环境变量 TC_MIGRATE_CONFIG
    3. 当前目录下的 tc-migrate.yaml
    """
    if config_path:
        p = Path(config_path)
        if not p.exists():
            raise FileNotFoundError(f"配置文件不存在: {p}")
        return p

    env_path = os.environ.get("TC_MIGRATE_CONFIG")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p

    local = Path.cwd() / DEFAULT_CONFIG_NAME
    if local.exists():
        return local

    raise FileNotFoundError(
        f"未找到配置文件。请通过 --config 指定，或在当前目录放置 {DEFAULT_CONFIG_NAME}"
    )


def load_config(
    config_path: Optional[str] = None,
    account_path: Optional[str] = None,
) -> MigrateConfig:
    """
    加载并校验配置文件。
    如果存在 account.yaml，自动将密钥信息合并进来（不覆盖已有值）。
    """
    path = find_config(config_path)
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ValueError(f"配置文件格式错误，应为 YAML 字典: {path}")

    # 尝试从 account.yaml 合并密钥信息
    account = load_account_file(account_path)
    if account:
        raw = merge_account_into_config(raw, account)

    try:
        config = MigrateConfig(**raw)
    except ValidationError as e:
        raise ValueError(f"配置校验失败:\n{e}") from e

    # 如果配置了 target_cidr_block，自动从目标网段分配 VPC CIDR
    if config.target_cidr_block:
        config.allocate_target_cidrs()

    return config


def save_config(config: MigrateConfig, output_path: str | Path) -> Path:
    """将配置对象保存为 YAML 文件"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = config.model_dump(mode="json")
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return path


def generate_example_config(output_path: str | Path) -> Path:
    """生成示例配置文件（多 VPC + VPC Peering + CLB/NAT/CVM/SG，含跨地域示例）"""
    example = {
        "region_a": "ap-guangzhou",
        "region_b": "ap-guangzhou",
        "account_a": {
            "secret_id": "AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "uin": "100098765432",
        },
        "account_b": {
            "secret_id": "AKIDyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "secret_key": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
            "uin": "100012345678",
        },
        # 目标网段：在 account.yaml 中设置 target_cidr_block
        # 设置后自动从该大网段中按源端 VPC 大小拆分出等大子网段分配给目标端
        "vpcs": {
            "prod": {
                "account_a_vpc_id": "vpc-prod-xxxx",
                "account_b_vpc_name": "vpc-b-prod",
                "account_b_vpc_cidr": "172.16.0.0/16",
                "account_b_subnets": [
                    {"name": "subnet-prod-web", "cidr": "172.16.1.0/24", "az": "ap-guangzhou-3"},
                    {"name": "subnet-prod-app", "cidr": "172.16.2.0/24", "az": "ap-guangzhou-4"},
                    {"name": "subnet-prod-db", "cidr": "172.16.3.0/24", "az": "ap-guangzhou-6"},
                ],
                "account_b_sg_name": "sg-b-prod",
                "account_b_sg_ingress_cidrs": ["172.16.0.0/16"],
            },
            "dev": {
                "account_a_vpc_id": "vpc-dev-xxxx",
                "account_b_vpc_name": "vpc-b-dev",
                "account_b_vpc_cidr": "172.17.0.0/16",
                "account_b_subnets": [
                    {"name": "subnet-dev-web", "cidr": "172.17.1.0/24", "az": "ap-guangzhou-3"},
                    {"name": "subnet-dev-app", "cidr": "172.17.2.0/24", "az": "ap-guangzhou-4"},
                ],
                "account_b_sg_name": "sg-b-dev",
                "account_b_sg_ingress_cidrs": ["172.17.0.0/16"],
            },
        },
        # ── 扩展资源配置（按产品类型，可选） ──
        "resources": {
            "clb": {
                "enabled": True,
                "instances": {
                    "prod-web-lb": {
                        "name": "prod-web-lb",
                        "load_balancer_type": "OPEN",
                        "vpc_key": "prod",
                        "listeners": [
                            {"protocol": "TCP", "port": 80},
                            {"protocol": "TCP", "port": 443},
                        ],
                    },
                },
            },
            "nat": {
                "enabled": True,
                "gateways": {
                    "prod-nat": {
                        "name": "prod-nat-gw",
                        "vpc_key": "prod",
                        "bandwidth": 200,
                    },
                },
            },
            "cvm": {
                "enabled": True,
                "instances": {
                    "web-server-1": {
                        "name": "prod-web-01",
                        "instance_type": "S5.MEDIUM4",
                        "vpc_key": "prod",
                        "subnet_index": 0,
                        "image_id": "img-eb30mz89",
                        "az": "ap-guangzhou-3",
                        "system_disk": {"type": "CLOUD_PREMIUM", "size": 50},
                        "data_disks": [
                            {"type": "CLOUD_SSD", "size": 100},
                        ],
                    },
                },
            },
            "sg": {
                "enabled": True,
                "security_groups": {
                    "sg-0": {
                        "name": "migrated-prod-web-sg",
                        "description": "Web tier security group migrated from source",
                        "vpc_key": "prod",
                        "ingress_rules": [
                            {"direction": "ingress", "action": "ACCEPT", "protocol": "TCP", "port": "80,443", "cidr_block": "0.0.0.0/0", "description": "Allow HTTP/HTTPS"},
                            {"direction": "ingress", "action": "ACCEPT", "protocol": "TCP", "port": "22", "cidr_block": "10.0.0.0/8", "description": "Allow SSH from internal"},
                            {"direction": "ingress", "action": "DROP", "protocol": "ALL", "port": "ALL", "cidr_block": "0.0.0.0/0", "description": "Default deny"},
                        ],
                        "egress_rules": [
                            {"direction": "egress", "action": "ACCEPT", "protocol": "ALL", "port": "ALL", "cidr_block": "0.0.0.0/0", "description": "Allow all outbound"},
                        ],
                    },
                },
            },
        },
        "tags": DEFAULT_TAGS.copy(),
    }

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# ============================================================\n")
        f.write("# tc-migrate.yaml — 腾讯云跨账号资源迁移配置文件\n")
        f.write("# 方案：CCN 云联网（每对 VPC 独立 CCN + 路由表，隔离性好）\n")
        f.write("# 支持资源：VPC / CLB / NAT / CVM / SG（插件可扩展）\n")
        f.write("# ============================================================\n")
        f.write("# 请将下方示例值替换为真实信息\n")
        f.write("# 注意：secret_id/secret_key 为敏感信息，请勿提交到 Git\n")
        f.write("# vpcs 下的每个 key（如 prod、dev）是 VPC 逻辑名\n")
        f.write("# resources 下按产品类型配置（clb/nat/cvm/sg），可省略不需要的类型\n")
        f.write("# 也可用 tc-migrate scan --save 自动扫描生成 resources 配置\n")
        f.write("#\n")
        f.write("# 🔑 跨地域支持：\n")
        f.write("#   - 如果 A/B 在同一地域，region_a 和 region_b 填相同值\n")
        f.write("#   - 如果需要跨地域 CCN，填不同值（如 region_a: ap-guangzhou, region_b: ap-shanghai）\n")
        f.write("#   - 也可以只写 region 字段（向后兼容，A/B 同地域）\n")
        f.write("#\n")
        f.write("# 🎯 目标网段自动拆分：\n")
        f.write("#   在 account.yaml 中设置 target_cidr_block（如 10.0.0.0/8）\n")
        f.write("#   程序会自动从该大网段中按源端 VPC 大小拆分分配给目标端\n")
        f.write("#   不设置则使用各 VPC 配置中的 account_b_vpc_cidr（默认与源端相同）\n")
        f.write("# ============================================================\n\n")
        yaml.dump(example, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return path
