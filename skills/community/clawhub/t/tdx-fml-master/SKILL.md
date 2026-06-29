---
name: "tdx-formula-master"
description: "通达信选股/指标公式大师：金叉放量突破龙头识别，含回测模板板块轮动主力资金分析"
metadata:
  openclaw:
    emoji: "📈"
    version: "2.0.1"
    author: "墨鱼精@g1776933879"
    tags: ["stock", "tdx", "formula", "finance", "china"]
---

# 📈 TDX Formula Master — 通达信公式大师

> **slug**: `tdx-formula-master` | **安装**: `clawhub install @g1776933879/tdx-formula-master`

## 核心能力

通达信（TDX）选股/指标/主图公式专家。覆盖 6 大场景、30+ 模板、含回测框架和板块轮动分析。

---

## 公式基础参考

### 基础行情
| 函数 | 简写 | 含义 |
|------|------|------|
| OPEN | O | 开盘价 |
| HIGH | H | 最高价 |
| LOW | L | 最低价 |
| CLOSE | C | 收盘价 |
| VOL | V | 成交量(手) |
| AMOUNT | AMO | 成交额(元) |

### 常用引用函数
| 函数 | 说明 |
|------|------|
| REF(X,N) | 引用N周期前值 |
| HHV(X,N) / LLV(X,N) | N周期最高/最低 |
| MA(X,N) / EMA(X,N) / SMA(X,N,M) | 移动平均 |
| COUNT(X,N) | N周期满足次数 |
| CROSS(A,B) | A上穿B(金叉) |
| BARSLAST(X) | 上次成立到当前 |
| EVERY(X,N) / EXIST(X,N) | 全部满足/存在 |
| SUM(X,N) | N周期累加 |

### ⚠️ 未来函数（禁止用于选股）
BACKSET / REFX / XMA / ZIG / PEAK / TROUGH / DRAWLINE / PEAKBARS / TROUGHBARS

---

## 6 大场景模板

### 📊 场景一：趋势跟踪

**均线多头排列（强势股）**
```tdx
MA5:=MA(C,5); MA10:=MA(C,10); MA20:=MA(C,20); MA60:=MA(C,60);
MA5>MA10 AND MA10>MA20 AND MA20>MA60 AND EVERY(MA5>MA10,3);
```

**均线金叉选股**
```tdx
MA5:=MA(C,5); MA10:=MA(C,10);
CROSS(MA5,MA10) AND VOL>REF(VOL,1);
```

**MACD金叉+零轴上方**
```tdx
DIF:=EMA(C,12)-EMA(C,26);
DEA:=EMA(DIF,9);
CROSS(DIF,DEA) AND DIF>0 AND DEA>0;
```

**趋势线突破（20日高点突破）**
```tdx
C>REF(HHV(H,20),1) AND V>REF(HHV(V,5),1)*1.2;
```

### 💥 场景二：量价异动

**倍量突破**
```tdx
VOL/REF(VOL,1)>2 AND C>REF(HHV(H,10),1);
```

**底部放量反弹**
```tdx
V>MA(V,5)*2 AND C>REF(C,1) AND LLV(L,20)=L;
```

**量比大于2**
```tdx
DYNAINFO(17)>2;
```

**缩量回踩均线（N字型买点）**
```tdx
MA20:=MA(C,20);
C>MA20 AND V<MA(V,20)*0.6 AND REF(L,1)<MA20 AND C>REF(C,1);
```

### 🏆 场景三：涨停/龙头辨识

**涨停板预警**
```tdx
H>=ZTPRICE(REF(C,1),0.1) AND C=H;
```

**连板识别（2板起步）**
```tdx
EVERY(C>=ZTPRICE(REF(C,1),0.1),2) AND C=H;
```

**板块龙头（突破+涨停）**
```tdx
INBLOCK('新能源') AND C>(HHV(H,20)*0.95) AND C>=ZTPRICE(REF(C,1),0.1);
```

**首板涨停 + 放量突破**
```tdx
涨停:=C>=ZTPRICE(REF(C,1),0.1) AND C=H;
首板:=REF(涨停,1)=0 AND 涨停;
放量突破:=V>REF(HHV(V,20),1)*1.5;
首板 AND 放量突破;
```

### 🔄 场景四：技术指标

**MACD底背离（创新低但DIF不创新低）**
```tdx
DIF:=EMA(C,12)-EMA(C,26);
LOW_NEW:=LLV(L,60)=L;
DIF_LOW:=LLV(DIF,60)=DIF;
LOW_NEW AND REF(DIF_LOW,1)=0 AND DIF_LOW=0;
```

**KDJ超买超卖**
```tdx
HH9:=HHV(H,9); LL9:=LLV(L,9);
RSV:=IF(HH9=LL9,50,(C-LL9)/(HH9-LL9)*100);
K:=SMA(RSV,3,1);
D:=SMA(K,3,1);
J:=3*K-2*D;
超卖: J<20;   {买入信号}
超买: J>80;   {卖出信号}
```

**RSI强势/超卖**
```tdx
RSI1:=SMA(MAX(C-REF(C,1),0),6,1)/SMA(ABS(C-REF(C,1)),6,1)*100;
RSI超卖:CROSS(RSI1,20);    {买入}
RSI超买:CROSS(80,RSI1);    {卖出}
```

**布林带下轨反弹**
```tdx
MID:=MA(C,20);
STD:=STD(C,20);
UPPER:=MID+2*STD;
LOWER:=MID-2*STD;
C<LOWER AND C>REF(C,1);   {触及下轨后反弹}
```

### 💰 场景五：主力资金

**量价背离（缩量上涨/放量下跌）**
```tdx
缩量上涨:C>REF(C,1) AND V<REF(V,1);    {缩量上涨：主力控盘}
放量下跌:C<REF(C,1) AND V>REF(V,1)*1.5;  {放量下跌：主力出货}
```

**筹码获利比例**
```tdx
WINNER(C)*100>60;    {获利盘>60% 处于强势区}
WINNER(C)*100<20;    {获利盘<20% 处于超跌区}
```

**主力净流入估算**
```tdx
外盘:=DYNAINFO(23);
内盘:=DYNAINFO(22);
主力净占比:=(外盘-内盘)/(外盘+内盘)*100;
主力净占比>10;    {主力净流入>10%}
```

### 📋 场景六：财务过滤

**净利润增长+低估值**
```tdx
FINANCE(30)>0 AND C/FINANCE(34)<10 AND C/FINANCE(34)>0;
```

**小市值+高增长**
```tdx
CAPITAL*C/100000000<100 {流通市值<100亿} AND FINANCE(33)>0.5;
```

**绩优白马股**
```tdx
FINANCE(33)>1 {每股收益>1} AND FINANCE(9)<60 {负债率<60%} AND FINANCE(18)>2 {每股公积金>2};
```

---

## 📊 选股组合策略

### 综合强势股
```tdx
MA5:=MA(C,5); MA10:=MA(C,10); MA20:=MA(C,20); MA60:=MA(C,60);
DIF:=EMA(C,12)-EMA(C,26); DEA:=EMA(DIF,9);
均线多头:=MA5>MA10 AND MA10>MA20 AND MA20>MA60;
放量:=V>REF(HHV(V,5),1)*1.2;
MACD多头:=DIF>DEA AND DIF>0;
强势:C>MA5 AND C>REF(C,1) AND DYNAINFO(14)>0;
选股:均线多头 AND 放量 AND MACD多头 AND 强势;
```

### 板块轮动（新能源+）
```tdx
INBLOCK('新能源') AND C>MA(C,20) AND V>REF(V,1)*1.5 AND DYNAINFO(17)>1.5;
```

### 3日阳线反弹
```tdx
阳线:=C>O; 三日连阳:=COUNT(阳线,3)=3;
站上5日:=C>MA(C,5);
选股:三日连阳 AND 站上5日;
```

---

## 🔬 回测框架（人工评估要点）

使用公式前建议评估以下指标：

| 指标 | 评估标准 | 说明 |
|------|---------|------|
| 信号频率 | 月均5-20次 | 太少错过机会，太多假信号 |
| 胜率 | >50% | 历史回测胜率 |
| 盈亏比 | >1.5 | 平均盈利/平均亏损 |
| 最大回撤 | <15% | 连续亏损的最大幅度 |
| 信号稳定性 | 各月信号数持平 | 避免只在特定行情有效 |

---

## 板块分类（常用）

| 分类 | 板块名称 |
|------|---------|
| 🚗 新能源 | 新能源车、锂电池、光伏、风能、储能 |
| 🤖 科技 | 人工智能、芯片、5G、信创、数据要素 |
| 💊 医药 | 创新药、CXO、中药、医疗器械 |
| 🏭 周期 | 煤炭、钢铁、有色、化工 |
| 💳 金融 | 银行、券商、保险、互联网金融 |
| 🛍️ 消费 | 白酒、食品饮料、家电、旅游 |

---

## 使用示例

```
用户: "通达信选股，均线金叉+放量"
→ 生成: MA5:=MA(C,5); MA10:=MA(C,10); CROSS(MA5,MA10) AND VOL>REF(VOL,1);

用户: "写个MACD底背离公式"
→ 输出底背离公式 + 标注无未来函数

用户: "通达信板块龙头识别"
→ INBLOCK('新能源') + 涨停条件 + 放量突破

用户: "帮我加个财务过滤"
→ FINANCE(30)>0 AND C/FINANCE(34)<10
```

## 🛠️ 内置工具脚本

技能包含 `scripts/` 目录下的通达信公式验证工具：

```bash
cd scripts/
node formula-validator.js check "CROSS(MA(C,5),MA(C,10)) AND VOL>REF(VOL,1);"
node formula-validator.js gen "均线金叉放量"
node formula-validator.js gen "macd底背离"
node formula-validator.js list
```

**功能**:
- `check` — 验证公式语法（检测未来函数、括号匹配、分号遗漏）
- `check-file` — 验证文件中的公式
- `gen` — 自然语言生成公式（20+模板）
- `list` — 列出所有公式模板

## 注意事项

- **选股公式严禁未来函数**
- 最后一行无分号 `;` 表示输出，加分号是赋值
- 通达信不区分大小写
- 测试先用 `REF(C,1)` 等无未来函数的实现
- 谨慎使用 `WINNER` / `COST`（基于全量历史数据，不同通达信版本可能差异大）
