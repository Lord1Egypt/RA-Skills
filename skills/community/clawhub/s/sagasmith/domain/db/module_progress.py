"""Mutable campaign progress over immutable imported module content."""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select

from .campaigns import CampaignNotFoundError
from .database import Database
from .models import (
    Campaign,
    CampaignEvent,
    ModuleChapter,
    ModuleSource,
    SceneIndex,
    SceneState,
    ToolAudit,
    WorldState,
)
class ModuleProgressError(RuntimeError):
    """Base error for campaign progress operations."""


class SceneNotFoundError(ModuleProgressError):
    """The requested scene was not found in any active module."""


class ChapterLockedError(ModuleProgressError):
    """The scene's chapter is locked and cannot be progressed into."""


@dataclass(frozen=True)
class SceneProgressInfo:
    campaign_id: str
    module_name: str
    chapter_key: str
    scene_id: str
    scene_title: str
    current_room: str | None
    explored_percent: int
    state_json: dict[str, Any]
    state_version: int


def _chapter_number(chapter_key: str) -> int | str:
    match = re.search(r"\d+", chapter_key)
    return int(match.group()) if match else chapter_key


class ModuleProgressService:
    """Enter or update an unlocked scene and synchronize world progress."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def set_scene(
        self,
        campaign_id: str,
        scene_id: str,
        *,
        current_room: str | None = None,
        explored_percent: int = 0,
        state_json: dict[str, Any] | None = None,
        session_id: str | None = None,
        actor_id: str | None = None,
    ) -> SceneProgressInfo:
        if not 0 <= explored_percent <= 100:
            raise ValueError("explored_percent must be between 0 and 100")
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            row = session.execute(
                select(SceneIndex, ModuleChapter, ModuleSource)
                .join(ModuleChapter, ModuleChapter.id == SceneIndex.chapter_id)
                .join(ModuleSource, ModuleSource.id == ModuleChapter.module_id)
                .where(
                    SceneIndex.id == scene_id,
                    ModuleSource.campaign_id == campaign_id,
                    ModuleSource.is_active.is_(True),
                )
            ).first()
            if row is None:
                raise SceneNotFoundError(
                    f"scene not found in active module for campaign {campaign_id}: {scene_id}"
                )
            scene, chapter, module = row
            if chapter.status == "locked":
                raise ChapterLockedError(f"chapter is locked: {chapter.chapter_key}")

            world = session.scalar(
                select(WorldState).where(WorldState.campaign_id == campaign_id)
            )
            previous_scene = ""
            if world is not None:
                world_payload = dict(world.state_json or {})
                previous_scene = str(world_payload.get("current_scene", ""))
                world_payload["current_chapter"] = _chapter_number(chapter.chapter_key)
                world_payload["current_scene"] = scene.title
                world.state_json = world_payload
                world.state_version += 1

            progress = session.scalar(
                select(SceneState).where(
                    SceneState.campaign_id == campaign_id,
                    SceneState.scene_id == scene.id,
                )
            )
            if progress is None:
                progress = SceneState(
                    id=f"scene_state_{uuid.uuid4().hex[:16]}",
                    campaign_id=campaign_id,
                    scene_id=scene.id,
                    current_room=current_room,
                    explored_percent=explored_percent,
                    state_json=dict(state_json or {}),
                )
                session.add(progress)
            else:
                progress.current_room = current_room
                progress.explored_percent = explored_percent
                progress.state_json = dict(state_json or progress.state_json or {})
                progress.state_version += 1
            session.flush()

            if previous_scene != scene.title:
                session.add(
                    CampaignEvent(
                        id=f"event_{uuid.uuid4().hex[:16]}",
                        campaign_id=campaign_id,
                        session_id=session_id,
                        event_type="scene_entered",
                        content=f"队伍进入场景：{scene.title}。",
                        actors=[],
                        visibility="party",
                        importance=3,
                        metadata_json={
                            "module_id": module.id,
                            "chapter_id": chapter.id,
                            "scene_id": scene.id,
                        },
                    )
                )
            session.add(
                ToolAudit(
                    id=f"audit_scene_{uuid.uuid4().hex[:16]}",
                    request_id=f"scene-set:{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    session_id=session_id,
                    actor_id=actor_id,
                    tool_name="dnd_module_set_scene",
                    engine_function="database.module_progress.set_scene",
                    arguments_json={
                        "scene_id": scene.id,
                        "current_room": current_room,
                        "explored_percent": explored_percent,
                    },
                    result_json={"scene_state_id": progress.id},
                    after_state_json=dict(progress.state_json or {}),
                    success=True,
                    state_version=progress.state_version,
                )
            )
            return self._info(progress, module, chapter, scene)

    def current(self, campaign_id: str) -> SceneProgressInfo | None:
        with self.database.transaction() as session:
            world = session.scalar(
                select(WorldState).where(WorldState.campaign_id == campaign_id)
            )
            if world is None:
                return None
            title = str((world.state_json or {}).get("current_scene", ""))
            if not title:
                return None
            row = session.execute(
                select(SceneState, SceneIndex, ModuleChapter, ModuleSource)
                .join(SceneIndex, SceneIndex.id == SceneState.scene_id)
                .join(ModuleChapter, ModuleChapter.id == SceneIndex.chapter_id)
                .join(ModuleSource, ModuleSource.id == ModuleChapter.module_id)
                .where(
                    SceneState.campaign_id == campaign_id,
                    SceneIndex.title == title,
                    ModuleSource.is_active.is_(True),
                )
                .order_by(SceneState.updated_at.desc())
            ).first()
            if row is None:
                return None
            progress, scene, chapter, module = row
            return self._info(progress, module, chapter, scene)

    @staticmethod
    def _info(
        progress: SceneState,
        module: ModuleSource,
        chapter: ModuleChapter,
        scene: SceneIndex,
    ) -> SceneProgressInfo:
        return SceneProgressInfo(
            campaign_id=progress.campaign_id,
            module_name=module.name,
            chapter_key=chapter.chapter_key,
            scene_id=scene.id,
            scene_title=scene.title,
            current_room=progress.current_room,
            explored_percent=progress.explored_percent,
            state_json=dict(progress.state_json or {}),
            state_version=progress.state_version,
        )
