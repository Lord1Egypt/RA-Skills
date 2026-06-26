---
name: rocketmq-kubectl
description: "Query and manage RocketMQ messages via kubectl exec. Use when user needs to: (1) Query cluster information, (2) Create, delete, or manage topics, (3) Check consumer progress and message accumulation, (4) Query messages by ID, key, or offset, (5) Reset consumer offset to clear message backlog, (6) Check consumer subscription status, (7) View topic statistics and TPS, (8) Send test messages. Accepts parameters like topic, namespace, group, message_id, command_type, broker_name, offset, queue_id."
---

# RocketMQ Query and Management

Query and manage RocketMQ via kubectl exec in Kubernetes cluster.

## Access Method

Use kubectl exec to access RocketMQ master pod:

```bash
# execute commands directly without login
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin <command> -n master1.teambition.local:9876
```

**Default Nameserver:** `master1.teambition.local:9876`

## Common Commands

### 1. Cluster Management

#### View Cluster Information

View cluster list, BrokerName, BrokerId, TPS and other information:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin clusterList -n master1.teambition.local:9876
```

View detailed cluster information (including yesterday and today's read/write totals):

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin clusterList -n master1.teambition.local:9876 -m
```

### 2. Topic Management

#### List All Topics

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin topiclist -n master1.teambition.local:9876
```

#### Create Topic

Create or update a topic with specified queue numbers:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin updateTopic -n master1.teambition.local:9876 -t <topic-name> -c <cluster-name> -r 8 -w 8
```

**Parameters:**
- `-r`: Number of read queues (default: 8)
- `-w`: Number of write queues (default: 8)
- `-c`: Cluster name (can be queried via clusterList)

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin updateTopic -n master1.teambition.local:9876 -t new-topic -c DefaultCluster -r 16 -w 16
```

#### Delete Topic

Delete a topic from a specific cluster:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin deleteTopic -n master1.teambition.local:9876 -t <topic-name> -c <cluster-name>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin deleteTopic -n master1.teambition.local:9876 -t old-topic -c DefaultCluster
```

#### Query Topic Status

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin topicStatus -n master1.teambition.local:9876 -t <topic-name>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin topicStatus -n master1.teambition.local:9876 -t tb-app-eventbus
```

#### Query Topic Route

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin topicRoute -n master1.teambition.local:9876 -t <topic-name>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin topicRoute -n master1.teambition.local:9876 -t tb-app-eventbus
```

### 3. Consumer Management

#### Query Consumer Progress

Check consumer progress and message accumulation. **Diff total** indicates the number of accumulated messages.

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumerProgress -n localhost:9876
```

Or specify namespace:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumerProgress -n master1.teambition.local:9876
```

#### Query Consumer Status

Check if consumer subscription relationships are consistent:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumerStatus -n master1.teambition.local:9876 -g <consumer-group>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumerStatus -n master1.teambition.local:9876 -g GID-TB-VERSION
```

### 4. Message Query

#### Query Message by ID

Query message consumption status by message ID:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgById -i <message-id> -n localhost:9876 -t <topic>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgById -i C0A8822F00002A9F00000008AE78670F -n localhost:9876 -t topic
```

#### Query Message by Key

Query messages by message key:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgByKey -n master1.teambition.local:9876 -t <topic-name> -k <message-key>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgByKey -n master1.teambition.local:9876 -t tb-app-eventbus -k order-12345
```

#### Query Message by Offset

Query messages by offset:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgByOffset -n master1.teambition.local:9876 -t <topic-name> -b <broker-name> -i <queue-id> -o <offset>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgByOffset -n master1.teambition.local:9876 -t tb-app-eventbus -b broker-a -i 0 -o 1000
```

**Note:** Broker name can be queried via clusterList command.

#### Read Message Body File

Read message body directly from file system:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- cat /tmp/rocketmq/msgbodys/<message-id>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- cat /tmp/rocketmq/msgbodys/C0A8822F00002A9F00000008AE78670F
```

### 5. Message Management

#### Reset Consumer Offset

Clear all accumulated messages for a consumer group:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin resetOffsetByTime -n localhost:9876 -g <consumer-group> -t <topic> -s -1
```

**Note:** The `-s -1` parameter means reset to the latest offset (clear all backlog).

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin resetOffsetByTime -n localhost:9876 -g GID-TB-VERSION -t teambition-core-eventbus -s -1
```

### 6. Topic Statistics

#### View All Topic Statistics

View topic subscription relationships, TPS, accumulation, 24h read/write totals:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin statsAll -n master1.teambition.local:9876
```

#### View Active Topics Only

Only show active topics:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin statsAll -n master1.teambition.local:9876 -a
```

### 7. Testing Commands

#### Send Test Message

Send a test message to a topic:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin sendMessage -n master1.teambition.local:9876 -t <topic-name> -p "test message body"
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin sendMessage -n master1.teambition.local:9876 -t tb-app-eventbus -p "test message"
```

#### Consume Messages (for Testing)

Consume messages from a topic for testing:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumeMessage -n master1.teambition.local:9876 -t <topic-name> -g <consumer-group>
```

Example:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumeMessage -n master1.teambition.local:9876 -t tb-app-eventbus -g GID-TB-VERSION
```

## Parameters

- `-n`: Nameserver address (default: master1.teambition.local:9876 or localhost:9876)
- `-t`: Topic name
- `-g`: Consumer group name
- `-i`: Message ID or queue ID
- `-k`: Message key
- `-b`: Broker name (not broker address)
- `-o`: Offset value
- `-s`: Timestamp or offset (-1 means latest)
- `-r`: Number of read queues
- `-w`: Number of write queues
- `-c`: Cluster name
- `-p`: Message body or print flag
- `-a`: Amount or active flag
- `-m`: More information flag

## Common Use Cases

### Check Message Accumulation

1. Query consumer progress:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumerProgress -n localhost:9876
```

2. Look for high **Diff total** values which indicate message backlog.

### Debug Consumer Issues

1. Check consumer status:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumerStatus -n master1.teambition.local:9876 -g <consumer-group>
```

2. Verify subscription relationships are consistent.

### Clear Message Backlog

When consumer has accumulated too many messages:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin resetOffsetByTime -n localhost:9876 -g <consumer-group> -t <topic> -s -1
```

### Create New Topic

When you need to create a new topic:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin updateTopic -n master1.teambition.local:9876 -t <topic-name> -c <cluster-name> -r 8 -w 8
```

### Find Message by Key

When you know the message key but not the message ID:

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgByKey -n master1.teambition.local:9876 -t <topic-name> -k <message-key>
```

## Output

- **clusterList**: Cluster information, broker details, TPS
- **topiclist**: List of all topics in the cluster
- **topicStatus**: Topic partition information, min/max offset
- **topicRoute**: Topic routing information (broker addresses)
- **consumerProgress**: Consumer group progress, accumulated message count (Diff total)
- **consumerStatus**: Consumer subscription details and status
- **queryMsgById**: Message details including body, properties, and consumption status
- **queryMsgByKey**: List of messages matching the key
- **queryMsgByOffset**: Message details at specific offset
- **statsAll**: Topic statistics including TPS, accumulation, and 24h totals

## Reference

For more commands, see: https://rocketmq.apache.org/zh/docs/deploymentOperations/02admintool/

## Examples

### View cluster information

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin clusterList -n master1.teambition.local:9876
```

### List all topics

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin topiclist -n master1.teambition.local:9876
```

### Create a new topic

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin updateTopic -n master1.teambition.local:9876 -t new-topic -c DefaultCluster -r 16 -w 16
```

### Check specific topic status

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin topicStatus -n master1.teambition.local:9876 -t tb-app-eventbus
```

### Check consumer message accumulation

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin consumerProgress -n localhost:9876
```

### Query specific message by ID

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgById -i C0A8822F00002A9F00000008AE78670F -n localhost:9876 -t topic
```

### Query messages by key

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin queryMsgByKey -n master1.teambition.local:9876 -t tb-app-eventbus -k order-12345
```

### View topic statistics

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin statsAll -n master1.teambition.local:9876
```

### Clear consumer backlog

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin resetOffsetByTime -n localhost:9876 -g GID-TB-VERSION -t teambition-core-eventbus -s -1
```

### Send test message

```bash
kubectl -n kube-system exec -it rocketmq-master1.teambition.local -- ./mqadmin sendMessage -n master1.teambition.local:9876 -t tb-app-eventbus -p "test message"
```
