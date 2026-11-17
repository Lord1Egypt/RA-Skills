# 参考文献多格式模板与示例

供 SKILL.md 引用的详细格式规范与各类文献示例。

## 一、GB/T 7714-2015 顺序编码制

### 通用结构

```
[序号] 作者. 题名[文献类型标识]. 出版项.
```

文献类型标识：专著[M]、期刊[J]、学位论文[D]、会议论文[C]、报纸[N]、报告[R]、标准[S]、专利[P]、电子资源[EB/OL]、数据库[DB/OL]、计算机程序[CP/OL]。

### 各类型示例

**期刊论文 [J]**
```
[1] 张三, 李四, 王五, 等. 基于深度学习的图像识别方法[J]. 计算机学报, 2023, 46(3): 512-525.
[2] Smith J K, Doe A, Brown C, et al. A novel approach to image recognition[J]. IEEE Transactions on PAMI, 2023, 45(2): 100-120.
```

**图书 / 专著 [M]**
```
[3] 王五. 机器学习导论[M]. 2版. 北京: 清华大学出版社, 2022.
[4] Goodfellow I, Bengio Y, Courville A. Deep learning[M]. Cambridge: MIT Press, 2016.
```

**学位论文 [D]**
```
[5] 赵六. 面向XXX的关键技术研究[D]. 北京: 清华大学, 2021.
```

**会议论文 [C]**
```
[6] Smith J K, Doe A. A novel approach to XXX[C]//Proceedings of ICML. 2023: 100-108.
```

**论文集章节 [M]//**
```
[7] 李四. 章节题名[M]//张三. 论文集名. 北京: 科学出版社, 2022: 88-95.
```

**标准 [S]**
```
[8] GB/T 7714-2015, 信息与文献 参考文献著录规则[S].
```

**专利 [P]**
```
[9] 张三. 一种XXX方法: 中国, ZL202310001234.5[P]. 2023-06-01.
```

**报告 [R]**
```
[10] 某机构. 2024年中国AI发展报告[R]. 北京: 某机构, 2024.
```

**电子资源 [EB/OL]**
```
[11] 中国知网. 中国学术文献网络出版总库[EB/OL]. (2024-01-01)[2024-06-01]. https://www.cnki.net.
```

**报纸 [N]**
```
[12] 张三. AI技术新突破[N]. 人民日报, 2024-06-01(05).
```

### 规则要点

- 作者：三人以内全列；超过三人列前三后加「, 等」(中) 或「, et al.」(英)
- 中文作者不倒置；英文作者姓在前、名缩写在后（Smith J K）
- 作者间用「,」；最后作者前不加「和/and」
- 卷期：`46(3): 512-525`
- 版次非第1版时需注明（如 `2版.`）
- 顺序编码按正文首次引用顺序编号

## 二、APA 第 7 版

### 通用结构

```
Author, A. A., & Author, B. B. (Year). Title. Source, volume(issue), pages. https://doi.org/xxx
```

### 各类型示例

**期刊论文**
```
张三, 李四, & 王五. (2023). 基于深度学习的图像识别方法. 计算机学报, 46(3), 512-525.
Smith, J. K., Doe, A., & Brown, C. (2023). A novel approach to image recognition. IEEE Transactions on PAMI, 45(2), 100-120. https://doi.org/10.1109/TPAMI.2023.001
```

**图书**
```
王五. (2022). 机器学习导论 (2nd ed.). 清华大学出版社.
Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning. MIT Press.
```

**学位论文**
```
赵六. (2021). 面向XXX的关键技术研究 [Doctoral dissertation, 清华大学]. 清华大学.
```

**会议论文**
```
Smith, J. K., & Doe, A. (2023). A novel approach to XXX. Proceedings of ICML, 100-108. https://doi.org/10.1109/XXX.2023.001
```

**电子资源**
```
中国知网. (2024, 1月1日). 中国学术文献网络出版总库. https://www.cnki.net
```

### 规则要点

- 作者姓全拼、名缩写（首字母）；作者间用「,」最后用「&」
- 21 人内全列；超 21 人列前 19 + … + 末位作者
- 文献列表按第一作者姓字母序排列
- 期刊名、书名斜体；卷号斜体，期号不斜体
- 文章题名仅首词首字母大写；期刊名、书名实词首字母大写
- DOI 写成 `https://doi.org/10.xxx`

## 三、MLA 第 9 版

### 通用结构

```
Author. "Title of Source." Title of Container, Contributor, Version, Number,
Publisher, Publication Date, Location.
```

### 各类型示例

**期刊论文**
```
张三, 李四, and 王五. "基于深度学习的图像识别方法." 计算机学报, vol. 46, no. 3, 2023, pp. 512-25.
Smith, John K., et al. "A Novel Approach to Image Recognition." IEEE Transactions on PAMI, vol. 45, no. 2, 2023, pp. 100-20.
```

**图书**
```
王五. 机器学习导论. 2nd ed., 清华大学出版社, 2022.
Goodfellow, Ian, et al. Deep Learning. MIT Press, 2016.
```

**学位论文**
```
赵六. "面向XXX的关键技术研究." 2021. 清华大学, Doctoral dissertation.
```

**会议论文**
```
Smith, John K., and Alice Doe. "A Novel Approach to XXX." Proceedings of ICML, 2023, pp. 100-08.
```

**电子资源**
```
中国知网. "中国学术文献网络出版总库." 2024, www.cnki.net.
```

### 规则要点

- 作者：姓在前、名在后（Full last, First）；三人以上用「et al.」
- 书名、期刊名斜体；文章题名加双引号
- 页码写法：`pp. 512-25`（省略重复数字）
- 含 DOI 或 URL；MLA 9 倾向含 DOI
- 文献列表按第一作者姓字母序排列

## 四、多格式快速对照

| 要素 | GB/T 7714 | APA 7 | MLA 9 |
|------|-----------|-------|-------|
| 作者连接 | `,` | 最后用 `&` | 最后用 `and` |
| 多作者截断 | 3人后 `等/et al.` | 21人后 `…+末位` | 3人后 `et al.` |
| 英文姓名 | 姓+名缩写 (Smith J K) | 姓+名缩写 (Smith, J. K.) | 姓全拼+名 (Smith, John K.) |
| 期刊名斜体 | 否 | 是 | 是 |
| 卷期 | `46(3): 512-525` | `46(3), 512-525` | `vol. 46, no. 3, pp. 512-25` |
| 排序 | 正文引用顺序 | 字母序 | 字母序 |
| DOI | 可选 | `https://doi.org/xxx` | 可选 URL |

## 五、字段缺失占位规范

缺字段时统一用占位标记，不编造：

| 缺失字段 | 占位写法 |
|----------|----------|
| 年份 | `[年份待补]` 或用 `n.d.` (APA) / `n.d.` (MLA) |
| 卷期页 | `[卷期页待补]` |
| 出版社 | `[出版社待补]` |
| DOI | 省略或 `[DOI待补]` |
| 会议名 | `[会议名待补]` |
