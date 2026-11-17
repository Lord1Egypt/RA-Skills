#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《小红书赛道深度分析主表》骨架（Markdown）。

用法:
  python3 scaffold_table.py "<品类名>" [输出路径]
  python3 scaffold_table.py --help

若不指定输出路径，则直接打印到标准输出。
生成后可用 scripts/finalize_report.py 做完整性自检并生成决策简报。

退出码: 0 = 成功; 2 = 用法错误（品类名为空 / 参数不合法）。
"""
import sys
import datetime
import os

USAGE = """用法:
  python3 scaffold_table.py "<品类名>" [输出路径]
  python3 scaffold_table.py --help

示例:
  python3 scaffold_table.py "熟龄抗老"                  # 打印到标准输出
  python3 scaffold_table.py "熟龄抗老" 赛道分析主表.md   # 写入指定文件
  python3 scaffold_table.py "熟龄抗老" ./output          # 目录自动补文件名

说明:
  品类名不能为空。输出路径若为已存在目录，会自动补文件名「赛道分析主表.md」。
  生成后可用 scripts/finalize_report.py 做完整性自检并生成决策简报。"""


def die(msg):
    print(f"错误: {msg}", file=sys.stderr)
    print("提示: 运行 python3 scaffold_table.py --help 查看用法。", file=sys.stderr)
    sys.exit(2)


def build(category: str) -> str:
    today = datetime.date.today().isoformat()
    return f"""# 小红书赛道深度分析主表 · {category}
生成日期: {today}
> 采集时间距本表生成 > 90 天的内容须标"需复核"；重投放品类须标注商业化浓度并打折解读。

## 一、研究任务与三问
- 这次最想看懂什么:
- 品牌最后要做出什么选择:
- 结论交给谁使用:
- 采集时间窗口（起止，> 90 天须标"需复核"）:

## 二、关键词四分组（含意图标注）
| 分组 | 关键词 | 意图阶段（发现/了解/比较/决策） | 对应问题 |
| --- | --- | --- | --- |
| 人群与阶段 |  |  | 谁有需求 |
| 问题与效果 |  |  | 哪里不满意 |
| 产品与选择 |  |  | 在找什么 |
| 达人关联 |  |  | 达人能否自然参与 |

## 三、采集记录（每轮一行）
| 轮次 | 关键词 | 排序角度 | 展示位置 | 去重后笔记 | 来源(搜索/达人主页) | 采集时间 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |

## 四、重点笔记与达人（合并去重，保留出处）
| 笔记/达人 | 出现关键词(保留全部) | 意图阶段 | 来源(本人/第三方) | 商业化浓度(自然/疑似投放/合作) | 发布时长/长尾信号 | 正文要点 | 素材 | 评论要点 | 关键判断 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 五、评论行为归类
| 内容 | 向往状态 | 追问选择 | 确认效果/风险 | 比较产品 | 评论者类型(真实/疑似营销) | 自来水信号 | 购买意图层(好奇/考虑/决策) | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 六、关键判断与下一步
- 用户在问什么:
- 平台内容怎样回答:
- 谁来讲 / 谁最可信（按角色生态位：种草/测评/专家/官方）:
- 供给结构（集中度 / 生态位分布 / 意图阶段覆盖 / 饱和或缺口）:
- 品类风险扫描（功效宣称违规密度 / 政策敏感 / 商业化扭曲度）:
- 下一步建议:

## 七、证据边界（必填）
- 样本量 / 覆盖:
- 不能下结论的部分:
- 需品牌自有数据验证的:

## 八、决策结论（必填，分析须收敛到投决）
- 投决建议: GO / NO-GO / 条件GO（附条件）:
- 找谁讲: 推荐达人类型与各自信问题边界（种草型讲状态/测评型给证据/专家型讲原理/官方型背书）:
- 讲什么角度: 状态/成分/实测/怎么选/值不值/进入日常生活:
- 进入策略: 主攻意图阶段 + 主打人群 + 内容矩阵形态:
- 证据边界内置信度: 高/中/低:

---

> 由擎漫网络 | Qomob.AI旗下小红书赛道深度分析引擎 v3.0.0提供支持
"""


def main():
    args = sys.argv[1:]
    if args and args[0] in ("--help", "-h"):
        print(USAGE)
        sys.exit(0)

    if not args:
        die("缺少品类名参数。用法: python3 scaffold_table.py \"<品类名>\" [输出路径]")

    category = args[0].strip()
    if not category:
        die("品类名不能为空。")

    out_path = args[1] if len(args) > 1 else None

    md = build(category)
    if out_path:
        if os.path.isdir(out_path):
            out_path = os.path.join(out_path, "赛道分析主表.md")
        parent = os.path.dirname(os.path.abspath(out_path))
        if not os.path.isdir(parent):
            die(f"输出目录不存在: {parent}")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(md)
        except OSError as e:
            die(f"写入失败: {e}")
        print(f"已生成主表骨架: {out_path}")
        print("提示: 填写完成后，用 scripts/finalize_report.py 自检并生成决策简报。")
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
