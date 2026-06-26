---
name: xtrade-futu-paper-trade
description: 使用富途纸面交易API查询行情、持仓并下单
metadata: {"openclaw":{"requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# 富途纸面交易 Skill

当用户需要查询行情、持仓、订单、成交或下单时，调用此技能。使用本技能时：
- 统一通过 {baseDir}/xtrade_xtrade_futu_skill.py 执行
- 首次执行会自动创建虚拟环境并安装依赖
- 依赖本地 FutuOpenD 服务

自动安装与引导
- 本技能会自动创建虚拟环境并安装 Python 依赖
- 若系统缺少 python3，请先安装后再重试
- 自动选择兼容 futu-api 的 Python 3.10/3.11/3.12 并重建虚拟环境
- FutuOpenD 属于官方程序，无法由技能自动下载安装
- 可使用 check 指令自动检测并给出引导步骤
- 完成后仅需设置 FUTU_TRADE_PWD 即可交易
- 安全限制：仅允许纸面交易，检测到 REAL 会拒绝执行

FutuOpenD 下载与登录
- 下载入口：https://www.futuhk.com/en/support/topic1_464
- 安装后解压，按文档启动 OpenD（Mac/Windows/Linux）并保持运行
- 登录方式：使用命令行参数 -login_account 与 -login_pwd 启动，不落盘保存密码
- 安全特性：默认不要求在本地保存账号密码

环境变量
- FUTU_HOST：FutuOpenD 地址，默认 127.0.0.1
- FUTU_PORT：FutuOpenD 端口，默认 11111
- FUTU_TRD_ENV：交易环境，仅支持 PAPER（或 SIMULATE）
- FUTU_TRD_MARKET：交易市场，默认 HK
- FUTU_TRADE_PWD：交易解锁密码
- FUTU_ACCOUNT：账号标识，可选
- FUTU_PASSWORD：账号密码，可选

常用命令
- 环境检查：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py check
- 查询账户资金与资产：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py funds
- 查询实时行情：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py quote --symbols HK.00700 HK.09988
- 查询持仓：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py positions
- 查询今日盈亏：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py today-pnl
- 下单买入：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py buy --symbol HK.00700 --qty 100 --price 320.5
- 下单卖出：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py sell --symbol HK.00700 --qty 100 --price 321.0
- 查询订单：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py orders --status all
- 撤单：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py cancel --order-id 8851102695472794941
- 查询成交（默认当日）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py fills --days 1
- 获取历史 K 线（日线）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py historical-kline --code HK.00700 --start 2025-01-01 --end 2025-01-31 --ktype DAY
- 获取历史 K 线（周线）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py historical-kline --code HK.00700 --start 2024-01-01 --end 2025-01-31 --ktype WEEK
- 获取历史 K 线（月线）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py historical-kline --code HK.00700 --start 2020-01-01 --end 2025-01-31 --ktype MONTH
- 获取历史 K 线（分钟线）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py historical-kline --code HK.00700 --start 2025-01-01 --end 2025-01-02 --ktype 1M
- 获取历史 K 线（分页）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py historical-kline --code HK.00700 --start 2025-01-01 --end 2025-01-31 --ktype DAY --max-count 200 --page-req-key <page_req_key>
- 查询财务报表：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py financial-report --code SH.600519 --start 2024-01-01 --end 2024-12-31
- 查询财务指标（季度）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py financial-indicators --code SH.600519 --period QUARTER
- 查询财务指标（半年度）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py financial-indicators --code SH.600519 --period HALF
- 查询财务指标（年度）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py financial-indicators --code SH.600519 --period YEAR
- 查询资产负债表（季度）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py financial-balance --code SH.600519 --period QUARTER
- 查询利润表（半年度）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py financial-income --code SH.600519 --period HALF
- 查询现金流量表（年度）：
  python3 {baseDir}/xtrade_xtrade_futu_skill.py financial-cashflow --code SH.600519 --period YEAR

替代接口说明
- financial-report、financial-indicators、financial-balance、financial-income、financial-cashflow 默认优先使用 futu-api
- 当 futu-api 缺失相关接口时，A 股与港股回退 AkShare
- A 股财务报表来自新浪财经（SH./SZ.）
- 港股财务指标来自东方财富，港股财务报表依赖 AkShare 港股接口支持

输出说明
- 所有输出为 JSON
- 失败时返回 error 字段，包含原因与建议
