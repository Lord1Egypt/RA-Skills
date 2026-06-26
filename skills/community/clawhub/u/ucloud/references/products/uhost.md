# UHost 产品规则

## 产品命名

- 将 `UHost` 视为 UCloud 云主机产品。
- 将用户请求中提及 `CVM`、`ECS`、`EC2`、`VM`、`云主机`、`云服务器` 或类似云 VM 的说法视为对 `UHost` 的请求，除非上下文明确指向其他产品。

## 创建约束

- 创建 UHost 时如果要使用 CloudInit、cloud-init、UserData 或启动初始化脚本，先查询镜像 `Features`。只有 `Features` 包含 `CloudInit` 时才传入 CloudInit/UserData 参数；否则更换镜像或不使用 CloudInit。
- 展示云主机登录用户名前，先根据操作系统发行版确定默认登录用户名。
- Ubuntu 镜像使用 `ubuntu`。Debian、RedHat 和 Rocky 镜像使用 `root`，除非镜像元数据或产品文档另有说明。
- 如果创建响应中未包含关键字段，先使用对应产品查询命令补齐；没有合适查询命令时再调用对应 Describe API。
