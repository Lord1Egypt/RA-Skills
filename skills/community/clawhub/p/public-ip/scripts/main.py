"""public_ip skill - 读取外网 IP 地址"""
import sys
import json
import urllib.request
import urllib.error


def parse_args(arg):
    arg = arg.strip()
    if not arg:
        return {"service": "auto"}
    if arg.startswith("{"):
        try:
            params = json.loads(arg)
            params.setdefault("service", "auto")
            return params
        except json.JSONDecodeError as e:
            return {"error": f"JSON 参数解析失败: {e}"}
    return {"service": arg}


def fetch_url(url, timeout=5):
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8").strip()


def get_ip_ipify():
    """通过 ipify 获取 IP"""
    ip = fetch_url("https://api.ipify.org")
    return ip, None


def get_ip_ifconfig():
    """通过 ifconfig.me 获取 IP"""
    ip = fetch_url("https://ifconfig.me/ip")
    return ip, None


def get_ip_myip():
    """通过 myip.com 获取 IP"""
    data = fetch_url("https://api.myip.com")
    obj = json.loads(data)
    return obj.get("ip", ""), obj


def get_ip_info(ip):
    """通过 ip-api 获取 IP 地理位置信息"""
    try:
        data = fetch_url(f"http://ip-api.com/json/{ip}?lang=zh-CN", timeout=5)
        obj = json.loads(data)
        return obj
    except Exception:
        return None


def get_public_ip(service="auto"):
    services = {
        "ipify": get_ip_ipify,
        "ifconfig": get_ip_ifconfig,
        "myip": get_ip_myip,
    }

    ip = None
    extra_info = None
    used_service = ""

    if service != "auto" and service in services:
        try:
            ip, extra_info = services[service]()
            used_service = service
        except Exception as e:
            return f"获取 IP 失败 ({service}): {e}"
    else:
        # 自动尝试
        for name, func in services.items():
            try:
                ip, extra_info = func()
                if ip:
                    used_service = name
                    break
            except Exception:
                continue

        if not ip:
            return """🌐 外网 IP 信息
==================================================
获取外网 IP 失败，可能原因：
1. 网络未连接
2. 防火墙阻止
3. 所有 IP 查询服务不可用"""

    # 获取地理位置
    info = get_ip_info(ip) or {}

    result = ["🌐 外网 IP 信息", "=" * 50]
    result.append(f"IP 地址: {ip}")
    if info:
        country = info.get("country", "未知")
        region = info.get("regionName", "")
        city = info.get("city", "")
        isp = info.get("isp", "未知")
        timezone = info.get("timezone", "未知")
        location = []
        if country:
            location.append(country)
        if region:
            location.append(region)
        if city:
            location.append(city)
        result.append(f"地理位置: {' '.join(location)}")
        result.append(f"ISP: {isp}")
        result.append(f"时区: {timezone}")
        if info.get("lat") and info.get("lon"):
            result.append(f"经纬度: {info['lat']}, {info['lon']}")
    elif extra_info:
        country = extra_info.get("country", "未知")
        result.append(f"地理位置: {country}")
    result.append(f"查询服务: {used_service}")

    return "\n".join(result)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    params = parse_args(arg)
    if "error" in params:
        print(params["error"])
    else:
        print(get_public_ip(params.get("service", "auto")))
