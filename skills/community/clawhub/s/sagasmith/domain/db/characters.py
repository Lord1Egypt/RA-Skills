"""Campaign-scoped character persistence operations."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .campaigns import CampaignNotFoundError
from .database import Database
from .models import Campaign, Character, Party, ToolAudit


class CharacterError(RuntimeError):
    """Base error for character persistence."""


class CharacterAlreadyExistsError(CharacterError):
    """The campaign already contains a character with the requested name."""


@dataclass(frozen=True)
class CharacterInfo:
    id: str
    campaign_id: str
    party_id: str | None
    name: str
    player_name: str | None
    class_name: str
    level: int
    hp: int
    max_hp: int
    armor_class: int
    sheet_json: dict[str, Any]


class CharacterService:
    """Create and inspect authoritative campaign character records."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self,
        campaign_id: str,
        name: str,
        *,
        character_id: str | None = None,
        player_name: str | None = None,
        class_name: str | None = None,
        level: int | None = None,
        hp: int | None = None,
        max_hp: int | None = None,
        armor_class: int | None = None,
        sheet_json: dict[str, Any] | None = None,
        actor_id: str | None = None,
    ) -> CharacterInfo:
        sheet = dict(sheet_json or {})
        resolved_class = class_name or str(sheet.get("class_name") or sheet.get("class") or "")
        resolved_level = int(level if level is not None else sheet.get("level", 1))
        hp_data = sheet.get("hp")
        resolved_hp = int(
            hp
            if hp is not None
            else (hp_data.get("current", 10) if isinstance(hp_data, dict) else hp_data or 10)
        )
        resolved_max_hp = int(
            max_hp
            if max_hp is not None
            else (hp_data.get("max", resolved_hp) if isinstance(hp_data, dict) else resolved_hp)
        )
        resolved_ac = int(
            armor_class if armor_class is not None else sheet.get("ac", 10)
        )
        character_id = character_id or f"character_{uuid.uuid4().hex[:16]}"

        try:
            with self.database.transaction() as session:
                campaign = session.get(Campaign, campaign_id)
                if campaign is None:
                    raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
                party = session.scalar(select(Party).where(Party.campaign_id == campaign_id))
                character = Character(
                    id=character_id,
                    campaign_id=campaign_id,
                    party_id=party.id if party is not None else None,
                    name=name,
                    player_name=player_name,
                    class_name=resolved_class,
                    level=resolved_level,
                    hp=resolved_hp,
                    max_hp=resolved_max_hp,
                    armor_class=resolved_ac,
                    sheet_json=sheet,
                )
                session.add(character)
                session.flush()
                audit_id = f"audit_character_{uuid.uuid4().hex[:16]}"
                session.add(
                    ToolAudit(
                        id=audit_id,
                        request_id=f"character-create:{uuid.uuid4().hex}",
                        campaign_id=campaign_id,
                        actor_id=actor_id,
                        tool_name="dnd_character_create",
                        engine_function="database.character.create",
                        arguments_json={"name": name, "player_name": player_name},
                        result_json={"character_id": character.id},
                        after_state_json=sheet,
                        success=True,
                        state_version=character.state_version,
                    )
                )
                return self._info(character)
        except IntegrityError as exc:
            raise CharacterAlreadyExistsError(
                f"character already exists in campaign {campaign_id}: {name}"
            ) from exc

    def list(self, campaign_id: str) -> list[CharacterInfo]:
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            statement = (
                select(Character)
                .where(Character.campaign_id == campaign_id)
                .order_by(Character.created_at, Character.id)
            )
            return [self._info(character) for character in session.scalars(statement)]

    @staticmethod
    def _info(character: Character) -> CharacterInfo:
        return CharacterInfo(
            id=character.id,
            campaign_id=character.campaign_id,
            party_id=character.party_id,
            name=character.name,
            player_name=character.player_name,
            class_name=character.class_name,
            level=character.level,
            hp=character.hp,
            max_hp=character.max_hp,
            armor_class=character.armor_class,
            sheet_json=dict(character.sheet_json or {}),
        )
