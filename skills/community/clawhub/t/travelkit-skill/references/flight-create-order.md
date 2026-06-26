# flight-create-order ref

## flight_create_order

Use after `flight_verify_solution` succeeds and user confirms continuing. Create order only after a second explicit creation confirmation; never auto-pay.

## Passenger Collection

- Before verified price + user continuation: do not collect ID/passport, phone, email, birthday, or name.
- Domestic mainland flights use Chinese document-name fields; do not ask for pinyin/English names.
- International/passport scenarios use passport English name fields.
- For Hong Kong/Macau/Taiwan or unclear routes, ask which valid travel document the passenger will use.
- Use natural Chinese + Markdown bullets, not code blocks or blank forms.
- Fixed prompts below must be output verbatim: do not rewrite, merge fields, add placeholders, add examples, or narrow passenger type.

**Domestic fixed prompt - must output verbatim**:

> 这趟是国内航班，后续需要乘机人证件信息。请把下面信息发我，我再帮你创建订单，但不会自动支付：
> 中文姓名请按证件姓名填写。

- 乘机人姓名
- 出生日期
- 性别
- 乘客类型：成人 / 儿童 / 婴儿
- 国籍
- 证件类型
- 证件号码
- 乘机人手机号
- 乘机人邮箱（可选：如果您希望我们通过邮箱给您发送通知，您可以填写邮箱）

**International fixed prompt - must output verbatim**:

> 这趟是国际航班，后续需要乘机人护照信息。请把下面信息发我，我再帮你创建订单，但不会自动支付：
> 护照英文姓和英文名需要与护照完全一致。

- 护照英文姓
- 护照英文名
- 出生日期
- 性别
- 乘客类型：成人 / 儿童 / 婴儿
- 国籍
- 护照号码
- 护照有效期（请填写具体日期）
- 乘机人手机号
- 乘机人邮箱（可选：如果您希望我们通过邮箱给您发送通知，您可以填写邮箱）

## Passenger Rules

- Required per passenger: phone, document type, document number.
- Email is optional notification info. If absent, omit passenger `email`; if supplier requires/rejects missing email, ask only for email.
- ID card, Mainland Travel Permit, and Taiwan Travel Permit names use Chinese as on document; passports use passport English name.
- For `travelDocument: idcard`, do not split the Chinese document name. Put the full document name in `givenNames` and pass `surname` as an empty string. Do not ask for surname/given-name splitting for compound surnames, ethnic/minority names, long names, or rare characters.
- Passport passengers still use passport English surname as `surname` and passport English given names as `givenNames`.
- If document type is unclear or cannot map to supported `travelDocument`, ask only for document type clarification.
- If contact name/phone is absent, default to first passenger's name/phone, mention this before creation, and do not collect contact email.

## Confirmation Before Creation

Before `flight_create_order`, summarize flight/route, departure/arrival time, passengers, contact info/defaults, final price, and returned notices. Amount line must be:

> 金额：¥{总价}（票面价 ¥{票面价} + 税价 ¥{税价}）

If verified solution returned any segment `availability <= 3`, include remaining ticket count, e.g. `当前余票不多，仅剩 {availability} 张，请尽快完成预订和支付；未支付前票价和余票可能变化。` For multi-segment journeys, use lowest returned availability.

Ask:
> 确认后我会为你创建订单，但不会自动支付。是否确认创建？

Only after explicit confirmation, call `flight_create_order` with verified `orderKey` and required internal confirmation fields; do not mention production/technical flags.

## After Creation

- When useful, call `flight_order_detail` and show `output-rules` fixed order template.
- Deadlines must come from explicit tool fields; if missing, use `output-rules` deadline wording.
- Amount: total = fare + tax; sum fare/tax across passengers/segments. If only total is returned, mark fare/tax as `未返回`.
- If unpaid, prompt payment options: domestic 微信、支付宝、易宝移动支付、信用卡、借记卡; international/cross-border also Airwallex.
- If low inventory was known, include remaining ticket count and remind prompt payment, otherwise ticket may sell out.

## Errors

- Ask only for missing/corrected fields; do not require resubmitting all passenger details.
- Name errors (`FirstName`, `LastName`, ID-card full name) mean document-name format issue. For ID-card passengers, ask only to verify or correct the full document name; do not ask for surname/given-name splitting and do not blame price/inventory.
- If an abnormal order is unpaid and unticketed, re-verify price before creating a corrected new order.
