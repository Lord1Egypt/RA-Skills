# dict_04_office_industrial.py
OFFICE_INDUSTRIAL = {
    "智慧办公空间": {
        "description": "高密度脑力劳动、协作与节能导向的生产空间",
        "hardware_matrix": [
            {"element": "电磁", "process": "计算/连接", "name": "LoRaWAN / KNX 企业级群控网关"},
            {"element": "光", "process": "执行", "name": "恒照度自适应照明系统 (靠近窗户自动调暗)"},
            {"element": "光", "process": "感知", "name": "高精度环境光照度传感器"},
            {"element": "气", "process": "执行", "name": "BACnet 协议中央空调/VAV变风量风机对接网关"},
            {"element": "电磁", "process": "感知", "name": "工位级人体存在传感器 (人走灯灭/工位占用统计)"},
            {"element": "能", "process": "感知", "name": "分区/分层智能电表 (能耗碳排放追踪)"},
            {"element": "视", "process": "交互", "name": "企业数字看板与能耗大屏终端"}
        ],
        "default_scenarios": ["上班通勤模式 (照明全开/空调预冷)", "午休模式 (灯光减半/关闭强风)", "下班节能巡检模式"]
    },
    "智能会议室": {
        "description": "聚焦演示、沟通与私密性的高频协同空间",
        "hardware_matrix": [
            {"element": "视", "process": "交互", "name": "门口会议室预约与状态电子墨水屏"},
            {"element": "电磁", "process": "感知", "name": "会议室占用感知雷达 (超时无人自动释放资源)"},
            {"element": "光", "process": "执行", "name": "可调光防眩目会议照明 + 演讲者聚光射灯"},
            {"element": "光", "process": "执行", "name": "电动遮光卷帘 (保护屏幕对比度与隐私)"},
            {"element": "气", "process": "感知", "name": "防缺氧 CO2 探测器 (联动新风防止开会犯困)"},
            {"element": "视", "process": "执行", "name": "无线投屏器与电动升降幕布/摄像头联动模块"}
        ],
        "default_scenarios": ["日常会议模式", "投影演示模式 (灯光调暗/幕布降下)", "头脑风暴模式 (灯光全亮/白板补光)"]
    },
    "智慧仓库": {
        "description": "物资流转、环境苛求与高安防等级的大型空间",
        "hardware_matrix": [
            {"element": "气", "process": "感知", "name": "工业级温湿度阵列传感器 (防货物受潮)"},
            {"element": "气", "process": "感知", "name": "大面积线型光电感烟火灾探测器"},
            {"element": "电磁", "process": "感知", "name": "叉车防撞/UWB 高精度室内定位锚点"},
            {"element": "光", "process": "执行", "name": "高悬挂工矿灯 (雷达感应人车车至亮灯)"},
            {"element": "能", "process": "执行", "name": "重型机械/卷帘门工业智能配电箱"},
            {"element": "视", "process": "感知", "name": "热成像防火摄像头与周界越线监控"}
        ],
        "default_scenarios": ["日常仓储模式 (人车跟随照明)", "恒温恒湿巡检模式", "火警最高级封锁模式"]
    },
    "智慧种植场": {
        "description": "植物生命周期维持、光合作用与水肥精准灌溉的大棚空间",
        "hardware_matrix": [
            {"element": "气", "process": "感知", "name": "土壤传感器 (EC电导率/温湿度/PH值)"},
            {"element": "气", "process": "感知", "name": "大棚环境微气象站 (光照度/CO2/空气温湿度)"},
            {"element": "能", "process": "执行", "name": "水肥一体机/电磁阀联动控制器"},
            {"element": "气", "process": "执行", "name": "大棚卷膜机/天窗双向电机 (通风控温)"},
            {"element": "光", "process": "执行", "name": "特定光谱植物补光灯 (红蓝光比例调配)"},
            {"element": "视", "process": "感知", "name": "病虫害 AI 识别轨道巡检摄像头"}
        ],
        "default_scenarios": ["自动滴灌模式", "强光补光模式", "高温强排风卷膜模式"]
    },
    "智慧工厂车间": {"description": "工业互联网边缘空间", "hardware_matrix": [{"element": "能", "process": "感知", "name": "三相电高精度能耗与电能质量监测仪"}, {"element": "声", "process": "感知", "name": "机械异响/高频振动声纹检测仪"}, {"element": "视", "process": "感知", "name": "安全帽/工作服 AI 合规识别探头"}], "default_scenarios": ["三班倒照明调控", "设备预防性维护预警"]},
    "智慧变电站": {"description": "极高危无人物理设施空间", "hardware_matrix": [{"element": "气", "process": "感知", "name": "SF6/六氟化硫气体泄漏探测器"}, {"element": "视", "process": "感知", "name": "双光谱热成像测温云台"}, {"element": "气", "process": "执行", "name": "防凝露智能除湿机"}], "default_scenarios": ["无人值守巡检", "异常温升紧急排风"]}
}