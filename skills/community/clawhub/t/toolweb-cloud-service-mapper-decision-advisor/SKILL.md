---
name: Multi-Cloud Service Mapper & Decision Advisor
description: AI-powered cloud service mapping and provider recommendation across Azure, AWS, and Google Cloud.
---

# Overview

The Multi-Cloud Service Mapper & Decision Advisor is an intelligent API that analyzes workload requirements and recommends optimal cloud services and providers. Built for organizations evaluating multi-cloud strategies, this tool uses AI to map business needs to Azure, AWS, and Google Cloud offerings—helping teams make data-driven infrastructure decisions.

Key capabilities include workload analysis with custom priorities, service category discovery, and provider metadata retrieval. The API considers team size, industry context, current cloud environment, and business priorities to deliver tailored recommendations. Ideal for cloud architects, DevOps teams, and organizations undergoing cloud migration or multi-cloud transformation initiatives.

Whether you're migrating from on-premises infrastructure, evaluating a second cloud platform, or optimizing service selection across providers, this tool reduces analysis time and ensures alignment with organizational constraints and goals.

## Usage

**Request:** Analyze a microservices workload running on Kubernetes with cost and performance priorities.

```json
{
  "workload_description": "Kubernetes-based microservices platform handling 10,000 requests per second with relational and NoSQL data stores",
  "selected_services": ["container-orchestration", "database", "api-gateway"],
  "current_cloud": "AWS",
  "priorities": ["cost-optimization", "performance", "security"],
  "team_size": "12",
  "industry": "fintech",
  "sessionId": "sess_12345abcde",
  "userId": 1001,
  "timestamp": "2025-01-15T14:30:00Z"
}
```

**Response:**

```json
{
  "analysis_id": "analysis_67890xyz",
  "workload_summary": {
    "description": "Kubernetes-based microservices platform handling 10,000 requests per second with relational and NoSQL data stores",
    "services_analyzed": 3,
    "priorities_considered": 3
  },
  "recommendations": [
    {
      "provider": "AWS",
      "primary_services": [
        {
          "service_name": "EKS",
          "category": "container-orchestration",
          "rationale": "Native Kubernetes service with deep AWS integration and cost optimization tools",
          "confidence_score": 0.95
        },
        {
          "service_name": "RDS + DynamoDB",
          "category": "database",
          "rationale": "Relational and NoSQL hybrid approach with managed scaling",
          "confidence_score": 0.92
        }
      ],
      "overall_match_score": 0.94
    },
    {
      "provider": "Google Cloud",
      "primary_services": [
        {
          "service_name": "GKE",
          "category": "container-orchestration",
          "rationale": "Kubernetes-native platform with strong observability",
          "confidence_score": 0.91
        }
      ],
      "overall_match_score": 0.87
    }
  ],
  "decision_factors": {
    "cost_optimization": "AWS and GCP offer sustained-use discounts; GCP has aggressive pricing",
    "performance": "All three providers support low-latency Kubernetes deployments",
    "security": "Fintech compliance (SOC2, ISO27001) supported across all providers"
  },
  "migration_insights": "Migrating from AWS to multi-cloud is low-risk; GCP GKE provides strong alternative"
}
```

## Endpoints

### POST /api/cloud-mapper/analyze
**Analyze Workload**

Generate multi-cloud service mapping and decision analysis for a given workload.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| workload_description | string | Yes | Detailed description of the workload, infrastructure, and technical requirements |
| selected_services | array[string] | No | List of cloud service categories to analyze (e.g., "container-orchestration", "database", "api-gateway") |
| current_cloud | string \| null | No | Current cloud provider if migrating ("AWS", "Azure", "GCP") |
| priorities | array[string] | No | Business and technical priorities such as "cost-optimization", "performance", "security", "compliance" |
| team_size | string \| null | No | Team size managing the infrastructure (e.g., "5-10", "10-20", "20+") |
| industry | string \| null | No | Industry vertical (e.g., "fintech", "healthcare", "retail", "manufacturing") |
| sessionId | string | Yes | Unique session identifier for tracking and audit purposes |
| userId | integer \| null | No | User ID for multi-tenant tracking and personalization |
| timestamp | string | Yes | ISO 8601 timestamp of the request |

**Response:** Returns analysis object containing recommendations from each provider with confidence scores, service mappings, decision factors, and migration insights.

---

### GET /api/cloud-mapper/services
**Get Services**

Retrieve all supported cloud service categories available for analysis.

**Parameters:** None

**Response:** Returns array of service categories (e.g., "compute", "container-orchestration", "database", "storage", "networking", "security", "analytics", "ai-ml", "serverless", "api-gateway").

---

### GET /api/cloud-mapper/providers
**Get Providers**

Retrieve provider metadata including name, region availability, and supported services.

**Parameters:** None

**Response:** Returns array of provider objects containing metadata for AWS, Azure, and Google Cloud (name, logo, regions, supported_services, documentation_url).

---

### GET /
**Root**

Service health check and API metadata endpoint.

**Parameters:** None

**Response:** Returns service status and basic API information.

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.toolweb.in/security/servicemapper
- **API Docs:** https://api.toolweb.in:8171/docs
