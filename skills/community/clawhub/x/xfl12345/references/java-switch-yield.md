---
name: java-switch-yield
description: 写 Java 多分支（3 条及以上常量匹配）逻辑时套用：用 Java 14+ 增强 switch（箭头标签 `case A ->`、块内 `yield` 返回值、enum 穷尽性校验）。通用的「3+ 分支用 switch」规则在 SKILL.md 里（适用所有支持 switch 的语言），本 skill 只讲 Java 专属的增强 switch / yield 高阶语法。写 Java 的 switch 就触发。
---

# Java 增强 switch（yield）

Java 14+ 增强 switch 比传统 switch 更安全优雅——本 skill 讲它的箭头标签、`yield`、enum 穷尽性。

## 为什么用增强 switch

传统 `switch` 两大坑：**忘写 `break` 导致 fall-through**（经典 bug）、**漏 `case` 不报错**。增强 switch（箭头标签 `->`）一次性解决：无 fall-through、enum 穷尽时漏 case 编译报错（String/int 仍需自己补 `default`）。

## 箭头标签（无 fall-through，无需 break）

```java
// ✅ 增强 switch：每个 case 一行，无穿透
String label = switch (status) {
    case PENDING -> "待处理";
    case PROCESSING -> "处理中";
    case DONE -> "完成";
    case FAILED -> "失败";
};
```

## 块 + yield（分支里要先执行语句再返回值）

```java
int code = switch (status) {
    case PENDING -> 0;
    case PROCESSING -> 1;
    case DONE -> 2;
    case FAILED -> {
        log.warn("处理失败：{}", errorMsg);
        yield 3;          // 块里用 yield 返回值
    }
};
```

## enum 穷尽性（漏 case 编译报错）

箭头 switch 覆盖了 enum 的所有值时**不需要 `default`**；以后给 enum 加一个常量忘了处理，编译器直接报错——这是防回归的免费保险。非 enum（String/int）或不想穷尽时，补 `default -> ...`。

## 语句形式（不返回值，只是分支执行动作）

```java
switch (type) {
    case USER -> handleUser();
    case GROUP -> handleGroup();
    case COMPANY -> handleCompany();
}
```

## 什么时候不用

只有 2 个分支、范围判断（如 `x > 0 && x < 10`）、复合条件，还是用 `if`。
