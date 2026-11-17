---
name: performance-testing
description: 性能与压测：用 k6（推荐，JS 脚本）或 Locust（Python）做负载/压力/尖峰/容量测试，度量吞吐、p95/p99 延迟与错误率，并设 CI 阈值门禁
source:
  type: derived
  repo: skills-repo/software-tester
  path: skills/performance-testing/SKILL.md
  version: 1.0.0
  updated: 2026-08-12
  url: https://skills.sh/grafana/skills/k6
metadata:
  category: 性能测试
  platform: 性能
  difficulty: 入门
---

# 性能与压测

> 用 k6 / Locust 对接口或服务做性能验证，输出可量化的吞吐、延迟与错误率指标，并作为 CI 门禁。改编自官方 Grafana k6 技能（skills.sh/grafana/skills/k6）。

## 能力

- **测试类型**：负载（load）/ 压力（stress）/ 尖峰（spike）/ 容量（soak）四类场景
- **工具**：k6（脚本即代码，推荐）、Locust（Python）
- **指标**：吞吐（RPS/QPS）、延迟（p50/p95/p99，关注长尾 p99）、错误率、资源占用
- **门禁**：`thresholds` 写进脚本，失败即非零退出，可作 merge gate

## 使用方式

```
/performance-testing 给 /api/health 加一个 200 VU 的压测，p95<500ms
/performance-testing 用 Locust 跑 100 并发 1 分钟
/performance-testing 给下单接口做容量测试，验证内存不泄漏
```

## 工作流

1. 明确目标：预期负载？找拐点？验证 SLA？
2. 选工具（k6 推荐），写脚本（stages + thresholds）
3. 在独立环境运行，避免打挂生产/共享环境
4. 读取吞吐/延迟/错误率，对照阈值判定通过/失败
5. 输出性能报告（见 [references/reporting.md](../../references/reporting.md)）

## k6 骨架（独立可用）

```js
import http from 'k6/http';
import { check } from 'k6';
import { Rate } from 'k6/metrics';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '1m',  target: 50 },
    { duration: '30s', target: 200 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('http://localhost:8080/api/health');
  check(res, { 'status 200': (r) => r.status === 200 });
}
```

运行：`k6 run script.js`

## 适用场景

- 上线前容量评估、性能退化防护、SLA 验证
- 接口/服务层性能基线建立

## 限制

- 压测需独立环境，禁止对生产/未授权目标施压
- 关注接口/服务层；前端渲染性能、数据库专项调优不在范围
- 完整方法论见整库 [references/performance-testing.md](../../references/performance-testing.md)
