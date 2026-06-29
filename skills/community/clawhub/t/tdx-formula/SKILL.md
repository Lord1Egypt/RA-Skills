---
name: "tdx-formula"
description: "通达信选股/指标公式编写助手，基于函数手册快速生成金叉、放量、突破等信号公式。"
---

# TDX Formula — 通达信公式创作技能

通达信（TDX）选股/指标公式编写助手。基于《通达信公式函数完整整理手册》提供的高质量参考资料，快速生成各类公式。

## 参考资料

本技能依赖以下核心知识库，请在使用前加载：

### 基础行情函数
| 函数 | 简写 | 含义 |
|------|------|------|
| OPEN | O | 开盘价 |
| HIGH | H | 最高价 |
| LOW | L | 最低价 |
| CLOSE | C | 收盘价 |
| VOL | V | 成交量（手） |
| AMOUNT | AMO | 成交额（元） |

### 即时行情 DYNAINFO
| 函数 | 含义 |
|------|------|
| DYNAINFO(3) | 前收盘价 |
| DYNAINFO(4) | 开盘价 |
| DYNAINFO(5) | 最高价 |
| DYNAINFO(6) | 最低价 |
| DYNAINFO(7) | 现价 |
| DYNAINFO(8) | 总量 |
| DYNAINFO(9) | 现量 |
| DYNAINFO(10) | 总金额 |
| DYNAINFO(11) | 均价 |
| DYNAINFO(14) | 涨幅 |
| DYNAINFO(17) | 量比 |
| DYNAINFO(22) | 内盘 |
| DYNAINFO(23) | 外盘 |

### 财务数据 FINANCE
| 函数 | 含义 |
|------|------|
| FINANCE(1) | 总股本（股） |
| FINANCE(7) | 流通股本（股） |
| FINANCE(9) | 资产负债率 % |
| FINANCE(18) | 每股公积金 |
| FINANCE(30) | 净利润 |
| FINANCE(33) | 每股收益（全年） |
| FINANCE(34) | 每股净资产 |
| FINANCE(40) | 流通市值 |
| CAPITAL | 当前流通股本（手） |

### 时间函数
DATE / YEAR / MONTH / DAY / WEEKDAY / HOUR / MINUTE / PERIOD

### 引用统计（核心常用）
- **REF(X,N)** — 引用N周期前的X值
- **HHV(X,N)** / **LLV(X,N)** — N周期最高/最低
- **MA(X,N)** — 简单移动平均
- **EMA(X,N)** — 指数移动平均
- **SMA(X,N,M)** — 加权移动平均
- **COUNT(X,N)** — N周期满足条件的次数
- **SUM(X,N)** — N周期累加
- **CROSS(A,B)** — A上穿B（金叉）
- **BARSLAST(X)** — 上次成立到当前周期数
- **EVERY(X,N)** — N周期一直满足
- **EXIST(X,N)** — N周期存在

### 数学运算
ABS / MAX / MIN / SQRT / ROUND / MOD / SIGN
**ZTPRICE(REF(C,1),0.1)** — 涨停价
**DTPRICE(REF(C,1),0.1)** — 跌停价

### 形态函数
| 函数 | 未来函数 | 说明 |
|------|---------|------|
| SAR(N,S,M) | ❌ 否 | 抛物转向止损 |
| WINNER(C) | ❌ 否 | 获利盘比例 |
| COST(N) | ❌ 否 | N%筹码成本 |
| ZIG(K,N) | ⚠️ 是 | 之字转向 |
| PEAK(K,N,M) | ⚠️ 是 | 前M个波峰值 |
| TROUGH(K,N,M) | ⚠️ 是 | 前M个波谷值 |

### 板板块函数
STKNAME / HYBLOCK / GNBLOCK / INBLOCK('板块名') / NAMELIKE('关键词')

### ⚠️ 未来函数清单（慎用）
BACKSET / REFX / XMA / ZIG / PEAK / TROUGH / DRAWLINE / PEAKBARS / TROUGHBARS
> 未来函数会导致信号后移、消失，**不可用于实盘选股和交易决策**。

### 绘图函数（用于指标公式）
STICKLINE(条件,上,下,宽,虚实) —— 画柱线
DRAWICON(条件,位置,图标号) —— 画图标
DRAWTEXT(条件,位置,'文字') —— 标注文字

### 线型颜色修饰
LINETHICK1-5 / STICK / DOTLINE / NODRAW
COLORRED / COLORGREEN / COLORYELLOW / COLORBLUE / COLORWHITE / COLORBLACK

---

## 常用公式模板

### 1. 均线金叉选股
```tdx
MA5:=MA(C,5);
MA10:=MA(C,10);
CROSS(MA5,MA10) AND VOL>REF(VOL,1);
```

### 2. 放量突破选股
```tdx
VOL/REF(VOL,1)>1.5 AND C>REF(HHV(H,20),1);
```

### 3. MACD金叉
```tdx
DIF:=EMA(C,12)-EMA(C,26);
DEA:=EMA(DIF,9);
CROSS(DIF,DEA);
```

### 4. 涨停板预警
```tdx
H>=ZTPRICE(REF(C,1),0.1) AND C=H;
```

### 5. 多头排列选股
```tdx
MA5:=MA(C,5);
MA10:=MA(C,10);
MA20:=MA(C,20);
MA5>MA10 AND MA10>MA20 AND EVERY(MA5>MA10,3);
```

### 6. 底部放量反弹
```tdx
V>MA(V,5)*2 AND C>REF(C,1) AND LLV(L,20)=L;
```

### 7. 量比大于2 选股
```tdx
DYNAINFO(17)>2;
```

### 8. 净利润增长选股（财务过滤）
```tdx
FINANCE(30)>0 AND C/FINANCE(34)<10;
```

### 9. 板块龙头（行业+概念过滤）
```tdx
INBLOCK('新能源') AND C>(HHV(H,20)*0.95);
```

### 10. 筹码获利比例
```tdx
WINNER(C)*100>60;
```

### 11. 均线多头+量能配合（完整指标）
```tdx
MA5:=MA(C,5);
MA10:=MA(C,10);
MA20:=MA(C,20);
MA60:=MA(C,60);
均线多头:=MA5>MA10 AND MA10>MA20 AND MA20>MA60;
放量:=V>REF(HHV(V,5),1)*1.2;
强势:=C>MA5 AND C>REF(C,1) AND DYNAINFO(14)>0;
选股:均线多头 AND 放量 AND 强势;
```

### 12. 三日阳线+站上均线（短期反弹）
```tdx
阳线:=C>O;
三日连阳:=COUNT(阳线,3)=3;
站上5日:=C>MA(C,5);
选股:三日连阳 AND 站上5日;
```

---

## 工作流程

### 用户需求 → 生成公式
1. 倾听用户描述选股/指标需求
2. 拆解为可量化的条件（价格、成交量、均线、财务、时间、板块等）
3. 基于函数手册选择合适的函数
4. 编写公式代码
5. 标注公式类型：**选股公式** / **指标公式**（主图/副图）
6. 标注是否有未来函数并给出风险提示

### 公式检查清单
- [ ] 语法正确（括号匹配、逗号分隔）
- [ ] 赋值语句用 `:=`，输出语句用 `:`
- [ ] 若为选股公式，最后一行有明确输出
- [ ] 变量名不冲突
- [ ] 未来函数已标注 warning

---

## 注意事项

- **选股公式**不要用未来函数（ZIG/PEAK/TROUGH/XMA/BACKSET/REFX）
- **指标公式**可以用绘图函数，但根信号不要依赖未来函数
- 测试先用 `REF(C,1)` 和 `HHV(H,20)` 等无未来函数实现需求
- 通达信公式不区分大小写
- 公式最后一行带分号 `;` 的是赋值语句，不带分号的是输出语句
