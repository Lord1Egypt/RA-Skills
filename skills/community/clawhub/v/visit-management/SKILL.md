---
name: visit-management
description: 走访计划管理与提醒技能。基于真实Excel台账（美兰中心C+服务.xlsx）生成走访计划，提醒走访任务。触发场景：(1) 定时任务每日09:00生成走访提醒，(2) 每周一09:00生成本周走访计划，(3) 手动触发走访管理（@企服助手 走访管理）。
---

# 走访计划管理与提醒技能 (Visit Management Skill)

## ⚠️ 重要说明

**本技能已自包含，无需安装 customer-management**

本版本 (v2.0.0) 已将所有客户管理逻辑直接内联到技能中，包括：
- 客户档案查询 (`query_customer_profile`)
- 客户画像构建 (`build_customer_portrait`)
- 客户时间线生成 (`build_customer_timeline`)
- 风险标记计算 (`calculate_risk_tags`)

无需依赖任何外部技能，开箱即用。

---

## 功能概述

本技能用于自动化走访计划管理，基于中集金地美兰中心真实Excel台账，根据企业等级、服务记录、续租预警等因素智能生成走访计划，并推送提醒给管家。

---

## 数据源配置

**数据文件**: `/Users/mac/美兰中心C+服务.xlsx`

**工作表映射**:
| 功能模块 | 工作表名 | 用途 |
|---------|---------|------|
| **C+服务记录** | C+服务记录 | 历史走访记录 |
| **客户档案** | 👨客户管理👨 | 企业画像（等级、截至日期、状态） |
| **费用收缴** | 👨💼费用收缴👨💼 | 欠费风险判断 |
| **能耗收缴** | 👨💼能耗收缴👨💼 | 能耗费用记录 |
| **报修情况** | 🛠️报修情况汇总🛠️ | 报修记录 |

---

## 客户管理逻辑（内联）

### 1. 查询客户档案

```python
def query_customer_profile(unit_no=None, tenant_name=None, contract_no=None):
    """
    查询客户档案
    
    Args:
        unit_no: 单元号（如 T1-601）
        tenant_name: 租户名（支持模糊匹配）
        contract_no: 合同号
    
    Returns:
        dict: 客户完整档案信息
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws = wb['👨客户管理👨']
    
    headers = [cell.value for cell in ws[1]]
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        # 匹配条件
        if unit_no and row[5] == unit_no:  # 单元号
            return build_customer_dict(headers, row)
        if tenant_name and tenant_name in str(row[6]):  # 租户名模糊匹配
            return build_customer_dict(headers, row)
        if contract_no and row[4] == contract_no:  # 合同号
            return build_customer_dict(headers, row)
    
    return None

def build_customer_dict(headers, row):
    """将Excel行数据转换为字典"""
    return {headers[i]: row[i] for i in range(len(headers))}
```

### 2. 构建客户画像

```python
def build_customer_portrait(unit_no):
    """
    构建客户画像 - 聚合多个数据源
    
    Args:
        unit_no: 单元号（主键）
    
    Returns:
        dict: 客户画像（包含服务、费用、报修等汇总）
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    
    portrait = {
        "基础信息": query_customer_profile(unit_no),
        "服务记录": [],
        "费用记录": [],
        "能耗记录": [],
        "报修记录": [],
        "风险标记": []
    }
    
    if not portrait["基础信息"]:
        return portrait
    
    # 1. 查询C+服务记录（关联字段：租户名）
    ws_service = wb['C+服务记录']
    tenant_name = portrait["基础信息"]["租户名"]
    
    for row in ws_service.iter_rows(min_row=2, values_only=True):
        if row[0] == tenant_name:  # 关联客户字段
            portrait["服务记录"].append({
                "走访时间": row[1],
                "走访管家": row[2],
                "客户情绪": row[3],
                "成交情况": row[4],
                "服务类别": row[5],
                "成交金额": row[6],
                "详情记录": row[7]
            })
    
    # 2. 查询费用收缴记录（关联字段：单元号）
    ws_fee = wb['👨💼费用收缴👨💼']
    
    for row in ws_fee.iter_rows(min_row=2, values_only=True):
        if row[1] == unit_no:  # 单元号
            portrait["费用记录"].append({
                "合同编号": row[0],
                "费项项目": row[3],
                "应收金额": row[4],
                "已收金额": row[6],
                "欠收金额": row[8],
                "是否支付": row[9],
                "月份": row[13]
            })
    
    # 3. 查询能耗收缴记录（关联字段：单元号）
    ws_energy = wb['👨💼能耗收缴👨💼']
    
    for row in ws_energy.iter_rows(min_row=2, values_only=True):
        if row[0] == unit_no:  # 单元号
            portrait["能耗记录"].append({
                "租户名": row[1],
                "应收金额": row[2],
                "已收金额": row[3],
                "欠费金额": row[4],
                "是否支付": row[5],
                "月份": row[6]
            })
    
    # 4. 查询报修记录（关联字段：楼层/单元）
    ws_repair = wb['🛠️报修情况汇总🛠️']
    
    for row in ws_repair.iter_rows(min_row=2, values_only=True):
        if unit_no in str(row[0]):  # 楼层/单元匹配
            portrait["报修记录"].append({
                "楼层/单元": row[0],
                "紧急程度": row[1],
                "报修细节描述": row[2],
                "报修人员": row[4],
                "报修时间": row[5],
                "维修人员": row[6],
                "维修跟进状态": row[7]
            })
    
    # 5. 计算风险标记
    portrait["风险标记"] = calculate_risk_tags(portrait)
    
    return portrait
```

### 3. 计算风险标记

```python
def calculate_risk_tags(portrait):
    """
    计算客户风险标记
    
    Returns:
        list: 风险标记列表（如 ["欠费风险", "流失风险"]）
    """
    risks = []
    
    # 1. 欠费风险判断
    欠费总额 = 0
    for fee in portrait["费用记录"]:
        if fee["是否支付"] == "否":
            欠费金额 = float(fee["欠收金额"]) if fee["欠收金额"] else 0
            欠费总额 += 欠费金额
    
    if 欠费总额 > 50000:
        risks.append("🚨 高欠费风险")
    elif 欠费总额 > 10000:
        risks.append("⚠️ 中度欠费风险")
    elif 欠费总额 > 0:
        risks.append("📢 轻度欠费提醒")
    
    # 2. 流失风险判断（续租预警）
    基础信息 = portrait["基础信息"]
    if 基础信息:
        截至日期 = parse_date(基础信息["截至日期"])
        剩余天数 = (截至日期 - datetime.now().date()).days
        
        if 剩余天数 <= 30:
            risks.append(f"🚨 流失风险（合同剩余{剩余天数}天）")
        elif 剩余天数 <= 90:
            risks.append(f"⚠️ 续租预警（合同剩余{剩余天数}天）")
    
    # 3. 投诉/报修频率判断
    报修次数 = len(portrait["报修记录"])
    if 报修次数 >= 3:
        risks.append(f"⚠️ 高频报修（{报修次数}次）")
    
    # 4. 服务满意度判断
    满意记录 = [s for s in portrait["服务记录"] if s["客户情绪"] == "满意"]
    总记录 = len(portrait["服务记录"])
    
    if 总记录 > 0 and len(满意记录) / 总记录 < 0.5:
        risks.append(f"⚠️ 低满意度（满意率{len(满意记录)/总记录*100:.1f}%）")
    
    return risks
```

### 4. 构建客户时间线

```python
def build_customer_timeline(unit_no):
    """
    构建客户时间线 - 按时间排序所有记录
    
    Args:
        unit_no: 单元号
    
    Returns:
        list: 时间线事件列表（按时间倒序）
    """
    portrait = build_customer_portrait(unit_no)
    
    timeline = []
    
    # 1. 合同事件
    基础信息 = portrait["基础信息"]
    if 基础信息:
        timeline.append({
            "时间": 基础信息["开始日期"],
            "事件类型": "合同签约",
            "事件描述": f"签约{基础信息['租期']}，单元{unit_no}",
            "详情": 基础信息
        })
    
    # 2. 服务记录事件
    for service in portrait["服务记录"]:
        timeline.append({
            "时间": service["走访时间"],
            "事件类型": "C+服务",
            "事件描述": f"管家{service['走访管家']}走访，情绪{service['客户情绪']}",
            "详情": service
        })
    
    # 3. 费用记录事件
    for fee in portrait["费用记录"]:
        timeline.append({
            "时间": fee["月份"],
            "事件类型": "费用收缴",
            "事件描述": f"{fee['费项项目']}，应收¥{fee['应收金额']}，已收¥{fee['已收金额']}",
            "详情": fee
        })
    
    # 4. 报修记录事件
    for repair in portrait["报修记录"]:
        timeline.append({
            "时间": repair["报修时间"],
            "事件类型": "报修工单",
            "事件描述": f"{repair['报修细节描述']}, 状态{repair['维修跟进状态']}",
            "详情": repair
        })
    
    # 5. 能耗记录事件
    for energy in portrait["能耗记录"]:
        timeline.append({
            "时间": energy["月份"],
            "事件类型": "能耗收缴",
            "事件描述": f"能耗应收¥{energy['应收金额']}，已收¥{energy['已收金额']}",
            "详情": energy
        })
    
    # 按时间排序（倒序，最新在前）
    timeline.sort(key=lambda x: parse_date(x["时间"]), reverse=True)
    
    return timeline

def parse_date(date_str):
    """解析多种格式的日期字符串"""
    if isinstance(date_str, datetime):
        return date_str.date() if hasattr(date_str, 'date') else date_str
    
    # 尝试多种日期格式
    formats = [
        "%Y-%m-%d",
        "%Y年%m月%d日",
        "%Y/%m/%d",
        "%Y.%m.%d"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except:
            continue
    
    return datetime.now().date()
```

---

## Excel工作表字段映射

### C+服务记录表（10字段）

| Excel列序号 | 字段名 | 用途 |
|-------------|--------|------|
| 1 | 租户名 | 关联客户管理表 |
| 2 | 走访时间 | 上次走访时间 |
| 3 | 走访管家 | 管家分配 |
| 4 | 客户情绪 | 满意度判断 |
| 5 | 成交情况 | 成交记录 |
| 6 | 服务类别 | 服务类型 |
| 7 | 成交金额 | 成交金额 |
| 8 | 详情记录 | 需求描述 |

---

## 核心逻辑

### 1. 走访质量评分算法

```python
def calculate_visit_quality_score(unit_no, visit_record):
    """
    计算单次走访的质量评分（满分100分）
    
    Args:
        unit_no: 单元号
        visit_record: 走访记录字典
    
    Returns:
        dict: 评分详情 {'总分': 85, '明细': {...}}
    """
    score = 0
    details = {}
    
    # 1. 客户情绪评分（权重40%）
    customer_emotion = visit_record.get('客户情绪', '')
    emotion_score = 0
    if customer_emotion == '满意':
        emotion_score = 40
    elif customer_emotion == '一般':
        emotion_score = 25
    elif customer_emotion == '不满意':
        emotion_score = 10
    score += emotion_score
    details['客户情绪'] = {'得分': emotion_score, '满分': 40}
    
    # 2. 成交情况评分（权重30%）
    deal_status = visit_record.get('成交情况', '')
    deal_score = 0
    if deal_status == '是':
        deal_score = 30
        # 额外奖励：成交金额越大，加分越多
        deal_amount = float(visit_record.get('成交金额', 0) or 0)
        if deal_amount > 5000:
            deal_score += 10  # 额外加分
    score += deal_score
    details['成交情况'] = {'得分': deal_score, '满分': 30}
    
    # 3. 服务类别完整性评分（权重20%）
    service_type = visit_record.get('服务类别', '')
    service_score = 0
    if service_type and service_type != '无':
        service_score = 20
    score += service_score
    details['服务类别'] = {'得分': service_score, '满分': 20}
    
    # 4. 详情记录完整性评分（权重10%）
    detail_record = visit_record.get('详情记录', '')
    record_score = 0
    if detail_record and len(detail_record) >= 20:  # 至少20个字符
        record_score = 10
    elif detail_record and len(detail_record) >= 10:
        record_score = 5
    score += record_score
    details['详情记录'] = {'得分': record_score, '满分': 10}
    
    return {
        '总分': min(score, 100),
        '明细': details
    }
```

### 2. 走访闭环追踪逻辑

```python
def track_visit_followup(unit_no, visit_date):
    """
    追踪走访后的问题跟进闭环情况
    
    Args:
        unit_no: 单元号
        visit_date: 走访日期
    
    Returns:
        dict: 闭环追踪结果
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_visit = wb['C+服务记录']
    
    # 读取走访记录
    visit_info = None
    followup_status = '未跟进'
    followup_days = 0
    
    for row in ws_visit.iter_rows(min_row=2, values_only=True):
        if row[0] == unit_no:  # 租户名匹配
            record_date = parse_date(row[1])  # 走访时间
            if record_date == visit_date:
                visit_info = {
                    '详情记录': row[7],  # 详情记录
                    '客户情绪': row[3],  # 客户情绪
                    '成交情况': row[4]   # 成交情况
                }
                break
    
    if not visit_info:
        return {'状态': '走访记录未找到', '跟进天数': 0}
    
    # 检查是否有问题需要跟进
    detail = visit_info.get('详情记录', '')
    has_issue = any(keyword in detail for keyword in ['问题', '需求', '投诉', '报修', '建议'])
    
    if not has_issue:
        return {'状态': '无需跟进', '跟进天数': 0}
    
    # 检查后续是否有跟进记录
    today = datetime.now().date()
    followup_found = False
    
    for row in ws_visit.iter_rows(min_row=2, values_only=True):
        if row[0] == unit_no:
            record_date = parse_date(row[1])
            if record_date > visit_date:
                # 检查是否是跟进记录
                followup_detail = row[7]
                if any(keyword in followup_detail for keyword in ['跟进', '解决', '回复', '处理']):
                    followup_found = True
                    followup_days = (record_date - visit_date).days
                    break
    
    if followup_found:
        followup_status = '已跟进'
    else:
        followup_days = (today - visit_date).days
        if followup_days > 7:
            followup_status = '超时未跟进'
        else:
            followup_status = '跟进中'
    
    return {
        '状态': followup_status,
        '跟进天数': followup_days,
        '问题摘要': detail[:50] + '...' if len(detail) > 50 else detail
    }
```

### 3. 走访计划生成算法（升级版）

```python
def generate_visit_plan():
    """
    智能生成走访计划
    
    Returns:
        dict: 走访计划清单
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_customer = wb['👨客户管理👨']
    
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    
    plan = {
        "高优先级": [],  # 必访
        "中优先级": [],  # 应访
        "低优先级": []   # 可访
    }
    
    # 遍历所有签约企业
    for row in ws_customer.iter_rows(min_row=2, values_only=True):
        if row[12] == "签约":  # 状态 = 签约
            unit_no = row[5]
            tenant_name = row[6]
            
            # 直接调用内联函数获取企业画像
            customer_profile = query_customer_profile(unit_no)
            
            if not customer_profile:
                continue
            
            level = customer_profile.get("等级", "B")
            lease_end_str = customer_profile.get("截至日期", "")
            lease_end = parse_date(lease_end_str)
            
            # 直接调用内联函数获取历史走访记录
            timeline = build_customer_timeline(unit_no)
            
            historical_visits = [e for e in timeline if e["事件类型"] == "C+服务"]
            last_visit = historical_visits[0] if historical_visits else None
            
            # 判断是否需要走访
            should_visit = False
            priority = "低"
            reason = ""
            
            # 规则1：A级企业 - 每月至少走访1次
            if level == "A":
                if not last_visit or (today - parse_date(last_visit["时间"])).days > 30:
                    should_visit = True
                    priority = "高"
                    reason = "A级企业月度走访"
            
            # 规则2：B级企业 - 每季度至少走访1次
            elif level == "B":
                if not last_visit or (today - parse_date(last_visit["时间"])).days > 90:
                    should_visit = True
                    priority = "中"
                    reason = "B级企业季度走访"
            
            # 规则3：续租预警企业 - 提前2个月开始密集走访
            days_remaining = (lease_end - today).days
            if days_remaining <= 60 and days_remaining > 0:
                should_visit = True
                priority = "高"
                reason = f"续租预警（剩余{days_remaining}天）"
            
            # 规则4：欠费企业 - 配合催缴走访
            # 从build_customer_portrait的风险标记中获取
            portrait = build_customer_portrait(unit_no)
            
            if any("欠费风险" in risk for risk in portrait.get("风险标记", [])):
                should_visit = True
                priority = "高"
                reason = "欠费企业催缴走访"
            
            if should_visit:
                # 计算历史走访质量评分
                quality_scores = []
                for visit in historical_visits[:5]:  # 取最近5次走访
                    visit_date = parse_date(visit["时间"])
                    # 从Excel读取详细记录
                    visit_detail = get_visit_detail_from_excel(unit_no, visit_date)
                    if visit_detail:
                        score_info = calculate_visit_quality_score(unit_no, visit_detail)
                        quality_scores.append(score_info['总分'])
                
                avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
                
                # 检查最近一次走访的闭环状态
                followup_status = '无需跟进'
                if last_visit:
                    last_visit_date = parse_date(last_visit["时间"])
                    followup_info = track_visit_followup(unit_no, last_visit_date)
                    followup_status = followup_info['状态']
                
                plan[f"{priority}优先级"].append({
                    "单元号": unit_no,
                    "租户名": tenant_name,
                    "等级": level,
                    "上次走访": last_visit["时间"] if last_visit else "无",
                    "生成原因": reason,
                    "历史质量评分": round(avg_quality_score, 2),
                    "闭环状态": followup_status
                })
    
    return plan
```

### 4. 从Excel读取走访详细记录

```python
def get_visit_detail_from_excel(unit_no, visit_date):
    """
    从Excel C+服务记录表读取指定日期的走访详细记录
    
    Args:
        unit_no: 单元号
        visit_date: 走访日期
    
    Returns:
        dict: 走访详细记录
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_visit = wb['C+服务记录']
    
    for row in ws_visit.iter_rows(min_row=2, values_only=True):
        # 匹配租户名和走访时间
        tenant_name = row[0]  # 租户名
        record_date = parse_date(row[1])  # 走访时间
        
        if tenant_name == unit_no and record_date == visit_date:
            return {
                '客户情绪': row[3],  # 客户情绪
                '成交情况': row[4],  # 成交情况
                '服务类别': row[5],  # 服务类别
                '成交金额': row[6],  # 成交金额
                '详情记录': row[7]   # 详情记录
            }
    
    return None
```

### 5. 管家分配逻辑

```python
def assign_visitor(unit_no):
    """
    根据单元号分配管家
    
    Args:
        unit_no: 单元号
    
    Returns:
        str: 管家姓名
    """
    # 管家分区表（可配置）
    visitor_zones = {
        "戚亮先": ["T1-6F", "T1-7F", "T1-8F"],
        "刘瑞": ["T1-9F", "T1-10F", "T1-11F"],
        "张三": ["T1-12F", "T1-13F", "T1-14F"]
    }
    
    # 提取楼层
    floor = unit_no.split("-")[1][:2] + "F"  # T1-601 → 6F
    
    for visitor, zones in visitor_zones.items():
        if floor in zones:
            return visitor
    
    return "未分配"
```

---

## 执行流程

```
Step 1 → 读取Excel客户管理表
         工作表：👨客户管理👨
         筛选：状态 = '签约'

Step 2 → 调用内联函数
         获取企业画像（等级、截至日期）
         获取历史走访记录（客户时间线）

Step 3 → 判断是否需要走访
         ├─ A级企业：上次走访 > 30天
         ├─ B级企业：上次走访 > 90天
         ├─ 续租预警：剩余 ≤ 60天
         └─ 欠费企业：有欠费风险标记

Step 4 → 分配管家
         根据单元号楼层分配

Step 5 → 生成本周走访计划
         分级：高/中/低优先级

Step 6 → 推送企微
         发送给各管家
```

---

## 走访计划推送模板

```
━━━━━━━━━━━━━━━
【本周走访计划】2026-05-28 ~ 2026-06-03

━━━ 高优先级（必访）━━━
1. T1-601 上海铭尤力
   等级：A | 上次走访：2026-02-02
   原因：A级企业月度走访
   管家：戚亮先

2. T1-XXX XXX公司
   原因：续租预警（剩余45天）
   管家：刘瑞

━━━ 中优先级（应访）━━━
1. T1-XXX XXX公司
   原因：B级企业季度走访
   管家：张三

━━━ 统计 ━━━
本周走访总数：XX个
高优先级：XX个 | 中优先级：XX个

⚡ 操作链接：[腾讯文档-走访计划]
━━━━━━━━━━━━━━━
```

---

## 定时任务配置

```json
{
  "name": "走访计划生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成本周走访计划，根据企业等级、续租预警、欠费风险智能规划走访任务"
  },
  "sessionTarget": "isolated"
}
```

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 走访管理`
2. **OpenClaw指令**: `生成本周走访计划`

---

## 配置参数

```json
{
  "visit_management": {
    "excel_path": "/Users/mac/美兰中心C+服务.xlsx",
    "level_a_visit_cycle_days": 30,
    "level_b_visit_cycle_days": 90,
    "renewal_alert_days": 60,
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
  }
}
```

---

## 使用示例

**用户输入**: `@企服助手 走访管理`

**输出**:
```
━━━━━━━━━━━━━━━
【本周走访计划】2026-05-28 ~ 2026-06-03

━━━ 高优先级（必访）━━━
共3个企业待走访

━━━ 中优先级（应访）━━━
共5个企业待走访

━━━ 低优先级（可访）━━━
共2个企业待走访

━━━ 统计 ━━━
本周走访总数：10个

⚡ 操作链接：[腾讯文档-走访计划]
━━━━━━━━━━━━━━━
```

---

## 版本历史

### v2.0.0 (2026-06-08)
- ✅ 移除 customer-management 依赖
- ✅ 内联所有客户管理逻辑
- ✅ 完全自包含，开箱即用

### v1.0.0 (2026-05-28)
- 初始版本
- 依赖 customer-management 技能
