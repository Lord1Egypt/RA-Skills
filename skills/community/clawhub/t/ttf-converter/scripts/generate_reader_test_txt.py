import os
import sys

CONTENT = """天地玄黄 宇宙洪荒 日月盈昃 辰宿列张
春眠不觉晓，ABC123；处处闻啼鸟。
ABC abc 1234567890
，。；：？！,.;:?!
《测试》〈样例〉「引号」『双引号』“弯引号”‘单引号’
() [] {} （）［］｛｝〔〕【】
— —— … ……
"""


def main(out_path: str):
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(CONTENT)
    print(out_path)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python generate_reader_test_txt.py output.txt')
        raise SystemExit(1)
    main(sys.argv[1])
