#!/usr/bin/env python3
"""URL Slug Generator - 将文本转换为SEO友好的URL别名"""
import sys
import json
import re
import unicodedata

PINYIN_MAP = {
    '的':'de','一':'yi','是':'shi','了':'le','在':'zai','不':'bu','有':'you',
    '人':'ren','这':'zhe','中':'zhong','大':'da','为':'wei','上':'shang',
    '个':'ge','国':'guo','我':'wo','以':'yi','要':'yao','他':'ta','时':'shi',
    '来':'lai','用':'yong','们':'men','生':'sheng','到':'dao','作':'zuo',
    '地':'di','于':'yu','出':'chu','就':'jiu','分':'fen','对':'dui','成':'cheng',
    '会':'hui','可':'ke','主':'zhu','发':'fa','年':'nian','动':'dong','同':'tong',
    '工':'gong','也':'ye','能':'neng','下':'xia','过':'guo','子':'zi','说':'shuo',
    '产':'chan','种':'zhong','面':'mian','而':'er','方':'fang','后':'hou','多':'duo',
    '定':'ding','行':'xing','学':'xue','所':'suo','民':'min','得':'de','经':'jing',
    '十':'shi','三':'san','之':'zhi','进':'jin','着':'zhe','等':'deng','部':'bu',
    '度':'du','家':'jia','里':'li','新':'xin','力':'li','请':'qing','联':'lian',
    '合':'he','机':'ji','无':'wu','心':'xin','量':'liang','么':'me','事':'shi',
    '知':'zhi','间':'jian','去':'qu','什':'shen','么':'me','还':'hai','天':'tian',
    '日':'ri','本':'ben','月':'yue','年':'nian','好':'hao','小':'xiao','伙':'huo',
    '伴':'ban','你':'ni','好':'hao','世':'shi','界':'jie','北':'bei','京':'jing',
    '上':'shang','海':'hai','深':'shen','圳':'zhen','广':'guang','州':'zhou',
    '杭':'hang','州':'zhou','成':'cheng','都':'dou','重':'chong','庆':'qing',
    '天':'tian','津':'jin','南':'nan','京':'jing','西':'xi','安':'an','武':'wu',
    '汉':'han','长':'chang','沙':'sha','数':'shu','据':'ju','科':'ke','技':'ji',
    '开':'kai','发':'fa','产':'chan','品':'pin','中':'zhong','文':'wen','英':'ying',
    '文':'wen','学':'xue','习':'xi','生':'sheng','活':'huo','工':'gong','作':'zuo',
}

def to_pinyin(text):
    result = []
    for char in text:
        if char in PINYIN_MAP:
            result.append(PINYIN_MAP[char])
        elif char.isascii():
            result.append(char.lower())
        elif char == ' ' or char == '-':
            result.append('-')
    return ''.join(result)

def make_slug(text, separator='-', uppercase=False):
    """将文本转换为URL友好的slug"""
    # Unicode正规化
    text = unicodedata.normalize('NFKD', text)
    
    # 中文转拼音
    if re.search(r'[\u4e00-\u9fff]', text):
        text = to_pinyin(text)
    
    # 移除非ASCII字母/数字/连字符/下划线
    slug = re.sub(r'[^a-zA-Z0-9\-_ ]', '', text)
    
    # 替换空格和下划线为指定分隔符
    slug = re.sub(r'[\s_]+', separator, slug)
    
    # 合并连续分隔符
    slug = re.sub(rf'{re.escape(separator)}+', separator, slug)
    
    # 去除首尾分隔符
    slug = slug.strip(separator)
    
    # 转为小写
    slug = slug.lower()
    
    if uppercase == 'upper':
        slug = slug.upper()
    elif uppercase == 'title':
        slug = separator.join(word.capitalize() for word in slug.split(separator))
    
    return slug

def main():
    args = sys.argv[1:]
    separator = '-'
    uppercase = False
    
    if '--separator' in args:
        idx = args.index('--separator')
        separator = args[idx + 1] if idx + 1 < len(args) else '_'
        args = args[:idx] + args[idx+2:]
    
    if '--upper' in args:
        uppercase = 'upper'
        args = [a for a in args if a != '--upper']
    elif '--title' in args:
        uppercase = 'title'
        args = [a for a in args if a != '--title']
    
    text = ' '.join(args)
    
    if not text:
        print(json.dumps({
            "usage": "slug.py <文本> [--separator <字符>] [--upper] [--title]",
            "examples": [
                "slug.py 'Hello World'",
                "slug.py '这是一个测试'",
                "slug.py 'Hello World' --separator _",
                "slug.py 'hello-world' --title"
            ]
        }, ensure_ascii=False, indent=2))
        return
    
    slug = make_slug(text, separator, uppercase)
    print(json.dumps({
        "input": text,
        "slug": slug,
        "separator": separator
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
