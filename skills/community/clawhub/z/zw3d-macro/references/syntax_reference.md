# ZW3D 宏语法参考

## 宏文件基本结构

```mac
# Author -用户名
# Date - 录制时间
# Version - ZW3D版本
# Description - 宏描述

MACRO main
[QaBlVersion,1]

[vxBuildDate,MM/DD/YYYY]    # 产品构建日期
[vxConfigDefault,版本号]    # 使用默认配置

# 宏主体 - 记录用户操作

[vxConfigRestore]    # 恢复用户配置
ENDMACRO
```

## 新建文件并指定文件名

新建文件时，应该提供与宏文件同名的文件名：

```mac
[vxSend,"$CdFileNew"]
[vxFormInitGlbl,UiFileNew,"89,1"]
[vxSendEvt,"UiFileNew",1,1,7,"FileNamexxx"]  # 设置文件名（不含扩展名）
[vxSendEvt,"UiFileNew",-1,0,0]                # 确认创建
```

**注意**：文件名应与宏文件名保持一致。例如，如果宏文件是 `create_block_100x100x100.mac`，则文件名应为 `create_block_100x100x100`。

---

## 基本宏语句

### vxSend - 发送命令
```mac
[vxSend,"$CdFileNew"]           # GUI命令 ($前缀)
[vxSend,"!FtAllBox"]            # 模板命令 (!前缀)
[vxSend,"~CdPaste"]             # 特殊命令 (~前缀)
[vxSend,"~CdUDFDelete"]         # UDF删除
[vxSend,"~CdUDFWizardShow"]     # UDF向导
[vxSend,"~CdUDFInsShow"]        # UDF插入
```

### vxSendEvt - 发送事件
```mac
[vxSendEvt,"表单名",控件ID,参数...]
[vxSendEvt,"UiFileNew",-1,0,0]
[vxSendEvt,"UiFileNew",1,1,7,"00CdUDFInsShow_011"]  # 带字符串参数
[vxSendEvt,"UiHistoryManager",220,(4,1),14,4]       # 历史管理器操作
[vxSendEvt,"UiManager",1,0,2,"UiHistoryManager"]    # 切换面板
```

### vxSendEvtOpt - 发送选项事件
```mac
[vxSendEvtOpt,-1,0,1,2]          # 点击OK按钮
[vxSendEvtOpt,14,0,3,2]          # 设置Combine method
[vxSendEvtOpt,4,0,1,6,"40"]      # 设置文本值
```

### vxFormEvtOpt - 表单选项事件
```mac
[vxFormEvtOpt,"FtFillet2",-1,0,1,2]  # 表单确认
```

### vxSendOptFocus - 设置焦点
```mac
[vxSendOptFocus,2,0]             # 设置Direction焦点
[vxSendOptFocus,4,0]             # 设置Spacing焦点
[vxSendOptFocus,10,0]            # 设置Number焦点
```

### vxInitCmd - 初始化命令参数
```mac
[vxInitCmd,命令名,<参数1><参数2>...]
[vxInitCmd,FtAllBox,<14,0><8,0>]           # 方块：Add方式, Corner类型
[vxInitCmd,FtAllBox,<14,0><8,1>]           # 方块：Add方式, Center类型
[vxInitCmd,FtAllExt,<14,0><31,1><2,0>...]  # 拉伸：多参数
[vxInitCmd,FtFillet2,<30,0><42,0><6,0.5>...]  # 倒圆角
[vxInitCmd,FtPtnFtr,<10,0><3,2><4,20>...]  # 阵列
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0>]  # 草图材质
[vxInitCmd,CdUDFCmd,<10,2><11,2>]         # UDF命令参数
```

### vxFormInitGlbl - 初始化GUI表单参数
```mac
[vxFormInitGlbl,表单名,"参数"]
[vxFormInitGlbl,UiFileNew,"89,1"]
```

### vxViewSet2 - 设置视图
```mac
[vxViewSet2,0.787,0.605,0.118,-0.299,0.208,0.931,0.539,-0.768,0.345,0,0,0,0,200,600,-600,1200]
```

---

## 鼠标操作语句

### 鼠标点击
```mac
[vxSend,"*14.6849,10.7585,1.01937,LMB_DN"]    # 左键按下
[vxSend,"*14.6849,10.7585,1.01937,LMB_UP"]    # 左键释放
[vxSend,"*-72.2222,51.2077,0,LMB_DN"]         # 选择点1
[vxSend,"*-71.9807,50.9662,0,LMB_UP"]         
[vxSend,"*109.662,-54.8309,0,LMB_DN"]         # 选择点2
[vxSend,"*109.662,-54.8309,0,LMB_UP"]
```

### 拖拽操作
```mac
[vxSend,"*-12.4669,-0.0760508,19.3003,DRAG"]  # 拖拽中
[vxSend,"*-17.9578,-2.92324,21.5365,DRAG"]    # 拖拽定义长度
[vxSend,"*-17.9578,-2.92324,21.5365,LMB_UP"]  # 释放完成
```

### 中键操作
```mac
[vxSend,"*-23.428,-34.6215,-40.4942,MMB_DN"]  # 中键按下(旋转视图)
[vxSend,"*-24.1594,-35.5001,-41.3082,DRAG"]   # 拖拽旋转
[vxSend,"*-24.1594,-35.5001,-41.3082,MMB_UP"] # 中键释放
```

---

## 控制结构

### IF-ELSEIF-ELSE-ENDIF
```mac
IF (条件)
    宏语句
ELSEIF (条件)
    宏语句
ELSE
    宏语句
ENDIF
```

### WHILE-ENDWHILE
```mac
WHILE (条件)
    宏语句
ENDWHILE
```

### BUFFER-ENDBUFFER
缓存多条宏语句，先推入指令管道而不执行
```mac
BUFFER
[vxSend,"!CdFileOpen2"]
[vxSend,"PartA.Z3PRT"]
ENDBUFFER
```

---

## 特殊关键字

### 调试
```mac
[DebugOn]                        # 开启逐行调试
+[vxSend,"$CdFileNew"]           # 单行断点
```

### 错误处理
```mac
[QaAllowRetry]                   # 允许命令失败一次
[QaExpectError]                  # 预期有错误
```

### 变量与函数
```mac
# 变量赋值
NUMBER1 = 5
SUM = NUMBER1 + NUMBER2

# 函数调用
FUNCTION cnt = QaFnHistCnt()
FUNCTION redefine = QaFnHistCanInfomRedefine(item)
```

---

## 基线输出命令

```mac
[QaOutVol]                       # 输出体积基线
[QaOutArea]                      # 输出面积基线
[QaOutBary,0]                    # 输出线框重心
[QaOutEntCnt,1]                  # 输出实体数量
[QaOutHist]                      # 输出历史记录
```

---

## 常用命令速查

### 文件操作
| 命令 | 说明 |
|------|------|
| `$CdFileNew` | 新建文件 |
| `$CdFileOpen` | 打开文件 |
| `!CdFileOpen2` | 打开文件(模板命令) |
| `~CdUDFDelete` | 删除UDF |

### 草图与建模
| 命令 | 说明 |
|------|------|
| `!CdProfNew` | 新建草图 |
| `!WrCrRects` | 绘制矩形 |
| `!FtAllBox` | 创建方块 |
| `!FtAllExt` | 拉伸特征 |
| `!FtFillet2` | 倒圆角 |
| `!FtPtnFtr` | 阵列特征 |
| `$CdEditParent` | 编辑父特征 |

### UDF操作
| 命令 | 说明 |
|------|------|
| `~CdUDFWizardShow` | UDF向导 |
| `~CdUDFInsShow` | 插入UDF |
| `UiUDFWizard` | UDF向导UI |
| `UiUDFWizardFtr` | UDF特征选择 |
| `UiUDFWizardDef` | UDF定义 |
| `UiUDFWizardExpr` | UDF表达式 |
| `UiUDFIns` | UDF插入UI |

### 历史管理
| 命令 | 说明 |
|------|------|
| `UiHistoryManager` | 历史管理器 |
| `UiManager` | UI管理器 |
| `UiInputManager` | 输入管理器 |

**选择特征进行编辑：**
括号中的第一位数字从1开始计数（流水号）。

例如，如果历史树包含：
1. 默认坐标系
2. 方块特征
3. 倒圆角特征

则：
- `(1,1)` - 默认坐标系
- `(2,1)` - 方块特征
- `(3,1)` - 倒圆角特征

示例（选择并编辑第2个特征，即方块）：
```mac
[vxSendEvt,"UiHistoryManager",220,(2,1),25,4]  # 选择方块特征
[vxSendEvt,"UiHistoryManager",220,(2,1),4,4]   # 激活编辑
[vxSend,"$CdHistEdit"]                          # 进入编辑模式
```

---

## 参数说明

### FtAllBox 参数
- `<8,0>` - Block type = Corner (角点方式)
- `<8,1>` - Block type = Center (中心方式)

**组合方式选项：**
```mac
[vxSendEvtOpt,14,0,1,2]    # 基体
[vxSendEvtOpt,14,0,2,2]    # 布尔加
[vxSendEvtOpt,14,0,3,2]    # 布尔减
```

**设置长宽高尺寸：**
```mac
[vxSendOptFocus,3,0]             # 长度输入框获得焦点
[vxSendEvtOpt,3,0,1,6,"100"]     # 设置长度 = 100
[vxSendEvtOpt,3,0,-1,6,"100"]    # 确认长度值

[vxSendOptFocus,4,0]             # 宽度输入框获得焦点
[vxSendEvtOpt,4,0,1,6,"100"]     # 设置宽度 = 100
[vxSendEvtOpt,4,0,-1,6,"100"]    # 确认宽度值

[vxSendOptFocus,5,0]             # 高度输入框获得焦点
[vxSendEvtOpt,5,0,1,6,"100"]     # 设置高度 = 100
[vxSendEvtOpt,5,0,-1,6,"100"]    # 确认高度值
```

### FtAllExt 常用参数
- `<2,0>` - 拉伸方向
- `<3,15>` - 拉伸深度
- `<14,0>` - Combine method

### FtFillet2 常用参数
- `<6,0.5>` - 圆角半径
- `<16,3>` - 边选择模式

**倒圆角完整流程：**
```mac
[vxSend,"!FtFillet2"]
[vxInitCmd,FtFillet2,<30,0><42,0><3,0><7,0><48,0><6,10><23,10><44,0><5,0><27,0><35,0><28,0><24,0><21,0><16,3><17,2><46,1><47,1><57,1>]
[vxInitCmd,FtFlltEdgSet,<2,5><22,0><6,0>]

# 选择边
[vxSend,"*50,50,50,LMB_DN"]
[vxSend,"*50,50,50,LMB_UP"]

# 确认倒圆角
[vxFormEvtOpt,"FtFillet2",-1,0,1,2]
```

### FtPtnFtr 常用参数
- `<3,2>` - 阵列类型 (2=圆形)
- `<3,3>` - 阵列类型 (3=线性)
- `<4,20>` - 阵列数量
- `<12,45>` - 角度/间距

---

## 复杂模型创建示例：桌子

### 设计思路
使用草图+拉伸的方式创建桌子，包含桌面和4条桌腿。

### 桌面创建
```mac
# 创建桌面草图
[vxSend,"!CdProfNew"]
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0><6,1><5,0>]
BUFFER
[vxSendEvtOpt,-1,0,1,2]          # 确认，使用默认平面
ENDBUFFER

# 绘制桌面矩形（1000x600）
[vxSend,"!WrCrRects"]
[vxInitCmd,WrCrRects,<15,1>]
[vxSendEvtOpt,1,0,1,6,"-500,-300<mm>"]  # 起始点(-500,-300)，使中心在原点
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"1000"]    # 长度1000
[vxSendOptFocus,6,0]
[vxSendEvtOpt,6,0,1,6,"600"]     # 宽度600
[vxSendEvtOpt,-1,0,1,2]          # 确认

# 拉伸桌面
[vxSend,"$CdEditParent"]
[vxSendEvt,"UiHistoryManager",220,(2,1),14,4]
[vxSendEvt,"UiHistoryManager",220,(2,1),2,4]
[vxSend,"!FtAllExt"]
[vxInitCmd,FtAllExt,<14,0><31,1><64,0><2,0><60,0><67,0><3,15><61,0><4,0><8,0><13,0><5,0><70,0><10,0><20,0><30,0><17,0><33,0><16,0><51,0>]
[vxSendOptFocus,3,0]
[vxSendEvtOpt,3,0,1,6,"30"]      # 厚度30mm
[vxSendEvtOpt,-1,0,1,2]
```

### 桌腿创建（4个在一个草图）
```mac
# 创建桌腿草图
[vxSend,"!CdProfNew"]
[vxInitCmd,CdMatInpSk,<4,0><19,0><11,0><6,1><5,0>]
BUFFER
[vxSendEvtOpt,-1,0,1,2]
ENDBUFFER

# 绘制4个桌腿矩形（50x50），位置在桌面四角内侧
# 左前：(-425, -250)
[vxSend,"!WrCrRects"]
[vxInitCmd,WrCrRects,<15,1>]
[vxSendEvtOpt,1,0,1,6,"-425,-250<mm>"
[vxSendOptFocus,5,0]
[vxSendEvtOpt,5,0,1,6,"50"
[vxSendOptFocus,6,0]
[vxSendEvtOpt,6,0,1,6,"50"
[vxSendEvtOpt,-1,0,1,2]

# 右前：(425, -250)
[vxSend,"!WrCrRects"]
[vxInitCmd,WrCrRects,<15,1>]
[vxSendEvtOpt,1,0,1,6,"425,-250<mm>"
...

# 左后：(-425, 250)
...

# 右后：(425, 250)
...

# 拉伸桌腿
[vxSend,"$CdEditParent"]
[vxSendEvt,"UiHistoryManager",220,(4,1),14,4]
[vxSendEvt,"UiHistoryManager",220,(4,1),2,4]
[vxSend,"!FtAllExt"]
[vxInitCmd,FtAllExt,<14,0><31,1><64,0><2,0><60,0><67,0><3,30><61,0><4,0><8,0><13,0><5,0><70,0><10,0><20,0><30,0><17,0><33,0><16,0><51,0>]
[vxSendOptFocus,3,0]
[vxSendEvtOpt,3,0,1,6,"700"]     # 长度700mm
[vxSendOptFocus,7,0]
[vxSendOptFocus,7,0]
[vxSend,"PntDirZ"]                # Z方向拉伸
[vxSendEvtOpt,-1,0,1,2]
```

### 定位计算
- 桌面：1000×600，起始点(-500,-300)，范围X:-500~500, Y:-300~300
- 桌腿：50×50，中心位置(±425, ±250)，确保在桌面范围内
- 边距：左右75mm，前后50mm

---

## 注意事项

1. **语序调整**: `vxInitCmd`, `vxFormInitGlbl`, `QaAllowRetry` 会自动提前一行执行
2. **BUFFER内语句**: 非`vxSend`语句会被封装成`FormCommand`
3. **配置恢复**: 必须保留`[vxConfigRestore]`，否则影响其他宏
4. **基线版本**: 新宏需要本地跑宏一次产生基线后，才有`[QaBlVersion]`
5. **坐标值**: 鼠标操作中的坐标是3D空间坐标，与视图相关
