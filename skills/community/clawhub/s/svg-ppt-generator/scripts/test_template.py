#!/usr/bin/env python3
"""Test the template engine — generate an 8-page PPT with every layout type."""

import os, sys

# Ensure the skill directory is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template_engine import generate_from_template

TEST_SLIDES = [
    {
        "type": "cover",
        "title": "2026 Cloud Strategy",
        "subtitle": "Annual Infrastructure Review & Roadmap",
        "date": "2026-03-29",
    },
    {
        "type": "section",
        "number": 1,
        "title": "Current State Analysis",
        "subtitle": "Where we are today",
    },
    {
        "type": "content",
        "tag": "OVERVIEW",
        "title": "Key Infrastructure Highlights",
        "bullets": [
            {"key": "Uptime", "val": "99.97% over the past 12 months across all regions"},
            {"key": "Cost Reduction", "val": "18% YoY through reserved instances and right-sizing"},
            "Migrated 42 services to containerised workloads on EKS",
            "Completed SOC 2 Type II certification in Q4 2025",
            "Launched edge caching in 5 new regions (APAC, LATAM)",
        ],
    },
    {
        "type": "table_data",
        "tag": "DATA",
        "title": "Service Health Scorecard",
        "headers": ["Service", "SLA", "P99 Latency", "Status"],
        "rows": [
            ["API Gateway",      "99.99%", "45 ms",  "Healthy"],
            ["Auth Service",     "99.95%", "120 ms", "Healthy"],
            ["Data Pipeline",    "99.90%", "2.1 s",  "Warning"],
            ["ML Inference",     "99.80%", "350 ms", "Healthy"],
            ["Notification Hub", "99.97%", "80 ms",  "Healthy"],
        ],
    },
    {
        "type": "two_column",
        "tag": "COMPARISON",
        "title": "Architecture Evolution",
        "left_title": "Before (2024)",
        "right_title": "After (2026)",
        "left_items": [
            "Monolithic EC2 fleet",
            "Manual scaling policies",
            "Single-region deployment",
            "SSH-based operations",
        ],
        "right_items": [
            "Microservices on EKS",
            "KEDA event-driven autoscaling",
            "Multi-region active-active",
            "GitOps with ArgoCD",
        ],
    },
    {
        "type": "stats",
        "tag": "KPI",
        "title": "Q1 2026 Performance Metrics",
        "stats": [
            {"value": "99.97%", "label": "Uptime",         "desc": "+0.12% vs Q4"},
            {"value": "42 ms",  "label": "Avg Latency",    "desc": "-15% vs Q4"},
            {"value": "12.4K",  "label": "Daily Deploys",  "desc": "Across all envs"},
            {"value": "$1.2M",  "label": "Monthly Spend",  "desc": "-18% YoY"},
        ],
    },
    {
        "type": "cards",
        "tag": "INITIATIVES",
        "title": "2026 Strategic Priorities",
        "cards": [
            {
                "title": "Zero-Trust Security",
                "items": [
                    "mTLS everywhere by Q2",
                    "SPIFFE/SPIRE identity mesh",
                    "Continuous compliance scans",
                ],
            },
            {
                "title": "AI/ML Platform",
                "items": [
                    "Bedrock-native RAG pipelines",
                    "Real-time feature store",
                    "Model observability dashboard",
                ],
            },
            {
                "title": "Cost Optimisation",
                "items": [
                    "Graviton4 migration wave",
                    "Spot fleet for batch jobs",
                    "FinOps self-service portal",
                ],
            },
        ],
    },
    {
        "type": "closing",
        "title": "Thank You",
        "subtitle": "Questions & Discussion",
    },
]


def main():
    out_dir = '/tmp/template_test'
    os.makedirs(out_dir, exist_ok=True)

    for theme in ('dark_tech', 'light_corporate'):
        out = os.path.join(out_dir, f'test_{theme}.pptx')
        print(f'\nGenerating {theme} ...')
        generate_from_template(TEST_SLIDES, out, theme=theme)
        size_kb = os.path.getsize(out) / 1024
        print(f'  -> {out}  ({size_kb:.0f} KB, {len(TEST_SLIDES)} slides)')

    print('\nDone.')


if __name__ == '__main__':
    main()
