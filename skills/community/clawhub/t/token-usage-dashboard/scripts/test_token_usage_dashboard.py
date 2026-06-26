#!/usr/bin/env python3

from pathlib import Path
from unittest import TestCase, main

import token_usage_dashboard as dashboard_module

from token_usage_dashboard import (
    apply_access_policy,
    build_dashboard_html,
    build_model_table_rows,
    build_summary,
    build_llm_pattern_analysis,
    build_cost_attribution,
    build_optimization_recommendations,
    build_prompt_optimization_engine,
    detect_spikes,
    detect_cost_anomalies,
    evaluate_alert_rules,
    evaluate_realtime_cost_controls,
    forecast_cost,
    parse_provider_list,
    build_multi_provider_aggregation,
    downsample_rows,
    generate_custom_report,
    main as dashboard_main,
    manage_tenant_config,
    model_totals,
    prepare_chart_series,
    resolve_access_policy,
    resolve_multi_tenant_context,
    run_report_scheduler,
)


class TestTokenDashboard(TestCase):
    def test_build_summary(self):
        rows = [
            {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.2}]},
            {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 0.8}, {"modelName": "o3", "cost": 0.5}]},
        ]
        summary = build_summary("codex", rows)
        self.assertEqual(summary["provider"], "codex")
        self.assertEqual(summary["rows"], 2)
        self.assertAlmostEqual(summary["totalCostUSD"], 2.5)
        self.assertEqual(summary["models"][0]["model"], "gpt-5")

    def test_model_totals_aggregates(self):
        rows = [
            {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.2}]},
            {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 0.8}, {"modelName": "o3", "cost": 0.5}]},
        ]
        totals = model_totals(rows)
        self.assertAlmostEqual(totals["gpt-5"], 2.0)
        self.assertAlmostEqual(totals["o3"], 0.5)

    def test_parse_provider_list_dedup_and_validation(self):
        self.assertEqual(parse_provider_list("codex,claude,codex"), ["codex", "claude"])
        with self.assertRaises(RuntimeError):
            parse_provider_list("codex,unknown")

    def test_build_multi_provider_aggregation_normalized_unified_totals(self):
        provider_rows = {
            "codex": [
                {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 2.0}]},
                {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "o3", "cost": 1.0}]},
            ],
            "claude": [
                {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "sonnet", "cost": 3.0}]},
                {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.5}]},
            ],
        }
        agg = build_multi_provider_aggregation(provider_rows)
        self.assertTrue(agg["available"])
        self.assertAlmostEqual(agg["totals"]["grandTotalCostUSD"], 7.5)
        self.assertEqual(agg["providers"][0]["provider"], "claude")
        self.assertAlmostEqual(agg["totals"]["models"]["gpt-5"], 3.5)
        self.assertEqual(len(agg["daily"]), 2)

    def test_dashboard_html_contains_multi_provider_unified_section(self):
        rows = [{"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}]}]
        agg = {
            "available": True,
            "providers": [{"provider": "codex", "totalCostUSD": 4.0}, {"provider": "claude", "totalCostUSD": 3.0}],
            "totals": {"grandTotalCostUSD": 7.0},
            "topModels": [{"model": "gpt-5", "totalCostUSD": 2.5}],
        }
        html = build_dashboard_html("codex", rows, top_models=2, multi_provider_agg=agg)
        self.assertIn("Multi-Provider Unified View", html)
        self.assertIn("Unified Top Models (cross-provider)", html)
        self.assertIn("Aggregated providers total", html)

    def test_summary_includes_pattern_analysis(self):
        rows = [
            {
                "date": "2026-03-01",
                "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}],
                "llmCalls": [{"modelName": "gpt-5", "promptTokens": 10, "completionTokens": 20, "totalTokens": 30, "cost": 0.1, "prompt": "summarize logs"}],
            }
        ]
        summary = build_summary("codex", rows)
        self.assertIn("llmPatternAnalysis", summary)
        self.assertTrue(summary["llmPatternAnalysis"]["available"])
        self.assertIn("costAttribution", summary)
        self.assertTrue(summary["costAttribution"]["available"])
        self.assertIn("optimizationRecommendations", summary)
        self.assertTrue(summary["optimizationRecommendations"]["available"])

    def test_summary_includes_7d_delta(self):
        rows = [
            {
                "date": f"2026-03-{d:02d}",
                "modelBreakdowns": [
                    {"modelName": "gpt-5", "cost": float(d)},
                    {"modelName": "o3", "cost": 1.0 if d >= 8 else 0.0},
                ],
            }
            for d in range(1, 15)
        ]
        summary = build_summary("codex", rows)
        self.assertAlmostEqual(summary["last7dCostUSD"], sum(float(d) + 1.0 for d in range(8, 15)))
        self.assertAlmostEqual(summary["prev7dCostUSD"], sum(float(d) for d in range(1, 8)))
        self.assertIsInstance(summary["last7dDeltaPct"], float)
        self.assertTrue(len(summary["movers"]) >= 2)
        self.assertEqual(summary["movers"][0]["model"], "gpt-5")

    def test_build_llm_pattern_analysis(self):
        rows = [
            {
                "date": "2026-03-01",
                "llmCalls": [
                    {
                        "modelName": "gpt-5",
                        "modelType": "chat",
                        "useCase": "support",
                        "userId": "alice",
                        "projectId": "proj-a",
                        "sessionId": "s1",
                        "promptTokens": 100,
                        "completionTokens": 200,
                        "totalTokens": 300,
                        "cost": 0.9,
                        "latencyMs": 500,
                        "prompt": "Please summarize Taiwan market outlook and risk factors",
                    },
                    {
                        "modelName": "o3",
                        "modelType": "reasoning",
                        "useCase": "analysis",
                        "userId": "bob",
                        "projectId": "proj-b",
                        "sessionId": "s2",
                        "promptTokens": 400,
                        "completionTokens": 120,
                        "totalTokens": 520,
                        "cost": 1.5,
                        "latencyMs": 900,
                        "prompt": "Analyze quarterly trend and optimization plan",
                    },
                ],
            }
        ]
        analysis = build_llm_pattern_analysis(rows)
        self.assertTrue(analysis["available"])
        self.assertEqual(analysis["calls"], 2)
        self.assertIn("dimensions", analysis)
        self.assertTrue(len(analysis["efficiency"]) >= 2)
        self.assertTrue(len(analysis["anonymizedPromptKeywords"]) > 0)

    def test_build_cost_attribution_unallocated_and_dimensions(self):
        rows = [
            {
                "date": "2026-03-01",
                "modelBreakdowns": [{"modelName": "gpt-5", "cost": 3.0}],
                "llmCalls": [
                    {
                        "modelName": "gpt-5",
                        "projectId": "proj-a",
                        "userId": "alice",
                        "department": "eng",
                        "application": "api-gateway",
                        "businessLine": "consumer",
                        "totalTokens": 100,
                        "cost": 1.2,
                    },
                    {
                        "modelName": "o3",
                        "projectId": "proj-b",
                        "userId": "bob",
                        "department": "sales",
                        "application": "crm",
                        "businessLine": "enterprise",
                        "totalTokens": 80,
                        "cost": 0.8,
                    },
                ],
            }
        ]
        attribution = build_cost_attribution(rows)
        self.assertTrue(attribution["available"])
        self.assertAlmostEqual(attribution["totalAttributedCostUSD"], 2.0)
        self.assertAlmostEqual(attribution["unallocatedCostUSD"], 1.0)
        self.assertIn("businessLine", attribution["dimensions"])
        self.assertEqual(attribution["dimensions"]["businessLine"][0]["key"], "consumer")

    def test_build_cost_attribution_share_sort_topn_and_unknown_fallback(self):
        rows = [
            {
                "date": "2026-03-01",
                "llmCalls": [
                    {"projectId": "proj-a", "cost": 3.0, "totalTokens": 30},
                    {"projectId": "proj-b", "cost": 2.0, "totalTokens": 20},
                    {"projectId": "proj-c", "cost": 1.0, "totalTokens": 10},
                    {"projectId": "proj-d", "cost": 0.5, "totalTokens": 5},
                    {"cost": 0.5, "totalTokens": 5},
                ],
            }
        ]
        attribution = build_cost_attribution(rows, top_n=3)
        projects = attribution["dimensions"]["project"]
        self.assertEqual([p["key"] for p in projects], ["proj-a", "proj-b", "proj-c"])
        share_sum = sum(p["sharePct"] for p in attribution["dimensions"]["project"])
        self.assertAlmostEqual(share_sum, 85.71428571428571)

        attribution_all = build_cost_attribution(rows, top_n=10)
        all_projects = attribution_all["dimensions"]["project"]
        self.assertIn("unknown", [p["key"] for p in all_projects])
        self.assertAlmostEqual(sum(p["sharePct"] for p in all_projects), 100.0)

    def test_build_optimization_recommendations_trigger_conditions(self):
        rows = [
            {
                "date": "2026-03-01",
                "llmCalls": [
                    {"projectId": "proj-a", "totalTokens": 100, "cost": 0.5},
                    {"projectId": "proj-a", "totalTokens": 110, "cost": 0.6},
                ] + [{"projectId": "proj-a", "totalTokens": 100, "cost": 0.2} for _ in range(25)],
            }
        ]
        pattern_analysis = {
            "efficiency": [
                {"model": "cheap", "costPer1kTokensUSD": 0.01, "totalTokens": 1000},
                {"model": "expensive", "costPer1kTokensUSD": 0.03, "totalTokens": 1000},
            ],
            "promptTokens": {"p50": 100, "p95": 250},
        }
        attribution = {
            "dimensions": {
                "project": [
                    {"key": "proj-a", "sharePct": 55.0},
                    {"key": "proj-b", "sharePct": 20.0},
                ]
            }
        }
        recs = build_optimization_recommendations(rows, pattern_analysis, attribution)
        self.assertTrue(recs["available"])
        rec_types = {r["type"] for r in recs["recommendations"]}
        self.assertIn("model_rightsizing", rec_types)
        self.assertIn("prompt_optimization", rec_types)
        self.assertIn("batching", rec_types)
        self.assertIn("budget_guardrail", rec_types)

    def test_build_prompt_optimization_engine_and_ab_plan(self):
        rows = [
            {
                "date": "2026-03-01",
                "llmCalls": [
                    {
                        "modelName": "gpt-5",
                        "projectId": "proj-a",
                        "promptTokens": 1000,
                        "completionTokens": 120,
                        "totalTokens": 1120,
                        "cost": 1.3,
                        "prompt": "請幫我分析這一整段歷史 log 並整理出重點與風險，附上完整上下文。",
                    },
                    {
                        "modelName": "gpt-5",
                        "projectId": "proj-a",
                        "promptTokens": 900,
                        "completionTokens": 130,
                        "totalTokens": 1030,
                        "cost": 1.1,
                        "prompt": "請幫我分析這一整段歷史 log 並整理出重點與風險，附上完整上下文。",
                    },
                ],
            }
        ]
        pattern = build_llm_pattern_analysis(rows)
        engine = build_prompt_optimization_engine(rows, pattern)
        self.assertTrue(engine["available"])
        self.assertGreaterEqual(len(engine["highConsumptionPrompts"]), 1)
        self.assertGreaterEqual(len(engine["abTests"]), 1)
        first = engine["highConsumptionPrompts"][0]
        self.assertIn("suggestions", first)
        self.assertTrue(any(s["type"] == "model_rightsizing" for s in first["suggestions"]))

    def test_build_summary_normalizes_call_records_once(self):
        from unittest.mock import patch

        rows = [{
            "date": "2026-03-01",
            "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}],
            "llmCalls": [{"modelName": "gpt-5", "totalTokens": 10, "cost": 0.2}],
        }]

        with patch("token_usage_dashboard._normalize_call_records", wraps=dashboard_module._normalize_call_records) as normalize_spy:
            summary = build_summary("codex", rows)
        self.assertIn("costAttribution", summary)
        self.assertIn("promptOptimizationEngine", summary)
        self.assertEqual(normalize_spy.call_count, 1)

    def test_detect_spikes(self):
        rows = [
            {"date": f"2026-03-{d:02d}", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 10.0}]}
            for d in range(1, 9)
        ]
        rows.append({"date": "2026-03-09", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 30.0}]})

        spikes = detect_spikes(rows, lookback_days=7, threshold_mult=2.0)
        self.assertEqual(len(spikes), 1)
        self.assertEqual(spikes[0]["date"], "2026-03-09")

    def test_build_summary_respects_spike_params(self):
        rows = [
            {"date": f"2026-03-{d:02d}", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 10.0}]}
            for d in range(1, 9)
        ]
        rows.append({"date": "2026-03-09", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 15.0}]})

        summary_default = build_summary("codex", rows)
        summary_sensitive = build_summary("codex", rows, spike_lookback_days=7, spike_threshold_mult=1.2)
        self.assertEqual(len(summary_default["spikes"]), 0)
        self.assertEqual(len(summary_sensitive["spikes"]), 1)

    def test_forecast_and_alerts(self):
        rows = [
            {"date": f"2026-03-{d:02d}", "modelBreakdowns": [{"modelName": "gpt-5", "cost": float(d)}]}
            for d in range(1, 16)
        ]
        f7 = forecast_cost(rows, horizon_days=7, lookback_days=14)
        self.assertEqual(f7["horizonDays"], 7)
        self.assertGreater(f7["predictedTotalCostUSD"], 0.0)

        anomalies = detect_cost_anomalies(rows + [{"date": "2026-03-16", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 100.0}]}], lookback_days=7, z_threshold=1.5)
        self.assertGreaterEqual(len(anomalies), 1)

        alerts = evaluate_alert_rules(
            rows,
            f7,
            anomalies,
            config={
                "rules": {"budgetThresholdUSD": 10, "budgetForecastPct": 50, "anomalyCountThreshold": 1},
                "notificationChannels": ["email", "discord:webhook"],
            },
        )
        self.assertTrue(len(alerts["triggered"]) >= 1)
        self.assertIn("email", alerts["notificationChannels"])

    def test_build_summary_includes_forecast_and_alerts(self):
        rows = [
            {"date": f"2026-03-{d:02d}", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 5.0}]}
            for d in range(1, 15)
        ]
        summary = build_summary("codex", rows, alert_config={"rules": {"budgetThresholdUSD": 20, "budgetForecastPct": 80}})
        self.assertIn("forecast", summary)
        self.assertIn("costAnomalies", summary)
        self.assertIn("alerts", summary)
        self.assertIn("next7Days", summary["forecast"])

    def test_evaluate_realtime_cost_controls_triggers_multi_layers(self):
        rows = [
            {
                "date": "2026-03-01",
                "modelBreakdowns": [{"modelName": "gpt-5", "cost": 6.0}],
                "llmCalls": [
                    {"projectId": "proj-a", "cost": 4.0, "totalTokens": 100},
                    {"projectId": "proj-b", "cost": 1.0, "totalTokens": 30},
                ],
            }
        ]
        controls = evaluate_realtime_cost_controls(
            rows,
            forecast_7d={"predictedTotalCostUSD": 20.0},
            anomalies=[{"date": "2026-03-01", "zScore": 3.1}],
            config={
                "layers": [
                    {"id": "global-forecast", "metric": "forecast_7d_total_cost", "threshold": 10, "action": "degrade", "routeToModel": "o3-mini"},
                    {"id": "project-cap", "metric": "dimension_cost", "dimension": "project", "key": "proj-a", "threshold": 3.0, "action": "switch_model", "routeToModel": "gpt-4.1-mini"},
                    {"id": "anomaly-circuit", "metric": "anomaly_count", "threshold": 1, "action": "stop_calls", "stopReason": "anomaly_spike"},
                ]
            },
        )
        self.assertTrue(controls["available"])
        self.assertEqual(len(controls["layers"]), 3)
        self.assertEqual(len(controls["triggeredActions"]), 3)
        self.assertIn("project:proj-a", [x["scope"] for x in controls["triggeredActions"]])

    def test_summary_and_dashboard_include_realtime_cost_control_section(self):
        rows = [{"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 3.0}], "llmCalls": [{"projectId": "proj-a", "cost": 2.0, "totalTokens": 50}]}]
        summary = build_summary(
            "codex",
            rows,
            cost_control_config={
                "layers": [
                    {"id": "global-cap", "metric": "actual_total_cost", "threshold": 2.5, "action": "degrade", "routeToModel": "o3-mini"}
                ]
            },
        )
        self.assertIn("realTimeCostControls", summary)
        self.assertTrue(summary["realTimeCostControls"]["available"])

        html = build_dashboard_html("codex", rows, top_models=2, cost_control_config={"layers": [{"id": "global-cap", "metric": "actual_total_cost", "threshold": 2.5, "action": "degrade"}]})
        self.assertIn("Real-time Cost Control Strategy", html)
        self.assertIn("Triggered Control Actions", html)


    def test_dashboard_html_contains_all_pattern_sections(self):
        rows = [{
            "date": "2026-03-01",
            "modelBreakdowns": [{"modelName": "gpt-5", "cost": 3.0}],
            "llmCalls": [{
                "modelName": "gpt-5", "modelType": "chat", "projectId": "proj-a", "useCase": "qa", "userId": "alice", "sessionId": "sess-1", "workflowId": "wf-1",
                "promptTokens": 10, "completionTokens": 20, "totalTokens": 30, "cost": 0.2, "latencyMs": 200,
                "prompt": "contact me at user@example.com and trace 1234567890 id 550e8400-e29b-41d4-a716-446655440000"
            }]
        }]
        html = build_dashboard_html("codex", rows, top_models=2)
        for text in [
            "Prompt tokens", "Completion tokens", "By Model Type", "By Project",
            "Hotspots · Top API Calls", "Hotspots · Top Sessions", "Hotspots · Top Workflows",
            "Anonymized Prompt Keywords", "Cost Attribution & Optimization Recommendations",
            "Optimization Recommendations", "Attribution by Department", "Attribution by Business Line",
            "Prompt 優化建議引擎 · High-Consumption Prompt Families", "Prompt 優化建議引擎 · A/B Testing Plans"
        ]:
            self.assertIn(text, html)

    def test_anonymization_masks_sensitive_strings(self):
        rows = [{
            "date": "2026-03-01",
            "llmCalls": [{
                "modelName": "gpt-5", "promptTokens": 1, "completionTokens": 1, "totalTokens": 2, "cost": 0.01,
                "prompt": "Email user@example.com uuid 550e8400-e29b-41d4-a716-446655440000 number 987654321012"
            }]
        }]
        analysis = build_llm_pattern_analysis(rows)
        kws = {x["keyword"] for x in analysis["anonymizedPromptKeywords"]}
        self.assertIn("<email>", kws)
        self.assertIn("<uuid>", kws)
        self.assertIn("<number>", kws)
        for forbidden in ["user", "example", "550e8400", "987654321012"]:
            self.assertFalse(any(forbidden in k for k in kws))

    def test_large_dataset_performance_smoke(self):
        import time
        rows = []
        for d in range(1, 2001):
            rows.append({
                "date": f"2026-01-{((d - 1) % 28) + 1:02d}",
                "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}],
                "llmCalls": [{"modelName": "gpt-5", "promptTokens": 100, "completionTokens": 200, "totalTokens": 300, "cost": 0.1, "sessionId": f"s{d}", "workflowId": f"w{d}", "prompt": f"task {d}"}],
            })
        t0 = time.perf_counter()
        html = build_dashboard_html("codex", rows, top_models=3, chart_max_points=300)
        elapsed = time.perf_counter() - t0
        self.assertIn("LLM Usage Pattern Deep Analysis", html)
        self.assertLess(elapsed, 6.0)

    def test_dashboard_html_contains_spike_visuals(self):
        rows = [
            {"date": f"2026-03-{d:02d}", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 10.0}]}
            for d in range(1, 9)
        ]
        rows.append({"date": "2026-03-09", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 30.0}]})
        html = build_dashboard_html("codex", rows, top_models=3, spike_lookback_days=7, spike_threshold_mult=2.0)
        self.assertIn("const spikeByDate", html)
        self.assertIn("⚠ Spike", html)
        self.assertIn("Daily Cost Spikes", html)
        self.assertIn("spike-row-2026-03-09", html)
        self.assertIn("scrollIntoView", html)
        self.assertIn("const dayBreakdownByDate", html)
        self.assertIn("Selected Day Model Breakdown", html)
        self.assertIn("DoD Δ", html)
        self.assertIn("renderSelectedDay", html)
        self.assertIn("id=\"spikesBody\"", html)
        self.assertIn("focusSpikeDate", html)
        self.assertIn("focusDate", html)
        self.assertIn("stepDate", html)
        self.assertIn("jumpSpike", html)
        self.assertIn("spikeOnlyToggle", html)
        self.assertIn("toggleSpikeOnlyMode", html)
        self.assertIn("toggleKeyboardHelp", html)
        self.assertIn("resetToLatestDay", html)
        self.assertIn("copyDeepLink", html)
        self.assertIn("id=\"copyLinkBtn\"", html)
        self.assertIn("id=\"selectedDayMeta\"", html)
        self.assertIn("Cost Forecast & Anomaly Alerts", html)
        self.assertIn("Detected Cost Anomalies", html)
        self.assertIn("Triggered Alerts", html)
        self.assertIn("LLM Usage Pattern Deep Analysis", html)
        self.assertIn("id=\"sortByDodToggle\"", html)
        self.assertIn("id=\"showOnlyChangesToggle\"", html)
        self.assertIn("sortByDodMode", html)
        self.assertIn("showOnlyChangesMode", html)
        self.assertIn("toggleDodSortMode", html)
        self.assertIn("toggleChangesOnlyMode", html)
        self.assertIn("ev.key === 'd'", html)
        self.assertIn("ev.key === 'x'", html)
        self.assertIn("sortDod", html)
        self.assertIn("changesOnly", html)
        self.assertIn("ev.key === 'c'", html)
        self.assertIn("ev.key === 'Home'", html)
        self.assertIn("ev.key === 'End'", html)
        self.assertIn("dod-pos", html)
        self.assertIn("dod-neg", html)
        self.assertIn("model-top", html)
        self.assertIn("Escape", html)
        self.assertIn("id=\"kbdHelp\"", html)
        self.assertIn("getInitialStateFromHash", html)
        self.assertIn("history.replaceState", html)
        self.assertIn("window.addEventListener('keydown'", html)
        self.assertIn("isEditable", html)
        self.assertIn("selectedSpikeDate", html)

    def test_prepare_chart_series_groups_other(self):
        rows = [
            {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "a", "cost": 3}, {"modelName": "b", "cost": 1}]},
            {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "a", "cost": 2}, {"modelName": "c", "cost": 4}]},
        ]
        labels, series, totals = prepare_chart_series(rows, top_models=1)
        self.assertEqual(labels, ["2026-03-01", "2026-03-02"])
        self.assertEqual(series["a"], [3.0, 2.0])
        self.assertEqual(series["Other"], [1.0, 4.0])
        self.assertEqual(totals, [4.0, 6.0])

    def test_build_model_table_rows_collapses_tail(self):
        ranked = [("a", 50.0), ("b", 30.0), ("c", 20.0)]
        html = build_model_table_rows(ranked, grand_total=100.0, max_rows=2)
        self.assertIn("<td>1</td><td>a</td>", html)
        self.assertIn("<td>2</td><td>b</td>", html)
        self.assertIn("Remaining 1 models", html)

    def test_dashboard_html_respects_max_table_rows(self):
        rows = [
            {
                "date": "2026-03-01",
                "modelBreakdowns": [
                    {"modelName": "m1", "cost": 3},
                    {"modelName": "m2", "cost": 2},
                    {"modelName": "m3", "cost": 1},
                ],
            }
        ]
        html = build_dashboard_html("codex", rows, top_models=3, max_table_rows=2)
        self.assertIn("Showing up to top 2 models", html)
        self.assertIn("Remaining 1 models", html)

    def test_downsample_rows_keeps_bounds(self):
        rows = [{"date": f"2026-01-{d:02d}", "modelBreakdowns": []} for d in range(1, 32)]
        sampled = downsample_rows(rows, max_points=10)
        self.assertEqual(len(sampled), 10)
        self.assertEqual(sampled[0]["date"], rows[0]["date"])
        self.assertEqual(sampled[-1]["date"], rows[-1]["date"])

    def test_dashboard_html_shows_downsample_hint(self):
        rows = [
            {"date": f"2026-03-{d:02d}", "modelBreakdowns": [{"modelName": "m1", "cost": float(d)}]}
            for d in range(1, 21)
        ]
        html = build_dashboard_html("codex", rows, top_models=3, chart_max_points=8)
        self.assertIn("Chart points: 8/20", html)

    def test_custom_report_generation_metrics_models_granularity(self):
        rows = [
            {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 3.0}, {"modelName": "o3", "cost": 1.0}]},
            {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 2.0}]},
            {"date": "2026-03-08", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 5.0}]},
        ]
        report = generate_custom_report(rows, metrics=["total_cost", "active_models", "avg_cost_per_model"], models=["gpt-5"], granularity="monthly")
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0]["period"], "2026-03")
        self.assertAlmostEqual(report[0]["totalCostUSD"], 10.0)

    def test_dashboard_html_contains_custom_report_builder(self):
        rows = [
            {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}]},
            {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "o3", "cost": 2.0}]},
        ]
        html = build_dashboard_html("codex", rows, top_models=2)
        self.assertIn("Custom Report Builder", html)
        self.assertIn("id=\"reportGranularity\"", html)
        self.assertIn("id=\"generateReportBtn\"", html)
        self.assertIn("id=\"downloadReportCsvBtn\"", html)
        self.assertIn("id=\"customReportBody\"", html)
        self.assertIn("generateCustomReportRows", html)
        self.assertIn("initCustomReportBuilder", html)

    def test_apply_access_policy_viewer_hides_breakdown(self):
        rows = [
            {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 3.0}, {"modelName": "o3", "cost": 1.0}]},
        ]
        _, policy = resolve_access_policy("viewer", None, None)
        filtered = apply_access_policy(rows, policy)
        self.assertEqual(filtered[0]["modelBreakdowns"], [])
        self.assertAlmostEqual(filtered[0]["totalCost"], 4.0)

    def test_apply_access_policy_allowed_models(self):
        rows = [
            {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 3.0}, {"modelName": "o3", "cost": 1.0}]},
        ]
        policy = {
            "canViewModelBreakdown": True,
            "canViewModelNames": True,
            "allowedModels": ["o3"],
        }
        filtered = apply_access_policy(rows, policy)
        self.assertEqual(len(filtered[0]["modelBreakdowns"]), 1)
        self.assertEqual(filtered[0]["modelBreakdowns"][0]["modelName"], "o3")
        self.assertAlmostEqual(filtered[0]["totalCost"], 1.0)


    def test_resolve_multi_tenant_context_isolates_org_data(self):
        payload = {
            "organizations": {
                "org-a": {"daily": [{"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}]}]},
                "org-b": {"daily": [{"date": "2026-03-01", "modelBreakdowns": [{"modelName": "o3", "cost": 9.0}]}]},
            }
        }
        import json, tempfile, os
        cfg = {
            "organizations": {
                "org-a": {
                    "defaultRole": "viewer",
                    "users": {"alice": {"role": "admin", "group": "eng"}},
                    "groups": {"eng": {"dashboardViews": ["eng-core"]}},
                    "dashboardViews": {"eng-core": {"allowedModels": ["gpt-5"]}},
                },
                "org-b": {"users": {}, "groups": {}, "dashboardViews": {}},
            }
        }
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            f.write(json.dumps(cfg))
            path = f.name
        try:
            rows, role, policy, meta = resolve_multi_tenant_context(payload, path, 'org-a', None, 'alice', 'eng-core')
            self.assertEqual(role, 'admin')
            self.assertEqual(meta['organizationId'], 'org-a')
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['modelBreakdowns'][0]['modelName'], 'gpt-5')
            self.assertEqual(policy.get('allowedModels'), ['gpt-5'])
        finally:
            os.unlink(path)

    def test_manage_tenant_config_user_and_view(self):
        import json, tempfile, os
        cfg = {
            "organizations": {
                "org-a": {"users": {}, "groups": {"analytics": {"dashboardViews": []}}, "dashboardViews": {}}
            }
        }
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            f.write(json.dumps(cfg))
            path = f.name
        try:
            manage_tenant_config(path, 'org-a', 'create', 'bob', 'analyst', 'analytics', None, None, None, None, None)
            manage_tenant_config(path, 'org-a', None, None, None, None, 'create', 'ops-view', 'gpt-5,o3', 30, None)
            result = manage_tenant_config(path, 'org-a', None, None, None, None, 'assign', 'ops-view', None, None, 'analytics')
            self.assertIn('bob', result['users'])
            self.assertIn('ops-view', result['views'])
            data = json.loads(Path(path).read_text())
            self.assertIn('ops-view', data['organizations']['org-a']['groups']['analytics']['dashboardViews'])
        finally:
            os.unlink(path)

    def test_manage_mode_does_not_require_input_payload(self):
        import json, os, sys, tempfile
        from unittest.mock import patch

        cfg = {"organizations": {"org-a": {"users": {}, "groups": {}, "dashboardViews": {}}}}
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            f.write(json.dumps(cfg))
            path = f.name
        try:
            argv = [
                "token_usage_dashboard.py",
                "--tenant-config", path,
                "--org-id", "org-a",
                "--manage-users", "list",
            ]
            with patch.object(sys, "argv", argv), patch("token_usage_dashboard.load_payload", side_effect=RuntimeError("should not load payload")):
                rc = dashboard_main()
            self.assertEqual(rc, 0)
        finally:
            os.unlink(path)

    def test_multi_tenant_user_without_group_is_deny_by_default(self):
        import json, os, tempfile

        payload = {"organizations": {"org-a": {"daily": [{"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 2.0}]}]}}}
        cfg = {
            "organizations": {
                "org-a": {
                    "users": {"alice": {"role": "analyst"}},
                    "groups": {},
                    "dashboardViews": {"team": {"allowedModels": ["gpt-5"]}},
                }
            }
        }
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            f.write(json.dumps(cfg))
            path = f.name
        try:
            with self.assertRaises(RuntimeError):
                resolve_multi_tenant_context(payload, path, "org-a", None, "alice", "team")
            rows, role, policy, _ = resolve_multi_tenant_context(payload, path, "org-a", None, "alice", None)
            self.assertEqual(role, "analyst")
            self.assertEqual(policy.get("allowedModels"), [])
            filtered = apply_access_policy(rows, policy)
            self.assertAlmostEqual(filtered[0]["totalCost"], 0.0)
        finally:
            os.unlink(path)

    def test_multi_tenant_role_override_requires_allow_flag(self):
        import json, os, tempfile

        payload = {"organizations": {"org-a": {"daily": [{"date": "2026-03-01", "modelBreakdowns": []}]}}}
        cfg = {
            "organizations": {
                "org-a": {
                    "users": {"alice": {"role": "viewer", "defaultDashboard": "team"}},
                    "groups": {},
                    "dashboardViews": {"team": {"allowedModels": ["gpt-5"]}},
                }
            }
        }
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            f.write(json.dumps(cfg))
            path = f.name
        try:
            _, role_ignored, _, _ = resolve_multi_tenant_context(payload, path, "org-a", "admin", "alice", None)
            _, role_override, _, _ = resolve_multi_tenant_context(payload, path, "org-a", "admin", "alice", None, allow_role_override=True)
            self.assertEqual(role_ignored, "viewer")
            self.assertEqual(role_override, "admin")
        finally:
            os.unlink(path)

    def test_assign_nonexistent_view_fails(self):
        import json, os, tempfile

        cfg = {
            "organizations": {
                "org-a": {"users": {}, "groups": {"analytics": {"dashboardViews": []}}, "dashboardViews": {}}
            }
        }
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as f:
            f.write(json.dumps(cfg))
            path = f.name
        try:
            with self.assertRaises(RuntimeError):
                manage_tenant_config(path, "org-a", None, None, None, None, "assign", "missing-view", None, None, "analytics")
        finally:
            os.unlink(path)

    def test_run_report_scheduler_generates_artifacts_and_history(self):
        import json, os, tempfile
        from datetime import datetime
        from zoneinfo import ZoneInfo

        payload = {
            "provider": "codex",
            "daily": [
                {"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.5}]},
                {"date": "2026-03-02", "modelBreakdowns": [{"modelName": "o3", "cost": 2.0}]},
            ],
        }
        config = {
            "jobs": [
                {
                    "id": "finance-weekly",
                    "name": "Finance Weekly",
                    "frequency": "weekly",
                    "granularity": "weekly",
                    "metrics": ["total_cost", "active_models"],
                    "formats": ["json", "csv"],
                    "recipients": [{"channel": "email", "target": "finance@example.com"}],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_report_scheduler(
                payload=payload,
                provider="codex",
                config=config,
                output_dir=Path(tmpdir),
                now=datetime(2026, 3, 12, 12, 0, 0, tzinfo=ZoneInfo("UTC")),
            )
            self.assertEqual(result["generated"], 1)
            history_path = Path(tmpdir) / "report_history.json"
            self.assertTrue(history_path.exists())
            history = json.loads(history_path.read_text())
            self.assertEqual(len(history["reports"]), 1)
            artifacts = history["reports"][0]["artifacts"]
            self.assertTrue(Path(artifacts["json"]).exists())
            self.assertTrue(Path(artifacts["csv"]).exists())

    def test_run_report_scheduler_blocks_unauthorized_recipient(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo
        import tempfile

        payload = {"provider": "codex", "daily": [{"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}]}]}
        config = {
            "jobs": [
                {
                    "id": "viewer-only",
                    "frequency": "daily",
                    "role": "viewer",
                    "allowedRoles": ["admin"],
                    "recipients": [{"channel": "email", "target": "ops@example.com"}],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_report_scheduler(
                payload=payload,
                provider="codex",
                config=config,
                output_dir=Path(tmpdir),
                now=datetime(2026, 3, 12, 12, 0, 0, tzinfo=ZoneInfo("UTC")),
            )
            deliveries = result["jobs"][0]["deliveries"]
            self.assertEqual(deliveries[0]["status"], "blocked")
            self.assertEqual(deliveries[0]["reason"], "role_not_allowed")

    def test_scheduler_cli_requires_config(self):
        import sys
        from unittest.mock import patch

        argv = ["token_usage_dashboard.py", "--run-report-scheduler"]
        with patch.object(sys, "argv", argv), patch("token_usage_dashboard.load_payload", return_value={"daily": []}):
            rc = dashboard_main()
        self.assertEqual(rc, 8)

    def test_alert_config_parsing_tolerates_invalid_numbers(self):
        rows = [{"date": "2026-03-01", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 1.0}]}]
        alerts = evaluate_alert_rules(
            rows,
            {"predictedTotalCostUSD": 100.0},
            [{"date": "2026-03-01", "zScore": "not-a-number"}],
            config={
                "rules": {
                    "budgetThresholdUSD": "bad-threshold",
                    "budgetForecastPct": "85.5",
                    "anomalyCountThreshold": "abc",
                },
                "notificationChannels": ["email", 123],
            },
        )
        self.assertEqual(alerts["notificationChannels"], ["email", "123"])
        self.assertTrue(any(a["rule"] == "anomaly_count_threshold" for a in alerts["triggered"]))

    def test_dashboard_html_escapes_xss_dynamic_strings(self):
        evil = "<img src=x onerror=alert(1)>"
        rows = [{
            "date": "2026-03-01",
            "modelBreakdowns": [{"modelName": evil, "cost": 3.0}],
            "llmCalls": [{"modelName": evil, "task": evil, "promptTokens": 1, "completionTokens": 1, "totalTokens": 2, "cost": 0.1}],
        }]
        html = build_dashboard_html(
            f"codex</title><script>alert(9)</script>",
            rows,
            top_models=3,
            role_name="viewer<script>alert(8)</script>",
            alert_config={
                "rules": {"budgetThresholdUSD": 1, "budgetForecastPct": 1, "anomalyCountThreshold": 1},
                "notificationChannels": ["slack<script>alert(7)</script>", evil],
            },
        )
        self.assertNotIn("<script>alert(9)</script>", html)
        self.assertNotIn("<td><img src=x onerror=alert(1)>", html)
        self.assertIn("&lt;img src=x onerror=alert(1)&gt;", html)
        self.assertIn("escapeHtml", html)

    def test_dashboard_html_escapes_alert_fields(self):
        rows = [{"date": f"2026-03-{d:02d}", "modelBreakdowns": [{"modelName": "gpt-5", "cost": 10.0}]} for d in range(1, 10)]
        anomalies = [{"date": "2026-03-09", "costUSD": 99.0, "zScore": 9.1, "severity": "<b>high</b>"}]
        alerts = evaluate_alert_rules(
            rows,
            {"predictedTotalCostUSD": 100.0},
            anomalies,
            config={"rules": {"budgetThresholdUSD": 1, "budgetForecastPct": 1, "anomalyCountThreshold": 1}, "notificationChannels": ["discord</td><script>alert(4)</script>"]},
        )
        html = build_dashboard_html("codex", rows, top_models=2, alert_config={"rules": alerts["rules"], "notificationChannels": alerts["notificationChannels"]})
        self.assertIn("&lt;/td&gt;&lt;script&gt;alert(4)&lt;/script&gt;", html)


if __name__ == "__main__":
    main()
