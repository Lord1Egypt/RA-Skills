"""Programmatic industry arbitration (not declarative JSON)."""
from __future__ import annotations

from domain.industry import INDUSTRY_HINTS, TITLE_INDUSTRY_HINTS


def _body_hits(matched: dict[str, list[str]], industry: str) -> list[str]:
    return [k for k in matched.get(industry, []) if k in INDUSTRY_HINTS.get(industry, [])]


def apply_industry_arbitration(
    scores: dict[str, float],
    matched: dict[str, list[str]],
    title_n: str,
) -> None:
    """Mutate scores in place using cross-industry conflict rules."""
    # 2025A 新增行业（E3）：行业专属词 ≥2 共现时压制 manufacturing 通用词
    # （与 nonferrous 同款规则；steel/chemicals/agriculture/semiconductor 年报必中 产量/产能类泛词）
    for ind in ("steel", "chemicals", "agriculture", "semiconductor", "telecom"):
        if scores.get(ind) and scores.get("manufacturing"):
            body = _body_hits(matched, ind)
            if len(body) >= 2:
                scores["manufacturing"] = scores["manufacturing"] * 0.4
                scores[ind] = scores.get(ind, 0.0) + 2.0
    if scores.get("bank") and scores.get("automobile"):
        bank_body = _body_hits(matched, "bank")
        if len(bank_body) < 2 and not any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("bank", [])):
            scores["bank"] = scores["bank"] * 0.3
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("automobile", [])):
            scores["automobile"] = scores.get("automobile", 0.0) + 5.0

    # 有色年报必命中 manufacturing 通用词：正文证据充分时压制通用制造
    if scores.get("nonferrous") and scores.get("manufacturing"):
        nf_body = _body_hits(matched, "nonferrous")
        if len(nf_body) >= 2:
            scores["manufacturing"] = scores["manufacturing"] * 0.4
        if len(nf_body) >= 3:
            scores["nonferrous"] = scores.get("nonferrous", 0.0) + 2.0

    # 有色冶炼常自备电厂：有色正文充分时压制 energy（电投能源类）
    if scores.get("nonferrous") and scores.get("energy"):
        nf_body = _body_hits(matched, "nonferrous")
        if len(nf_body) >= 2:
            scores["energy"] = scores["energy"] * 0.4
        if len(nf_body) >= 3:
            scores["nonferrous"] = scores.get("nonferrous", 0.0) + 2.0

    # 保险 vs 银行：银行词偶发出现在保险投资/托管语境；保险正文充分或标题含保险时压制 bank
    if scores.get("insurance") and scores.get("bank"):
        ins_body = _body_hits(matched, "insurance")
        if len(ins_body) >= 2 or any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("insurance", [])):
            scores["bank"] = scores["bank"] * 0.35
        if len(ins_body) >= 3:
            scores["insurance"] = scores.get("insurance", 0.0) + 2.0

    # 保险准则附注污染：无保险标题且缺少保险强信号时，若其他行业标题命中或正文充分，压制 insurance。
    # 强信号（保费/偿付/NBV 等）保留，避免把平安等综合金融误压成 broker。
    _INSURANCE_STRONG = {
        "原保险保费收入", "保险业务收入", "综合偿付能力充足率", "核心偿付能力充足率",
        "承保利润", "新业务价值", "内含价值", "已赚保费",
    }
    if scores.get("insurance") and not any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("insurance", [])):
        ins_body = _body_hits(matched, "insurance")
        strong = [k for k in ins_body if k in _INSURANCE_STRONG]
        if len(strong) < 2:
            for rival in (
                "consumer", "pharma", "automobile", "nonferrous", "real_estate",
                "energy", "fossil_energy", "transport_infrastructure", "manufacturing",
                "broker", "bank",
            ):
                if not scores.get(rival):
                    continue
                rival_body = _body_hits(matched, rival)
                rival_title = any(h in title_n for h in TITLE_INDUSTRY_HINTS.get(rival, []))
                if rival_title or len(rival_body) >= 2:
                    scores["insurance"] = scores["insurance"] * 0.25
                    break

    # 券商 vs 银行：银行也有「手续费及佣金」；经纪/投行/净资本等 ≥2 或标题含证券/券商时压制 bank
    if scores.get("broker") and scores.get("bank"):
        br_body = _body_hits(matched, "broker")
        if len(br_body) >= 2 or any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("broker", [])):
            scores["bank"] = scores["bank"] * 0.35
        if len(br_body) >= 3:
            scores["broker"] = scores.get("broker", 0.0) + 2.0
        # 银行集团必含投行/资管/两融子公司词（如招银国际/招银理财）：
        # 银行正文充分（存款/贷款/资本充足率等强词）或标题含银行时反向压制 broker
        bank_body = _body_hits(matched, "bank")
        if len(bank_body) >= 3 or any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("bank", [])):
            scores["broker"] = scores["broker"] * 0.3
        if len(bank_body) >= 4:
            scores["bank"] = scores.get("bank", 0.0) + 2.0

    # 地产 vs 制造：地产正文充分时压制 manufacturing 通用词
    if scores.get("real_estate") and scores.get("manufacturing"):
        re_body = _body_hits(matched, "real_estate")
        if len(re_body) >= 2:
            scores["manufacturing"] = scores["manufacturing"] * 0.4
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("real_estate", [])):
            scores["real_estate"] = scores.get("real_estate", 0.0) + 3.0

    # 能源 vs 制造：装机/发电等充分时压制 manufacturing
    if scores.get("energy") and scores.get("manufacturing"):
        en_body = _body_hits(matched, "energy")
        if len(en_body) >= 2:
            scores["manufacturing"] = scores["manufacturing"] * 0.4
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("energy", [])):
            scores["energy"] = scores.get("energy", 0.0) + 3.0

    # 制药 vs 制造：制药年报常含产销量；药品监管词充分时压制 manufacturing
    if scores.get("pharma") and scores.get("manufacturing"):
        ph_body = _body_hits(matched, "pharma")
        if len(ph_body) >= 2:
            scores["manufacturing"] = scores["manufacturing"] * 0.4
        if len(ph_body) >= 3:
            scores["pharma"] = scores.get("pharma", 0.0) + 2.0
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("pharma", [])):
            scores["pharma"] = scores.get("pharma", 0.0) + 3.0

    # 器械标题：无制药高信号时不定型 pharma
    if scores.get("pharma") and any(h in title_n for h in ("器械", "诊断", "IVD", "体外诊断")):
        ph_body = _body_hits(matched, "pharma")
        if len(ph_body) < 2:
            scores["pharma"] = scores["pharma"] * 0.3

    # 消费 vs 制造：酒/乳年报必含产销量
    if scores.get("consumer") and scores.get("manufacturing"):
        cs = _body_hits(matched, "consumer")
        if len(cs) >= 2:
            scores["manufacturing"] = scores["manufacturing"] * 0.4
        if len(cs) >= 3:
            scores["consumer"] = scores.get("consumer", 0.0) + 2.0
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("consumer", [])):
            scores["consumer"] = scores.get("consumer", 0.0) + 3.0

    # 珠宝/黄金标题：无经销/同店等高信号时不定型 consumer
    if scores.get("consumer") and any(h in title_n for h in ("黄金", "珠宝", "首饰")):
        cs = _body_hits(matched, "consumer")
        if len(cs) < 2:
            scores["consumer"] = scores["consumer"] * 0.25

    # 消费 vs 银行：银行「零售」语境；消费渠道词充分时压制 bank。
    # 银行正文充分（存款/贷款等强词）或标题含银行时不压——多重 0.35 叠乘曾把
    # bank=10（8 词+标题）打穿到 1.9，让 automobile(3) 渔翁得利（招行汽车金融词）
    if scores.get("consumer") and scores.get("bank"):
        cs = _body_hits(matched, "consumer")
        bank_strong = (len(_body_hits(matched, "bank")) >= 3
                       or any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("bank", [])))
        if len(cs) >= 2 and not bank_strong:
            scores["bank"] = scores["bank"] * 0.35

    # 交运 vs 制造/地产/能源/汽车
    if scores.get("transport_infrastructure") and scores.get("manufacturing"):
        tr = _body_hits(matched, "transport_infrastructure")
        if len(tr) >= 2:
            scores["manufacturing"] = scores["manufacturing"] * 0.4
    if scores.get("transport_infrastructure") and scores.get("real_estate"):
        tr = _body_hits(matched, "transport_infrastructure")
        re_body = _body_hits(matched, "real_estate")
        tr_title = any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("transport_infrastructure", []))
        re_title = any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("real_estate", []))
        # 高速/港口运营商常附带物业投资：运营词充分或标题为高速/港口时压制地产
        if len(tr) >= 2 or tr_title:
            scores["real_estate"] = scores["real_estate"] * 0.35
            scores["transport_infrastructure"] = scores.get("transport_infrastructure", 0.0) + 3.0
        elif len(re_body) >= 2 or re_title:
            scores["transport_infrastructure"] = scores["transport_infrastructure"] * 0.4
            scores["real_estate"] = scores.get("real_estate", 0.0) + 3.0
    if scores.get("transport_infrastructure") and scores.get("energy"):
        tr = _body_hits(matched, "transport_infrastructure")
        en_body = _body_hits(matched, "energy")
        tr_title = any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("transport_infrastructure", []))
        # 高速/港口偶发披露光伏/装机：交运充分时压制 energy
        if len(tr) >= 2 or tr_title:
            scores["energy"] = scores["energy"] * 0.4
        elif len(en_body) >= 2:
            scores["transport_infrastructure"] = scores["transport_infrastructure"] * 0.4
    if scores.get("transport_infrastructure") and scores.get("automobile"):
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("automobile", [])):
            scores["automobile"] = scores.get("automobile", 0.0) + 5.0
            scores["transport_infrastructure"] = scores["transport_infrastructure"] * 0.3
    if scores.get("transport_infrastructure") and any(
        h in title_n for h in TITLE_INDUSTRY_HINTS.get("transport_infrastructure", [])
    ):
        scores["transport_infrastructure"] = scores.get("transport_infrastructure", 0.0) + 3.0

    # 智驾/汽车电子方案商 vs 整车厂：双方年报互含对方语境词（方案商提「汽车/新能源」指客户，
    # 整车厂提「智能驾驶/算力」指自研）。用专属词双向仲裁：
    # 方案商专属（ADAS/域控/流片/SoC/车规/自动驾驶…）≥2 且无整车专属词（整车/分车型/皮卡）→ 压 automobile；
    # 整车专属词 ≥2 → 压 auto_electronics（保 OEM 年报不被自家智驾叙事带偏）
    if scores.get("auto_electronics") and scores.get("automobile"):
        _AE_STRONG = ("ADAS", "域控制器", "域控", "流片", "SoC", "车规", "車規",
                      "自动驾驶", "自動駕駛", "辅助驾驶", "輔助駕駛", "智能驾驶", "智能駕駛")
        _AUTO_STRONG = ("整车", "整車", "分车型", "分車型", "皮卡", "乘用车", "乘用車")
        ae_strong = [k for k in _body_hits(matched, "auto_electronics") if k in _AE_STRONG]
        au_strong = [k for k in _body_hits(matched, "automobile") if k in _AUTO_STRONG]
        if len(ae_strong) >= 2 and not au_strong:
            scores["automobile"] = scores["automobile"] * 0.25
            scores["auto_electronics"] = scores.get("auto_electronics", 0.0) + 2.0
        elif len(au_strong) >= 2:
            scores["auto_electronics"] = scores["auto_electronics"] * 0.3
        elif len(ae_strong) >= 3:
            scores["automobile"] = scores["automobile"] * 0.5

    # 化石能源 vs 制造 / 电力 / 有色
    if scores.get("fossil_energy") and scores.get("manufacturing"):
        fo = _body_hits(matched, "fossil_energy")
        if len(fo) >= 2:
            scores["manufacturing"] = scores["manufacturing"] * 0.4
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("fossil_energy", [])):
            scores["fossil_energy"] = scores.get("fossil_energy", 0.0) + 3.0
    if scores.get("fossil_energy") and scores.get("energy"):
        fo = _body_hits(matched, "fossil_energy")
        if len(fo) >= 2:
            scores["energy"] = scores["energy"] * 0.4
        # 纯电力标题仍抬 energy
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("energy", [])):
            scores["energy"] = scores.get("energy", 0.0) + 3.0
    if scores.get("fossil_energy") and scores.get("nonferrous"):
        fo = _body_hits(matched, "fossil_energy")
        nf = _body_hits(matched, "nonferrous")
        coalish = [k for k in fo if any(t in k for t in ("原煤", "商品煤", "吨煤", "煤炭", "洗选", "长协"))]
        metalish = [k for k in nf if any(t in k for t in ("矿产", "电解", "冶炼", "精矿", "有色"))]
        if len(coalish) >= 2 and len(metalish) < 2:
            scores["nonferrous"] = scores["nonferrous"] * 0.4
        if len(metalish) >= 2:
            scores["fossil_energy"] = scores["fossil_energy"] * 0.4
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("nonferrous", [])):
            scores["nonferrous"] = scores.get("nonferrous", 0.0) + 3.0
        if any(h in title_n for h in TITLE_INDUSTRY_HINTS.get("fossil_energy", [])):
            scores["fossil_energy"] = scores.get("fossil_energy", 0.0) + 3.0


# 跨业态邻接晋升白名单：主行业判定下，第二业态的表 hints 共现 ≥2 时放行晋升
# （神华 fossil+电力 5 处 power_generation hint、神火/电投 有色+煤 实证——煤电铝/煤电一体为常态业态）
CROSS_INDUSTRY_TABLE_ALLOWLIST: dict[str, dict[str, list[str]]] = {
    "fossil_energy": {"energy": ["power_generation", "installed_capacity", "utilization_hours"]},
    "energy": {"fossil_energy": ["coal_production", "coal_reserves", "coal_cost_price"]},
    "nonferrous": {"fossil_energy": ["coal_production", "coal_reserves", "coal_cost_price"]},
    "automobile": {"auto_electronics": ["ad_shipments", "customer_concentration"]},
    "auto_electronics": {"automobile": ["nev_sales", "production_sales"]},
}
