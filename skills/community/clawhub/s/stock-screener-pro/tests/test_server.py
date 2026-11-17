import os
import sys
import unittest
import json
import numpy as np
import pandas as pd
from unittest.mock import patch


SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

import server


class BacktestAccountingTests(unittest.TestCase):
    def test_sell_proceeds_are_added_to_cash(self):
        closes = ([10.0] * 20) + ([12.0] * 5) + ([8.0] * 10)
        bars = [
            {
                "date": f"2026-01-{index + 1:02d}",
                "open": close,
                "close": close,
                "high": close,
                "low": close,
                "vol": 1000.0,
            }
            for index, close in enumerate(closes)
        ]
        with patch.object(server, "_fetch_kline", return_value=bars):
            result = server.backtest_strategy("600519", strategy="sma_cross")

        sell_trades = [trade for trade in result["recent_trades"] if trade["action"] == "SELL"]
        self.assertTrue(sell_trades)
        self.assertGreater(sell_trades[-1]["cash_after"], 0)
        self.assertGreater(result["final_capital"], 0)

    def test_new_strategy_catalog_has_book_research_templates(self):
        catalog = server.get_strategies()
        self.assertIn("book_volume_turnover", {item["id"] for item in catalog["screening_strategies"]})
        self.assertIn("ma_5_10_60_trend", {item["id"] for item in catalog["backtest_strategies"]})
        self.assertIn("macd_cross_trend", {item["id"] for item in catalog["backtest_strategies"]})


class VibeFactorResearchTests(unittest.TestCase):
    def test_benchmark_uses_fixed_non_chat_alpha_command(self):
        fake_result = {"status": "success", "exit_code": 0, "stdout": "ok", "stderr": ""}
        with patch.object(server, "_vibe_trading_command", return_value="/usr/local/bin/vibe-trading"), patch.object(
            server, "_run_research_backend", return_value=fake_result
        ) as runner:
            result = server.run_factor_research(
                action="benchmark", zoo="gtja191", universe="csi300", period="2018-2025", top_n=12
            )

        self.assertEqual(
            runner.call_args.args[0],
            ["/usr/local/bin/vibe-trading", "alpha", "bench", "--zoo", "gtja191", "--universe", "csi300", "--period", "2018-2025", "--top", "12"],
        )
        self.assertTrue(result["no_llm"])
        self.assertTrue(result["no_broker_orders"])
        self.assertTrue(result["research_only"])

    def test_list_uses_json_and_validated_filters(self):
        fake_result = {"status": "success", "exit_code": 0, "stdout": "[]", "stderr": ""}
        with patch.object(server, "_vibe_trading_command", return_value="/usr/local/bin/vibe-trading"), patch.object(
            server, "_run_research_backend", return_value=fake_result
        ) as runner:
            result = server.run_factor_research(action="list", zoo="academic", theme="momentum", limit=10)

        self.assertEqual(
            runner.call_args.args[0],
            ["/usr/local/bin/vibe-trading", "alpha", "list", "--universe", "csi300", "--limit", "10", "--json", "--zoo", "academic", "--theme", "momentum"],
        )
        self.assertEqual(result["operation"], "list")

    def test_invalid_benchmark_inputs_do_not_launch_backend(self):
        with patch.object(server, "_vibe_trading_command") as command, patch.object(server, "_run_research_backend") as runner:
            result = server.run_factor_research(action="benchmark", zoo="unknown", period="2025")
        self.assertEqual(result["status"], "error")
        command.assert_called_once()
        runner.assert_not_called()


class TencentFactorResearchTests(unittest.TestCase):
    def test_quantaalpha_compatible_factor_formulas_match_upstream_definitions(self):
        dates = pd.date_range("2025-01-01", periods=25, freq="B")
        close = pd.Series(np.arange(1.0, 26.0))
        volume = pd.Series(np.arange(101.0, 126.0))
        bars = pd.DataFrame(
            {
                "date": dates,
                "o": close,
                "c": close,
                "h": close + 1.0,
                "l": close - 1.0,
                "v": volume,
            }
        )

        factors = server._calculate_tencent_price_factors(bars)
        last = factors.iloc[-1]

        self.assertAlmostEqual(last["qa_roc5"], 25.0 / 20.0 - 1.0)
        self.assertAlmostEqual(last["qa_roc20"], 25.0 / 5.0 - 1.0)
        self.assertAlmostEqual(last["qa_vratio5"], 125.0 / np.mean([121.0, 122.0, 123.0, 124.0, 125.0]))
        self.assertAlmostEqual(last["qa_volatility10"], np.std(np.arange(16.0, 26.0), ddof=1) / 25.0)
        self.assertAlmostEqual(last["qa_rsv10"], (25.0 - 15.0) / (26.0 - 15.0 + 1e-12))
        self.assertAlmostEqual(last["qa_ma_ratio10_20"], np.mean(np.arange(16.0, 26.0)) / np.mean(np.arange(6.0, 26.0)) - 1.0)

    def test_factor_rows_exclude_signals_whose_forward_return_exits_after_end_date(self):
        dates = pd.date_range("2025-01-01", periods=60, freq="B")
        close = np.arange(60, dtype=float) + 100.0
        bars = pd.DataFrame({"date": dates, "o": close, "c": close, "h": close, "l": close, "v": 1000.0})
        end_date = pd.Timestamp("2025-03-05")
        rows = server._build_tencent_factor_rows(
            "600000", bars, pd.Timestamp("2025-01-01"), end_date, forward_days=5
        )
        self.assertFalse(rows.empty)
        self.assertTrue((rows["forward_return_end_date"] <= end_date).all())

    def test_factor_research_uses_point_in_time_forward_returns_and_oos_split(self):
        dates = pd.date_range("2024-10-01", periods=220, freq="B")

        def fake_bars(code, start, end, refresh_cache=False):
            code_rank = int(code[-2:])
            daily_return = 0.0001 + code_rank * 0.00001
            close = 100.0 * np.power(1.0 + daily_return, np.arange(len(dates)))
            return pd.DataFrame(
                {"date": dates, "o": close, "c": close, "h": close * 1.01, "l": close * 0.99, "v": 1000.0 + code_rank}
            )

        codes = [f"6000{index:02d}" for index in range(20)]
        with patch.object(server, "_load_tencent_factor_bars", side_effect=fake_bars):
            result = server.run_tencent_factor_research(
                stock_codes=codes,
                start_date="2025-01-01",
                end_date="2025-06-30",
                factor_ids=["momentum_20"],
                forward_days=10,
                rebalance_days=10,
                oos_split="2025-05-01",
                random_seeds=5,
            )

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data_source"], "tencent-public")
        self.assertEqual(result["signal_lag_days"], 1)
        factor = result["factor_results"][0]
        self.assertEqual(factor["factor_id"], "momentum_20")
        self.assertGreater(factor["out_of_sample"]["observations"], 0)
        self.assertIn("eligible_for_further_validation", factor)

    def test_factor_research_builds_seeded_control_in_stock_code_order(self):
        dates = pd.date_range("2024-10-01", periods=220, freq="B")

        def fake_bars(code, start, end, refresh_cache=False):
            rank = int(code[-2:]) + 1
            close = 100.0 * np.power(1.0 + rank * 0.00002, np.arange(len(dates)))
            return pd.DataFrame(
                {"date": dates, "o": close, "c": close, "h": close * 1.01, "l": close * 0.99, "v": 1000.0 + rank}
            )

        codes = [f"6000{index:02d}" for index in range(20)]
        with patch.object(server, "_load_tencent_factor_bars", side_effect=fake_bars):
            first = server.run_tencent_factor_research(
                codes, "2025-01-01", "2025-06-30", ["qa_roc20"], 10, 10, "2025-05-01", 5
            )
            second = server.run_tencent_factor_research(
                list(reversed(codes)), "2025-01-01", "2025-06-30", ["qa_roc20"], 10, 10, "2025-05-01", 5
            )

        self.assertEqual(first["factor_results"], second["factor_results"])

    def test_factor_research_requires_a_cross_section_not_holdings_only(self):
        result = server.run_tencent_factor_research(
            stock_codes=["601138", "601991"], start_date="2025-01-01", end_date="2025-06-30"
        )
        self.assertEqual(result["status"], "error")
        self.assertIn("20-120", result["message"])

    def test_portfolio_scoring_requires_a_peer_cross_section(self):
        with patch.object(server, "_run_tencent_factor_research") as research:
            result = server.score_portfolio(
                portfolio_codes=["601138", "601991"],
                peer_codes=["600519"],
                start_date="2025-01-01",
                as_of_date="2025-12-31",
            )
        self.assertEqual(result["status"], "error")
        self.assertIn("20-120", result["message"])
        research.assert_not_called()

    def test_portfolio_scoring_handles_a_factor_without_enough_validation(self):
        codes = [f"6000{index:02d}" for index in range(20)]
        dates = pd.date_range("2025-01-01", periods=45, freq="B")

        def fake_bars(code, start, end, refresh_cache=False):
            rank = int(code[-2:]) + 1
            close = np.arange(45, dtype=float) * (0.02 * rank) + 100.0
            return pd.DataFrame(
                {
                    "date": dates,
                    "o": close,
                    "c": close,
                    "h": close + rank * 0.1,
                    "l": close - rank * 0.1,
                    "v": np.arange(45, dtype=float) + 1000.0 + rank,
                }
            )

        validation = {
            "status": "success",
            "oos_split": "2025-02-01",
            "failed_stock_codes": [],
            "factor_results": [
                {
                    "factor_id": "qa_roc5",
                    "direction_selected_in_train": "high",
                    "out_of_sample": {
                        "mean_rank_ic": 0.12,
                        "top_minus_bottom_cumulative_return": 0.04,
                        "top_group_max_drawdown": 0.03,
                    },
                    "eligible_for_further_validation": True,
                }
            ],
        }
        with patch.object(server, "_run_tencent_factor_research", return_value=validation), patch.object(
            server, "_load_tencent_factor_bars", side_effect=fake_bars
        ), patch.object(server, "_get_a_share_pool", return_value=[]):
            result = server.score_portfolio(
                portfolio_codes=codes[:2],
                peer_codes=codes[2:],
                start_date="2025-01-01",
                as_of_date="2025-03-31",
                factor_ids=["qa_roc5", "qa_rsv10"],
            )

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["factors_without_sufficient_validation"], ["qa_rsv10"])
        self.assertEqual(result["active_composite_factors"], ["qa_roc5"])
        self.assertEqual(len(result["positions"]), 2)
        self.assertTrue(result["research_only"])
        self.assertTrue(result["no_llm"])
        self.assertTrue(result["no_broker_orders"])


class TechnicalResearchSnapshotTests(unittest.TestCase):
    def test_snapshot_exposes_research_observations_and_data_limits(self):
        bars = []
        for i in range(65):
            close = 10.0 + i * 0.12
            bars.append({
                "date": f"2026-01-{i + 1:02d}",
                "open": close - 0.05,
                "close": close,
                "high": close + 0.1,
                "low": close - 0.1,
                "vol": 1000.0 + i * 10,
            })
        snapshot = server._technical_research_snapshot(bars, {"pct_chg": 1.0, "vol_ratio": 1.8})
        self.assertEqual(snapshot["status"], "success")
        self.assertEqual(snapshot["ma_5_10_60"]["alignment"], "多头排列")
        self.assertIn("macd_12_26_9", snapshot)
        self.assertIn("kdj_9_3_3", snapshot)
        self.assertTrue(snapshot["research_only"])
        self.assertTrue(any("宝塔线" in item for item in snapshot["data_limits"]))


class DsaSecurityTests(unittest.TestCase):
    def test_remote_dsa_is_always_blocked(self):
        with patch.object(server, "DSA_BASE_URL", "https://example.com"):
            url, error = server._validated_dsa_base_url()
        self.assertIsNone(url)
        self.assertIn("仅允许", error)

    def test_loopback_dsa_is_allowed(self):
        with patch.object(server, "DSA_BASE_URL", "http://127.0.0.1:8000"):
            url, error = server._validated_dsa_base_url()
        self.assertEqual(url, "http://127.0.0.1:8000")
        self.assertIsNone(error)


class StockCodeValidationTests(unittest.TestCase):
    def test_standard_stock_code_forms_are_normalized(self):
        self.assertEqual(server._clean_code("600519.SH"), ("sh", "600519"))
        self.assertEqual(server._clean_code("sz000001"), ("sz", "000001"))

    def test_stock_code_rejects_non_six_digit_input(self):
        with self.assertRaises(ValueError):
            server._clean_code("600519&unexpected=value")


class TonghuashunParserTests(unittest.TestCase):
    def test_realtime_quote_response_is_normalized(self):
        response = {
            "errorcode": 0,
            "tables": [
                {
                    "thscode": "600519.SH",
                    "table": {
                        "latest": [1500.0],
                        "open": [1490.0],
                        "high": [1510.0],
                        "low": [1488.0],
                        "preClose": [1480.0],
                        "changeRatio": [1.3514],
                        "turnoverRatio": [0.42],
                        "volume": [123400.0],
                        "amount": [185100000.0],
                    },
                }
            ],
        }
        stocks = [{"code": "600519", "name": "贵州茅台", "market": "sh"}]
        with patch.object(server, "_ths_post", return_value=response):
            quotes = server._fetch_batch_quotes_ths(stocks)

        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["code"], "600519")
        self.assertEqual(quotes[0]["name"], "贵州茅台")
        self.assertEqual(quotes[0]["price"], 1500.0)
        self.assertEqual(quotes[0]["data_source"], "tonghuashun-ifind")

    def test_history_response_is_normalized(self):
        response = {
            "errorcode": 0,
            "tables": [
                {
                    "thscode": "600519.SH",
                    "time": ["2026-08-20", "2026-08-21"],
                    "table": {
                        "open": [1490.0, 1500.0],
                        "high": [1510.0, 1520.0],
                        "low": [1480.0, 1495.0],
                        "close": [1505.0, 1515.0],
                        "volume": [1000.0, 1200.0],
                    },
                }
            ],
        }
        with patch.object(server, "_ths_post", return_value=response):
            bars = server._fetch_kline_ths("600519", count=2)

        self.assertEqual([bar["date"] for bar in bars], ["2026-08-20", "2026-08-21"])
        self.assertEqual(bars[-1]["close"], 1515.0)
        self.assertEqual(bars[-1]["data_source"], "tonghuashun-ifind")


class NetworkTransportTests(unittest.TestCase):
    def test_tencent_quote_fallback_uses_https(self):
        with patch.object(server.urllib.request, "urlopen") as opener:
            opener.return_value.__enter__.return_value.read.return_value = b""
            server._fetch_batch_quotes_tencent(
                [{"code": "600519", "name": "贵州茅台", "market": "sh"}]
            )
        request = opener.call_args.args[0]
        self.assertTrue(request.full_url.startswith("https://qt.gtimg.cn/"))

    def test_tencent_kline_fallback_uses_https(self):
        response = b'{"data":{"sh600519":{"qfqday":[]}}}'
        with patch.object(server.urllib.request, "urlopen") as opener:
            opener.return_value.__enter__.return_value.read.return_value = response
            server._fetch_kline_tencent("600519", count=2)
        request = opener.call_args.args[0]
        self.assertTrue(request.full_url.startswith("https://ifzq.gtimg.cn/"))


class Ai4TradeIntegrationTests(unittest.TestCase):
    def test_account_query_requires_environment_token_without_network_call(self):
        with patch.object(server, "AI4TRADE_TOKEN", ""), patch.object(server.urllib.request, "urlopen") as opener:
            result = server.get_ai4trade_account()
        self.assertEqual(result["status"], "error")
        opener.assert_not_called()

    def test_mutation_is_blocked_without_explicit_confirmation(self):
        with patch.object(server.urllib.request, "urlopen") as opener:
            result = server.manage_ai4trade_follow(leader_id=10, confirm=False)
        self.assertEqual(result["status"], "confirmation_required")
        opener.assert_not_called()


class QuantResearchAdapterTests(unittest.TestCase):
    def test_vibe_research_rejects_order_intent_before_subprocess(self):
        with patch.object(server, "_run_research_backend") as runner:
            result = server.run_vibe_trading_research("请帮我下单买入 600519", confirm_external_ai=True)
        self.assertEqual(result["status"], "error")
        runner.assert_not_called()

    def test_vibe_research_requires_external_ai_confirmation(self):
        with patch.object(server, "_run_research_backend") as runner:
            result = server.run_vibe_trading_research("回测 600519 的均线策略", confirm_external_ai=False)
        self.assertEqual(result["status"], "confirmation_required")
        runner.assert_not_called()

    def test_vibe_research_uses_fixed_local_command_and_guard_prompt(self):
        fake_result = {"status": "success", "stdout": "{}", "stderr": "", "exit_code": 0}
        with patch.object(server, "_vibe_trading_command", return_value="/usr/local/bin/vibe-trading"), patch.object(
            server, "_run_research_backend", return_value=fake_result
        ) as runner:
            result = server.run_vibe_trading_research("回测 600519 的均线策略", confirm_external_ai=True)
        command = runner.call_args.args[0]
        self.assertEqual(command[0], "/usr/local/bin/vibe-trading")
        self.assertIn("--json", command)
        self.assertIn("Do not select or use broker connectors", command[-1])
        self.assertTrue(result["research_only"])

    def test_a_share_ticker_is_normalized_for_tradingagents(self):
        self.assertEqual(server._a_share_ticker("600519.SH"), "600519.SS")
        self.assertEqual(server._a_share_ticker("sz000001"), "000001.SZ")

    def test_vibe_swarm_maps_topic_to_the_upstream_preset_schema(self):
        fake_result = {"status": "success", "stdout": "{}", "stderr": "", "exit_code": 0}
        with patch.object(server, "_vibe_trading_command", return_value="/usr/local/bin/vibe-trading"), patch.object(
            server, "_run_research_backend", return_value=fake_result
        ) as runner:
            result = server.run_vibe_trading_swarm(
                "investment_committee", "贵州茅台估值与风险", confirm_external_ai=True
            )
        payload = json.loads(runner.call_args.args[0][-1])
        self.assertEqual(payload["target"], "贵州茅台估值与风险")
        self.assertIn("market", payload)
        self.assertTrue(result["research_only"])

    def test_tradingagents_requires_confirmation_before_import_or_run(self):
        with patch.object(server, "_python_has_module") as module_check:
            result = server.run_agent_research(
                engine="tradingagents", stock_code="600519", analysis_date="2026-08-20", confirm_external_ai=False
            )
        self.assertEqual(result["status"], "confirmation_required")
        module_check.assert_not_called()

    def test_quantaalpha_mining_rejects_order_intent_before_runtime_checks(self):
        with patch.object(server, "_quantaalpha_status") as status:
            result = server.run_quantaalpha_research(
                action="mine", direction="帮我下单买入工业富联", confirm_external_ai=True
            )
        self.assertEqual(result["status"], "error")
        status.assert_not_called()

    def test_quantaalpha_mining_requires_explicit_model_confirmation(self):
        with patch.object(server, "_quantaalpha_status") as status:
            result = server.run_quantaalpha_research(
                action="mine", direction="研究高质量低波动因子", confirm_external_ai=False
            )
        self.assertEqual(result["status"], "confirmation_required")
        status.assert_not_called()

    def test_quantaalpha_mining_uses_pinned_runtime_and_openclaw_bridge(self):
        runtime = {
            "package_available": True,
            "config_available": True,
            "qlib_data_available": True,
            "full_factor_data_available": True,
        }

        class FakeBridge:
            token = "one-run-token"
            base_url = "http://127.0.0.1:12345/v1"

            def __init__(self, timeout_seconds):
                self.timeout_seconds = timeout_seconds

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return None

        fake_result = {"status": "success", "stdout": "ok", "stderr": "", "exit_code": 0}
        with patch.object(server, "_quantaalpha_status", return_value=runtime), patch.object(
            server, "_quantaalpha_python", return_value="/fixed/quantaalpha/bin/python"
        ), patch.object(server, "_quantaalpha_paths", return_value={
            "repo": "/fixed/quantaalpha/repo",
            "qlib": "/fixed/quantaalpha/data/qlib/cn_data",
            "factor_full": "/fixed/quantaalpha/data/factor_source",
            "factor_debug": "/fixed/quantaalpha/data/factor_source_debug",
            "results": "/tmp/quantaalpha-test-results",
        }), patch.object(server, "_openclaw_cli", return_value="/usr/local/bin/openclaw"), patch.object(
            server, "_OpenClawInferenceBridge", FakeBridge
        ), patch.object(server.os, "makedirs"), patch.object(
            server, "_latest_quantaalpha_factor_library", return_value="/fixed/results/all_factors_library.json"
        ), patch.object(server, "_run_research_backend", return_value=fake_result) as runner:
            result = server.run_quantaalpha_research(
                action="mine",
                direction="研究盈利质量与低波动的交互因子",
                step_n=5,
                confirm_external_ai=True,
            )
        command = runner.call_args.args[0]
        environment = runner.call_args.kwargs["environment"]
        self.assertEqual(command[:3], ["/fixed/quantaalpha/bin/python", "-m", "quantaalpha.cli"])
        self.assertIn("--step_n=5", command)
        self.assertIn("Research-only factor discovery", command[4])
        self.assertEqual(environment["OPENAI_API_KEY"], "one-run-token")
        self.assertEqual(environment["CHAT_MODEL"], "openclaw/default")
        self.assertEqual(environment["CHAT_STREAM"], "false")
        self.assertEqual(environment["LOG_LLM_CHAT_CONTENT"], "false")
        self.assertEqual(result["pinned_commit"], server.QUANTAALPHA_COMMIT)
        self.assertTrue(result["no_broker_orders"])

    def test_skill_status_has_only_supported_agent_backends(self):
        with patch.object(server, "_python_has_module", return_value=True), patch.object(
            server, "_vibe_trading_command", return_value="/usr/local/bin/vibe-trading"
        ):
            result = server.get_skill_status()
        self.assertIn("agent_research", result)
        self.assertEqual(set(result["agent_research"]), {
            "research_only",
            "no_background_jobs",
            "no_broker_orders",
            "vibe_trading_command_available",
            "tradingagents_package_available",
            "quantaalpha",
            "openclaw_model_bridge_available",
            "backend_python_configured",
            "artifact_dir",
        })

    def test_skill_status_can_return_compacted_legacy_catalog_and_cache(self):
        with patch.object(server, "get_strategies", return_value={"screening_strategies": []}), patch.object(
            server, "predict_cache_status", return_value={"cached_count": 0}
        ):
            result = server.get_skill_status(include_details=True)
        self.assertEqual(result["strategy_catalog"], {"screening_strategies": []})
        self.assertEqual(result["prediction_cache"], {"cached_count": 0})

    def test_ai4trade_aggregator_routes_read_requests(self):
        with patch.object(server, "get_ai4trade_account", return_value={"status": "success", "account": {}}) as account:
            result = server.get_ai4trade(resource="account")
        self.assertEqual(result["status"], "success")
        account.assert_called_once()

    def test_ai4trade_aggregator_keeps_mutations_confirmation_gated(self):
        with patch.object(server.urllib.request, "urlopen") as opener:
            result = server.manage_ai4trade(action="follow", leader_id=10, confirm=False)
        self.assertEqual(result["status"], "confirmation_required")
        opener.assert_not_called()

    def test_authenticated_request_uses_fixed_ai4trade_host(self):
        response = json.dumps({"signals": []}).encode("utf-8")
        with patch.object(server, "AI4TRADE_TOKEN", "test-token"), patch.object(
            server.urllib.request, "urlopen"
        ) as opener:
            opener.return_value.__enter__.return_value.read.return_value = response
            result = server.get_ai4trade_signal_feed(limit=5)
        request = opener.call_args.args[0]
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["untrusted_external_data"])
        self.assertTrue(request.full_url.startswith("https://ai4trade.ai/api/signals/feed?"))
        self.assertEqual(request.get_header("Authorization"), "Bearer test-token")

    def test_points_exchange_is_blocked_without_explicit_confirmation(self):
        with patch.object(server.urllib.request, "urlopen") as opener:
            result = server.exchange_ai4trade_points(amount=10, confirm=False)
        self.assertEqual(result["status"], "confirmation_required")
        opener.assert_not_called()


if __name__ == "__main__":
    unittest.main()
