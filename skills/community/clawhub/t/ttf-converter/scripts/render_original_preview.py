from PIL import Image, ImageDraw, ImageFont
import os
import sys

TEST_LINES = [
    '原始横版测试',
    '中文正文：天地玄黄 宇宙洪荒 日月盈昃 辰宿列张',
    '数字字母：ABC abc 1234567890',
    '单点标点：，。；：？！,.;:?!',
    '书名号引号：《测试》〈样例〉「引号」『双引号』“弯引号”‘单引号’',
    '括号：() [] {} （）［］｛｝〔〕【】',
    '破折号省略号：— —— … ……',
    '混排：春眠不觉晓，ABC123；处处闻啼鸟。',
]


def main(font_path: str, out_path: str):
    title = f"{os.path.splitext(os.path.basename(font_path))[0]} 原始横版测试"
    width, height = 1800, 2200
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    ft_title = ImageFont.truetype(font_path, 72)
    ft_body = ImageFont.truetype(font_path, 54)

    y = 70
    for i, line in enumerate([title] + TEST_LINES[1:]):
        font = ft_title if i == 0 else ft_body
        draw.text((60, y), line, font=font, fill='black')
        y += 145 if i == 0 else 165

    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    img.save(out_path)
    print(out_path)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python render_original_preview.py input.ttf output.png')
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2])
