#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 LLM 进行需求文档检查（增强版 + 智能配置引导）
支持多种配置来源：环境变量、OpenClaw 配置、本地缓存、临时输入

优化点：
- ✅ 自动检测所有可用配置
- ✅ 配置保存到本地 config.json
- ✅ 简化引导流程（一键检测）
- ✅ 配置验证（测试连接）
- ✅ 友好错误提示
"""

import sys
import json
import requests
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


# ============================================================================
# 配置管理
# ============================================================================


def get_llm_config() -> Optional[Dict]:
    """
    获取 LLM 配置（智能检测 + 自动选择）

    检测顺序：
    1. 本地缓存配置（config.json）- 最快
    2. 环境变量 - 通用
    3. OpenClaw 配置 - 自动扫描所有 provider
    4. 引导用户配置
    """

    # 1️⃣ 本地缓存配置（优先使用，避免重复检测）
    local_config = load_local_config()
    if local_config:
        print("✅ 使用本地缓存配置")
        print(f"   Source: {local_config.get('source', 'unknown')}")
        print(f"   Model: {local_config.get('model', 'glm-5')}")
        return local_config

    # 2️⃣ 环境变量（通用方案）
    env_config = get_env_config()
    if env_config:
        print("✅ 使用环境变量配置")
        print(f"   Base URL: {env_config['base_url']}")
        print(f"   Model: {env_config.get('model', 'glm-5')}")
        # 保存到本地缓存
        save_local_config(env_config, source="env")
        return env_config

    # 3️⃣ OpenClaw 配置（自动扫描所有 provider）
    openclaw_configs = scan_openclaw_providers()
    if openclaw_configs:
        provider_names = list(openclaw_configs.keys())
        print(
            f"✅ 检测到 {len(openclaw_configs)} 个 OpenClaw provider: {', '.join(provider_names)}"
        )

        # 自动选择优先级最高的 provider
        selected_provider = select_best_provider(provider_names)
        config = openclaw_configs[selected_provider]

        print(f"   已自动选择：{selected_provider}")
        print(f"   Base URL: {config['base_url']}")

        # 保存到本地缓存
        save_local_config(config, source=f"openclaw:{selected_provider}")
        return config

    # 4️⃣ 引导用户配置
    print("\n⚠️  未检测到 LLM API 配置")
    return guide_config_setup()


def get_env_config() -> Optional[Dict]:
    """从环境变量读取配置"""
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if api_key and base_url:
        return {
            "api_key": api_key,
            "base_url": base_url,
            "model": os.getenv("OPENAI_MODEL", "glm-5"),
        }
    return None


def load_local_config() -> Optional[Dict]:
    """从本地 config.json 读取缓存配置"""
    config_path = Path(__file__).parent.parent / "config.json"

    if not config_path.exists():
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        api_config = config.get("api", {})

        # 检查必需字段
        if (
            not api_config
            or not api_config.get("api_key")
            or not api_config.get("base_url")
        ):
            return None

        # 处理 model 为 null 的情况
        model = api_config.get("model")
        if model is None or model == "":
            model = "glm-5"

        return {
            "api_key": api_config["api_key"],
            "base_url": api_config["base_url"],
            "model": model,
            "source": api_config.get("source", "local"),
        }
    except Exception as e:
        print(f"⚠️ 读取本地配置失败：{e}")
        return None


def save_local_config(config: Dict, source: str = "manual"):
    """保存配置到本地 config.json"""
    config_path = Path(__file__).parent.parent / "config.json"

    try:
        # 读取现有配置
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                local_config = json.load(f)
        else:
            local_config = {"version": "2.4", "description": "需求文档检查技能配置文件"}

        # 更新 API 配置
        local_config["api"] = {
            "api_key": config["api_key"],
            "base_url": config["base_url"],
            "model": config.get("model", "glm-5"),
            "source": source,
            "last_updated": datetime.now().isoformat(),
        }

        # 保存配置
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(local_config, f, indent=2, ensure_ascii=False)

        print("✅ 配置已保存到 config.json")

    except Exception as e:
        print(f"⚠️ 保存配置失败：{e}")


def scan_openclaw_providers() -> Dict[str, Dict]:
    """扫描 OpenClaw 配置中的所有可用 provider"""
    config_path = Path.home() / ".openclaw" / "openclaw.json"

    if not config_path.exists():
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        models_config = config.get("models", {})
        providers = models_config.get("providers", {})

        available = {}
        for provider_name, provider_config in providers.items():
            if provider_config and provider_config.get("apiKey"):
                available[provider_name] = {
                    "api_key": provider_config["apiKey"],
                    "base_url": provider_config.get(
                        "baseUrl", "https://dashscope.aliyuncs.com/compatible-mode/v1"
                    ),
                    "model": "glm-5",  # 默认模型
                }

        return available

    except Exception as e:
        print(f"⚠️ 读取 OpenClaw 配置失败：{e}")
        return {}


def select_best_provider(providers: List[str]) -> str:
    """
    选择最优 provider

    优先级：
    1. bailian (阿里云百炼，性价比高)
    2. moonshot (Kimi，长文本)
    3. openai (通用)
    4. zhipu (智谱，embedding)
    5. 其他（按字母顺序）
    """
    priority = ["bailian", "moonshot", "openai", "zhipu"]

    for p in priority:
        if p in providers:
            return p

    # 返回第一个
    return sorted(providers)[0]


def guide_config_setup() -> Optional[Dict]:
    """引导用户配置 API Key（简化版）"""

    print("\n" + "=" * 60)
    print("AI 检查功能需要配置 API Key\n")

    print("【A】自动检测（推荐）✨")
    print("  - 扫描环境变量、OpenClaw 配置")
    print("  - 自动选择最优配置")
    print("  - 保存到本地，下次无需重复配置\n")

    print("【B】手动配置")
    print("  - 输入 API Key 和 Base URL")
    print("  - 适合临时使用或特殊需求\n")

    print("【C】跳过")
    print("  - 使用规则检查模式（功能受限）\n")

    print("=" * 60)

    choice = input("\n请选择（默认 A）: ").strip().upper()

    if choice == "" or choice == "A":
        # 自动检测
        print("\n🔍 正在检测可用配置...")

        # 检测环境变量
        env_config = get_env_config()
        if env_config:
            print("✅ 检测到环境变量配置")
            save_local_config(env_config, source="env")
            return env_config

        # 检测 OpenClaw
        openclaw_configs = scan_openclaw_providers()
        if openclaw_configs:
            provider_names = list(openclaw_configs.keys())
            print(
                f"✅ 检测到 {len(openclaw_configs)} 个 OpenClaw provider: {', '.join(provider_names)}"
            )
            selected = select_best_provider(provider_names)
            config = openclaw_configs[selected]
            print(f"   已选择：{selected}")
            save_local_config(config, source=f"openclaw:{selected}")
            return config

        print("\n❌ 未检测到任何可用配置")
        print("请手动配置或检查 ~/.openclaw/openclaw.json")
        return None

    elif choice == "B":
        # 手动配置
        print("\n请输入配置信息：")
        api_key = input("API Key: ").strip()

        if not api_key:
            print("\n❌ API Key 不能为空")
            return None

        base_url = input(
            "Base URL（默认 https://coding.dashscope.aliyuncs.com/v1）: "
        ).strip()
        base_url = base_url or "https://coding.dashscope.aliyuncs.com/v1"

        model = input("Model（默认 glm-5）: ").strip() or "glm-5"

        config = {"api_key": api_key, "base_url": base_url, "model": model}

        # 询问是否保存
        save_choice = input("\n是否保存配置到 config.json？（Y/n）: ").strip().lower()
        if save_choice == "" or save_choice == "y":
            save_local_config(config, source="manual")

        return config

    else:
        # 跳过
        print("\n⚠️ 将使用规则检查模式（功能受限）")
        return None


def validate_config(config: Dict, timeout: int = 10) -> bool:
    """
    验证配置是否可用（测试连接）

    Returns:
        bool: True 表示配置可用，False 表示不可用
    """
    try:
        response = requests.post(
            f"{config['base_url']}/chat/completions",
            headers={
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json",
            },
            json={
                "model": config.get("model", "glm-5"),
                "messages": [{"role": "user", "content": "Hello, this is a test."}],
                "max_tokens": 10,
            },
            timeout=timeout,
        )

        if response.status_code == 200:
            return True
        else:
            print(f"⚠️  API 返回错误：{response.status_code}")
            try:
                error = response.json()
                print(f"   {error.get('error', {}).get('message', 'Unknown error')}")
            except:
                print(f"   {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("⚠️  请求超时，请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("⚠️  无法连接到 API 服务器，请检查 Base URL")
        return False
    except Exception as e:
        print(f"⚠️  验证失败：{e}")
        return False


# ============================================================================
# LLM 检查器
# ============================================================================


def check_with_llm(
    content: str,
    filename: str,
    model: str = "glm-5",
    config: Optional[Dict] = None,
    timeout: int = 120,
    max_retries: int = 3,
) -> Dict:
    """
    使用 LLM 检查需求文档

    Args:
        content: 需求文档内容
        filename: 文件名
        model: 模型名称
        config: API 配置（如果不传，自动获取）
        timeout: 超时时间（秒），默认 120 秒
        max_retries: 最大重试次数，默认 3 次

    Returns:
        Dict: 检查结果
    """

    # 获取配置
    if config is None:
        config = get_llm_config()

    if config is None:
        return {
            "success": False,
            "error": "未配置 LLM API",
            "summary": {"status": "skipped", "message": "未配置 API，跳过 AI 检查"},
            "warnings": [],
            "passed": [],
            "gwt_acceptance": {},
        }

    # 使用配置中的 model（如果未指定）
    if model == "glm-5" and config.get("model"):
        model = config["model"]

    # 构建 prompt
    prompt = build_check_prompt(content, filename)

    # 重试逻辑
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                print(f"  🔄 第 {attempt} 次重试...")

            # 调用 LLM API
            response = requests.post(
                f"{config['base_url']}/chat/completions",
                headers={
                    "Authorization": f"Bearer {config['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一位经验丰富的需求文档评审专家，擅长发现需求文档中的问题并给出建设性的优化建议。",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 4000,
                },
                timeout=timeout,
            )

            if response.status_code != 200:
                error_msg = f"API 请求失败：{response.status_code}"
                try:
                    error = response.json()
                    error_msg = error.get("error", {}).get("message", error_msg)
                except:
                    pass

                # 如果是服务器错误，可以重试
                if response.status_code >= 500 and attempt < max_retries:
                    print(f"  ⚠️  {error_msg}，准备重试...")
                    continue

                return {
                    "success": False,
                    "error": error_msg,
                    "summary": {"status": "error", "message": error_msg},
                    "warnings": [],
                    "passed": [],
                    "gwt_acceptance": {},
                }

            # 解析响应
            result = response.json()
            llm_output = result["choices"][0]["message"]["content"]

            # 解析 LLM 输出
            return parse_llm_output(llm_output, content)

        except requests.exceptions.Timeout:
            last_error = "API 请求超时"
            if attempt < max_retries:
                print(f"  ⚠️  请求超时（{timeout}秒），准备重试...")
                continue

        except requests.exceptions.ConnectionError:
            last_error = "网络连接失败"
            if attempt < max_retries:
                print(f"  ⚠️  网络连接失败，准备重试...")
                continue

        except Exception as e:
            last_error = str(e)
            if attempt < max_retries:
                print(f"  ⚠️  {str(e)}，准备重试...")
                continue

    # 所有重试都失败了
    return {
        "success": False,
        "error": last_error,
        "summary": {
            "status": "error",
            "message": f"检查失败（已重试{max_retries}次）: {last_error}",
        },
        "warnings": [],
        "passed": [],
        "gwt_acceptance": {},
    }


def build_check_prompt(content: str, filename: str) -> str:
    """构建检查 prompt"""

    return f"""
请帮助检查以下需求文档，提供完善建议以提升文档质量。

## 检查维度（13 项）

### 核心建议（影响理解的关键项）
1. **流程描述** - 是否有业务流程图或流程说明，帮助理解整体业务
2. **异常处理** - 是否说明了异常场景和错误提示，帮助用户应对问题

### 完善建议（提升文档质量）
3. **改造内容标注** - 新增/改造/优化内容是否清晰标注，方便理解改动范围
4. **元素完整性** - 输入/输出/处理/界面元素是否完整，帮助开发理解需求
5. **交互逻辑** - 用户操作流程和系统响应逻辑是否清晰，帮助理解业务场景
6. **算法公式** - 计算逻辑、公式规则是否说明，帮助准确实现功能
7. **查询关联** - 数据查询逻辑、表关联关系是否说明，帮助设计数据流程
8. **GWT 验收标准** - 是否有 Given-When-Then 格式的验收标准，帮助验证功能
9. **系统对接描述** ⭐新增 - 如果涉及系统对接，建议包含以下内容：
   - 对接方（哪个系统/部门）
   - 对接数据内容（具体字段、数据类型）
   - 对接数据应用（用途、业务场景）
   - 对接频率（实时/定时/批量）
   - 对接方式（API/文件/MQ/数据库）
   - 数据时效性（T+0/T+1/延迟要求）

### 优化建议（锦上添花）
10. **分项描述** - 功能点是否拆分清晰，方便理解细节
11. **界面细节** - UI/UX 说明、原型图是否完整，帮助前端实现
12. **改造类型** - 新增/改造/优化类型是否标注，帮助理解变更性质
13. **原型附件** - 是否有原型图或截图，帮助直观理解界面

## 特别说明

- 如果需求涉及系统对接（关键词：对接、接口、上游、下游、外部系统），建议检查第9项
- 如果不涉及系统对接，第9项标记为"不适用"

## 输出要求

请按以下 JSON 格式输出检查结果：

```json
{{
  "summary": {{
    "status": "excellent|pass|suggestion|needs_improvement",
    "message": "总体评价（温柔话术，建议式）"
  }},
  "passed": ["检查通过的维度列表"],
  "suggestions": [
    {{
      "dimension": "维度名称",
      "priority": "core|improve|optimize",
      "issue": "可以完善的地方（温柔话术）",
      "suggestion": "具体的完善建议",
      "quote": "原文引用（如果适用）"
    }}
  ],
  "gwt_acceptance": {{
    "has_gwt": true/false,
    "examples": ["GWT 示例列表"]
  }}
}}
```

## 话术要求

- 使用"建议式"话术，帮助用户完善文档
- 用"如果能...会更完整"代替"未说明..."
- 用"建议补充"代替"缺失"
- 用"可以考虑"代替"必须"
- priority说明：
  - core: 核心建议，影响理解的关键内容
  - improve: 完善建议，提升文档质量
  - optimize: 优化建议，锦上添花
- 拿不准时温柔建议，让用户自己判断

## 需求文档内容

文件名：{filename}

---

{content}

---

请开始检查并输出 JSON 格式的检查结果。
"""


def parse_llm_output(llm_output: str, original_content: str) -> Dict:
    """解析 LLM 输出的 JSON"""

    try:
        # 尝试提取 JSON
        import re

        json_match = re.search(r"```json\s*(.*?)\s*```", llm_output, re.DOTALL)

        if json_match:
            json_str = json_match.group(1)
        else:
            # 尝试直接解析
            json_str = llm_output

        result = json.loads(json_str)

        return {
            "success": True,
            "summary": result.get("summary", {}),
            "passed": result.get("passed", []),
            "warnings": result.get("warnings", []),
            "gwt_acceptance": result.get("gwt_acceptance", {}),
            "source": "llm",
        }

    except json.JSONDecodeError as e:
        # JSON 解析失败，返回降级结果
        print(f"⚠️  LLM 输出解析失败：{e}")

        return {
            "success": True,
            "summary": {
                "status": "warning",
                "message": "AI 检查完成，但结果解析失败，请参考原始输出",
            },
            "passed": [],
            "warnings": [
                {
                    "dimension": "格式",
                    "issue": "AI 返回格式可能不完整",
                    "suggestion": "建议人工复核文档质量",
                }
            ],
            "gwt_acceptance": {},
            "source": "llm_fallback",
            "raw_output": llm_output,
        }


# ============================================================================
# 主函数（独立运行测试）
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LLM 配置测试")
    print("=" * 60)

    config = get_llm_config()

    if config:
        print("\n✅ 配置获取成功")
        print(f"   API Key: {config['api_key'][:20]}...")
        print(f"   Base URL: {config['base_url']}")
        print(f"   Model: {config.get('model', 'glm-5')}")
        print(f"   Source: {config.get('source', 'unknown')}")

        # 验证配置
        print("\n🔍 正在验证配置...")
        if validate_config(config):
            print("✅ 配置验证通过，可以正常使用")
        else:
            print("❌ 配置验证失败，请检查 API Key 和网络连接")
    else:
        print("\n❌ 未获取到配置")
