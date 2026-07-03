#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工伤索赔文档生成脚本

功能：
1. 生成工伤认定申请书
2. 生成工伤待遇计算表
3. 生成索赔材料清单

使用方式：
  命令行参数模式：
    python generate_injury_claim_docs.py --output-dir <输出目录> [参数...]

  JSON配置文件模式（推荐）：
    python generate_injury_claim_docs.py --config <案件信息JSON> --output-dir <输出目录>

参数说明：
  --applicant-name        申请人姓名
  --applicant-gender      申请人性别
  --applicant-id          申请人身份证号
  --applicant-phone       申请人电话
  --applicant-address     申请人住址
  --employer-name         用人单位全称
  --employer-address      用人单位地址
  --employer-legal-rep    法定代表人姓名
  --employer-phone        用人单位电话
  --city                  所在城市（用于确定地区标准）
  --injury-date           受伤日期（YYYY-MM-DD）
  --injury-type           工伤情形类型（1-7对应第14条第1-7项，v1-v3对应第15条）
  --injury-description    受伤经过描述
  --diagnosis             诊断结果
  --monthly-salary        月工资标准
  --disability-level      伤残等级（1-10，如已鉴定）
  --work-start-date       入职日期
  --insured               是否已缴工伤保险（true/false）
  --output-dir            输出目录

JSON配置文件格式：
{
  "applicant_name": "张三",
  "applicant_gender": "男",
  "applicant_id": "110101199001011234",
  "applicant_phone": "13800138000",
  "applicant_address": "北京市海淀区XX路XX号",
  "employer_name": "XX科技有限公司",
  "employer_address": "北京市朝阳区XX路XX号",
  "employer_legal_rep": "李四",
  "employer_phone": "010-12345678",
  "city": "北京",
  "injury_date": "2024-03-15",
  "injury_type": "1",
  "injury_description": "申请人在车间操作机器时，右手被卷入机器导致右手食指、中指骨折",
  "diagnosis": "右手食指、中指骨折",
  "monthly_salary": 8000,
  "disability_level": 9,
  "work_start_date": "2022-06-01",
  "insured": true,
  "treatment_start_date": "2024-03-15",
  "treatment_end_date": "2024-06-15",
  "hospital_days": 15,
  "recurrent_treatment": false,
  "monthly_salary_before": 8000,
  "resigned": false
}
"""

import argparse
import json
import os
from datetime import datetime, date


# 一次性伤残补助金月数（1-10级）
DISABILITY_SUBSIDY_MONTHS = {
    1: 27, 2: 25, 3: 23, 4: 21,
    5: 18, 6: 16, 7: 13, 8: 11,
    9: 9, 10: 7
}

# 伤残津贴比例（1-6级，按月发放）
DISABILITY_ALLOWANCE_RATE = {
    1: 0.90, 2: 0.85, 3: 0.80, 4: 0.75,
    5: 0.70, 6: 0.60
}

# 生活护理费比例
NURSING_CARE_RATE = {
    "完全不能自理": 0.50,
    "大部分不能自理": 0.40,
    "部分不能自理": 0.30
}

# 一次性工伤医疗补助金月数（部分主要城市）
MEDICAL_SUBSIDY_MONTHS = {
    "北京": {5: 18, 6: 15, 7: 12, 8: 9, 9: 6, 10: 3},
    "上海": {5: 18, 6: 15, 7: 12, 8: 9, 9: 6, 10: 3},
    "广东": {5: 20, 6: 16, 7: 12, 8: 8, 9: 4, 10: 2},
    "江苏": {5: 20, 6: 16, 7: 12, 8: 8, 9: 4, 10: 2},
    "浙江": {5: 24, 6: 18, 7: 12, 8: 8, 9: 4, 10: 2},
    "山东": {5: 22, 6: 18, 7: 13, 8: 10, 9: 7, 10: 4},
    "四川": {5: 18, 6: 16, 7: 10, 8: 8, 9: 6, 10: 4},
    "河南": {5: 20, 6: 16, 7: 10, 8: 8, 9: 6, 10: 4},
}

# 一次性伤残就业补助金月数（部分主要城市）
EMPLOYMENT_SUBSIDY_MONTHS = {
    "北京": {5: 18, 6: 15, 7: 12, 8: 9, 9: 6, 10: 3},
    "上海": {5: 18, 6: 15, 7: 12, 8: 9, 9: 6, 10: 3},
    "广东": {5: 20, 6: 16, 7: 12, 8: 8, 9: 4, 10: 2},
    "江苏": {5: 20, 6: 16, 7: 12, 8: 8, 9: 4, 10: 2},
    "浙江": {5: 24, 6: 18, 7: 12, 8: 8, 9: 4, 10: 2},
    "山东": {5: 36, 6: 30, 7: 20, 8: 16, 9: 12, 10: 8},
    "四川": {5: 28, 6: 24, 7: 16, 8: 12, 9: 8, 10: 4},
    "河南": {5: 36, 6: 30, 7: 20, 8: 16, 9: 12, 10: 6},
}

# 工伤情形类型映射
INJURY_TYPE_MAP = {
    "1": "在工作时间和工作场所内，因工作原因受到事故伤害",
    "2": "工作时间前后在工作场所内，从事与工作有关的预备性或收尾性工作受到事故伤害",
    "3": "在工作时间和工作场所内，因履行工作职责受到暴力等意外伤害",
    "4": "患职业病",
    "5": "因工外出期间，由于工作原因受到伤害",
    "6": "在上下班途中，受到非本人主要责任的交通事故伤害",
    "7": "法律、行政法规规定应当认定为工伤的其他情形",
    "v1": "在工作时间和工作岗位，突发疾病死亡或在48小时之内经抢救无效死亡（视同工伤）",
    "v2": "在抢险救灾等维护国家利益、公共利益活动中受到伤害（视同工伤）",
    "v3": "职工原在军队服役，因战、因公负伤致残，到用人单位后旧伤复发（视同工伤）",
}

# 参考社平工资（2023年度部分城市，需每年更新）
SOCIAL_AVG_SALARY = {
    "北京": 12500, "上海": 12300, "广东": 10500,
    "深圳": 13700, "江苏": 9500, "浙江": 9000,
    "山东": 8000, "四川": 7500, "河南": 6500,
}


def calc_months_between(start_date_str, end_date_str):
    """计算两个日期之间的月数"""
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        months = (end.year - start.year) * 12 + (end.month - start.month)
        if end.day < start.day:
            months -= 1
        return max(months, 0)
    except Exception:
        return 0


def format_money(amount):
    """格式化金额"""
    return f"{amount:,.0f}"


def calculate_compensation(case):
    """计算工伤待遇"""
    results = []
    total = 0

    level = case.get("disability_level")
    salary = case.get("monthly_salary", 0)
    city = case.get("city", "")
    avg_salary = SOCIAL_AVG_SALARY.get(city, 8000)

    # 本人工资封顶保底
    capped_salary = min(max(salary, avg_salary * 0.6), avg_salary * 3)

    # 停工留薪期工资
    treatment_start = case.get("treatment_start_date", case.get("injury_date"))
    treatment_end = case.get("treatment_end_date")
    if treatment_start and treatment_end:
        stop_work_months = calc_months_between(treatment_start, treatment_end)
        if stop_work_months > 0:
            stop_work_pay = salary * stop_work_months
            results.append({
                "item": f"停工留薪期工资（{stop_work_months}个月）",
                "formula": f"月工资{format_money(salary)}元 × {stop_work_months}个月",
                "amount": stop_work_pay,
                "payer": "用人单位"
            })
            total += stop_work_pay

    # 住院伙食补助费
    hospital_days = case.get("hospital_days", 0)
    if hospital_days > 0:
        food_subsidy = int(avg_salary / 21.75 * 0.7 * hospital_days)
        results.append({
            "item": f"住院伙食补助费（{hospital_days}天）",
            "formula": f"社平工资/21.75 × 70% × {hospital_days}天",
            "amount": food_subsidy,
            "payer": "工伤保险基金"
        })
        total += food_subsidy

    # 一次性伤残补助金
    if level and level in DISABILITY_SUBSIDY_MONTHS:
        months = DISABILITY_SUBSIDY_MONTHS[level]
        subsidy = capped_salary * months
        results.append({
            "item": f"一次性伤残补助金（{level}级，{months}个月）",
            "formula": f"本人工资{format_money(capped_salary)}元 × {months}个月",
            "amount": subsidy,
            "payer": "工伤保险基金"
        })
        total += subsidy

    # 伤残津贴（1-6级，按月）
    if level and level in DISABILITY_ALLOWANCE_RATE:
        rate = DISABILITY_ALLOWANCE_RATE[level]
        monthly_allowance = capped_salary * rate
        results.append({
            "item": f"伤残津贴（{level}级，按月发放）",
            "formula": f"本人工资{format_money(capped_salary)}元 × {rate*100:.0f}%",
            "amount": monthly_allowance,
            "payer": "工伤保险基金（1-4级）/ 用人单位（5-6级）",
            "monthly": True
        })

    # 一次性工伤医疗补助金和伤残就业补助金（5-10级，解除合同时）
    if level and 5 <= level <= 10 and case.get("resigned", False):
        city_key = city
        # 尝试匹配地区
        matched_city = None
        for key in MEDICAL_SUBSIDY_MONTHS:
            if key in city or city in key:
                matched_city = key
                break
        if matched_city:
            med_months = MEDICAL_SUBSIDY_MONTHS[matched_city].get(level, 0)
            emp_months = EMPLOYMENT_SUBSIDY_MONTHS[matched_city].get(level, 0)
            if med_months > 0:
                med_subsidy = avg_salary * med_months
                results.append({
                    "item": f"一次性工伤医疗补助金（{level}级，{med_months}个月）",
                    "formula": f"社平工资{format_money(avg_salary)}元 × {med_months}个月",
                    "amount": med_subsidy,
                    "payer": "工伤保险基金"
                })
                total += med_subsidy
            if emp_months > 0:
                emp_subsidy = avg_salary * emp_months
                results.append({
                    "item": f"一次性伤残就业补助金（{level}级，{emp_months}个月）",
                    "formula": f"社平工资{format_money(avg_salary)}元 × {emp_months}个月",
                    "amount": emp_subsidy,
                    "payer": "用人单位"
                })
                total += emp_subsidy
        else:
            results.append({
                "item": f"一次性工伤医疗补助金和伤残就业补助金",
                "formula": f"请查询{city}当地标准",
                "amount": 0,
                "payer": "基金/用人单位",
                "note": f"未找到{city}的标准，请查询当地最新规定"
            })

    return results, total


def generate_recognition_application(case):
    """生成工伤认定申请书"""
    today = datetime.now().strftime("%Y年%m月%d日")
    city = case.get("city", "")
    injury_type = case.get("injury_type", "1")
    injury_desc = INJURY_TYPE_MAP.get(injury_type, "工伤")

    content = f"""# 工伤认定申请书

**申请人**：{case.get("applicant_name", "（待填）")}，性别：{case.get("applicant_gender", "（待填）")}

身份证号：{case.get("applicant_id", "（待填）")}

住址：{case.get("applicant_address", "（待填）")}

电话：{case.get("applicant_phone", "（待填）")}

**用人单位**：{case.get("employer_name", "（待填）")}

统一社会信用代码：{case.get("employer_credit_code", "（待填）")}

住所地：{case.get("employer_address", "（待填）")}

法定代表人：{case.get("employer_legal_rep", "（待填）")}

电话：{case.get("employer_phone", "（待填）")}

---

## 请求事项

请求依法认定申请人于{case.get("injury_date", "（待填）")}所受伤害为工伤。

## 事故发生经过

{case.get("injury_description", "（请详细描述事故发生的时间、地点、经过及受伤部位）")}

**工伤情形**：{injury_desc}

**受伤时间**：{case.get("injury_date", "（待填）")}

**受伤部位及诊断**：{case.get("diagnosis", "（待填）")}

**就诊医院**：{case.get("hospital_name", "（待填）")}

## 申请人陈述

申请人系{case.get("employer_name", "用人单位")}员工，于{case.get("work_start_date", "（待填）")}入职，从事{case.get("job_position", "（待填）")}工作，月工资{format_money(case.get("monthly_salary", 0))}元。

{case.get("injury_description", "")}

事故发生后，申请人立即前往{case.get("hospital_name", "医院")}就诊，经诊断为：{case.get("diagnosis", "（待填）")}。

申请人认为，上述伤害符合《工伤保险条例》第{("14" if not injury_type.startswith("v") else "15")}条第{("1" if injury_type == "1" else "")}项之规定，应当认定为工伤。为维护申请人的合法权益，特向贵局申请工伤认定，请依法予以认定。

此致

{city}人力资源和社会保障局

**申请人**：{case.get("applicant_name", "（待填）")}（签名）

{today}

---

## 附件清单

1. 申请人身份证复印件
2. 劳动合同（复印件）
3. 医疗诊断证明（复印件）
4. 病历资料（复印件）
5. 事故现场照片（如有）
6. 目击证人证言（如有）
7. 其他相关证据材料
"""

    return content


def generate_compensation_table(case):
    """生成待遇计算表"""
    results, total = calculate_compensation(case)
    today = datetime.now().strftime("%Y年%m月%d日")
    city = case.get("city", "")
    level = case.get("disability_level")
    avg_salary = SOCIAL_AVG_SALARY.get(city, 8000)

    level_text = f"{level}级" if level else "未鉴定"

    content = f"""# 工伤保险待遇计算表

申请人：{case.get("applicant_name", "（待填）")}

用人单位：{case.get("employer_name", "（待填）")}

所在地区：{city}

生成日期：{today}

---

## 基础信息

| 项目 | 内容 |
|------|------|
| 受伤日期 | {case.get("injury_date", "（待填）")} |
| 诊断结果 | {case.get("diagnosis", "（待填）")} |
| 伤残等级 | {level_text} |
| 月工资标准 | ¥{format_money(case.get("monthly_salary", 0))} |
| 当地社平工资（参考） | ¥{format_money(avg_salary)} |
| 是否缴工伤保险 | {"是" if case.get("insured") else "否"} |

## 待遇项目明细

| 序号 | 待遇项目 | 计算方式 | 金额(元) | 支付主体 |
|------|---------|---------|---------|---------|
"""

    for i, r in enumerate(results, 1):
        monthly_mark = "/月" if r.get("monthly") else ""
        note = f"（{r['note']}）" if r.get("note") else ""
        content += f"| {i} | {r['item']}{note} | {r['formula']} | {format_money(r['amount'])}{monthly_mark} | {r['payer']} |\n"

    if not results:
        content += "| - | 暂无计算数据，请补充伤残等级等信息 | - | - | - |\n"

    # 合计行（不含按月支付项）
    one_time_total = sum(r["amount"] for r in results if not r.get("monthly"))
    content += f"| **合计** | 一次性支付项目合计 | | **{format_money(one_time_total)}** | |\n"

    content += f"""
## 计算说明

1. **本人工资**：指工伤前12个月平均月缴费工资，封顶为社平工资300%，保底为社平工资60%
2. **社平工资**：统筹地区上年度职工月平均工资，每年更新（本表使用参考值，实际以当地公布数据为准）
3. **一次性工伤医疗补助金和伤残就业补助金**：仅5-10级伤残职工解除/终止劳动合同时支付
4. **伤残津贴**：1-4级退出工作岗位按月领取；5-6级用人单位难以安排工作时按月领取
5. **停工留薪期**：一般不超过12个月，伤情严重经批准可延长但不超过12个月

> **注意：** 以上计算基于参考数据，实际金额以当地社保经办机构核定为准。社平工资和地区标准每年更新，请查询当地最新数据。

## 未参保情况说明

{"用人单位已缴纳工伤保险，大部分待遇由工伤保险基金支付。" if case.get("insured") else "**用人单位未缴纳工伤保险，全部待遇由用人单位按上述标准支付。**"}
"""

    return content


def generate_document_checklist(case):
    """生成索赔材料清单"""
    injury_type = case.get("injury_type", "1")
    today = datetime.now().strftime("%Y年%m月%d日")

    content = f"""# 工伤索赔材料清单

申请人：{case.get("applicant_name", "（待填）")}

用人单位：{case.get("employer_name", "（待填）")}

生成日期：{today}

---

## 一、基础材料

- [ ] 身份证复印件（正反面，2份）
- [ ] 劳动合同（原件+复印件）
- [ ] 工资银行流水（近12个月）
- [ ] 社保缴纳记录
- [ ] 用人单位工商信息（国家企业信用信息公示系统截图）

## 二、工伤认定材料

- [ ] 工伤认定申请表
- [ ] 事故发生经过书面说明
- [ ] 首次门诊/急诊病历
- [ ] 住院病历（含入院记录、手术记录、出院小结）
- [ ] 诊断证明书
- [ ] 影像资料（X光/CT/MRI胶片及报告）
"""

    # 根据工伤情形补充
    if injury_type == "6":  # 上下班途中交通事故
        content += """## 三、交通事故专项材料（上下班途中工伤）

- [ ] 交通事故责任认定书
- [ ] 居住证明（租房合同/房产证/居住证）
- [ ] 上下班路线说明及地图标注
- [ ] 正常上下班时间证明（考勤/排班表）
- [ ] 事故现场照片
"""
    elif injury_type == "5":  # 因工外出
        content += """## 三、因工外出专项材料

- [ ] 出差审批/派遣证明
- [ ] 出差行程安排（邮件/通知截图）
- [ ] 机票/火车票/住宿发票
- [ ] 同行人员证言（如有）
"""
    elif injury_type == "4":  # 职业病
        content += """## 三、职业病专项材料

- [ ] 职业病诊断证明书
- [ ] 职业史证明
- [ ] 岗位危害因素检测报告
- [ ] 历年职业健康体检记录
"""
    elif injury_type == "3":  # 暴力伤害
        content += """## 三、暴力伤害专项材料

- [ ] 公安机关案件处理记录或证明
- [ ] 法医伤情鉴定书
- [ ] 证明因履行工作职责的证据
- [ ] 目击同事证言
"""
    elif injury_type == "v1":  # 突发疾病死亡
        content += """## 三、突发疾病死亡专项材料

- [ ] 120出车记录
- [ ] 急诊病历（含接诊时间）
- [ ] 抢救记录
- [ ] 死亡证明
- [ ] 48小时内死亡的时间证明
- [ ] 证明在工作时间和工作岗位突发疾病的证据
"""
    else:
        content += """## 三、事故伤害专项材料

- [ ] 事故现场照片/视频
- [ ] 用人单位事故报告（如有）
- [ ] 目击同事证言
- [ ] 监控录像（如有）
"""

    content += f"""
## 四、劳动能力鉴定材料（如需鉴定）

- [ ] 劳动能力鉴定申请表
- [ ] 工伤认定决定书（复印件）
- [ ] 完整病历资料
- [ ] 诊断证明书
- [ ] 影像资料及报告
- [ ] 身份证复印件
- [ ] 近期免冠照片

## 五、工伤保险待遇申领材料

- [ ] 工伤保险待遇申领表
- [ ] 工伤认定决定书（复印件）
- [ ] 劳动能力鉴定结论书（复印件）
- [ ] 医疗费发票（原件）
- [ ] 医疗费明细清单
- [ ] 身份证及银行卡复印件
- [ ] 用人单位参保证明

---

> **材料整理规范：**
> 1. 所有材料提交复印件，原件自行保管
> 2. 按上述顺序排列装订
> 3. 每页注明"复印件与原件一致"并签字
> 4. 编制证据目录，注明证明目的
"""

    return content


def main():
    parser = argparse.ArgumentParser(
        description="工伤索赔文档生成脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--config", help="案件信息JSON配置文件路径")
    parser.add_argument("--output-dir", default=".", help="输出目录")
    parser.add_argument("--applicant-name", help="申请人姓名")
    parser.add_argument("--applicant-gender", help="申请人性别")
    parser.add_argument("--applicant-id", help="身份证号")
    parser.add_argument("--applicant-phone", help="联系电话")
    parser.add_argument("--applicant-address", help="住址")
    parser.add_argument("--employer-name", help="用人单位全称")
    parser.add_argument("--employer-address", help="用人单位地址")
    parser.add_argument("--employer-legal-rep", help="法定代表人")
    parser.add_argument("--employer-phone", help="用人单位电话")
    parser.add_argument("--city", help="所在城市")
    parser.add_argument("--injury-date", help="受伤日期 YYYY-MM-DD")
    parser.add_argument("--injury-type", default="1", help="工伤情形类型")
    parser.add_argument("--injury-description", help="受伤经过")
    parser.add_argument("--diagnosis", help="诊断结果")
    parser.add_argument("--monthly-salary", type=int, help="月工资标准")
    parser.add_argument("--disability-level", type=int, help="伤残等级(1-10)")
    parser.add_argument("--work-start-date", help="入职日期")
    parser.add_argument("--insured", choices=["true", "false"], help="是否缴工伤保险")
    parser.add_argument("--treatment-start-date", help="治疗开始日期")
    parser.add_argument("--treatment-end-date", help="治疗结束日期")
    parser.add_argument("--hospital-days", type=int, help="住院天数")
    parser.add_argument("--resided", choices=["true", "false"], help="是否已离职")

    args = parser.parse_args()

    # 加载案件信息
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            case = json.load(f)
    else:
        case = {}
        for key in vars(args):
            val = getattr(args, key)
            if val is not None and key not in ("config", "output_dir"):
                if key in ("monthly_salary", "disability_level", "hospital_days"):
                    case[key] = int(val)
                elif key == "insured" or key == "resigned":
                    case[key] = (val == "true")
                else:
                    case[key] = val

    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)

    # 生成文档
    app_content = generate_recognition_application(case)
    comp_content = generate_compensation_table(case)
    doc_content = generate_document_checklist(case)

    # 写入文件
    app_path = os.path.join(args.output_dir, "工伤认定申请书.md")
    comp_path = os.path.join(args.output_dir, "工伤待遇计算表.md")
    doc_path = os.path.join(args.output_dir, "索赔材料清单.md")

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_content)
    print(f"工伤认定申请书已生成：{app_path}")

    with open(comp_path, "w", encoding="utf-8") as f:
        f.write(comp_content)
    print(f"工伤待遇计算表已生成：{comp_path}")

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(doc_content)
    print(f"索赔材料清单已生成：{doc_path}")

    # 打印待遇合计
    _, total = calculate_compensation(case)
    print(f"一次性支付待遇总金额：¥{format_money(total)}")

    print(f"输出目录：{os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    main()
