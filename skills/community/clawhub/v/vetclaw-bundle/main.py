"""
VetClaw — 宠物医院AI技能套装 Web应用
提供52个宠物医院自动化技能的Web界面
"""
import os
import json
import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="VetClaw", version="1.0.0", description="宠物医院AI技能套装")

BASE_DIR = Path(__file__).parent
CONFIG_DIR = BASE_DIR / "config"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DB_PATH = BASE_DIR / "data" / "vetclaw.db"

# Ensure dirs
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
(DB_PATH.parent).mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ─── Knowledge Base ───
def load_knowledge_base() -> dict:
    kb_file = CONFIG_DIR / "vet-knowledge-base.json"
    if kb_file.exists():
        return json.loads(kb_file.read_text(encoding="utf-8"))
    return {}

def load_config() -> dict:
    cfg_file = CONFIG_DIR / "vet-config.yaml"
    if cfg_file.exists():
        try:
            import yaml
            return yaml.safe_load(cfg_file.read_text(encoding="utf-8")) or {}
        except ImportError:
            pass
    return {"clinic": {"name": "VetClaw宠物医院", "address": "待配置", "phone": "待配置",
            "hours": {"weekday": "09:00-21:00", "weekend": "10:00-18:00"}}}

# ─── Database ───
def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        wechat TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER REFERENCES clients(id),
        name TEXT NOT NULL,
        species TEXT,
        breed TEXT,
        age TEXT,
        gender TEXT,
        neutered INTEGER DEFAULT 0,
        weight REAL,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER REFERENCES pets(id),
        client_id INTEGER REFERENCES clients(id),
        doctor TEXT,
        service_type TEXT,
        appointment_time TEXT,
        status TEXT DEFAULT 'pending',
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_id INTEGER REFERENCES pets(id),
        client_id INTEGER REFERENCES clients(id),
        doctor TEXT,
        symptoms TEXT,
        diagnosis TEXT,
        treatment TEXT,
        prescription TEXT,
        notes TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        quantity INTEGER DEFAULT 0,
        unit TEXT,
        expiry_date TEXT,
        min_stock INTEGER DEFAULT 5,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT,
        skill_used TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    """)
    conn.commit()
    conn.close()

init_db()

# ─── DeepSeek LLM (optional) ───
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

def llm_chat(prompt: str, system: str = "") -> str:
    """Call DeepSeek API if configured, else return None"""
    if not DEEPSEEK_API_KEY:
        return None
    try:
        import httpx
        resp = httpx.post("https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [
                {"role": "system", "content": system or "你是VetClaw宠物医院AI助手。"},
                {"role": "user", "content": prompt}
            ], "temperature": 0.3}, timeout=30)
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return None

# ─── Skill Handlers ───
SKILL_REGISTRY = {}

def register_skill(skill_id):
    def decorator(fn):
        SKILL_REGISTRY[skill_id] = fn
        return fn
    return decorator

@register_skill("vet-intake")
def handle_intake(message: str, config: dict) -> str:
    """新客户信息采集"""
    # Parse structured info from message
    info = {}
    patterns = {
        "name": r"(?:主人|客户|姓名)[：:]\s*(\S+)",
        "phone": r"(?:电话|手机|联系方式)[：:]\s*(1[3-9]\d{9})",
        "pet_name": r"(?:宠物名?|猫|狗)[叫是]?\s*(\S+)",
        "species": r"(猫|狗|兔|仓鼠|鸟|龟|蛇)",
        "breed": r"(?:品种|品)[：:]\s*(\S+)",
        "age": r"(\d+)\s*(?:岁|个月|月)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, message)
        if m:
            info[key] = m.group(1)

    if info.get("phone") and info.get("pet_name"):
        conn = get_db()
        try:
            cur = conn.execute("INSERT INTO clients (name, phone) VALUES (?, ?)",
                             (info.get("name", "未填写"), info["phone"]))
            client_id = cur.lastrowid
            conn.execute("""INSERT INTO pets (client_id, name, species, breed, age)
                          VALUES (?, ?, ?, ?, ?)""",
                        (client_id, info["pet_name"], info.get("species", ""),
                         info.get("breed", ""), info.get("age", "")))
            conn.commit()
            return (f"✅ 新客户建档成功！\n"
                   f"客户：{info.get('name', '未填写')} | 电话：{info['phone']}\n"
                   f"宠物：{info['pet_name']} | 种类：{info.get('species', '未填写')}\n"
                   f"品种：{info.get('breed', '未填写')} | 年龄：{info.get('age', '未填写')}\n\n"
                   f"下一步可「预约挂号」安排就诊。")
        finally:
            conn.close()

    return ("📋 新客户信息采集\n\n"
           "请提供以下信息（用中文冒号分隔）：\n"
           "主人：张三\n"
           "电话：13800138000\n"
           "宠物名：旺财\n"
           "种类：狗\n"
           "品种：金毛\n"
           "年龄：3岁")

@register_skill("vet-appointment")
def handle_appointment(message: str, config: dict) -> str:
    """预约挂号"""
    # Parse time
    time_match = re.search(r"(今|明|后)?天?\s*(上午|下午|晚上)?\s*(\d{1,2})[：:点](\d{2})?", message)
    service_match = re.search(r"(体检|疫苗|绝育|洗牙|看病|急诊|驱虫|手术|复查)", message)
    pet_match = re.search(r"(?:给|帮)?\s*(\S+?)\s*(?:预约|挂号)", message)

    if time_match:
        day_offset = 0
        if time_match.group(1) == "明":
            day_offset = 1
        elif time_match.group(1) == "后":
            day_offset = 2
        hour = int(time_match.group(3))
        minute = int(time_match.group(4) or "0")
        period = time_match.group(2) or ""
        if period in ("下午", "晚上") and hour < 12:
            hour += 12
        target_date = datetime.now() + timedelta(days=day_offset)
        time_str = f"{target_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}"
        service = service_match.group(1) if service_match else "看病"

        conn = get_db()
        try:
            conn.execute("""INSERT INTO appointments (pet_id, client_id, doctor, service_type,
                          appointment_time, status) VALUES (1, 1, '待分配', ?, ?, 'confirmed')""",
                        (service, time_str))
            conn.commit()
            return (f"✅ 预约成功！\n"
                   f"服务：{service}\n"
                   f"时间：{time_str}\n"
                   f"状态：已确认\n\n"
                   f"请提前10分钟到院，如有变动请提前通知。")
        finally:
            conn.close()

    return ("📅 预约挂号\n\n"
           "请告诉我：\n"
           "1. 宠物名字\n"
           "2. 预约时间（如：明天下午3点）\n"
           "3. 服务类型（体检/疫苗/绝育/看病/驱虫）\n\n"
           "示例：给旺财预约明天下午3点疫苗")

@register_skill("vet-emergency")
def handle_emergency(message: str, config: dict) -> str:
    """急诊分流 - 症状紧急程度判断"""
    RED_FLAGS = ["抽搐", "大出血", "呼吸困难", "休克", "倒地不起", "大量吐血", "难产", "中毒"]
    YELLOW_FLAGS = ["呕吐不止", "腹泻带血", "不吃东西超过24小时", "精神萎靡", "发烧", "骨折",
                    "眼睛肿胀", "排尿困难", "腹胀"]
    GREEN_FLAGS = ["轻微咳嗽", "打喷嚏", "少量眼屎", "皮肤瘙痒", "掉毛", "耳螨"]

    msg_lower = message
    for flag in RED_FLAGS:
        if flag in msg_lower:
            return (f"🚨 紧急！检测到「{flag}」症状\n\n"
                   f"⚠️ 请立即带宠物来院就诊！\n"
                   f"急诊电话：{config.get('clinic',{}).get('phone','请拨打医院电话')}\n\n"
                   f"急救建议：\n"
                   f"- 保持宠物安静，避免移动\n"
                   f"- 如有出血，用干净布压迫止血\n"
                   f"- 如疑似中毒，保留呕吐物或毒物样本\n"
                   f"- 全程不要给宠物喂食喂水")

    for flag in YELLOW_FLAGS:
        if flag in msg_lower:
            return (f"⚠️ 中等紧急：检测到「{flag}」症状\n\n"
                   f"建议今天内就诊。如症状恶化（精神极差、持续呕吐、出血），请立即来急诊。\n\n"
                   f"就诊前注意：\n"
                   f"- 记录症状持续时间\n"
                   f"- 最近饮食变化\n"
                   f"- 是否接触过异常物品\n\n"
                   f"📞 可先电话咨询：{config.get('clinic',{}).get('phone','待配置')}")

    for flag in GREEN_FLAGS:
        if flag in msg_lower:
            return (f"ℹ️ 非紧急：检测到「{flag}」症状\n\n"
                   f"建议预约常规门诊即可。\n"
                   f"如症状持续超过3天或加重，请及时就诊。\n\n"
                   f"可输入「预约」安排就诊时间。")

    return ("🏥 急诊分流\n\n"
           "请描述宠物症状，例如：\n"
           "- 「我的狗一直在抽搐」\n"
           "- 「猫呕吐了3次」\n"
           "- 「狗狗耳朵很痒」\n\n"
           f"紧急情况请直接拨打：{config.get('clinic',{}).get('phone','医院电话')}")

@register_skill("vet-phone-ai")
def handle_phone_ai(message: str, config: dict) -> str:
    """AI电话接听 - 意图识别"""
    clinic = config.get("clinic", {})
    intents = {
        "预约": handle_appointment,
        "挂号": handle_appointment,
        "价格": handle_price_lookup,
        "多少钱": handle_price_lookup,
        "收费": handle_price_lookup,
        "地址": handle_directions,
        "在哪": handle_directions,
        "怎么走": handle_directions,
        "几点": handle_hours,
        "营业": handle_hours,
        "开门": handle_hours,
        "急": handle_emergency,
        "危险": handle_emergency,
    }

    for keyword, handler in intents.items():
        if keyword in message:
            return f"📞 意图识别：{keyword}\n\n" + handler(message, config)

    # Fallback
    llm_resp = llm_chat(message, f"你是{clinic.get('name','宠物医院')}的AI前台。用简洁中文回复宠物相关咨询。")
    if llm_resp:
        return f"📞 AI前台回复：\n\n{llm_resp}"

    return (f"📞 您好，这里是{clinic.get('name','宠物医院')}！\n\n"
           f"我可以帮您：\n"
           f"1. 预约挂号 → 说「预约」\n"
           f"2. 查询价格 → 说「多少钱」\n"
           f"3. 问地址 → 说「在哪」\n"
           f"4. 急诊咨询 → 描述症状\n\n"
           f"或直接描述您的需求。")

@register_skill("vet-hours")
def handle_hours(message: str, config: dict) -> str:
    """营业时间查询"""
    clinic = config.get("clinic", {})
    hours = clinic.get("hours", {"weekday": "09:00-21:00", "weekend": "10:00-18:00"})
    today = datetime.now()
    weekday = today.weekday()

    if weekday < 5:
        today_hours = hours.get("weekday", "09:00-21:00")
        day_type = "工作日"
    else:
        today_hours = hours.get("weekend", "10:00-18:00")
        day_type = "周末"

    return (f"🕐 营业时间\n\n"
           f"工作日（周一至周五）：{hours.get('weekday','09:00-21:00')}\n"
           f"周末（周六日）：{hours.get('weekend','10:00-18:00')}\n\n"
           f"今天是{['一','二','三','四','五','六','日'][weekday]}，{day_type}，营业时间 {today_hours}\n\n"
           f"节假日安排请关注公众号通知。")

@register_skill("vet-directions")
def handle_directions(message: str, config: dict) -> str:
    """到院路线指引"""
    clinic = config.get("clinic", {})
    return (f"📍 到院路线\n\n"
           f"地址：{clinic.get('address', '请在config中配置地址')}\n"
           f"电话：{clinic.get('phone', '请在config中配置电话')}\n\n"
           f"🚗 自驾：搜索「{clinic.get('name','宠物医院')}」导航\n"
           f"🚇 地铁：请根据实际地址填写\n"
           f"🚌 公交：请根据实际地址填写\n\n"
           f"院内有停车位，请从正门进入。")

@register_skill("vet-price-lookup")
def handle_price_lookup(message: str, config: dict) -> str:
    """项目价格查询"""
    clinic = config.get("clinic", {})
    raw_services = clinic.get("services", [])
    # Normalize service format: support both {name, price_min, price_max} and {type, price_range}
    services = []
    for svc in raw_services:
        name = svc.get("name") or svc.get("type", "未知")
        if "price_range" in svc:
            price = f"¥{svc['price_range']}"
        elif "price_min" in svc:
            price = f"¥{svc['price_min']}-{svc['price_max']}"
        else:
            price = "面议"
        services.append({"name": name, "price": price})

    if not services:
        services = [
            {"name": "基础诊疗", "price": "¥50-200"},
            {"name": "疫苗接种", "price": "¥80-300"},
            {"name": "绝育手术", "price": "¥500-2000"},
            {"name": "急诊", "price": "¥200-5000"},
            {"name": "体检套餐", "price": "¥200-800"},
            {"name": "洗牙", "price": "¥300-800"},
            {"name": "驱虫", "price": "¥50-200"},
            {"name": "皮肤病", "price": "¥100-500"},
        ]

    # Check if asking about specific service
    for svc in services:
        svc_name = svc["name"]
        if svc_name in message:
            return (f"💰 {svc_name}价格\n\n"
                   f"参考价格：{svc['price']}\n"
                   f"具体费用根据宠物体型和实际情况调整。\n\n"
                   f"📞 详细咨询：{clinic.get('phone','待配置')}")

    lines = "💰 服务价格参考\n\n"
    for svc in services:
        lines += f"  {svc['name']}：{svc['price']}\n"
    lines += f"\n📞 详细咨询：{clinic.get('phone','待配置')}"
    return lines

@register_skill("vet-feedback")
def handle_feedback(message: str, config: dict) -> str:
    """满意度收集"""
    # Simple rating parser
    rating_match = re.search(r"([1-5])\s*[分星★]", message)
    if rating_match:
        rating = int(rating_match.group(1))
        if rating >= 4:
            return f"❤️ 感谢您的{rating}星好评！您的认可是我们最大的动力。欢迎推荐给其他宠物家长！"
        elif rating == 3:
            return f"感谢反馈（{rating}星）。我们会努力改进，如有具体建议请告诉我们。"
        else:
            return f"抱歉让您失望了（{rating}星）。我们会认真对待您的反馈，负责人将尽快联系您。"

    return ("⭐ 就诊满意度评价\n\n"
           "请给本次就诊打分（1-5星）：\n"
           "⭐⭐⭐⭐⭐ 5星 - 非常满意\n"
           "⭐⭐⭐⭐ 4星 - 满意\n"
           "⭐⭐⭐ 3星 - 一般\n"
           "⭐⭐ 2星 - 不满意\n"
           "⭐ 1星 - 非常不满意\n\n"
           "输入如：「4星，医生很耐心」")

@register_skill("vet-record-lookup")
def handle_record_lookup(message: str, config: dict) -> str:
    """病历检索"""
    pet_match = re.search(r"(?:查|找|看)\s*(\S+?)\s*(?:的)?(?:病历|就诊)", message)
    pet_name = pet_match.group(1) if pet_match else None

    conn = get_db()
    try:
        if pet_name:
            rows = conn.execute("""SELECT mr.*, p.name as pet_name FROM medical_records mr
                                 JOIN pets p ON mr.pet_id = p.id WHERE p.name LIKE ?
                                 ORDER BY mr.created_at DESC LIMIT 5""", (f"%{pet_name}%",)).fetchall()
        else:
            rows = conn.execute("""SELECT mr.*, p.name as pet_name FROM medical_records mr
                                 JOIN pets p ON mr.pet_id = p.id
                                 ORDER BY mr.created_at DESC LIMIT 5""").fetchall()

        if rows:
            result = "📋 最近病历记录\n\n"
            for r in rows:
                result += (f"【{r['pet_name']}】{r['created_at']}\n"
                          f"  症状：{r['symptoms']}\n"
                          f"  诊断：{r['diagnosis']}\n"
                          f"  处理：{r['treatment']}\n\n")
            return result
        return f"未找到{'「'+pet_name+'」的' if pet_name else ''}病历记录。请确认宠物名或先创建病历。"
    finally:
        conn.close()

@register_skill("vet-lab-interpret")
def handle_lab_interpret(message: str, config: dict) -> str:
    """化验单解读"""
    # Try LLM first
    llm_resp = llm_chat(
        f"请用通俗语言解读以下宠物化验结果，标注异常指标并说明可能含义：\n{message}",
        "你是兽医AI助手，用简洁易懂的中文解读宠物化验单。不要做诊断，只解读数值含义。"
    )
    if llm_resp:
        return f"🔬 化验单解读\n\n{llm_resp}"

    # Template fallback
    wbc_match = re.search(r"WBC[：:]\s*([\d.]+)", message, re.IGNORECASE)
    rbc_match = re.search(r"RBC[：:]\s*([\d.]+)", message, re.IGNORECASE)
    result_parts = []

    if wbc_match:
        wbc = float(wbc_match.group(1))
        if wbc > 17.0:
            result_parts.append(f"WBC {wbc} ↑↑ 偏高，可能提示感染或炎症")
        elif wbc < 6.0:
            result_parts.append(f"WBC {wbc} ↓↓ 偏低，可能提示免疫系统问题")
        else:
            result_parts.append(f"WBC {wbc} ✓ 正常范围")

    if rbc_match:
        rbc = float(rbc_match.group(1))
        if rbc > 8.5:
            result_parts.append(f"RBC {rbc} ↑ 偏高，可能脱水")
        elif rbc < 5.5:
            result_parts.append(f"RBC {rbc} ↓ 偏低，可能贫血")
        else:
            result_parts.append(f"RBC {rbc} ✓ 正常范围")

    if result_parts:
        return "🔬 化验单解读\n\n" + "\n".join(result_parts) + "\n\n⚠️ 此为参考解读，请以兽医诊断为准。"

    return ("🔬 化验单解读\n\n"
           "请粘贴化验结果，例如：\n"
           "WBC: 15.2  RBC: 6.5  PLT: 250\n\n"
           "或发送化验单照片（需配置LLM）。")

@register_skill("vet-vaccine-schedule")
def handle_vaccine_schedule(message: str, config: dict) -> str:
    """疫苗接种计划"""
    kb = load_knowledge_base()
    species = "dog"
    if "猫" in message:
        species = "cat"

    schedules = kb.get("vaccine_schedules", {}).get(species, {})
    species_name = "犬" if species == "dog" else "猫"

    if schedules:
        result = f"💉 {species_name}疫苗接种计划\n\n"
        for stage, vaccines in schedules.items():
            result += f"【{stage}】\n"
            if isinstance(vaccines, list):
                for v in vaccines:
                    result += f"  • {v}\n"
            result += "\n"
        result += "⚠️ 具体接种时间请遵医嘱，体弱宠物需评估后再接种。"
        return result

    return ("💉 疫苗接种计划\n\n"
           "请告诉我宠物的种类（猫/狗）和年龄，我来生成接种计划。\n"
           "示例：「2个月大的小狗疫苗计划」")

@register_skill("vet-qa-kb")
def handle_qa_kb(message: str, config: dict) -> str:
    """兽医知识库问答"""
    kb = load_knowledge_base()
    diseases = kb.get("common_diseases", {})

    # Search in knowledge base
    for disease_name, info in diseases.items():
        if disease_name in message:
            symptoms = "、".join(info.get("symptoms", []))
            urgency = info.get("urgency", "unknown")
            advice = info.get("advice", "")
            urgency_map = {"high": "🚨 高度紧急", "medium": "⚠️ 中等紧急", "low": "ℹ️ 低度关注"}
            return (f"📖 {disease_name}\n\n"
                   f"紧急程度：{urgency_map.get(urgency, urgency)}\n"
                   f"典型症状：{symptoms}\n"
                   f"建议：{advice}")

    # Try LLM
    llm_resp = llm_chat(
        message,
        "你是宠物医疗知识问答助手。用简洁中文回答宠物健康问题，不要做诊断，只提供参考信息。建议复杂问题就医。"
    )
    if llm_resp:
        return f"📖 知识库回复\n\n{llm_resp}\n\n⚠️ 仅供参考，请以兽医诊断为准。"

    return ("📖 兽医知识库\n\n"
           "请提问，例如：\n"
           "- 「犬瘟热症状是什么」\n"
           "- 「猫呕吐怎么办」\n"
           "- 「狗不吃东西精神差」")

@register_skill("vet-daily-report")
def handle_daily_report(message: str, config: dict) -> str:
    """每日营收报表"""
    conn = get_db()
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        appointments = conn.execute(
            "SELECT COUNT(*) as cnt FROM appointments WHERE appointment_time LIKE ?",
            (f"{today}%",)).fetchone()
        total_appts = appointments["cnt"] if appointments else 0

        # Get appointment breakdown
        by_service = conn.execute(
            "SELECT service_type, COUNT(*) as cnt FROM appointments WHERE appointment_time LIKE ? GROUP BY service_type",
            (f"{today}%",)).fetchall()

        return (f"📊 每日运营报表 — {today}\n\n"
               f"预约总数：{total_appts} 单\n" +
               ("\n服务分类：\n" + "\n".join(f"  {r['service_type']}：{r['cnt']}单" for r in by_service) if by_service else "") +
               f"\n\n客户总数：{conn.execute('SELECT COUNT(*) FROM clients').fetchone()[0]}\n"
               f"宠物总数：{conn.execute('SELECT COUNT(*) FROM pets').fetchone()[0]}")
    finally:
        conn.close()

@register_skill("vet-inventory")
def handle_inventory(message: str, config: dict) -> str:
    """库存管理"""
    conn = get_db()
    try:
        # Add item
        add_match = re.search(r"(?:添加|入库|进货)\s*(\S+?)\s*(\d+)\s*(\S*)", message)
        if add_match:
            name = add_match.group(1)
            qty = int(add_match.group(2))
            unit = add_match.group(3) or "个"
            conn.execute("INSERT INTO inventory (name, quantity, unit) VALUES (?, ?, ?)",
                        (name, qty, unit))
            conn.commit()
            return f"✅ 已入库：{name} × {qty}{unit}"

        # Query inventory
        rows = conn.execute("SELECT * FROM inventory ORDER BY quantity ASC LIMIT 20").fetchall()
        if rows:
            result = "📦 库存清单\n\n"
            for r in rows:
                warning = " ⚠️ 库存不足!" if r["quantity"] <= (r["min_stock"] or 5) else ""
                result += f"  {r['name']}：{r['quantity']}{r['unit'] or '个'}{warning}\n"
            return result

        return "📦 库存为空。输入「添加XX 10个」入库。"
    finally:
        conn.close()

# ─── Chat Router ───
def route_message(message: str) -> tuple:
    """Route message to appropriate skill handler. Returns (skill_id, response)."""
    config = load_config()

    # Intent matching by trigger words
    trigger_map = {
        "vet-emergency": ["急", "抽搐", "出血", "中毒", "倒地", "呼吸困难", "休克"],
        "vet-appointment": ["预约", "挂号", "看诊"],
        "vet-intake": ["新客户", "登记", "建档", "主人"],
        "vet-hours": ["营业时间", "几点开门", "几点关门", "上班时间"],
        "vet-directions": ["怎么走", "地址在哪", "在哪", "导航"],
        "vet-price-lookup": ["多少钱", "价格", "收费", "费用"],
        "vet-lab-interpret": ["化验单", "血常规", "生化", "WBC", "RBC"],
        "vet-vaccine-schedule": ["疫苗", "打疫苗", "免疫"],
        "vet-record-lookup": ["病历", "查病历", "就诊记录"],
        "vet-qa-kb": ["什么病", "怎么办", "症状", "犬瘟", "猫瘟"],
        "vet-daily-report": ["日报", "今日营收", "运营报表"],
        "vet-inventory": ["库存", "入库", "进货", "添加"],
        "vet-feedback": ["满意", "评价", "打分", "星"],
    }

    # Priority order
    priority = ["vet-emergency", "vet-appointment", "vet-intake", "vet-hours",
                "vet-directions", "vet-price-lookup", "vet-lab-interpret",
                "vet-vaccine-schedule", "vet-record-lookup", "vet-qa-kb",
                "vet-daily-report", "vet-inventory", "vet-feedback"]

    for skill_id in priority:
        triggers = trigger_map.get(skill_id, [])
        for t in triggers:
            if t in message:
                handler = SKILL_REGISTRY.get(skill_id)
                if handler:
                    return skill_id, handler(message, config)

    # Default: try LLM, fallback to phone-ai
    handler = SKILL_REGISTRY.get("vet-phone-ai")
    if handler:
        return "vet-phone-ai", handler(message, config)

    return None, "请输入具体需求，例如：预约、价格、地址、营业时间等。"

# ─── API Routes ───
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not message:
        return JSONResponse({"error": "消息不能为空"}, status_code=400)

    skill_id, response = route_message(message)

    # Save conversation
    conn = get_db()
    try:
        conn.execute("INSERT INTO conversations (session_id, role, content, skill_used) VALUES (?, ?, ?, ?)",
                    (session_id, "user", message, None))
        conn.execute("INSERT INTO conversations (session_id, role, content, skill_used) VALUES (?, ?, ?, ?)",
                    (session_id, "assistant", response, skill_id))
        conn.commit()
    finally:
        conn.close()

    return JSONResponse({"response": response, "skill": skill_id, "session_id": session_id})

@app.get("/api/health")
async def health():
    return {"status": "ok", "skills": len(SKILL_REGISTRY), "llm_configured": bool(DEEPSEEK_API_KEY)}

@app.get("/api/services")
async def services():
    config = load_config()
    return {"clinic": config.get("clinic", {}), "skills": list(SKILL_REGISTRY.keys())}

@app.get("/api/conversation/{session_id}")
async def get_conversation(session_id: str):
    conn = get_db()
    try:
        rows = conn.execute("SELECT role, content, skill_used, created_at FROM conversations WHERE session_id = ? ORDER BY id DESC LIMIT 50",
                          (session_id,)).fetchall()
        return {"conversation": [dict(r) for r in reversed(rows)]}
    finally:
        conn.close()

@app.get("/api/stats")
async def stats():
    conn = get_db()
    try:
        return {
            "clients": conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0],
            "pets": conn.execute("SELECT COUNT(*) FROM pets").fetchone()[0],
            "appointments": conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0],
            "medical_records": conn.execute("SELECT COUNT(*) FROM medical_records").fetchone()[0],
            "inventory_items": conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0],
        }
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
