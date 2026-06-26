"""
幸福开瓶器 - profile_manager 测试套件
运行: python tests/test_profile_manager.py
"""

import sys
import os
import json
import shutil
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


def test_import():
    try:
        import profile_manager
        return True, "模块导入成功"
    except Exception as e:
        return False, f"模块导入失败: {e}"


def test_get_profile():
    import profile_manager

    tmp = tempfile.mkdtemp(prefix="xingfu_test_")

    try:
        orig_data = profile_manager.DATA_DIR
        orig_profile = profile_manager.PROFILE_FILE
        profile_manager.DATA_DIR = tmp
        profile_manager.PROFILE_FILE = os.path.join(tmp, "user_profile.json")

        profile = profile_manager.get_profile()
        assert isinstance(profile, dict), "返回值应为 dict"

        core_keys = ["constellation", "zodiac", "self_evaluation", "mood_keywords"]
        has_fields = all(k in profile for k in core_keys)
        return has_fields, f"画像读取成功，核心字段完整: {has_fields}"

    except Exception as e:
        return False, f"画像读取失败: {e}"
    finally:
        profile_manager.DATA_DIR = orig_data
        profile_manager.PROFILE_FILE = orig_profile
        shutil.rmtree(tmp, ignore_errors=True)


def test_update_profile():
    import profile_manager

    tmp = tempfile.mkdtemp(prefix="xingfu_test_")

    try:
        orig_data = profile_manager.DATA_DIR
        orig_profile = profile_manager.PROFILE_FILE
        profile_manager.DATA_DIR = tmp
        profile_manager.PROFILE_FILE = os.path.join(tmp, "user_profile.json")

        profile_manager.update_profile("constellation", "天蝎座", confidence="high")
        profile = profile_manager.get_profile()
        return profile["constellation"] == "天蝎座", f"画像更新: constellation={profile.get('constellation')}"

    except Exception as e:
        return False, f"画像更新失败: {e}"
    finally:
        profile_manager.DATA_DIR = orig_data
        profile_manager.PROFILE_FILE = orig_profile
        shutil.rmtree(tmp, ignore_errors=True)


def test_update_confidence():
    import profile_manager

    tmp = tempfile.mkdtemp(prefix="xingfu_test_")

    try:
        orig_data = profile_manager.DATA_DIR
        orig_profile = profile_manager.PROFILE_FILE
        profile_manager.DATA_DIR = tmp
        profile_manager.PROFILE_FILE = os.path.join(tmp, "user_profile.json")

        profile_manager.get_profile()
        before = profile_manager.get_confidence("constellation")

        profile_manager.update_confidence("constellation", 1)
        after = profile_manager.get_confidence("constellation")

        return True, f"置信度更新: {before} → {after}"

    except Exception as e:
        return False, f"置信度更新失败: {e}"
    finally:
        profile_manager.DATA_DIR = orig_data
        profile_manager.PROFILE_FILE = orig_profile
        shutil.rmtree(tmp, ignore_errors=True)


def test_intervention_framework():
    try:
        fpath = os.path.join(
            os.path.dirname(__file__), "..", "scripts", "intervention_framework.json"
        )
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        zones = ["red_zone", "yellow_zone", "green_zone"]
        ok = all(z in data and "trigger_keywords" in data[z] for z in zones)

        red_n = len(data["red_zone"]["trigger_keywords"])
        yellow_n = len(data["yellow_zone"]["trigger_keywords"])
        green_n = len(data["green_zone"]["trigger_keywords"])

        return ok, f"干预框架完整 (红:{red_n} 黄:{yellow_n} 绿:{green_n})"

    except Exception as e:
        return False, f"干预框架加载失败: {e}"


def main():
    tests = [
        ("模块导入", test_import),
        ("画像读取", test_get_profile),
        ("画像更新", test_update_profile),
        ("置信度更新", test_update_confidence),
        ("干预框架", test_intervention_framework),
    ]

    passed = 0
    failed = 0

    print("=" * 50)
    print("幸福开瓶器 - 测试套件")
    print("=" * 50)

    for name, fn in tests:
        try:
            ok, msg = fn()
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] {name}: {msg}")
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1

    print("=" * 50)
    print(f"结果: {passed}/{len(tests)} 通过, {failed} 失败")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)