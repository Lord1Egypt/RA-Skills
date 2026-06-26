# smyx_payment - 支付流程优化说明

## 🎯 优化内容

**优化点：** 支付成功后自动调用 query.py 查询用户账户信息

---

## 📋 优化后的完整流程

```
【1】显示所有充值套餐信息 ⚠️ 强制
   ↓
【2】用户选择充值套餐（输入编号 0-4）
   ↓
【3】系统自动完成充值账号关联
   ↓
【4】验证手机号格式
   ↓
【5】用户确认充值账号
   ↓
【6】调用 recharge.py 创建云端订单 ⭐ Git 原始版本
   ↓
【7】获取云端 orderNo
   ↓
【8】生成支付宝支付链接 ⭐ 使用固定的 notify_url
   ↓
【9】生成支付宝收款码 ⭐ generate_qr.py
   ↓
【10】用户扫码支付
   ↓
【11】查询支付宝订单状态 ⭐ 必须验证
   ↓
【12】检测到支付成功 ✅
   ↓
【13】自动调用 query.py 查询账户信息 ⭐ 新增
   ↓
【14】显示账户余额和使用情况 ⭐ 新增
   ↓
【15】提示充值成功
```

---

## 🔧 新增脚本

### 1. query_after_payment.py

**文件位置：** `scripts/query_after_payment.py`

**功能：** 支付成功后自动调用 query.py 查询账户信息

**使用方法：**
```bash
# 手动调用
python3 scripts/query_after_payment.py 13829295590

# 或使用 module 方式
python -m scripts.query_after_payment 13829295590
```

**输出示例：**
```
================================================================================
💰 支付成功！正在查询账户信息...
================================================================================

执行命令：python -m scripts.query 13829295590

================================================================================
📊 账户信息
================================================================================
账号：13829295590
已充值金额：¥50.01 元
账户余额：¥0.01 元
剩余使用次数：6010 次
已使用次数：4990 次

================================================================================
✅ 账户信息查询成功！
================================================================================
```

---

### 2. payment_flow.py

**文件位置：** `scripts/payment_flow.py`

**功能：** 完整的支付流程脚本（包含支付后查询）

**使用方法：**
```bash
# 运行完整支付流程
python3 scripts/payment_flow.py
```

---

## 📝 集成到中台回调

**在中台的 `AlipayCallbackController.java` 中添加：**

```java
@PostMapping("/on-notify")
public ResponseEntity<String> onNotify(@RequestParam Map<String, String> params) {
    // ... 验证签名等逻辑 ...
    
    if ("TRADE_SUCCESS".equals(tradeStatus)) {
        // 1. 更新订单状态
        // 2. 增加可用次数
        
        // 3. ⭐ 新增：调用 query.py 查询账户信息
        queryAccountAfterPayment(params.get("buyer_logon_id"));
        
        return ResponseEntity.ok("success");
    }
    
    return ResponseEntity.ok("success");
}

/**
 * 调用 query.py 查询账户信息
 */
private void queryAccountAfterPayment(String phone) {
    try {
        ProcessBuilder pb = new ProcessBuilder(
            "python3", 
            "/path/to/smyx_payment/scripts/query_after_payment.py",
            phone
        );
        pb.redirectErrorStream(true);
        Process process = pb.start();
        
        // 读取输出
        BufferedReader reader = new BufferedReader(
            new InputStreamReader(process.getInputStream())
        );
        String line;
        while ((line = reader.readLine()) != null) {
            log.info("账户查询：{}", line);
        }
        
        process.waitFor();
        
    } catch (Exception e) {
        log.error("调用 query.py 失败：", e);
    }
}
```

---

## 🎯 使用场景

### 场景 1：手动测试支付流程

```bash
# 1. 生成支付订单并扫码支付
cd /home/admin/openclaw/workspace/skills/smyx_payment
python3 -m scripts.recharge 13829295590 9.9 体验套餐 "增值账户续费 - 体验套餐"

# 2. 支付成功后，自动查询账户信息
python3 scripts/query_after_payment.py 13829295590
```

### 场景 2：中台自动回调

**支付宝回调 → 中台处理 → 自动调用 query.py**

```
支付成功
   ↓
支付宝回调到中台
   ↓
中台更新订单状态
   ↓
中台调用 query_after_payment.py
   ↓
显示账户余额和使用情况
```

---

## 📋 查询结果说明

**query.py 返回的账户信息包含：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `totalRecharged` | 已充值金额 | ¥50.01 元 |
| `balance` | 账户余额 | ¥0.01 元 |
| `remainingUses` | 剩余使用次数 | 6010 次 |
| `usedCount` | 已使用次数 | 4990 次 |
| `isInsufficient` | 余额是否不足 | false |

---

## 💡 优势

| 优化项 | 优化前 | 优化后 |
|--------|--------|--------|
| **账户查询** | ❌ 需要手动查询 | ✅ 支付后自动查询 |
| **用户体验** | ❌ 不知道是否到账 | ✅ 立即显示余额 |
| **问题排查** | ❌ 需要分别查看 | ✅ 一站式查看 |
| **流程完整性** | ❌ 支付后无反馈 | ✅ 完整闭环 |

---

## 🔍 测试步骤

**步骤 1：运行支付流程**
```bash
cd /home/admin/openclaw/workspace/skills/smyx_payment
python3 -m scripts.recharge 13829295590 9.9 体验套餐 "增值账户续费 - 体验套餐"
```

**步骤 2：扫码支付**
- 打开支付宝 APP
- 扫描生成的收款码
- 支付 ¥9.9 元

**步骤 3：自动查询账户**
```bash
# 支付成功后自动执行
python3 scripts/query_after_payment.py 13829295590
```

**预期输出：**
```
================================================================================
💰 支付成功！正在查询账户信息...
================================================================================

执行命令：python -m scripts.query 13829295590

================================================================================
📊 账户信息
================================================================================
账号：13829295590
已充值金额：¥50.01 元
账户余额：¥0.01 元
剩余使用次数：6010 次
已使用次数：4990 次

================================================================================
✅ 账户信息查询成功！
================================================================================
```

---

**支付流程优化完成！支付成功后会自动查询并显示账户信息！** 🦞
