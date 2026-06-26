# 值对象（Value Object）规范

## 核心特征

- **无唯一标识**：由属性值定义，相等性基于属性
- **不可变**：构造后字段不可修改
- **可共享**：无副作用，可在多处引用

## 构造规范

所有校验在构造时完成，构造后不可变。

```java
public record Money(BigDecimal amount, Currency currency) {

    public static final Money ZERO = new Money(BigDecimal.ZERO, Currency.CNY);

    public Money {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new DomainException("Amount must be positive");
        }
        if (currency == null) {
            throw new DomainException("Currency required");
        }
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.HALF_UP);
    }
}
```

## 业务行为方法

值对象封装与该概念相关的**业务行为**，而非简单的 getter/setter。

```java
public record Money(BigDecimal amount, Currency currency) {

    public Money add(Money other) {
        checkCurrencyMatch(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }

    public Money subtract(Money other) {
        checkCurrencyMatch(other);
        if (other.amount.compareTo(this.amount) > 0) {
            throw new DomainException("Insufficient amount");
        }
        return new Money(this.amount.subtract(other.amount), this.currency);
    }

    public Money multiply(int multiplier) {
        return new Money(this.amount.multiply(BigDecimal.valueOf(multiplier)), this.currency);
    }

    public boolean isGreaterThan(Money other) {
        checkCurrencyMatch(other);
        return this.amount.compareTo(other.amount) > 0;
    }

    private void checkCurrencyMatch(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new DomainException("Currency mismatch");
        }
    }
}
```

## equals / hashCode

使用 Java record 自动生成，或显式重写。

```java
// record 自动提供 equals/hashCode/toString
public record Address(String province, String city, String detail, String zipCode) {

    public Address {
        if (StringUtils.isBlank(province) || StringUtils.isBlank(city)) {
            throw new DomainException("Province and city required");
        }
    }

    public String fullAddress() {
        return province + " " + city + " " + detail;
    }
}
```

## 何时使用值对象

将以下场景建模为值对象：
- **金额**：Money（包含币种和精度处理）
- **地址**：Address（省市区详情）
- **电话号码**：PhoneNumber（格式化验证）
- **日期范围**：DateRange（开始/结束日期及校验）
- **颜色/规格**：任何由多个属性描述且无唯一标识的概念

## 检查清单

- 不可变（final 字段，无 setter）
- 基于属性判等（record 自动处理）
- 可共享（无副作用）
- 行为封装（与概念相关的业务方法）
- 构造时校验

## 反模式

- 使用 String/Long 裸类型替代值对象（如用 String 代替 Money）
- 值对象内部包含可变状态
