# UDS NRC (Negative Response Code) 参考

## 常用NRC及测试意义

| NRC | 名称 | 说明 | 测试场景 |
|-----|------|------|----------|
| 0x10 | generalReject | 通用拒绝 | ECU内部错误 |
| 0x11 | serviceNotSupported | 不支持的服务 | 发送ECU不支持的SID |
| 0x12 | subFunctionNotSupported | 不支持的子功能 | 无效子功能参数 |
| 0x13 | incorrectMessageLengthOrInvalidFormat | 消息长度/格式错误 | 错误长度请求 |
| 0x14 | responseTooLong | 响应过长 | 多DID读取超限 |
| 0x22 | conditionsNotCorrect | 条件不满足 | 前置条件未满足 |
| 0x24 | requestSequenceError | 请求序列错误 | 流程不正确 |
| 0x25 | noResponseFromSubnetComponent | 子网无响应 | 网关场景 |
| 0x31 | requestOutOfRange | 请求超范围 | 无效DID/参数值 |
| 0x33 | securityAccessDenied | 安全访问被拒 | 未解锁写入/控制 |
| 0x35 | invalidKey | 无效密钥 | 安全访问密钥错误 |
| 0x36 | exceededNumberOfAttempts | 超过尝试次数 | 安全访问锁定 |
| 0x37 | requiredTimeDelayNotExpired | 延时未到 | 安全访问锁定期 |
| 0x70 | uploadDownloadNotAccepted | 上传下载拒绝 | 刷写条件不满足 |
| 0x72 | generalProgrammingFailure | 编程失败 | Flash写入错误 |
| 0x73 | wrongBlockSequenceCounter | 块序列错误 | 刷写数据序列 |
| 0x78 | requestCorrectlyReceivedResponsePending | 等待(Pending) | 需等待继续接收 |
| 0x7E | subFunctionNotSupportedInActiveSession | 子功能在当前会话不支持 | 会话限制 |
| 0x7F | serviceNotSupportedInActiveSession | 服务在当前会话不支持 | 会话限制 |

## UDS服务与会话矩阵

| 服务 | SID | Default(0x01) | Programming(0x02) | Extended(0x03) |
|------|-----|:---:|:---:|:---:|
| DiagnosticSessionControl | 0x10 | ✓ | ✓ | ✓ |
| ECUReset | 0x11 | ✓ | ✓ | ✓ |
| ClearDTC | 0x14 | ✓ | ✗ | ✓ |
| ReadDTCInfo | 0x19 | ✓ | ✗ | ✓ |
| ReadDataByIdentifier | 0x22 | 按DID | 按DID | 按DID |
| SecurityAccess | 0x27 | ✗ | ✓ | ✓ |
| CommunicationControl | 0x28 | ✗ | ✗ | ✓ |
| WriteDataByIdentifier | 0x2E | 按DID | 按DID | 按DID |
| IOControlByIdentifier | 0x2F | ✗ | ✗ | ✓ |
| RoutineControl | 0x31 | ✗ | ✓ | ✓ |
| RequestDownload | 0x34 | ✗ | ✓ | ✗ |
| TransferData | 0x36 | ✗ | ✓ | ✗ |
| RequestTransferExit | 0x37 | ✗ | ✓ | ✗ |
| TesterPresent | 0x3E | ✓ | ✓ | ✓ |
| ControlDTCSetting | 0x85 | ✗ | ✗ | ✓ |

## 安全访问等级

| 等级 | Seed请求 | Key发送 | 典型用途 |
|------|----------|---------|----------|
| Level 1 | 0x01 | 0x02 | 常规解锁(DID写入、IOControl) |
| Level 3 | 0x05 | 0x06 | 编程解锁(刷写) |
| Level FBL | 0x11 | 0x12 | Bootloader解锁 |
| Level IMMO | 0x41 | 0x42 | 防盗解锁 |

## 诊断调查表关键属性清单

### DID属性
- DID Number (hex): DID编号，必须
- DID Name: DID英文名称
- DID Name (Chinese): DID中文名称
- CVT (约定值): M(必须)/C(条件)/S(选填)/U(未用)
- R/W State: R(只读)/W(只写)/R/W(读写)
- Size (Bytes): 数据总长度
- Byte/Bit Position: 子数据位置
- Sub Data Name: 子数据名称
- Range Min/Max: 数据物理值范围
- Unit: 物理单位
- MethodType: 编码方法(identical/BCD/Linear/texttable)
- Data Type: 数据类型(ASCII/Linear/RAW/BITPATTERN等)
- Default Value: 物理默认值
- Storage Position: 存储位置(Flash/EEPROM/RAM)
- Functional Addressing: 是否支持功能寻址(Y/N)
- Session Matrix: 各会话下的读写权限(Y/N)
- Security Level Matrix: 各安全等级下的读写权限(Y/N)

### IOControl属性
- IOControlParam: 控制参数类型
- DID Number: IO对象的DID编号
- Parameters: 请求/响应参数列表
- Security Level: 需要的安全等级
- Conditions: 前置条件

### Routine属性
- RID Number: Routine编号
- ControlType: 01(Start)/02(Stop)/03(RequestResults)
- Parameters: 请求/响应参数列表
- Security Level: 需要的安全等级
- Conditions: 前置条件

### DTC属性
- DTC Number (hex): 3字节DTC编号
- Failure Type Byte: 故障类型
- DTC Name: 故障描述
- Priority: 优先级
- Monitor Enable Criteria: 监测使能条件
- Monitor Type: continuous/on-demand
- Test Failed/Pass Criteria: 判定条件
- DTC Aging: 老化周期数
- Snapshot Record: 快照数据列表
