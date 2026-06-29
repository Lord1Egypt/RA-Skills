# FAQ

Q: 生成的峰图为什么有噪声？
A: 噪声是模拟真实检测器响应的加法性高斯噪声，噪声水平由 noise_level 参数控制。降低该值可减少噪声。

Q: 两个峰距离很近时为什么看起来像一个？
A: 当两个峰的中心距离小于约 2×HWHM 时，高斯拖尾互相覆盖，合成信号表现为单峰或肩峰。这是色谱分离度不够的物理表现，用 cluster 或 merged 类型可控制标注行为。

Q: 标注为什么会重叠？如何解决？
A: 相邻峰高度相近时标注会发生重叠。系统碰撞避让算法自动处理：按空间分组（1 min 内），组内按峰高双向均摊，offset 从基准 300 上下分布，最小间距 70，最低 offset 80。用户也可对特定峰配置 annotate: false 跳过标注，或改用融峰(merged)类型减少标注数量。

Q: 扫描速率和总点数是什么关系？
A: 总点数 = 时间范围 × 扫描速率。例如 scan_rate=150、时长 10 min → 1500 点。

Q: CSV 导出数据中小数位不一致是怎么回事？
A: 数据存储为 6 位小数的浮点数，显示精度取决于查看工具。

Q: 负峰怎么配置？支持哪些场景？
A: 将峰的 height 设为负数即可生成倒峰，适用于模拟色谱溶剂峰倒置、检测器极性反转等场景。Y 轴自动缩放包含负区间，标注自动反向指向下方，不会掉到峰下面（最低 offset=80 硬约束）。簇峰和融峰均支持全负子峰的配置。

Q: 出错或参数非法怎么办？
A: 检查 JSON 格式是否合法，确保 RT/height/HWHM 为正数（负峰 height 可负）。扫描速率建议 ≥ 50 pts/min。

Q: 能否在 Python 代码中直接调用？
A: 可以。通过 import 方式调用核心函数：
```python
import sys
sys.path.append("skills/simulated-peak-plot/scripts")
from generate_peak import gaussian_peak, generate_composite_peak
import numpy as np
t = np.linspace(0, 10, 1000)
signal = gaussian_peak(t, 5.0, 800, 0.08)
```

Q: 不同类型的峰（单峰/簇峰/融峰）能否混合使用？
A: 可以。在 peaks 数组中任意排列单峰、簇峰和融峰即可，标注算法自动适配类型。

Q: 一次最多能生成多少个峰？超大数据量时怎么办？
A: 单次配置支持的峰组数量无硬上限，但建议不超过 20 组（含子峰）。扫描速率建议 50~500 pts/min，过低信号锯齿明显，过高文件体积增大。总点数超过 50000 时建议降低扫描速率或缩短时间窗口。

Q: 能否只生成数据不画图？
A: 可以。脚本运行后数据保存在 CSV 文件中（export_csv: true）；也可以在代码中调用 gaussian_peak() 和 generate_composite_peak() 直接获取信号数组。