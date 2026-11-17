#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STARBORNE 本地启动器。

引擎脚本 starborne_*.py 里的 STATE 指向沙箱路径 /workspace/starborne，
在 Windows 本机不存在，save_state 会直接抛 FileNotFoundError。
本启动器不改引擎源码，只在导入后把 STATE 重定向到本项目目录，
让存档 (warehouse.json) 落在游戏目录里。

用法：
    python play.py 单抽
    python play.py 十连
    python play.py 货舱
    python play.py 状态
    python play.py 卖 P-HD-ggy2a0f2
    python play.py 数羊 1 2 3 4 5
    python play.py 拆解 <ID> / 升级 <ID>
    （材料合成已禁用：靠合成最多只能到银河，远古/虚空不许靠合成做出来）
    python play.py 规则 / 详解 <ID> / 最强 / 删除装备 <ID> / 清空货舱 确认
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = None

# 找到引擎脚本（starborne_*.py），排除本启动器自身
for fn in sorted(os.listdir(HERE)):
    if fn.startswith("starborne_") and fn.endswith(".py"):
        ENGINE = os.path.join(HERE, fn)
        break

if ENGINE is None:
    sys.exit("找不到引擎脚本 starborne_*.py")

spec = importlib.util.spec_from_file_location("starborne_engine", ENGINE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# 存档落在游戏目录（首次运行自动创建，赠 300 钱启动资金）
mod.STATE = os.path.join(HERE, "warehouse.json")

if __name__ == "__main__":
    # 材料合成全禁：两条配方（2星尘→太古原石、2太古→虚空）产出的正是"远古/虚空"的门槛材料，
    # 放行任何一条，就能靠合成把装备顶到远古/虚空。靠合成最多只到银河，远古/虚空必须靠原始掉落。
    if sys.argv[1:2] == ["合成"]:
        print("🚫 材料合成已禁用。合成只能把材料往上换（星尘→太古→虚空），"
              "放行就能靠合成升远古/虚空；靠合成最多只到银河。前期升级请直接用原始材料（`升级` 不受影响）。")
        sys.exit(0)
    mod.main()
