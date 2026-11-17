#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保险销售合规自查 · 风险画像与整改台账生成器
================================================

面向中小保险中介机构、保险专业代理机构与转型独立代理人：
输入机构规模与关键管控现状，输出十组三十四项检查的风险画像、
优先整改项与整改台账 CSV。

设计原则
--------
1. 只依赖 Python 标准库，零 pip 依赖，不联网，不上传任何数据
2. 只做"体检 + 清单 + 整改建议"，不做违规认定，不出法律意见
3. 权重与风险分布来自真实行政处罚案例（26 例，见 references/监管案例与依据库.md）
4. Windows 控制台中文/符号兼容：强制 UTF-8 + 不输出 emoji

用法
----
    python compliance_audit.py --scale 8 --channels 3 --staff 12
    python compliance_audit.py --scale 8 --channels 3 --staff 12 --json
    python compliance_audit.py --list-group A
    python compliance_audit.py --scale 8 --channels 3 --staff 12 --export-todo

参数
----
    --scale N        分支机构数量（默认 1）
    --channels N     销售渠道数（默认 1）
    --staff N        从业人员数（默认 5）
    --agents N       代理人数量（默认 3）
    --premium N      年保费规模（万元，默认 500）
    --douluo yes|no  是否已建立双录质检台账（默认 no）
    --selfpolicy yes|no  是否有自保件互保件（默认 no）
    --export-todo    导出整改台账 CSV 到脚本同级目录
    --list-group X   只列出某一组检查项（A-J）
    --json           以 JSON 输出
"""
import argparse
import csv
import io
import json
import os
import sys

# Windows 控制台输出中文/符号会抛 UnicodeEncodeError —— 强制 UTF-8 并替换不可编码字符
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
except Exception:
    pass

# ─────────────────────────── 十组检查项结构化数据 ───────────────────────────
# tier: 'required' 必查 / 'conditional' 视情况 / 'bonus' 加分项
# weight: 该项在风险画像中的权重（1-5）
# hits: 该项在 26 例真实处罚案例中的命中次数（用于排序，不用于制造恐慌）
CHECKS = [
    # A 组：双录
    {'id': 'A1', 'group': 'A', 'name': '双录要素完整性', 'tier': 'required', 'weight': 5, 'hits': 6,
     'how': '调近3月应双录保单清单，逐单核验五环节：出示身份证明 / 出示条款与免责书面说明 / 明确说明义务含犹豫期后损失 / 投保人明确肯定答复 / 投保人签署文件',
     'basis': '保险销售行为可回溯管理暂行办法第7条；保险销售行为管理办法第25、31条', 'risk': '高'},
    {'id': 'A2', 'group': 'A', 'name': '双录真实性与不可剪辑', 'tier': 'required', 'weight': 5, 'hits': 4,
     'how': '抽检质检不合格件与投诉件原始视听资料：录制是否连续、能否辨识面部特征与交谈、有无剪辑拼接、时间显示精确到分、画面与单证是否一致',
     'basis': '保险销售行为可回溯管理暂行办法第8条；地方双录通知第三条', 'risk': '高'},
    {'id': 'A3', 'group': 'A', 'name': '双录质检比例与整改闭环', 'tier': 'required', 'weight': 5, 'hits': 3,
     'how': '核质检台账：一般保单月质检不低于30%；特殊群体不低于60%；投连险及60周岁以上100%；在犹豫期内完成；问题15个工作日内整改留痕',
     'basis': '可回溯办法第10条；地方双录通知质检条款', 'risk': '高'},
    {'id': 'A4', 'group': 'A', 'name': '双录归档与保存期限', 'tier': 'conditional', 'weight': 3, 'hits': 1,
     'how': '核视听资料是否由承保公司统一保存；期限自合同终止起算，一年期以下不少于5年、一年期以上不少于10年；纠纷件保存至纠纷结束后2年；调阅审批留痕',
     'basis': '可回溯办法第12、13条', 'risk': '中'},
    {'id': 'A5', 'group': 'A', 'name': '银行渠道双录覆盖率', 'tier': 'conditional', 'weight': 4, 'hits': 3,
     'how': '银保一年期以上新单清单与双录成功清单做差集，核未双录占比与原因；核银行是否将双录成功信息反馈承保公司',
     'basis': '可回溯办法第4、9条；商业银行代理销售业务管理办法第41条', 'risk': '高'},
    {'id': 'A6', 'group': 'A', 'name': '双录覆盖范围与产品口径', 'tier': 'required', 'weight': 4, 'hits': 1,
     'how': '核双录产品清单是否覆盖一年期以上及一年期以下但保证续保的人身险；政策性产品与团体险是否正确排除',
     'basis': '可回溯办法第4、6条；地方双录通知适用范围条款', 'risk': '高'},

    # B 组：适当性
    {'id': 'B1', 'group': 'B', 'name': '风险测评真实性与独立性', 'tier': 'required', 'weight': 5, 'hits': 2,
     'how': '抽测评原始记录与录音录像，核是否本人独立填写；线下结果是否反馈客户确认后留存；线上是否展示结果供客户确认；有无批量自动提交与后补修改',
     'basis': '金融机构产品适当性管理办法第13、17条；中保协适当性自律规范', 'risk': '高'},
    {'id': 'B2', 'group': 'B', 'name': '测评有效期与频次管控', 'tier': 'required', 'weight': 4, 'hits': 0,
     'how': '导出评估记录，核有效期原则上12个月、到期须重评；单日不超2次、12个月累计不超8次；等级变动是否经客户确认',
     'basis': '金融机构产品适当性管理办法第29条', 'risk': '高'},
    {'id': 'B3', 'group': 'B', 'name': '产品与客户适当性匹配', 'tier': 'required', 'weight': 5, 'hits': 1,
     'how': '按产品风险等级与客户风险承受能力等级拉3月成交保单比对，重点查高复杂产品卖给低承受能力客户；查已评估但不匹配仍成交件；核不匹配时是否出具建议终止投保书面留痕',
     'basis': '金融机构产品适当性管理办法第12、38条；中保协自律规范匹配条款', 'risk': '高'},
    {'id': 'B4', 'group': 'B', 'name': '财务支付水平与需求评估', 'tier': 'required', 'weight': 4, 'hits': 1,
     'how': '抽一年期以上个人身险新单，核是否留存家庭收入资产与保费承担能力信息；比期缴保费与年收入、缴费年限与年龄之和；超阈值件是否取得签名投保声明',
     'basis': '金融机构产品适当性管理办法第34、35、39条', 'risk': '高'},

    # C 组：夸大承诺
    {'id': 'C1', 'group': 'C', 'name': '禁夸大与保本承诺', 'tier': 'required', 'weight': 5, 'hits': 4,
     'how': '抽长险双录、朋友圈与宣传稿，检索保本、保收益、稳赚、保证收益、零风险、比存款利息高、随时可取等表述；核是否用保证、一定、肯定修饰非保证收益',
     'basis': '金融机构产品适当性管理办法第13条；保险销售行为管理办法第17条；金融产品网络营销管理办法第10条', 'risk': '高'},
    {'id': 'C2', 'group': 'C', 'name': '宣传内容与条款一致性', 'tier': 'required', 'weight': 5, 'hits': 3,
     'how': '抽在售宣传材料、朋友圈、海报、展架与短视频脚本，逐句与已报备条款和产品说明书比对：名称、保障范围、保险期间、缴费方式、现金价值、免责、犹豫期、等待期、退保损失',
     'basis': '保险销售行为管理办法第17、25条；消保办法第22、23条', 'risk': '高'},
    {'id': 'C3', 'group': 'C', 'name': '分红万能投连的非保证利益提示', 'tier': 'conditional', 'weight': 4, 'hits': 1,
     'how': '抽三类产品双录与投保声明，核是否说明利益不确定性、红利基于精算假设不保证、万能超最低保证利率收益不确定、投连可能本金亏损、账户风险等级与费用扣除',
     'basis': '金融机构产品适当性管理办法第22、37条；保险销售行为管理办法第22、25条', 'risk': '高'},

    # D 组：返佣费用
    {'id': 'D1', 'group': 'D', 'name': '费用账务与列支真实性', 'tier': 'required', 'weight': 5, 'hits': 5,
     'how': '调3月手续费、佣金、劳务费、咨询费明细，与业务系统保单和发票三方比对；有无无真实业务对应费用、与业务规模不匹配的大额费用、票据要素不符；有无以个人薪酬名义支付渠道回扣',
     'basis': '保险法第86、170条；保险销售行为管理办法第8、9条', 'risk': '高'},
    {'id': 'D2', 'group': 'D', 'name': '虚挂中介与虚挂保单', 'tier': 'conditional', 'weight': 4, 'hits': 1,
     'how': '从费用台账反查合作机构：抽前10大费用支付对象，核实际承保保单数、签单人员名单与委托协议；核有无仅过账无展业；核投保人信息真实性',
     'basis': '保险法第116条；保险销售行为管理办法第8、9、33条', 'risk': '高'},
    {'id': 'D3', 'group': 'D', 'name': '给予合同外利益排查', 'tier': 'required', 'weight': 5, 'hits': 5,
     'how': '抽新单检投保环节礼品返现权益记录、渠道协议外费用支付、销售人员自付返佣；核是否经个人账户向投保人转账；核有无以贷转存、代缴优惠形式变相返佣',
     'basis': '保险法第116、131条；保险销售行为管理办法第8、32条；消保办法第28条', 'risk': '高'},
    {'id': 'D4', 'group': 'D', 'name': '业务人员套利与利益输送', 'tier': 'conditional', 'weight': 4, 'hits': 2,
     'how': '查员工与代理人自办保单、代开发票、代签单、代收保费记录；核是否为他人牟取不正当利益；核有无代客持有保单、代客操作网银购买',
     'basis': '保险法第116条；保险销售行为管理办法第8、9条', 'risk': '高'},

    # E 组：保费管理
    {'id': 'E1', 'group': 'E', 'name': '保费收取路径与资金流', 'tier': 'required', 'weight': 5, 'hits': 1,
     'how': '抽保单收款路径：付款账户是否必须为投保人、被保险人或受益人本人；有无业务员个人或第三方账户代收代付；银行代收到账与承保时序是否一致',
     'basis': '保险销售行为管理办法第32条；保险法第116条', 'risk': '高'},
    {'id': 'E2', 'group': 'E', 'name': '保费截留与账实核对', 'tier': 'required', 'weight': 5, 'hits': 1,
     'how': '每月将保费应收与实际到账逐单比对找差异，抽取差异单核是否涉及销售人员代收、坐支、账外循环；核应收未收台账与追偿记录',
     'basis': '保险法第116、131条；保险销售行为管理办法第32、41条', 'risk': '高'},

    # F 组：如实告知
    {'id': 'F1', 'group': 'F', 'name': '如实告知询问具体性', 'tier': 'required', 'weight': 5, 'hits': 1,
     'how': '抽健康险、意外险、寿险新单投保单及询问表，检是否有概括性询问条款；核双录中是否就具体疾病、症状、用药、职业风险逐项提问与客户答复',
     'basis': '保险销售行为管理办法第27条；保险法第16条', 'risk': '高'},
    {'id': 'F2', 'group': 'F', 'name': '投保人信息真实性', 'tier': 'required', 'weight': 4, 'hits': 1,
     'how': '核心系统抽样比对新单投保信息与身份信息：姓名、证件号、职业、收入、医保参保、既往病史；核财产险健康险销售环节是否实际询问医保参保情况',
     'basis': '保险销售行为管理办法第7、33条；保险法第116条', 'risk': '中'},
    {'id': 'F3', 'group': 'F', 'name': '客户告知书与投保意愿确认', 'tier': 'required', 'weight': 5, 'hits': 2,
     'how': '抽新单：告知书是否机构统一制作并当场出示；投保单、投保提示书、免责说明、投保声明是否由投保人本人签署；核抄录风险提示语是否本人笔迹',
     'basis': '保险销售行为管理办法第29、24条；保险代理人监管规定第50条', 'risk': '高'},
    {'id': 'F4', 'group': 'F', 'name': '回访真实性与时效', 'tier': 'required', 'weight': 5, 'hits': 2,
     'how': '抽一年期以上个人身险新单全部回访记录：是否在犹豫期内完成、是否由非销售推介人员开展；抽查录音核验逐项确认；核是否向销售本人回访',
     'basis': '保险销售行为管理办法第35条；可回溯办法第11条；中保协回访确认清单', 'risk': '高'},

    # G 组：销售误导
    {'id': 'G1', 'group': 'G', 'name': '宣传审核与授权发布', 'tier': 'required', 'weight': 5, 'hits': 4,
     'how': '建自建宣传内容台账：抽公众号、朋友圈、短视频、微信群内容各20条，核是否事前审核授权发布；核是否使用统一销售用语；核自媒体账号是否登记在册',
     'basis': '保险销售行为管理办法第17、18条；金融产品网络营销管理办法第7、16条', 'risk': '高'},
    {'id': 'G2', 'group': 'G', 'name': '销售话术合规抽查', 'tier': 'required', 'weight': 5, 'hits': 2,
     'how': '抽质检标记有销售误导件及投诉件，按关键词检：混淆保险与存款理财、贬低同业、最后一天与停售施压、随时全额退',
     'basis': '保险销售行为管理办法第17、25条；消保办法第23条', 'risk': '高'},
    {'id': 'G3', 'group': 'G', 'name': '销售行为真实性留痕', 'tier': 'conditional', 'weight': 3, 'hits': 3,
     'how': '抽新单核投保单笔迹与实际情况、提交时间与面签时间、双录时间与出单时间一致性；关注犹豫期内快速退保复效高风险件；核不正当利益排查记录',
     'basis': '保险销售行为管理办法第29、33条；保险法第116条', 'risk': '中'},

    # H 组：无证展业
    {'id': 'H1', 'group': 'H', 'name': '执业登记与报备', 'tier': 'required', 'weight': 5, 'hits': 4,
     'how': '从监管信息系统导出从业人员名单，与在岗展业名单、签单名单做差集；核每人是否仅通过一家机构登记；核登记与授权范围是否匹配',
     'basis': '保险代理人监管规定第38、94条；保险销售行为管理办法第3条', 'risk': '高'},
    {'id': 'H2', 'group': 'H', 'name': '展业地域范围', 'tier': 'conditional', 'weight': 3, 'hits': 2,
     'how': '核许可证载明经营区域与实际展业地域：近3月保单投保人地址与出单机构所在区域比对，识别跨区展业件；核是否超出被代理公司授权区域',
     'basis': '保险销售行为管理办法第11条；保险法第164条', 'risk': '中'},
    {'id': 'H3', 'group': 'H', 'name': '第三方机构展业管理', 'tier': 'required', 'weight': 5, 'hits': 2,
     'how': '核合作第三方是否持合法资格；协议是否覆盖全流程责任边界；银行网点或现场是否有银行与保险机构以外人员从事销售宣传推介；核代销产品准入与尽调记录',
     'basis': '保险法第116条；保险销售行为管理办法第9条；商业银行代理销售业务管理办法', 'risk': '高'},
    {'id': 'H4', 'group': 'H', 'name': '分支机构与许可证管理', 'tier': 'conditional', 'weight': 2, 'hits': 1,
     'how': '核本机构及下属分支机构许可证、营业执照、场所报备：是否在核准地址经营；有无未经批准设立；许可证遗失未补领',
     'basis': '保险法第113、164条；保险公司管理规定', 'risk': '中'},

    # I 组：自保互保
    {'id': 'I1', 'group': 'I', 'name': '自保互保识别与考核排除', 'tier': 'conditional', 'weight': 4, 'hits': 0,
     'how': '导出近3月保单，识别投保人、被保险人、受益人与销售本人或直系亲属的保单，统计自保互保占比、继续率、退保率；核基本法是否将其排除在入职转正晋级与业绩考核之外、佣金是否不优于其他保单',
     'basis': '地方自保互保管理规定（现行明文监管依据，未见直接处罚决定书）', 'risk': '高'},
    {'id': 'I2', 'group': 'I', 'name': '自保互保虚增保费与双录', 'tier': 'conditional', 'weight': 4, 'hits': 1,
     'how': '对识别出的自保互保件核是否存在即保即退、即买即借、循环投保；核一年期以上自保互保件是否双录；核有无掩盖直系亲属关系投保',
     'basis': '地方自保互保管理规定', 'risk': '高'},

    # J 组：数据与消保
    {'id': 'J1', 'group': 'J', 'name': '业务档案完整性', 'tier': 'required', 'weight': 3, 'hits': 2,
     'how': '抽近3月新单档案（机构自行抽查不低于当月应双录件数5%）：保单基本情况、保费代收交付、佣金金额与收取、提供代理服务人员姓名与报酬账户；核保存期限',
     'basis': '保险代理人监管规定第50条；保险销售行为管理办法第41条', 'risk': '中'},
    {'id': 'J2', 'group': 'J', 'name': '客户信息保护', 'tier': 'required', 'weight': 5, 'hits': 1,
     'how': '抽客户信息访问与导出日志、第三方共享台账：核有无违规查询下载复制存储篡改；对外提供是否有单独同意与协议约束；核第三方是否跨平台传递客户信息',
     'basis': '消保办法第13、42至48条；保险销售行为管理办法第7条', 'risk': '高'},
    {'id': 'J3', 'group': 'J', 'name': '业务与财务数据真实性', 'tier': 'required', 'weight': 5, 'hits': 4,
     'how': '每月核心业务系统、业务报表、财务系统、监管报送四方比对；抽差异单核原因；核销售数据与实际承保、继续率、新单量与财务收入、渠道费用的匹配性',
     'basis': '保险法第170条；保险销售行为管理办法第12、42条', 'risk': '高'},
    {'id': 'J4', 'group': 'J', 'name': '投诉处理与消保闭环', 'tier': 'conditional', 'weight': 3, 'hits': 1,
     'how': '抽近3月保险销售类投诉件，核是否建立处理机制并落实多元化解；核回访发现销售误导是否及时处理；核消保内部考核与审计覆盖',
     'basis': '消保办法第15、16、18、19条；保险销售行为管理办法第35条', 'risk': '中'},
]

GROUP_NAMES = {
    'A': '双录（录音录像）合规',
    'B': '销售适当性',
    'C': '夸大与承诺收益',
    'D': '返佣与手续费',
    'E': '保费管理与挪用',
    'F': '未如实告知',
    'G': '销售误导',
    'H': '未登记与无证展业',
    'I': '自保件与互保件',
    'J': '数据与消费者权益保护',
}


def compute_profile(args):
    """根据机构规模与管控现状计算风险画像。

    逻辑：每组先按"该组在本机构的暴露度"打分（规模越大、管控越弱 → 暴露越高），
    再按组内检查项的权重与真实处罚命中率排序，输出优先整改项。
    """
    scale = max(1, args.scale)
    staff = max(1, args.staff)
    channels = max(1, args.channels)
    premium = max(0, args.premium)

    # 暴露度：规模与渠道复杂度放大风险；管控现状削弱风险
    size_factor = min(3.0, 1.0 + 0.12 * (scale - 1) + 0.05 * (staff - 1) + 0.15 * (channels - 1))
    if premium > 5000:
        size_factor += 0.2
    if premium > 20000:
        size_factor += 0.2

    # 管控修正
    control = 1.0
    if args.douluo == 'yes':
        control *= 0.78          # 有双录质检台账，A 组风险下调
    if args.selfpolicy == 'no':
        control *= 1.0           # 无自保互保说明未涉及，不额外加权

    groups = {}
    for c in CHECKS:
        g = groups.setdefault(c['group'], {
            'group': c['group'], 'name': GROUP_NAMES[c['group']],
            'items': [], 'weight_sum': 0, 'hits_sum': 0,
        })
        g['items'].append(c)
        g['weight_sum'] += c['weight']
        g['hits_sum'] += c['hits']

    # 每组暴露度
    group_exposure = {
        'A': 1.25 if args.douluo == 'no' else 0.85,
        'B': 1.00 + 0.10 * (channels - 1),
        'C': 1.10,
        'D': 1.30 if premium > 2000 else 1.05,
        'E': 1.15,
        'F': 1.10,
        'G': 1.15 if args.selfpolicy == 'yes' else 1.00,
        'H': 1.20 if staff > 20 else 0.90,
        'I': 1.30 if args.selfpolicy == 'yes' else 0.70,
        'J': 1.05 + 0.10 * (channels - 1),
    }

    for g in groups.values():
        g['exposure'] = round(group_exposure.get(g['group'], 1.0) * size_factor * control, 3)
        g['avg_weight'] = round(g['weight_sum'] / len(g['items']), 2)
        g['hit_total'] = g['hits_sum']

    # 全局分数：各组暴露度按组内平均权重加权，归一到 0-100
    # 归一化基准取"最大可能暴露度"（大机构 + 全部无管控），使分数有可解释的绝对含义：
    #   100 分 ≈ 一个 30+ 分支、5 渠道、200 人、5 亿保费、零管控的机构
    total_w = sum(g['avg_weight'] for g in groups.values())
    weighted = sum(g['exposure'] * g['avg_weight'] for g in groups.values()) / max(1e-6, total_w)
    # 基准：size_factor 上限 3.0 × control 上限 1.0 × 最高组暴露度 1.30
    baseline = 3.0 * 1.0 * 1.30
    score = max(2.0, min(100.0, round(weighted / baseline * 100.0, 1)))

    if score >= 65:
        level = '高风险'
        advice = '存在多项处罚高发项，建议立即自查并向合规负责人或律师报告'
    elif score >= 40:
        level = '中风险'
        advice = '部分高风险项缺少留痕，建议优先补齐Top 10整改项'
    elif score >= 22:
        level = '偏低风险'
        advice = '基础管控已有，建议做常态化台账与季度复核'
    else:
        level = '低风险'
        advice = '管控较完善，建议保持并关注属地新规与新产品口径'

    # 优先整改项：按 组暴露度 × 组内项权重 × (1 + 命中率) 排序
    ranked = []
    for g in groups.values():
        for it in g['items']:
            score_item = g['exposure'] * it['weight'] * (1 + it['hits'] / 6.0)
            ranked.append((round(score_item, 2), g, it))
    ranked.sort(key=lambda x: -x[0])

    top = ranked[:10]

    return {
        'score': score,
        'level': level,
        'advice': advice,
        'size_factor': round(size_factor, 2),
        'control_factor': round(control, 2),
        'groups': sorted(groups.values(), key=lambda g: -g['exposure']),
        'top_items': [{'id': it['id'], 'name': it['name'], 'group': g['name'],
                        'risk': it['risk'], 'priority': p, 'how': it['how'],
                        'basis': it['basis']} for p, g, it in top],
        'input': {'scale': scale, 'channels': channels, 'staff': staff,
                  'agents': args.agents, 'premium': premium,
                  'douluo': args.douluo, 'selfpolicy': args.selfpolicy},
    }


def export_todo(profile):
    """导出整改台账 CSV。"""
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '整改台账模板.csv')
    with io.open(out, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['序号', '编号', '检查项', '所属组', '风险等级', '优先级得分',
                    '自查动作', '监管依据', '自查结论(符合/部分符合/不符合)', '整改动作',
                    '责任人', '完成日期', '复核人'])
        for i, t in enumerate(profile['top_items'], 1):
            w.writerow([i, t['id'], t['name'], t['group'], t['risk'], t['priority'],
                        t['how'], t['basis'], '', '', '', '', ''])
    return out


def render_text(profile, todo_path=None):
    L = []
    L.append('保险销售合规自查 · 风险画像')
    L.append('=' * 52)
    inp = profile['input']
    L.append('机构画像：分支机构 %s 个 · 销售渠道 %s 个 · 从业 %s 人 · 代理人 %s 人 · 年保费 %s 万'
             % (inp['scale'], inp['channels'], inp['staff'], inp['agents'], inp['premium']))
    L.append('管控现状：双录质检台账=%s · 自保互保=%s'
             % ('已建立' if inp['douluo'] == 'yes' else '未建立',
                '有' if inp['selfpolicy'] == 'yes' else '无'))
    L.append('')
    L.append('总分 %.1f / 100    风险等级：%s' % (profile['score'], profile['level']))
    L.append('建议：%s' % profile['advice'])
    L.append('')
    L.append('【十组风险分布】')
    for g in profile['groups']:
        bar = '#' * int(round(g['exposure'] * 10))
        L.append('  %-2s %-22s 暴露度 %5.2f  %s' % (g['group'], g['name'], g['exposure'], bar))
    L.append('')
    L.append('【优先整改 Top 10】')
    for i, t in enumerate(profile['top_items'], 1):
        L.append('  %2d. [%s] %s（%s，风险%s）' % (i, t['id'], t['name'], t['group'], t['risk']))
        L.append('      查：%s' % t['how'])
        L.append('      依：%s' % t['basis'])
    if todo_path:
        L.append('')
        L.append('整改台账已导出：%s' % todo_path)
    L.append('')
    L.append('本工具为合规自查辅助，不构成法律意见或监管认定结论。')
    L.append('高风险场景须由具备相应责任的人员复核。')
    return '\n'.join(L)


def list_group(g):
    out = []
    out.append('%s 组 · %s' % (g, GROUP_NAMES.get(g, '')))
    out.append('-' * 52)
    for c in CHECKS:
        if c['group'] != g:
            continue
        out.append('[%s] %s（%s / 权重%d / 处罚命中%d例）' % (c['id'], c['name'], c['risk'], c['weight'], c['hits']))
        out.append('  查：%s' % c['how'])
        out.append('  依：%s' % c['basis'])
    return '\n'.join(out)


def main():
    p = argparse.ArgumentParser(
        description='保险销售合规自查 · 风险画像与整改台账生成器（纯标准库、不联网）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument('--scale', type=int, default=1, help='分支机构数量')
    p.add_argument('--channels', type=int, default=1, help='销售渠道数')
    p.add_argument('--staff', type=int, default=5, help='从业人员数')
    p.add_argument('--agents', type=int, default=3, help='代理人数量')
    p.add_argument('--premium', type=int, default=500, help='年保费规模（万元）')
    p.add_argument('--douluo', choices=['yes', 'no'], default='no', help='是否已建立双录质检台账')
    p.add_argument('--selfpolicy', choices=['yes', 'no'], default='no', help='是否有自保件互保件')
    p.add_argument('--export-todo', action='store_true', help='导出整改台账 CSV')
    p.add_argument('--list-group', help='只列出某一组检查项（A-J）')
    p.add_argument('--json', action='store_true', help='以 JSON 输出')
    args = p.parse_args()

    if args.list_group:
        g = args.list_group.strip().upper()
        if g not in GROUP_NAMES:
            print('无效组别：%s（可选 %s）' % (g, '、'.join(sorted(GROUP_NAMES))))
            return 2
        print(list_group(g))
        return 0

    profile = compute_profile(args)
    todo_path = export_todo(profile) if args.export_todo else None

    if args.json:
        profile['todo_csv'] = todo_path
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print(render_text(profile, todo_path))
    return 0


if __name__ == '__main__':
    sys.exit(main())
