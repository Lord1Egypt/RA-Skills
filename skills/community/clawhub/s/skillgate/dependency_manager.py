"""
Skill Dependency Manager — 依赖管理。
管理 skill 之间的依赖关系。
"""
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class SkillDependency:
    """一个 skill 的依赖声明。"""
    name: str
    depends_on: List[str]  # 依赖哪些 skill


# 我们的 skill 依赖关系
DEPENDENCIES = [
    SkillDependency(
        name="skillgate",
        depends_on=[]  # 不依赖任何 skill
    ),
    SkillDependency(
        name="lgd-gate-methodology",
        depends_on=[]  # 不依赖任何 skill
    ),
    SkillDependency(
        name="reg-citation-normalizer",
        depends_on=[]  # 不依赖任何 skill
    ),
    SkillDependency(
        name="medxpert-termbase",
        depends_on=[]  # 不依赖任何 skill
    ),
    SkillDependency(
        name="iso14971-risk-matrix",
        depends_on=[]  # 不依赖任何 skill
    ),
]


def build_dependency_graph() -> Dict[str, List[str]]:
    """构建依赖图。"""
    graph = {}
    for dep in DEPENDENCIES:
        graph[dep.name] = dep.depends_on
    return graph


def get_dependencies(skill_name: str) -> List[str]:
    """获取一个 skill 的所有依赖（递归）。"""
    graph = build_dependency_graph()

    if skill_name not in graph:
        return []

    visited = set()
    result = []

    def dfs(name: str):
        if name in visited:
            return
        visited.add(name)
        for dep in graph[name]:
            dfs(dep)
            if dep not in result:
                result.append(dep)

    dfs(skill_name)
    return result


def check_dependency_chain() -> bool:
    """检查依赖链有没有循环依赖。"""
    graph = build_dependency_graph()

    visited = set()
    stack = set()

    def has_cycle(name: str) -> bool:
        visited.add(name)
        stack.add(name)

        for dep in graph.get(name, []):
            if dep not in visited:
                if has_cycle(dep):
                    return True
            elif dep in stack:
                return True

        stack.remove(name)
        return False

    for skill_name in graph:
        if skill_name not in visited:
            if has_cycle(skill_name):
                return True

    return False


def main():
    print("=" * 60)
    print("  🔗 Skill Dependency Manager — 依赖管理")
    print("=" * 60)

    graph = build_dependency_graph()

    print(f"\n  总 skill 数: {len(graph)}")
    print(f"\n  依赖关系：")
    for name, deps in graph.items():
        if deps:
            print(f"    {name} → 依赖: {', '.join(deps)}")
        else:
            print(f"    {name} → 无依赖")

    has_cycle = check_dependency_chain()
    print(f"\n  循环依赖检查: {'❌ 有循环依赖' if has_cycle else '✅ 无循环依赖'}")

    print("\n" + "=" * 60)
    print("  ✅ 依赖管理检查完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
