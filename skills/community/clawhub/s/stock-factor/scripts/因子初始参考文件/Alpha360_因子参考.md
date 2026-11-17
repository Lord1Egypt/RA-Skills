# Alpha360 初始参考因子清单（提取自 Qlib 官方源码）

> 来源：`qlib/contrib/data/loader.py` 中 `Alpha360DL.get_feature_config()`，及 `qlib/contrib/data/handler.py` 中 `class Alpha360`。
> Alpha360 为**原始价量数据**（近 60 日 6 字段相对最新值归一），与 Alpha158 的构造特征不同。
> 总因子数：**360**（6 字段 × 60 日）

## 字段分布

| 字段 | 数量 | 说明 |
| --- | --- | --- |
| close | 60 | `CLOSE*` 各日值 / $close 归一 |
| open | 60 | `OPEN*` 各日值 / $close 归一 |
| high | 60 | `HIGH*` 各日值 / $close 归一 |
| low | 60 | `LOW*` 各日值 / $close 归一 |
| vwap | 60 | `VWAP*` 各日值 / $close 归一 |
| volume | 60 | `VOLUME*` 各日值 / ($volume+1e-12) 归一 |

## close 字段因子（CLOSE0 ~ CLOSE59）

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `CLOSE59` | `Ref($close, 59)/$close` | 前59日 close 价格相对最新收盘归一 |
| 2 | `CLOSE58` | `Ref($close, 58)/$close` | 前58日 close 价格相对最新收盘归一 |
| 3 | `CLOSE57` | `Ref($close, 57)/$close` | 前57日 close 价格相对最新收盘归一 |
| 4 | `CLOSE56` | `Ref($close, 56)/$close` | 前56日 close 价格相对最新收盘归一 |
| 5 | `CLOSE55` | `Ref($close, 55)/$close` | 前55日 close 价格相对最新收盘归一 |
| 6 | `CLOSE54` | `Ref($close, 54)/$close` | 前54日 close 价格相对最新收盘归一 |
| 7 | `CLOSE53` | `Ref($close, 53)/$close` | 前53日 close 价格相对最新收盘归一 |
| 8 | `CLOSE52` | `Ref($close, 52)/$close` | 前52日 close 价格相对最新收盘归一 |
| 9 | `CLOSE51` | `Ref($close, 51)/$close` | 前51日 close 价格相对最新收盘归一 |
| 10 | `CLOSE50` | `Ref($close, 50)/$close` | 前50日 close 价格相对最新收盘归一 |
| 11 | `CLOSE49` | `Ref($close, 49)/$close` | 前49日 close 价格相对最新收盘归一 |
| 12 | `CLOSE48` | `Ref($close, 48)/$close` | 前48日 close 价格相对最新收盘归一 |
| 13 | `CLOSE47` | `Ref($close, 47)/$close` | 前47日 close 价格相对最新收盘归一 |
| 14 | `CLOSE46` | `Ref($close, 46)/$close` | 前46日 close 价格相对最新收盘归一 |
| 15 | `CLOSE45` | `Ref($close, 45)/$close` | 前45日 close 价格相对最新收盘归一 |
| 16 | `CLOSE44` | `Ref($close, 44)/$close` | 前44日 close 价格相对最新收盘归一 |
| 17 | `CLOSE43` | `Ref($close, 43)/$close` | 前43日 close 价格相对最新收盘归一 |
| 18 | `CLOSE42` | `Ref($close, 42)/$close` | 前42日 close 价格相对最新收盘归一 |
| 19 | `CLOSE41` | `Ref($close, 41)/$close` | 前41日 close 价格相对最新收盘归一 |
| 20 | `CLOSE40` | `Ref($close, 40)/$close` | 前40日 close 价格相对最新收盘归一 |
| 21 | `CLOSE39` | `Ref($close, 39)/$close` | 前39日 close 价格相对最新收盘归一 |
| 22 | `CLOSE38` | `Ref($close, 38)/$close` | 前38日 close 价格相对最新收盘归一 |
| 23 | `CLOSE37` | `Ref($close, 37)/$close` | 前37日 close 价格相对最新收盘归一 |
| 24 | `CLOSE36` | `Ref($close, 36)/$close` | 前36日 close 价格相对最新收盘归一 |
| 25 | `CLOSE35` | `Ref($close, 35)/$close` | 前35日 close 价格相对最新收盘归一 |
| 26 | `CLOSE34` | `Ref($close, 34)/$close` | 前34日 close 价格相对最新收盘归一 |
| 27 | `CLOSE33` | `Ref($close, 33)/$close` | 前33日 close 价格相对最新收盘归一 |
| 28 | `CLOSE32` | `Ref($close, 32)/$close` | 前32日 close 价格相对最新收盘归一 |
| 29 | `CLOSE31` | `Ref($close, 31)/$close` | 前31日 close 价格相对最新收盘归一 |
| 30 | `CLOSE30` | `Ref($close, 30)/$close` | 前30日 close 价格相对最新收盘归一 |
| 31 | `CLOSE29` | `Ref($close, 29)/$close` | 前29日 close 价格相对最新收盘归一 |
| 32 | `CLOSE28` | `Ref($close, 28)/$close` | 前28日 close 价格相对最新收盘归一 |
| 33 | `CLOSE27` | `Ref($close, 27)/$close` | 前27日 close 价格相对最新收盘归一 |
| 34 | `CLOSE26` | `Ref($close, 26)/$close` | 前26日 close 价格相对最新收盘归一 |
| 35 | `CLOSE25` | `Ref($close, 25)/$close` | 前25日 close 价格相对最新收盘归一 |
| 36 | `CLOSE24` | `Ref($close, 24)/$close` | 前24日 close 价格相对最新收盘归一 |
| 37 | `CLOSE23` | `Ref($close, 23)/$close` | 前23日 close 价格相对最新收盘归一 |
| 38 | `CLOSE22` | `Ref($close, 22)/$close` | 前22日 close 价格相对最新收盘归一 |
| 39 | `CLOSE21` | `Ref($close, 21)/$close` | 前21日 close 价格相对最新收盘归一 |
| 40 | `CLOSE20` | `Ref($close, 20)/$close` | 前20日 close 价格相对最新收盘归一 |
| 41 | `CLOSE19` | `Ref($close, 19)/$close` | 前19日 close 价格相对最新收盘归一 |
| 42 | `CLOSE18` | `Ref($close, 18)/$close` | 前18日 close 价格相对最新收盘归一 |
| 43 | `CLOSE17` | `Ref($close, 17)/$close` | 前17日 close 价格相对最新收盘归一 |
| 44 | `CLOSE16` | `Ref($close, 16)/$close` | 前16日 close 价格相对最新收盘归一 |
| 45 | `CLOSE15` | `Ref($close, 15)/$close` | 前15日 close 价格相对最新收盘归一 |
| 46 | `CLOSE14` | `Ref($close, 14)/$close` | 前14日 close 价格相对最新收盘归一 |
| 47 | `CLOSE13` | `Ref($close, 13)/$close` | 前13日 close 价格相对最新收盘归一 |
| 48 | `CLOSE12` | `Ref($close, 12)/$close` | 前12日 close 价格相对最新收盘归一 |
| 49 | `CLOSE11` | `Ref($close, 11)/$close` | 前11日 close 价格相对最新收盘归一 |
| 50 | `CLOSE10` | `Ref($close, 10)/$close` | 前10日 close 价格相对最新收盘归一 |
| 51 | `CLOSE9` | `Ref($close, 9)/$close` | 前9日 close 价格相对最新收盘归一 |
| 52 | `CLOSE8` | `Ref($close, 8)/$close` | 前8日 close 价格相对最新收盘归一 |
| 53 | `CLOSE7` | `Ref($close, 7)/$close` | 前7日 close 价格相对最新收盘归一 |
| 54 | `CLOSE6` | `Ref($close, 6)/$close` | 前6日 close 价格相对最新收盘归一 |
| 55 | `CLOSE5` | `Ref($close, 5)/$close` | 前5日 close 价格相对最新收盘归一 |
| 56 | `CLOSE4` | `Ref($close, 4)/$close` | 前4日 close 价格相对最新收盘归一 |
| 57 | `CLOSE3` | `Ref($close, 3)/$close` | 前3日 close 价格相对最新收盘归一 |
| 58 | `CLOSE2` | `Ref($close, 2)/$close` | 前2日 close 价格相对最新收盘归一 |
| 59 | `CLOSE1` | `Ref($close, 1)/$close` | 前1日 close 价格相对最新收盘归一 |
| 60 | `CLOSE0` | `$close/$close` | close 当日价格相对最新收盘归一 |

## open 字段因子（OPEN0 ~ OPEN59）

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `OPEN59` | `Ref($open, 59)/$close` | 前59日 open 价格相对最新收盘归一 |
| 2 | `OPEN58` | `Ref($open, 58)/$close` | 前58日 open 价格相对最新收盘归一 |
| 3 | `OPEN57` | `Ref($open, 57)/$close` | 前57日 open 价格相对最新收盘归一 |
| 4 | `OPEN56` | `Ref($open, 56)/$close` | 前56日 open 价格相对最新收盘归一 |
| 5 | `OPEN55` | `Ref($open, 55)/$close` | 前55日 open 价格相对最新收盘归一 |
| 6 | `OPEN54` | `Ref($open, 54)/$close` | 前54日 open 价格相对最新收盘归一 |
| 7 | `OPEN53` | `Ref($open, 53)/$close` | 前53日 open 价格相对最新收盘归一 |
| 8 | `OPEN52` | `Ref($open, 52)/$close` | 前52日 open 价格相对最新收盘归一 |
| 9 | `OPEN51` | `Ref($open, 51)/$close` | 前51日 open 价格相对最新收盘归一 |
| 10 | `OPEN50` | `Ref($open, 50)/$close` | 前50日 open 价格相对最新收盘归一 |
| 11 | `OPEN49` | `Ref($open, 49)/$close` | 前49日 open 价格相对最新收盘归一 |
| 12 | `OPEN48` | `Ref($open, 48)/$close` | 前48日 open 价格相对最新收盘归一 |
| 13 | `OPEN47` | `Ref($open, 47)/$close` | 前47日 open 价格相对最新收盘归一 |
| 14 | `OPEN46` | `Ref($open, 46)/$close` | 前46日 open 价格相对最新收盘归一 |
| 15 | `OPEN45` | `Ref($open, 45)/$close` | 前45日 open 价格相对最新收盘归一 |
| 16 | `OPEN44` | `Ref($open, 44)/$close` | 前44日 open 价格相对最新收盘归一 |
| 17 | `OPEN43` | `Ref($open, 43)/$close` | 前43日 open 价格相对最新收盘归一 |
| 18 | `OPEN42` | `Ref($open, 42)/$close` | 前42日 open 价格相对最新收盘归一 |
| 19 | `OPEN41` | `Ref($open, 41)/$close` | 前41日 open 价格相对最新收盘归一 |
| 20 | `OPEN40` | `Ref($open, 40)/$close` | 前40日 open 价格相对最新收盘归一 |
| 21 | `OPEN39` | `Ref($open, 39)/$close` | 前39日 open 价格相对最新收盘归一 |
| 22 | `OPEN38` | `Ref($open, 38)/$close` | 前38日 open 价格相对最新收盘归一 |
| 23 | `OPEN37` | `Ref($open, 37)/$close` | 前37日 open 价格相对最新收盘归一 |
| 24 | `OPEN36` | `Ref($open, 36)/$close` | 前36日 open 价格相对最新收盘归一 |
| 25 | `OPEN35` | `Ref($open, 35)/$close` | 前35日 open 价格相对最新收盘归一 |
| 26 | `OPEN34` | `Ref($open, 34)/$close` | 前34日 open 价格相对最新收盘归一 |
| 27 | `OPEN33` | `Ref($open, 33)/$close` | 前33日 open 价格相对最新收盘归一 |
| 28 | `OPEN32` | `Ref($open, 32)/$close` | 前32日 open 价格相对最新收盘归一 |
| 29 | `OPEN31` | `Ref($open, 31)/$close` | 前31日 open 价格相对最新收盘归一 |
| 30 | `OPEN30` | `Ref($open, 30)/$close` | 前30日 open 价格相对最新收盘归一 |
| 31 | `OPEN29` | `Ref($open, 29)/$close` | 前29日 open 价格相对最新收盘归一 |
| 32 | `OPEN28` | `Ref($open, 28)/$close` | 前28日 open 价格相对最新收盘归一 |
| 33 | `OPEN27` | `Ref($open, 27)/$close` | 前27日 open 价格相对最新收盘归一 |
| 34 | `OPEN26` | `Ref($open, 26)/$close` | 前26日 open 价格相对最新收盘归一 |
| 35 | `OPEN25` | `Ref($open, 25)/$close` | 前25日 open 价格相对最新收盘归一 |
| 36 | `OPEN24` | `Ref($open, 24)/$close` | 前24日 open 价格相对最新收盘归一 |
| 37 | `OPEN23` | `Ref($open, 23)/$close` | 前23日 open 价格相对最新收盘归一 |
| 38 | `OPEN22` | `Ref($open, 22)/$close` | 前22日 open 价格相对最新收盘归一 |
| 39 | `OPEN21` | `Ref($open, 21)/$close` | 前21日 open 价格相对最新收盘归一 |
| 40 | `OPEN20` | `Ref($open, 20)/$close` | 前20日 open 价格相对最新收盘归一 |
| 41 | `OPEN19` | `Ref($open, 19)/$close` | 前19日 open 价格相对最新收盘归一 |
| 42 | `OPEN18` | `Ref($open, 18)/$close` | 前18日 open 价格相对最新收盘归一 |
| 43 | `OPEN17` | `Ref($open, 17)/$close` | 前17日 open 价格相对最新收盘归一 |
| 44 | `OPEN16` | `Ref($open, 16)/$close` | 前16日 open 价格相对最新收盘归一 |
| 45 | `OPEN15` | `Ref($open, 15)/$close` | 前15日 open 价格相对最新收盘归一 |
| 46 | `OPEN14` | `Ref($open, 14)/$close` | 前14日 open 价格相对最新收盘归一 |
| 47 | `OPEN13` | `Ref($open, 13)/$close` | 前13日 open 价格相对最新收盘归一 |
| 48 | `OPEN12` | `Ref($open, 12)/$close` | 前12日 open 价格相对最新收盘归一 |
| 49 | `OPEN11` | `Ref($open, 11)/$close` | 前11日 open 价格相对最新收盘归一 |
| 50 | `OPEN10` | `Ref($open, 10)/$close` | 前10日 open 价格相对最新收盘归一 |
| 51 | `OPEN9` | `Ref($open, 9)/$close` | 前9日 open 价格相对最新收盘归一 |
| 52 | `OPEN8` | `Ref($open, 8)/$close` | 前8日 open 价格相对最新收盘归一 |
| 53 | `OPEN7` | `Ref($open, 7)/$close` | 前7日 open 价格相对最新收盘归一 |
| 54 | `OPEN6` | `Ref($open, 6)/$close` | 前6日 open 价格相对最新收盘归一 |
| 55 | `OPEN5` | `Ref($open, 5)/$close` | 前5日 open 价格相对最新收盘归一 |
| 56 | `OPEN4` | `Ref($open, 4)/$close` | 前4日 open 价格相对最新收盘归一 |
| 57 | `OPEN3` | `Ref($open, 3)/$close` | 前3日 open 价格相对最新收盘归一 |
| 58 | `OPEN2` | `Ref($open, 2)/$close` | 前2日 open 价格相对最新收盘归一 |
| 59 | `OPEN1` | `Ref($open, 1)/$close` | 前1日 open 价格相对最新收盘归一 |
| 60 | `OPEN0` | `$open/$close` | open 当日价格相对最新收盘归一 |

## high 字段因子（HIGH0 ~ HIGH59）

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `HIGH59` | `Ref($high, 59)/$close` | 前59日 high 价格相对最新收盘归一 |
| 2 | `HIGH58` | `Ref($high, 58)/$close` | 前58日 high 价格相对最新收盘归一 |
| 3 | `HIGH57` | `Ref($high, 57)/$close` | 前57日 high 价格相对最新收盘归一 |
| 4 | `HIGH56` | `Ref($high, 56)/$close` | 前56日 high 价格相对最新收盘归一 |
| 5 | `HIGH55` | `Ref($high, 55)/$close` | 前55日 high 价格相对最新收盘归一 |
| 6 | `HIGH54` | `Ref($high, 54)/$close` | 前54日 high 价格相对最新收盘归一 |
| 7 | `HIGH53` | `Ref($high, 53)/$close` | 前53日 high 价格相对最新收盘归一 |
| 8 | `HIGH52` | `Ref($high, 52)/$close` | 前52日 high 价格相对最新收盘归一 |
| 9 | `HIGH51` | `Ref($high, 51)/$close` | 前51日 high 价格相对最新收盘归一 |
| 10 | `HIGH50` | `Ref($high, 50)/$close` | 前50日 high 价格相对最新收盘归一 |
| 11 | `HIGH49` | `Ref($high, 49)/$close` | 前49日 high 价格相对最新收盘归一 |
| 12 | `HIGH48` | `Ref($high, 48)/$close` | 前48日 high 价格相对最新收盘归一 |
| 13 | `HIGH47` | `Ref($high, 47)/$close` | 前47日 high 价格相对最新收盘归一 |
| 14 | `HIGH46` | `Ref($high, 46)/$close` | 前46日 high 价格相对最新收盘归一 |
| 15 | `HIGH45` | `Ref($high, 45)/$close` | 前45日 high 价格相对最新收盘归一 |
| 16 | `HIGH44` | `Ref($high, 44)/$close` | 前44日 high 价格相对最新收盘归一 |
| 17 | `HIGH43` | `Ref($high, 43)/$close` | 前43日 high 价格相对最新收盘归一 |
| 18 | `HIGH42` | `Ref($high, 42)/$close` | 前42日 high 价格相对最新收盘归一 |
| 19 | `HIGH41` | `Ref($high, 41)/$close` | 前41日 high 价格相对最新收盘归一 |
| 20 | `HIGH40` | `Ref($high, 40)/$close` | 前40日 high 价格相对最新收盘归一 |
| 21 | `HIGH39` | `Ref($high, 39)/$close` | 前39日 high 价格相对最新收盘归一 |
| 22 | `HIGH38` | `Ref($high, 38)/$close` | 前38日 high 价格相对最新收盘归一 |
| 23 | `HIGH37` | `Ref($high, 37)/$close` | 前37日 high 价格相对最新收盘归一 |
| 24 | `HIGH36` | `Ref($high, 36)/$close` | 前36日 high 价格相对最新收盘归一 |
| 25 | `HIGH35` | `Ref($high, 35)/$close` | 前35日 high 价格相对最新收盘归一 |
| 26 | `HIGH34` | `Ref($high, 34)/$close` | 前34日 high 价格相对最新收盘归一 |
| 27 | `HIGH33` | `Ref($high, 33)/$close` | 前33日 high 价格相对最新收盘归一 |
| 28 | `HIGH32` | `Ref($high, 32)/$close` | 前32日 high 价格相对最新收盘归一 |
| 29 | `HIGH31` | `Ref($high, 31)/$close` | 前31日 high 价格相对最新收盘归一 |
| 30 | `HIGH30` | `Ref($high, 30)/$close` | 前30日 high 价格相对最新收盘归一 |
| 31 | `HIGH29` | `Ref($high, 29)/$close` | 前29日 high 价格相对最新收盘归一 |
| 32 | `HIGH28` | `Ref($high, 28)/$close` | 前28日 high 价格相对最新收盘归一 |
| 33 | `HIGH27` | `Ref($high, 27)/$close` | 前27日 high 价格相对最新收盘归一 |
| 34 | `HIGH26` | `Ref($high, 26)/$close` | 前26日 high 价格相对最新收盘归一 |
| 35 | `HIGH25` | `Ref($high, 25)/$close` | 前25日 high 价格相对最新收盘归一 |
| 36 | `HIGH24` | `Ref($high, 24)/$close` | 前24日 high 价格相对最新收盘归一 |
| 37 | `HIGH23` | `Ref($high, 23)/$close` | 前23日 high 价格相对最新收盘归一 |
| 38 | `HIGH22` | `Ref($high, 22)/$close` | 前22日 high 价格相对最新收盘归一 |
| 39 | `HIGH21` | `Ref($high, 21)/$close` | 前21日 high 价格相对最新收盘归一 |
| 40 | `HIGH20` | `Ref($high, 20)/$close` | 前20日 high 价格相对最新收盘归一 |
| 41 | `HIGH19` | `Ref($high, 19)/$close` | 前19日 high 价格相对最新收盘归一 |
| 42 | `HIGH18` | `Ref($high, 18)/$close` | 前18日 high 价格相对最新收盘归一 |
| 43 | `HIGH17` | `Ref($high, 17)/$close` | 前17日 high 价格相对最新收盘归一 |
| 44 | `HIGH16` | `Ref($high, 16)/$close` | 前16日 high 价格相对最新收盘归一 |
| 45 | `HIGH15` | `Ref($high, 15)/$close` | 前15日 high 价格相对最新收盘归一 |
| 46 | `HIGH14` | `Ref($high, 14)/$close` | 前14日 high 价格相对最新收盘归一 |
| 47 | `HIGH13` | `Ref($high, 13)/$close` | 前13日 high 价格相对最新收盘归一 |
| 48 | `HIGH12` | `Ref($high, 12)/$close` | 前12日 high 价格相对最新收盘归一 |
| 49 | `HIGH11` | `Ref($high, 11)/$close` | 前11日 high 价格相对最新收盘归一 |
| 50 | `HIGH10` | `Ref($high, 10)/$close` | 前10日 high 价格相对最新收盘归一 |
| 51 | `HIGH9` | `Ref($high, 9)/$close` | 前9日 high 价格相对最新收盘归一 |
| 52 | `HIGH8` | `Ref($high, 8)/$close` | 前8日 high 价格相对最新收盘归一 |
| 53 | `HIGH7` | `Ref($high, 7)/$close` | 前7日 high 价格相对最新收盘归一 |
| 54 | `HIGH6` | `Ref($high, 6)/$close` | 前6日 high 价格相对最新收盘归一 |
| 55 | `HIGH5` | `Ref($high, 5)/$close` | 前5日 high 价格相对最新收盘归一 |
| 56 | `HIGH4` | `Ref($high, 4)/$close` | 前4日 high 价格相对最新收盘归一 |
| 57 | `HIGH3` | `Ref($high, 3)/$close` | 前3日 high 价格相对最新收盘归一 |
| 58 | `HIGH2` | `Ref($high, 2)/$close` | 前2日 high 价格相对最新收盘归一 |
| 59 | `HIGH1` | `Ref($high, 1)/$close` | 前1日 high 价格相对最新收盘归一 |
| 60 | `HIGH0` | `$high/$close` | high 当日价格相对最新收盘归一 |

## low 字段因子（LOW0 ~ LOW59）

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `LOW59` | `Ref($low, 59)/$close` | 前59日 low 价格相对最新收盘归一 |
| 2 | `LOW58` | `Ref($low, 58)/$close` | 前58日 low 价格相对最新收盘归一 |
| 3 | `LOW57` | `Ref($low, 57)/$close` | 前57日 low 价格相对最新收盘归一 |
| 4 | `LOW56` | `Ref($low, 56)/$close` | 前56日 low 价格相对最新收盘归一 |
| 5 | `LOW55` | `Ref($low, 55)/$close` | 前55日 low 价格相对最新收盘归一 |
| 6 | `LOW54` | `Ref($low, 54)/$close` | 前54日 low 价格相对最新收盘归一 |
| 7 | `LOW53` | `Ref($low, 53)/$close` | 前53日 low 价格相对最新收盘归一 |
| 8 | `LOW52` | `Ref($low, 52)/$close` | 前52日 low 价格相对最新收盘归一 |
| 9 | `LOW51` | `Ref($low, 51)/$close` | 前51日 low 价格相对最新收盘归一 |
| 10 | `LOW50` | `Ref($low, 50)/$close` | 前50日 low 价格相对最新收盘归一 |
| 11 | `LOW49` | `Ref($low, 49)/$close` | 前49日 low 价格相对最新收盘归一 |
| 12 | `LOW48` | `Ref($low, 48)/$close` | 前48日 low 价格相对最新收盘归一 |
| 13 | `LOW47` | `Ref($low, 47)/$close` | 前47日 low 价格相对最新收盘归一 |
| 14 | `LOW46` | `Ref($low, 46)/$close` | 前46日 low 价格相对最新收盘归一 |
| 15 | `LOW45` | `Ref($low, 45)/$close` | 前45日 low 价格相对最新收盘归一 |
| 16 | `LOW44` | `Ref($low, 44)/$close` | 前44日 low 价格相对最新收盘归一 |
| 17 | `LOW43` | `Ref($low, 43)/$close` | 前43日 low 价格相对最新收盘归一 |
| 18 | `LOW42` | `Ref($low, 42)/$close` | 前42日 low 价格相对最新收盘归一 |
| 19 | `LOW41` | `Ref($low, 41)/$close` | 前41日 low 价格相对最新收盘归一 |
| 20 | `LOW40` | `Ref($low, 40)/$close` | 前40日 low 价格相对最新收盘归一 |
| 21 | `LOW39` | `Ref($low, 39)/$close` | 前39日 low 价格相对最新收盘归一 |
| 22 | `LOW38` | `Ref($low, 38)/$close` | 前38日 low 价格相对最新收盘归一 |
| 23 | `LOW37` | `Ref($low, 37)/$close` | 前37日 low 价格相对最新收盘归一 |
| 24 | `LOW36` | `Ref($low, 36)/$close` | 前36日 low 价格相对最新收盘归一 |
| 25 | `LOW35` | `Ref($low, 35)/$close` | 前35日 low 价格相对最新收盘归一 |
| 26 | `LOW34` | `Ref($low, 34)/$close` | 前34日 low 价格相对最新收盘归一 |
| 27 | `LOW33` | `Ref($low, 33)/$close` | 前33日 low 价格相对最新收盘归一 |
| 28 | `LOW32` | `Ref($low, 32)/$close` | 前32日 low 价格相对最新收盘归一 |
| 29 | `LOW31` | `Ref($low, 31)/$close` | 前31日 low 价格相对最新收盘归一 |
| 30 | `LOW30` | `Ref($low, 30)/$close` | 前30日 low 价格相对最新收盘归一 |
| 31 | `LOW29` | `Ref($low, 29)/$close` | 前29日 low 价格相对最新收盘归一 |
| 32 | `LOW28` | `Ref($low, 28)/$close` | 前28日 low 价格相对最新收盘归一 |
| 33 | `LOW27` | `Ref($low, 27)/$close` | 前27日 low 价格相对最新收盘归一 |
| 34 | `LOW26` | `Ref($low, 26)/$close` | 前26日 low 价格相对最新收盘归一 |
| 35 | `LOW25` | `Ref($low, 25)/$close` | 前25日 low 价格相对最新收盘归一 |
| 36 | `LOW24` | `Ref($low, 24)/$close` | 前24日 low 价格相对最新收盘归一 |
| 37 | `LOW23` | `Ref($low, 23)/$close` | 前23日 low 价格相对最新收盘归一 |
| 38 | `LOW22` | `Ref($low, 22)/$close` | 前22日 low 价格相对最新收盘归一 |
| 39 | `LOW21` | `Ref($low, 21)/$close` | 前21日 low 价格相对最新收盘归一 |
| 40 | `LOW20` | `Ref($low, 20)/$close` | 前20日 low 价格相对最新收盘归一 |
| 41 | `LOW19` | `Ref($low, 19)/$close` | 前19日 low 价格相对最新收盘归一 |
| 42 | `LOW18` | `Ref($low, 18)/$close` | 前18日 low 价格相对最新收盘归一 |
| 43 | `LOW17` | `Ref($low, 17)/$close` | 前17日 low 价格相对最新收盘归一 |
| 44 | `LOW16` | `Ref($low, 16)/$close` | 前16日 low 价格相对最新收盘归一 |
| 45 | `LOW15` | `Ref($low, 15)/$close` | 前15日 low 价格相对最新收盘归一 |
| 46 | `LOW14` | `Ref($low, 14)/$close` | 前14日 low 价格相对最新收盘归一 |
| 47 | `LOW13` | `Ref($low, 13)/$close` | 前13日 low 价格相对最新收盘归一 |
| 48 | `LOW12` | `Ref($low, 12)/$close` | 前12日 low 价格相对最新收盘归一 |
| 49 | `LOW11` | `Ref($low, 11)/$close` | 前11日 low 价格相对最新收盘归一 |
| 50 | `LOW10` | `Ref($low, 10)/$close` | 前10日 low 价格相对最新收盘归一 |
| 51 | `LOW9` | `Ref($low, 9)/$close` | 前9日 low 价格相对最新收盘归一 |
| 52 | `LOW8` | `Ref($low, 8)/$close` | 前8日 low 价格相对最新收盘归一 |
| 53 | `LOW7` | `Ref($low, 7)/$close` | 前7日 low 价格相对最新收盘归一 |
| 54 | `LOW6` | `Ref($low, 6)/$close` | 前6日 low 价格相对最新收盘归一 |
| 55 | `LOW5` | `Ref($low, 5)/$close` | 前5日 low 价格相对最新收盘归一 |
| 56 | `LOW4` | `Ref($low, 4)/$close` | 前4日 low 价格相对最新收盘归一 |
| 57 | `LOW3` | `Ref($low, 3)/$close` | 前3日 low 价格相对最新收盘归一 |
| 58 | `LOW2` | `Ref($low, 2)/$close` | 前2日 low 价格相对最新收盘归一 |
| 59 | `LOW1` | `Ref($low, 1)/$close` | 前1日 low 价格相对最新收盘归一 |
| 60 | `LOW0` | `$low/$close` | low 当日价格相对最新收盘归一 |

## vwap 字段因子（VWAP0 ~ VWAP59）

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `VWAP59` | `Ref($vwap, 59)/$close` | 前59日 vwap 价格相对最新收盘归一 |
| 2 | `VWAP58` | `Ref($vwap, 58)/$close` | 前58日 vwap 价格相对最新收盘归一 |
| 3 | `VWAP57` | `Ref($vwap, 57)/$close` | 前57日 vwap 价格相对最新收盘归一 |
| 4 | `VWAP56` | `Ref($vwap, 56)/$close` | 前56日 vwap 价格相对最新收盘归一 |
| 5 | `VWAP55` | `Ref($vwap, 55)/$close` | 前55日 vwap 价格相对最新收盘归一 |
| 6 | `VWAP54` | `Ref($vwap, 54)/$close` | 前54日 vwap 价格相对最新收盘归一 |
| 7 | `VWAP53` | `Ref($vwap, 53)/$close` | 前53日 vwap 价格相对最新收盘归一 |
| 8 | `VWAP52` | `Ref($vwap, 52)/$close` | 前52日 vwap 价格相对最新收盘归一 |
| 9 | `VWAP51` | `Ref($vwap, 51)/$close` | 前51日 vwap 价格相对最新收盘归一 |
| 10 | `VWAP50` | `Ref($vwap, 50)/$close` | 前50日 vwap 价格相对最新收盘归一 |
| 11 | `VWAP49` | `Ref($vwap, 49)/$close` | 前49日 vwap 价格相对最新收盘归一 |
| 12 | `VWAP48` | `Ref($vwap, 48)/$close` | 前48日 vwap 价格相对最新收盘归一 |
| 13 | `VWAP47` | `Ref($vwap, 47)/$close` | 前47日 vwap 价格相对最新收盘归一 |
| 14 | `VWAP46` | `Ref($vwap, 46)/$close` | 前46日 vwap 价格相对最新收盘归一 |
| 15 | `VWAP45` | `Ref($vwap, 45)/$close` | 前45日 vwap 价格相对最新收盘归一 |
| 16 | `VWAP44` | `Ref($vwap, 44)/$close` | 前44日 vwap 价格相对最新收盘归一 |
| 17 | `VWAP43` | `Ref($vwap, 43)/$close` | 前43日 vwap 价格相对最新收盘归一 |
| 18 | `VWAP42` | `Ref($vwap, 42)/$close` | 前42日 vwap 价格相对最新收盘归一 |
| 19 | `VWAP41` | `Ref($vwap, 41)/$close` | 前41日 vwap 价格相对最新收盘归一 |
| 20 | `VWAP40` | `Ref($vwap, 40)/$close` | 前40日 vwap 价格相对最新收盘归一 |
| 21 | `VWAP39` | `Ref($vwap, 39)/$close` | 前39日 vwap 价格相对最新收盘归一 |
| 22 | `VWAP38` | `Ref($vwap, 38)/$close` | 前38日 vwap 价格相对最新收盘归一 |
| 23 | `VWAP37` | `Ref($vwap, 37)/$close` | 前37日 vwap 价格相对最新收盘归一 |
| 24 | `VWAP36` | `Ref($vwap, 36)/$close` | 前36日 vwap 价格相对最新收盘归一 |
| 25 | `VWAP35` | `Ref($vwap, 35)/$close` | 前35日 vwap 价格相对最新收盘归一 |
| 26 | `VWAP34` | `Ref($vwap, 34)/$close` | 前34日 vwap 价格相对最新收盘归一 |
| 27 | `VWAP33` | `Ref($vwap, 33)/$close` | 前33日 vwap 价格相对最新收盘归一 |
| 28 | `VWAP32` | `Ref($vwap, 32)/$close` | 前32日 vwap 价格相对最新收盘归一 |
| 29 | `VWAP31` | `Ref($vwap, 31)/$close` | 前31日 vwap 价格相对最新收盘归一 |
| 30 | `VWAP30` | `Ref($vwap, 30)/$close` | 前30日 vwap 价格相对最新收盘归一 |
| 31 | `VWAP29` | `Ref($vwap, 29)/$close` | 前29日 vwap 价格相对最新收盘归一 |
| 32 | `VWAP28` | `Ref($vwap, 28)/$close` | 前28日 vwap 价格相对最新收盘归一 |
| 33 | `VWAP27` | `Ref($vwap, 27)/$close` | 前27日 vwap 价格相对最新收盘归一 |
| 34 | `VWAP26` | `Ref($vwap, 26)/$close` | 前26日 vwap 价格相对最新收盘归一 |
| 35 | `VWAP25` | `Ref($vwap, 25)/$close` | 前25日 vwap 价格相对最新收盘归一 |
| 36 | `VWAP24` | `Ref($vwap, 24)/$close` | 前24日 vwap 价格相对最新收盘归一 |
| 37 | `VWAP23` | `Ref($vwap, 23)/$close` | 前23日 vwap 价格相对最新收盘归一 |
| 38 | `VWAP22` | `Ref($vwap, 22)/$close` | 前22日 vwap 价格相对最新收盘归一 |
| 39 | `VWAP21` | `Ref($vwap, 21)/$close` | 前21日 vwap 价格相对最新收盘归一 |
| 40 | `VWAP20` | `Ref($vwap, 20)/$close` | 前20日 vwap 价格相对最新收盘归一 |
| 41 | `VWAP19` | `Ref($vwap, 19)/$close` | 前19日 vwap 价格相对最新收盘归一 |
| 42 | `VWAP18` | `Ref($vwap, 18)/$close` | 前18日 vwap 价格相对最新收盘归一 |
| 43 | `VWAP17` | `Ref($vwap, 17)/$close` | 前17日 vwap 价格相对最新收盘归一 |
| 44 | `VWAP16` | `Ref($vwap, 16)/$close` | 前16日 vwap 价格相对最新收盘归一 |
| 45 | `VWAP15` | `Ref($vwap, 15)/$close` | 前15日 vwap 价格相对最新收盘归一 |
| 46 | `VWAP14` | `Ref($vwap, 14)/$close` | 前14日 vwap 价格相对最新收盘归一 |
| 47 | `VWAP13` | `Ref($vwap, 13)/$close` | 前13日 vwap 价格相对最新收盘归一 |
| 48 | `VWAP12` | `Ref($vwap, 12)/$close` | 前12日 vwap 价格相对最新收盘归一 |
| 49 | `VWAP11` | `Ref($vwap, 11)/$close` | 前11日 vwap 价格相对最新收盘归一 |
| 50 | `VWAP10` | `Ref($vwap, 10)/$close` | 前10日 vwap 价格相对最新收盘归一 |
| 51 | `VWAP9` | `Ref($vwap, 9)/$close` | 前9日 vwap 价格相对最新收盘归一 |
| 52 | `VWAP8` | `Ref($vwap, 8)/$close` | 前8日 vwap 价格相对最新收盘归一 |
| 53 | `VWAP7` | `Ref($vwap, 7)/$close` | 前7日 vwap 价格相对最新收盘归一 |
| 54 | `VWAP6` | `Ref($vwap, 6)/$close` | 前6日 vwap 价格相对最新收盘归一 |
| 55 | `VWAP5` | `Ref($vwap, 5)/$close` | 前5日 vwap 价格相对最新收盘归一 |
| 56 | `VWAP4` | `Ref($vwap, 4)/$close` | 前4日 vwap 价格相对最新收盘归一 |
| 57 | `VWAP3` | `Ref($vwap, 3)/$close` | 前3日 vwap 价格相对最新收盘归一 |
| 58 | `VWAP2` | `Ref($vwap, 2)/$close` | 前2日 vwap 价格相对最新收盘归一 |
| 59 | `VWAP1` | `Ref($vwap, 1)/$close` | 前1日 vwap 价格相对最新收盘归一 |
| 60 | `VWAP0` | `$vwap/$close` | vwap 当日价格相对最新收盘归一 |

## volume 字段因子（VOLUME0 ~ VOLUME59）

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `VOLUME59` | `Ref($volume, 59)/($volume+1e-12)` | 前59日成交量相对最新成交量归一（/$volume+1e-12） |
| 2 | `VOLUME58` | `Ref($volume, 58)/($volume+1e-12)` | 前58日成交量相对最新成交量归一（/$volume+1e-12） |
| 3 | `VOLUME57` | `Ref($volume, 57)/($volume+1e-12)` | 前57日成交量相对最新成交量归一（/$volume+1e-12） |
| 4 | `VOLUME56` | `Ref($volume, 56)/($volume+1e-12)` | 前56日成交量相对最新成交量归一（/$volume+1e-12） |
| 5 | `VOLUME55` | `Ref($volume, 55)/($volume+1e-12)` | 前55日成交量相对最新成交量归一（/$volume+1e-12） |
| 6 | `VOLUME54` | `Ref($volume, 54)/($volume+1e-12)` | 前54日成交量相对最新成交量归一（/$volume+1e-12） |
| 7 | `VOLUME53` | `Ref($volume, 53)/($volume+1e-12)` | 前53日成交量相对最新成交量归一（/$volume+1e-12） |
| 8 | `VOLUME52` | `Ref($volume, 52)/($volume+1e-12)` | 前52日成交量相对最新成交量归一（/$volume+1e-12） |
| 9 | `VOLUME51` | `Ref($volume, 51)/($volume+1e-12)` | 前51日成交量相对最新成交量归一（/$volume+1e-12） |
| 10 | `VOLUME50` | `Ref($volume, 50)/($volume+1e-12)` | 前50日成交量相对最新成交量归一（/$volume+1e-12） |
| 11 | `VOLUME49` | `Ref($volume, 49)/($volume+1e-12)` | 前49日成交量相对最新成交量归一（/$volume+1e-12） |
| 12 | `VOLUME48` | `Ref($volume, 48)/($volume+1e-12)` | 前48日成交量相对最新成交量归一（/$volume+1e-12） |
| 13 | `VOLUME47` | `Ref($volume, 47)/($volume+1e-12)` | 前47日成交量相对最新成交量归一（/$volume+1e-12） |
| 14 | `VOLUME46` | `Ref($volume, 46)/($volume+1e-12)` | 前46日成交量相对最新成交量归一（/$volume+1e-12） |
| 15 | `VOLUME45` | `Ref($volume, 45)/($volume+1e-12)` | 前45日成交量相对最新成交量归一（/$volume+1e-12） |
| 16 | `VOLUME44` | `Ref($volume, 44)/($volume+1e-12)` | 前44日成交量相对最新成交量归一（/$volume+1e-12） |
| 17 | `VOLUME43` | `Ref($volume, 43)/($volume+1e-12)` | 前43日成交量相对最新成交量归一（/$volume+1e-12） |
| 18 | `VOLUME42` | `Ref($volume, 42)/($volume+1e-12)` | 前42日成交量相对最新成交量归一（/$volume+1e-12） |
| 19 | `VOLUME41` | `Ref($volume, 41)/($volume+1e-12)` | 前41日成交量相对最新成交量归一（/$volume+1e-12） |
| 20 | `VOLUME40` | `Ref($volume, 40)/($volume+1e-12)` | 前40日成交量相对最新成交量归一（/$volume+1e-12） |
| 21 | `VOLUME39` | `Ref($volume, 39)/($volume+1e-12)` | 前39日成交量相对最新成交量归一（/$volume+1e-12） |
| 22 | `VOLUME38` | `Ref($volume, 38)/($volume+1e-12)` | 前38日成交量相对最新成交量归一（/$volume+1e-12） |
| 23 | `VOLUME37` | `Ref($volume, 37)/($volume+1e-12)` | 前37日成交量相对最新成交量归一（/$volume+1e-12） |
| 24 | `VOLUME36` | `Ref($volume, 36)/($volume+1e-12)` | 前36日成交量相对最新成交量归一（/$volume+1e-12） |
| 25 | `VOLUME35` | `Ref($volume, 35)/($volume+1e-12)` | 前35日成交量相对最新成交量归一（/$volume+1e-12） |
| 26 | `VOLUME34` | `Ref($volume, 34)/($volume+1e-12)` | 前34日成交量相对最新成交量归一（/$volume+1e-12） |
| 27 | `VOLUME33` | `Ref($volume, 33)/($volume+1e-12)` | 前33日成交量相对最新成交量归一（/$volume+1e-12） |
| 28 | `VOLUME32` | `Ref($volume, 32)/($volume+1e-12)` | 前32日成交量相对最新成交量归一（/$volume+1e-12） |
| 29 | `VOLUME31` | `Ref($volume, 31)/($volume+1e-12)` | 前31日成交量相对最新成交量归一（/$volume+1e-12） |
| 30 | `VOLUME30` | `Ref($volume, 30)/($volume+1e-12)` | 前30日成交量相对最新成交量归一（/$volume+1e-12） |
| 31 | `VOLUME29` | `Ref($volume, 29)/($volume+1e-12)` | 前29日成交量相对最新成交量归一（/$volume+1e-12） |
| 32 | `VOLUME28` | `Ref($volume, 28)/($volume+1e-12)` | 前28日成交量相对最新成交量归一（/$volume+1e-12） |
| 33 | `VOLUME27` | `Ref($volume, 27)/($volume+1e-12)` | 前27日成交量相对最新成交量归一（/$volume+1e-12） |
| 34 | `VOLUME26` | `Ref($volume, 26)/($volume+1e-12)` | 前26日成交量相对最新成交量归一（/$volume+1e-12） |
| 35 | `VOLUME25` | `Ref($volume, 25)/($volume+1e-12)` | 前25日成交量相对最新成交量归一（/$volume+1e-12） |
| 36 | `VOLUME24` | `Ref($volume, 24)/($volume+1e-12)` | 前24日成交量相对最新成交量归一（/$volume+1e-12） |
| 37 | `VOLUME23` | `Ref($volume, 23)/($volume+1e-12)` | 前23日成交量相对最新成交量归一（/$volume+1e-12） |
| 38 | `VOLUME22` | `Ref($volume, 22)/($volume+1e-12)` | 前22日成交量相对最新成交量归一（/$volume+1e-12） |
| 39 | `VOLUME21` | `Ref($volume, 21)/($volume+1e-12)` | 前21日成交量相对最新成交量归一（/$volume+1e-12） |
| 40 | `VOLUME20` | `Ref($volume, 20)/($volume+1e-12)` | 前20日成交量相对最新成交量归一（/$volume+1e-12） |
| 41 | `VOLUME19` | `Ref($volume, 19)/($volume+1e-12)` | 前19日成交量相对最新成交量归一（/$volume+1e-12） |
| 42 | `VOLUME18` | `Ref($volume, 18)/($volume+1e-12)` | 前18日成交量相对最新成交量归一（/$volume+1e-12） |
| 43 | `VOLUME17` | `Ref($volume, 17)/($volume+1e-12)` | 前17日成交量相对最新成交量归一（/$volume+1e-12） |
| 44 | `VOLUME16` | `Ref($volume, 16)/($volume+1e-12)` | 前16日成交量相对最新成交量归一（/$volume+1e-12） |
| 45 | `VOLUME15` | `Ref($volume, 15)/($volume+1e-12)` | 前15日成交量相对最新成交量归一（/$volume+1e-12） |
| 46 | `VOLUME14` | `Ref($volume, 14)/($volume+1e-12)` | 前14日成交量相对最新成交量归一（/$volume+1e-12） |
| 47 | `VOLUME13` | `Ref($volume, 13)/($volume+1e-12)` | 前13日成交量相对最新成交量归一（/$volume+1e-12） |
| 48 | `VOLUME12` | `Ref($volume, 12)/($volume+1e-12)` | 前12日成交量相对最新成交量归一（/$volume+1e-12） |
| 49 | `VOLUME11` | `Ref($volume, 11)/($volume+1e-12)` | 前11日成交量相对最新成交量归一（/$volume+1e-12） |
| 50 | `VOLUME10` | `Ref($volume, 10)/($volume+1e-12)` | 前10日成交量相对最新成交量归一（/$volume+1e-12） |
| 51 | `VOLUME9` | `Ref($volume, 9)/($volume+1e-12)` | 前9日成交量相对最新成交量归一（/$volume+1e-12） |
| 52 | `VOLUME8` | `Ref($volume, 8)/($volume+1e-12)` | 前8日成交量相对最新成交量归一（/$volume+1e-12） |
| 53 | `VOLUME7` | `Ref($volume, 7)/($volume+1e-12)` | 前7日成交量相对最新成交量归一（/$volume+1e-12） |
| 54 | `VOLUME6` | `Ref($volume, 6)/($volume+1e-12)` | 前6日成交量相对最新成交量归一（/$volume+1e-12） |
| 55 | `VOLUME5` | `Ref($volume, 5)/($volume+1e-12)` | 前5日成交量相对最新成交量归一（/$volume+1e-12） |
| 56 | `VOLUME4` | `Ref($volume, 4)/($volume+1e-12)` | 前4日成交量相对最新成交量归一（/$volume+1e-12） |
| 57 | `VOLUME3` | `Ref($volume, 3)/($volume+1e-12)` | 前3日成交量相对最新成交量归一（/$volume+1e-12） |
| 58 | `VOLUME2` | `Ref($volume, 2)/($volume+1e-12)` | 前2日成交量相对最新成交量归一（/$volume+1e-12） |
| 59 | `VOLUME1` | `Ref($volume, 1)/($volume+1e-12)` | 前1日成交量相对最新成交量归一（/$volume+1e-12） |
| 60 | `VOLUME0` | `$volume/($volume+1e-12)` | 最新成交量相对最新成交量归一（/$volume+1e-12） |

## 备注

- 索引含义：`CLOSE0`=当日(最新)收盘价归一(=1)，`CLOSE1`=前1日，`CLOSE59`=前59日，依此类推。
- price 类字段(close/open/high/low/vwap) 统一除以 `$close` 消除量纲；volume 除以 `($volume+1e-12)`。
- 若进一步做中心化/标准化（如 ZScore），`CLOSE0`/`VOLUME0` 会变为 0。
- Alpha360 是**原始特征**，通常直接喂给模型（如 LSTM/Transformer）学习，而非作为人工构造因子使用。
- 标签（label）默认配置：`Ref($close, -2)/Ref($close, -1) - 1` -> `LABEL0`（未来 2 日收益率）。
