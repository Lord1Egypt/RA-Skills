# 性能与压测（Performance & Load Testing）

> 对接口/服务做性能验证：负载（load）、压力（stress）、尖峰（spike）、容量（soak）测试，用 k6（推荐，JS 脚本）或 Locust（Python）度量吞吐、延迟与错误率，并设阈值门禁。

## 何时使用

- 用户说「加个压测」「看这个接口能扛多少 QPS」「性能回归测试」「p95 延迟门禁」
- 上线前容量评估、性能退化防护、SLA 验证

## k6（推荐，脚本即代码）

### 安装

```bash
brew install k6        # macOS
```

### 脚本骨架

```js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   //  ramp-up 负载
    { duration: '1m',  target: 50 },   //  持续
    { duration: '30s', target: 200 },  //  压力
    { duration: '30s', target: 0 },    //  退出
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  //  p95 < 500ms
    http_req_failed: ['rate<0.01'],    //  错误率 < 1%
  },
};

export default function () {
  const res = http.get('http://localhost:8080/api/health');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

运行：`k6 run script.js`

## Locust（Python）

```python
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)
    @task
    def health(self):
        self.client.get('/api/health')
```

运行：`locust -f locustfile.py --headless -u 100 -r 10 -t 1m`

## 关键指标

- **吞吐（RPS/QPS）**：单位时间请求数。
- **延迟**：p50 / p95 / p99，关注长尾 p99 而非平均。
- **错误率**：失败请求占比，阈值通常 < 1%。
- **资源**：CPU/内存/连接数，定位瓶颈。

## 测试类型

| 类型 | 目的 | 配置 |
|------|------|------|
| Load | 预期负载下表现 | 稳定目标用户数 |
| Stress | 找拐点/上限 | 持续加压到崩溃 |
| Spike | 突发流量韧性 | 瞬时拉高再回落 |
| Soak | 内存泄漏/长稳 | 中等负载跑数小时 |

## 阈值门禁（CI）

- 把 `thresholds` 写进脚本，失败即非零退出，可作 merge gate。
- 与 [references/test-strategy.md](test-strategy.md) 的 CI 门禁联动。

## 相关子技能（L3）

- 落地为性能 / 压测动作（k6 / Locust 脚本与阈值门禁）→ [skills/performance-testing/SKILL.md](../skills/performance-testing/SKILL.md)

## 限制

- 压测需有独立环境，避免打挂生产/共享环境。
- 本 playbook 关注接口/服务层；前端渲染性能、数据库专项调优不在范围。
