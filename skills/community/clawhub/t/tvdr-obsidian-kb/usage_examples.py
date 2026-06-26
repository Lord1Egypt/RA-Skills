"""
Obsidian知识库使用示例
展示如何使用obsidian_kb技能的各个功能
"""

from obsidian_kb import ObsidianKB, create_note, search_notes, save_experience

def basic_usage_example():
    """基础使用示例"""
    print("=== Obsidian知识库基础使用示例 ===")
    
    # 初始化
    kb = ObsidianKB()
    
    # 检查健康状态
    print("1. 检查API健康状态...")
    health = kb.check_health()
    print(f"健康检查结果: {health}")
    
    # 创建笔记
    print("\n2. 创建笔记...")
    content = """# Python编程技巧

## 装饰器模式
装饰器是Python中的重要概念，可以动态扩展函数功能。

```python
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数执行时间: {end - start:.2f}s")
        return result
    return wrapper
```

## 列表推导式
简化代码的利器：
```python
# 传统写法
squares = []
for i in range(10):
    squares.append(i*i)

# 列表推导式
squares = [i*i for i in range(10)]
```

"""
    
    result = create_note(
        title="Python编程技巧总结", 
        content=content,
        tags=["编程", "Python", "技巧"],
        folder="project_lessons"
    )
    print(f"创建笔记结果: {result}")
    
    # 搜索笔记
    print("\n3. 搜索笔记...")
    search_result = search_notes("Python编程", limit=5)
    print(f"搜索结果: {search_result}")
    
    # 获取统计信息
    print("\n4. 获取知识库统计...")
    stats = kb.get_stats()
    print(f"统计信息: {stats}")

def save_experience_example():
    """保存工作经验示例"""
    print("\n=== 保存工作经验示例 ===")
    
    experience_content = """
# 2026-03-28 调试VPN连接问题

## 问题背景
今天遇到VPN连接测试异常的情况，虽然基础网络正常，但VPN连接超时。

## 排查过程
1. 首先测试了基础网络连接
   - Ping 8.8.8.8: 184ms延迟，0%丢包 ✅
   - DNS解析正常 ✅
   - 出口网关: 192.168.18.1 ✅

2. 检查VPN状态
   - 发现WireGuard接口存在 (`wg_hr`)
   - VPN地址: 192.1.1.17/24
   - 但外部连接超时，说明VPN可能未完全激活

3. 查看路由表
   - 存在多个默认路由可能造成冲突
   - VPN路由优先级需要确认

## 解决方案
```bash
# 检查WireGuard状态
sudo wg show

# 检查VPN进程
ps aux | grep wg

# 检查VPN配置文件
cat /etc/wireguard/wg_hr.conf
```

## 经验总结
- 网络问题排查要分层：物理层→网络层→应用层
- VPN连接问题可能是配置、路由或服务状态问题
- 保留排查过程记录便于后续参考
"""

    result = save_experience(
        title="VPN连接问题调试记录",
        content=experience_content,
        category="运维经验",
        tags=["VPN", "网络", "调试", "WireGuard"]
    )
    print(f"保存工作经验结果: {result}")

def workflow_example():
    """工作流使用示例"""
    print("\n=== 工作流使用示例 ===")
    
    # 创建工作流文档
    workflow_content = """# OpenClaw项目工作流程

## 1. 项目创建阶段
- 使用项目模板创建新项目
- 设置角色分工：@美术、@配音、@小编
- 确定项目规范和格式要求

## 2. 设计阶段  
- 角色设计（character.json, profile.json）
- 场景设计（scene.json, views/）
- 分镜设计（storyboard.json, frame.json）

## 3. 内容制作阶段
- 剧本创作（scripts/）
- 音频制作（audio/, subtitles/）
- 视觉素材（assets/）

## 4. 交付阶段
- 质量检查
- 文档归档
- 项目总结

## 注意事项
- 文件命名必须遵循规范
- 素材编号一一对应
- 按照工作流程推进
"""
    
    result = create_note(
        title="OpenClaw项目工作流程",
        content=workflow_content,
        tags=["工作流", "OpenClaw", "项目管理"],
        folder="wf_overview"
    )
    print(f"工作流文档创建结果: {result}")

if __name__ == "__main__":
    try:
        basic_usage_example()
        save_experience_example() 
        workflow_example()
        print("\n✅ 所有示例执行完成！")
    except Exception as e:
        print(f"❌ 示例执行出错: {e}")