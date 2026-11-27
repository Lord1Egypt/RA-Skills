# 获取联系方式 API 参考

## python脚本参数
- `--bus_type`：业务类型（必需）；1=公司，2=人物
- `--bus_ids`：公司ID或人物ID列表（空格分隔，必需，最多20个）
- `--task_id`：原列表任务 ID（可选）；列表查询后获取具体联系方式时必须传入，使返回值合并进原任务的 `result.jsonl` 和 `result.xlsx`
- `--user_confirmed`：用户已在独立消息中确认ID数量和费用后必须传入

## 响应数据

### 邮箱列表 emails
- val：邮箱地址
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- reason：原因

### 电话列表 phones
- val：电话
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- is_ws：是否WhatsApp（0=未检测，1=是，2=否，3=不确定）
- phone_type：号码类型（0=未检测，1=固定电话，2=移动电话，3=已检测但未知）
- country_code：电话所属国家二字码
- dialing_code：电话所属国际冠码
- area_code：电话所属地区码
- international_number：国际格式号码
- telephone：号码（去除冠码与区码）
- national_number：号码属国格式

### 社交媒体列表 socials
- val：社媒完整链接
- social_url：社媒链接路径
- social_type：社媒类型（linkedin, facebook, twitter, youtube, instagram, pinterest, github, tiktok）
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- reason：原因

### 网站列表 websites
- val：网址
- is_valid：是否有效（0=未检测，1=是，2=否，3=不确定）
- is_sensitive：是否敏感（0=未检测，1=是，2=否，3=不确定）
- reason：原因

## 本地结果交付

脚本成功时会在 `contactDelivery.displayRows` 中返回全部联系方式对象，当前回复必须展示实际邮箱、电话、WhatsApp 等完整值，不得只报告查询成功或联系方式数量。

传入 `--task_id` 时，脚本还会更新列表任务的 `delivery`：把已购买的联系方式合并回完整 JSONL，重新生成完整 Excel，并给出更新后的前 10 条预览。对单独发起的联系方式任务仍须预先确认费用。原始列表请求已经明确要求具体联系方式时，优先使用列表脚本的 `--include_contacts` 自动链路；用户对完整任务最高费用确认一次后，内部按最多 20 个 ID 分批执行，不得逐批再次确认或展示中间结果。

自动链路会聚合全部批次的请求数、具体值合并数和缺失数。每批原始响应写入任务目录的 `contact_response_batches.jsonl`；具体联系方式合并数为 0 时，联系方式阶段返回失败状态并报告实际费用。
