import os
import argparse
import jieba
import numpy as np
from datetime import datetime
from wordcloud import WordCloud
from PIL import Image


def is_png(filename: str):
    if not os.path.exists(filename):
        raise Exception('Mask file does not exist.')

    try:
        with Image.open(filename) as img:
            return img.format == 'PNG'
    except IOError:
        raise Exception('Mask file has some IOError.')


def is_markdown_by_extension(filename: str):
    return filename.endswith('.md')


def extract_text(filename: str):
    if not os.path.exists(filename):
        print('Target file does not exist.')
        return ''
    text = ''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                text = text + f'{line}'
        return text
    except IOError:
        print('Target file has some IOError.')
        return ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_text', type=str, help='text to generate word cloud')
    parser.add_argument('--target_file', type=str, help='file to generate word cloud')
    parser.add_argument('--target_dir', type=str, help='list md file in dir to generate word cloud')
    parser.add_argument('--width', type=int, default=800, help='width of the word cloud picture')
    parser.add_argument('--height', type=int, default=600, help='height of the word cloud picture')
    parser.add_argument('--mask', type=str, help='the sharp of the word cloud，must white background and black sharp')
    parser.add_argument('--max_words', type=int, required=True, help='max words to show in the word cloud')
    parser.add_argument('--font_path', type=str, help='font file path')
    parser.add_argument('--output_dir', type=str, help='output directory ')
    parser.add_argument('--stop_words_file', type=str, help='file path of stop words')

    args = parser.parse_args()

    if args.target_text is None and args.target_file is None and args.target_dir is None:
        raise Exception('Please specify either --target_text or --target_file or --target_dir')

    text = ""

    if args.target_text is not None:
        text = text + f'{args.target_text} '

    if args.target_file is not None:
        if not os.path.exists(args.target_file):
            raise Exception('Target file does not exist.')
        if not is_markdown_by_extension(args.target_file):
            raise Exception('Target file must be a markdown file.')
        text = text + ' '
        text = text + extract_text(args.target_file)

    if args.target_dir is not None:
        if not os.path.exists(args.target_dir):
            raise Exception('Target dir does not exist.')
        for root, dirs, files in os.walk(args.target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if not is_markdown_by_extension(file_path):
                    continue
                text = text + ' '
                text = text + extract_text(file_path)

    if text.strip() == '':
        raise Exception('No text to generate word cloud.')

    # use jieba to cut text
    words = jieba.cut(text)

    # stat word freq
    word_freq = {}
    for word in words:
        if len(word) > 1:
            word_freq[word] = word_freq.get(word, 0) + 1

    # generate text by word and freq
    text_for_wc = " ".join([f"{word} " * freq for word, freq in word_freq.items()])

    # load stop words
    stop_words = []
    if args.stop_words_file is not None:
        if not os.path.exists(args.stop_words_file):
            print('Stop words file does not exist.')
            stop_words = []
        else:
            try:
                with open(args.stop_words_file, 'r', encoding='utf-8') as f:
                    stop_words = {
                        line.strip().lstrip('-').strip()
                        for line in f
                        if line.strip().startswith('-')
                    }
            except FileNotFoundError:
                print('Warning: stopwords.md file not found. Using empty stop words list.')
                stop_words = []
            except IOError as e:
                print(f'Warning: Error reading stopwords.md: {e}. Using empty stop words list.')
                stop_words = []

    my_wordcloud = None

    # mask first
    if args.mask is not None:
        if not is_png(args.mask):
            raise Exception('Mask file must be a PNG file.')

        img = Image.open(args.mask).convert('RGBA')
        mask = np.array(img)

        my_wordcloud = WordCloud(
            font_path=args.font_path,
            mask=mask,
            background_color='white',
            max_words=args.max_words,
            stopwords=stop_words,
            collocations=False
        )
    else:
        my_wordcloud = WordCloud(
            font_path=args.font_path,
            width=args.width,
            height=args.height,
            background_color='white',
            max_words=args.max_words,
            stopwords=stop_words,
            collocations=False
        )

    my_wordcloud.generate(text_for_wc)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    output_file = os.path.join(args.output_dir, f'wordcloud_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')

    my_wordcloud.to_file(output_file)


if __name__ == "__main__":
    main()







