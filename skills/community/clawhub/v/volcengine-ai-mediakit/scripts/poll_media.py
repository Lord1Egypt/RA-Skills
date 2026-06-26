#!/usr/bin/env python3

"""
poll_media.py — 重启媒体类任务轮询

用法:
  python <SKILL_DIR>/scripts/poll_media.py <task_type> <RunId> [space_name]

task_type 取值：
  voiceSeparation / audioNoiseReduction /
  enhanceVideo / videSuperResolution / videoInterlacing /
  portraitImageRetouching / greenScreen / intelligentSlicing /
  subtitlesRemoval / ocr / asr / highlight
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_manage import ApiManage
from vod_common import get_space_name, out, bail

def main():
    if len(sys.argv) < 3:
        bail("用法: python <SKILL_DIR>/scripts/poll_media.py <task_type> <RunId> [space_name]")
    task_type = sys.argv[1]
    run_id    = sys.argv[2]
    api = ApiManage()
    space_name = get_space_name(argv_pos=3)
    result = api.poll_media(task_type, run_id, space_name)
    out(result)

if __name__ == "__main__":
    main()
