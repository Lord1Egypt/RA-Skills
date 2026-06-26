---
name: workorder-dispatch
description: 工单分派与SLA监控技能。基于真实Excel台账（美兰中心C+服务.xlsx）自动分派报修工单，跟踪处理进度，超时自动升级。触发场景：(1) 企业报修（企微、电话、邮件），(2) 管家上报维修需求，(3) 定时监控工单状态（每小时），(4) 超时未处理自动升级。
---

# 工单分派与SLA监控技能 (Workorder Dispatch Skill)

## 功能概述

本技能用于自动化报修工单的全生命周期管理，基于中集金地美兰中心真实Excel台账，包括工单创建、自动分派、进度跟踪、SLA监控和超时升级。

---

## 数据源配置

**数据文件**: `/Users/mac/美兰中心C+服务.xlsx`

**工作表映射**:
| 功能模块 | 工作表名 | 用途 |
|---------|---------|------|
| **报修汇总** | 🛠️报修情况汇总🛠️ | 主数据源（工单记录） |

---

## 数据接口（真实Excel字段映射）

### 报修情况汇总表字段（13个）

**关键字段**:
| Excel列序号 | 字段名 | 类型 | 说明 | 示例值 |
|-------------|--------|------|------|--------|
| 1 | 楼层/单元 | TEXT | 报修位置 | T1-1009 / T1-9F女厕 |
| 2 | 紧急程度 | TEXT | SLA分级依据 | 紧急！急需处理！ |
| 3 | 报修细节描述 | TEXT | 问题描述 | 单元跳闸，手动无法推动总阀 |
| 4 | 报修相关现场照片【越多越好】 | TEXT | 照片链接 | （可选） |
| 5 | 报修人员 | TEXT | 报修人 | 方总/刘瑞 |
| 6 | 报修时间 | DATE/TEXT | 创建时间 | 2026年5月6日 |
| 7 | 维修人员 | TEXT | 分派对象 | 蔡其恩/杨杉 |
| 8 | 维修跟进状态 | TEXT | 工单状态 | 已完成/待处理 |
| 9 | 跟进状态及结果描述 | TEXT | 处理结果 | 已修复 |
| 10 | 维修费用 | NUMERIC | 费用 | 0 |
| 11 | 维修完成时间 | DATE/TEXT | 完成时间 | 2026年5月6日 |
| 12 | 维修用时天数 | NUMERIC | 耗时 | 0 |
| 13 | 月份 | DATE/TEXT | 月份 | 2026年4月24日 |

---

## 核心逻辑

### 1. SLA分级规则

| 紧急程度 | SLA响应时限 | Agent动作 | 企微推送级别 |
|---------|-------------|-----------|-------------|
| 紧急！急需处理！ | 1小时内 | 立即@all推送 | 🚨 紧急（@all） |
| 紧急！一周内处理！ | 24小时内 | 企微提醒维修主管 | 📢 普通 |
| 不紧急！一月内处理！ | 3日内 | 静默记录，每日汇总 | 📝 静默 |

---

### 2. 自动分派算法

```python
def dispatch_workorder(unit_no, description, urgency):
    """
    根据报修描述自动分派维修人员
    
    Args:
        unit_no: 楼层/单元
        description: 报修细节描述
        urgency: 紧急程度
    
    Returns:
        str: 维修人员姓名
    """
    # 1. 确定专业领域
    if "电" in description or "跳闸" in description or "开关" in description:
        specialty = "电工"
        candidates = ["蔡其恩"]  # 电工名单
    elif "水" in description or "漏水" in description or "水管" in description:
        specialty = "水工"
        candidates = ["杨杉"]  # 水工名单
    else:
        specialty = "万能工"
        candidates = ["蔡其恩", "杨杉"]  # 万能工名单
    
    # 2. 选择维修人员（简化版：轮询分配）
    # TODO: 后期可增加工作量统计，选择当前工单最少的人员
    assignee = candidates[0]
    
    return assignee
```

---

### 3. SLA超时监控

```python
def check_sla_timeout():
    """
    检查待处理工单是否超时
    
    Returns:
        dict: 超时工单清单
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_repair = wb['🛠️报修情况汇总🛠️']
    
    today = datetime.now().date()
    
    timeout_orders = {
        "紧急超时": [],   # 紧急工单超过1小时
        "普通超时": [],   # 普通工单超过24小时
        "即将超时": []    # 接近超时
    }
    
    for row in ws_repair.iter_rows(min_row=2, values_only=True):
        status = row[7]  # 维修跟进状态
        
        if status == "待处理":
            unit_no = row[0]        # 楼层/单元
            urgency = row[1]        # 紧急程度
            description = row[2]    # 报修细节描述
            report_time = parse_excel_date(row[5])  # 报修时间
            
            # 计算已过时间
            elapsed_hours = (today - report_time).total_seconds() / 3600
            
            # 判断是否超时
            if urgency == "紧急！急需处理！":
                if elapsed_hours > 1:
                    timeout_orders["紧急超时"].append({
                        "楼层/单元": unit_no,
                        "紧急程度": urgency,
                        "报修细节描述": description,
                        "已过时间": f"{elapsed_hours:.1f}小时"
                    })
                elif elapsed_hours > 0.5:  # 接近超时（30分钟）
                    timeout_orders["即将超时"].append({
                        "楼层/单元": unit_no,
                        "紧急程度": urgency,
                        "报修细节描述": description,
                        "剩余时间": f"{1 - elapsed_hours:.1f}小时"
                    })
            
            elif urgency == "紧急！一周内处理！":
                if elapsed_hours > 24:
                    timeout_orders["普通超时"].append({
                        "楼层/单元": unit_no,
                        "紧急程度": urgency,
                        "报修细节描述": description,
                        "已过时间": f"{elapsed_hours:.1f}小时"
                    })
    
    return timeout_orders
```

---

### 4. 工单创建与分派流程

```python
def create_and_dispatch_workorder(unit_no, description, reporter, urgency="紧急！一周内处理！"):
    """
    创建并分派工单
    
    Args:
        unit_no: 楼层/单元
        description: 报修细节描述
        reporter: 报修人员
        urgency: 紧急程度（默认）
    
    Returns:
        dict: 工单信息
    """
    # 1. 自动分派维修人员
    assignee = dispatch_workorder(unit_no, description, urgency)
    
    # 2. 创建工单信息
    workorder = {
        "楼层/单元": unit_no,
        "紧急程度": urgency,
        "报修细节描述": description,
        "报修人员": reporter,
        "报修时间": datetime.now().strftime("%Y年%m月%d日"),
        "维修人员": assignee,
        "维修跟进状态": "待处理",
        "跟进状态及结果描述": "已分派，等待维修",
        "维修费用": 0,
        "维修完成时间": None,
        "维修用时天数": None,
        "客户评价": None,
        "评价详情": None
    }
    
    # 3. TODO: 写入Excel（需要xlsx skill支持）
    # append_to_excel('/Users/mac/美兰中心C+服务.xlsx', '🛠️报修情况汇总🛠️', workorder)
    
    # 4. 发送企微通知
    send_wecom_notification(assignee, workorder)
    
    return workorder
```

### 5. 工单完成确认流程

```python
def confirm_workorder_completion(unit_no, assignee, result_description, cost=0):
    """
    确认工单完成
    
    Args:
        unit_no: 楼层/单元
        assignee: 维修人员
        result_description: 维修结果描述
        cost: 维修费用（默认0）
    
    Returns:
        dict: 更新后的工单信息
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_repair = wb['🛠️报修情况汇总🛠️']
    
    today = datetime.now().date()
    
    # 1. 查找匹配的工单
    for row in ws_repair.iter_rows(min_row=2):
        if row[0].value == unit_no and row[6].value == assignee and row[7].value == "待处理":
            # 2. 更新工单状态
            row[7].value = "已完成"  # 维修跟进状态
            row[8].value = result_description  # 跟进状态及结果描述
            row[9].value = cost  # 维修费用
            row[10].value = today.strftime("%Y年%m月%d日")  # 维修完成时间
            
            # 计算维修用时天数
            report_time = parse_excel_date(row[5].value)  # 报修时间
            days_used = (today - report_time).days
            row[11].value = days_used  # 维修用时天数
            
            # 3. 保存Excel
            wb.save('/Users/mac/美兰中心C+服务.xlsx')
            
            # 4. 发送完成通知
            notification = {
                "楼层/单元": unit_no,
                "维修人员": assignee,
                "维修结果": result_description,
                "维修费用": cost,
                "完成时间": today.strftime("%Y年%m月%d日"),
                "用时天数": days_used
            }
            send_completion_notification(notification)
            
            return notification
    
    return None
```

### 6. 工单状态更新

```python
def update_workorder_status(unit_no, assignee, new_status, notes=""):
    """
    更新工单状态
    
    Args:
        unit_no: 楼层/单元
        assignee: 维修人员
        new_status: 新状态（待处理/处理中/已完成/已取消）
        notes: 状态更新说明
    
    Returns:
        bool: 是否更新成功
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_repair = wb['🛠️报修情况汇总🛠️']
    
    for row in ws_repair.iter_rows(min_row=2):
        if row[0].value == unit_no and row[6].value == assignee:
            # 更新状态
            row[7].value = new_status
            
            # 更新结果描述（追加说明）
            current_desc = row[8].value or ""
            update_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
            row[8].value = f"{current_desc}\n{update_time} 状态更新：{new_status}。{notes}"
            
            wb.save('/Users/mac/美兰中心C+服务.xlsx')
            return True
    
    return False
```

### 7. 维修评价系统

```python
def add_workorder_feedback(unit_no, assignee, rating, comment=""):
    """
    添加工单评价
    
    Args:
        unit_no: 楼层/单元
        assignee: 维修人员
        rating: 评分（1-5）
        comment: 评价详情
    
    Returns:
        bool: 是否添加成功
    """
    wb = openpyxl.load_workbook('/Users/mac/美兰中心C+服务.xlsx')
    ws_repair = wb['🛠️报修情况汇总🛠️']
    
    for row in ws_repair.iter_rows(min_row=2):
        if row[0].value == unit_no and row[6].value == assignee and row[7].value == "已完成":
            # 添加评价
            row[12].value = rating  # 客户评价（需要扩展Excel列）
            row[13].value = comment  # 评价详情（需要扩展Excel列）
            
            wb.save('/Users/mac/美兰中心C+服务.xlsx')
            
            # 发送评价通知
            send_feedback_notification({
                "楼层/单元": unit_no,
                "维修人员": assignee,
                "评分": rating,
                "评价": comment
            })
            
            return True
    
    return False
```

---

## 企微推送模板

### 紧急工单分派

```
━━━━━━━━━━━━━━━
【紧急工单分派】

📍 位置：{unit_no}
🚨 紧急程度：{urgency}
📝 报修描述：{description}
👤 报修人：{reporter}
⏰ 报修时间：{report_time}

👷 维修人员：{assignee}
⚡ 请立即处理！

━━━━━━━━━━━━━━━
```

### SLA超时升级

```
⚠️⚠️⚠️ 【SLA超时升级】⚠️⚠️⚠️

📍 位置：{unit_no}
🚨 紧急程度：{urgency}
📝 报修描述：{description}
⏰ 已过时间：{elapsed_hours}小时

@all 请维修主管立即介入！

━━━━━━━━━━━━━━━
```

---

## 执行流程

```
Step 1 → 读取Excel报修汇总表
         工作表：🛠️报修情况汇总🛠️
         筛选：维修跟进状态 = '待处理'

Step 2 → SLA超时检查
         ├─ 紧急工单：超过1小时 → 立即@all升级
         ├─ 普通工单：超过24小时 → 提醒维修主管
         └─ 即将超时：提前预警

Step 3 → 自动分派（新工单）
         ├─ 分析报修描述 → 确定专业领域
         ├─ 选择维修人员 → 轮询分配
         └─ 发送企微通知

Step 4 → 状态更新
         记录处理进度，更新工单状态

Step 5 → 定时监控
         每小时检查一次SLA状态
```

---

## 定时任务配置

```json
{
  "name": "工单SLA监控",
  "schedule": {
    "kind": "cron",
    "expr": "0 * * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "检查待处理工单的SLA状态，发现超时工单立即升级推送"
  },
  "sessionTarget": "isolated"
}
```

---

## 手动触发方式

1. **企微 @提及**: `@企服助手 创建工单 {位置} {描述}`
2. **OpenClaw指令**: `检查工单状态`

---

## 配置参数

```json
{
  "workorder_dispatch": {
    "excel_path": "/Users/mac/美兰中心C+服务.xlsx",
    "sla_urgent_hours": 1,
    "sla_normal_hours": 24,
    "wecom_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "maintenance_staff": {
      "电工": ["蔡其恩"],
      "水工": ["杨杉"],
      "万能工": ["蔡其恩", "杨杉"]
    }
  }
}
```

---

## 使用示例

### 示例1：检查工单状态

**用户输入**: `@企服助手 检查工单状态`

**输出**:
```
━━━━━━━━━━━━━━━
【工单状态监控】2026-05-28

━━━ 待处理工单 ━━━
共2个待处理

1. T1-9F女厕
   紧急程度：紧急！一周内处理！
   报修描述：女厕左手第二扇门打不开
   维修人员：（待分派）
   状态：配件采购中......

2. T1-909
   紧急程度：不紧急！一月内处理！
   报修描述：单元玻璃爆破
   维修人员：杨杉
   状态：玻璃自爆联系维保更换中......

━━━ 已完成工单 ━━━
共1个已完成

━━━ 统计 ━━━
总工单数：3个
已完成：1个 | 待处理：2个

⚡ 操作链接：[腾讯文档-报修汇总]
━━━━━━━━━━━━━━━
```

---

## 后续扩展接口

1. **工单评价系统** - 企业对维修服务进行评价
2. **维修知识库** - 常见问题解决方案库
3. **预防性维护** - 基于历史数据预测设备故障
4. **工作量统计** - 维修人员工作量和绩效分析

---

## 注意事项

1. **日期格式解析** - Excel日期格式多样，需要统一解析
2. **维修人员排班** - 需要考虑维修人员的休假、调班情况
3. **紧急工单升级** - 紧急工单超时必须立即@all通知
4. **工单关闭流程** - 需要确认维修完成后再关闭工单

---

**当前状态**: 技能已调整，数据源已映射到真实Excel报修汇总表。

**核心改进**: 从独立的知识库查询 → 改为直接读取Excel报修汇总表 + SLA超时监控逻辑。