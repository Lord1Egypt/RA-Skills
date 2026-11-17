
const DEFS = {
  AttrDTO: {
    type: "object",
    description: "线索画像标签/属性",
    properties: {
      attr_key: { type: "string", description: "属性键（原始 code）" },
      attr_label: { type: "string", description: "属性展示名（中文）" },
      attr_values: { type: "array", items: { type: "string" }, description: "属性值，多值时为数组" },
      source: {
        type: "string",
        enum: ["inner", "outer", "manual", "system"],
        description: "属性来源：inner=站内画像 outer=站外画像 manual=人工录入 system=系统规则计算",
      },
      category: {
        type: "integer",
        enum: [0, 1],
        description: "0=普通（非标签类展示），1=标签类（公海/私海列表页展示的标签）",
      },
    },
  },
  FollowLogDTO: {
    type: "object",
    description: "跟进日志条目",
    properties: {
      content: { type: "string", description: "渲染好的变更内容文案，前端/CLI 直接展示" },
      created_at: { type: "integer", description: "毫秒时间戳" },
      action_type: {
        type: "string",
        enum: ["claim", "release", "assign", "follow_status", "accept_level", "remark", "convert", "audit"],
        description: "操作类型 code",
      },
      action_name: {
        type: "string",
        description:
          "操作类型中文名，按 action_type 反查：claim=认领线索 release=释放线索 assign=指派线索 follow_status=修改状态 accept_level=修改采纳 remark=跟进记录 convert=转化入驻 audit=审核操作",
      },
      operator_id: { type: "string", description: "操作人ID" },
      operator_name: { type: "string", description: "操作人姓名" },
    },
  },
  HotItemDTO: {
    type: "object",
    description: "热卖商品，get_lead_detail 按站外店铺查询填充",
    properties: {
      item_id: { type: "string", description: "商品ID" },
      title: { type: "string", description: "商品标题" },
      image_urls: { type: "array", items: { type: "string" }, description: "商品图片链接" },
      price: { type: "number", description: "商品价格" },
      month_sales: { type: "integer", description: "月销量" },
      total_sales: { type: "integer", description: "总销量" },
      item_url: { type: "string", description: "商品链接" },
    },
  },
  OuterShopDTO: {
    type: "object",
    description: "站外店铺信息",
    properties: {
      shop_id: { type: "string", description: "站外平台店铺ID" },
      shop_name: { type: "string", description: "店铺名称（原始名，含旗舰店/专卖店等后缀）" },
      company_name: { type: "string", description: "店铺主体公司名" },
      license_no: { type: "string", description: "营业执照号" },
      legal_person: { type: "string", description: "法定代表人姓名" },
      platform: {
        type: "integer",
        enum: [0, 1, 2, 3, 4],
        description: "站外平台：0=小红书 1=抖音 2=京东 3=得物 4=淘天（淘宝+天猫）",
      },
      platform_name: { type: "string", description: "平台名称中文展示（如“淘天”“抖音”）" },
      shop_type_zh: { type: "string", description: "店铺类型中文，常见取值：旗舰店/专营店/企业店等（自由文本，非强枚举）" },
      main_category: { type: "string", description: "主营类目" },
      location: { type: "string", description: "店铺所在地区" },
      settle_status: { type: "string", description: "入驻状态，常见取值：正常营业/已关店/已注册/未注册（自由文本，非强枚举）" },
      avg_item_price: { type: "integer", description: "站外客单价，⚠️ 单位：分（不是元）" },
      month_gmv: { type: "integer", description: "月GMV，单位：元（已截断为整数）" },
      year_gmv: { type: "integer", description: "近12个月GMV（字段名叫 year_gmv，口径是近12个月而非自然年），单位：元（已截断为整数）" },
      b_level: {
        type: "string",
        enum: ["B0", "B1", "B2", "B3", "B4", "B5", "B6"],
        description: "GMV分层等级，基于月GMV计算，数字越大等级越高（B6最高）",
      },
      shop_url: { type: "string", description: "店铺链接" },
      ext: { type: "object", description: "资质/行业标签等", additionalProperties: { type: "string" } },
      qcc_phone: {
        type: "string",
        description: "企业工商注册电话（企查查来源）。⚠️ 受 get_lead_detail 的 plain_phone 开关控制：plain_phone=false（list_* 接口固定用这个）时脱敏，true 时明文",
      },
      qcc_phone_zone: { type: "string", description: "qcc_phone 的区号部分" },
      hot_items: { type: "array", items: { $ref: "#/$defs/HotItemDTO" } },
    },
  },
  LeadExtraMetricDTO: {
    type: "object",
    description: "线索扩展指标：10 个 0-100 行业百分位字段",
    properties: {
      fans_dgmv_pct: { type: "number", description: "站内粉丝DGMV行业百分位" },
      trade_fan_avg_dgmv_pct: { type: "number", description: "交易粉丝人均DGMV行业百分位" },
      avg_note_ces_pct: { type: "number", description: "平均笔记CES行业百分位" },
      outer_gmv30d_pct: { type: "number", description: "站外近一个月GMV行业百分位" },
      outer_gmv1y_pct: { type: "number", description: "站外近一年GMV行业百分位" },
      outer_avg_item_price_pct: { type: "number", description: "站外客单价行业百分位" },
      outer_monthly_sales_pct: { type: "number", description: "月销量行业百分位" },
      fans_pct: { type: "number", description: "粉丝数行业百分位" },
      note_cnt30d_pct: { type: "number", description: "近30天有效笔记数行业百分位" },
      total_asset_pct: { type: "number", description: "人群资产行业百分位" },
    },
  },
  InsiteAccountDTO: {
    type: "object",
    description: "站内小红书账号信息",
    properties: {
      author_id: { type: "string", description: "小红书账号唯一标识" },
      nickname: { type: "string", description: "账号昵称" },
      account_url: { type: "string", description: "账号主页链接，固定格式 https://www.xiaohongshu.com/user/profile/{author_id}" },
      region: { type: "string", description: "常驻地区，省+市拼接" },
      follower_count: { type: "integer", description: "累计粉丝数" },
      note_count: { type: "integer", description: "⚠️ 字段名是 note_count，实际口径是近30天有效笔记数，不是账号历史全部笔记数" },
      avg_note_ces: { type: "number", description: "笔记 CES 值" },
      fans_dgmv: { type: "integer", description: "粉丝近30天导购GMV，单位：分" },
      fan_buyer_cnt30d: { type: "integer", description: "粉丝近30天下单用户数" },
      trade_fan_avg_dgmv: { type: "integer", description: "粉丝近30天人均导购GMV，单位：分" },
      insite_carrier_dgmv30d: { type: "number", description: "站内经营载体近30天成交额" },
      insite_shop_url: { type: "string", description: "站内店铺链接" },
      total_asset: { type: "integer", description: "总资产（站外GMV+站内导购GMV之和），单位：元" },
      like_cnt30d: { type: "integer", description: "近30天点赞数" },
      fav_cnt30d: { type: "integer", description: "近30天收藏数" },
      gender_dist: { type: "string", description: "粉丝性别分布，JSON 字符串" },
      age_dist: { type: "string", description: "粉丝年龄段分布，JSON 字符串" },
      fan_r_level_dist: { type: "string", description: "粉丝R等级分布，JSON 字符串（如 {\"R1\":100,\"R2\":50,...}）" },
      fan_r4_plus_ratio: { type: "number", description: "R4+粉丝占比，百分数（如 12.34 表示 12.34%）" },
      carrier_dgmv_dist: { type: "string", description: "站内成交载体近30天成交分布，JSON 字符串" },
      ext: { type: "object", description: "资质/行业标签等", additionalProperties: { type: "string" } },
      login_phone: {
        type: "string",
        description: "登录手机号。⚠️ 受 get_lead_detail 的 plain_phone 开关控制：plain_phone=false（list_* 接口固定用这个）时脱敏，true 时明文",
      },
      login_phone_zone: { type: "string", description: "login_phone 的区号部分" },
      pro_account_phone: {
        type: "string",
        description: "专业号客服电话。⚠️ 同 login_phone，受 plain_phone 开关控制",
      },
      pro_account_phone_zone: { type: "string", description: "pro_account_phone 的区号部分" },
    },
  },
  LeadDTO: {
    type: "object",
    description: "线索完整信息。get_lead_detail 的 data.lead 与 list_private_leads / list_public_leads 的 data.leads[] 元素共用这份 schema",
    properties: {
      lead_id: { type: "string", description: "线索唯一ID（UUID）" },
      lead_name: { type: "string", description: "线索名称（已去除旗舰店/专卖店等常见店铺类型后缀的品牌/商家名）" },
      source_type: { type: "string", enum: ["outer", "insite"], description: "线索来源：outer=站外 / insite=站内" },
      score_level: {
        type: "string",
        enum: ["S0", "S1", "S2"],
        description: "线索评分等级，S0 最高、S2 最低",
      },
      score: { type: "number", description: "线索综合评分，0~100分" },
      owner_id: { type: "string", description: "未认领时为空字符串" },
      owner_name: { type: "string", description: "未认领时为空字符串" },
      owner_email: { type: "string", description: "未认领时为空字符串" },
      owner_dept_id: { type: "string", description: "未认领时为空字符串" },
      owner_dept_name: { type: "string", description: "未认领时为空字符串" },
      claimed_at: { type: "integer", description: "认领时间戳（毫秒）" },
      expected_release_time: {
        type: "integer",
        description:
          "私海线索预计释放时间（毫秒时间戳），只要线索在私海就一定有值。⚠️ 这只是展示用的预计时间，已客保/已挂接的线索实际不会被释放，不代表到点一定释放；get_lead_detail 没有这个字段，只有 list_private_leads 才返回。",
      },
      follow_status: {
        type: "string",
        enum: ["PENDING", "CONTACTED", "TALKING", "INTERESTED", "NO_INTENT", "PROPOSAL_SENT", "PROTECTED", "SETTLED", "CRM_BLOCKED"],
        description:
          "PENDING=待建联 CONTACTED=已建联 TALKING=沟通中 INTERESTED=有明确意向 NO_INTENT=无意向(终态) PROPOSAL_SENT=已提供营销方案 PROTECTED=已客保 SETTLED=已入驻(终态) CRM_BLOCKED=已被CRM挂接(终态)",
      },
      accept_level: {
        type: "integer",
        enum: [300, 200, 100, -100],
        description: "300=P0(强意向) 200=P1(中意向) 100=P2(弱意向) -100=不采纳；未标记时字段可能缺省",
      },
      remark: { type: "string", description: "运营填写的跟进备注" },
      industry: { type: "string", description: "线索所属行业中文名，与团队类型判定/权限过滤口径一致" },
      created_at: { type: "integer", description: "毫秒时间戳" },
      audit_status: {
        type: "integer",
        enum: [0, 1, 2, 3],
        description: "0=待审核 1=已上线（对普通用户可见） 2=已驳回 3=已下线",
      },
      team_type: {
        type: "integer",
        enum: [0, 1, 2],
        description: "0=生态+KA共享 1=生态 2=KA",
      },
      audit_time: { type: "integer", description: "毫秒时间戳" },
      lead_status: {
        type: "integer",
        enum: [0, 1, 2, 3, 4, 5],
        description: "0=未注册 1=已注册可客保 2=已开店可客保 3=未开店已客保 4=已开店已客保 5=已挂接(CRM)",
      },
      attrs: { type: "array", items: { $ref: "#/$defs/AttrDTO" } },
      follow_logs: { type: "array", items: { $ref: "#/$defs/FollowLogDTO" } },
      outer_shops: { type: "array", items: { $ref: "#/$defs/OuterShopDTO" } },
      insite_accounts: { type: "array", items: { $ref: "#/$defs/InsiteAccountDTO" } },
      extra_metric: { $ref: "#/$defs/LeadExtraMetricDTO" },
    },
  },
};

const RESPONSE_ENVELOPE = {
  success: { type: "boolean" },
  code: { type: "integer" },
  msg: { type: "string" },
};

// list_private_leads / list_public_leads 共用的过滤字段（除各自独有的 follow_status/accept_level/not_online 外）
const LIST_COMMON_FILTER_PROPERTIES = {
  lead_id: { type: "string", description: "线索唯一ID（UUID）" },
  lead_name: { type: "string", description: "线索名称模糊匹配（跟 keyword 是同一个底层字段，两者都传取交集）" },
  industries: { type: "array", items: { type: "string" }, description: "行业中文名多选（IN），如 [\"美妆\", \"3C\"]" },
  score_level: {
    type: "string",
    enum: ["S0", "S1", "S2"],
    description: "线索评分等级精确匹配，S0 最高、S2 最低",
  },
  keyword: { type: "string", description: "关键词搜索，目前实现上等同于按线索名称模糊匹配，跟 lead_name 是同一个底层字段" },
  platform: {
    type: "integer",
    enum: [0, 1, 2, 3, 4],
    description: "站外平台：0=小红书 1=抖音 2=京东 3=得物 4=淘天（淘宝+天猫）；筛的是站外店铺所在平台",
  },
  main_category: { type: "string", description: "站外店铺主营类目模糊匹配" },
  settle_status: { type: "string", description: "站外店铺入驻状态精确匹配，常见取值：正常营业/已关店/已注册/未注册（自由文本，非强枚举）" },
  outer_shop_type: { type: "string", description: "站外店铺类型精确匹配，常见取值：旗舰店/专营店/企业店等（自由文本，非强枚举）" },
  avg_item_price_min: { type: "integer", description: "站外客单价下限，单位：分" },
  avg_item_price_max: { type: "integer", description: "站外客单价上限，单位：分" },
  insite_shop_type: { type: "string", description: "站内商家类型精确匹配，取值：工厂直供/矿口/产地/批发商/品牌/主理人/零售商/其他" },
  follower_count_min: { type: "integer", description: "站内账号粉丝数下限" },
  follower_count_max: { type: "integer", description: "站内账号粉丝数上限" },
  province: { type: "string", description: "账号/店铺常驻省份精确匹配" },
  brand_name: { type: "string", description: "品牌名称模糊匹配" },
  followable_status: { type: "string", description: "可跟进状态精确匹配" },
  lead_status: {
    type: "integer",
    enum: [0, 1, 2, 3, 4, 5],
    description: "0=未注册 1=已注册可客保 2=已开店可客保 3=未开店已客保 4=已开店已客保 5=已挂接(CRM)",
  },
  page_num: { type: "integer", default: 1 },
  page_size: { type: "integer", default: 20, description: "服务端上限 500" },
};

export const API_SCHEMAS = {
  get_lead_detail: {
    id: "get_lead_detail",
    command: "get-lead-detail",
    path: "/edith/api/seller/merchant_lead/get_lead_detail",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "获取线索详情",
    notes: [
      "⚠️ 不是纯只读接口：当 source=private 且 plain_phone=true 时，(1) insite_accounts[].login_phone/pro_account_phone 和 outer_shops[].qcc_phone 会连同主手机号一起返回明文（默认脱敏）；(2) 如果该线索当前是 PENDING/CONTACTED 状态，会静默把跟进状态自动推进为 TALKING。没有明确业务需要、没有征得用户同意之前不要传 plain_phone=true。",
      "没有权限查看该 lead_id 时，响应会伪装成业务失败 \"lead not found\"，不会明确提示\"无权限\"——遇到 not found 不代表 lead_id 一定错了，也可能是没权限看这条线索所属的行业/团队。",
      "⚠️ CLI 会给 data.lead 追加 quality_highlight（非后端原始字段，本地基于 extra_metric 计算），用于生成“优秀指标”一句话摘要，规则见 SKILL.md「详情视图」。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        source: { type: "string", enum: ["private", "public"], description: "私海详情传 private 才可能返回明文手机号，见 notes" },
        plain_phone: { type: "boolean", default: false, description: "是否返回明文手机号，见 notes 的 PII 警示" },
      },
      required: ["lead_id"],
    },
    responseSchema: {
      type: "object",
      properties: { ...RESPONSE_ENVELOPE, data: { type: "object", properties: { lead: { $ref: "#/$defs/LeadDTO" } } } },
      $defs: DEFS,
    },
  },

  list_private_leads: {
    id: "list_private_leads",
    command: "list-private-leads",
    path: "/edith/api/seller/merchant_lead/list_private_leads",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "查询私海线索列表",
    notes: [
      "owner 永远是当前登录人，请求里没有也不能传别人的 owner——不存在“查别人私海”这回事。",
      "没有权限查看的线索会被伪装成 \"lead not found\"，不会明确提示\"无权限\"——遇到 not found 不代表 lead_id 一定错了，也可能是没权限看这条线索所属的行业/团队。",
      "⚠️ CLI 会给每条线索追加 quality_highlight（非后端原始字段，本地基于 extra_metric 计算），用于生成“优秀指标”一句话摘要，规则见 SKILL.md「列表视图」。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        ...LIST_COMMON_FILTER_PROPERTIES,
        follow_status: {
          type: "string",
          enum: ["PENDING", "CONTACTED", "TALKING", "INTERESTED", "NO_INTENT", "PROPOSAL_SENT", "PROTECTED", "SETTLED", "CRM_BLOCKED"],
          description: "私海独有过滤字段",
        },
        accept_level: {
          type: "integer",
          enum: [300, 200, 100, -100],
          description: "私海独有过滤字段，数字 code 不是字符串",
        },
      },
      required: [],
    },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            page_num: { type: "integer" },
            page_size: { type: "integer" },
            leads: { type: "array", items: { $ref: "#/$defs/LeadDTO" } },
          },
        },
      },
      $defs: DEFS,
    },
  },

  list_public_leads: {
    id: "list_public_leads",
    command: "list-public-leads",
    path: "/edith/api/seller/merchant_lead/list_public_leads",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "查询公海线索列表",
    notes: [
      "没有权限查看的线索会被伪装成 \"lead not found\"，不会明确提示\"无权限\"——遇到 not found 不代表 lead_id 一定错了，也可能是没权限看这条线索所属的行业/团队。",
      "⚠️ CLI 会给每条线索追加 quality_highlight（非后端原始字段，本地基于 extra_metric 计算），用于生成“优秀指标”一句话摘要，规则见 SKILL.md「列表视图」。",
      "recommend 仅本接口支持，list_private_leads 没有这个字段；向用户表达时的措辞规则见 SKILL.md「智能推荐」。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        ...LIST_COMMON_FILTER_PROPERTIES,
        not_online: { type: "boolean", description: "未传或 false=只看已上线；true=只看未上线/待审核" },
        recommend: { type: "boolean", default: false, description: "true=按你的历史行业命中优先排序；未传或 false=原始排序" },
      },
      required: [],
    },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            page_num: { type: "integer" },
            page_size: { type: "integer" },
            leads: { type: "array", items: { $ref: "#/$defs/LeadDTO" } },
          },
        },
      },
      $defs: DEFS,
    },
  },

  private_stat: {
    id: "private_stat",
    command: "private-stat",
    path: "/edith/api/seller/merchant_lead/private_stat",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "私海线索概览统计",
    notes: ["ownerId 完全来自登录态（IDL 已删除 req.ownerId 字段），不需要也不能传参数。"],
    requestSchema: { type: "object", properties: {}, required: [] },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            following_count: { type: "integer", description: "跟进中（TALKING）" },
            converted_count: { type: "integer", description: "已客保（PROTECTED）" },
            settled_count: { type: "integer", description: "已入驻数" },
            active_count: { type: "integer", description: "动销数" },
            converted_gmv: { type: "integer", description: "转化累计 GMV" },
            public_total: { type: "integer", description: "对侧公海总数（权限过滤后）" },
          },
        },
      },
    },
  },

  public_stat: {
    id: "public_stat",
    command: "public-stat",
    path: "/edith/api/seller/merchant_lead/public_stat",
    method: "POST",
    mutating: false,
    verified: true,
    summary: "公海数据信息",
    notes: [],
    requestSchema: { type: "object", properties: {}, required: [] },
    responseSchema: {
      type: "object",
      properties: {
        ...RESPONSE_ENVELOPE,
        data: {
          type: "object",
          properties: {
            total: { type: "integer" },
            s0_count: { type: "integer" },
            s1_count: { type: "integer" },
            s2_count: { type: "integer" },
            private_total: { type: "integer", description: "当前用户自己的私海总数" },
          },
        },
      },
    },
  },

  update_follow_status: {
    id: "update_follow_status",
    command: "update-follow-status",
    path: "/edith/api/seller/merchant_lead/update_follow_status",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "更新跟进状态",
    notes: ["follow_status 服务端严格校验，传枚举外的值直接报错（不是静默忽略）。"],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        follow_status: {
          type: "string",
          enum: ["PENDING", "CONTACTED", "TALKING", "INTERESTED", "NO_INTENT", "PROPOSAL_SENT", "PROTECTED", "SETTLED", "CRM_BLOCKED"],
          description:
            "PENDING=待建联 CONTACTED=已建联 TALKING=沟通中 INTERESTED=有明确意向 NO_INTENT=无意向(终态) PROPOSAL_SENT=已提供营销方案 PROTECTED=已客保 SETTLED=已入驻(终态) CRM_BLOCKED=已被CRM挂接(终态)",
        },
      },
      required: ["lead_id", "follow_status"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  update_remark: {
    id: "update_remark",
    command: "update-remark",
    path: "/edith/api/seller/merchant_lead/update_remark",
    method: "POST",
    mutating: true,
    verified: true,
    summary: "更新线索备注",
    notes: [
      "lead_id 必须用下划线命名传参；用驼峰 leadId 会被网关当成缺少必填参数拦截。",
      "不要多传 schema 之外的字段（例如 not_online）——多传会导致服务端返回业务性的 \"lead not found\"，而不是静默忽略。",
      "remark 传空字符串会被当成清空备注处理，不会报错。",
    ],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        source: { type: "string", enum: ["private", "public"], description: "缺失会导致服务端报 500 EOF" },
        remark: { type: "string", description: "备注内容，允许空字符串（清空备注）" },
      },
      required: ["lead_id", "source", "remark"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  update_accept_level: {
    id: "update_accept_level",
    command: "update-accept-level",
    path: "/edith/api/seller/merchant_lead/update_accept_level",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "更新采纳情况（私海优先级）",
    notes: ["⚠️ accept_level 是数字 code，不是 \"P0\" 这种字符串；传枚举外的数字会被服务端拒绝。"],
    requestSchema: {
      type: "object",
      properties: {
        lead_id: { type: "string", description: "线索 ID" },
        accept_level: {
          type: "integer",
          enum: [300, 200, 100, -100],
          description: "300=P0(强意向) 200=P1(中意向) 100=P2(弱意向) -100=不采纳",
        },
      },
      required: ["lead_id", "accept_level"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  claim_lead: {
    id: "claim_lead",
    command: "claim-lead",
    path: "/edith/api/seller/merchant_lead/claim_lead",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "认领线索",
    notes: [
      "认领人身份完全来自登录态（token 对应的操作人），不能代别人认领。",
      "业务错误“线索已被认领，请刷新页面查看最新数据”是正常的抢单失败场景，不代表调用方式错了。",
      "⚠️ 认领后如需撤销，用 release-lead（把线索释放回公海）。",
    ],
    requestSchema: {
      type: "object",
      properties: { lead_id: { type: "string", description: "线索 ID" } },
      required: ["lead_id"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  release_lead: {
    id: "release_lead",
    command: "release-lead",
    path: "/edith/api/seller/lead/release_lead",
    method: "POST",
    mutating: true,
    verified: false,
    summary: "释放线索（私海→公海，claim-lead 的反向操作）",
    notes: [
      "把线索从私海释放回公海，是目前唯一能撤销 claim-lead 认领的接口。",
    ],
    requestSchema: {
      type: "object",
      properties: { lead_id: { type: "string", description: "线索 ID" } },
      required: ["lead_id"],
    },
    responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  },

  // assign_lead: 暂时下线，保留代码待后续需要时恢复。
  // assign_lead: {
  //   id: "assign_lead",
  //   command: "assign-lead",
  //   path: "/edith/api/seller/merchant_lead/assign_lead",
  //   method: "POST",
  //   mutating: true,
  //   verified: false,
  //   summary: "分配线索",
  //   notes: [
  //     "只改归属人（owner），不会动跟进状态（follow_status）。",
  //     "触发分配动作的操作人来自登录态，跟 owner_* 字段（被分配人）是两个不同的角色，不要混淆。",
  //   ],
  //   requestSchema: {
  //     type: "object",
  //     properties: {
  //       lead_id: { type: "string", description: "线索 ID" },
  //       owner_id: { type: "string", description: "被分配人的操作人 ID（必填）" },
  //       owner_name: { type: "string" },
  //       owner_email: { type: "string" },
  //       owner_dept_id: { type: "string" },
  //       owner_dept_name: { type: "string" },
  //     },
  //     required: ["lead_id", "owner_id"],
  //   },
  //   responseSchema: { type: "object", properties: { ...RESPONSE_ENVELOPE } },
  // },
};

export function listCommands() {
  return Object.values(API_SCHEMAS);
}

export function getSchemaByCommand(command) {
  return listCommands().find((s) => s.command === command) || null;
}
