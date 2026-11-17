#!/usr/bin/env python3
"""
hs_lookup.py — HS 编码查询辅助工具
用法：python hs_lookup.py <关键词> [--detail]
示例：python hs_lookup.py 锂电池
       python hs_lookup.py led 灯 --detail
"""

import sys
import re
import io

# Fix Windows GBK encoding for console output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import requests
except ImportError:
    print("[警告] requests 库未安装，将使用本地参考数据。安装方式：pip install requests")
    USE_LOCAL = True
else:
    USE_LOCAL = False

# 本地 HS 编码参考库（常见品类）
LOCAL_HS_DATABASE = {
    "手机": {"code": "8517.12", "desc": "手机（具有通话功能的移动电话）", "note": "含蜂窝网络通讯功能"},
    "智能手机": {"code": "8517.12", "desc": "智能手机", "note": "含蜂窝网络通讯功能"},
    "锂电池": {"code": "8507.60", "desc": "锂离子蓄电池", "note": "出口需UN38.3测试+危包证"},
    "锂离子电池": {"code": "8507.60", "desc": "锂离子蓄电池", "note": "出口需UN38.3测试+危包证"},
    "充电宝": {"code": "8507.60", "desc": "锂离子蓄电池（便携式移动电源）", "note": "按锂电池管理，注意瓦时数"},
    "变压器": {"code": "8504.32", "desc": "额定容量超过1KVA但不超过16KVA的互感变压器", "note": ""},
    "适配器": {"code": "8504.40", "desc": "静止式变流器", "note": "含电源适配器/充电器"},
    "充电器": {"code": "8504.40", "desc": "静止式变流器（电池充电器）", "note": ""},
    "电线": {"code": "8544.20", "desc": "同轴电缆及其他同轴电导体", "note": ""},
    "电缆": {"code": "8544.49", "desc": "其他电导体，额定电压≤80V", "note": "铜芯/铝芯；有护套/无护套"},
    "连接器": {"code": "8536.69", "desc": "插头及插座，额定电压≤1000V", "note": "含USB/HDMI等连接器"},
    "开关": {"code": "8536.50", "desc": "电路的开关、保护或连接用的电气装置", "note": "手动/感应/遥控开关"},
    "led灯": {"code": "9405.39", "desc": "其他电灯及照明装置", "note": "LED灯具；注意与传统灯具区分"},
    "led灯条": {"code": "9405.39", "desc": "其他电灯及照明装置（LED灯条/灯带）", "note": ""},
    "耳机": {"code": "8518.30", "desc": "耳机、耳塞及头戴送受话器", "note": "有线 vs 蓝牙有子目区分"},
    "蓝牙耳机": {"code": "8518.30", "desc": "耳机（包括蓝牙耳机）", "note": "含无线耳机"},
    "音箱": {"code": "8518.21", "desc": "单喇叭音箱", "note": "含蓝牙音箱；多媒体音箱"},
    "音箱多": {"code": "8518.22", "desc": "多喇叭音箱", "note": ""},
    "显示器": {"code": "8528.52", "desc": "专用于或主要用于自动数据处理系统的监视器", "note": "含液晶显示器"},
    "监视器": {"code": "8528.52", "desc": "专用于自动数据处理系统的监视器", "note": ""},
    "监控摄像头": {"code": "8525.80", "desc": "电视摄像机、数字摄像机", "note": "含网络摄像机（IP Camera）"},
    "路由器": {"code": "8517.62", "desc": "网络通讯设备（路由器/交换机）", "note": ""},
    "交换机": {"code": "8517.62", "desc": "网络通讯设备（交换机）", "note": ""},
    "塑料粒子": {"code": "3901.10", "desc": "初级形状的聚乙烯，比重小于0.94", "note": "PE粒子；LDPE"},
    "聚乙烯": {"code": "3901.10", "desc": "初级形状的聚乙烯（比重<0.94）", "note": ""},
    "聚丙烯": {"code": "3902.10", "desc": "初级形状的聚丙烯", "note": "PP粒子"},
    "abs": {"code": "3903.30", "desc": "初级形状的丙烯腈-丁二烯-苯乙烯共聚物", "note": "ABS粒子"},
    "塑料餐具": {"code": "3924.10", "desc": "塑料制餐具、厨房用具、其他家用制品", "note": "一次性塑料餐具归此类"},
    "塑料盒": {"code": "3923.10", "desc": "塑料制箱、盒、筐（供运输或包装用）", "note": ""},
    "轮胎": {"code": "4011.10", "desc": "机动小客车用新的充气橡胶轮胎", "note": "轿车轮胎"},
    "卡车轮胎": {"code": "4011.20", "desc": "客或货运机动车用新的充气橡胶轮胎", "note": ""},
    "橡胶密封件": {"code": "4016.93", "desc": "硫化橡胶制密封垫、垫片、垫圈", "note": ""},
    "手套乳胶": {"code": "4015.11", "desc": "硫化橡胶制医疗、外科或兽医用手套", "note": "一次性医用手套"},
    "手套": {"code": "4015.19", "desc": "其他硫化橡胶制手套", "note": "非医疗用乳胶手套"},
    "玩具": {"code": "9503.00", "desc": "玩具（玩偶零件、其他玩具、缩小模型等）", "note": "含电子玩具"},
    "毛绒玩具": {"code": "9503.00", "desc": "玩具（毛绒玩具）", "note": ""},
    "拼装玩具": {"code": "9503.00", "desc": "玩具（拼装类）", "note": ""},
    "自行车": {"code": "8712.00", "desc": "自行车及其他非机动自行车", "note": ""},
    "童车": {"code": "8715.00", "desc": "婴孩车及其零件", "note": ""},
    "服装": {"code": "6109.00", "desc": "T恤衫、汗衫及其他内衣纹针织T恤", "note": "棉质T恤；化纤另计"},
    "衬衫": {"code": "6106.20", "desc": "针织或钩编的女式衬衫", "note": ""},
    "鞋": {"code": "6402.19", "desc": "橡胶或塑料制外底及鞋面的其他鞋", "note": "运动鞋/拖鞋/凉鞋"},
    "皮鞋": {"code": "6403.99", "desc": "皮革制外底、皮革或再生皮革制鞋面的鞋靴", "note": ""},
    "布鞋": {"code": "6404.19", "desc": "纺织材料制鞋面、橡胶或塑料外底的鞋", "note": ""},
    "棉纱": {"code": "5205.00", "desc": "棉纱线（缝纫线除外），非供零售用", "note": "精梳/非精梳；支数"},
    "箱包": {"code": "4202.12", "desc": "塑料或纺织材料作面的衣箱、提箱", "note": "布箱/行李箱"},
    "背包": {"code": "4202.92", "desc": "塑料片或纺织材料作面的其他容器", "note": ""},
    "沙发": {"code": "9401.61", "desc": "带软垫的框架座椅（ upholstered seats）", "note": ""},
    "床垫": {"code": "9404.21", "desc": "海绵橡胶或泡沫塑料制褥垫", "note": "乳胶床垫 vs 海绵床垫"},
    "瓷砖": {"code": "6907.21", "desc": "陶瓷砖、瓦、块及类似品（陶瓷贴面砖）", "note": "有釉/无釉；吸水率"},
    "化妆品": {"code": "3304.99", "desc": "其他美容品或化妆品及护肤品", "note": "护肤类"},
    "面膜": {"code": "3304.99", "desc": "美容品或化妆品（面膜）", "note": ""},
    "油漆": {"code": "3208.90", "desc": "涂料及清漆（含溶于水介质的聚合物）", "note": "水性漆"},
    "胶水": {"code": "3506.10", "desc": "适于作胶或粘合剂的零售包装产品", "note": "瞬间胶/结构胶"},
    "不锈钢管": {"code": "7306.40", "desc": "不锈钢制其他圆形截面焊缝管", "note": ""},
    "阀门": {"code": "8481.80", "desc": "龙头、旋塞、阀门及类似装置", "note": "球阀/闸阀/截止阀"},
    "轴承": {"code": "8482.10", "desc": "滚珠轴承", "note": ""},
    "电机": {"code": "8501.10", "desc": "电动机，功率不超过37.5W", "note": "微型电机"},
    "电动机": {"code": "8501.53", "desc": "多相交流电动机，功率超过75W", "note": ""},
}


def search_local(keyword, detail=False):
    """本地数据库模糊搜索"""
    keyword = keyword.lower()
    results = []

    for key, info in LOCAL_HS_DATABASE.items():
        if keyword in key or key in keyword or any(kw in key for kw in keyword.split()):
            results.append((key, info))

    return results


def search_online(keyword):
    """联网查询（调用腾邦HS编码查询API示例）"""
    try:
        # 注意：实际使用时请替换为可用的HS编码查询API
        url = f"https://api.example.com/hs/search?q={keyword}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"[提示] 在线查询失败：{e}，将使用本地数据库。")
    return None


def format_result(results, detail=False):
    """格式化输出结果"""
    if not results:
        return "未找到匹配的HS编码，建议通过海关官网或专业报关行确认。"

    output = []
    for i, (key, info) in enumerate(results, 1):
        output.append(f"  {i}. [{info['code']}] {info['desc']}")
        if detail:
            if info.get('note'):
                output.append(f"     📌 备注：{info['note']}")

    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n[本地数据库] 当前收录品类：", len(LOCAL_HS_DATABASE))
        print("示例关键词：", list(LOCAL_HS_DATABASE.keys())[:10])
        sys.exit(0)

    keyword = " ".join(sys.argv[1:]).strip()
    detail_flag = "--detail" in sys.argv

    print(f"\n🔍 查询关键词：{keyword}")
    print("─" * 50)

    # 本地搜索
    results = search_local(keyword, detail=detail_flag)

    if results:
        print(f"📦 本地数据库匹配结果（{len(results)} 条）：")
        print(format_result(results, detail=detail_flag))
    else:
        print("❌ 本地数据库未找到匹配结果")

    # 联网搜索（如果安装了requests）
    if USE_LOCAL:
        print("\n💡 提示：安装 requests 库后可启用联网查询：")
        print("   pip install requests")
    else:
        online_result = search_online(keyword)
        if online_result:
            print("\n📡 联网查询结果：", online_result)

    # 通用提示
    print("\n⚠️  重要提示：")
    print("   HS编码归类以《中华人民共和国海关进出口税则》为准。")
    print("   涉及金额较大或新产品时，建议委托专业报关行或申请海关预归类决定。")
    print("   联网API需要配置有效的API Key（如需使用）。")


if __name__ == "__main__":
    main()
