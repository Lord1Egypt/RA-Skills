#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from activity_claim import is_joined_claim_kind
from recommendation_logic import (
    build_recommendation_fallback_copy,
    build_recommendation_material_lines,
)
from response_rendering import (
    escape_table_cell,
    render_markdown_table,
    render_primary_response,
    render_text_section,
)

WEATHER_LABELS = {
    "sunny": "晴",
    "cloudy": "多云",
    "rainy": "雨",
    "snowy": "雪",
    "unknown": "未知",
}

ORDER_STATE_LABELS = {
    0: "未知",
    1: "待支付",
    2: "制作中",
    3: "待取餐",
    4: "已取消",
    5: "退款中",
    6: "已完成",
}

LEAD_CAPTURE_COPY = "请把您微信小程序【新一咖啡】绑定的手机号发过来，我帮您领取Skill用户大礼包。"
UNREGISTERED_LOGIN_COPY = "请先到微信小程序搜索【新一咖啡】，登录/注册并绑定手机号；完成后把绑定手机号发来，我再帮你继续领取。"
ACTIVITY_GIFT_SUMMARY = "Skill用户大礼包包含：小龙虾贴纸、Skill用户身份标识、Skill用户专享赠饮券。"
ACTIVITY_RULE_LINES = [
    "活动规则：",
    "小龙虾贴纸：到任意门店对暗号【小龙虾】领取，先到先得。",
    "Skill用户专享赠饮券：（前100名）爆款苦尽甘来拿铁免费兑换券 / （101-500名）5折饮品券 / （501-以后）8折饮品券。",
    "Skill用户身份标识：参与即可添加SKILL 标签、龙虾头像。",
]
ACTIVITY_QUERY_KEYWORDS = ("活动", "福利", "券", "见面礼", "龙虾", "领取")
ORDER_QUERY_KEYWORDS = (
    "我的订单",
    "个人订单",
    "历史订单",
    "订单历史",
    "订单记录",
    "订单信息",
    "订单状态",
    "已完成订单",
    "已完成",
    "买过",
    "购买",
    "消费",
    "几单",
    "多少单",
    "下过单",
)
ORDER_EXACT_QUERIES = ("订单", "历史记录")


def build_register_instruction() -> str:
    return UNREGISTERED_LOGIN_COPY


def build_activity_flow_lines() -> list[str]:
    return [
        LEAD_CAPTURE_COPY,
        ACTIVITY_GIFT_SUMMARY,
        *ACTIVITY_RULE_LINES,
        "我会先按您发来的手机号查询领取；如果没有查到绑定记录，再提醒您完成小程序登录/绑定。",
    ]


def build_realtime_unavailable_lines(scope: str, error: Any) -> list[str]:
    return [
        f"{scope}暂时没拿到：{error}",
        "可以继续回答品牌能力、领取流程或推荐思路，但必须明确这不是实时门店/菜单结果。",
        "未确认状态的活动/手机号领取以领取查询结果为准；本地已确认领取的手机号以本地状态优先；不要猜用户是否已参加或券是否已到账。",
        "门店、菜单、价格、库存和排队信息不要编造；建议稍后重试或打开小程序确认。",
    ]


def render_store_query_unavailable(error: Any) -> str:
    return render_text_section(
        "实时数据状态",
        [
            f"门店实时数据暂时没拿到：{error}",
            "可以说明本 Skill 支持查询门店、地址、电话、设施和排队信息。",
            "不要编造门店名、地址、电话或排队信息；建议稍后重试或打开小程序查看。",
        ],
    )


def render_recommendation_unavailable(error: Any) -> str:
    return render_text_section(
        "实时数据状态",
        build_realtime_unavailable_lines("推荐上下文", error),
    )


def build_unregistered_activity_lines(mobile: Any) -> list[str]:
    mobile_text = str(mobile).strip() if mobile else "当前手机号"
    return [
        f"{mobile_text} 目前还没查到【新一咖啡】小程序登录/绑定记录。",
        "🎁 领取步骤",
        "第一步：绑定手机号\n打开微信 → 搜索【新一咖啡】小程序 → 登录/注册并绑定您的手机号",
        "第二步：发送手机号给我\n绑定完成后，把您的手机号发过来，我帮您领取Skill用户大礼包。",
        ACTIVITY_GIFT_SUMMARY,
        *ACTIVITY_RULE_LINES,
        "这不是没有活动，而是需要先完成小程序登录/绑定后才能发放礼包。",
    ]


def pick_store_contact(store: dict[str, Any]) -> Any:
    for key in ("storeMobile", "contactPhone", "phone", "telephone", "tel"):
        value = store.get(key)
        if value:
            return value

    return None


def split_store_facilities(store: dict[str, Any]) -> list[str]:
    facilities = store.get("facilities")
    if not facilities:
        return []

    text = str(facilities).replace("，", ",").replace("。", ",")
    return [item.strip() for item in text.split(",") if item.strip()]


def render_store_facilities_text(store: dict[str, Any]) -> Any:
    return store.get("facilities") or None


def format_coupon_label(coupon_names: list[str]) -> str:
    if not coupon_names:
        return ""

    if len(coupon_names) == 1:
        return f"「{coupon_names[0]}」"

    return "、".join(f"「{name}」" for name in coupon_names)


def format_coupon_reward(coupon_names: list[str]) -> str:
    if not coupon_names:
        return "Skill用户专享赠饮券（具体饮品以小程序卡券为准）"

    if len(coupon_names) == 1:
        return f"Skill用户专享赠饮券{format_coupon_label(coupon_names)}"

    return f"Skill用户专享赠饮券：{format_coupon_label(coupon_names)}"


def build_claim_detail_lines(data: dict[str, Any], items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["系统识别该手机号已参与/已领取，本次没有新的券发放。"]

    lines: list[str] = []
    for index, item in enumerate(items, 1):
        message = item.get("message") or ("发放成功" if item.get("state") == 1 else "未发放成功")
        coupon = item.get("coupon")
        coupon_name = coupon.get("name") if isinstance(coupon, dict) else None
        coupon_count = item.get("couponNum")
        if item.get("state") == 1:
            coupon_text = format_coupon_reward([coupon_name] if coupon_name else [])
            if coupon_count and coupon_count != 1:
                coupon_text = f"{coupon_text} x{coupon_count}"
            lines.append(f"到账券：{coupon_text}。")
        elif coupon_name:
            lines.append(f"{format_coupon_reward([coupon_name])}暂未发放成功：{message}。")
        else:
            lines.append(f"券状态：{message}。")

    return lines


def render_context_section(context: dict[str, Any]) -> str:
    mobile_source = "-"
    mobile = context.get("mobile")
    if mobile:
        mobile_source = "本地缓存" if context.get("mobileFromStore") else "本次输入"

    rows = [
        ["手机号", mobile],
        ["手机号来源", mobile_source],
        ["用户问题", context.get("query")],
        ["推荐场景", context.get("scene")],
        ["用户偏好", context.get("preference")],
    ]
    if is_activity_query(context):
        activity_joined = context.get("activityJoined")
        if activity_joined is True:
            activity_joined_label = "是"
        elif activity_joined is False:
            activity_joined_label = "否"
        else:
            activity_joined_label = "未确认"
        rows.insert(2, ["是否已参加活动", activity_joined_label])

    return render_markdown_table(
        title="用户上下文",
        headers=["字段", "内容"],
        rows=rows,
        empty_text="暂无上下文信息。",
    )


def context_matches_keywords(context: dict[str, Any], keywords: tuple[str, ...]) -> bool:
    text = " ".join(
        str(context.get(key) or "")
        for key in ("query", "scene", "preference")
    )
    return any(keyword in text for keyword in keywords)


def is_activity_query(context: dict[str, Any]) -> bool:
    return context_matches_keywords(context, ACTIVITY_QUERY_KEYWORDS)


def is_order_query(context: dict[str, Any]) -> bool:
    text = " ".join(
        str(context.get(key) or "")
        for key in ("query", "scene", "preference")
    ).strip()
    if text in ORDER_EXACT_QUERIES:
        return True
    return context_matches_keywords(context, ORDER_QUERY_KEYWORDS)


def render_brand_activity_section(context: dict[str, Any]) -> str:
    activity_joined = context.get("activityJoined")

    if activity_joined is True:
        lines = [
            f"**Skill用户大礼包**：用户身份已验证成功，{ACTIVITY_GIFT_SUMMARY}",
            *ACTIVITY_RULE_LINES,
            "回答时可以说明福利已经到账，不要再要求用户重新登录小程序或再次告知手机号。",
        ]
    else:
        lines = [
            f"**Skill用户大礼包**：{LEAD_CAPTURE_COPY}",
            ACTIVITY_GIFT_SUMMARY,
            *ACTIVITY_RULE_LINES,
            "先假设用户已经登录/绑定小程序，只请求用户发送手机号；只有查询后确认未绑定时，再提示去微信小程序搜索【新一咖啡】登录/注册并绑定手机号。",
        ]

    return render_text_section("品牌活动", lines)


def render_weather_section(weather: dict[str, Any] | None) -> str:
    rows: list[list[Any]] = []
    if weather:
        rows.append(
            [
                weather.get("city"),
                WEATHER_LABELS.get(weather.get("condition"), weather.get("condition")),
                weather.get("temperatureC"),
            ]
        )

    return render_markdown_table(
        title="天气",
        headers=["城市", "天气", "温度(°C)"],
        rows=rows,
        empty_text="暂无天气数据。",
    )


def format_order_goods(goods: list[dict[str, Any]]) -> str:
    entries: list[str] = []
    for item in goods:
        name = item.get("name") or "-"
        detail_parts = [part for part in [item.get("spec"), item.get("attr")] if part]
        if detail_parts:
            entries.append(f"{name}（{' / '.join(detail_parts)}）")
        else:
            entries.append(name)

    return "；".join(entries) if entries else "-"


def format_order_state(state: Any) -> str:
    if isinstance(state, int):
        return ORDER_STATE_LABELS.get(state, f"状态{state}")

    return escape_table_cell(state)


def build_activity_completion_lines(kind: str, coupon_names: list[str]) -> list[str]:
    if kind == "already_claimed":
        return [
            "该手机号已经领取过 Skill用户大礼包。",
            f"已领取内容：小龙虾贴纸（到任意门店对暗号【小龙虾】领取，先到先得）；Skill用户身份标识；{format_coupon_reward(coupon_names)}。",
            *ACTIVITY_RULE_LINES,
            "你已经领取礼包，现在可以查看你过去的订单信息。",
        ]

    if is_joined_claim_kind(kind):
        return [
            "身份验证成功。Skill用户大礼包已发放到账：",
            f"小龙虾贴纸（到任意门店对暗号【小龙虾】领取，先到先得）；Skill用户身份标识；{format_coupon_reward(coupon_names)}。",
            *ACTIVITY_RULE_LINES,
            "你已经领取礼包，现在可以查看你过去的订单信息。",
        ]

    return []


def render_orders_section(orders: dict[str, Any] | None) -> str:
    if orders is None:
        return "## 订单历史\n未提供手机号，未查询订单历史。"

    rows = [
        [
            item.get("createdAt"),
            item.get("orderSn"),
            format_order_state(item.get("state")),
            item.get("pickNo"),
            item.get("serverTime"),
            item.get("store", {}).get("name") if item.get("store") else None,
            format_order_goods(item.get("goods", [])),
            item.get("goodsNum"),
        ]
        for item in orders.get("orders", [])
    ]

    return render_markdown_table(
        title="订单历史",
        headers=[
            "下单时间",
            "订单号",
            "状态",
            "排号",
            "预计取餐时间",
            "门店",
            "商品",
            "杯数",
        ],
        rows=rows,
        empty_text="暂无订单记录。",
    )


def build_order_followup_lines(orders: dict[str, Any] | None) -> list[str]:
    if orders is None:
        return ["用户追问订单信息时，当前未提供手机号，不能查询过去订单。"]

    order_list = orders.get("orders", [])
    completed_orders = [order for order in order_list if order.get("state") == 6]
    goods_names: list[str] = []
    store_names: list[str] = []
    for order in order_list:
        store = order.get("store") or {}
        if store.get("name"):
            store_names.append(str(store.get("name")))
        for good in order.get("goods", []):
            if good.get("name"):
                goods_names.append(str(good.get("name")))

    completed_count = len(completed_orders)
    if completed_count >= 10:
        completed_line = f"用户追问订单信息时再展开：你已完成{completed_count}单，是新一的骨灰级粉丝吧。"
    elif completed_count > 0:
        completed_line = f"用户追问订单信息时再展开：你已完成{completed_count}单，看得出来是真喜欢新一。"
    else:
        completed_line = "用户追问订单信息时再展开：当前还没看到已完成订单。"

    lines = [completed_line, f"当前可见订单数：{len(order_list)}单。"]
    if goods_names:
        unique_goods_names = list(dict.fromkeys(goods_names))
        lines.append(f"买过的商品可以提这些：{'、'.join(unique_goods_names[:5])}。")
    if store_names:
        unique_store_names = list(dict.fromkeys(store_names))
        lines.append(f"到过的门店可以提这些：{'、'.join(unique_store_names[:3])}。")

    return lines


def render_order_followup_section(
    context: dict[str, Any],
    orders: dict[str, Any] | None,
) -> str:
    if not is_order_query(context):
        return ""

    return render_text_section("订单追问素材", build_order_followup_lines(orders))


def render_goods_section(goods: list[dict[str, Any]]) -> str:
    rows = [
        [
            item.get("name"),
            item.get("categories", []),
            item.get("price"),
            item.get("cupSizes", []),
            item.get("temperatures", []),
            item.get("sugarLevels", []),
            item.get("calories"),
            item.get("ingredients", []),
        ]
        for item in goods
    ]

    return render_markdown_table(
        title="商品列表",
        headers=["商品名称", "分类", "价格", "杯型", "温度", "糖度", "卡路里", "配料"],
        rows=rows,
        empty_text="暂无商品数据。",
    )


def format_store_status(store: dict[str, Any]) -> str:
    parts: list[str] = []
    if store.get("businessStatus") is not None:
        parts.append(f"营业状态={store.get('businessStatus')}")
    if store.get("operatingStatus") is not None:
        parts.append(f"运营状态={store.get('operatingStatus')}")
    if store.get("realtimeState") is not None:
        parts.append(f"实时状态={store.get('realtimeState')}")
    return " / ".join(parts) if parts else "-"


def build_store_feature_tags(store: dict[str, Any]) -> list[str]:
    feature_tags: list[str] = []

    def append_tag(tag: Any) -> None:
        if not tag:
            return
        text = str(tag).strip()
        if text and text not in feature_tags:
            feature_tags.append(text)

    for facility in split_store_facilities(store):
        append_tag(facility)

    for label in store.get("labels", []):
        if isinstance(label, dict):
            append_tag(label.get("name"))

    if store.get("supportUnattendedMode") == 1:
        append_tag("支持无人模式")

    if store.get("storeType") == 2:
        append_tag("Box 门店")

    return feature_tags


def render_stores_section(stores: list[dict[str, Any]]) -> str:
    rows = [
        [
            item.get("name"),
            item.get("address"),
            pick_store_contact(item),
            render_store_facilities_text(item),
            format_store_status(item),
            build_store_feature_tags(item),
            item.get("makingCupCount"),
            item.get("makingCupMinutes"),
        ]
        for item in stores
    ]

    return render_markdown_table(
        title="门店列表",
        headers=["门店名称", "地址", "联系电话", "设施文案", "状态", "特色标签", "制作中杯数", "制作时长(分钟)"],
        rows=rows,
        empty_text="暂无门店数据。",
    )


def render_answer_requirements_section(
    stores: list[dict[str, Any]],
    context: dict[str, Any],
) -> str:
    activity_query = is_activity_query(context)
    lines = [
        "先给出一段有温度的主推荐文案，像懂茶饮也懂咖啡的店员姐姐给朋友建议一样自然，熟门店、懂口味，会认真帮用户挑选，松弛有温度，而不是像报告摘要。",
        "可以参考这种语气：“今天这个温度喝它刚好”“如果你想提神又不想太苦，可以先看这杯”。",
        "回答需要有层次和重点：推荐饮品、适合它的几个原因、必要时的活动留资提示分成 2-4 个短块，不要堆成一整段。",
        "主推饮品名必须加粗，也就是要加粗突出；如果提到备选饮品，也可以加粗突出。只有用户明确提到门店时，才返回门店信息并加粗门店名。",
        "可以少量使用合适 emoji 做层次锚点或增强温度，比如饮品、天气、门店、活动各 0-1 个；不要每行都加，也不要连续堆 emoji。",
        "把推荐依据自然融进表达里，可以用轻量分点，但不要使用“推荐理由”，也不要使用“根据你的历史订单偏好”“历史偏好匹配”“天气适配”“推荐门店”这类机械标题。",
        "如果使用订单偏好做个性化推荐，把用户常点饮品当作口味参考，优先主推口味相邻但不常点或未点过的饮品；不要默认推荐用户最常点的饮品，除非菜单里没有合适替代。",
        "语气要真诚、松弛、有人情味；少用营销腔、感叹号和模板化开场，不要复述固定模板。",
        "接口没返回的数据不要编造；没有商品、券名、订单或活动状态时，明确说当前没拿到。用户没有明确问门店时，不要主动提门店缺失。",
        "只有用户追问订单、完成多少单、买过什么时，才根据订单数据返回已完成订单数和购买信息；订单很多时可以更热络，少量订单不要贴重度粉丝标签。",
    ]

    if activity_query and context.get("activityJoined"):
        lines.append("登录成功后只提示用户已经领取礼包、现在可以查看过去的订单信息；不要主动展开已完成多少单或购买明细。")
        lines.append("用户正在问活动/福利/领取，且已参加过活动：用普通陈述说明已领取/已到账和实际券名；不要写成功失败数量等技术化信息。")
    elif activity_query or not context.get("activityJoined"):
        lines.append(
            f"用户未参加过活动或当前手机号状态未确认，回答末尾可以用分割线 `---` 单独隔开主动留资文案：{LEAD_CAPTURE_COPY} 用户提交手机号后如果仍未注册，再提示：{UNREGISTERED_LOGIN_COPY}"
        )
    else:
        lines.append("当前问题不需要账户权益信息；最终回答只围绕用户当前的饮品、菜单、订单或门店问题，不要追加无关的账户、礼包或领取状态。")

    if activity_query:
        lines.append(
            "用户正在问活动/福利，最终回答只说明“**Skill用户大礼包**”；不要扩展到其它商品信息。"
        )

    if stores:
        if activity_query:
            store_transition_line = (
                "根据用户这次意图自然承接门店：领活动奖励时可说“您可以到我们的店领取奖励”；"
                "饮品推荐时可说“您可以到我们店里畅饮”。"
            )
        else:
            store_transition_line = "根据用户这次意图自然承接门店：饮品推荐时可说“您可以到我们店里畅饮”。"
        lines.extend(
            [
                "若回答中展示门店，必须展示全部返回门店，带上每家门店名和详细地址；如果当前回答不需要门店，可以完全不展示门店。",
                "不要只推荐某一家门店，不要写只让用户去某一家店的单店引导；不能只展示第一家或任意一家。",
                "若展示门店，门店电话也一并给出；如果没有电话字段，再明确说明未提供联系电话。",
                "若展示门店且门店返回了 facilities，必须明确返回这段设施文案，不要省略。",
                "当前没有用户定位，门店部分不要说“附近”“就近”或“离你近”，也不要把技术口吻说给用户。",
                store_transition_line,
                "门店名加粗，地址、电话、设施和排队信息用短行呈现。",
            ]
        )
    return render_text_section("回答要求", lines)


def render_recommendation_context(
    *,
    context: dict[str, Any],
    goods: list[dict[str, Any]],
    weather: dict[str, Any] | None,
    orders: dict[str, Any] | None,
) -> str:
    sections = [
        render_context_section(context),
        render_weather_section(weather),
        render_orders_section(orders),
        render_order_followup_section(context, orders),
        render_goods_section(goods),
    ]
    sections.append(render_answer_requirements_section([], context))
    if is_activity_query(context):
        sections.insert(1, render_brand_activity_section(context))

    recommendation_material_lines = build_recommendation_material_lines(goods, orders, weather)
    if recommendation_material_lines:
        sections.append(
            render_text_section(
                "推荐素材",
                recommendation_material_lines,
            )
        )

    return "\n\n".join(section for section in sections if section.strip())


def render_claim_result(
    data: dict[str, Any] | None,
    context_data: dict[str, Any] | None = None,
) -> str:
    data = data if isinstance(data, dict) else {}
    kind = data.get("kind")
    items = data.get("items", [])
    items = items if isinstance(items, list) else []
    user = data.get("user")

    if kind == "unregistered":
        return render_primary_response(
            "领取结果：请先登录小程序",
            build_unregistered_activity_lines(data.get("requestedMobile")),
        )

    coupon_names = [
        item.get("coupon", {}).get("name")
        for item in items
        if item.get("state") == 1 and item.get("coupon")
    ]
    coupon_names = [name for name in coupon_names if name]

    context_data = context_data or {}
    goods = context_data.get("goods", [])
    weather = context_data.get("weather")
    orders = context_data.get("orders")
    recommendation_copy = build_recommendation_fallback_copy(goods, orders, weather)

    title = "领取结果：处理完成"
    lines: list[str] = []

    if is_joined_claim_kind(kind):
        title = "领取结果：已领取过" if kind == "already_claimed" else "领取结果：身份验证成功"
        lines.extend(build_activity_completion_lines(kind, coupon_names))
        if kind != "already_claimed" or items:
            lines.extend(build_claim_detail_lines(data, items))
    elif kind == "no_reward_config":
        title = "领取方式"
        lines.extend(build_activity_flow_lines())
    else:
        lines.append("活动处理已完成。")

    if user and user.get("nickname"):
        lines.append(f"当前识别用户：{user.get('nickname')}")

    if recommendation_copy:
        lines.append(recommendation_copy)

    return render_primary_response(title, lines)
