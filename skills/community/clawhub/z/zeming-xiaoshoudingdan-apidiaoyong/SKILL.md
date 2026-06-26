# 龙虾技能名称：zeming-xiaoshoudingdanhedui
# 功能：钉钉API导入 → 20项展示核对 → A/B/C选择

order_data = {
    "审批编号": "202603220741000009948",
    "所在部门": "办公室-业务部",
    "顾客姓名": "李鸿冰",
    "客户地址": "陕西省西安市港务区西派璟悦一单元1802",
    "联系电话": "18993318889",
    "产品类型": ["洗衣机", "电视"],
    "品牌": ["卡萨帝", "海信"],
    "产品型号": ["CE B10LWDUBHKU1", "75D3K"],
    "订购数量": [1, 2],
    "单价": [5000, 3199],
    "合计金额": [5000, 6398],
    "收回手续": 0,
    "是否开票": "是",
    "交款方式": "电汇",
    "配送方式": "库房送货",
    "是否参与节能补贴": "门店补贴",
    "开发票金额": [5000, 6398],
    "补贴金额": [750, 959.70],
    "订购说明": "咸鱼销售",
    "发起人": "段震"
}

def show_20_items():
    print("===== 钉钉20项指定项目展示 =====")
    print(f"1  审批编号：{order_data['审批编号']}")
    print(f"2  所在部门：{order_data['所在部门']}")
    print(f"3  顾客姓名：{order_data['顾客姓名']}")
    print(f"4  客户地址：{order_data['客户地址']}")
    print(f"5  联系电话：{order_data['联系电话']}")
    print(f"6  产品类型：{'、'.join(order_data['产品类型'])}")
    print(f"7  品牌：{'、'.join(order_data['品牌'])}")
    print(f"8  产品型号：{' / '.join(order_data['产品型号'])}")
    print(f"9  订购数量：{' / '.join(map(str, order_data['订购数量']))}")
    print(f"10 单价(元)：{' / '.join(map(str, order_data['单价']))}")
    print(f"11 合计金额：{' / '.join(map(str, order_data['合计金额']))}")
    print(f"12 收回手续：{order_data['收回手续']}")
    print(f"13 是否开票：{order_data['是否开票']}")
    print(f"14 交款方式：{order_data['交款方式']}")
    print(f"15 配送方式：{order_data['配送方式']}")
    print(f"16 是否参与节能补贴：{order_data['是否参与节能补贴']}")
    print(f"17 开发票金额(元)：{' / '.join(map(str, order_data['开发票金额']))}")
    print(f"18 补贴金额(元)：{' / '.join(map(str, order_data['补贴金额']))}")
    print(f"19 订购说明：{order_data['订购说明']}")
    print(f"20 发起人：{order_data['发起人']}")

    print("\n请选择操作：")
    print("A - 数据完全正确，继续下一步")
    print("B - 数据有错误，重新查询钉钉API")
    print("C - 退出流程")

# 执行展示
show_20_items()

# 龙虾自动跳转规则（已内置）
# 用户选择 A → 自动执行 技能2
# 用户选择 B → 重新执行本技能
# 用户选择 C → 结束