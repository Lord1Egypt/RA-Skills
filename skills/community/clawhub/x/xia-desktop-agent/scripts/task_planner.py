"""任务规划器 - 通过LLM将自然语言拆解为操作步骤"""

import json
import logging
import requests

logger = logging.getLogger(__name__)

LLM_URL = "http://127.0.0.1:18789/v1/chat/completions"

SYSTEM_PROMPT = """你是一个桌面操作规划器。将用户的自然语言任务拆解为具体的桌面操作步骤。

每步操作格式为JSON对象，包含：
- action: 操作类型，可选值：click, double_click, type_text, press_key, scroll, open_app, wait, screenshot, find_and_click
- 参数根据action类型：
  - click/double_click: x, y (坐标) 或 text (屏幕文字描述)
  - type_text: text (要输入的文字)
  - press_key: key (按键名，如 enter, tab, ctrl+c)
  - scroll: amount (正数上，负数下)
  - open_app: app (应用名)
  - wait: seconds (秒数)
  - screenshot: 无参数
  - find_and_click: text (要查找的文字/元素描述)
- description: 步骤说明（中文）

返回JSON数组，不要其他内容。示例：
[
  {"action": "open_app", "app": "notepad", "description": "打开记事本"},
  {"action": "wait", "seconds": 1, "description": "等待记事本启动"},
  {"action": "type_text", "text": "Hello World", "description": "输入文字"}
]"""


def plan_task(task: str, max_steps: int = 20) -> list[dict]:
    """将自然语言任务拆解为操作步骤列表"""
    payload = {
        "model": "default",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"任务：{task}\n\n最多{max_steps}步，返回JSON数组。"}
        ],
        "temperature": 0.1,
        "max_tokens": 2048
    }

    try:
        resp = requests.post(LLM_URL, json=payload, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

        # 提取JSON（处理markdown代码块包裹的情况）
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        steps = json.loads(content.strip())
        if not isinstance(steps, list):
            raise ValueError("返回结果不是数组")

        # 限制最大步数
        steps = steps[:max_steps]
        logger.info(f"任务规划完成: {len(steps)} 步")
        for i, step in enumerate(steps, 1):
            logger.info(f"  {i}. [{step.get('action')}] {step.get('description', '')}")
        return steps

    except json.JSONDecodeError as e:
        logger.error(f"解析LLM返回失败: {e}")
        logger.error(f"原始内容: {content[:500]}")
        return []
    except Exception as e:
        logger.error(f"任务规划失败: {e}")
        return []


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python task_planner.py <任务描述>")
        sys.exit(1)

    task = sys.argv[1]
    steps = plan_task(task)
    print(json.dumps(steps, ensure_ascii=False, indent=2))
