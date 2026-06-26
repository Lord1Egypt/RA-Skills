# TI-ONE 控制台参考信息

## 控制台 URL 格式

### 训练任务详情

```
https://console.cloud.tencent.com/tione/v2/job/detail/{训练任务ID}?regionId={regionId}&workspaceId={workspaceId}
```

示例：`https://console.cloud.tencent.com/tione/v2/job/detail/train-1542619990512406272?regionId=4&workspaceId=0`

### Notebook 开发机详情

```
https://console.cloud.tencent.com/tione/v2/notebook/detail/{NotebookID}?detail=info&regionId={regionId}&workspaceId={workspaceId}
```

示例：`https://console.cloud.tencent.com/tione/v2/notebook/detail/nb-1542622025290711936?detail=info&regionId=4&workspaceId=0`

### 在线推理服务详情

```
https://console.cloud.tencent.com/tione/v2/service/group/detail/{服务组ID}?tab=management&regionId={regionId}&workspaceId={workspaceId}
```

示例：`https://console.cloud.tencent.com/tione/v2/service/group/detail/ms-z4ddl2xp?tab=management&regionId=4&workspaceId=0`

### 资源组详情

```
https://console.cloud.tencent.com/tione/v2/space-manage/resource/detail/{资源组ID}?regionId={regionId}&tab=detail
```

示例：`https://console.cloud.tencent.com/tione/v2/space-manage/resource/detail/rsg-x865ng7l?regionId=4&tab=detail`

> 注意：资源组详情 URL 不包含 `workspaceId` 参数，因为资源组属于空间管理维度，不受工作空间约束。

## 地域 ID 映射

控制台 URL 中的 `regionId` 参数与 API `region` 的对应关系：

| region | regionId | 地域名称 |
|--------|----------|----------|
| ap-guangzhou | 1 | 广州 |
| ap-shanghai | 4 | 上海 |
| ap-beijing | 8 | 北京 |
| ap-nanjing | 33 | 南京 |
| ap-shanghai-adc | 78 | 上海ADC |
| ap-zhongwei | 102 | 中卫 |

## 工作空间 ID

控制台 URL 中的 `workspaceId` 参数：

- **默认工作空间**：`workspaceId=0`
- **用户自定义工作空间**：在 TI-ONE 控制台创建，随机的长整数ID
- 查询时未传 `workspaceId` 参数默认为 `0`
- 可通过环境变量 `TIONE_WORKSPACE_ID` 配置默认值
