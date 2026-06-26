---
name: validate-einvoice-xml
description: 验证XML文件是否为中国数电票（全面数字化电子发票）格式。检查XML结构、必需字段和数电票特征。当用户需要验证XML是否为数电票、检查数电票格式合规性、或处理电子发票XML文件时使用。
---

# 数电票XML验证

验证XML文件是否符合中国数电票（全面数字化电子发票）格式规范。

## 数电票XML关键特征

数电票XML必须包含以下核心结构和字段：

### 1. 根元素
- 根元素名称为 `EInvoice`

### 2. 头部信息 (Header)
必需子元素：
- `EIid` - 发票唯一标识（20位数字）
- `EInvoiceTag` - 发票标签（如 SWEI4400）
- `Version` - 版本号
- `InherentLabel` - 固有标签（包含发票类型信息）

### 3. 发票数据 (EInvoiceData)
必需包含以下部分：
- `SellerInformation` - 销售方信息（SellerIdNum, SellerName）
- `BuyerInformation` - 购买方信息（BuyerIdNum, BuyerName）
- `BasicInformation` - 基本信息（金额、开票时间等）
- `IssuItemInformation` - 开票项目信息（至少一个）

### 4. 销售方认证 (SellerAuthentication)
- `AuthenticationMethods` - 认证方式

### 5. 税务监管信息 (TaxSupervisionInfo)
- `InvoiceNumber` - 发票号码（20位）
- `IssueTime` - 开票日期
- `TaxBureauCode` - 税务局代码
- `TaxBureauName` - 税务局名称

### 6. 税务局签名 (TaxBureauSignature)
- `SignatureValue` - 签名值（包含数字签名）

## 验证流程

1. **XML格式检查**
   - 验证是否为有效的XML文件
   - 检查XML声明（encoding="utf-8"）

2. **根元素验证**
   - 确认根元素为 `EInvoice`

3. **必需元素检查**
   - 检查 Header/EIid 是否存在（20位数字）
   - 检查 Header/EInvoiceTag 是否存在
   - 检查 EInvoiceData/SellerInformation/SellerIdNum
   - 检查 EInvoiceData/BuyerInformation/BuyerIdNum
   - 检查 TaxSupervisionInfo/InvoiceNumber（20位）

4. **数电票特征验证**
   - 发票号码为20位数字（区别于传统发票的8位或12位）
   - 包含数字签名（TaxBureauSignature/SignatureValue）
   - 包含税务局信息

## 验证脚本

使用以下Python脚本进行验证：

```python
import xml.etree.ElementTree as ET
import re

def validate_einvoice_xml(file_path):
    """
    验证XML是否为数电票格式
    返回: (is_valid: bool, message: str, details: dict)
    """
    result = {
        "is_valid_xml": False,
        "has_einvoice_root": False,
        "has_required_fields": False,
        "invoice_number": None,
        "seller_id": None,
        "buyer_id": None,
        "errors": []
    }
    
    try:
        # 1. 解析XML
        tree = ET.parse(file_path)
        root = tree.getroot()
        result["is_valid_xml"] = True
        
        # 2. 检查根元素
        if root.tag != "EInvoice":
            result["errors"].append(f"根元素应为 'EInvoice'，实际为 '{root.tag}'")
            return False, "非数电票格式：根元素不匹配", result
        result["has_einvoice_root"] = True
        
        # 3. 检查必需字段
        ns = {'': root.tag}  # 处理命名空间
        
        # 检查 EIid
        eiid = root.find('.//EIid')
        if eiid is None or not eiid.text:
            result["errors"].append("缺少必需字段: Header/EIid")
        elif eiid.text and not re.match(r'^\d{20}$', eiid.text.strip()):
            result["errors"].append(f"EIid 应为20位数字，实际为: {eiid.text}")
        
        # 检查 EInvoiceTag
        einvoice_tag = root.find('.//EInvoiceTag')
        if einvoice_tag is None or not einvoice_tag.text:
            result["errors"].append("缺少必需字段: Header/EInvoiceTag")
        
        # 检查 InvoiceNumber (20位数电票号码)
        invoice_num = root.find('.//InvoiceNumber')
        if invoice_num is not None and invoice_num.text:
            result["invoice_number"] = invoice_num.text.strip()
            if not re.match(r'^\d{20}$', invoice_num.text.strip()):
                result["errors"].append(f"InvoiceNumber 应为20位数字，实际为: {invoice_num.text}")
        
        # 检查销售方纳税人识别号
        seller_id = root.find('.//SellerIdNum')
        if seller_id is not None and seller_id.text:
            result["seller_id"] = seller_id.text.strip()
        
        # 检查购买方纳税人识别号
        buyer_id = root.find('.//BuyerIdNum')
        if buyer_id is not None and buyer_id.text:
            result["buyer_id"] = buyer_id.text.strip()
        
        # 检查数字签名
        signature = root.find('.//SignatureValue')
        if signature is None or not signature.text:
            result["errors"].append("缺少数字签名: TaxBureauSignature/SignatureValue")
        
        # 检查税务局信息
        tax_bureau = root.find('.//TaxBureauName')
        if tax_bureau is None or not tax_bureau.text:
            result["errors"].append("缺少税务局信息: TaxSupervisionInfo/TaxBureauName")
        
        # 判定结果
        if len(result["errors"]) == 0:
            result["has_required_fields"] = True
            return True, "验证通过：该XML是有效的数电票格式", result
        else:
            return False, f"验证失败：发现 {len(result['errors'])} 个问题", result
            
    except ET.ParseError as e:
        result["errors"].append(f"XML解析错误: {str(e)}")
        return False, "XML格式错误：无法解析文件", result
    except Exception as e:
        result["errors"].append(f"验证过程出错: {str(e)}")
        return False, f"验证异常: {str(e)}", result


def print_validation_report(file_path):
    """打印详细的验证报告"""
    is_valid, message, details = validate_einvoice_xml(file_path)
    
    print("=" * 60)
    print("数电票XML验证报告")
    print("=" * 60)
    print(f"文件路径: {file_path}")
    print(f"验证结果: {'✓ 通过' if is_valid else '✗ 失败'}")
    print(f"结果说明: {message}")
    print("-" * 60)
    
    if details["invoice_number"]:
        print(f"发票号码: {details['invoice_number']}")
    if details["seller_id"]:
        print(f"销售方税号: {details['seller_id']}")
    if details["buyer_id"]:
        print(f"购买方税号: {details['buyer_id']}")
    
    if details["errors"]:
        print("\n问题列表:")
        for i, error in enumerate(details["errors"], 1):
            print(f"  {i}. {error}")
    
    print("=" * 60)
    return is_valid


# 使用示例
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print_validation_report(sys.argv[1])
    else:
        print("用法: python validate_einvoice.py <xml文件路径>")
```

## 快速判断方法

如果只需要快速判断，检查以下3个关键特征：

1. **根元素是 `EInvoice`** - 区别于传统发票的 `Invoice`
2. **发票号码是20位数字** - 区别于传统发票的8位或12位
3. **包含 `TaxBureauSignature`** - 税务局数字签名

满足以上3点，基本可以确定为数电票XML。

## 与传统电子发票的区别

| 特征 | 数电票 | 传统电子发票 |
|------|--------|-------------|
| 根元素 | `EInvoice` | `Invoice` |
| 发票号码 | 20位数字 | 8位或12位 |
| 发票代码 | 无 | 有（10位或12位）|
| 数字签名 | TaxBureauSignature | 可能不同 |
| 版本标识 | Version字段 | 可能无 |

## 输出格式

验证完成后，输出以下格式的报告：

```markdown
## 数电票验证结果

**文件**: [文件名]

**验证结果**: [通过/失败]

**发票信息**:
- 发票号码: [20位号码]
- 销售方: [纳税人识别号]
- 购买方: [纳税人识别号]
- 开票日期: [日期]

**详细检查**:
- [x] XML格式正确
- [x] 根元素为EInvoice
- [x] 包含EIid字段（20位）
- [x] 包含发票号码（20位）
- [x] 包含数字签名
- [ ] [如有失败项]

**结论**: [该文件是/不是]有效的数电票XML
```
