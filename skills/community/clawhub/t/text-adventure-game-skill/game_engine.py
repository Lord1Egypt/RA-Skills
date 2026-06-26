#!/usr/bin/env python3
"""
文字冒险游戏引擎
支持自定义剧本、自由互动、精美排版
"""
import json
import os
import random
from typing import Dict, List, Optional

class TextAdventureEngine:
    def __init__(self, save_path: str = "game_saves"):
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)
        
        # 游戏状态
        self.game_state: Dict = {
            "title": "文字冒险游戏",
            "current_scene": "",
            "player": {
                "name": "冒险者",
                "health": 100,
                "max_health": 100,
                "stamina": 100,
                "max_stamina": 100,
                "level": 1,
                "exp": 0,
                "inventory": [],
                "attributes": {}
            },
            "history": [],
            "world": {},
            "npcs": {},
            "quests": [],
            "options": [],
            "game_status": "进行中"
        }
        
        # 排版符号
        self.style = {
            "separator": "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "bullet": "🔹",
            "scene": "🏷️",
            "health": "❤️",
            "stamina": "⚡",
            "exp": "🌟",
            "item": "✅",
            "warning": "⚠️",
            "success": "✅",
            "dialogue": "💬",
            "combat": "⚔️"
        }
    
    def load_script(self, script_content: str) -> None:
        """加载用户提供的剧本"""
        lines = script_content.strip().split('\n')
        
        # 解析标题
        if lines and lines[0].strip():
            self.game_state["title"] = lines[0].strip().lstrip('#').strip()
        
        # 解析初始场景
        content_lines = [line for line in lines[1:] if line.strip()]
        if content_lines:
            self.game_state["current_scene"] = '\n'.join(content_lines)
        else:
            self.game_state["current_scene"] = "你站在一个陌生的地方，不知道自己是谁，也不知道要去哪里。四周一片荒凉，只有一条小路延伸向远方。"
        
        # 生成初始选项
        self._generate_initial_options()
    
    def _generate_initial_options(self) -> None:
        """生成初始场景选项"""
        self.game_state["options"] = [
            "沿着小路往前走",
            "观察周围的环境",
            "检查自己身上的物品"
        ]
    
    def process_player_action(self, action: str) -> str:
        """处理玩家的输入/选择，生成回应"""
        action_lower = action.lower()
        
        # 处理系统命令
        if action_lower == "存档":
            self._save_game()
            return self._format_response("游戏已保存！", status="success")
        elif action_lower == "读档":
            self._load_game()
            return self._format_response("游戏已加载！", status="success")
        elif action_lower in ["状态", "属性", "背包"]:
            return self._format_status()
        elif action_lower == "重新开始":
            self._reset_game()
            return self._format_response("游戏已重置！", status="success")
        elif action_lower in ["帮助", "help"]:
            return self._format_help()
        elif action_lower == "退出":
            self.game_state["game_status"] = "已结束"
            return self._format_response("游戏已结束，期待下次冒险！", status="info")
        
        # 记录历史
        self.game_state["history"].append({
            "action": action,
            "response": ""
        })
        
        # 生成剧情回应
        response = self._generate_story_response(action)
        self.game_state["history"][-1]["response"] = response
        
        # 生成新的选项
        self._generate_options(action)
        
        return self._format_response(response)
    
    def _generate_story_response(self, action: str) -> str:
        """根据玩家动作生成剧情回应（示例逻辑，可扩展接入LLM）"""
        # 示例回应库
        responses = {
            "沿着小路往前走": "你沿着小路走了大约一个小时，前方出现了一个分岔路口。左边的路通向一片茂密的森林，右边的路通向一座看起来荒废已久的村庄。",
            "观察周围的环境": "你仔细观察四周，发现路边有一块破旧的路牌，上面的文字已经模糊不清，只能隐约看到" + random.choice(["'危险'", "'前方有熊'", "'禁止入内'"]) + "的字样。地上散落着一些奇怪的脚印，看起来不像是人类的。",
            "检查自己身上的物品": "你翻了翻身上的口袋，找到了一些铜币、一块干硬的面包、还有一把生锈的小刀。衣服内侧缝着一个陌生的徽章，你完全不记得它的来历。",
            "走左边的路": "你走进了森林，树木越来越茂密，光线也越来越暗。空气中弥漫着潮湿的腐叶味道，偶尔传来奇怪的叫声。走了没多久，你看到前面有一个小木屋，烟囱里正冒着烟。",
            "走右边的路": "你走向荒废的村庄，村子里静悄悄的，一个人影都没有。大部分房屋都已经倒塌，只有村口的酒馆看起来还算完整。酒馆的门半掩着，里面似乎有声音传出来。",
            "进入木屋": "你推开门，木屋里面很温暖，壁炉里的火正烧得旺。一个白发苍苍的老人坐在火炉边，看到你进来，抬起头笑了笑：'旅行者，欢迎来到我的小屋，要不要喝杯热酒暖暖身子？'"
        }
        
        # 模糊匹配
        for key in responses:
            if key in action or action in key:
                return responses[key]
        
        # 默认回应
        return f"你选择了：{action}\n\n（剧情正在生成中...你的选择将会影响后续的冒险）"
    
    def _generate_options(self, last_action: str) -> None:
        """根据当前场景生成选项"""
        # 示例选项逻辑
        if "分岔路口" in self.game_state["current_scene"]:
            self.game_state["options"] = [
                "走左边的路去森林",
                "走右边的路去村庄",
                "先在原地休息一下"
            ]
        elif "森林" in self.game_state["current_scene"] and "小木屋" in self.game_state["current_scene"]:
            self.game_state["options"] = [
                "敲门进入木屋",
                "偷偷绕到屋后看看",
                "继续往森林深处走"
            ]
        elif "村庄" in self.game_state["current_scene"] and "酒馆" in self.game_state["current_scene"]:
            self.game_state["options"] = [
                "进入酒馆看看",
                "搜索其他房屋",
                "离开村庄回到分岔路口"
            ]
        else:
            self.game_state["options"] = [
                "继续前进",
                "停下来休息",
                "检查背包"
            ]
    
    def _format_response(self, content: str, status: str = "normal") -> str:
        """格式化输出，生成精美排版"""
        output = []
        
        # 标题栏
        output.append(f"{self.style['scene']} 【当前场景】：{self.game_state['title']}")
        output.append(self.style["separator"])
        
        # 剧情内容
        output.append(content)
        output.append("")
        
        # 选项
        if self.game_state["options"]:
            output.append(f"{self.style['bullet']} 你可以选择：")
            for i, option in enumerate(self.game_state["options"], 1):
                output.append(f"  {i}. {option}")
            output.append("")
        
        # 状态摘要
        output.append(f"{self.style['health']} 生命值：{self.game_state['player']['health']}/{self.game_state['player']['max_health']}")
        output.append(f"{self.style['stamina']} 体力：{self.game_state['player']['stamina']}/{self.game_state['player']['max_stamina']}")
        output.append(f"{self.style['exp']} 经验：{self.game_state['player']['exp']}/{self.game_state['player']['level'] * 100}")
        
        if len(self.game_state["player"]["inventory"]) > 0:
            output.append("")
            output.append("🎒 背包物品：")
            for item in self.game_state["player"]["inventory"]:
                output.append(f"  {self.style['item']} {item}")
        
        output.append(self.style["separator"])
        
        # 提示
        if status == "success":
            output.append(f"{self.style['success']} 操作成功！")
        elif status == "warning":
            output.append(f"{self.style['warning']} 请注意：这可能是一个危险的选择！")
        elif status == "info":
            output.append("ℹ️ 提示：输入'帮助'查看所有可用命令")
        
        return '\n'.join(output)
    
    def _format_status(self) -> str:
        """格式化状态输出"""
        player = self.game_state["player"]
        output = []
        
        output.append(f"📊 【玩家状态】：{player['name']}")
        output.append(self.style["separator"])
        output.append(f"等级：Lv.{player['level']}")
        output.append(f"{self.style['health']} 生命值：{player['health']}/{player['max_health']}")
        output.append(f"{self.style['stamina']} 体力：{player['stamina']}/{player['max_stamina']}")
        output.append(f"{self.style['exp']} 经验值：{player['exp']}/{player['level'] * 100}")
        output.append("")
        
        if player["inventory"]:
            output.append("🎒 背包物品：")
            for item in player["inventory"]:
                output.append(f"  {self.style['item']} {item}")
        else:
            output.append("🎒 背包是空的")
        
        if self.game_state["quests"]:
            output.append("")
            output.append("📋 当前任务：")
            for quest in self.game_state["quests"]:
                status = "✅ 已完成" if quest["completed"] else "🔄 进行中"
                output.append(f"  {status} {quest['name']}")
        
        output.append(self.style["separator"])
        output.append("ℹ️ 提示：输入'帮助'查看所有可用命令")
        
        return '\n'.join(output)
    
    def _format_help(self) -> str:
        """格式化帮助信息"""
        output = []
        output.append("❓ 【游戏帮助】")
        output.append(self.style["separator"])
        output.append("🔹 基础操作：")
        output.append("  直接输入你想做的事情，比如：'往前走'、'和老人对话'")
        output.append("  也可以输入选项编号快速选择，比如：'1'、'2'")
        output.append("")
        output.append("🔹 系统命令：")
        output.append("  存档 - 保存当前游戏进度")
        output.append("  读档 - 读取最近的存档")
        output.append("  状态 - 查看当前属性和背包")
        output.append("  重新开始 - 重置游戏回到初始状态")
        output.append("  退出 - 结束当前游戏")
        output.append("  帮助 - 显示此帮助信息")
        output.append(self.style["separator"])
        output.append("💡 小提示：多和NPC对话，仔细搜索场景，可能会发现隐藏的道具和剧情！")
        
        return '\n'.join(output)
    
    def _save_game(self, save_name: str = "default") -> None:
        """保存游戏进度"""
        save_file = os.path.join(self.save_path, f"{save_name}.json")
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(self.game_state, f, ensure_ascii=False, indent=2)
    
    def _load_game(self, save_name: str = "default") -> None:
        """加载游戏进度"""
        save_file = os.path.join(self.save_path, f"{save_name}.json")
        if os.path.exists(save_file):
            with open(save_file, "r", encoding="utf-8") as f:
                self.game_state = json.load(f)
    
    def _reset_game(self) -> None:
        """重置游戏"""
        self.game_state = {
            "title": "文字冒险游戏",
            "current_scene": "你站在一个陌生的地方，不知道自己是谁，也不知道要去哪里。四周一片荒凉，只有一条小路延伸向远方。",
            "player": {
                "name": "冒险者",
                "health": 100,
                "max_health": 100,
                "stamina": 100,
                "max_stamina": 100,
                "level": 1,
                "exp": 0,
                "inventory": [],
                "attributes": {}
            },
            "history": [],
            "world": {},
            "npcs": {},
            "quests": [],
            "options": ["沿着小路往前走", "观察周围的环境", "检查自己身上的物品"],
            "game_status": "进行中"
        }

# 示例用法
if __name__ == "__main__":
    engine = TextAdventureEngine()
    engine.load_script("""森林冒险
你站在幽暗的森林入口，四周雾气弥漫，不知道前方等待着什么。传说森林深处藏着巨大的宝藏，但也充满了危险。
""")
    print(engine.process_player_action("观察周围的环境"))
