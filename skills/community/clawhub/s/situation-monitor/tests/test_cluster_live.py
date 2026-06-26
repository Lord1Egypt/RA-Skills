from monitoring_the_situation.cluster_live import detect_incidents_from_cluster


def test_detect_incidents_from_cluster_finds_oom_and_image_pull() -> None:
    pods_payload = {
        "items": [
            {
                "metadata": {
                    "name": "payment-processor-abc",
                    "creationTimestamp": "2026-03-25T20:00:00Z",
                    "labels": {"app": "payment-processor"},
                },
                "status": {
                    "containerStatuses": [
                        {
                            "state": {"waiting": {"reason": "CrashLoopBackOff"}},
                            "lastState": {"terminated": {"reason": "OOMKilled"}},
                        }
                    ]
                },
            },
            {
                "metadata": {
                    "name": "user-service-def",
                    "creationTimestamp": "2026-03-25T20:05:00Z",
                    "labels": {"app": "user-service"},
                },
                "status": {
                    "containerStatuses": [
                        {
                            "state": {
                                "waiting": {
                                    "reason": "ImagePullBackOff",
                                    "message": "Back-off pulling image",
                                }
                            },
                            "lastState": {},
                        }
                    ]
                },
            },
        ]
    }
    events_payload = {
        "items": [
            {
                "involvedObject": {"name": "payment-processor-abc"},
                "reason": "BackOff",
                "message": "Back-off restarting failed container",
            },
            {
                "involvedObject": {"name": "user-service-def"},
                "reason": "Failed",
                "message": "Failed to pull image",
            },
        ]
    }

    incidents = detect_incidents_from_cluster(
        pods_payload,
        events_payload,
        namespace="production",
    )

    services = {item.service: item for item in incidents}
    assert "payment-processor" in services
    assert "user-service" in services
    assert "OOMKilled" in services["payment-processor"].title
    assert "ImagePullBackOff" in services["user-service"].title
