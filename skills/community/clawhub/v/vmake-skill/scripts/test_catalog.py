"""Offline catalog contract tests: never upload, consume, or submit tasks."""
import json
import unittest
from unittest.mock import Mock, patch

import config as app_config
from ai.api import AiApi
from client import (
    ConfigFetchError,
    ConsumeDeniedError,
    SkillClient,
    normalize_task_catalog,
)
import vmake_ai


def _client_with_catalog(catalog):
    instance = object.__new__(SkillClient)
    instance.config_response = {}
    instance.task_catalog = catalog
    instance._pipeline_trace = []
    instance._notices = []
    instance._notice_keys = set()
    instance.api = Mock()
    return instance


class CatalogTests(unittest.TestCase):
    def test_user_agent_uses_configured_name_and_version(self):
        self.assertTrue(app_config.USER_AGENT_NAME)
        self.assertEqual(
            app_config.USER_AGENT,
            f"{app_config.USER_AGENT_NAME}-{app_config.VERSION}",
        )

    def test_explicit_v1_schema_keeps_metadata_rich_alias_legacy(self):
        catalog = normalize_task_catalog(
            {
                "schema": "v1",
                "algorithm": {
                    "invoke": {
                        "hdvideoallinone": {
                            "material_id": "SKM0001",
                            "name": "Smart",
                            "description": "Server metadata on a legacy alias.",
                            "media_type": "video",
                            "task": "video/smart-remove",
                            "profile": {"version": "v1"},
                        }
                    }
                },
            }
        )

        self.assertEqual(catalog["mode"], "legacy")
        self.assertEqual(catalog["entries"][0]["material_id"], "hdvideoallinone")
        self.assertEqual(catalog["entries"][0]["profile"], {"version": "v1"})

    def test_explicit_v2_schema_does_not_require_metadata_heuristic(self):
        catalog = normalize_task_catalog(
            {
                "schema": "v2",
                "algorithm": {
                    "invoke": {
                        "SKM0001": {
                            "task": "video/smart-remove",
                            "params": {},
                        }
                    }
                },
            }
        )

        self.assertEqual(catalog["mode"], "v2")
        self.assertEqual(catalog["entries"][0]["material_id"], "SKM0001")

    def test_unknown_explicit_schema_fails_closed(self):
        catalog = normalize_task_catalog(
            {
                "schema": "v3",
                "algorithm": {
                    "invoke": {
                        "SKM0001": {
                            "name": "Smart",
                            "media_type": "video",
                        }
                    }
                },
            }
        )

        self.assertEqual(
            catalog,
            {"mode": "unavailable", "source": "schema", "entries": []},
        )

    def test_v2_catalog_prefers_server_description_and_key_as_material_id(self):
        response = {
            "algorithm": {
                "invoke": {
                    "material-video-smart": {
                        "name": "Smart",
                        "description": "服务端视频智能消除描述",
                        "media_type": "video",
                        "task": "video/smart-remove",
                        "task_type": "mtlab",
                        "params": {"parameter": {"mode": "smart"}},
                    }
                }
            }
        }

        catalog = normalize_task_catalog(response)

        self.assertEqual(catalog["mode"], "v2")
        self.assertEqual(catalog["source"], "algorithm.invoke")
        self.assertEqual(catalog["entries"][0]["material_id"], "material-video-smart")
        self.assertEqual(
            catalog["entries"][0]["description"], "服务端视频智能消除描述"
        )

        public = vmake_ai._public_catalog(catalog, "video")
        self.assertEqual(
            public["tasks"],
            [
                {
                    "material_id": "material-video-smart",
                    "name": "Smart",
                    "description": "服务端视频智能消除描述",
                    "media_type": "video",
                }
            ],
        )
        self.assertIn("material-video-smart", json.dumps(public))

        client = _client_with_catalog(catalog)
        self.assertEqual(
            client.resolve_task("Smart")["material_id"], "material-video-smart"
        )

    def test_v2_blank_description_remains_blank(self):
        response = {
            "algorithm": {
                "catalog": [
                    {
                        "material_id": "material-image-smart",
                        "name": "Smart",
                        "description": "  ",
                        "media_type": "image",
                        "task": "image/smart-remove",
                    }
                ]
            }
        }

        catalog = normalize_task_catalog(response)

        self.assertEqual(catalog["mode"], "v2")
        self.assertEqual(catalog["entries"][0]["description"], "")

    def test_explicit_v2_catalog_merges_runtime_invoke_fields(self):
        response = {
            "algorithm": {
                "catalog": {
                    "material-video-pro": {
                        "name": "Smart Pro",
                        "description": "服务端 Pro 描述",
                        "media_type": "video",
                    }
                },
                "invoke": {
                    "material-video-pro": {
                        "task": "video/smart-pro",
                        "task_type": "mtlab",
                        "params": {"parameter": {"quality": "pro"}},
                        "profile": {"media_profiles": {"media_data_type": "url"}},
                    }
                },
            }
        }

        entry = normalize_task_catalog(response)["entries"][0]

        self.assertEqual(entry["task"], "video/smart-pro")
        self.assertEqual(entry["params"]["parameter"]["quality"], "pro")
        self.assertEqual(
            entry["profile"]["media_profiles"]["media_data_type"], "url"
        )

    def test_legacy_alias_is_accepted_only_when_remote_invoke_returns_it(self):
        catalog = normalize_task_catalog(
            {
                "algorithm": {
                    "invoke": {
                        "videoscreenclear": {
                            "task": "video/screen-clear",
                            "params": {},
                        }
                    }
                }
            }
        )
        client = _client_with_catalog(catalog)

        self.assertEqual(catalog["mode"], "legacy")
        self.assertEqual(
            client.resolve_task("videoscreenclear")["material_id"],
            "videoscreenclear",
        )
        with self.assertRaisesRegex(KeyError, "local fallback is disabled"):
            client.resolve_task("hdvideoallinone")

    def test_profile_override_does_not_depend_on_catalog_mode(self):
        catalog = normalize_task_catalog(
            {
                "schema": "v1",
                "algorithm": {
                    "invoke": {
                        "videoscreenclear": {
                            "task": "video/screen-clear",
                            "params": {},
                        }
                    }
                },
            }
        )
        client = _client_with_catalog(catalog)
        client.api.getFileUrl.return_value = "https://example.test/input.mp4"
        client._consume_permission = Mock(return_value={"context": "ctx"})
        client.api.invoke_task.return_value = {"ok": True}

        result = client.run_task(
            "videoscreenclear",
            "/tmp/not-uploaded.mp4",
            profile={"version": "v1"},
        )

        self.assertEqual(result, {"ok": True})
        client.api.invoke_task.assert_called_once_with(
            "videoscreenclear",
            "https://example.test/input.mp4",
            None,
            "ctx",
            profile={"version": "v1"},
        )

    def test_v2_does_not_fall_back_to_local_legacy_name(self):
        catalog = normalize_task_catalog(
            {
                "algorithm": {
                    "invoke": {
                        "material-video-smart": {
                            "name": "Smart",
                            "description": "服务端描述",
                            "media_type": "video",
                            "task": "video/smart-remove",
                        }
                    }
                }
            }
        )
        client = _client_with_catalog(catalog)

        with self.assertRaisesRegex(KeyError, "Unknown V2 task selector"):
            client.resolve_task("videoscreenclear")

    def test_invalid_task_stops_before_upload_and_consume(self):
        catalog = normalize_task_catalog(
            {
                "algorithm": {
                    "invoke": {
                        "material-video-smart": {
                            "name": "Smart",
                            "description": "服务端描述",
                            "media_type": "video",
                            "task": "video/smart-remove",
                        }
                    }
                }
            }
        )
        client = _client_with_catalog(catalog)
        client._consume_permission = Mock()

        with self.assertRaisesRegex(KeyError, "Unknown V2 task selector"):
            client.run_task("videoscreenclear", "/tmp/not-uploaded.mp4")

        client.api.getFileUrl.assert_not_called()
        client._consume_permission.assert_not_called()

    def test_consume_rejected_media_domain_requests_direct_upload(self):
        error = ConsumeDeniedError(
            10103,
            "This media URL is not supported. Please upload the image or video "
            "file directly and try again.",
            {},
        )

        output = vmake_ai._envelope_consume_denied(error, "Smart")

        self.assertEqual(output["error"], "input_unavailable")
        self.assertEqual(output["failure_stage"], "consume_quota")
        self.assertIn("upload the image or video file directly", output["agent_instruction"])
        self.assertIn("not submitted", output["agent_instruction"])

    def test_other_invalid_request_stays_consume_param_error(self):
        error = ConsumeDeniedError(10103, "Invalid task parameter.", {})

        output = vmake_ai._envelope_consume_denied(error, "Smart")

        self.assertEqual(output["error"], "consume_param_error")

    def test_unknown_consume_code_preserves_server_notice(self):
        notice = {
            "code": "server_defined_upgrade_notice",
            "level": "error",
            "message": "Please upgrade the Skill before retrying.",
        }
        error = ConsumeDeniedError(
            90001,
            "The current AK only supports the legacy Skill.",
            {"meta": {"code": 90001}, "response": {"notices": [notice]}},
        )

        output = vmake_ai._envelope_consume_denied(error, "Smart")

        self.assertEqual(output["error"], "consume_denied")
        self.assertEqual(output["notices"], [notice])
        self.assertIn("unknown notice codes", output["agent_instruction"])

    def test_notices_are_deduplicated_and_unknown_fields_are_preserved(self):
        client = _client_with_catalog({"mode": "legacy", "source": None, "entries": []})
        notice = {
            "code": "server_defined_notice",
            "message": "Server-controlled message",
            "dedupe_key": "same-notice",
            "future_field": {"value": 1},
        }

        self.assertEqual(client._collect_notices({"notices": [notice, notice]}), 1)

        self.assertEqual(client.get_notices(), [notice])

    def test_warning_notice_does_not_turn_success_into_failure(self):
        result = {
            "ok": True,
            "notices": [
                {
                    "code": "upgrade_available",
                    "level": "warning",
                    "message": "Please upgrade when convenient.",
                }
            ],
        }

        self.assertFalse(vmake_ai._is_failed_cli_result(result))
        self.assertEqual(
            vmake_ai._success_envelope("Smart", result)["skill_status"],
            "completed",
        )

    def test_legacy_update_fields_become_notice_without_stdout_text(self):
        client = _client_with_catalog(None)
        client.wapi = Mock()
        client.wapi.request.return_value = {
            "latest_version": "v1.4.0",
            "need_update": True,
            "update_message": "Please upgrade the Skill.",
            "algorithm": {"invoke": {}},
        }
        client._get_cached_gid = Mock(return_value=None)

        with patch("builtins.print") as print_mock:
            client.fetch_config(version="v1.3.0")

        print_mock.assert_not_called()
        self.assertEqual(
            client.wapi.request.call_args.kwargs["body"]["supported_schemas"],
            ["v2", "v1"],
        )
        self.assertEqual(
            client.get_notices(),
            [
                {
                    "code": "skill_upgrade_available",
                    "level": "warning",
                    "message": "Please upgrade the Skill.",
                    "dedupe_key": "skill_upgrade_available:v1.4.0",
                }
            ],
        )

    def test_legacy_update_notice_is_added_alongside_other_config_notice(self):
        client = _client_with_catalog(None)
        client.wapi = Mock()
        client.wapi.request.return_value = {
            "latest_version": "v2.0.0",
            "need_update": True,
            "update_message": "Please upgrade the Skill.",
            "notices": [
                {
                    "code": "service_maintenance",
                    "level": "warning",
                    "message": "Vmake will undergo maintenance tonight.",
                }
            ],
            "algorithm": {"invoke": {}},
        }
        client._get_cached_gid = Mock(return_value=None)

        client.fetch_config(version="v1.3.0")

        self.assertEqual(
            [notice["code"] for notice in client.get_notices()],
            ["service_maintenance", "skill_upgrade_available"],
        )

    def test_existing_upgrade_notice_is_not_synthesized_again(self):
        client = _client_with_catalog(None)
        client.wapi = Mock()
        client.wapi.request.return_value = {
            "latest_version": "v2.0.0",
            "need_update": True,
            "update_message": "Fallback upgrade message.",
            "notices": [
                {
                    "code": "skill_upgrade_available",
                    "level": "warning",
                    "message": "Server-provided upgrade message.",
                    "dedupe_key": "server-upgrade-notice",
                }
            ],
            "algorithm": {"invoke": {}},
        }
        client._get_cached_gid = Mock(return_value=None)

        client.fetch_config(version="v1.3.0")

        self.assertEqual(len(client.get_notices()), 1)
        self.assertEqual(
            client.get_notices()[0]["message"],
            "Server-provided upgrade message.",
        )

    def test_fetch_config_keeps_server_profile_in_runtime_invoke(self):
        client = _client_with_catalog(None)
        client.wapi = Mock()
        client.wapi.request.return_value = {
            "schema": "v2",
            "algorithm": {
                "invoke": {
                    "SKM0001": {
                        "task": "image/restore",
                        "params": {},
                        "profile": {
                            "media_profiles": {"media_data_type": "url"}
                        },
                    }
                }
            },
        }
        client._get_cached_gid = Mock(return_value=None)

        with patch.dict(app_config.INVOKE, {}, clear=True):
            client.fetch_config(version="v2.0.0")
            self.assertEqual(
                app_config.INVOKE["SKM0001"]["profile"],
                {"media_profiles": {"media_data_type": "url"}},
            )

    def test_fetch_config_omits_profile_when_server_does_not_send_it(self):
        client = _client_with_catalog(None)
        client.wapi = Mock()
        client.wapi.request.return_value = {
            "schema": "v2",
            "algorithm": {
                "invoke": {
                    "SKM0001": {
                        "task": "image/restore",
                        "params": {},
                    }
                }
            },
        }
        client._get_cached_gid = Mock(return_value=None)

        with patch.dict(app_config.INVOKE, {}, clear=True):
            client.fetch_config(version="v2.0.0")
            self.assertNotIn("profile", app_config.INVOKE["SKM0001"])

    def test_fetch_legacy_config_does_not_rewrite_runtime_invoke(self):
        client = _client_with_catalog(None)
        client.wapi = Mock()
        client.wapi.request.return_value = {
            "schema": "v1",
            "algorithm": {
                "invoke": {
                    "videoscreenclear": {
                        "task": "video/screen-clear",
                        "params": {},
                        "profile": {"version": "v1"},
                    }
                }
            },
        }
        client._get_cached_gid = Mock(return_value=None)

        with patch.dict(app_config.INVOKE, {}, clear=True):
            client.fetch_config(version="v2.0.0")
            self.assertEqual(
                app_config.INVOKE["videoscreenclear"]["profile"],
                {"version": "v1"},
            )

    def test_config_failure_output_does_not_expose_reqid_or_raw_response(self):
        error = ConfigFetchError(
            10101,
            "skill v2 config not available",
            {"meta": {"reqid": "internal-debug-only"}},
            original_code=10101,
        )

        output = vmake_ai._config_failure_envelope(error)
        encoded = json.dumps(output)

        self.assertEqual(output["error"], "config_unavailable")
        self.assertEqual(output["api_code"], 10101)
        self.assertNotIn("reqid", encoded)
        self.assertNotIn("internal-debug-only", encoded)

    def test_empty_v2_catalog_requires_a_user_visible_message(self):
        client = Mock()
        client.get_task_catalog.return_value = {
            "mode": "v2",
            "source": "algorithm.invoke",
            "entries": [],
        }
        client.get_notices.return_value = []
        args = Mock(agent_name=None, agent_version=None, agent_model=None, media_type="")

        with patch("client.SkillClient", return_value=client), patch.object(
            vmake_ai, "_print_json"
        ) as print_json:
            exit_code = vmake_ai.cmd_catalog(args)

        output = print_json.call_args.args[0]
        self.assertEqual(exit_code, 1)
        self.assertEqual(output["error"], "config_catalog_empty")
        self.assertEqual(output["skill_status"], "failed")
        self.assertIn("user-visible", output["agent_instruction"])
        self.assertIn("no matching Vmake task", output["agent_instruction"])
        self.assertIn("Vmake official support", output["agent_instruction"])

    def test_v2_display_name_resolves_to_internal_id_only_inside_client(self):
        catalog = normalize_task_catalog(
            {
                "algorithm": {
                    "invoke": {
                        "material-video-smart": {
                            "name": "Smart",
                            "description": "服务端描述",
                            "media_type": "video",
                            "task": "video/smart-remove",
                        }
                    }
                }
            }
        )
        client = _client_with_catalog(catalog)
        client.api.getFileUrl.return_value = "https://example.test/input.mp4"
        client.api.invoke_task.return_value = {"ok": True}
        notice = {
            "code": "legacy_skill_compatibility_used",
            "message": "This request used compatibility mode.",
        }
        client._consume_permission = Mock(
            return_value={"context": "ctx", "notices": [notice]}
        )

        result = client.run_task("Smart", "/tmp/not-uploaded.mp4")

        self.assertEqual(result, {"ok": True, "notices": [notice]})
        client._consume_permission.assert_called_once_with(
            "https://example.test/input.mp4", "material-video-smart"
        )
        client.api.invoke_task.assert_called_once_with(
            "material-video-smart",
            "https://example.test/input.mp4",
            None,
            "ctx",
        )
        self.assertNotIn("material-video-smart", json.dumps(client._pipeline_trace))

    def test_duplicate_v2_display_name_stops_without_guessing(self):
        client = _client_with_catalog(
            {
                "mode": "v2",
                "source": "algorithm.invoke",
                "entries": [
                    {"material_id": "internal-a", "name": "Subtitle"},
                    {"material_id": "internal-b", "name": "Subtitle"},
                ],
            }
        )

        with self.assertRaisesRegex(KeyError, "ambiguous"):
            client.resolve_task("Subtitle")
        self.assertEqual(client.resolve_task("internal-a")["material_id"], "internal-a")
        self.assertEqual(client.resolve_task("internal-b")["material_id"], "internal-b")

    def test_dynamic_v2_video_name_builds_video_worker(self):
        payload = vmake_ai.build_spawn_run_task(
            "Smart",
            "/tmp/video.mp4",
            "",
            "oc_test",
            "feishu",
            3600,
            media_type="video",
        )

        worker = payload["sessions_spawn_args"]["task"]
        self.assertIn("feishu_send_video.py", worker)
        self.assertIn("Smart", payload["command"])


class InvokeTaskTypeTests(unittest.TestCase):
    def test_ai_api_offers_decoded_responses_to_notice_handler(self):
        handler = Mock()
        client = object.__new__(AiApi)
        client._notice_handler = handler
        payload = {
            "notices": [
                {
                    "code": "future_notice",
                    "message": "A server-defined message.",
                }
            ]
        }

        client._emit_response_notices(payload)

        handler.assert_called_once_with(payload)

    def test_invoke_task_uses_remote_task_type(self):
        client = object.__new__(AiApi)
        client.invoke = Mock(return_value={"ok": True})
        preset = {
            "material-workflow": {
                "task": "image/restore",
                "task_type": "workflow",
                "params": {"parameter": {"quality": "2k"}},
            }
        }

        with patch.dict(app_config.INVOKE, preset, clear=True):
            result = client.invoke_task(
                "material-workflow",
                "https://example.test/input.jpg",
                context="ctx",
            )

        self.assertEqual(result, {"ok": True})
        client.invoke.assert_called_once_with(
            "https://example.test/input.jpg",
            {"parameter": {"quality": "2k"}},
            "image/restore",
            "ctx",
            "workflow",
        )

    def test_invoke_task_merges_server_profile_with_override(self):
        client = object.__new__(AiApi)
        client.invoke = Mock(return_value={"ok": True})
        preset = {
            "material-workflow": {
                "task": "image/restore",
                "profile": {
                    "media_profiles": {"media_data_type": "url", "format": "jpg"},
                    "version": "v1",
                },
            }
        }

        with patch.dict(app_config.INVOKE, preset, clear=True):
            result = client.invoke_task(
                "material-workflow",
                "https://example.test/input.jpg",
                profile={"media_profiles": {"format": "png"}},
            )

        self.assertEqual(result, {"ok": True})
        client.invoke.assert_called_once_with(
            "https://example.test/input.jpg",
            {},
            "image/restore",
            "",
            "mtlab",
            profile={
                "media_profiles": {"media_data_type": "url", "format": "png"},
                "version": "v1",
            },
        )

    def test_run_attaches_profile_to_first_init_image(self):
        client = object.__new__(AiApi)
        client.Key = "ak"
        client.Secret = "sk"
        client._notice_handler = None
        client.getAiStrategy = Mock(
            return_value={
                "url": "https://algo.example.test",
                "push_path": "push",
                "sync_timeout": 1,
            }
        )
        signer = Mock()
        captured = {}

        def sign_request(_uri, _method, _headers, body):
            captured.update(json.loads(body))
            return object()

        signer.sign.side_effect = sign_request
        response = Mock(
            status_code=200,
            content=json.dumps(
                {"data": {"status": 10, "result": {"urls": []}}}
            ).encode(),
        )
        session = Mock()
        session.send.return_value = response
        init_images = [{"url": "https://example.test/input.jpg"}]

        with patch("ai.api.sign.Signer", return_value=signer), patch(
            "ai.api.requests.Session", return_value=session
        ):
            client.run(
                init_images,
                {},
                "image/restore",
                "mtlab",
                profile={"media_profiles": {"media_data_type": "url"}},
            )

        self.assertNotIn("profile", init_images[0])
        self.assertEqual(
            captured["init_images"][0]["profile"],
            {"media_profiles": {"media_data_type": "url"}},
        )

    def test_invoke_task_defaults_missing_or_blank_task_type_to_mtlab(self):
        for configured_task_type in (None, "", "   "):
            with self.subTest(task_type=configured_task_type):
                client = object.__new__(AiApi)
                client.invoke = Mock(return_value={"ok": True})
                preset = {
                    "legacy-material": {
                        "task": "image/restore",
                        "params": {},
                    }
                }
                if configured_task_type is not None:
                    preset["legacy-material"]["task_type"] = configured_task_type

                with patch.dict(app_config.INVOKE, preset, clear=True):
                    client.invoke_task(
                        "legacy-material",
                        "https://example.test/input.jpg",
                    )

                client.invoke.assert_called_once_with(
                    "https://example.test/input.jpg",
                    {},
                    "image/restore",
                    "",
                    "mtlab",
                )


if __name__ == "__main__":
    unittest.main()
