from typing import Dict, List, Optional, Any
import time
import json
from xianyu_api_client_skill import XianYuAPIClient

# Batch operation safety limits
MAX_BATCH_SIZE = 20  # Maximum products per batch

class XianYuProductManager:
    """闲鱼商品管理器

    安全设计原则：
    1. create_product() 默认需要用户确认
    2. create_product_unsafe() 供自动化脚本使用（跳过确认）
    3. 批量操作有硬性上限限制
    """

    def __init__(self, api_client: Optional[XianYuAPIClient] = None):
        """
        初始化商品管理器

        Args:
            api_client: API客户端实例，如果为None则自动创建
        """
        self.api_client = api_client or XianYuAPIClient()

        # AI服务商品模板库
        self.templates = {
            'basic': {
                'price': 29900,
                'original_price': 39900,
                'title': 'AI客服Agent 自动回复省70%人力 电商/服务业专用',
                'content': self._get_basic_description()
            },
            'standard': {
                'price': 69900,
                'original_price': 89900,
                'title': 'AI数据分析Agent 自动生成爆款选题 内容创作者必备',
                'content': self._get_standard_description()
            },
            'premium': {
                'price': 150000,
                'original_price': 199000,
                'title': 'AI工作流定制 企业级多平台集成 复杂业务自动化',
                'content': self._get_premium_description()
            }
        }

        # 使用用户提供的分类ID
        self.channel_cat_id = "2e6dedc88ae9177ab108d382c4e6ea42"

    def _get_basic_description(self) -> str:
        """基础版服务描述 - 优化结构"""
        return """【服务内容】
• 训练专属AI客服Agent，自动回答常见问题
• 接入店铺商品数据（尺码表、库存、物流信息）
• 支持微信/淘宝/闲鱼多平台集成
• 3天内交付，提供完整使用文档和培训

【真实案例】
上周帮一个淘宝女装店主做了个AI客服Agent，效果超出预期！

客户痛点：
- 每天咨询量200+，人工客服忙不过来
- 大量重复问题：尺码、发货、退换货
- 晚上和周末没人值班，流失客户

我的解决方案：
✅ 训练专属AI客服Agent
✅ 接入店铺商品数据（尺码表、库存、物流）
✅ 自动回答常见问题 + 转人工复杂问题
✅ 支持微信/淘宝多平台

【实际效果】
📈 人工客服工作量减少70%
📈 夜间咨询回复率从0%提升到95%
📈 客户满意度提升，差评减少
💰 投入299元，一个月省下3000+人工成本

【常见问题】
Q: 需要什么技术基础吗？
A: 完全不需要！我们会提供完整的使用培训和文档。

Q: 效果不好怎么办？
A: 100%满意保证，不满意可退款，支持支付宝担保交易。

Q: 后续维护怎么收费？
A: 30天免费维护，后续按需提供付费支持服务。

Q: 多久能交付？
A: 基础版3天，标准版5天，高级版7天内交付。"""

    def _get_standard_description(self) -> str:
        """标准版服务描述 - 优化结构"""
        return """【服务内容】
• 复杂业务流程自动化，多平台数据集成
• 钉钉+飞书+企业微信+微信数据打通
• 智能决策支持和数据分析
• 5天内交付，免费需求分析+使用培训

【真实案例】
帮一家电商公司做了多平台工作流自动化，彻底解决数据孤岛问题！

客户痛点：
- 四个平台数据分散，手动切换效率低下
- 重复录入工作占每天3小时
- 数据不一致导致决策错误

我的解决方案：
✅ 定制工作流自动化Agent
✅ 四平台数据实时同步
✅ 自动生成日报和关键指标
✅ 专属技术支持团队

【实际效果】
📈 日常工作效率提升80%
📈 数据准确性达到99.9%
📈 管理决策速度提升50%
💰 投入699元，年节省人力成本2万+

【常见问题】
Q: 支持哪些平台集成？
A: 钉钉、飞书、企业微信、微信、淘宝、小红书等主流平台。

Q: 数据安全如何保障？
A: 所有数据本地处理，不上传第三方服务器，符合企业安全要求。

Q: 可以定制特殊需求吗？
A: 当然可以！我们会根据您的具体业务流程定制开发。

Q: 交付后如何维护？
A: 30天免费维护，提供详细技术文档和视频教程。"""

    def _get_premium_description(self) -> str:
        """高级版服务描述 - 优化结构"""
        return """【服务内容】
• 企业级复杂业务逻辑定制开发
• 多系统深度集成和API对接
• 专属AI解决方案设计
• 7天内交付，一对一需求分析

【真实案例】
为一家连锁零售企业定制了完整的AI运营解决方案！

客户痛点：
- 50+门店数据无法统一管理
- 客户服务响应慢，满意度低
- 运营决策缺乏数据支撑

我的解决方案：
✅ 企业级AI运营Agent定制
✅ 50+门店数据统一管理平台
✅ 智能客服+数据分析+决策支持一体化
✅ 专属技术团队长期支持

【实际效果】
📈 客户服务响应时间缩短90%
📈 运营决策效率提升70%
📈 年度人力成本节省15万+
🏆 获得客户年度最佳技术合作伙伴奖

【常见问题】
Q: 适合多大规模的企业？
A: 适合中小型企业到大型企业，可根据规模定制方案。

Q: 实施周期多长？
A: 标准7天交付，复杂项目可分阶段实施。

Q: 后续升级和扩展？
A: 提供长期技术支持，可随时扩展新功能模块。

Q: 价格包含哪些服务？
A: 包含需求分析、开发、测试、培训、90天维护全套服务。"""

    def generate_product_data(self, service_type: str, price_tier: str,
                            custom_title: Optional[str] = None,
                            custom_content: Optional[str] = None,
                            image_config: Optional[Dict[str, Any]] = None,
                            user_name: Optional[str] = None) -> Dict[str, Any]:
        """
        生成商品数据

        Args:
            service_type: 服务类型（如 'workflow', 'chatbot', 'automation'）
            price_tier: 价格档次 ('basic', 'standard', 'premium')
            custom_title: 自定义标题（可选）
            custom_content: 自定义描述（可选）
            image_config: 图片配置字典，支持remote_urls字段
            user_name: 闲鱼账号（必需）

        Returns:
            商品数据字典
        """
        if price_tier not in self.templates:
            raise ValueError(f"Invalid price tier: {price_tier}")

        template = self.templates[price_tier]

        # 获取图片URL列表
        images = self.get_images_from_config(image_config or {})

        # 默认闲鱼账号
        actual_user_name = user_name or "xy137114666612"

        return {
            "item_biz_type": 2,
            "sp_biz_type": 1,
            "channel_cat_id": self.channel_cat_id,
            "price": template['price'],
            "original_price": template['original_price'],
            "express_fee": 0,
            "stock": 20,
            "outer_id": f"AI-{service_type.upper()}-{price_tier.upper()}-{int(time.time())}",
            "stuff_status": 100,
            "province_id": 110000,
            "city_id": 110100,
            "district_id": 110101,
            "publish_shop": [{
                "user_name": actual_user_name,
                "images": images,
                "title": custom_title or template['title'],
                "content": custom_content or template['content'],
                "service_support": "SDR"
            }]
        }

    def create_product(self, service_type: str, price_tier: str,
                      custom_title: Optional[str] = None,
                      custom_content: Optional[str] = None,
                      image_config: Optional[Dict[str, Any]] = None,
                      user_name: Optional[str] = None,
                      dry_run: bool = False) -> Dict[str, Any]:
        """
        创建单个商品（默认需要用户确认）

        Args:
            dry_run: 如果为True，只打印预览不实际创建
        """
        product_data = self.generate_product_data(
            service_type, price_tier, custom_title, custom_content, image_config, user_name
        )
        if dry_run:
            print(f"\n[Dry Run] 商品预览 - {service_type}/{price_tier}")
            print(json.dumps(product_data, indent=2, ensure_ascii=False))
            return {"code": 0, "msg": "dry_run", "data": product_data}
        return self.api_client.create_product(product_data)

    def create_product_unsafe(self, service_type: str, price_tier: str,
                             custom_title: Optional[str] = None,
                             custom_content: Optional[str] = None,
                             image_config: Optional[Dict[str, Any]] = None,
                             user_name: Optional[str] = None,
                             dry_run: bool = False) -> Dict[str, Any]:
        """
        创建单个商品（跳过确认，供自动化使用）

        警告：务必先用 dry_run=True 预览请求数据。
        """
        product_data = self.generate_product_data(
            service_type, price_tier, custom_title, custom_content, image_config, user_name
        )
        if dry_run:
            print(f"\n[Dry Run (unsafe)] 商品预览 - {service_type}/{price_tier}")
            print(json.dumps(product_data, indent=2, ensure_ascii=False))
            return {"code": 0, "msg": "dry_run", "data": product_data}
        return self.api_client.create_product_unsafe(product_data)

    def create_batch_products(self, service_types: List[str],
                             price_tiers: List[str],
                             image_config: Optional[Dict[str, Any]] = None,
                             user_name: Optional[str] = None,
                             dry_run: bool = False) -> List[Dict[str, Any]]:
        """
        批量创建商品（默认需要用户确认）

        Args:
            dry_run: 如果为True，只打印预览不实际创建
        """
        total = len(service_types) * len(price_tiers)
        if total > MAX_BATCH_SIZE:
            raise ValueError(f"Batch size {total} exceeds maximum of {MAX_BATCH_SIZE} products")

        if dry_run:
            print(f"\n[Dry Run] 批量创建预览（{total} 个商品）:")
            for st in service_types:
                for pt in price_tiers:
                    pd = self.generate_product_data(st, pt, image_config=image_config, user_name=user_name)
                    print(f"  - {st}/{pt}: title={pd['publish_shop'][0]['title']}, price={pd['price']/100:.2f}")
            return [{"code": 0, "msg": "dry_run", "count": total}]

        results = []
        for service_type in service_types:
            for price_tier in price_tiers:
                try:
                    result = self.create_product(service_type, price_tier, image_config=image_config, user_name=user_name)
                    results.append({
                        'service_type': service_type, 'price_tier': price_tier,
                        'success': True, 'result': result
                    })
                except Exception as e:
                    results.append({
                        'service_type': service_type, 'price_tier': price_tier,
                        'success': False, 'error': str(e)
                    })
        return results

    def create_batch_products_unsafe(self, service_types: List[str],
                                    price_tiers: List[str],
                                    image_config: Optional[Dict[str, Any]] = None,
                                    user_name: Optional[str] = None,
                                    dry_run: bool = False) -> List[Dict[str, Any]]:
        """
        批量创建商品（跳过确认，供自动化使用）
        """
        total = len(service_types) * len(price_tiers)
        if total > MAX_BATCH_SIZE:
            raise ValueError(f"Batch size {total} exceeds maximum of {MAX_BATCH_SIZE} products")

        if dry_run:
            print(f"\n[Dry Run (unsafe)] 批量创建预览（{total} 个商品）:")
            for st in service_types:
                for pt in price_tiers:
                    pd = self.generate_product_data(st, pt, image_config=image_config, user_name=user_name)
                    print(f"  - {st}/{pt}: title={pd['publish_shop'][0]['title']}, price={pd['price']/100:.2f}")
            return [{"code": 0, "msg": "dry_run", "count": total}]

        results = []
        for service_type in service_types:
            for price_tier in price_tiers:
                try:
                    result = self.create_product_unsafe(service_type, price_tier, image_config=image_config, user_name=user_name)
                    results.append({
                        'service_type': service_type, 'price_tier': price_tier,
                        'success': True, 'result': result
                    })
                except Exception as e:
                    results.append({
                        'service_type': service_type, 'price_tier': price_tier,
                        'success': False, 'error': str(e)
                    })
        return results

    def get_images_from_config(self, config: Dict[str, Any]) -> List[str]:
        """
        根据配置获取图片URL列表
        """
        images = []

        # 优先使用远程URL
        if config.get('remote_urls'):
            images.extend(config['remote_urls'])

        # 如果都没有，使用默认示例图片
        if not images:
            images = ["https://sc02.alicdn.com/kf/Ad9aeca17b83741918e6e13c5a8101a65j.png"]

        return images
