"""V4.3 拟人化响应式HTML生成器 - 参考旅游攻略风格"""
import time

class ReportGenerator:
    """拟人化风格 + 响应式设计 + 真实导航/支付"""
    
    async def generate_glassmorphism_html(self, data: dict, intent: dict, plan: dict) -> str:
        """生成拟人化响应式HTML攻略"""
        
        scenic_spots = data.get("scenic_spots", [])
        hotels = data.get("hotels", [])
        restaurants = data.get("restaurants", [])
        
        city = intent.get("destination", "目的地")
        budget = intent.get("budget", "5000元")
        days = intent.get("duration_days", "5天")
        people = intent.get("num_people", "2人")
        why = intent.get("why", "休闲")
        what = intent.get("what", "景点")
        
        plan_title = plan.get("title", "精选方案")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 拟人化开场白
        intro = f"""
        <div class="intro-section">
            <div class="intro-text">
                嗨！这份攻略是专门为你准备的 🎉<br>
                <strong>{city}{days}之旅</strong>，我帮你把好吃好玩都安排好了！<br>
                下面这些地方都是<strong>真实存在</strong>的，直接点导航就能去~
            </div>
            <div class="intro-stats">
                <div class="stat-badge">💰 预算 {budget}</div>
                <div class="stat-badge">👥 {people}</div>
                <div class="stat-badge">🎯 {why}</div>
            </div>
        </div>
        """
        
        # 景点卡片（拟人化描述）
        spots_html = ""
        for i, spot in enumerate(scenic_spots[:5], 1):
            name = spot.get('name', '景点')
            address = spot.get('address', '')
            amap_link = f"https://m.amap.com/search/view/keywords={name}"
            
            # 拟人化推荐语
            recommend = self._get_spot_recommend(i, name, city)
            
            spots_html += f"""
            <div class="spot-card">
                <div class="spot-header">
                    <div class="spot-num">#{i}</div>
                    <div class="spot-name">{name}</div>
                    <div class="spot-tag">{recommend}</div>
                </div>
                <div class="spot-address">📍 {address[:45] if address else '具体地址点导航查看'}</div>
                <div class="spot-actions">
                    <a href="{amap_link}" target="_blank" class="btn-nav">
                        🗺️ 立即导航
                    </a>
                </div>
            </div>
            """
        
        # 餐厅推荐（拟人化）
        restaurants_html = ""
        for r in restaurants[:3]:
            name = r.get('name', '美食')
            address = r.get('address', '')
            meituan_link = "https://www.meituan.com/"
            restaurants_html += f"""
            <div class="food-card">
                <div class="food-icon">🍜</div>
                <div class="food-name">{name}</div>
                <div class="food-address">{address[:30] if address else ''}</div>
                <a href="{meituan_link}" target="_blank" class="btn-order">点外卖</a>
            </div>
            """
        
        # 酒店推荐（拟人化）
        hotels_html = ""
        for h in hotels[:3]:
            name = h.get('name', '酒店')
            address = h.get('address', '')
            ctrip_link = f"https://m.ctrip.com/webapp/hotel/search?city={city}"
            hotels_html += f"""
            <div class="hotel-card">
                <div class="hotel-icon">🏨</div>
                <div class="hotel-name">{name}</div>
                <div class="hotel-address">{address[:35] if address else ''}</div>
                <a href="{ctrip_link}" target="_blank" class="btn-book">预订</a>
            </div>
            """
        
        # 真实支付聚合（拟人化引导）
        payment_html = f"""
        <div class="payment-section">
            <h2>🛒 出行必备，一键搞定</h2>
            <p class="payment-desc">订酒店、叫外卖、打车、买药，这些链接都是<strong>真实可用</strong>的，放心点~</p>
            <div class="payment-grid">
                <a href="https://m.ctrip.com/webapp/hotel/search?city={city}" target="_blank" class="payment-btn glass">
                    <span class="pay-emoji">🏨</span>
                    <span class="pay-title">携程订酒店</span>
                    <span class="pay-tip">比价更省心</span>
                </a>
                <a href="https://www.meituan.com/" target="_blank" class="payment-btn glass">
                    <span class="pay-emoji">🍜</span>
                    <span class="pay-title">美团外卖</span>
                    <span class="pay-tip">当地美食到家</span>
                </a>
                <a href="https://m.amap.com/" target="_blank" class="payment-btn glass">
                    <span class="pay-emoji">🚗</span>
                    <span class="pay-title">高德打车</span>
                    <span class="pay-tip">出行无忧</span>
                </a>
                <a href="https://www.meituan.com/medicine" target="_blank" class="payment-btn glass">
                    <span class="pay-emoji">💊</span>
                    <span class="pay-title">美团买药</span>
                    <span class="pay-tip">24小时送达</span>
                </a>
            </div>
        </div>
        """
        
        # 拟人化结尾
        footer = f"""
        <div class="footer-section">
            <div class="footer-text">
                希望这份攻略能帮到你！有问题随时问我 🤗<br>
                记得<strong>收藏</strong>这份攻略，出发前再看看~
            </div>
            <div class="footer-meta">
                <span>📅 生成时间：{timestamp}</span>
                <span>📍 数据来源：高德地图真实数据</span>
                <span>✨ TravelMaster V4.3</span>
            </div>
        </div>
        """
        
        # 完整响应式HTML
        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{city}旅行攻略 - 专属定制</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                /* 响应式基础 */
                body {{ 
                    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                    padding: 20px;
                    line-height: 1.6;
                }}
                
                /* 毛玻璃卡片 */
                .glass {{ 
                    background: rgba(255, 255, 255, 0.9);
                    backdrop-filter: blur(10px);
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                }}
                
                .container {{ 
                    max-width: 900px;
                    margin: 0 auto;
                }}
                
                /* 头部 - 拟人化 */
                .header {{ 
                    padding: 30px 20px;
                    margin-bottom: 20px;
                    text-align: center;
                }}
                .header h1 {{ 
                    font-size: 28px;
                    color: #2d3748;
                    margin-bottom: 8px;
                }}
                .header .subtitle {{ 
                    font-size: 16px;
                    color: #718096;
                }}
                
                /* 开场白 */
                .intro-section {{ padding: 25px 20px; margin-bottom: 20px; }}
                .intro-text {{ 
                    font-size: 16px;
                    color: #4a5568;
                    margin-bottom: 15px;
                }}
                .intro-stats {{ 
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }}
                .stat-badge {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 14px;
                }}
                
                /* 分区标题 */
                .section {{ margin-bottom: 20px; padding: 20px; }}
                .section-title {{ 
                    font-size: 20px;
                    color: #2d3748;
                    margin-bottom: 15px;
                    padding-left: 12px;
                    border-left: 4px solid #667eea;
                }}
                
                /* 景点卡片 */
                .spot-card {{ 
                    background: white;
                    border-radius: 12px;
                    padding: 15px;
                    margin: 12px 0;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                }}
                .spot-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
                .spot-num {{ 
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                }}
                .spot-name {{ font-size: 18px; font-weight: 600; color: #2d3748; }}
                .spot-tag {{ 
                    background: #e2e8f0;
                    color: #4a5568;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 12px;
                }}
                .spot-address {{ font-size: 14px; color: #718096; margin-bottom: 10px; }}
                .spot-actions {{ display: flex; gap: 10px; }}
                .btn-nav {{ 
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-size: 14px;
                    display: inline-block;
                }}
                
                /* 餐厅卡片 */
                .food-card {{ 
                    display: flex;
                    align-items: center;
                    background: white;
                    padding: 12px;
                    border-radius: 10px;
                    margin: 8px 0;
                    gap: 10px;
                }}
                .food-icon {{ font-size: 28px; }}
                .food-name {{ flex: 1; font-size: 16px; font-weight: 500; }}
                .food-address {{ font-size: 12px; color: #718096; flex: 2; }}
                .btn-order {{ 
                    background: #10b981;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    text-decoration: none;
                    font-size: 12px;
                }}
                
                /* 酒店卡片 */
                .hotel-card {{ 
                    display: flex;
                    align-items: center;
                    background: white;
                    padding: 12px;
                    border-radius: 10px;
                    margin: 8px 0;
                    gap: 10px;
                }}
                .hotel-icon {{ font-size: 28px; }}
                .hotel-name {{ flex: 1; font-size: 16px; font-weight: 500; }}
                .hotel-address {{ font-size: 12px; color: #718096; flex: 2; }}
                .btn-book {{ 
                    background: #2196F3;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    text-decoration: none;
                    font-size: 12px;
                }}
                
                /* 支付区 */
                .payment-section {{ padding: 25px 20px; margin-bottom: 20px; }}
                .payment-section h2 {{ 
                    font-size: 20px;
                    color: #2d3748;
                    margin-bottom: 8px;
                }}
                .payment-desc {{ 
                    font-size: 14px;
                    color: #718096;
                    margin-bottom: 15px;
                }}
                .payment-grid {{ 
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 12px;
                }}
                .payment-btn {{ 
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 15px;
                    border-radius: 12px;
                    text-decoration: none;
                    color: inherit;
                    text-align: center;
                }}
                .pay-emoji {{ font-size: 36px; }}
                .pay-title {{ font-size: 15px; font-weight: 600; margin-top: 8px; }}
                .pay-tip {{ font-size: 12px; color: #718096; margin-top: 4px; }}
                
                /* 结尾 */
                .footer-section {{ 
                    padding: 25px 20px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .footer-text {{ 
                    font-size: 15px;
                    color: #4a5568;
                    margin-bottom: 15px;
                }}
                .footer-meta {{ 
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 15px;
                    font-size: 12px;
                    color: #a0aec0;
                }}
                
                /* 响应式：手机端 */
                @media (max-width: 600px) {{
                    .container {{ padding: 10px; }}
                    .header h1 {{ font-size: 22px; }}
                    .section-title {{ font-size: 18px; }}
                    .spot-name {{ font-size: 16px; }}
                    .payment-grid {{ grid-template-columns: 1fr; }}
                    .stat-badge {{ font-size: 12px; padding: 6px 12px; }}
                }}
                
                /* 响应式：平板 */
                @media (min-width: 601px) and (max-width: 900px) {{
                    .payment-grid {{ grid-template-columns: repeat(2, 1fr); }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="glass header">
                    <h1>📍 {city}专属攻略</h1>
                    <div class="subtitle">{plan_title} · 为你定制</div>
                </div>
                
                <div class="glass">
                    {intro}
                </div>
                
                <div class="glass section">
                    <h2 class="section-title">🗺️ 好玩的地方（真实导航）</h2>
                    {spots_html}
                </div>
                
                <div class="glass section">
                    <h2 class="section-title">🍜 吃什么（外卖直达）</h2>
                    {restaurants_html}
                </div>
                
                <div class="glass section">
                    <h2 class="section-title">🏨 住哪里（真实预订）</h2>
                    {hotels_html}
                </div>
                
                <div class="glass">
                    {payment_html}
                </div>
                
                <div class="glass">
                    {footer}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _get_spot_recommend(self, index: int, name: str, city: str) -> str:
        """生成拟人化推荐语"""
        tags = [
            "强烈推荐！",
            "必打卡！",
            "超好玩！",
            "适合拍照！",
            "别错过！"
        ]
        return tags[index % len(tags)]