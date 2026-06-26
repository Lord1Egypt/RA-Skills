#!/usr/bin/env python3
import json
import os
import subprocess
import tempfile


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_SH = os.path.join(ROOT, "run.sh")


def run_cmd(args, env):
    proc = subprocess.run(
        ["bash", RUN_SH] + args,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def main():
    with tempfile.TemporaryDirectory() as td:
        env = os.environ.copy()
        env["WARDROBE_DB_PATH"] = os.path.join(td, "wardrobe.db")

        run_cmd(["init", "--json"], env)
        run_cmd(
            [
                "add",
                "--name",
                "白色T恤",
                "--category",
                "上衣",
                "--color",
                "白色",
                "--season",
                "夏",
                "--json",
            ],
            env,
        )
        run_cmd(
            [
                "add",
                "--name",
                "蓝色牛仔裤",
                "--category",
                "下装",
                "--color",
                "蓝色",
                "--season",
                "四季",
                "--json",
            ],
            env,
        )
        run_cmd(
            [
                "add",
                "--name",
                "黑色西裤",
                "--category",
                "下装",
                "--color",
                "黑色",
                "--style",
                "商务",
                "--season",
                "四季",
                "--json",
            ],
            env,
        )

        outfit = run_cmd(
            ["outfit", "--scene", "commute", "--weather", "30°C晴天", "--json"],
            env,
        )
        assert outfit["status"] == "ok"
        assert outfit["scene"] == "work"
        assert "missing_categories" in outfit
        assert "selected_items" in outfit
        assert outfit["outfit_id"]

        feedback = run_cmd(
            [
                "feedback",
                "--outfit-id",
                outfit["outfit_id"],
                "--feedback",
                "like",
                "--note",
                "适合通勤",
                "--json",
            ],
            env,
        )
        assert feedback["updated"] is True

        outfit_after_feedback = run_cmd(
            ["outfit", "--scene", "commute", "--weather", "22°C晴天", "--json"],
            env,
        )
        assert outfit_after_feedback["preference_applied"] is True
        assert "preference_reasons" in outfit_after_feedback
        assert len(outfit_after_feedback["preference_reasons"]) > 0

        # 连续快速生成，确保 outfit_id 不冲突
        outfit_rapid_1 = run_cmd(
            ["outfit", "--scene", "commute", "--weather", "22°C晴天", "--json"],
            env,
        )
        outfit_rapid_2 = run_cmd(
            ["outfit", "--scene", "commute", "--weather", "22°C晴天", "--json"],
            env,
        )
        assert outfit_rapid_1["outfit_id"] != outfit_rapid_2["outfit_id"]

    print("OK")


if __name__ == "__main__":
    main()
