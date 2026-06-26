#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker Connector 技能 - 技能主类
帮助用户调用 Quicker 工具中的动作
"""

import re
import sys
from typing import Optional, List, Dict, Any

from quicker_connector import (
    QuickerConnector,
    QuickerAction,
    QuickerActionResult,
    is_initialized,
    print_initialization_guide
)


class QuickerSkill:
    """Quicker 技能主类"""

    def __init__(self, source: str = "csv"):
        """
        初始化技能

        Args:
            source: 数据源类型，"csv" 或 "db"
        """
        print("正在初始化 Quicker 技能...")

        if not is_initialized():
            print("\n技能尚未配置！")
            print_initialization_guide()
            sys.exit(1)

        try:
            self.connector = QuickerConnector(source=source)
            self.actions = self.connector.read_actions()
            print(f"已加载 {len(self.actions)} 个 Quicker 动作")
        except Exception as e:
            print(f"初始化失败: {e}")
            sys.exit(1)

    def should_trigger(self, user_input: str) -> bool:
        """
        判断是否应该触发该技能

        Args:
            user_input: 用户输入

        Returns:
            是否触发
        """
        return re.search(r'quicker', user_input, re.IGNORECASE) is not None

    def process_request(self, user_input: str) -> str:
        """
        处理用户请求

        Args:
            user_input: 用户输入

        Returns:
            处理结果
        """
        if not self.should_trigger(user_input):
            return "该请求不包含 Quicker 关键词，无法处理"

        user_need = self._extract_user_need(user_input)
        print(f"\n用户需求: {user_need}")

        matches = self.connector.match_actions(user_need, top_n=5)

        if not matches:
            return f"未找到与 '{user_need}' 相关的动作"

        result_text = f"找到 {len(matches)} 个匹配的 Quicker 动作:\n\n"

        for i, match in enumerate(matches, 1):
            action = match['action']
            score = match['score']
            result_text += f"{i}. {action.name} (分数: {score:.2f})\n"
            if action.description and len(action.description) < 100:
                result_text += f"   描述: {action.description}\n"
            result_text += f"   ID: {action.id}\n\n"

        selected_action = self._select_action(matches)
        if not selected_action:
            return "已取消操作"

        print(f"\n即将执行动作: {selected_action.name}")
        result = self.connector.execute_action(selected_action.id)

        return self._format_result(result)

    def _extract_user_need(self, user_input: str) -> str:
        """
        从用户输入中提取需求

        Args:
            user_input: 用户输入

        Returns:
            用户需求
        """
        need = re.sub(r'quicker', '', user_input, flags=re.IGNORECASE)
        need = re.sub(r'帮我|用|调用|执行|的', '', need)
        need = need.strip()
        return need or user_input

    def _select_action(self, matches: List[Dict[str, Any]]) -> Optional[QuickerAction]:
        """
        选择动作

        Args:
            matches: 匹配结果列表

        Returns:
            选中的动作，如果用户取消则返回 None
        """
        if not matches:
            return None

        if len(matches) == 1 and matches[0]['score'] > 0.8:
            print(f"自动选择: {matches[0]['action'].name}")
            return matches[0]['action']

        print("\n请选择要执行的动作:")
        for i, match in enumerate(matches, 1):
            print(f"  {i}. {match['action'].name}")

        print(f"\n自动选择分数最高的动作: {matches[0]['action'].name}")
        return matches[0]['action']

    def _format_result(self, result: QuickerActionResult) -> str:
        """
        格式化执行结果

        Args:
            result: 执行结果

        Returns:
            格式化后的结果文本
        """
        if result.success:
            output = "动作执行成功\n"
            if result.output:
                output += f"\n执行结果:\n{result.output}"
            return output
        else:
            output = "动作执行失败"
            if result.error:
                output += f"\n错误信息: {result.error}"
            return output

    def interactive_mode(self):
        """交互式模式"""
        print("\n" + "=" * 60)
        print("Quicker 技能交互模式")
        print("=" * 60)
        print("输入您的需求，或输入 'quit' 退出\n")

        while True:
            try:
                user_input = input("\n> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                    print("再见！")
                    break

                result = self.process_request(user_input)
                print(f"\n{result}")

            except KeyboardInterrupt:
                print("\n\n再见！")
                break
            except Exception as e:
                print(f"\n发生错误: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("Quicker Connector 技能")
    print("=" * 60)

    source = "csv"
    if len(sys.argv) > 1:
        if sys.argv[1] == "db":
            source = "db"

    skill = QuickerSkill(source=source)

    if len(sys.argv) > 1 and sys.argv[1] not in ["csv", "db"]:
        user_input = ' '.join(sys.argv[1:])
        print(f"\n处理请求: '{user_input}'")
        result = skill.process_request(user_input)
        print(f"\n{result}")
    else:
        skill.interactive_mode()


if __name__ == "__main__":
    main()
