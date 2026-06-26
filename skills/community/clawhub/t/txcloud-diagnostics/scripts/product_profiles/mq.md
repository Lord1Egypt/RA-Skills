# 消息队列类

## 产品参数

| 产品 | Namespace | Dimension Key | ID 格式 | 核心指标 |
|------|-----------|--------------|---------|---------|
| CKafka | `QCE/CKAFKA` | `instanceId` | ckafka-xxx | InstanceDiskUsage, CpuUsage, MemUsage, InstanceProCount, InstanceConCount, InstanceMsgHeap, InstanceProFlow, InstanceConFlow, InstanceConnectCount |
| RocketMQ | `QCE/ROCKETMQ` | `tenant` + `topic`/`group` | rocketmq-xxx | RocketmqTenantProducerTps, RocketmqTenantConsumerTps, RocketmqTenantDiff, RocketmqTenantProduceMessageSize, RocketmqTenantConsumerMessageSize |
| RabbitMQ | `QCE/RABBITMQ` | `instanceid` + `node`/`vhost`/`queue` | rabbitmq-xxx | InstanceRabbitmqPublishedRate, InstanceRabbitmqDeliveredTotalRate, InstanceRabbitmqQueueMessagesReady, InstanceRabbitmqConnections, NodeRabbitmqCpuUsage, NodeRabbitmqMemUsage, NodeRabbitmqDiskUsage |
| Pulsar (TDMQ) | `QCE/TDMQ` | `tenant` + `environmentId`/`topicName`/`subName` | 集群ID | PulsarTenantTps, TenantCaculateRateIn, TenantCaculateRateOut, PulsarTenantThroughputIn, PulsarTenantThroughputOut, SubMsgBacklog, PulsarDiskUsage |
| CMQ | `QCE/TDMQ` | `environmentId` + `tenantId` + `topicName` | cmqq-xxx | CmqQueueMsgBacklog, CmqTopicMsgBacklog, MsgRateIn, MsgRateOut, StorageSize, StorageBacklogPercentage |

## 指标决策表

| 问题现象 | 产品 | 推荐指标 |
|----------|------|---------|
| 消息堆积 | CKafka | InstanceMsgHeap, InstanceProCount, InstanceConCount, InstanceDiskUsage |
| 消息堆积 | RocketMQ | RocketmqTenantDiff, RocketmqTenantProducerTps, RocketmqTenantConsumerTps |
| 消息堆积 | RabbitMQ | InstanceRabbitmqQueueMessagesReady, InstanceRabbitmqQueueMessagesUnacked |
| 消息堆积 | Pulsar | SubMsgBacklog, TenantCaculateRateIn, TenantCaculateRateOut |
| 吞吐低/延迟高 | CKafka | InstanceProFlow, InstanceConFlow, InstanceProCount, InstanceConCount |
| 磁盘告警 | CKafka | InstanceDiskUsage, InstanceProFlow, InstanceConFlow |
| 资源瓶颈 | RabbitMQ | NodeRabbitmqCpuUsage, NodeRabbitmqMemUsage, NodeRabbitmqDiskUsage |
| 笼统/不明确 | CKafka | InstanceProCount, InstanceConCount, InstanceDiskUsage, InstanceMsgHeap, CpuUsage |

## 注意事项

- CKafka 标准版 dimension key `instanceId`（大写I），专业版 `instanceid`（小写i）
- Pulsar 和 CMQ 共用 namespace `QCE/TDMQ`，通过 `tenant`/`environmentId` 等维度区分
