"""
Semantic Search Skill 使用示例

演示如何在不同场景下使用 skill
"""

import asyncio


# ==================== 示例 1: 在项目中使用（推荐） ====================

async def example_in_project():
    """在项目环境中使用 skill（自动使用项目配置）"""
    print("=== 示例 1: 在项目中使用 ===\n")
    
    # 直接导入，自动使用项目配置
    from src import SemanticSearchSkill
    
    # 不需要传配置，自动使用项目的 CONFIG
    skill = SemanticSearchSkill()
    
    # 表格检索
    result = await skill.invoke("table_search", {
        "query": "查找用户相关的表",
        "limit": 10
    })
    
    print(f"表格检索结果：{len(result['data'])} 条")
    print(f"第一条：{result['data'][0] if result['data'] else '无结果'}\n")


# ==================== 示例 2: 自定义配置 ====================

async def example_custom_config():
    """使用自定义配置"""
    print("=== 示例 2: 自定义配置 ===\n")
    
    from src import SemanticSearchSkill
    
    # 自定义配置
    custom_config = {
        "flight_db": {
            "host": "localhost",
            "port": 31337,
            "user": "admin",
            "password": "password"
        },
        "llm": {
            "model": "qwen3_30b",
            "api_key": "EMPTY",
            "base_url": "http://192.168.0.14:8867/v1"
        }
    }
    
    skill = SemanticSearchSkill(config=custom_config)
    
    # 字段检索
    result = await skill.invoke("field_search", {
        "query": "查找创建时间字段",
        "resource_id": 1,
        "limit": 5
    })
    
    print(f"字段检索结果：{result['data']}\n")


# ==================== 示例 3: 在 OpenClaw 中使用 ====================

async def example_in_openclaw():
    """在 OpenClaw 中使用"""
    print("=== 示例 3: 在 OpenClaw 中使用 ===\n")
    
    # 如果发布到 ClawHub
    # from openclaw import skill
    
    # result = await skill.invoke("semantic-search", {
    #     "action": "table_search",
    #     "query": "查找用户表",
    #     "limit": 10
    # })
    
    print("在 OpenClaw 中调用已发布的 skill")
    print("npx clawhub install semantic-search\n")


# ==================== 示例 4: 批量调用 ====================

async def example_batch_call():
    """批量并发调用"""
    print("=== 示例 4: 批量调用 ===\n")
    
    from src import SemanticSearchSkill
    
    skill = SemanticSearchSkill()
    
    # 并发执行多个查询
    tasks = [
        skill.invoke("table_search", {"query": "用户表", "limit": 5}),
        skill.invoke("table_search", {"query": "订单表", "limit": 5}),
        skill.invoke("table_search", {"query": "产品表", "limit": 5}),
    ]
    
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"查询 {i+1}: {len(result['data'])} 条结果")
    
    print()


# ==================== 示例 5: 在工作流中使用 ====================

async def example_in_workflow():
    """在 LangGraph 工作流中使用"""
    print("=== 示例 5: 在工作流中使用 ===\n")
    
    from src import SemanticSearchSkill
    
    skill = SemanticSearchSkill()
    
    # 模拟工作流中的一个节点
    async def search_node(state):
        """搜索节点"""
        query = state.get("query", "")
        
        # 表格检索
        tables = await skill.invoke("table_search", {
            "query": query,
            "limit": 3
        })
        
        # 字段检索
        if tables["data"]:
            fields = await skill.invoke("field_search", {
                "query": "时间字段",
                "resource_id": tables["data"][0]["resource_id"],
                "limit": 5
            })
        else:
            fields = {"data": []}
        
        return {
            "tables": tables["data"],
            "fields": fields["data"]
        }
    
    # 测试
    state = {"query": "用户信息"}
    result = await search_node(state)
    
    print(f"工作流结果:")
    print(f"  表格：{len(result['tables'])} 个")
    print(f"  字段：{len(result['fields'])} 个\n")


# ==================== 主函数 ====================

async def main():
    """运行所有示例"""
    print("=" * 60)
    print("Semantic Search Skill 使用示例")
    print("=" * 60)
    print()
    
    try:
        # 运行示例
        await example_in_project()
        # await example_custom_config()
        # await example_in_openclaw()
        # await example_batch_call()
        # await example_in_workflow()
        
        print("=" * 60)
        print("示例运行完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 示例运行失败：{e}")
        print("\n可能原因:")
        print("1. 项目配置未正确加载")
        print("2. 数据库连接失败")
        print("3. LLM 服务不可用")
        print("\n请检查配置和环境！")


if __name__ == "__main__":
    asyncio.run(main())
