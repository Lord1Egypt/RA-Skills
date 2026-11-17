#!/usr/bin/env python3
"""
zhongshan-lesson-plan — 中专教案模板填充脚本

用法:
    python fill_lesson_plan.py \\
        --template 模板文件.docx \\
        --topic "教案主题" \\
        --hours 2 \\
        [--teacher "教师姓名"] \\
        [--class "班级名称"] \\
        [--textbook "教材名称"] \\
        --output 输出文件.docx

示例:
    python fill_lesson_plan.py \\
        --template 中专教案模板.docx \\
        --topic "51单片机的定时器T0工作原理及编程" \\
        --hours 2 \\
        --output 51单片机教案.docx
"""

import argparse
import os
import re
import sys
import zipfile
from lxml import etree

# Word Processing ML 命名空间
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

# 默认值
DEFAULT_TEACHER = '刘某某'
DEFAULT_CLASS = '22级电子信息1班'
DEFAULT_TEXTBOOK = '《模拟电子技术基础》（第5版）'

# 课程名称推断规则
COURSE_INFER_RULES = [
    (r'MOS|MOSFET|NMOS|PMOS|CMOS|半导体|JFET', '模拟电子技术基础'),
    (r'51单片机|定时器|中断|Keil|AT89S51|PWM|单片机', '单片机原理与应用'),
    (r'C语言|指针|数组|结构体|链表|C\+\+', 'C程序设计'),
    (r'数字电路|逻辑门|触发器|Karnaugh|布尔|卡诺', '数字电子技术基础'),
    (r'传感器|ADC|DAC|滤波|运算放大器|运放', '传感器与检测技术'),
    (r'自动控制|PID|传递函数|频域|根轨迹|控制', '自动控制原理'),
    (r'通信原理|调制解调|香农|信道编码|通信', '通信原理'),
    (r'微机原理|汇编|总线|接口|8086', '微机原理与接口技术'),
    (r'信号与系统|傅里叶|拉普拉斯|Z变换|频谱', '信号与系统'),
    (r'电机|变压器|电力电子|逆变器|整流', '电力电子技术'),
    (r'PLC|梯形图|步进电机|伺服|可编程', 'PLC应用技术'),
    (r'PCB|Altium|布线|封装|EDA', 'EDA技术与PCB设计'),
    (r'嵌入式|Linux|ARM|RTOS|STM32|RISC-V', '嵌入式系统设计'),
    (r'无线|WIFI|BLE|LoRa|NB-IoT|物联网|IoT', '物联网技术概论'),
    (r'人工智能|深度学习|神经网络|卷积|Transformer', '人工智能基础'),
    (r'数据库|SQL|ER图|事务|索引|关系代数', '数据库原理与应用'),
    (r'计算机网络|TCP/IP|OSI|路由协议|网络协议', '计算机网络'),
]


def infer_course_name(topic: str) -> str:
    """根据主题关键词推断课程名称。"""
    for pattern, course in COURSE_INFER_RULES:
        if re.search(pattern, topic, re.IGNORECASE):
            return course
    return topic  # 无法推断则直接使用主题


def make_paragraph(text: str, alignment: str = 'left') -> etree._Element:
    """创建带格式的段落元素。

    Args:
        text: 段落文本
        alignment: 对齐方式 ('left', 'center', 'right')

    Returns:
        lxml 段落元素
    """
    p = etree.SubElement(etree.Element('dummy'), W + 'p')
    pPr = etree.SubElement(p, W + 'pPr')

    # 对齐方式
    jc = etree.SubElement(pPr, W + 'jc')
    jc.set(W + 'val', alignment)

    # 行间距
    sp = etree.SubElement(pPr, W + 'spacing')
    sp.set(W + 'before', '20')
    sp.set(W + 'after', '20')
    sp.set(W + 'line', '320')
    sp.set(W + 'lineRule', 'auto')

    # 运行（Run）
    r = etree.SubElement(p, W + 'r')
    rPr = etree.SubElement(r, W + 'rPr')

    # 字体设置
    rf = etree.SubElement(rPr, W + 'rFonts')
    rf.set(W + 'ascii', '宋体')
    rf.set(W + 'hAnsi', '宋体')
    rf.set(W + 'eastAsia', '宋体')

    # 字号（21 = 10.5pt）
    sz = etree.SubElement(rPr, W + 'sz')
    sz.set(W + 'val', '21')
    szCs = etree.SubElement(rPr, W + 'szCs')
    szCs.set(W + 'val', '21')

    # 文本内容
    t = etree.SubElement(r, W + 't')
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return p


def fill_cell(cell: etree._Element, content, alignment: str = 'left'):
    """填充单元格内容。

    Args:
        cell: lxml 单元格元素
        content: 字符串或多段落列表
        alignment: 对齐方式
    """
    # 清除旧段落
    for p in cell.findall(W + 'p'):
        cell.remove(p)

    if isinstance(content, str):
        if content.strip():
            cell.append(make_paragraph(content, alignment))
    elif isinstance(content, list):
        for line in content:
            if line.strip():
                cell.append(make_paragraph(line, alignment))


def analyze_template(template_path: str) -> dict:
    """分析模板的表格结构。

    Returns:
        包含行信息、单元格数的字典
    """
    with zipfile.ZipFile(template_path, 'r') as z:
        doc_xml = z.read('word/document.xml')
    root = etree.fromstring(doc_xml)
    body = root.find(W + 'body')
    tbl = body.find(W + 'tbl')
    rows = tbl.findall(W + 'tr')

    structure = []
    for ri, row in enumerate(rows):
        cells = row.findall(W + 'tc')
        row_info = {
            'index': ri,
            'row_number': ri + 1,
            'cell_count': len(cells),
            'cells': []
        }
        for ci, cell in enumerate(cells):
            cell_info = {'index': ci}
            tc_pr = cell.find(W + 'tcPr')
            if tc_pr is not None:
                gs = tc_pr.find(W + 'gridSpan')
                if gs is not None:
                    cell_info['grid_span'] = int(gs.get(W + 'val'))
                vm = tc_pr.find(W + 'vMerge')
                if vm is not None:
                    cell_info['v_merge'] = vm.get(W + 'val')
            # 提取文本
            texts = []
            for p in cell.findall(W + 'p'):
                for t in p.findall(W + 't'):
                    if t.text:
                        texts.append(t.text)
            cell_info['text'] = ''.join(texts).strip()
            row_info['cells'].append(cell_info)
        structure.append(row_info)

    return {
        'structure': structure,
        'row_count': len(rows),
        'expected_cells': [r['cell_count'] for r in structure],
    }


def generate_lesson_plan(topic: str, hours: int, teacher: str,
                         class_name: str, textbook: str) -> dict:
    """生成教案内容映射。

    Returns:
        content_map: {(row_index, cell_index): content}
    """
    course_name = infer_course_name(topic)
    content_map = {}

    # 基本信息
    content_map[(0, 1)] = teacher          # 授课教师
    content_map[(0, 3)] = course_name      # 课程名称
    content_map[(1, 1)] = textbook         # 授课教材
    content_map[(2, 1)] = class_name       # 授课班级
    content_map[(3, 1)] = topic            # 授课内容
    content_map[(3, 3)] = f'{hours}课时'   # 授课时长

    # 知识目标
    content_map[(4, 2)] = [
        f'掌握{topic}的基本原理和核心概念',
        f'理解{topic}的工作机制',
        f'熟悉相关术语和标准定义',
        f'掌握{topic}的基本编程/操作方法',
    ]

    # 能力目标
    content_map[(5, 2)] = [
        f'能够独立完成{topic}的相关编程/操作',
        f'能够分析和解决{topic}中的常见问题',
        f'具备{topic}的实践应用能力',
        f'能够根据需求选择合适的技术方案',
    ]

    # 素质目标
    content_map[(6, 2)] = [
        '培养严谨细致的科学态度',
        '提高逻辑思维和问题分析能力',
        '增强团队协作和沟通表达能力',
        '树立工程实践和质量意识',
    ]

    # 思政元素
    content_map[(7, 1)] = [
        f'通过{topic}的学习，感受我国在相关领域的技术发展成就',
        '培养实事求是的科学态度和工匠精神',
        '树立科技报国的责任感和使命感',
        '增强自主学习能力和终身学习意识',
    ]

    # 重点难点
    content_map[(8, 1)] = [
        '【教学重点】',
        f'1. {topic}的核心概念和原理',
        f'2. {topic}的关键技术和方法',
        f'3. {topic}在实际中的应用场景',
        '',
        '【教学难点】',
        f'1. {topic}中抽象概念的理解',
        f'2. {topic}的实际操作和编程实现',
        f'3. {topic}中常见问题的分析与解决',
    ]

    # 教法学法
    content_map[(9, 1)] = [
        '【教法】',
        '案例教学法、演示法、讲授法、任务驱动法',
        '',
        '【学法】',
        '自主探究法、合作学习法、实践操作法、归纳总结法',
    ]

    # 教学环节（R13，索引12）
    content_map[(12, 0)] = [
        f'【环节一】导入新课（{max(5, int(hours*60*0.05))}分钟）',
        f'通过生活实例引入{topic}的概念，激发学习兴趣',
        '',
        f'【环节二】知识讲授（{max(20, int(hours*60*0.3))}分钟）',
        f'1. 详细讲解{topic}的基本原理',
        f'2. 结合图示和案例分析',
        f'3. 强调重点和易错点',
        '',
        f'【环节三】实例演示（{max(10, int(hours*60*0.15))}分钟）',
        f'1. 教师现场演示{topic}的操作/编程过程',
        f'2. 逐步讲解关键步骤',
        f'3. 展示常见错误及解决方法',
        '',
        f'【环节四】课堂练习（{max(15, int(hours*60*0.2))}分钟）',
        f'1. 学生独立完成{topic}相关练习',
        f'2. 教师巡回指导',
        f'3. 小组讨论与互助',
        '',
        f'【环节五】课堂小结（{max(5, int(hours*60*0.05))}分钟）',
        f'1. 回顾{topic}的核心知识点',
        f'2. 总结学习方法',
        f'3. 布置课后作业',
    ]
    content_map[(12, 1)] = [
        '展示案例，提问引导',
        'PPT讲解，板书演示',
        'IDE实时演示，逐步讲解',
        '布置任务，巡回指导',
        '总结归纳，点评作业',
    ]
    content_map[(12, 2)] = [
        '观看案例，思考问题',
        '听讲、记录、提问',
        '跟随演示，同步操作',
        '独立完成练习，小组讨论',
        '回顾总结，整理笔记',
    ]

    # 课后作业
    content_map[(13, 1)] = [
        '1. 完成教材相关章节习题',
        f'2. 编写与{topic}相关的编程/操作练习',
        '3. 预习下一节课内容',
    ]
    content_map[(13, 3)] = [
        '课堂表现（20%）+ 编程练习（40%）+ 小组合作（20%）+ 课后作业（20%）',
    ]

    # 教学反思
    content_map[(14, 1)] = [
        f'【教学效果预期】',
        f'1. 90%以上学生能掌握{topic}的基本概念',
        '2. 85%以上学生能独立完成相关实践操作',
        '',
        f'【可能存在的问题】',
        f'1. {topic}的部分概念较为抽象，学生理解可能有困难',
        '2. 课堂练习时间可能不足',
        '',
        f'【改进措施】',
        '1. 增加可视化辅助工具',
        '2. 适当延长实践环节时间',
        '3. 提供课后辅导资料',
    ]

    return content_map


def fill_template(template_path: str, content_map: dict, output_path: str):
    """将教案内容填充到模板中。

    Args:
        template_path: 模板文件路径
        content_map: 内容映射字典
        output_path: 输出文件路径
    """
    with zipfile.ZipFile(template_path, 'r') as zin:
        doc_xml = zin.read('word/document.xml')
    root = etree.fromstring(doc_xml)
    body = root.find(W + 'body')
    tbl = body.find(W + 'tbl')
    rows = tbl.findall(W + 'tr')

    filled = skipped = 0
    for (ri, ci), content in content_map.items():
        if ri >= len(rows):
            skipped += 1
            print(f'  ⚠️ 跳过: 行索引 {ri} 超出范围（共{len(rows)}行）')
            continue
        cells = rows[ri].findall(W + 'tc')
        if ci >= len(cells):
            skipped += 1
            print(f'  ⚠️ 跳过: R{ri+1}C{ci+1} 不存在（共{len(cells)}个单元格）')
            continue
        fill_cell(cells[ci], content)
        filled += 1

    # 写回文件
    new_doc_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    if os.path.exists(output_path):
        os.remove(output_path)
    with zipfile.ZipFile(template_path, 'r') as zin:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr(item, new_doc_xml)
                else:
                    zout.writestr(item, zin.read(item.filename))

    print(f'\n✅ 填充完成: {filled} 个单元格已填写, {skipped} 个跳过')
    print(f'📄 输出文件: {output_path}')
    return filled, skipped


def verify_output(output_path: str, expected_rows: int = 15,
                  expected_cells: list = None):
    """验证输出文件的结构完整性。"""
    if expected_cells is None:
        expected_cells = [4, 2, 2, 4, 3, 3, 3, 2, 2, 2, 1, 3, 3, 4, 2]

    with zipfile.ZipFile(output_path, 'r') as z:
        doc_xml = z.read('word/document.xml')
    root = etree.fromstring(doc_xml)
    rows = root.findall('.//' + W + 'tr')

    print('\n🔍 验证结果:')
    all_ok = True

    # 行数
    if len(rows) != expected_rows:
        print(f'  ❌ 行数错误: 期望{expected_rows}, 实际{len(rows)}')
        all_ok = False
    else:
        print(f'  ✅ 行数正确: {len(rows)}')

    # 每行单元格数
    for i, row in enumerate(rows):
        cells = row.findall(W + 'tc')
        if len(cells) != expected_cells[i]:
            print(f'  ❌ R{i+1} 单元格数错误: 期望{expected_cells[i]}, 实际{len(cells)}')
            all_ok = False

    # vMerge
    r5_cells = rows[4].findall(W + 'tc')
    r5_vm = r5_cells[0].find(W + 'tcPr').find(W + 'vMerge') if r5_cells else None
    if r5_vm is not None and r5_vm.get(W + 'val') == 'restart':
        print(f'  ✅ R5 vMerge=restart 正确')
    else:
        print(f'  ❌ R5 vMerge 异常')
        all_ok = False

    r6_cells = rows[5].findall(W + 'tc')
    r6_vm = r6_cells[0].find(W + 'tcPr').find(W + 'vMerge') if r6_cells else None
    if r6_vm is not None and 'val' not in r6_vm.attrib:
        print(f'  ✅ R6 vMerge continue 正确')
    else:
        print(f'  ❌ R6 vMerge 异常')
        all_ok = False

    # 内容检查
    r0_c1 = rows[0].findall(W + 'tc')[1]
    texts = [t.text for t in r0_c1.iter() if etree.QName(t.tag).localname == 't' and t.text]
    if texts and '刘' in ''.join(texts):
        print(f'  ✅ 授课教师字段已填充')

    if all_ok:
        print('\n🎉 所有验证通过！')
    else:
        print('\n⚠️ 部分验证未通过，请检查')

    return all_ok


def main():
    parser = argparse.ArgumentParser(
        description='中专教案模板填充工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --template 模板.docx --topic "51单片机定时器" --hours 2
  %(prog)s --template 模板.docx --topic "C语言数据类型" --hours 4 --teacher "王老师"
        """
    )
    parser.add_argument('--template', '-t', required=True, help='模板文件路径')
    parser.add_argument('--topic', help='教案主题（必填，除非 --analyze）')
    parser.add_argument('--hours', '-H', type=int, default=2, help='课时数（默认2）')
    parser.add_argument('--teacher', default=DEFAULT_TEACHER, help='授课教师（默认: 刘某某）')
    parser.add_argument('--class-name', default=DEFAULT_CLASS, help='授课班级（默认: 22级电子信息1班）')
    parser.add_argument('--textbook', default=DEFAULT_TEXTBOOK, help='授课教材')
    parser.add_argument('--output', '-o', help='输出文件路径（必填，除非 --analyze）')
    parser.add_argument('--analyze', action='store_true', help='仅分析模板结构，不生成教案')
    parser.add_argument('--verify', '-v', help='验证指定输出文件')

    args = parser.parse_args()

    # 验证模板文件存在
    if not os.path.exists(args.template):
        print(f'❌ 模板文件不存在: {args.template}')
        sys.exit(1)

    # --analyze 模式：只需要模板路径
    if args.analyze:
        if not args.topic:
            args.topic = ''
        if not args.output:
            args.output = ''
        print(f'📋 分析模板: {args.template}')
        structure = analyze_template(args.template)
        print(f'   总行数: {structure["row_count"]}')
        print(f'   每行单元格数: {structure["expected_cells"]}')
        for row in structure['structure']:
            parts = []
            for cell in row['cells']:
                text = cell.get('text', '')[:20]
                gs = cell.get('grid_span', '')
                vm = cell.get('v_merge', '')
                parts.append(f'C{cell["index"]+1}(gs={gs},vm={vm})="{text}"')
            print(f'   R{row["row_number"]}: {" | ".join(parts)}')
        return

    if args.verify:
        verify_output(args.verify)
        return

    # 生成教案
    if not args.topic or not args.output:
        print('❌ 请同时提供 --topic 和 --output 参数（或使用 --analyze 仅分析）')
        sys.exit(1)

    print(f'📝 生成教案:')
    print(f'   主题: {args.topic}')
    print(f'   课时: {args.hours}')
    print(f'   教师: {args.teacher}')
    print(f'   班级: {args.class_name}')
    print(f'   教材: {args.textbook}')
    print(f'   课程名: {infer_course_name(args.topic)}')

    content_map = generate_lesson_plan(
        topic=args.topic,
        hours=args.hours,
        teacher=args.teacher,
        class_name=args.class_name,
        textbook=args.textbook,
    )

    fill_template(args.template, content_map, args.output)
    verify_output(args.output)


if __name__ == '__main__':
    main()
