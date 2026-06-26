#!/usr/bin/env python3
"""
使用示例：用 word-track-changes 升级真实报告
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from track_changes import TrackChangesProcessor

INPUT_DOC = "/tmp/report_original.docx"
OUTPUT_DOC = "/tmp/report_upgraded_example.docx"


def main():
    print("=== Word Track Changes - 升级示例 ===\n")
    
    p = TrackChangesProcessor(INPUT_DOC)
    p.set_author("大宝")
    
    # 1. 替换销量数据（跨多个 <w:t> 节点）
    print("1. 替换销量数据...")
    p.replace_text_with_revision(
        old_text="根据SNE Research的数据，2023年中国燃料电池汽车销量为5791辆，同比增长72%，而同期韩国、日本、欧洲等主要市场销量均出现大幅下滑，其中韩国销量为4631辆，同比下降55.2%，日本销量仅为422辆，同比下降50.2%。",
        new_text="根据中国汽车工业协会数据，2025年全年全国燃料电池汽车产销分别为7655辆和7797辆；据高工氢电产业研究所（GGII）统计，2025年国内燃料电池汽车上牌销量首次突破一万辆，达到10760辆，同比大涨51.6%。"
    )
    
    # 2. 更新成本数据（短文本，但同样跨节点）
    print("2. 更新成本数据...")
    p.replace_text_with_revision(
        old_text="系统成本低于每千瓦2000元",
        new_text="系统成本低于每千瓦2000元；据高工氢电了解，2025年个别企业系统成本已接近1000元/kW，电堆及膜电极目标售价分别约为600元/kW与300元/kW"
    )
    
    # 3. 在段落后插入新内容
    print("3. 插入2025年企业动态...")
    p.insert_paragraph_after(
        search_text="接近纯电动驱动系统水平。",
        new_text="2025年上半年，亿华通、国鸿氢能、国富氢能、重塑能源等头部企业陆续发布中期业绩，呈现分化态势：多数企业实现净利减亏，\"第二曲线\"成效初显，但商业化初期瓶颈仍待突破。"
    )
    
    # 启用修订追踪
    print("4. 启用修订追踪...")
    p.enable_track_changes()
    
    # 保存
    p.save(OUTPUT_DOC)
    p.cleanup()
    
    print(f"\n✓ 完成！输出文件: {OUTPUT_DOC}")
    print("在 Word 中打开后，选择【审阅】→【所有标记】即可查看绿色插入和红色删除线。")


if __name__ == "__main__":
    main()
