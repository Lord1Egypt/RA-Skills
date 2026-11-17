#!/usr/bin/env python3
"""
公司名称/岗位提取共享模块
被 build-progress-table.py 与 apply-progress-updates.py 共同使用
"""

import re

# ── 公司别名表：关键词 -> 规范公司名 ──────────────────────────────
COMPANY_ALIASES = [
    (['蚂蚁集团', '蚂蚁', '蚂小招', 'antgroup'], '蚂蚁集团'),
    (['腾讯', 'tencent'], '腾讯'),
    (['美团', 'meituan'], '美团'),
    (['OPPO', 'oppo'], 'OPPO'),
    (['阿里巴巴', '阿里', 'alibaba'], '阿里巴巴'),
    (['淘天'], '淘天集团'),
    (['联想', 'lenovo'], '联想'),
    (['大疆', 'DJI', 'dji'], '大疆'),
    (['网易游戏互娱'], '网易游戏互娱'),
    (['网易', 'netease'], '网易'),
    (['中兴', 'zte', 'joinus'], '中兴通讯'),
    (['高通', 'qualcomm'], '高通'),
    (['前程无忧', '51job'], '前程无忧'),
]

# 招聘平台/笔试系统域名：这些发件人不是公司，主题中提取不到公司名时忽略该邮件
PLATFORM_DOMAINS = [
    'nowcoder.com', 'nowcoder.org', 'acmcoder.com', 'joinus.cc',
    'mokahr.com', 'moka.ai', '51job.com', 'meetsystem.cn', 'smartinterview.cn',
    'dingtalk.com', 'feishu.cn', 'larksuite.com',
]

# 无意义的发件人显示名（清理后若命中则跳过，改用域名兜底）
MEANINGLESS_NAMES = [
    '招聘管理系统', '管理系统', '系统', '客服', '通知', '邮箱', '自动回复',
    'noreply', 'no-reply', 'donotreply', 'support', 'service', 'info',
    'recruit', 'recruitment', 'campus', 'hr', 'ehr', 'mailer', 'admin',
]


def clean_company_name(name):
    """清理公司名：去掉招聘/校招/年份/业务词等后缀"""
    if not name:
        return ''
    name = name.strip().strip('【】')
    for suffix in [
        '2027届校园招聘', '2026届校园招聘', '2027校园招聘', '2026校园招聘',
        '2027届实习生招聘', '2026届实习生招聘', '2027实习生招聘', '2026实习生招聘',
        '校园招聘', '实习生招聘', '实习招聘', '校招', '招聘', '校园', '实习生',
        '在线笔试', '在线测评', '笔试', '测评', '面试邀约', '面试通知', '面试邀请',
        '空中宣讲会', '宣讲会', '报名邀请', '邀请函', '邀请反馈', '邀约', '邀请',
        '测评邀请', '考试邀请函', '内推邀请', '投递成功通知', '投递成功', '投递邀请',
        '简历投递', '感谢你的关注与参与', '官方', '专场',
    ]:
        name = name.replace(suffix, '')
    name = re.sub(r'(19|20)\d{2}', '', name)   # 去年份
    name = re.sub(r'\d+届?', '', name)         # 去"27届"等
    name = re.sub(r'[\s\-—_·｜|]+', '', name)  # 去空白/符号
    return name.strip()


def match_alias(text):
    """在文本中匹配公司别名，返回规范公司名或 None"""
    if not text:
        return None
    low = text.lower()
    for keywords, company in COMPANY_ALIASES:
        for kw in keywords:
            if kw.lower() in low:
                return company
    return None


def is_meaningless(name):
    """判断清理后的显示名是否无意义（系统名/英文占位等）"""
    if not name:
        return True
    low = name.lower()
    if any(m in low for m in MEANINGLESS_NAMES):
        return True
    # 纯英文且不在别名表（如人名、域名）→ 无意义
    if re.fullmatch(r'[a-zA-Z0-9.\-_ ]+', name):
        return match_alias(name) is None
    return False


def extract_company(subject, from_addr):
    """从主题 + 发件人提取公司名称。只返回别名表命中的公司名。

    优先级：主题【】> 主题全文 > 发件人显示名（括号内优先）> 域名。
    平台域名且主题无公司名时返回 None（调用方忽略该邮件）；
    无法识别时返回 '未知公司'（保留一行供用户手动归类）。
    """
    subject = subject or ''
    from_addr = from_addr or ''

    domain = ''
    m = re.search(r'@([a-zA-Z0-9.-]+)', from_addr)
    if m:
        domain = m.group(1).lower()

    # 1. 主题【】内
    m = re.search(r'【([^】]+)】', subject)
    if m:
        hit = match_alias(m.group(1))
        if hit:
            return hit

    # 2. 主题全文
    hit = match_alias(subject)
    if hit:
        return hit

    # 3. 发件人显示名（括号内容优先）
    display = re.sub(r'\s*<[^>]*>', '', from_addr).strip().strip('"')
    m = re.search(r'[（(]([^（）()]+)[)）]', display)
    if m:
        hit = match_alias(m.group(1))
        if hit:
            return hit
    hit = match_alias(display)
    if hit:
        return hit

    # 4. 域名
    if domain:
        hit = match_alias(domain)
        if hit:
            return hit

    # 5. 招聘平台/笔试系统域名且无法归属 → 忽略
    if any(domain == d or domain.endswith('.' + d) for d in PLATFORM_DOMAINS):
        return None

    # 6. 无法识别
    return '未知公司'


def extract_position(subject):
    """从主题轻量提取岗位信息；提取不到返回 None（留空由用户手动填写）"""
    if not subject:
        return None
    # 宣传/招聘会类邮件不参与岗位提取（如研究院招聘广告）
    for skip in ['招聘会', '宣讲会', '内推', '热招', '启动', '开放中', '邀请你加入']:
        if skip in subject:
            return None
    keywords = [
        '算法', '后端', '前端', '客户端', '测试开发', '测试', '产品经理', '产品运营', '产品',
        '运营', '数据分析', '数据挖掘', '数据开发', '机器学习', '深度学习', '人工智能',
        '嵌入式', '硬件', '芯片', '集成电路', 'Java开发', 'C++开发', 'Go开发', 'Python开发',
        '安全', '云计算', '大数据', '视觉', 'NLP', '自然语言', '图像',
    ]
    for kw in keywords:
        if kw in subject:
            return kw
    return None
