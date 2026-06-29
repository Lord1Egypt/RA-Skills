#!/usr/bin/env python3
"""签证聪明办 — 中国公民出境签证智能指南
Tools: check_visa / visa_checklist / visa_policy_update
"""

import json
import sys
import urllib.request
import urllib.parse
import re
from datetime import datetime

# ============================================================
# 签证数据库 — 80+ 热门目的地
# 格式: destination_key -> {visa_types: {purpose: {...}}}
# ============================================================
VISA_DB = {
    # ---- 亚洲 ----
    "泰国": {
        "en": "Thailand",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "2024年3月1日起永久互免签证。护照有效期需6个月以上，需出示返程机票和酒店确认单。免签停留30天，可延期30天。",
                "evisa_url": ""
            },
            "business": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "商务活动免签停留30天，正式工作需办理Non-B签证。",
                "evisa_url": ""
            },
            "transit": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "过境同样享受免签待遇。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄(如需办非免签类型)",
        "checklist_tips": "免签入境需准备：返程机票、酒店预订单、足够资金证明(1万泰铢/人或2万泰铢/家庭)"
    },
    "日本": {
        "en": "Japan",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 15,
                "visa_fee": 200,
                "processing_time": 5,
                "entry_count": "单次",
                "notes": "单次短期滞在签证15天。3年多次签证需年收入20万+或近3年内2次赴日记录；5年多次需年收入50万+。2024年简化了部分申请材料。",
                "evisa_url": ""
            },
            "business": {
                "type": "需提前申请",
                "max_stay": 90,
                "visa_fee": 200,
                "processing_time": 5,
                "entry_count": "单次",
                "notes": "需日方邀请函、身元保证书、滞在日程表。",
                "evisa_url": ""
            },
            "transit": {
                "type": "过境免签",
                "max_stay": 3,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "经日本转机可享72小时过境免签(Shore Pass)，但建议提前确认航空公司政策。",
                "evisa_url": ""
            }
        },
        "photo_spec": "4.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "单次签证核心：在职证明+银行流水(余额建议5万+)+行程单。多次签证核心：高收入证明+纳税记录+旧签证。首次申请建议通过旅行社代办。"
    },
    "韩国": {
        "en": "South Korea",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 30,
                "visa_fee": 195,
                "processing_time": 5,
                "entry_count": "单次",
                "notes": "有过OECD国家签证记录可简化材料。10年多次签证需满足特定条件(医生/律师/教授等)。济州岛免签30天。",
                "evisa_url": ""
            },
            "business": {
                "type": "需提前申请",
                "max_stay": 90,
                "visa_fee": 195,
                "processing_time": 5,
                "entry_count": "单次",
                "notes": "需韩方邀请函、事业者登录证明、纳税证明。",
                "evisa_url": ""
            },
            "transit": {
                "type": "过境免签",
                "max_stay": 3,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "经韩国转机前往美/加/澳/新/欧，持确认续程机票可免签停留72小时。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "有美/日/加/澳/新签证或永居可申请多次简化。首次申请需：护照+照片+申请表+在职证明+银行流水+身份证复印件。"
    },
    "新加坡": {
        "en": "Singapore",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 30,
                "visa_fee": 153,
                "processing_time": 3,
                "entry_count": "多次",
                "notes": "必须通过授权旅行社/航空公司在线申请，不接受个人直接递签。电子签，审批后邮件发送。",
                "evisa_url": "https://www.ica.gov.sg/entry-visa"
            },
            "business": {
                "type": "需提前申请",
                "max_stay": 30,
                "visa_fee": 153,
                "processing_time": 3,
                "entry_count": "多次",
                "notes": "需新加坡方邀请函+公司注册证明。",
                "evisa_url": "https://www.ica.gov.sg/entry-visa"
            },
            "transit": {
                "type": "过境免签",
                "max_stay": 4,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "持有效澳/加/德/日/新(西兰)/瑞/英/美签证，经新加坡转机可享96小时免签(VFTF)。",
                "evisa_url": ""
            }
        },
        "photo_spec": "4.0×5.2cm，白底，近3个月拍摄",
        "checklist_tips": "新加坡签证必须通过授权旅行社代办。核心材料：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订。拒签常见原因：材料不全、银行余额不足。"
    },
    "马来西亚": {
        "en": "Malaysia",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "2023年12月1日起对中国公民免签30天。需填写MDAC电子入境卡(出发前3天内)，出示返程机票和酒店确认。",
                "evisa_url": "https://imigresen-online.imi.gov.my/mdac/main"
            },
            "business": {
                "type": "需提前申请",
                "max_stay": 30,
                "visa_fee": 200,
                "processing_time": 5,
                "entry_count": "单次",
                "notes": "商务访问需马方邀请函，正式工作需办就业签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×5.0cm，白底(如需办签证类型)",
        "checklist_tips": "免签入境需：MDAC电子入境卡+返程机票+酒店预订+足够资金。MDAC必须出发前3天在线填写。"
    },
    "越南": {
        "en": "Vietnam",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 90,
                "visa_fee": 25,
                "processing_time": 3,
                "entry_count": "单次",
                "notes": "2023年8月起电子签有效期延长至90天。也可办落地签(25美元)但建议提前办电子签更省时。",
                "evisa_url": "https://evisa.xuatnhapcanh.gov.vn/"
            }
        },
        "photo_spec": "4.0×6.0cm，白底",
        "checklist_tips": "电子签在线申请最快，3个工作日。落地签需准备：护照照片+签证费25美元+入境批文(旅行社代办)。"
    },
    "柬埔寨": {
        "en": "Cambodia",
        "visa_types": {
            "tourism": {
                "type": "电子签/落地签",
                "max_stay": 30,
                "visa_fee": 30,
                "processing_time": 3,
                "entry_count": "单次",
                "notes": "电子签和落地签均可。电子签e-visa在线申请3天出签。落地签在口岸办理需30美元现金+照片。",
                "evisa_url": "https://www.evisa.gov.kh/"
            }
        },
        "photo_spec": "4.0×6.0cm，白底",
        "checklist_tips": "落地签最方便，但旺季排队久。建议电子签提前办。需准备：护照+照片+签证费。"
    },
    "缅甸": {
        "en": "Myanmar",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 28,
                "visa_fee": 50,
                "processing_time": 3,
                "entry_count": "单次",
                "notes": "电子签在线申请，3个工作日。部分口岸可落地签但建议电子签。",
                "evisa_url": "https://evisa.moip.gov.mm/"
            }
        },
        "photo_spec": "4.0×6.0cm，白底",
        "checklist_tips": "电子签需上传护照扫描件和照片。入境时需出示酒店预订和返程机票。"
    },
    "老挝": {
        "en": "Laos",
        "visa_types": {
            "tourism": {
                "type": "落地签",
                "max_stay": 30,
                "visa_fee": 20,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "落地签20美元，需1张证件照+护照+申请表。也可电子签提前办。",
                "evisa_url": "https://laoevisa.gov.la/"
            }
        },
        "photo_spec": "4.0×6.0cm，白底",
        "checklist_tips": "落地签方便，但建议带现金和照片。提前办电子签更省时。"
    },
    "菲律宾": {
        "en": "Philippines",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 30,
                "visa_fee": 167,
                "processing_time": 5,
                "entry_count": "单次",
                "notes": "需在使领馆递签。有美/日/加/澳/申根有效签证可免签7天(需从第三国入境)。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底",
        "checklist_tips": "核心材料：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订。有发达国家签证可免签7天。"
    },
    "印度尼西亚": {
        "en": "Indonesia",
        "visa_types": {
            "tourism": {
                "type": "落地签/电子签",
                "max_stay": 30,
                "visa_fee": 35,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "VOA落地签35美元，可延期30天。电子签e-VOA提前申请更方便。",
                "evisa_url": "https://molina.imigrasi.go.id/"
            }
        },
        "photo_spec": "4.0×6.0cm，白底(如需办其他类型)",
        "checklist_tips": "落地签最方便，需护照+返程机票+签证费35美元。e-VOA提前在线申请省排队时间。"
    },
    "印度": {
        "en": "India",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 30,
                "visa_fee": 25,
                "processing_time": 4,
                "entry_count": "单次",
                "notes": "e-Tourist Visa在线申请，30天单次入境。也有1年/5年多次电子签选项。需上传照片和护照扫描件。",
                "evisa_url": "https://indianvisaonline.gov.in/evisa/tvoa.html"
            },
            "business": {
                "type": "电子签",
                "max_stay": 365,
                "visa_fee": 80,
                "processing_time": 4,
                "entry_count": "多次",
                "notes": "e-Business Visa，1年多次入境，每次停留180天。",
                "evisa_url": "https://indianvisaonline.gov.in/evisa/tvoa.html"
            }
        },
        "photo_spec": "5.0×5.0cm，白底，JPEG格式上传",
        "checklist_tips": "电子签全程在线办理，需上传照片+护照首页扫描件。注意照片格式要求严格，很多被拒是因为照片不合格。"
    },
    "斯里兰卡": {
        "en": "Sri Lanka",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 30,
                "visa_fee": 50,
                "processing_time": 2,
                "entry_count": "双次",
                "notes": "ETA电子签在线申请，通常1-2天出签。也可落地签但费用更高。",
                "evisa_url": "https://eta.gov.lk/"
            }
        },
        "photo_spec": "3.5×4.5cm，白底",
        "checklist_tips": "ETA在线申请最方便，需护照扫描件+返程机票确认。"
    },
    "尼泊尔": {
        "en": "Nepal",
        "visa_types": {
            "tourism": {
                "type": "落地签",
                "max_stay": 90,
                "visa_fee": 30,
                "processing_time": 0,
                "entry_count": "多次",
                "notes": "落地签15天30美元/30天50美元/90天125美元。也可在线预先申请。",
                "evisa_url": "https://nepaliport.immigration.gov.np/"
            }
        },
        "photo_spec": "无需照片(落地签自助机拍照)",
        "checklist_tips": "落地签自助机办理非常方便，无需照片。带护照+签证费现金即可。"
    },
    "阿联酋": {
        "en": "UAE",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "2018年起对中国公民免签30天，可延期。迪拜/阿布扎比等均可免签入境。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境需：护照有效期6个月以上+返程机票。停留可延期一次(30天)。"
    },
    "卡塔尔": {
        "en": "Qatar",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签30天，可延期30天。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需护照有效期6个月以上+返程机票+酒店预订。"
    },
    "格鲁吉亚": {
        "en": "Georgia",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "2024年9月起对中国公民免签30天。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需护照有效期6个月以上。"
    },
    "亚美尼亚": {
        "en": "Armenia",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 90,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "多次",
                "notes": "对中国公民免签90天/180天内。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需护照有效期6个月以上。从格鲁吉亚陆路入境很方便。"
    },
    "乌兹别克斯坦": {
        "en": "Uzbekistan",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "2025年起对中国公民免签30天。此前为电子签。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需护照有效期6个月以上。"
    },
    "哈萨克斯坦": {
        "en": "Kazakhstan",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 14,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签14天。需从阿斯塔纳/阿拉木图等国际机场入境。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签14天，需护照有效期6个月以上+返程机票。"
    },
    "沙特阿拉伯": {
        "en": "Saudi Arabia",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 90,
                "visa_fee": 80,
                "processing_time": 1,
                "entry_count": "多次",
                "notes": "电子签在线申请，即时出签，1年多次入境每次90天。也可落地签但费用更高。",
                "evisa_url": "https://visa.visitsaudi.com/"
            }
        },
        "photo_spec": "无需(电子签上传)",
        "checklist_tips": "电子签非常方便，在线即时出签。注意沙特文化禁忌，入境需遵守当地法规。"
    },
    # ---- 欧洲 ----
    "法国": {
        "en": "France",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证，可在26个申根国通行。需在主要停留国或首入国使领馆申请。France-Visas在线填表+TLScontact预约递签。",
                "evisa_url": "https://france-visas.gouv.fr/"
            },
            "business": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "商务申根签证，需法方邀请函+公司担保信。",
                "evisa_url": "https://france-visas.gouv.fr/"
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄，不可微笑",
        "checklist_tips": "申根签核心：行程单+酒店预订+往返机票+保险(3万欧元)+银行流水(余额建议5万+)+在职证明。法国签相对容易，是申根热门首签国。提前2-3个月申请，旺季预约紧张。"
    },
    "德国": {
        "en": "Germany",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过VFS Global递签。德国审核较严，建议材料充分。",
                "evisa_url": "https://videx.diplom.de/"
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "德国签审核严格，银行流水要稳定(切忌临时大额存入)，在职证明需详细。面试可能被问到具体行程细节。"
    },
    "意大利": {
        "en": "Italy",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过VFS Global递签。意大利签相对容易，出签率较高。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "意大利签出签率较高，材料与法国申根类似。旺季(5-9月)预约紧张，提前2-3个月申请。"
    },
    "西班牙": {
        "en": "Spain",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过BLS International递签。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "西班牙签材料与申根标准一致。注意BLS预约有时紧张。"
    },
    "瑞士": {
        "en": "Switzerland",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过TLScontact递签。非申根国但适用申根签证政策。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "瑞士虽非EU但属申根区。材料与申根标准一致。"
    },
    "希腊": {
        "en": "Greece",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。希腊签出签率较高。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "希腊签出签率较高，是申根签热门选择。旺季(6-9月)预约紧张。"
    },
    "荷兰": {
        "en": "Netherlands",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过VFS Global递签。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "荷兰申根签标准流程，审核适中。"
    },
    "葡萄牙": {
        "en": "Portugal",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。葡萄牙签出签率较高。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "葡萄牙签出签率较高，适合首次申根。"
    },
    "捷克": {
        "en": "Czech Republic",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过VFS Global递签。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "捷克申根签标准流程。布拉格是热门旅游目的地。"
    },
    "匈牙利": {
        "en": "Hungary",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。匈牙利签出签率较高。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "匈牙利签出签率较高，材料要求相对宽松。"
    },
    "波兰": {
        "en": "Poland",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "波兰申根签标准流程。"
    },
    "冰岛": {
        "en": "Iceland",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过VFS Global递签。冰岛签出签率较高。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "冰岛签出签率较高，但冬季旅游需特别注意保险覆盖。"
    },
    "挪威": {
        "en": "Norway",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过VFS Global递签。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "挪威申根签标准流程。北欧国家审核较严，材料需充分。"
    },
    "芬兰": {
        "en": "Finland",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。通过VFS Global递签。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "芬兰申根签标准流程。"
    },
    "瑞典": {
        "en": "Sweden",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "瑞典申根签标准流程。"
    },
    "丹麦": {
        "en": "Denmark",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。丹麦签含格陵兰和法罗群岛。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "丹麦申根签标准流程。如去格陵兰需单独注明。"
    },
    "奥地利": {
        "en": "Austria",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "奥地利申根签标准流程。"
    },
    "比利时": {
        "en": "Belgium",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "申根签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "比利时申根签标准流程。"
    },
    "克罗地亚": {
        "en": "Croatia",
        "visa_types": {
            "tourism": {
                "type": "需提前申请(申根)",
                "max_stay": 90,
                "visa_fee": 615,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "2023年1月加入申根区，按申根签证办理。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "克罗地亚已加入申根区，持申根签证可入境。"
    },
    "塞尔维亚": {
        "en": "Serbia",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签30天，持有效申根/英/美签证可免签90天。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，持申根/英/美签证可延长至90天。"
    },
    "波黑": {
        "en": "Bosnia and Herzegovina",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 90,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签90天(每180天内)。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需护照有效期6个月以上。"
    },
    "白俄罗斯": {
        "en": "Belarus",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签30天(每年最多90天)。需从明斯克机场入境。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签需从明斯克国际机场入境，陆路入境需签证。"
    },
    "俄罗斯": {
        "en": "Russia",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 30,
                "visa_fee": 350,
                "processing_time": 7,
                "entry_count": "单次",
                "notes": "需俄罗斯邀请函。团队游可免签15天(需旅行社组织)。电子签仅限远东/加里宁格勒等部分地区。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底",
        "checklist_tips": "核心材料：护照+照片+邀请函+申请表+保险。个人旅游签需俄方旅行社邀请函。团队游免签最方便。"
    },
    "土耳其": {
        "en": "Turkey",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 30,
                "visa_fee": 50,
                "processing_time": 1,
                "entry_count": "单次",
                "notes": "e-Visa在线申请，即时出签。需持有效OECD国家签证或居留许可。",
                "evisa_url": "https://www.evisa.gov.tr/"
            }
        },
        "photo_spec": "无需(电子签)",
        "checklist_tips": "电子签非常方便，前提是持有有效的OECD国家(美/加/澳/新/申根/英/日/韩)签证或居留。无OECD签证需通过使领馆申请。"
    },
    "英国": {
        "en": "United Kingdom",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 180,
                "visa_fee": 1150,
                "processing_time": 15,
                "entry_count": "多次",
                "notes": "标准访客签证6个月多次入境。2年/5年/10年长期签证可选，费用递增。UKVI在线申请+VFS递签。",
                "evisa_url": "https://www.gov.uk/standard-visitor"
            },
            "business": {
                "type": "需提前申请",
                "max_stay": 180,
                "visa_fee": 1150,
                "processing_time": 15,
                "entry_count": "多次",
                "notes": "商务访客签证，允许会议/考察/培训等，不允许工作。",
                "evisa_url": "https://www.gov.uk/standard-visitor"
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "英国签核心：银行流水(6个月，余额建议10万+)+在职证明+行程单。资金证明最重要，切忌临时大额转入。2年签性价比高(仅比6个月贵约300元)。"
    },
    "爱尔兰": {
        "en": "Ireland",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 90,
                "visa_fee": 600,
                "processing_time": 15,
                "entry_count": "单次",
                "notes": "短期停留签证。持英国签证可使用爱尔兰英爱签证互免计划(BIVS)入境。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "如果有英国签证(标注BIVS)，可免签入境爱尔兰。单独申请爱尔兰签材料与英国类似。"
    },
    # ---- 北美洲 ----
    "美国": {
        "en": "United States",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 180,
                "visa_fee": 1250,
                "processing_time": 15,
                "entry_count": "多次",
                "notes": "B1/B2签证10年多次入境，每次停留最长6个月。需面签。EVUS登记后才能入境。",
                "evisa_url": ""
            },
            "business": {
                "type": "需提前申请",
                "max_stay": 180,
                "visa_fee": 1250,
                "processing_time": 15,
                "entry_count": "多次",
                "notes": "B1/B2商务旅游签证10年多次。需面签。",
                "evisa_url": ""
            },
            "transit": {
                "type": "需提前申请",
                "max_stay": 29,
                "visa_fee": 1250,
                "processing_time": 15,
                "entry_count": "多次",
                "notes": "美国没有过境免签，转机也需签证。C类过境签证或B1/B2均可。",
                "evisa_url": ""
            }
        },
        "photo_spec": "5.0×5.0cm，白底，近6个月拍摄，不可戴眼镜",
        "checklist_tips": "美签核心：DS-160表+面签+签证费。面签重点：证明无移民倾向(稳定工作+资产+家庭联系)。拒签常见原因：白本护照、无稳定收入、回答不一致。通过后需EVUS登记(免费)。"
    },
    "加拿大": {
        "en": "Canada",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 180,
                "visa_fee": 850,
                "processing_time": 20,
                "entry_count": "多次",
                "notes": "临时居民签证(TRV)，通常给到护照有效期。也可申请eTA(需持美签)。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "加拿大签核心：资金证明(6个月银行流水)+在职证明+行程单。持有效美签可简化申请。生物信息采集需到签证中心。"
    },
    "墨西哥": {
        "en": "Mexico",
        "visa_types": {
            "tourism": {
                "type": "免签(有条件)",
                "max_stay": 180,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "多次",
                "notes": "持有效美/加/日/英/申根签证可免签180天。无上述签证需申请墨西哥签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底(如需办签)",
        "checklist_tips": "有美/加/日/英/申根签证直接免签，最方便。无上述签证需办墨西哥签证，建议先办美签。"
    },
    "古巴": {
        "en": "Cuba",
        "visa_types": {
            "tourism": {
                "type": "落地签/旅游卡",
                "max_stay": 30,
                "visa_fee": 200,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "中国公民需办理旅游卡(Tarjeta del Turista)，可在航空公司或旅行社购买。部分机场可现场办理。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(旅游卡)",
        "checklist_tips": "旅游卡通常由航空公司代办(约200元)，也可在旅行社购买。需护照+返程机票+酒店预订+保险。"
    },
    # ---- 大洋洲 ----
    "澳大利亚": {
        "en": "Australia",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 90,
                "visa_fee": 960,
                "processing_time": 15,
                "entry_count": "多次",
                "notes": "访客签证600类(Subclass 600)，可在线申请ImmiAccount。1年/3年多次可选。",
                "evisa_url": "https://online.immi.gov.au/"
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "澳签核心：在线申请ImmiAccount+资金证明+在职证明+行程单。电调概率较高(电话调查)，确保信息一致。银行流水稳定，切忌临时大额转入。"
    },
    "新西兰": {
        "en": "New Zealand",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 90,
                "visa_fee": 1200,
                "processing_time": 20,
                "entry_count": "多次",
                "notes": "访客签证，可在线申请。5年多次签证可选(需满足条件)。",
                "evisa_url": "https://www.immigration.govt.nz/"
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "新西兰签核心：在线申请+资金证明+在职证明。审核较严格，材料需真实完整。白本护照建议先办其他签证积累出行记录。"
    },
    "斐济": {
        "en": "Fiji",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 120,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签120天。需返程机票+酒店预订+足够资金。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需护照有效期6个月以上+返程机票+酒店预订。"
    },
    # ---- 南美洲 ----
    "巴西": {
        "en": "Brazil",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 90,
                "visa_fee": 1050,
                "processing_time": 15,
                "entry_count": "多次",
                "notes": "旅游签证90天多次入境。需在巴西驻华使领馆递签。2024年对中国实行电子签政策。",
                "evisa_url": ""
            }
        },
        "photo_spec": "5.0×7.0cm，白底，近6个月拍摄",
        "checklist_tips": "巴西签证材料较多：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订+行程单。照片尺寸特殊(5×7cm)注意不要弄错。"
    },
    "阿根廷": {
        "en": "Argentina",
        "visa_types": {
            "tourism": {
                "type": "电子签(AVE)",
                "max_stay": 90,
                "visa_fee": 200,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "持有效美签/B1B2可申请AVE电子旅行授权，10年多次入境每次90天。无美签需到使领馆申请纸质签证。",
                "evisa_url": "https://www.migraciones.gob.ar/"
            }
        },
        "photo_spec": "4.0×4.0cm，白底(如需办签)",
        "checklist_tips": "有美签可在线申请AVE电子授权非常方便。无美签需纸质签证，建议先办美签再走AVE。"
    },
    "秘鲁": {
        "en": "Peru",
        "visa_types": {
            "tourism": {
                "type": "免签(有条件)",
                "max_stay": 180,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "多次",
                "notes": "持有效美/加/英/澳/申根签证可免签180天。无上述签证需申请秘鲁签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底(如需办签)",
        "checklist_tips": "有美签/申根签直接免签最方便。无上述签证需办秘鲁签证。"
    },
    "智利": {
        "en": "Chile",
        "visa_types": {
            "tourism": {
                "type": "免签(有条件)",
                "max_stay": 90,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "多次",
                "notes": "持有效美/加签证可免签90天。无上述签证需申请智利签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底(如需办签)",
        "checklist_tips": "有美/加签证直接免签。无则需办智利签证，建议先办美签。"
    },
    "哥伦比亚": {
        "en": "Colombia",
        "visa_types": {
            "tourism": {
                "type": "免签(有条件)",
                "max_stay": 90,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "持有效美签/申根签证可免签90天。无上述签证需申请哥伦比亚签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底(如需办签)",
        "checklist_tips": "有美签/申根签直接免签。无则需办签证。"
    },
    # ---- 非洲 ----
    "埃及": {
        "en": "Egypt",
        "visa_types": {
            "tourism": {
                "type": "落地签/电子签",
                "max_stay": 30,
                "visa_fee": 25,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "落地签25美元，需准备：酒店预订+返程机票+2000美元现金或等值。电子签也可在线申请。",
                "evisa_url": "https://visa2egypt.gov.eg/"
            }
        },
        "photo_spec": "无需(落地签)",
        "checklist_tips": "落地签最方便，但需携带2000美元现金(有时会查)。电子签提前办更省心。"
    },
    "摩洛哥": {
        "en": "Morocco",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 90,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "2016年起对中国公民免签90天。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需护照有效期6个月以上+返程机票+酒店预订。"
    },
    "突尼斯": {
        "en": "Tunisia",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 90,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "2017年起对中国公民免签90天。需持有效往返机票和酒店预订。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需返程机票+酒店预订。"
    },
    "南非": {
        "en": "South Africa",
        "visa_types": {
            "tourism": {
                "type": "需提前申请",
                "max_stay": 90,
                "visa_fee": 550,
                "processing_time": 10,
                "entry_count": "多次",
                "notes": "需在南非签证中心递签。审核周期较长，建议提前1个月申请。",
                "evisa_url": ""
            }
        },
        "photo_spec": "3.5×4.5cm，白底，近6个月拍摄",
        "checklist_tips": "南非签材料较多：护照+照片+申请表+在职证明+银行流水+往返机票+酒店预订+黄热病疫苗接种证明(如从疫区来)。"
    },
    "肯尼亚": {
        "en": "Kenya",
        "visa_types": {
            "tourism": {
                "type": "电子签",
                "max_stay": 90,
                "visa_fee": 51,
                "processing_time": 3,
                "entry_count": "单次",
                "notes": "eVisa在线申请，3个工作日。2024年起肯尼亚推行ETA系统替代传统签证。",
                "evisa_url": "https://evisa.go.ke/"
            }
        },
        "photo_spec": "无需(电子签上传)",
        "checklist_tips": "电子签在线申请，需上传护照扫描件+照片+酒店预订+往返机票。"
    },
    "坦桑尼亚": {
        "en": "Tanzania",
        "visa_types": {
            "tourism": {
                "type": "落地签/电子签",
                "max_stay": 90,
                "visa_fee": 50,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "落地签50美元，也可电子签提前办。需黄热病疫苗接种证明。",
                "evisa_url": "https://eservices.immigration.go.tz/"
            }
        },
        "photo_spec": "无需(落地签)",
        "checklist_tips": "落地签方便但可能排队。建议提前办电子签。需黄热病疫苗(黄本)。"
    },
    "毛里求斯": {
        "en": "Mauritius",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 60,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签60天。需返程机票+酒店预订+足够资金。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需返程机票+酒店预订+资金证明。"
    },
    "塞舌尔": {
        "en": "Seychelles",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签30天，可延期。需返程机票+酒店预订+足够资金。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需返程机票+酒店预订。海岛度假热门目的地。"
    },
    # ---- 其他热门 ----
    "马尔代夫": {
        "en": "Maldives",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "对中国公民免签30天，可延期至60天。需返程机票+酒店预订。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签入境，需返程机票+酒店预订。度假村预订确认单很重要。"
    },
    "巴厘岛": {
        "en": "Bali (Indonesia)",
        "visa_types": {
            "tourism": {
                "type": "落地签/电子签",
                "max_stay": 30,
                "visa_fee": 35,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "巴厘岛属印度尼西亚，落地签VOA 35美元，可延期30天。e-VOA可提前在线申请。",
                "evisa_url": "https://molina.imigrasi.go.id/"
            }
        },
        "photo_spec": "4.0×6.0cm，白底(如需办其他类型)",
        "checklist_tips": "落地签最方便，需护照+返程机票+签证费35美元。e-VOA提前在线申请省排队。"
    },
    "济州岛": {
        "en": "Jeju Island (South Korea)",
        "visa_types": {
            "tourism": {
                "type": "免签",
                "max_stay": 30,
                "visa_fee": 0,
                "processing_time": 0,
                "entry_count": "单次",
                "notes": "济州岛对中国公民免签30天，直飞济州即可。但仅限济州岛，去韩国本土需签证。",
                "evisa_url": ""
            }
        },
        "photo_spec": "无需(免签)",
        "checklist_tips": "免签直飞济州岛即可，需护照+往返机票。注意：仅限济州岛活动，不能前往韩国本土。"
    },
}

# 别名映射：用户可能输入的各种名称
ALIAS_MAP = {
    # 亚洲
    "泰国": "泰国", "Thailand": "泰国", "thailand": "泰国",
    "日本": "日本", "Japan": "日本", "japan": "日本",
    "韩国": "韩国", "南韩": "韩国", "South Korea": "韩国",
    "新加坡": "新加坡", "Singapore": "新加坡",
    "马来西亚": "马来西亚", "Malaysia": "马来西亚",
    "越南": "越南", "Vietnam": "越南",
    "柬埔寨": "柬埔寨", "Cambodia": "柬埔寨",
    "缅甸": "缅甸", "Myanmar": "缅甸",
    "老挝": "老挝", "Laos": "老挝",
    "菲律宾": "菲律宾", "Philippines": "菲律宾",
    "印度尼西亚": "印度尼西亚", "印尼": "印度尼西亚", "Indonesia": "印度尼西亚",
    "印度": "印度", "India": "印度",
    "斯里兰卡": "斯里兰卡", "Sri Lanka": "斯里兰卡",
    "尼泊尔": "尼泊尔", "Nepal": "尼泊尔",
    "阿联酋": "阿联酋", "迪拜": "阿联酋", "UAE": "阿联酋", "Dubai": "阿联酋",
    "卡塔尔": "卡塔尔", "Qatar": "卡塔尔",
    "格鲁吉亚": "格鲁吉亚", "Georgia": "格鲁吉亚",
    "亚美尼亚": "亚美尼亚", "Armenia": "亚美尼亚",
    "乌兹别克斯坦": "乌兹别克斯坦", "Uzbekistan": "乌兹别克斯坦",
    "哈萨克斯坦": "哈萨克斯坦", "Kazakhstan": "哈萨克斯坦",
    "沙特": "沙特阿拉伯", "沙特阿拉伯": "沙特阿拉伯", "Saudi Arabia": "沙特阿拉伯",
    # 欧洲
    "法国": "法国", "France": "法国",
    "德国": "德国", "Germany": "德国",
    "意大利": "意大利", "Italy": "意大利",
    "西班牙": "西班牙", "Spain": "西班牙",
    "瑞士": "瑞士", "Switzerland": "瑞士",
    "希腊": "希腊", "Greece": "希腊",
    "荷兰": "荷兰", "Netherlands": "荷兰", "Holland": "荷兰",
    "葡萄牙": "葡萄牙", "Portugal": "葡萄牙",
    "捷克": "捷克", "Czech": "捷克", "Czech Republic": "捷克",
    "匈牙利": "匈牙利", "Hungary": "匈牙利",
    "波兰": "波兰", "Poland": "波兰",
    "冰岛": "冰岛", "Iceland": "冰岛",
    "挪威": "挪威", "Norway": "挪威",
    "芬兰": "芬兰", "Finland": "芬兰",
    "瑞典": "瑞典", "Sweden": "瑞典",
    "丹麦": "丹麦", "Denmark": "丹麦",
    "奥地利": "奥地利", "Austria": "奥地利",
    "比利时": "比利时", "Belgium": "比利时",
    "克罗地亚": "克罗地亚", "Croatia": "克罗地亚",
    "塞尔维亚": "塞尔维亚", "Serbia": "塞尔维亚",
    "波黑": "波黑", "波斯尼亚": "波黑", "Bosnia": "波黑",
    "白俄罗斯": "白俄罗斯", "Belarus": "白俄罗斯",
    "俄罗斯": "俄罗斯", "Russia": "俄罗斯",
    "土耳其": "土耳其", "Turkey": "土耳其", "Türkiye": "土耳其",
    "英国": "英国", "UK": "英国", "United Kingdom": "英国", "英格兰": "英国",
    "爱尔兰": "爱尔兰", "Ireland": "爱尔兰",
    # 北美
    "美国": "美国", "USA": "美国", "US": "美国", "United States": "美国", "美利坚": "美国",
    "加拿大": "加拿大", "Canada": "加拿大",
    "墨西哥": "墨西哥", "Mexico": "墨西哥",
    "古巴": "古巴", "Cuba": "古巴",
    # 大洋洲
    "澳大利亚": "澳大利亚", "澳洲": "澳大利亚", "Australia": "澳大利亚",
    "新西兰": "新西兰", "New Zealand": "新西兰", "纽西兰": "新西兰",
    "斐济": "斐济", "Fiji": "斐济",
    # 南美
    "巴西": "巴西", "Brazil": "巴西",
    "阿根廷": "阿根廷", "Argentina": "阿根廷",
    "秘鲁": "秘鲁", "Peru": "秘鲁",
    "智利": "智利", "Chile": "智利",
    "哥伦比亚": "哥伦比亚", "Colombia": "哥伦比亚",
    # 非洲
    "埃及": "埃及", "Egypt": "埃及",
    "摩洛哥": "摩洛哥", "Morocco": "摩洛哥",
    "突尼斯": "突尼斯", "Tunisia": "突尼斯",
    "南非": "南非", "South Africa": "南非",
    "肯尼亚": "肯尼亚", "Kenya": "肯尼亚",
    "坦桑尼亚": "坦桑尼亚", "Tanzania": "坦桑尼亚",
    "毛里求斯": "毛里求斯", "Mauritius": "毛里求斯",
    "塞舌尔": "塞舌尔", "Seychelles": "塞舌尔",
    # 热门海岛/地区
    "马尔代夫": "马尔代夫", "Maldives": "马尔代夫",
    "巴厘岛": "巴厘岛", "Bali": "巴厘岛",
    "济州岛": "济州岛", "Jeju": "济州岛",
    # 申根通用
    "申根": "法国", "Schengen": "法国",  # 申根查询默认返回法国(最热门首签国)
    "欧洲": "法国", "Europe": "法国",
}

# ============================================================
# 通用材料清单模板
# ============================================================
BASE_CHECKLIST = {
    "必备": [
        {"name": "护照原件", "detail": "有效期6个月以上，至少2页空白签证页", "priority": "必须"},
        {"name": "签证申请表", "detail": "在线填写并打印，签名与护照一致", "priority": "必须"},
        {"name": "证件照", "detail": "按目的地规格要求(见photo_spec)", "priority": "必须"},
        {"name": "身份证正反面复印件", "detail": "清晰复印在A4纸上", "priority": "必须"},
        {"name": "往返机票预订单", "detail": "确认的往返航班预订(部分免签国也需)", "priority": "必须"},
        {"name": "酒店预订确认单", "detail": "覆盖全程住宿(可取消预订也行)", "priority": "必须"},
    ],
    "建议补充": [
        {"name": "在职证明", "detail": "公司抬头纸+公章+负责人签字+联系方式+薪资+准假说明", "priority": "强烈建议"},
        {"name": "银行流水", "detail": "近6个月银行对账单(余额建议5万+，切忌临时大额存入)", "priority": "强烈建议"},
        {"name": "旅行保险", "detail": "覆盖全程+医疗保额3万欧元以上(申根强制)", "priority": "强烈建议"},
        {"name": "行程单", "detail": "每日行程安排(景点+交通+住宿)", "priority": "建议"},
        {"name": "户口本复印件", "detail": "全本复印(部分国家要求)", "priority": "建议"},
    ],
    "可选加分": [
        {"name": "房产证复印件", "detail": "国内固定资产证明，提高过签率", "priority": "可选"},
        {"name": "车辆登记证复印件", "detail": "国内固定资产证明", "priority": "可选"},
        {"name": "存款证明", "detail": "银行冻结存款证明(5万+)", "priority": "可选"},
        {"name": "结婚证复印件", "detail": "已婚加分项，证明国内约束力", "priority": "可选"},
        {"name": "旧护照/旧签证", "detail": "良好出行记录，提高过签率", "priority": "可选"},
    ]
}

# 按目的补充材料
PURPOSE_EXTRA = {
    "business": [
        {"name": "邀请函", "detail": "外方公司/机构出具的正式邀请函(含邀请方信息+访问目的+费用承担)", "priority": "必须"},
        {"name": "公司派遣信", "detail": "中方公司出具的派遣函(含职位+薪资+出访目的+费用承担)", "priority": "必须"},
        {"name": "营业执照复印件", "detail": "中方公司营业执照副本复印件加盖公章", "priority": "建议"},
        {"name": "双方往来证明", "detail": "商务往来邮件/合同/发票等", "priority": "建议"},
    ],
    "transit": [
        {"name": "第三国签证", "detail": "目的地国家的有效签证", "priority": "必须"},
        {"name": "联程机票", "detail": "确认的转机航班预订", "priority": "必须"},
    ],
    "study": [
        {"name": "录取通知书", "detail": "学校正式录取信/Offer", "priority": "必须"},
        {"name": "资金证明", "detail": "学费+生活费的存款证明", "priority": "必须"},
        {"name": "学历证明", "detail": "最高学历证书+成绩单(公证)", "priority": "必须"},
        {"name": "语言成绩", "detail": "IELTS/TOEFL等语言考试成绩", "priority": "必须"},
    ],
}

# 常见拒签原因
COMMON_REJECTION_REASONS = [
    "资金证明不足或不真实(临时大额存入、来源不明)",
    "在职证明信息不完整(缺联系方式、薪资、准假说明)",
    "行程安排不合理(日期冲突、住宿未覆盖全程)",
    "材料造假(虚假酒店/机票预订被查出)",
    "移民倾向(单身白本、无稳定收入、无国内约束力)",
    "面签表现差(回答不一致、过度紧张、与材料矛盾)",
    "护照问题(有效期不足、空白页不够、有不良记录)",
    "申请表填写错误(信息不一致、漏填重要信息)",
]


def resolve_destination(dest: str) -> str:
    """解析目的地名称，返回VISA_DB中的key"""
    if dest in VISA_DB:
        return dest
    if dest in ALIAS_MAP:
        mapped = ALIAS_MAP[dest]
        if mapped in VISA_DB:
            return mapped
    # 模糊匹配：包含关系
    for key in VISA_DB:
        if dest in key or key in dest:
            return key
    # 英文名匹配
    for key, data in VISA_DB.items():
        if data.get("en", "").lower() == dest.lower():
            return key
    return ""


def check_visa(destination: str, purpose: str = "tourism") -> dict:
    """工具1: 查询签证要求"""
    dest_key = resolve_destination(destination)
    if not dest_key:
        return {
            "success": False,
            "error": f"未找到「{destination}」的签证信息",
            "suggestion": "请尝试输入更常见的国家/地区名称，如：泰国、日本、法国、美国、澳大利亚等",
            "supported_count": len(VISA_DB)
        }
    
    data = VISA_DB[dest_key]
    purpose_data = data["visa_types"].get(purpose)
    if not purpose_data:
        # fallback到tourism
        purpose_data = data["visa_types"].get("tourism", {})
    
    result = {
        "success": True,
        "destination": dest_key,
        "destination_en": data.get("en", ""),
        "purpose": purpose,
        "visa_info": purpose_data,
        "photo_spec": data.get("photo_spec", "3.5×4.5cm，白底，近6个月拍摄"),
        "checklist_tips": data.get("checklist_tips", "")
    }
    
    return result


def visa_checklist(destination: str, purpose: str = "tourism", 
                   first_time: bool = True, has_old_visa: bool = False) -> dict:
    """工具2: 生成材料清单"""
    dest_key = resolve_destination(destination)
    if not dest_key:
        return {
            "success": False,
            "error": f"未找到「{destination}」的签证信息"
        }
    
    data = VISA_DB[dest_key]
    visa_info = data["visa_types"].get(purpose, data["visa_types"].get("tourism", {}))
    
    # 免签/落地签不需要常规材料清单
    visa_type = visa_info.get("type", "")
    if visa_type in ["免签"]:
        return {
            "success": True,
            "destination": dest_key,
            "visa_type": visa_type,
            "message": f"✅ {dest_key}对中国公民免签，无需申请签证！",
            "entry_requirements": [
                "护照有效期6个月以上",
                "返程/续程机票确认单",
                "酒店预订确认单",
                "足够资金证明(部分国家会抽查)"
            ],
            "tips": data.get("checklist_tips", ""),
            "photo_spec": "无需(免签)"
        }
    
    if visa_type in ["落地签"]:
        return {
            "success": True,
            "destination": dest_key,
            "visa_type": visa_type,
            "message": f"✅ {dest_key}可办理落地签，抵达后在口岸办理即可",
            "landing_visa_requirements": [
                "护照有效期6个月以上",
                f"签证费: {visa_info.get('visa_fee', 'N/A')}美元现金",
                "1张证件照(白底3.5×4.5cm)",
                "返程机票确认单",
                "酒店预订确认单"
            ],
            "tips": data.get("checklist_tips", ""),
            "photo_spec": data.get("photo_spec", "3.5×4.5cm，白底")
        }
    
    # 需要提前申请的完整材料清单
    checklist = {
        "required": list(BASE_CHECKLIST["必备"]),
        "recommended": list(BASE_CHECKLIST["建议补充"]),
        "optional": list(BASE_CHECKLIST["可选加分"]),
    }
    
    # 按目的补充
    if purpose in PURPOSE_EXTRA:
        checklist["required"].extend(PURPOSE_EXTRA[purpose])
    
    # 首次申请额外提示
    if first_time:
        checklist["first_time_tips"] = [
            "首次申请建议材料尽量充分，宁可多不可少",
            "白本护照(无出国记录)建议先办免签/落地签国家积累出行记录",
            "银行流水保持稳定，至少提前3个月开始准备",
        ]
    
    # 有旧签证的补充
    if has_old_visa:
        checklist["old_visa_bonus"] = "旧签证记录是加分项，特别是发达国家签证(美/申根/日/澳)，提交旧护照复印件可提高过签率"
    
    # 申根签证特殊说明
    if "申根" in visa_type:
        checklist["schengen_notes"] = [
            "申根签证可在26个申根国通行，但需在主要停留国使领馆申请",
            "旅行保险医疗保额必须≥3万欧元(强制要求)",
            "申根签证费统一为615元人民币(约80欧元)",
            "建议首签选择法国/意大利/希腊(出签率相对较高)",
        ]
    
    result = {
        "success": True,
        "destination": dest_key,
        "visa_type": visa_type,
        "max_stay": visa_info.get("max_stay", "N/A"),
        "processing_time": f"{visa_info.get('processing_time', 'N/A')}个工作日",
        "visa_fee": f"¥{visa_info.get('visa_fee', 'N/A')}",
        "photo_spec": data.get("photo_spec", "3.5×4.5cm，白底，近6个月拍摄"),
        "checklist": checklist,
        "rejection_reasons": COMMON_REJECTION_REASONS[:5],  # 前5个最常见
        "tips": data.get("checklist_tips", "")
    }
    
    return result


def visa_policy_update(destination: str, months: int = 3) -> dict:
    """工具3: 签证政策速递(联网搜索)"""
    dest_key = resolve_destination(destination)
    if not dest_key:
        return {
            "success": False,
            "error": f"未找到「{destination}」的签证信息"
        }
    
    data = VISA_DB[dest_key]
    dest_en = data.get("en", dest_key)
    
    # 构建搜索查询
    query = f"{dest_key} 签证 中国 最新政策 {datetime.now().year}"
    query_en = f"China visa policy {dest_en} latest update"
    
    updates = []
    
    # 搜索中文
    try:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=5"
        req = urllib.request.Request(search_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        # 简单提取搜索结果摘要
        snippets = re.findall(r'<div[^>]*>(.*?)</div>', html)
        for s in snippets[:5]:
            clean = re.sub(r'<[^>]+>', '', s).strip()
            if len(clean) > 30 and ("签证" in clean or "免签" in clean or "visa" in clean.lower()):
                updates.append({"source": "web", "content": clean[:200]})
    except Exception:
        pass
    
    # 内置近期重大政策变动(手动维护)
    POLICY_UPDATES = [
        {"date": "2024-03", "dest": "泰国", "content": "中泰永久互免签证协定正式生效，中国公民免签入境30天"},
        {"date": "2024-06", "dest": "格鲁吉亚", "content": "对中国公民免签30天"},
        {"date": "2024-09", "dest": "格鲁吉亚", "content": "免签政策正式实施"},
        {"date": "2025-01", "dest": "乌兹别克斯坦", "content": "对中国公民免签30天(此前为电子签)"},
        {"date": "2024-11", "dest": "日本", "content": "简化部分签证申请材料，3年多次签证条件放宽"},
        {"date": "2024-01", "dest": "马来西亚", "content": "对中国公民免签30天(需填MDAC电子入境卡)"},
        {"date": "2024-06", "dest": "澳大利亚", "content": "600类签证在线申请流程优化，部分情况可免生物信息采集"},
        {"date": "2024-01", "dest": "新加坡", "content": "对中国公民实施30天免签(此前需签证)"},
        {"date": "2023-08", "dest": "越南", "content": "电子签有效期从30天延长至90天"},
        {"date": "2024-10", "dest": "巴西", "content": "对中国实行电子签证政策，简化申请流程"},
    ]
    
    # 筛选与目的地相关的政策更新
    relevant_updates = [u for u in POLICY_UPDATES if u["dest"] == dest_key]
    
    result = {
        "success": True,
        "destination": dest_key,
        "current_visa_type": data["visa_types"].get("tourism", {}).get("type", "未知"),
        "recent_updates": relevant_updates if relevant_updates else f"近{months}个月暂无{dest_key}签证重大政策变动",
        "web_search_results": updates[:3] if updates else "联网搜索暂无最新结果",
        "disclaimer": "签证政策可能随时调整，请以各国驻华使领馆最新公告为准。建议出发前核实最新要求。"
    }
    
    return result


def main():
    """主入口"""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: visa_guide.py <tool> <args_json>", "tools": ["check_visa", "visa_checklist", "visa_policy_update"]}, ensure_ascii=False))
        sys.exit(1)
    
    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON arguments"}, ensure_ascii=False))
        sys.exit(1)
    
    if tool == "check_visa":
        result = check_visa(
            destination=args.get("destination", ""),
            purpose=args.get("purpose", "tourism")
        )
    elif tool == "visa_checklist":
        result = visa_checklist(
            destination=args.get("destination", ""),
            purpose=args.get("purpose", "tourism"),
            first_time=args.get("first_time", True),
            has_old_visa=args.get("has_old_visa", False)
        )
    elif tool == "visa_policy_update":
        result = visa_policy_update(
            destination=args.get("destination", ""),
            months=args.get("months", 3)
        )
    else:
        result = {"error": f"Unknown tool: {tool}", "available_tools": ["check_visa", "visa_checklist", "visa_policy_update"]}
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
