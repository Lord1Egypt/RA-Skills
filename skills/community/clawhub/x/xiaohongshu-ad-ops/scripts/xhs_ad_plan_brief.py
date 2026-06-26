#!/usr/bin/env python3
import json, re, sys
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore').strip()


def main():
    if len(sys.argv) < 2:
        print('Usage: xhs_ad_plan_brief.py <input.txt>')
        sys.exit(1)
    p = Path(sys.argv[1])
    text = read_text(p)
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    title = lines[0][:32] if lines else '未命名投放项目'
    result = {
        'project': title,
        'goal_guess': '留资 / 私信转化',
        'core_offer_guess': lines[0] if lines else '',
        'suggested_audiences': [
            '痛点明确但尚未行动的人',
            '已经在找解决方案的人',
            '看过同类内容、具备一定认知的人'
        ],
        'creative_angles': [
            '痛点角度',
            '结果角度',
            '案例角度',
            '反常识角度',
            '对比角度'
        ],
        'budget_split_hint': {
            'test_phase': '先小预算测 3-5 个角度',
            'scale_phase': '保留转化率高且线索质量好的组放量'
        },
        'cta_examples': [
            '先私信我，发你一版案例',
            '评论区留“想看”，我发你完整方案',
            '先领取清单，再决定要不要深入聊'
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
