"use strict";
// StockToday 接口权限分类 (从 gateway.py 复制, 单一 source of truth)
// 更新时间: 2026-06-15
// gateway.py 实际规则: V2 全部; V1 仅 LIGHT; V0 仅 plugins
Object.defineProperty(exports, "__esModule", { value: true });
exports.ALL_API_SET = exports.PRO_API_SET = exports.LIGHT_API_SET = exports.PRO_ONLY_APIS = exports.LIGHT_APIS = void 0;
exports.classifyUserAccess = classifyUserAccess;
exports.LIGHT_APIS = [
    'stock_basic', 'trade_cal', 'stock_st', 'namechange', 'stock_company', 'stk_managers', 'stk_rewards', 'new_share', 'bak_basic', 'bse_mapping', 'stock_hsgt',
    'daily', 'weekly', 'monthly', 'pro_bar', 'adj_factor', 'daily_basic', 'stk_limit', 'suspend_d', 'hsgt_top10', 'ggt_top10', 'bak_daily',
    'stk_weekly_monthly', 'stk_week_month_adj',
    'income', 'balancesheet', 'cashflow', 'forecast', 'express', 'dividend', 'fina_indicator', 'fina_audit', 'fina_mainbz', 'disclosure_date',
    'income_vip', 'balancesheet_vip', 'cashflow_vip', 'fina_indicator_vip', 'express_vip', 'forecast_vip', 'fina_mainbz_vip',
    'top10_holders', 'top10_floatholders', 'pledge_stat', 'pledge_detail', 'repurchase', 'share_float', 'block_trade', 'stk_holdernumber', 'stk_holdertrade',
    'moneyflow', 'moneyflow_hsgt', 'moneyflow_ths', 'moneyflow_dc', 'moneyflow_ind_ths', 'moneyflow_ind_dc', 'moneyflow_mkt_dc', 'moneyflow_cnt_ths',
    'top_list', 'top_inst', 'limit_list_d', 'limit_list_ths', 'limit_step', 'limit_cpt_list',
    'ths_index', 'ths_daily', 'ths_member', 'ths_hot',
    'dc_index', 'dc_daily', 'dc_member', 'dc_hot',
    'kpl_list', 'kpl_concept',
    'hm_list', 'hm_detail',
    'tdx_index', 'tdx_daily', 'tdx_member',
    'stk_auction',
    'cyq_perf', 'cyq_chips', 'ccass_hold', 'ccass_hold_detail', 'hk_hold',
    'broker_recommend', 'report_rc', 'stk_surv', 'stk_nineturn',
    'stk_ah_comparison', 'stk_factor_pro', 'ci_index_member',
    'ggt_daily', 'ggt_monthly', 'irm_qa_sz', 'irm_qa_sh',
    'bo_cinema', 'bo_daily', 'bo_monthly', 'bo_weekly', 'film_record', 'teleplay_record',
    'tmt_twincome', 'tmt_twincomedetail',
    'index_basic', 'index_daily', 'index_weekly', 'index_monthly', 'index_weight', 'index_dailybasic', 'index_classify', 'index_member_all', 'daily_info', 'sz_daily_info', 'index_global',
    'ci_daily', 'sw_daily', 'idx_factor_pro',
    'fund_basic', 'fund_company', 'fund_manager', 'fund_share', 'fund_nav', 'fund_div', 'fund_portfolio', 'fund_daily', 'fund_adj', 'fund_factor_pro',
    'fund_sales_ratio', 'fund_sales_vol',
    'etf_basic', 'etf_index', 'etf_share_size',
    'fut_basic', 'fut_daily', 'fut_weekly_monthly', 'fut_wsr', 'fut_settle', 'fut_holding', 'fut_mapping', 'fut_weekly_detail', 'ft_limit',
    'opt_basic', 'opt_daily',
    'cb_basic', 'cb_issue', 'cb_call', 'cb_rate', 'cb_daily', 'cb_share', 'cb_factor_pro',
    'repo_daily', 'bc_otcqt', 'bc_bestotcqt', 'bond_blk', 'bond_blk_detail',
    'eco_cal', 'shibor', 'shibor_quote', 'cn_gdp', 'cn_cpi', 'cn_ppi', 'cn_pmi', 'cn_m', 'sf_month',
    'libor', 'us_tbr', 'us_trycr', 'us_tltr', 'us_trltr', 'us_tycr', 'hibor', 'wz_index', 'gz_index',
    'fx_obasic', 'fx_daily',
    'hk_basic', 'hk_tradecal',
    'us_basic', 'us_tradecal',
    'sge_basic', 'sge_daily',
    'margin', 'margin_detail', 'margin_secs', 'slb_sec', 'slb_len', 'slb_sec_detail', 'slb_len_mm',
    'stk_account', 'stk_account_old',
    'kpl_concept_cons',
    'shibor_lpr',
];
exports.PRO_ONLY_APIS = [
    'hk_daily_adj', 'hk_income', 'hk_balancesheet', 'hk_cashflow', 'hk_fina_indicator', 'hk_adjfactor',
    'us_daily_adj', 'us_income', 'us_balancesheet', 'us_cashflow', 'us_fina_indicator', 'us_adjfactor',
    'news', 'major_news', 'cctv_news', 'anns_d', 'npr', 'research_report',
    'realtime_list', 'realtime_quote', 'realtime_tick',
    'cb_price_chg', 'stk_premarket', 'stk_auction_o', 'stk_auction_c',
    'yc_cb',
    'rt_min', 'rt_k', 'rt_idx_k', 'rt_sw_k', 'rt_idx_min', 'rt_etf_k', 'rt_fut_min', 'rt_hk_k',
    'stk_mins', 'ft_mins', 'idx_mins', 'opt_mins',
    'hk_daily', 'hk_mins', 'us_daily',
    'rt_etf_min', 'etf_mins',
    'rt_tick', 'rt_idx_tick', 'rt_etf_tick', 'rt_sw_tick', 'rt_hk_tick',
];
exports.LIGHT_API_SET = new Set(exports.LIGHT_APIS);
exports.PRO_API_SET = new Set(exports.PRO_ONLY_APIS);
exports.ALL_API_SET = new Set([...exports.LIGHT_APIS, ...exports.PRO_ONLY_APIS]);
/**
 * 核心 API: 给定用户权限和插件, 计算可用的 API 分类
 * 完全对齐 gateway.py 的 check_api_permission 逻辑
 */
function classifyUserAccess(permission, plugins, sampleSize = 8) {
    const perm = permission || 'V0';
    const pls = plugins || [];
    const lightArr = [];
    const proArr = [];
    const pluginArr = [];
    for (const api of exports.LIGHT_APIS) {
        if (perm === 'V0' ? pls.includes(api) : true)
            lightArr.push(api);
    }
    for (const api of exports.PRO_ONLY_APIS) {
        if (perm === 'V2') {
            proArr.push(api);
        }
        else if (perm === 'V0') {
            if (pls.includes(api))
                pluginArr.push(api);
        }
        else {
            // V1: 需要 plugin 解锁
            if (pls.includes(api))
                pluginArr.push(api);
        }
    }
    const total = lightArr.length + proArr.length + pluginArr.length;
    const tierMap = {
        V0: 'free', V1: 'basic', V2: 'advanced', V3: 'advanced', V4: 'advanced',
    };
    const tierLabelMap = {
        V0: '无基础权限 (仅 plugin)', V1: '基础版 (旗舰积分)', V2: '高级版 (龙虾套餐)', V3: '高级版', V4: '高级版',
    };
    // 抽样示例 (从不同分类挑 8 个有代表性的)
    const samples = [];
    const SAMPLES = {
        daily: 'A股日线行情',
        pro_bar: '复权行情',
        income: '利润表',
        fina_indicator: '财务指标',
        top_list: '龙虎榜',
        index_daily: '指数日线',
        fund_daily: '基金日线',
        hk_daily: '港股日线',
        realtime_quote: '实时报价',
        stk_factor_pro: '股票因子(专业)',
        rt_tick: '股票实时Tick',
        news: '新闻资讯',
    };
    const pickOrder = ['daily', 'pro_bar', 'income', 'fina_indicator', 'top_list', 'index_daily', 'fund_daily', 'hk_daily', 'realtime_quote', 'stk_factor_pro', 'rt_tick', 'news'];
    for (const n of pickOrder) {
        if (samples.length >= sampleSize)
            break;
        if (lightArr.includes(n) || proArr.includes(n) || pluginArr.includes(n)) {
            samples.push({ name: n, description: SAMPLES[n] || n });
        }
    }
    return {
        tier: tierMap[perm] || 'unknown',
        tierLabel: tierLabelMap[perm] || perm,
        totalAvailable: total,
        totalUnavailable: 240 - total,
        lightApisAvailable: lightArr.length,
        proApisAvailable: proArr.length,
        pluginUnlockedApis: pluginArr,
        examples: samples,
    };
}
