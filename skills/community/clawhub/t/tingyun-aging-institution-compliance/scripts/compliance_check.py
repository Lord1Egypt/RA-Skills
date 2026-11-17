#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compliance_check.py — 养老机构运营合规自查与测算工具（零依赖标准库）

用途：
    把养老机构的六类检查项落成可勾选的三态判定骨架，
    测算护理员分档配比缺口、生成证书到期预警、
    输出整改优先级与归档目录建议。

    定位：对照自查辅助工具。
    不出具合规合格结论，不替代民政/消防/住建部门认定，不代办任何许可。

用法：
    python compliance_check.py --init
    python compliance_check.py --input institution.json
    python compliance_check.py --input institution.json --json
    python compliance_check.py --input institution.json --staffing-only
    python compliance_check.py --input institution.json \
        --ratio-selfcare 8 --ratio-partial 5 --ratio-full 4

输入 JSON 结构（示例数据，非真实机构）：
    {
      "institution": {
        "name": "示例养老院",
        "beds_total": 150,
        "residents_by_level": {"自理": 60, "半失能": 50, "全失能": 40},
        "staff": {
          "nursing_total": 18, "nursing_certified": 15,
          "kitchen_total": 6, "kitchen_health_cert": 5,
          "fire_control_room_certified": 2, "security_fire_certified": 1
        }
      },
      "standards": {
        "ratio_selfcare": 10, "ratio_partial": 6, "ratio_full": 3
      },
      "certificates": [
        {"holder": "张三", "type": "养老护理员培训合格证",
         "expires": "2026-12-31", "on_duty": true}
      ]
    }

字段说明：
    institution.name                    机构名称
    institution.beds_total              床位总数（可选）
    institution.residents_by_level       护理等级人数 {"自理": n, "半失能": n, "全失能": n}
    institution.staff.nursing_total     养老护理员总数（可选）
    institution.staff.nursing_certified 其中持养老护理员培训合格证的人数（可选）
    institution.staff.kitchen_total     食堂从业人员总数（可选）
    institution.staff.kitchen_health_cert  其中持有效健康证明的人数（可选）
    institution.staff.fire_control_room_certified 消防控制室持证值班人数（可选）
    institution.staff.security_fire_certified    安保持消防设施操作员证人数（可选）
    standards.ratio_selfcare            自理老人配比分母（默认 10）
    standards.ratio_partial             半失能配比分母（默认 6）
    standards.ratio_full                全失能配比分母（默认 3）
    certificates                        证书列表，可选，用于到期预警
      holder / type / expires(YYYY-MM-DD) / on_duty(bool)

标准与口径来源（写入报告尾部，便于回溯）：
    GB48013-2026《养老机构基本规范》        2026-07-30 发布，2027-08-01 实施，设 1 年过渡期
    GB48014-2026《养老机构重大事故隐患判定准则》25 条直接判定要素 / 28 条综合判定要素 / 2 类排除情形
    辽宁省民政厅《安全隐患检查事项清单》    2026-10-29，64 项（33 必查 + 31 抽查）
    护理员配比 1:10 / 1:6 / 1:3             耒阳市公办养老机构集中供养项目口径
"""

import json
import math
import os
import sys
from datetime import date, datetime

# Windows 控制台编码兜底
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
except Exception:
    pass


# ---------------------------------------------------------------------------
# 64 项检查项库（6 大类）
# 结构：类名 -> [(检查项目, 检查事项, 检查依据, 是否必查), ...]
# 依据原文保留书名与文号，便于回溯核对。
# ---------------------------------------------------------------------------

CHECKLIST = [
    ("建筑、燃气、用电和特种设备安全", [
        ("建设情况", "养老机构是否按照基本建设程序办理用地、规划、建设、验收等手续，是否擅自投入使用或改变建筑使用功能，是否违规改扩建。",
         "《土地管理法》《城乡规划法》《建筑法》《消防法》", False),
        ("场所安全", "养老机构是否设置在C级或D级危房的建筑内。",
         "GB48014-2026", True),
        ("场所安全", "投入使用的自建房是否取得房屋安全鉴定合格证明。",
         "国办发明电〔2022〕10号", True),
        ("场所安全", "养老机构墙体或临近山坡挡土墙是否出现裂缝、变形、风化、空鼓等现象；是否出现地基沉降。",
         "GB55022-2021", False),
        ("燃气安全", "是否依法建立健全燃气安全管理制度。",
         "《城镇燃气管理条例》（国务院令第583号）", False),
        ("燃气安全", "是否使用合格的液化石油气瓶、调压器、连接软管、灶具等燃气具及配件，是否按规定要求设置燃气泄漏报警、自动切断装置。",
         "安委〔2023〕3号；GB55009-2021；GB48013-2026；GB48014-2026", False),
        ("用电安全", "是否使用老旧、“三无”、无CCC认证延长线插座。",
         "民发〔2023〕37号；GB48013-2026；GB48014-2026", True),
        ("特种设备安全", "特种设备使用单位是否办理使用登记并取得证书，登记标志是否置于该特种设备的显著位置。",
         "《特种设备安全法》；GB48013-2026", True),
        ("特种设备安全", "特种设备使用单位是否建立特种设备安全技术档案。",
         "《特种设备安全法》", False),
        ("特种设备安全", "是否对特种设备进行经常性维护保养和定期自行检查，是否对安全附件、安全保护装置进行定期校验、检修，并记录。",
         "《特种设备安全法》；GB48013-2026；GB48014-2026", True),
        ("特种设备安全", "是否在检验合格有效期届满前一个月向特种设备检验机构提出定期检验要求。",
         "《特种设备安全法》", False),
    ]),
    ("消防安全", [
        ("装饰装修", "是否使用易燃可燃夹芯彩钢板。",
         "《消防法》；GB48013-2026；GB48014-2026", True),
        ("装饰装修", "房间顶棚和屋面是否采用易燃可燃材料。",
         "《消防法》；GB48013-2026；GB48014-2026", True),
        ("装饰装修", "外墙外保温和外立面装饰是否采用易燃可燃材料。",
         "《消防法》；GB48014-2026", True),
        ("防火分隔", "老年人居室是否按要求采用不燃性墙体分隔，是否分隔至梁、楼板或屋面板的底面基层。",
         "GB48013-2026；GB48014-2026", True),
        ("防火分隔", "电缆井是否进行防火封堵。",
         "《消防法》；GB48013-2026；GB48014-2026", True),
        ("消防设施及用电设备", "消防设施是否停用失效。",
         "《消防法》；GB48013-2026；GB48014-2026", True),
        ("值班值守", "消防控制室是否存在值班脱岗、无证上岗。",
         "GB25506-2010；GB48013-2026；GB48014-2026", True),
        ("安全疏散和避难逃生", "是否按要求设置避难间及安全疏散设施。",
         "国办函〔2026〕14号；GB48013-2026；GB48014-2026", True),
        ("安全疏散和避难逃生", "新建、改扩建的养老机构是否建立中度和重度失能老年人生活单元、照料单元安全防护体系。",
         "国办函〔2026〕14号", True),
        ("预案制定和演练", "是否按要求制定灭火和应急疏散预案，是否常态化开展针对性消防演练。",
         "公安部令第61号；GB48013-2026；GB48014-2026", True),
    ]),
    ("食品安全", [
        ("食品安全主体责任落实", "食堂、承包经营企业是否取得合法有效的食品经营许可证；是否与承包经营企业依法签订合同。从供餐单位订餐的，是否从取得食品生产经营许可的供餐单位订购，并按照要求对订购的食品进行查验。",
         "《食品安全法》；《食品安全法实施条例》（国务院令第721号）；市场监管总局令第98号", False),
        ("食品安全主体责任落实", "是否依法配备具备食品安全管理能力的食品安全总监、食品安全员；是否对二人进行法律、法规、规章、标准和专业知识培训、考核。",
         "市场监管总局令第98号", False),
        ("食品安全主体责任落实", "是否落实自查要求，制定并有效执行《食品安全风险管控清单》，建立健全日管控、周排查、月调度工作制度和机制，对应形成《每日食品安全检查记录》《每周食品安全排查治理报告》《每月食品安全调度会议纪要》并存档备查。",
         "市场监管总局令第98号", True),
        ("从业人员管理情况", "是否落实从业人员每日健康状况检查（晨检）制度；从业人员是否每年进行健康检查，持有合法有效的健康证明后上岗工作，并对健康证明进行公示；是否组织开展从业人员培训考核并做好培训记录。",
         "《食品安全法》；GB31654-2021", True),
        ("从业人员管理情况", "是否严格落实从业人员卫生要求，进入食品处理区穿戴清洁工作衣帽，洗净手部，不留长指甲、涂指甲油、化妆、佩戴外露饰物；专间和专用操作区内的从业人员操作时是否佩戴清洁的口罩，能遮住口鼻，清洗消毒手部。",
         "GB31654-2021", True),
        ("食品原料控制", "是否严格执行食品、食品添加剂、食品相关产品进货查验记录制度，是否按规定查验并留存供货者的许可资质证明复印件、产品合格证明文件，确保货票相符；是否现场检查食品原料感官性状无异常、包装和标签标识等符合要求。",
         "《食品安全法》；GB31654-2021", True),
        ("食品原料控制", "食品原料、半成品、成品以及非食品是否混放；贮存过程中是否离地、离墙，符合食品安全所需的温度、湿度等要求；冷冻（藏）设施设备是否有可正确显示内部温度的测温装置；冷冻（藏）温度是否符合食品安全要求；需冷冻（藏）的食品是否按要求及时冷冻（藏）；散装食品（食用农产品除外）贮存位置是否标明名称、生产日期或批号、使用时限等信息；食品贮存区是否存放有毒有害物质和感官性状异常、超过保质期、来源不明的食品及原料；食品添加剂是否专柜（位）贮存并标注“食品添加剂”字样。",
         "《食品安全法》；《食品安全法实施条例》；GB31654-2021", True),
        ("加工制作过程控制", "是否具有与其加工制作的食品品种、数量相适应的加工场所及设施设备等；食品原料、半成品、成品及其盛放容器和各类清洗水池、加工制作工具是否区分标识明显、分开放置和使用；防止食品交叉污染的措施是否有效。专间及专用操作区内的标识、人员卫生及操作是否符合要求，使用的食品容器、工具、设备和清洁工具是否保持清洁并专用。",
         "《食品经营许可审查通则》（市场监管总局公告2024年第12号）；GB31654-2021", True),
        ("加工制作过程控制", "是否严格控制食品加工制作温度、时间等关键参数，确保食品烧熟煮透。是否按要求进行食品留样。",
         "《食品安全法实施条例》；GB31654-2021", True),
        ("加工制作过程控制", "是否在加工环节违法使用有毒有害物质和非食品原料；是否采购、贮存、使用亚硝酸盐等国家禁止在餐饮业使用的食品添加剂品种；是否按规定使用食品添加剂，并记录食品添加剂使用情况。",
         "《食品安全法》；GB31654-2021", True),
        ("加工制作过程控制", "供餐单位供餐的，供餐单位是否具备符合贮存、运输要求的设施设备；食品的传送电梯、配送车辆、存放食品的车厢或配送箱（包）、与食品直接接触的配送容器及配送过程是否符合要求；配送过程中，食品的盛放容器是否密闭，食品容器上标注信息是否符合要求。",
         "《食品安全法实施条例》；GB31654-2021", True),
        ("场所环境卫生情况", "场所和设施设备是否布局合理、能正常使用；是否保持场所建筑结构完好、环境整洁、防止病媒生物侵入及滋生；墙壁、天花板、门窗、地面、排水沟、操作台、食品加工用具等是否破损、积油、积水，有霉斑、污垢等。",
         "GB31654-2021", False),
        ("场所环境卫生情况", "是否配齐配全防尘，防蝇、防鼠、防虫等病媒生物防制设施设备；是否定期开展鼠（虫）害等病媒生物消杀，并做好记录；是否存在明显的病媒生物活动迹象；是否设置专用的废弃物存放设施，并加盖、设置明显的区分标识，及时清除不溢出。",
         "GB31654-2021", True),
        ("餐饮具清洗消毒情况", "是否设置独立的洗消间或隔断场所，并配备专用清洗消毒水池、保洁设施，标有明显标识；使用的洗涤剂、消毒剂等食品相关产品是否符合相关国家标准；采用物理消毒的，消毒设施是否运转正常且满足需要；采用化学消毒的，消毒液使用、配制等符合要求；保洁设施是否符合相关要求，存放的餐饮具是否清洁。使用统一消毒或配送餐饮具服务的，是否查验其消毒资质，每批次索取并留存消毒合格证明。",
         "《食品安全法》；《食品安全法实施条例》；GB31654-2021", True),
    ]),
    ("防汛安全", [
        ("选址评估", "是否位于蓄滞洪区内，是否依照防洪法规定办理洪水影响评价许可并按许可实施建设，是否纳入属地蓄滞洪区运用预案，是否纳入属地防汛应急预案。",
         "《防洪法》；水防〔2024〕300号", False),
        ("选址评估", "是否处于山洪灾害危险区、河流洪水威胁区、城市内涝易发区，是否纳入属地防汛应急预案。是否存在洪水冲击、淹没风险。",
         "国办函〔2026〕14号；GB48013-2026；GB48014-2026", False),
        ("选址评估", "是否处于地质灾害易发区，对灾害事故高风险区域内已建成的养老机构，分类采取防护加固措施或搬迁。",
         "国办函〔2026〕14号；GB48013-2026；GB48014-2026", False),
        ("应急准备", "是否编制养老机构防汛应急预案，是否建立人员转移避险台账，明确转移避险责任人、转移条件、转移方式、安置地点等，是否对失能老年人等重点人员落实“一对一”转移措施，是否每年开展1次突发事件应急演练。",
         "GB48013-2026；GB48014-2026", False),
        ("应急准备", "是否建立应急救援队伍，是否与当地应急救援队伍建立联系机制，明确联系人、联系方式等。是否配备救生衣等必要的应急物资。是否按要求设置无障碍通道等安全疏散设施，配备担架、轮椅、呼救器等安全疏散辅助器材。",
         "国办函〔2026〕14号；《中共中央办公厅 国务院办公厅关于进一步提升基层应急管理能力的意见》", False),
        ("应急准备", "是否建立防汛责任制，是否落实属地政府、行业主管部门的防汛包保责任人，是否落实养老机构防汛安全责任人，是否建立汛期应急值守机制，明确带班领导和工作人员。",
         "《中共中央办公厅 国务院办公厅关于进一步提升基层应急管理能力的意见》；民发〔2025〕32号", False),
        ("应急准备", "是否建立健全属地政府、行业主管部门和养老机构的预警“叫应”机制，明确预警传递渠道和养老机构接收人员、反馈方式等。",
         "《中共中央办公厅 国务院办公厅关于进一步提升基层应急管理能力的意见》；民发〔2025〕32号", False),
        ("应急准备", "是否开展汛期风险隐患排查，行业主管部门、养老机构对度汛隐患是否进行全面自查自改，是否建立包括山洪、河流洪水、城市内涝和地质等灾害的风险隐患清单。",
         "国办函〔2026〕14号", False),
    ]),
    ("服务质量安全", [
        ("运营秩序", "是否依法登记、备案；备案信息是否与养老机构实际情况相符。",
         "《养老机构管理办法》（民政部令第66号）", False),
        ("运营秩序", "是否建立制定服务标准和工作流程，并予以公开。",
         "《养老机构管理办法》（民政部令第66号）", False),
        ("运营秩序", "是否与老年人或其代理人签订服务协议。是否建立入院评估制度，对老年人身心状况进行评估，根据评估结果确定照料护理等级。",
         "《养老机构管理办法》（民政部令第66号）", True),
        ("服务档案", "是否建立老年人信息档案和健康档案，收集和妥善保管服务协议等相关资料；档案的保管期限是否不少于服务协议期满后五年。",
         "《养老机构管理办法》（民政部令第66号）；GB48013-2026", False),
        ("服务档案", "是否在各出入口、接待大厅、值班室、楼道、食堂等公共场所安装视频监控设施，监控视频图像是否保存不少于30天。",
         "《养老机构管理办法》（民政部令第66号）；GB48013-2026", False),
        ("服务档案", "是否公开投诉处理电话和安全责任人信息，投诉是否由专人负责处理、反馈，留存记录。",
         "GB48013-2026", False),
        ("从业人员", "是否配备与服务和运营相适应的工作人员，依法与其签订聘用合同或劳动合同。从事医疗、康复、消防等服务的人员，是否具备相应的职业资格。",
         "《养老机构管理办法》（民政部令第66号）；GB48013-2026", False),
        ("从业人员", "提供直接护理服务的养老护理员与老年人配备比例是否不低于相关要求。",
         "GB48013-2026；GB48014-2026", False),
        ("从业人员", "养老护理员是否经培训合格后上岗。从业人员是否至少每半年接受1次岗位安全、职业安全教育，且考核合格率不低于80％。",
         "GB38600-2019；GB48013-2026；GB48014-2026", True),
        ("服务规范", "是否按照“九防”相关服务安全基本规范，提供照料护理服务。",
         "《养老机构服务安全基本规范》（GB38600-2019）", True),
        ("服务规范", "是否专人管理易燃易爆、有毒有害、尖锐物品以及吸烟火种。",
         "《养老机构服务安全基本规范》（GB38600-2019）；GB48013-2026；GB48014-2026", True),
        ("服务规范", "是否对老年人居住和公共区域进行卫生清洁并消毒，保持无异味、地面无积水；是否每日至少打扫1次卫生间，厕位及周边无水渍、污渍。",
         "GB48013-2026", True),
        ("服务规范", "从业人员是否存在态度恶劣、冷漠、欺辱、殴打、谩骂、虐待老年人等行为。",
         "《养老机构管理办法》（民政部令第66号）", True),
        ("服务规范", "养老机构是否每年开展不少于1次的服务满意度测评。",
         "GB48013-2026", False),
        ("服务规范", "使用保护性约束器具，是否遵照医嘱，是否与老年人或相关第三方签署知情同意书，按照操作规范执行。",
         "《养老机构老年人保护性约束服务规范》（GB/T46911-2025）", False),
        ("服务规范", "老年人在机构突发危重疾病或受伤后，养老机构是否及时转送医疗机构救治并及时通知代理人或紧急联系人。",
         "《养老机构管理办法》（民政部令第66号）", False),
    ]),
    ("资金安全", [
        ("收费管理", "采用预收费方式的养老机构，是否按照有关要求收取、管理、使用、退还预收资金等。收取押金、会员费的养老机构，是否开设专用存款账户。",
         "民发〔2024〕19号；民办发〔2025〕9号", False),
        ("资金管理", "是否制定财务管理制度，运营补贴、建设补贴、政府购买服务等资金管理使用是否合规；公办养老机构资金管理使用是否存在违规情况。",
         "国办发〔2020〕48号", False),
        ("收费管理", "是否依照其登记类型、经营性质、运营方式、设施设备条件、管理水平、服务质量、照料护理等级等因素确定服务项目的收费标准，并遵守国家和地方政府价格管理有关规定。是否在醒目位置公示各类服务项目收费标准和收费依据，接受社会监督。",
         "《养老机构管理办法》（民政部令第66号）", False),
        ("收费管理", "是否以承诺还本付息、给予其他投资回报等方式，诱导老年人或其代理人交纳预收费。",
         "民发〔2024〕19号；民办发〔2025〕9号", True),
        ("资金管理", "申领和使用奖补贴资金、项目资金等是否符合有关规定，是否存在虚报冒领、骗取套取、违规使用等问题。",
         "国办发〔2020〕48号", False),
    ]),
]

# 三态取值
STATES = ("符合", "不符合", "需人工确认")

# 整改优先级规则：
#   P0 = 必查 且 依据含 GB48014（直接判定要素覆盖范围）
#   P1 = 必查
#   P2 = 抽查
#   P3 = 由 --extra-p3 指定的自定义观察项（默认空）
P0_HINT = "必查项且依据含 GB48014，命中直接判定要素范围"

# 三本台账（集中用餐单位，市场监管总局令第98号）
LEDGER_DOCS = [
    ("《每日食品安全检查记录》", "日管控", "每日",
     "未发现问题也要记录，实行零风险报告"),
    ("《每周食品安全排查治理报告》", "周排查", "每周",
     "问题内容 + 整改措施 + 完成时限 + 复查结果"),
    ("《每月食品安全调度会议纪要》", "月调度", "每月",
     "负责人月度调度与复盘记录"),
]

# 归因到 GB48013 七个方面（据地方清单条目与国标方面的对应关系推导，用于差距归类）
GB48013_ASPECTS = {
    "建设情况": "选址与建筑",
    "场所安全": "选址与建筑",
    "燃气安全": "设施与设备",
    "用电安全": "设施与设备",
    "特种设备安全": "设施与设备",
    "装饰装修": "设施与设备",
    "防火分隔": "设施与设备",
    "消防设施及用电设备": "设施与设备",
    "值班值守": "安全管理",
    "安全疏散和避难逃生": "设施与设备",
    "预案制定和演练": "安全管理",
    "食品安全主体责任落实": "运营管理",
    "从业人员管理情况": "安全管理",
    "食品原料控制": "基础服务",
    "加工制作过程控制": "基础服务",
    "场所环境卫生情况": "基础服务",
    "餐饮具清洗消毒情况": "基础服务",
    "选址评估": "选址与建筑",
    "应急准备": "安全管理",
    "运营秩序": "运营管理",
    "服务档案": "入院出院管理",
    "从业人员": "安全管理",
    "服务规范": "基础服务",
    "收费管理": "运营管理",
    "资金管理": "运营管理",
}

DISCLAIMER = (
    "本表为依据公开标准与地方检查清单编制的对照自查辅助材料，用于帮助机构梳理自查要点、"
    "准备证据、跟踪整改。不构成法律意见，不出具合规合格结论。检查结论由民政、消防、"
    "住建等主管部门依法作出。地方检查清单以辽宁省民政厅 2026-10-29 版为示例，各地条目数、"
    "分类与必查/抽查划分不同，使用前须替换为本地区主管部门现行清单。标准的具体条款以正式"
    "发布文本为准。记录应当真实，不得补记、不得编造；发现历史记录缺失应如实说明。"
)

SOURCES = [
    ("GB48013-2026《养老机构基本规范》", "2026-07-30 发布，2027-08-01 实施，设 1 年过渡期，7 方面 90 项要求"),
    ("GB48014-2026《养老机构重大事故隐患判定准则》", "25 条直接判定要素 / 28 条综合判定要素 / 2 类排除情形"),
    ("辽宁省民政厅《安全隐患检查事项清单》", "2026-10-29，64 项（33 必查 + 31 抽查）"),
    ("护理员配比 1:10 / 1:6 / 1:3", "耒阳市公办养老机构集中供养项目口径，须以本地要求为准"),
]


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def flag(note):
    """标记一个项目。"""
    return {"note": note}


def flatten():
    """把分类结构压平成带全局序号的列表。"""
    out = []
    idx = 0
    for cat, items in CHECKLIST:
        for item in items:
            idx += 1
            project, question, basis, must = item
            out.append({
                "no": idx,
                "category": cat,
                "project": project,
                "question": question,
                "basis": basis,
                "must_check": must,
                "aspect": GB48013_ASPECTS.get(project, "运营管理"),
            })
    return out


def priority_of(row):
    """按 必查性 × 后果严重度 定优先级。"""
    if row["must_check"] and "GB48014" in row["basis"]:
        return "P0"
    if row["must_check"]:
        return "P1"
    return "P2"


def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
    except Exception:
        return None


def staffing_calc(inst, ratios):
    """护理员分档配比测算：所需 = Σ (该等级人数 ÷ 该等级配比)，向上取整。"""
    residents = inst.get("residents_by_level") or {}
    rows = []
    total_need = 0
    for level, denom in ratios:
        n = residents.get(level)
        if n is None:
            rows.append({
                "level": level,
                "residents": None,
                "ratio": "1:%s" % denom,
                "need": None,
                "note": "未填写该护理等级人数，需人工确认",
            })
            continue
        need = int(math.ceil(float(n) / float(denom))) if denom > 0 else None
        if need is not None:
            total_need += need
        rows.append({
            "level": level,
            "residents": n,
            "ratio": "1:%s" % denom,
            "need": need,
            "note": "",
        })
    return rows, total_need


def cert_alerts(certs, today):
    """证书到期预警：<=90 天黄，<=30 天橙，已过期红。"""
    out = []
    for c in certs or []:
        exp = parse_date(c.get("expires"))
        if exp is None:
            out.append({
                "holder": c.get("holder", ""),
                "type": c.get("type", ""),
                "expires": c.get("expires", ""),
                "level": "未获取到",
                "days": None,
                "on_duty": bool(c.get("on_duty")),
                "note": "未填写或无法解析有效期，需人工确认",
            })
            continue
        days = (exp - today).days
        if days < 0:
            lvl, note = "红", "已过期，需立即调整排班"
        elif days <= 30:
            lvl, note = "橙", "30 天内到期，需已提交复审/换证申请"
        elif days <= 90:
            lvl, note = "黄", "90 天内到期，需安排复审/换证"
        else:
            lvl, note = "绿", "在有效期内"
        out.append({
            "holder": c.get("holder", ""),
            "type": c.get("type", ""),
            "expires": exp.isoformat(),
            "level": lvl,
            "days": days,
            "on_duty": bool(c.get("on_duty")),
            "note": note,
        })
    return out


def build(data, ratios_override=None, today=None):
    today = today or date.today()
    inst = data.get("institution") or {}
    staff = inst.get("staff") or {}
    std = data.get("standards") or {}
    ov = ratios_override or [None, None, None]

    ratios = [
        ("自理", ov[0] if ov[0] is not None else int(std.get("ratio_selfcare", 10))),
        ("半失能", ov[1] if ov[1] is not None else int(std.get("ratio_partial", 6))),
        ("全失能", ov[2] if ov[2] is not None else int(std.get("ratio_full", 3))),
    ]

    rows = flatten()
    for r in rows:
        r["priority"] = priority_of(r)
        r["result"] = ""          # 三态待填：符合 / 不符合 / 需人工确认
        r["evidence"] = ""        # 证据位置待填
        r["remark"] = ""

    by_cat = []
    for cat, _ in CHECKLIST:
        sub = [r for r in rows if r["category"] == cat]
        must = sum(1 for r in sub if r["must_check"])
        by_cat.append({
            "category": cat,
            "total": len(sub),
            "must": must,
            "spot": len(sub) - must,
            "p0": sum(1 for r in sub if r["priority"] == "P0"),
        })

    staffing_rows, staffing_need = staffing_calc(inst, ratios)

    # 持证缺口的结构性提示（只提示，不作结论）
    staff_flags = []
    nt = staff.get("nursing_total")
    nc = staff.get("nursing_certified")
    if nt is not None and nc is not None and nc < nt:
        staff_flags.append("养老护理员持培训合格证人数少于在岗总数，缺口 %d 人"
                           % (nt - nc))
    kt = staff.get("kitchen_total")
    kh = staff.get("kitchen_health_cert")
    if kt is not None and kh is not None and kh < kt:
        staff_flags.append("食堂从业人员持有效健康证明人数少于总数，缺口 %d 人"
                           % (kt - kh))
    if staffing_need and nt is not None and nt < staffing_need:
        staff_flags.append("在岗护理员 %d 人，分档配比测算需 %d 人，缺口 %d 人"
                           % (nt, staffing_need, staffing_need - nt))
    if nt is not None and nc is not None and nc < staffing_need:
        staff_flags.append("持证护理员 %d 人，少于分档配比测算所需 %d 人"
                           % (nc, staffing_need))

    alerts = cert_alerts(data.get("certificates") or [], today)

    p0 = [r for r in rows if r["priority"] == "P0"]

    return {
        "meta": {
            "generated_on": today.isoformat(),
            "institution": inst.get("name", "未填写机构名称"),
            "beds_total": inst.get("beds_total"),
            "checklist_source": "辽宁省民政厅《安全隐患检查事项清单》2026-10-29（示例口径，须换本地清单）",
            "standards": ["GB48013-2026", "GB48014-2026"],
        },
        "disclaimer": DISCLAIMER,
        "summary": {
            "items_total": len(rows),
            "must_check": sum(1 for r in rows if r["must_check"]),
            "spot_check": sum(1 for r in rows if not r["must_check"]),
            "p0": len(p0),
            "p1": sum(1 for r in rows if r["priority"] == "P1"),
            "p2": sum(1 for r in rows if r["priority"] == "P2"),
        },
        "by_category": by_cat,
        "items": rows,
        "staffing": {
            "rows": staffing_rows,
            "need_total": staffing_need,
            "on_duty_nursing": nt,
            "certified_nursing": nc,
            "flags": staff_flags,
        },
        "certificates": alerts,
        "food_ledgers": [
            {"doc": d, "mechanism": m, "freq": f, "key": k, "status": "待核对"}
            for (d, m, f, k) in LEDGER_DOCS
        ],
        "archive_suggestion": [
            "按 6 大类分册：建筑燃气电气特种设备 / 消防安全 / 食品安全 / 防汛安全 / 服务质量安全 / 资金安全",
            "每册前放目录页：项号 · 类别 · 必查标记 · 三态结论 · 证据页码",
            "扫描件命名：类别-项号-简述-日期（例：消防-05-电缆井封堵-20261018）",
            "整改台账放最前（检查组通常先看整改情况）",
        ],
        "sources": [{"name": n, "note": t} for (n, t) in SOURCES],
    }


# ---------------------------------------------------------------------------
# 文本报告
# ---------------------------------------------------------------------------

def render(res):
    L = []
    m = res["meta"]
    s = res["summary"]
    A = L.append

    A("=" * 72)
    A("养老机构运营合规自查报告")
    A("机构：%s" % m["institution"])
    if m.get("beds_total"):
        A("床位：%s" % m["beds_total"])
    A("生成日期：%s" % m["generated_on"])
    A("标准：%s" % " / ".join(m["standards"]))
    A("清单口径：%s" % m["checklist_source"])
    A("=" * 72)
    A("")
    A("【必读】%s" % res["disclaimer"])
    A("")

    A("-" * 72)
    A("一、总览")
    A("-" * 72)
    A("检查项合计：%d 项（必查 %d / 抽查 %d）"
      % (s["items_total"], s["must_check"], s["spot_check"]))
    A("整改优先级：P0 %d 项 / P1 %d 项 / P2 %d 项"
      % (s["p0"], s["p1"], s["p2"]))
    A("")
    A("分类统计：")
    A("%-32s %6s %6s %6s %6s" % ("类别", "项数", "必查", "抽查", "P0"))
    for c in res["by_category"]:
        A("%-32s %6d %6d %6d %6d"
          % (c["category"], c["total"], c["must"], c["spot"], c["p0"]))
    A("")

    st = res["staffing"]
    A("-" * 72)
    A("二、护理员分档配比测算")
    A("-" * 72)
    A("%-10s %10s %10s %10s" % ("护理等级", "在院人数", "配比", "所需人数"))
    for r in st["rows"]:
        A("%-10s %10s %10s %10s  %s"
          % (r["level"],
             r["residents"] if r["residents"] is not None else "未填写",
             r["ratio"],
             r["need"] if r["need"] is not None else "需人工确认",
             r["note"]))
    A("")
    A("合计所需护理员：%s 人" % (st["need_total"] if st["need_total"] else "需人工确认"))
    A("在岗护理员：%s 人；持培训合格证：%s 人"
      % (st["on_duty_nursing"] if st["on_duty_nursing"] is not None else "未填写",
         st["certified_nursing"] if st["certified_nursing"] is not None else "未填写"))
    if st["flags"]:
        A("")
        A("需关注：")
        for f in st["flags"]:
            A("  - %s" % f)
    else:
        A("")
        A("需关注：未发现结构性格式差异（仍需人工核对实际在岗与持证情况）")
    A("")

    if res["certificates"]:
        A("-" * 72)
        A("三、证书到期预警（<=90天 黄 / <=30天 橙 / 已过期 红）")
        A("-" * 72)
        A("%-14s %-26s %-12s %-6s %-8s" % ("持证人", "证书类型", "到期日", "预警", "剩余天"))
        for c in res["certificates"]:
            A("%-14s %-26s %-12s %-6s %-8s"
              % (c["holder"][:13], c["type"][:25], c["expires"],
                 c["level"], c["days"] if c["days"] is not None else "-"))
            if c["note"]:
                A("      └ %s" % c["note"])
        A("")

    A("-" * 72)
    A("四、食品安全三本台账（市场监管总局令第98号）")
    A("-" * 72)
    for f in res["food_ledgers"]:
        A("%-22s %-8s %-6s  关键点：%s  [%s]"
          % (f["doc"], f["mechanism"], f["freq"], f["key"], f["status"]))
    A("")

    A("-" * 72)
    A("五、逐项判定表（三态待填）")
    A("-" * 72)
    A("填写口径：证据优先 —— 先问能否拿出最近一个完整周期的记录，再判断是否满足依据。")
    A("拿不出记录 → 需人工确认；记录与现场矛盾 → 不符合（更严重，涉及记录真实性）。")
    A("")
    for cat, _ in CHECKLIST:
        A("【%s】" % cat)
        for r in [x for x in res["items"] if x["category"] == cat]:
            A("  %2d. [%s] %s · %s"
              % (r["no"], r["priority"], r["project"], "必查" if r["must_check"] else "抽查"))
            A("      检查：%s" % r["question"])
            A("      依据：%s" % r["basis"])
            A("      归类：%s" % r["aspect"])
            A("      结论：[符合/不符合/需人工确认]        证据位置：______        备注：______")
        A("")

    A("-" * 72)
    A("六、整改台账模板（六字段缺一不闭环）")
    A("-" * 72)
    A("%-4s %-10s %-26s %-24s %-10s %-12s %-14s"
      % ("序", "优先级", "问题描述（事实+位置+时间）", "依据条款", "整改措施（人+动作+时间）",
         "责任人", "完成时限"))
    A("-" * 72)
    A("%-4s %-10s %-26s %-24s %-10s %-12s %-14s"
      % ("1", "P0/P1/P2", "（客观事实，勿写笼统）", "标准号/文号+条目",
         "谁+做什么+何时", "姓名+岗位", "具体日期"))
    A("%-4s %-10s %-26s %-24s %-10s %-12s %-14s"
      % ("2", "", "", "", "", "", ""))
    A("%-4s %-10s %-26s %-24s %-10s %-12s %-14s"
      % ("3", "", "", "", "", "", ""))
    A("")
    A("第七字段（复查结果）：复查人 ____ 复查日期 ____ 复查结论 ____")
    A("  ※ 此项空着视为未闭环 —— 检查组通常重点看这一列。")
    A("")

    A("-" * 72)
    A("七、证据归档建议")
    A("-" * 72)
    for a in res["archive_suggestion"]:
        A("  - %s" % a)
    A("")
    A("  证据三件套（整改后缺一等于没改）：")
    A("    1) 整改前照片（有参照物、能看出位置、有时间信息）")
    A("    2) 同机位整改后照片（前后对比才最有说服力）")
    A("    3) 有签认的复查记录（谁、何日、确认了什么）")
    A("")
    A("  证据四级：A 级有签认系统记录 > B 级签字纸质记录 > C 级带时间地点的照片 > D 级制度文件")
    A("  三条红线：不得补记、不得编造、不得用模板代替真实记录")
    A("")

    A("-" * 72)
    A("八、口径与来源")
    A("-" * 72)
    for src in res["sources"]:
        A("  - %s：%s" % (src["name"], src["note"]))
    A("")
    A("  本地清单口径请替换为所在省市民政（养老服务）主管部门现行清单。")
    A("=" * 72)
    return "\n".join(L)


TEMPLATE = {
    "_说明": "养老机构合规自查输入模板（示例数据，请替换为本机构真实情况）",
    "institution": {
        "name": "示例养老院",
        "beds_total": 150,
        "residents_by_level": {"自理": 60, "半失能": 50, "全失能": 40},
        "staff": {
            "nursing_total": 18,
            "nursing_certified": 15,
            "kitchen_total": 6,
            "kitchen_health_cert": 5,
            "fire_control_room_certified": 2,
            "security_fire_certified": 1
        }
    },
    "standards": {
        "ratio_selfcare": 10,
        "ratio_partial": 6,
        "ratio_full": 3
    },
    "certificates": [
        {"holder": "示例人员A", "type": "养老护理员培训合格证",
         "expires": "2027-03-31", "on_duty": True},
        {"holder": "示例人员B", "type": "消防设施操作员",
         "expires": "2026-11-20", "on_duty": True},
        {"holder": "示例人员C", "type": "健康证明",
         "expires": "2026-10-10", "on_duty": True}
    ]
}


def main():
    args = sys.argv[1:]
    inp = None
    as_json = False
    init = False
    staffing_only = False
    ratios = [None, None, None]

    i = 0
    while i < len(args):
        a = args[i]
        # 归一化 --flag=value 形式，便于统一分支判断
        if a.startswith("--") and "=" in a:
            a_key = a.split("=", 1)[0]
        else:
            a_key = a
        if a_key == "--init":
            init = True
        elif a_key == "--json":
            as_json = True
        elif a_key == "--staffing-only":
            staffing_only = True
        elif a_key == "--input":
            i += 1
            if i >= len(args):
                print("错误：--input 需要一个 JSON 文件路径")
                return 2
            inp = args[i]
        elif a_key == "--ratio-selfcare":
            v, i = _read_int(args, i)
            ratios[0] = v
        elif a_key == "--ratio-partial":
            v, i = _read_int(args, i)
            ratios[1] = v
        elif a_key == "--ratio-full":
            v, i = _read_int(args, i)
            ratios[2] = v
        elif a_key in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            print("未知参数：%s（用 --help 查看用法）" % a)
            return 2
        i += 1

    if init:
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return 0

    if not inp:
        print("错误：需要 --input <文件> 或 --init。用 --help 查看用法。")
        return 2

    if not os.path.exists(inp):
        print("错误：找不到输入文件 %s" % inp)
        return 2

    try:
        with open(inp, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("错误：输入 JSON 解析失败：%s" % e)
        return 2

    ov = ratios
    res = build(data, ratios_override=ov)

    if staffing_only:
        res = {
            "meta": res["meta"],
            "disclaimer": res["disclaimer"],
            "staffing": res["staffing"],
            "certificates": res["certificates"],
        }
        if as_json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print("护理员分档配比测算")
            st = res["staffing"]
            for r in st["rows"]:
                print("  %-8s 在院 %-8s 配比 %-8s 所需 %s"
                      % (r["level"],
                         r["residents"] if r["residents"] is not None else "未填写",
                         r["ratio"],
                         r["need"] if r["need"] is not None else "需人工确认"))
            print("  合计所需：%s 人" % (st["need_total"] or "需人工确认"))
            for f in st["flags"]:
                print("  ! %s" % f)
            for c in res["certificates"]:
                print("  证书 %s / %s 到期 %s -> %s（%s）"
                      % (c["holder"], c["type"], c["expires"], c["level"], c["note"]))
        return 0

    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    return 0


def _read_int(args, i):
    """读取 --flag 的整数值。

    支持两种写法：
        --ratio-selfcare 8     （空格分隔）
        --ratio-selfcare=8     （等号分隔）
    返回 (值, 新的循环下标)。
    """
    a = args[i]
    if "=" in a:
        tail = a.split("=", 1)[1]
        try:
            return int(tail), i
        except ValueError:
            return 10, i
    if i + 1 < len(args):
        try:
            return int(args[i + 1]), i + 1
        except ValueError:
            return 10, i
    return 10, i


if __name__ == "__main__":
    sys.exit(main())
