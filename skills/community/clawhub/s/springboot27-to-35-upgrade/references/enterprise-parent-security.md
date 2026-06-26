# 企业父 POM 专项（bw-spring-boot-starter-parent-security）

当项目父 POM 命中以下坐标时执行：

- `com.baiwang.basictools:bw-spring-boot-starter-parent-security`

## 检查项

1. 目标父版本是否为 Boot 3.5 对齐版本。
2. 父 POM 托管依赖变化是否影响当前业务依赖。
3. 内部 starter 是否已有 Boot 3 兼容版本。

## 建议扫描

```bash
rg -n "bw-spring-boot-starter-parent-security|<parent>|<artifactId>|<version>" -g "**/pom.xml"
```

## 处理策略

- 先升级父 POM为3.5.2版本，再观察依赖树差异。
- 对冲突依赖先在 `dependencyManagement` 固定版本。
- 若内部 starter 未升级，给出阻塞清单并暂停业务层迁移。
