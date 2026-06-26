#!/usr/bin/env python3
"""
Token Query Script v2.1 - 使用浏览器绕过 Cloudflare
基于 GMGN API 文档，通过浏览器 fetch 获取数据
"""

import json
import sys
import asyncio
import websockets
import urllib.request
import subprocess

CHROME_WS_BASE = "ws://localhost:9222"

# GMGN API 配置
GMGN_BASE = "https://gmgn.ai"
DEVICE_ID = "bf3bd459-9cc5-46f0-95bf-8297b8a58c72"
FP_DID = "c44ca81f8d7dabb1d0dc62c33c0ee26d"
CLIENT_ID = "gmgn_web_20260304-11376-fc51c8a"
FROM_APP = "gmgn"
APP_VER = "20260304-11376-fc51c8a"
TZ_NAME = "Asia/Shanghai"
TZ_OFFSET = "28800"
APP_LANG = "zh-CN"
OS = "web"
WORKER = "0"

def get_common_params():
    return f"device_id={DEVICE_ID}&fp_did={FP_DID}&client_id={CLIENT_ID}&from_app={FROM_APP}&app_ver={APP_VER}&tz_name={TZ_NAME}&tz_offset={TZ_OFFSET}&app_lang={APP_LANG}&os={OS}&worker={WORKER}"

def fetch_twitter_data_bird(twitter_url):
    """使用 bird CLI 获取推特数据（同步函数）"""
    if not twitter_url:
        return None
    
    # 从 URL 中提取用户名
    # 支持格式：@username, username, https://x.com/username, username/status/123
    username = None
    
    if 'x.com/' in twitter_url or 'twitter.com/' in twitter_url:
        parts = twitter_url.split('/')
        for i, part in enumerate(parts):
            if part in ['x.com', 'twitter.com'] and i + 1 < len(parts):
                username = parts[i + 1]
                break
    elif '/' in twitter_url:
        # 处理 username/status/123 格式
        username = twitter_url.split('/')[0]
    else:
        username = twitter_url.strip('@')
    
    if not username or 'communities' in username or 'status' in username or username.isdigit():
        return None
    
    try:
        # 获取用户推文（包含用户信息）
        tweets_result = subprocess.run(
            ['bird', 'user-tweets', username, '-n', '10', '--json-full'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if tweets_result.returncode != 0:
            return None
        
        tweets = json.loads(tweets_result.stdout)
        if not tweets:
            return None
        
        # 从第一条推文的 _raw 中提取完整用户信息
        first_tweet = tweets[0]
        raw_data = first_tweet.get('_raw', {})
        
        # 尝试从 core.user_results.result.legacy 中获取用户信息
        user_legacy = raw_data.get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {})
        
        return {
            'username': user_legacy.get('screen_name', username),
            'followers': user_legacy.get('followers_count', 0),
            'bio': user_legacy.get('description', ''),
            'location': user_legacy.get('location', ''),
            'tweets': tweets
        }
    except Exception as e:
        return None

# 格式化函数
def fmt_num(n):
    if n is None: return "N/A"
    n = float(n)
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.2f}M"
    if n >= 1e3: return f"${n/1e3:.1f}K"
    return f"${n:.2f}"

def fmt_price(p):
    if p is None: return "N/A"
    p = float(p)
    if p >= 1: return f"${p:.4f}"
    if p >= 0.001: return f"${p:.8f}".rstrip('0')
    return f"${p:.12f}".rstrip('0')

async def get_page_id():
    try:
        resp = urllib.request.urlopen(f"http://localhost:9222/json/list")
        tabs = json.loads(resp.read())
        # 优先使用 gmgn.ai 页面
        for t in tabs:
            if t.get('type') == 'page' and 'gmgn.ai' in t.get('url', ''):
                return t['id']
        # 如果没有 gmgn.ai 页面，使用第一个页面
        for t in tabs:
            if t.get('type') == 'page':
                return t['id']
    except Exception as e:
        print(f"Error getting page ID: {e}", file=sys.stderr)
    return None

async def chrome_fetch(ws, url):
    js = f"fetch('{url}').then(r=>r.json())"
    await ws.send(json.dumps({'id':1,'method':'Runtime.evaluate','params':{'expression':js,'awaitPromise':True}}))
    resp = await ws.recv()
    result = json.loads(resp).get('result',{}).get('result',{})
    if result.get('type') == 'object':
        # 获取对象的 JSON 字符串
        obj_id = result.get('objectId')
        if obj_id:
            await ws.send(json.dumps({'id':2,'method':'Runtime.callFunctionOn','params':{'objectId':obj_id,'functionDeclaration':'function(){return JSON.stringify(this)}'}}))
            resp2 = await ws.recv()
            json_str = json.loads(resp2).get('result',{}).get('result',{}).get('value','{}')
            return json.loads(json_str)
    return {}

async def fetch_token_data(ws, chain, address):
    params = get_common_params()
    result = {}
    
    # 1. 代币统计
    url = f"{GMGN_BASE}/api/v1/token_stat/{chain}/{address}?{params}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        stat = data.get('data', {})
        result['holder_count'] = stat.get('holder_count')
        result['top_10_holder_rate'] = float(stat.get('top_10_holder_rate', 0))
    
    # 2. 安全检测
    url = f"{GMGN_BASE}/api/v1/mutil_window_token_security_launchpad/{chain}/{address}?{params}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        security = data.get('data', {}).get('security', {})
        result['is_honeypot'] = security.get('is_honeypot', False)
        result['is_renounced'] = security.get('is_renounced', False)
        result['buy_tax'] = security.get('buy_tax', '0')
        result['sell_tax'] = security.get('sell_tax', '0')
        result['is_open_source'] = security.get('is_open_source', False)
    
    # 3. 搜索获取基础信息
    url = f"{GMGN_BASE}/vas/api/v1/search_v3?{params}&chain={chain}&q={address}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        coins = data.get('data', {}).get('coins', [])
        if coins:
            coin = coins[0]
            result['name'] = coin.get('name')
            result['symbol'] = coin.get('symbol')
            result['price'] = float(coin.get('price', 0))
            result['market_cap'] = float(coin.get('mcp', 0))
            result['liquidity'] = float(coin.get('liquidity', 0))
            result['volume_24h'] = float(coin.get('volume_24h', 0))
            
            # 计算24小时涨跌幅
            price_24h = coin.get('price_24h')
            if price_24h and float(price_24h) > 0:
                current_price = float(coin.get('price', 0))
                price_24h_float = float(price_24h)
                result['change_24h'] = ((current_price - price_24h_float) / price_24h_float) * 100
    
    # 4. K线数据获取5分钟和1小时涨跌幅
    url = f"{GMGN_BASE}/api/v1/token_mcap_candles/{chain}/{address}?{params}&pool_type=tpool&resolution=5m&limit=15"
    candle_data = await chrome_fetch(ws, url)
    if candle_data.get('code') == 0:
        candles = candle_data.get('data', {}).get('list', [])
        if len(candles) >= 2:
            current_price = float(candles[-1].get('close', 0))
            # 5分钟涨跌幅
            price_5m_ago = float(candles[-2].get('close', 0))
            if price_5m_ago > 0:
                result['change_5m'] = ((current_price - price_5m_ago) / price_5m_ago) * 100
            # 1小时涨跌幅 (12个5分钟K线)
            if len(candles) >= 13:
                price_1h_ago = float(candles[-13].get('close', 0))
                if price_1h_ago > 0:
                    result['change_1h'] = ((current_price - price_1h_ago) / price_1h_ago) * 100
    
    # 5. 链接信息
    url = f"{GMGN_BASE}/api/v1/mutil_window_token_link_rug_vote/{chain}/{address}?{params}"
    data = await chrome_fetch(ws, url)
    if data.get('code') == 0:
        link = data.get('data', {}).get('link', {})
        result['twitter'] = link.get('twitter_username')
        result['website'] = link.get('website')
        result['description'] = link.get('description', '')  # 保存描述信息
    
    # 6. KOL 分析
    url = f"{GMGN_BASE}/vas/api/v1/token_holders/{chain}/{address}?{params}&limit=100&cost=20&tag=renowned&orderby=amount_percentage&direction=desc"
    kol_data = await chrome_fetch(ws, url)
    if kol_data.get('code') == 0:
        holders = kol_data.get('data', {}).get('list', [])
        # 过滤掉已清仓的 KOL (end_holding_at 不为 None 表示已清仓)
        active_holders = [h for h in holders if h.get('end_holding_at') is None]
        if active_holders:
            result['kol_holders'] = active_holders[:5]  # 取前5个显示
            result['kol_total'] = len(active_holders)  # 保存总数
    
    # 7. 开发者分析 - 通过持有者列表获取 dev 标签的地址
    url = f"{GMGN_BASE}/vas/api/v1/token_holders/{chain}/{address}?{params}&limit=10&tag=dev&orderby=amount_percentage&direction=desc"
    dev_data = await chrome_fetch(ws, url)
    if dev_data.get('code') == 0:
        dev_list = dev_data.get('data', {}).get('list', [])
        if dev_list:
            dev = dev_list[0]  # 取第一个 dev
            result['dev_address'] = dev.get('address')
            result['dev_profit'] = dev.get('profit', 0)
            result['dev_realized_pnl'] = dev.get('realized_pnl', 0)
            result['dev_name'] = dev.get('name') or dev.get('twitter_username')
            result['dev_twitter'] = dev.get('twitter_username')
            
            # 查询该开发者创建的其他代币
            dev_addr = dev.get('address')
            if dev_addr:
                dev_tokens_url = f"{GMGN_BASE}/api/v1/dev_created_tokens/{chain}/{dev_addr}?{params}"
                dev_tokens_data = await chrome_fetch(ws, dev_tokens_url)
                if dev_tokens_data.get('code') == 0:
                    tokens_info = dev_tokens_data.get('data', {})
                    all_tokens = tokens_info.get('tokens', [])
                    result['dev_total_tokens'] = len(all_tokens)
                
                # 筛选市值大于 1M 的代币
                big_tokens = []
                for token in all_tokens:
                    mc = token.get('market_cap', 0)
                    if mc:
                        try:
                            mc = float(mc)
                            if mc > 1000000:  # 大于 1M
                                big_tokens.append({
                                    'name': token.get('symbol'),  # 使用 symbol 作为名称
                                    'symbol': token.get('symbol'),
                                    'address': token.get('token_address'),  # 使用 token_address
                                    'market_cap': mc
                                })
                        except (ValueError, TypeError):
                            continue
                
                if big_tokens:
                    # 按市值排序，取前5个
                    big_tokens.sort(key=lambda x: x['market_cap'], reverse=True)
                    result['dev_big_tokens'] = big_tokens[:5]
    
    # ========== 额外数据采集：用于AI分析 ==========
    
    # 获取交易记录（最近50条）
    url = f"{GMGN_BASE}/vas/api/v1/token_trades/{chain}/{address}?{params}&limit=50"
    trades_data = await chrome_fetch(ws, url)
    if trades_data.get('code') == 0:
        result['trades'] = trades_data.get('data', {}).get('history', [])
    
    # 获取持有者详细列表（前100个）
    url = f"{GMGN_BASE}/vas/api/v1/token_holders/{chain}/{address}?{params}&limit=100&orderby=amount_percentage&direction=desc"
    holders_data = await chrome_fetch(ws, url)
    if holders_data.get('code') == 0:
        result['holders_detail'] = holders_data.get('data', {}).get('list', [])
    
    # 获取开发者推特数据（使用 bird CLI）
    twitter_username = result.get('twitter')
    if twitter_username:
        twitter_data = fetch_twitter_data_bird(twitter_username)
        if twitter_data:
            result['twitter_data'] = twitter_data
    
    return result

def calculate_score(token):
    score = 5
    risks = []
    
    mc = token.get('market_cap', 0) or 0
    liq = token.get('liquidity', 0) or 0
    holders = token.get('holder_count', 0) or 0
    top10 = token.get('top_10_holder_rate', 0) or 0
    buy_tax = float(token.get('buy_tax', 0) or 0)
    sell_tax = float(token.get('sell_tax', 0) or 0)
    
    if liq > 500000: score += 1
    elif liq < 20000:
        score -= 1
        risks.append("流动性偏低")
    
    if 100000 < mc < 2000000: score += 1
    elif mc > 5000000: score -= 1
    
    if holders > 5000: score += 1
    elif holders < 200:
        score -= 1
        risks.append("持有者较少")
    
    if top10 > 0.5:
        score -= 1
        risks.append(f"Top10集中度{top10*100:.1f}%")
    
    if buy_tax > 5 or sell_tax > 5:
        score -= 1
        risks.append(f"税率偏高(买{buy_tax}%/卖{sell_tax}%)")
    
    if token.get('is_honeypot'):
        score -= 2
        risks.append("⚠️ 蜜罐风险")
    
    score = max(1, min(10, score))
    return score, risks

def format_message(token, chain, address):
    score, risks = calculate_score(token)
    
    # 计算创建时间
    import time
    created_at = token.get('created_at', 0)
    if created_at:
        age_seconds = int(time.time() - created_at)
        if age_seconds < 3600:
            age_str = f"{age_seconds // 60} 分钟前"
        elif age_seconds < 86400:
            age_str = f"{age_seconds // 3600} 小时前"
        else:
            age_str = f"{age_seconds // 86400} 天前"
    else:
        age_str = "未知"
    
    # 计算交易量占市值比例
    vol_mc_ratio = 0
    if token.get('volume_24h') and token.get('market_cap'):
        vol_mc_ratio = (token['volume_24h'] / token['market_cap']) * 100
    
    # 风险等级和建议
    if score >= 7:
        risk_level = "🟢 Low"
        action = "✅ 可以考虑"
    elif score >= 5:
        risk_level = "🟡 Medium"
        action = "👀 可以关注"
    else:
        risk_level = "🔴 High"
        action = "⚠️ 谨慎观望"
    
    # Conviction 评分（基于流动性和持有者）
    conviction = 5
    liq = token.get('liquidity', 0) or 0
    holders = token.get('holder_count', 0) or 0
    if liq > 100000 and holders > 1000:
        conviction = 7
    elif liq > 50000 and holders > 500:
        conviction = 6
    elif liq < 10000 or holders < 100:
        conviction = 4
    
    # 获取涨跌幅
    change_24h = token.get('change_24h', 0) or 0
    change_1h = token.get('change_1h', 0) or 0
    
    # 构建消息
    msg = f"🔔 代币分析 | {chain.upper()}\n\n"
    msg += f"{token.get('name', 'Unknown')} (${token.get('symbol', 'N/A')}) | {chain.upper()}\n\n"
    msg += f"CA: {address}\n"
    msg += f"| 指标 | 数值 |\n"
    msg += f"| ---------- | ----------------- |\n"
    msg += f"| 💰 价格 | {fmt_price(token.get('price'))} |\n"
    msg += f"| 📊 市值 | {fmt_num(token.get('market_cap'))} |\n"
    msg += f"| 💧 流动性 | {fmt_num(token.get('liquidity'))} |\n"
    
    # 涨跌幅
    change_5m = token.get('change_5m')
    if change_5m is not None:
        msg += f"| ⚡ 5m | {'+' if change_5m >= 0 else ''}{change_5m:.2f}% |\n"
    
    change_1h = token.get('change_1h')
    if change_1h is not None:
        msg += f"| ⏱️ 1h | {'+' if change_1h >= 0 else ''}{change_1h:.2f}% |\n"
    
    change_24h = token.get('change_24h')
    if change_24h is not None:
        msg += f"| 📈 24h | {'+' if change_24h >= 0 else ''}{change_24h:.2f}% |\n"
    
    msg += f"| 👥 Holders | {token.get('holder_count', 'N/A')} |\n"
    msg += f"| 📦 24h Vol | {fmt_num(token.get('volume_24h'))} ({vol_mc_ratio:.0f}% of MC) |\n"
    
    msg += f"\n• Early Score: {score}/10\n"
    msg += f"• Conviction: {conviction}/10\n"
    msg += f"• Risk: {risk_level}\n"
    msg += f"• Action: {action}\n"
    
    # Why Alpha 分析
    why_alpha = generate_why_alpha(token, chain, age_str, change_24h, change_1h)
    msg += f"• Why Alpha: {why_alpha}\n"
    
    # Narrative Vibe
    narrative = generate_narrative(token, chain)
    msg += f"• Narrative Vibe: {narrative}\n"
    
    # KOL 信息
    if token.get('kol_holders'):
        kol_total = token.get('kol_total', len(token['kol_holders']))
        kol_info = format_kol_info(token['kol_holders'])
        if kol_info:
            msg += f"• 🎯 已上车KOL: {kol_info} (共{kol_total}个)\n"
    
    # 开发者信息
    if token.get('dev_address'):
        dev_info = format_dev_info(token)
        if dev_info:
            msg += f"• 👨‍💻 开发者: {dev_info}\n"
        
        # 显示开发者的大市值代币
        big_tokens = token.get('dev_big_tokens', [])
        if big_tokens:
            # 过滤掉当前代币
            current_addr = address.lower()
            other_tokens = [t for t in big_tokens if t.get('address') and t.get('address').lower() != current_addr]
            if other_tokens:
                msg += f"• 💎 历史成功项目: {format_big_tokens(other_tokens)}\n"
    
    # 风险提示
    if risks:
        risk_detail = generate_risk_detail(token, risks)
        msg += f"• ⚠️ 风险提示: {risk_detail}\n"
    
    # AI 智能分析
    msg += "\n"
    
    # 1. 代币叙事分析
    narrative_analysis = generate_narrative_analysis(token, chain)
    if narrative_analysis:
        msg += f"📖 代币叙事分析：{narrative_analysis}\n\n"
    
    # 2. 筹码分布分析
    chip_analysis = generate_chip_analysis(token)
    if chip_analysis:
        msg += f"💰 筹码分布分析：{chip_analysis}\n\n"
    
    # 3. 老鼠仓分析
    insider_analysis = generate_insider_analysis(token)
    if insider_analysis:
        msg += f"🐀 老鼠仓分析：{insider_analysis}\n"
    
    # 4. AI 机器人分析
    ai_bot_analysis = generate_ai_bot_analysis(token)
    if ai_bot_analysis:
        msg += f"\n{ai_bot_analysis}\n"
    
    # 链接信息
    links = []
    if token.get('twitter'):
        twitter = token['twitter']
        if not twitter.startswith('http'):
            twitter = f"https://x.com/{twitter}"
        links.append(f"🐦 [Twitter]({twitter})")
    if token.get('website'):
        links.append(f"🌐 [Website]({token['website']})")
    links.append(f"🔗 [GMGN](https://gmgn.ai/{chain}/token/{address})")
    
    if links:
        msg += f"\n{' | '.join(links)}"
    
    return msg

def generate_why_alpha(token, chain, age_str, change_24h, change_1h):
    """生成 Why Alpha 分析"""
    name = token.get('name', '该代币')
    mc = token.get('market_cap', 0) or 0
    liq = token.get('liquidity', 0) or 0
    vol = token.get('volume_24h', 0) or 0
    holders = token.get('holder_count', 0) or 0
    
    analysis = f"这支名为\"{name}\"的 {chain.upper()} 代币，创建 {age_str}，"
    
    if change_24h is not None and change_24h != 0:
        if change_24h > 0:
            analysis += f"24小时内上涨 {change_24h:.2f}%，"
        else:
            analysis += f"24小时内下跌 {abs(change_24h):.2f}%，"
    
    if change_1h is not None and change_1h != 0:
        if change_1h > 0:
            analysis += f"1小时内上涨 {change_1h:.2f}%。"
        else:
            analysis += f"1小时内下跌 {abs(change_1h):.2f}%。"
    
    analysis += f"当前市值约为 {fmt_num(mc)}，"
    
    if liq < 10000:
        analysis += f"但流动性极低，仅为 {fmt_num(liq)}。"
    elif liq < 50000:
        analysis += f"流动性为 {fmt_num(liq)}。"
    else:
        analysis += f"流动性较好，为 {fmt_num(liq)}。"
    
    if vol > 0 and mc > 0:
        vol_ratio = (vol / mc) * 100
        if vol_ratio < 10:
            analysis += f"24小时交易量为 {fmt_num(vol)}，仅占市值的 {vol_ratio:.0f}%，表明交易活跃度较低。"
        else:
            analysis += f"24小时交易量为 {fmt_num(vol)}，占市值的 {vol_ratio:.0f}%，交易较为活跃。"
    
    analysis += f"持有者数量为 {holders} 人。"
    
    return analysis

def generate_narrative(token, chain):
    """生成 Narrative Vibe"""
    narratives = [f"{chain.upper()} 生态"]
    
    name = token.get('name', '').lower()
    symbol = token.get('symbol', '').lower()
    
    # 根据名称判断叙事
    if any(x in name or x in symbol for x in ['dog', 'cat', 'pepe', 'frog', '狗', '猫', '青蛙']):
        narratives.append("动物币")
    elif any(x in name or x in symbol for x in ['trump', 'biden', 'musk', 'cz']):
        narratives.append("名人币")
    elif any(x in name or x in symbol for x in ['ai', 'gpt', 'bot']):
        narratives.append("AI概念")
    elif any(x in name or x in symbol for x in ['game', 'play', '游戏']):
        narratives.append("游戏")
    elif any(x in name or x in symbol for x in ['rip', 'memorial', '纪念']):
        narratives.append("纪念代币")
    else:
        narratives.append("MEME币")
    
    return ", ".join(narratives)

def generate_risk_detail(token, risks):
    """生成详细风险提示"""
    liq = token.get('liquidity', 0) or 0
    
    if liq < 10000:
        return "流动性极低，滑点巨大。这意味着少量交易就会引起价格剧烈波动，存在较高的操作风险，请务必谨慎。"
    elif liq < 50000:
        return "流动性偏低，存在一定滑点风险。建议小额测试后再进行大额交易。"
    elif "持有者较少" in " ".join(risks):
        return "持有者数量较少，筹码可能集中在少数地址，存在砸盘风险。"
    elif "Top10集中度" in " ".join(risks):
        return "Top10持仓集中度较高，大户可能随时抛售，需警惕价格波动。"
    else:
        return "请注意市场风险，做好止损准备。"

def generate_narrative_analysis(token, chain):
    """代币叙事分析 - 基于描述和交易热度"""
    description = token.get('description', '')
    name = token.get('name', '')
    
    # 如果有描述，优先使用描述分析叙事
    if description:
        analysis = f"{description}"
    else:
        # 没有描述时，基于名称推测叙事
        name_lower = name.lower()
        if any(x in name_lower for x in ['ai', 'agent', 'gpt', 'bot']):
            analysis = f"{name} 是一个AI概念代币。"
        elif any(x in name_lower for x in ['trump', 'musk', 'cz']):
            analysis = f"{name} 是一个名人相关代币。"
        else:
            analysis = f"{name} 的具体叙事信息暂未公开。"
    
    # 补充交易热度判断
    trades = token.get('trades', [])
    if trades:
        buy_count = len([t for t in trades if t.get('event') == 'buy'])
        sell_count = len([t for t in trades if t.get('event') == 'sell'])
        
        if buy_count > sell_count * 1.5:
            analysis += " 当前买盘强劲，叙事热度上升。"
        elif sell_count > buy_count * 1.5:
            analysis += " 当前卖压较大，叙事热度下降。"
    
    return analysis

def generate_chip_analysis(token):
    """筹码分布分析 - 基于持有者详细数据"""
    holders_detail = token.get('holders_detail', [])
    top10_rate = token.get('top_10_holder_rate', 0)
    
    if not holders_detail:
        return f"Top10持仓占比{top10_rate*100:.1f}%，详细持仓数据不足。"
    
    # 分析前10大持有者
    top10 = holders_detail[:10]
    
    # 统计盈利/亏损情况
    profit_holders = [h for h in top10 if h.get('unrealized_profit', 0) > 0]
    loss_holders = [h for h in top10 if h.get('unrealized_profit', 0) < 0]
    
    # 统计标签
    pool_holders = [h for h in top10 if 'pool' in h.get('tags', [])]
    cex_holders = [h for h in top10 if h.get('addr_type') == 2]
    
    analysis = f"Top10持仓{top10_rate*100:.1f}%，其中{len(profit_holders)}个盈利、{len(loss_holders)}个亏损。"
    
    if len(pool_holders) > 0:
        analysis += f"包含{len(pool_holders)}个流动性池。"
    if len(cex_holders) > 0:
        analysis += f"有{len(cex_holders)}个CEX地址。"
    
    if top10_rate > 0.6:
        analysis += "筹码高度集中，控盘风险极高。"
    elif len(profit_holders) > 7:
        analysis += "大部分大户盈利，存在获利了结压力。"
    elif len(loss_holders) > 7:
        analysis += "大部分大户被套，可能死扛或割肉。"
    
    return analysis

def generate_insider_analysis(token):
    """老鼠仓分析 - 基于早期交易和持仓数据"""
    trades = token.get('trades', [])
    holders_detail = token.get('holders_detail', [])
    
    if not trades:
        return "交易数据不足，无法分析老鼠仓行为。"
    
    # 分析早期买入者（交易记录中最早的买入）
    buy_trades = [t for t in trades if t.get('event') == 'buy']
    if not buy_trades:
        return "无买入记录，无法分析。"
    
    # 按时间排序，找出最早的买入
    buy_trades_sorted = sorted(buy_trades, key=lambda x: x.get('timestamp', 0))
    early_buyers = buy_trades_sorted[:10]  # 前10笔买入
    
    # 统计早期买入者的标签
    early_tags = []
    for trade in early_buyers:
        tags = trade.get('maker_tags', [])
        early_tags.extend(tags)
    
    # 检查是否有sniper、bundler等标签
    sniper_count = sum(1 for tag in early_tags if 'sniper' in str(tag).lower())
    bundler_count = sum(1 for tag in early_tags if 'bundler' in str(tag).lower())
    
    analysis = f"前10笔买入中，发现{sniper_count}个sniper、{bundler_count}个bundler。"
    
    if sniper_count > 3:
        analysis += "⚠️ 大量sniper提前埋伏，存在内幕交易嫌疑。"
    elif bundler_count > 3:
        analysis += "⚠️ 多个bundler参与，可能存在自买自卖行为。"
    else:
        analysis += "早期买入者相对正常，未发现明显老鼠仓迹象。"
    
    return analysis

def generate_ai_bot_analysis(token):
    """🤖 AI 机器人分析 - 基于推特数据深度分析"""
    twitter_data = token.get('twitter_data')
    if not twitter_data:
        return None
    
    username = twitter_data.get('username', '')
    followers = twitter_data.get('followers', 0)
    bio = twitter_data.get('bio', '')
    location = twitter_data.get('location', '')
    tweets = twitter_data.get('tweets', [])
    
    # 身份判断
    if followers == 0 and (not bio or len(bio) < 10):
        identity = "骗子/恶意部署者"
        risk = "🔴 高"
    elif followers < 100:
        identity = "可疑小号"
        risk = "🟡 中"
    else:
        identity = "正常账号"
        risk = "🟢 低"
    
    # 分析推文内容
    rug_signals = []
    for tweet in tweets[:5]:
        text = tweet.get('text', '').lower()
        if 'rug' in text or 'scam' in text:
            rug_signals.append("明牌作恶")
        if 'dev wallet' in text or 'insta sell' in text:
            rug_signals.append("提及立即抛售")
    
    analysis = f"🤖 AI 分析 · @{username}\n\n"
    analysis += f"身份：{identity}\n"
    analysis += f"风险：{risk}\n"
    analysis += f"账号：{location or '未知'}，{followers} 粉丝\n\n"
    
    if rug_signals:
        analysis += f"💬 发现风险信号：{', '.join(set(rug_signals))}\n\n"
    
    analysis += f"📝 推文：共 {len(tweets)} 条推文"
    if bio:
        analysis += f"，Bio: {bio[:50]}..."
    
    return analysis

def format_kol_info(kol_holders):
    """格式化 KOL 信息"""
    if not kol_holders or not isinstance(kol_holders, list):
        return None
    
    kols = []
    for holder in kol_holders[:3]:  # 最多显示3个
        name = holder.get('name') or holder.get('twitter_username')
        tag = holder.get('wallet_tag_v2', '')
        
        if name:
            if tag:
                kols.append(f"{name}({tag})")
            else:
                kols.append(name)
        elif tag:
            # 如果没有名字，显示标签
            kols.append(tag)
    
    return ", ".join(kols) if kols else None

def format_dev_info(token):
    """格式化开发者信息"""
    dev_addr = token.get('dev_address', '')
    dev_name = token.get('dev_name', '')
    dev_twitter = token.get('dev_twitter', '')
    total_tokens = token.get('dev_total_tokens', 0)
    profit = token.get('dev_profit', 0)
    pnl = token.get('dev_realized_pnl', 0)
    
    if not dev_addr:
        return None
    
    # 缩短地址显示
    short_addr = f"{dev_addr[:6]}...{dev_addr[-4:]}"
    
    info_parts = []
    
    # 开发者名称或地址
    if dev_name:
        info_parts.append(f"{dev_name} ({short_addr})")
    elif dev_twitter:
        info_parts.append(f"@{dev_twitter} ({short_addr})")
    else:
        info_parts.append(short_addr)
    
    if total_tokens > 0:
        info_parts.append(f"发币{total_tokens}个")
    
    if profit != 0:
        if profit > 0:
            info_parts.append(f"本币盈利{fmt_num(profit)}")
        else:
            info_parts.append(f"本币亏损{fmt_num(abs(profit))}")
    
    if pnl != 0 and pnl is not None:
        info_parts.append(f"PNL {pnl:.1f}x")
    
    return " | ".join(info_parts)

def format_big_tokens(big_tokens):
    """格式化大市值代币列表"""
    if not big_tokens:
        return None
    
    tokens_str = []
    for token in big_tokens:
        name = token.get('name', 'Unknown')
        symbol = token.get('symbol', '')
        mc = token.get('market_cap', 0)
        addr = token.get('address', '')
        
        # 缩短地址
        short_addr = f"{addr[:6]}...{addr[-4:]}" if addr else ''
        
        # 格式：名称(符号) 市值 地址
        token_info = f"{name}"
        if symbol:
            token_info += f"(${symbol})"
        token_info += f" {fmt_num(mc)}"
        if short_addr:
            token_info += f" {short_addr}"
        
        tokens_str.append(token_info)
    
    return ", ".join(tokens_str)

async def main():
    if len(sys.argv) < 2:
        print("Usage: token_query_v2.py <address> [chain]")
        print("       token_query_v2.py <chain> <address>")
        sys.exit(1)
    
    # 自动识别链
    if len(sys.argv) == 2:
        address = sys.argv[1].strip()
        # 根据地址格式判断链
        if address.startswith('0x') and len(address) == 42:
            # EVM 链：BSC 优先（更常用）
            chains = ['bsc', 'base']
        else:
            # Solana 地址
            chains = ['sol']
    else:
        chain = sys.argv[1].strip().lower()
        address = sys.argv[2].strip()
        chains = [chain]
    
    page_id = await get_page_id()
    if not page_id:
        print("❌ 无法连接到 Chrome DevTools")
        sys.exit(1)
    
    ws_url = f"{CHROME_WS_BASE}/devtools/page/{page_id}"
    
    async with websockets.connect(ws_url) as ws:
        for chain in chains:
            token = await fetch_token_data(ws, chain, address)
            
            if token.get('name'):
                message = format_message(token, chain, address)
                print(message)
                return
        
        print("❌ 未找到代币数据")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
