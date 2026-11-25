"""六爻和大六壬的传统文本盘面。"""


def format_liuyao_result(data):
    """格式化六爻起卦结果"""
    result = []

    if data.get('success') is False:
        result.append("起卦失败，请稍后重试")
        return "\n".join(result)

    cast_result = data.get('result', {})
    if not isinstance(cast_result, dict):
        result.append("起卦数据异常")
        return "\n".join(result)

    # 标题
    result.append("")
    result.append("卦象命局")
    result.append("═══════════════════════════════════════════")

    # 本卦 / 变卦
    bengua_full = cast_result.get('benguaming_full', '')
    biangua_full = cast_result.get('bianguaming_full', '')
    guagong = cast_result.get('guagong', '')
    bengua_type = cast_result.get('bengua_type', [])
    biangua_type = cast_result.get('biangua_type', [])

    bengua_label = "本卦：{}".format(bengua_full)
    if guagong:
        bengua_label += "（{}宫）".format(guagong)
    if bengua_type:
        bengua_label += "【{}】".format("、".join(bengua_type))

    biangua_label = "变卦：{}".format(biangua_full)
    if biangua_type:
        biangua_label += "（{}）".format("、".join(biangua_type))

    result.append("")
    result.append("{}　之　{}".format(bengua_label, biangua_label))

    # 起卦时间
    cast_time = cast_result.get('time', '') or data.get('cast_time', '')
    if cast_time:
        result.append("")
        result.append("起卦时间：{}".format(cast_time))

    # 月建、日辰、空亡、卦身
    yuejian = cast_result.get('yuejian', '')
    richen = cast_result.get('richen', '')
    kongwang = cast_result.get('kongwang', '')
    guashen = cast_result.get('guashen', '')
    info_line = []
    if yuejian:
        info_line.append("月建：{}".format(yuejian))
    if richen:
        info_line.append("日辰：{}".format(richen))
    if kongwang:
        info_line.append("空亡：{}".format(kongwang))
    if guashen:
        info_line.append("卦身：{}".format(guashen))
    if info_line:
        result.append("")
        result.append("　".join(info_line))

    # 辅助信息（床帐、香闺）
    chuangzhang = cast_result.get('chuangzhang', [])
    xianggui = cast_result.get('xianggui', [])
    if chuangzhang or xianggui:
        result.append("")
        result.append("辅助信息")
        aux = []
        if chuangzhang:
            aux.append("床帐：{}".format("".join(chuangzhang)))
        if xianggui:
            aux.append("香闺：{}".format("".join(xianggui)))
        result.append("　{}".format("　".join(aux)))

    # 六爻表格（从上爻到初爻）
    result.append("")
    result.append("六神　　本卦（六亲·干支·爻）　　　动　　变卦（六亲·干支·爻）")
    result.append("─────────────────────────────────────────────────────────────")

    def line_symbol(line):
        if line == '⚊':
            return '━━━━━━'
        else:
            return '━━　━━'

    def moving_symbol(origin):
        if not origin.get('is_changed'):
            return '  '
        if origin.get('line') == '⚊':
            return '○'
        else:
            return '×'

    def shi_ying_mark(origin):
        if origin.get('is_subject'):
            return '世'
        if origin.get('is_object'):
            return '应'
        return '  '

    fushen_list = []
    for i in range(6, 0, -1):
        yao = cast_result.get('yao_{}'.format(i), {})
        liushen = yao.get('liushen', '　　')
        origin = yao.get('origin', {})
        variant = yao.get('variant', {})

        o_relative = origin.get('relative', '')
        o_gan = origin.get('gan', '')
        o_zhi = origin.get('zhi', '')
        o_line = line_symbol(origin.get('line', ''))
        shi_ying = shi_ying_mark(origin)
        moving = moving_symbol(origin)

        v_relative = variant.get('relative', '')
        v_gan = variant.get('gan', '')
        v_zhi = variant.get('zhi', '')
        v_line = line_symbol(variant.get('line', ''))

        row = "{liushen}　{o_rel} {o_gan}{o_zhi} {o_line}　{sy}　{mv}　　{v_rel} {v_gan}{v_zhi} {v_line}".format(
            liushen=liushen,
            o_rel=o_relative,
            o_gan=o_gan,
            o_zhi=o_zhi,
            o_line=o_line,
            sy=shi_ying,
            mv=moving,
            v_rel=v_relative,
            v_gan=v_gan,
            v_zhi=v_zhi,
            v_line=v_line
        )
        result.append(row)

        # 收集伏神
        fushen = origin.get('fushen')
        if fushen:
            fushen_list.append("第{}爻伏：{} {}{}".format(
                i, fushen.get('relative', ''), fushen.get('gan', ''), fushen.get('zhi', '')))

    # 伏神
    if fushen_list:
        result.append("")
        result.append("伏神")
        for f in fushen_list:
            result.append("　{}".format(f))

    # 神煞
    shensha = cast_result.get('shensha', [])
    if shensha:
        result.append("")
        result.append("神煞")
        for ss in shensha:
            name = ss.get('name', '')
            zhi = ss.get('zhi', [])
            result.append("　{}：{}".format(name, "、".join(zhi)))

    # 八字
    bazi = cast_result.get('bazi', '')
    if bazi:
        result.append("")
        result.append("八字：{}".format(bazi))

    # 起卦明细
    time_detail = cast_result.get('_time_detail')
    if time_detail and isinstance(time_detail, dict):
        result.append("")
        result.append("起卦明细")
        lunar_caption = time_detail.get('lunar_caption', '')
        if lunar_caption:
            result.append("　农历：{}".format(lunar_caption))
        result.append("　年干支：{}".format(time_detail.get('year_gan_zhi', '')))
        result.append("　时支：{}（序{}）".format(
            time_detail.get('time_zhi', ''), time_detail.get('time_zhi_seq', '')))
        result.append("　上卦：{}（月+日+时={}，mod8={}）".format(
            time_detail.get('upper_gua', ''), time_detail.get('sum_upper', ''), time_detail.get('upper_mod8', '')))
        result.append("　下卦：{}（月+日+时+年={}，mod8={}）".format(
            time_detail.get('lower_gua', ''), time_detail.get('sum_lower', ''), time_detail.get('lower_mod8', '')))
        result.append("　动爻：第{}爻".format(time_detail.get('moving_yao', '')))

    result.append("")
    result.append("💡 请结合用户所问事项，基于卦象进行解读")
    result.append("")
    result.append("🔮 本卦象由 [循古排盘](https://www.xungufa.com) 提供 · 专业古法命理排盘平台")
    return "\n".join(result)

def format_daliuren_result(data):
    """格式化大六壬起课结果（仅显示日课盘）"""
    result = []

    if data.get('status') != 'success':
        result.append("起课失败，请稍后重试")
        return "\n".join(result)

    meta = data.get('meta', {})
    courses = data.get('courses', {})
    ri = courses.get('ri', {})
    if not ri:
        result.append("日课数据缺失")
        return "\n".join(result)

    # 天将简称→全称映射
    jiang_map = {
        '龍': '青龙', '雀': '朱雀', '勾': '勾陈', '蛇': '腾蛇',
        '貴': '贵人', '后': '天后', '陰': '太阴', '玄': '玄武',
        '常': '太常', '虎': '白虎', '空': '天空', '合': '六合'
    }
    def jiang_full(short):
        return jiang_map.get(short, short)

    # 标题
    result.append("")
    result.append("大六壬·日课盘")
    result.append("═══════════════════════════════════════════")

    # 干支 / 月将
    gz_str = meta.get('gz_str', '')
    yuejiang_name = ri.get('yuejiang_name', '')
    yuejiang = ri.get('yuejiang', '')
    result.append("")
    result.append("干支：{}".format(gz_str))
    result.append("月将：{} {}".format(yuejiang_name, yuejiang))

    # 旬空 / 驿马
    xunkong = meta.get('xunkong', '')
    yima = ri.get('yima', '')
    result.append("旬空：{}".format(xunkong))
    result.append("驿马：{}".format(yima))

    # 三传
    chuan = ri.get('chuan', {})
    result.append("")
    result.append("┃ 三传")
    result.append("├───────────────────────────────────")
    for label in ['初傳', '中傳', '末傳']:
        c = chuan.get(label, {})
        liuqin = c.get('liuqin', '')
        gan = c.get('gan', '')
        zhi = c.get('zhi', '')
        jiang = jiang_full(c.get('jiang', ''))
        kong_mark = "（空）" if c.get('kong') else ""
        display_label = label.replace('傳', '传')
        result.append("│ {}　　{}　　{}{}　　{}{}".format(
            display_label, liuqin, gan, zhi, jiang, kong_mark))
    result.append("")

    # 四课（自右向左：四课、三课、二课、一课）
    sike = ri.get('sike', {})
    result.append("┃ 四课（自右向左）")
    result.append("├───────────────────────────────────")
    header = "│ {:^8}{:^8}{:^8}{:^8}".format("四课", "三课", "二课", "一课")
    result.append(header)

    jiang_row = "│ "
    tian_row = "│ "
    di_row = "│ "
    for ke_name in ['四課', '三課', '二課', '一課']:
        ke = sike.get(ke_name, {})
        jiang_row += "{:^8}".format(jiang_full(ke.get('jiang', '')))
        tian_row += "{:^8}".format(ke.get('tian', ''))
        di_row += "{:^8}".format(ke.get('di', ''))
    result.append(jiang_row)
    result.append(tian_row)
    result.append(di_row)
    result.append("")

    # 天地盘（4x4排列）
    grid = ri.get('grid', {})
    result.append("┃ 天地盘")
    result.append("├───────────────────────────────────")
    # 按地支顺序排列: 巳午未申 / 辰(中心)酉 / 卯(中心)戌 / 寅丑子亥
    grid_layout = [
        ['巳', '午', '未', '申'],
        ['辰', None, None, '酉'],
        ['卯', None, None, '戌'],
        ['寅', '丑', '子', '亥']
    ]
    center_label_shown = False
    for row in grid_layout:
        line_jiang = "│ "
        line_tian = "│ "
        line_di = "│ "
        for cell in row:
            if cell is None:
                line_jiang += "{:^10}".format("")
                if not center_label_shown:
                    line_tian += "{:^10}".format("日课")
                    center_label_shown = True
                else:
                    line_tian += "{:^10}".format("")
                line_di += "{:^10}".format("")
            else:
                g = grid.get(cell, {})
                line_jiang += "{:^10}".format(jiang_full(g.get('jiang', '')))
                line_tian += "{:^10}".format(g.get('tian', ''))
                line_di += "{:^10}".format(cell)
        result.append(line_jiang)
        result.append(line_tian)
        result.append(line_di)
        result.append("│")

    # 格局
    geju = ri.get('geju', [])
    if geju:
        result.append("")
        result.append("┃ 格局")
        result.append("├───────────────────────────────────")
        result.append("│ {}".format("　".join(geju)))

    result.append("")
    result.append("💡 请结合用户所问事项，基于课式进行解读")
    result.append("")
    result.append("🔮 本课盘由 [循古排盘](https://www.xungufa.com) 提供 · 专业古法命理排盘平台")
    return "\n".join(result)
