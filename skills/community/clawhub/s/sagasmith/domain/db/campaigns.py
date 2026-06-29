"""Campaign lifecycle operations for the D&D database."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy import select

from .database import Database
from .models import (
    Campaign,
    CampaignRuleProfile,
    CampaignRulePublication,
    CampaignSave,
    Party,
    PlotSummary,
    RulePublication,
    RuleSet,
    WorldState,
)


class CampaignError(RuntimeError):
    """Base error for campaign lifecycle operations."""


class CampaignAlreadyExistsError(CampaignError):
    """A campaign already uses the requested ID."""


class CampaignNotFoundError(CampaignError):
    """The requested campaign does not exist."""


_DEFAULT_RULE_SET_ID = "dnd5e-2024-srd-5.2.1"


@dataclass(frozen=True)
class CampaignInfo:
    id: str
    name: str
    status: str
    module_name: str | None
    system_version: str
    description: str | None
    save_count: int = 0


class CampaignService:
    """Create, inspect, list, and change campaign lifecycle state."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self,
        name: str,
        *,
        campaign_id: str | None = None,
        module_name: str | None = None,
        description: str | None = None,
    ) -> CampaignInfo:
        campaign_id = campaign_id or f"campaign_{uuid.uuid4().hex[:16]}"
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is not None:
                raise CampaignAlreadyExistsError(
                    f"campaign already exists: {campaign_id}"
                )
            campaign = Campaign(
                id=campaign_id,
                name=name,
                module_name=module_name,
                description=description,
                config={"user_md_player_roles": ""},
            )
            session.add(campaign)
            session.flush()
            session.add(
                WorldState(
                    id=f"world_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    state_json={
                        "faction_relations": {},
                        "discovered_locations": [],
                        "quest_progress": {"完成": [], "进行中": [], "待触发": []},
                        "key_npc_status": {},
                        "current_chapter": 0,
                        "current_scene": "",
                        "day_in_game": 1,
                    },
                )
            )
            session.add(
                Party(
                    id=f"party_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    state_json={},
                )
            )
            session.add(
                PlotSummary(
                    id=f"summary_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    scope="campaign",
                    summary="",
                )
            )
            # A newly created campaign starts on the active core rules release
            # when a corpus is installed. Supplements remain an explicit choice.
            rule_set = session.get(RuleSet, _DEFAULT_RULE_SET_ID)
            if rule_set is None or rule_set.status != "active":
                rule_set = session.scalar(
                    select(RuleSet)
                    .where(RuleSet.status == "active")
                    .order_by(RuleSet.created_at.desc(), RuleSet.id)
                    .limit(1)
                )
            if rule_set is not None:
                profile_id = f"rule_profile_{uuid.uuid4().hex}"
                session.add(
                    CampaignRuleProfile(
                        id=profile_id,
                        campaign_id=campaign_id,
                        rule_set_id=rule_set.id,
                        locale=rule_set.locale,
                    )
                )
                core_publications = session.scalars(
                    select(RulePublication)
                    .where(
                        RulePublication.rule_set_id == rule_set.id,
                        RulePublication.publication_type == "core",
                        RulePublication.parent_publication_id.is_(None),
                    )
                    .order_by(RulePublication.priority.desc(), RulePublication.id)
                )
                for publication in core_publications:
                    session.add(
                        CampaignRulePublication(
                            id=f"rule_profile_publication_{uuid.uuid4().hex}",
                            profile_id=profile_id,
                            publication_id=publication.id,
                            enabled=True,
                            priority=publication.priority,
                        )
                    )
            return self._info(campaign, save_count=0)

    def list(self, *, status: str | None = None) -> list[CampaignInfo]:
        with self.database.transaction() as session:
            statement = select(Campaign).order_by(Campaign.created_at, Campaign.id)
            if status is not None:
                statement = statement.where(Campaign.status == status)
            return [
                self._info(c, save_count=self._save_count(session, c.id))
                for c in session.scalars(statement)
            ]

    def get(self, campaign_id: str) -> CampaignInfo:
        with self.database.transaction() as session:
            campaign = session.get(Campaign, campaign_id)
            if campaign is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            return self._info(campaign, save_count=self._save_count(session, campaign_id))

    def set_status(self, campaign_id: str, status: str) -> CampaignInfo:
        if status not in {"active", "archived"}:
            raise ValueError("status must be active or archived")
        with self.database.transaction() as session:
            campaign = session.get(Campaign, campaign_id)
            if campaign is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            campaign.status = status
            session.flush()
            return self._info(campaign, save_count=self._save_count(session, campaign_id))

    def delete(self, campaign_id: str) -> None:
        with self.database.transaction() as session:
            campaign = session.get(Campaign, campaign_id)
            if campaign is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            session.delete(campaign)

    def has_saves(self, campaign_id: str) -> bool:
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            return self._save_count(session, campaign_id) > 0

    def start(
        self,
        name: str,
        *,
        campaign_id: str | None = None,
        module_name: str | None = None,
        description: str | None = None,
        source_path: str | None = None,
    ) -> CampaignInfo:
        """One-shot campaign startup: create + initial snapshot + optional module import.

        Returns the CampaignInfo for the newly created campaign.
        Raises CampaignAlreadyExistsError if *campaign_id* is taken.
        """
        from .module_content import ModuleImportService
        from .snapshots import CampaignSnapshotService

        campaign_id = campaign_id or f"campaign_{uuid.uuid4().hex[:16]}"
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is not None:
                raise CampaignAlreadyExistsError(
                    f"campaign already exists: {campaign_id}"
                )
            campaign = Campaign(
                id=campaign_id,
                name=name,
                module_name=module_name,
                description=description,
                config={"user_md_player_roles": ""},
            )
            session.add(campaign)
            session.flush()
            session.add(
                WorldState(
                    id=f"world_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    state_json={
                        "faction_relations": {},
                        "discovered_locations": [],
                        "quest_progress": {"完成": [], "进行中": [], "待触发": []},
                        "key_npc_status": {},
                        "current_chapter": 0,
                        "current_scene": "",
                        "day_in_game": 1,
                    },
                )
            )
            session.add(
                Party(
                    id=f"party_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                )
            )
            session.add(
                PlotSummary(
                    id=f"summary_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    scope="campaign",
                    summary="",
                )
            )
            rule_set = session.get(RuleSet, _DEFAULT_RULE_SET_ID) or session.scalar(
                select(RuleSet).order_by(RuleSet.created_at)
            )
            if rule_set is not None:
                profile_id = f"profile_{uuid.uuid4().hex[:16]}"
                session.add(
                    CampaignRuleProfile(
                        id=profile_id,
                        campaign_id=campaign_id,
                        rule_set_id=rule_set.id,
                    )
                )
                session.flush()
                for publication in session.scalars(
                    select(RulePublication).order_by(RulePublication.priority)
                ):
                    session.add(
                        CampaignRulePublication(
                            id=f"rule_profile_publication_{uuid.uuid4().hex}",
                            profile_id=profile_id,
                            publication_id=publication.id,
                            enabled=True,
                            priority=publication.priority,
                        )
                    )
            session.flush()
            # Create initial snapshot (slot 1)
            snapshots = CampaignSnapshotService(self.database)
            snapshots._create_in_session(session, campaign_id, label="初始状态")
        # Import module outside the campaign transaction to avoid nested transactions
        if source_path:
            try:
                ModuleImportService(self.database).import_path(
                    campaign_id,
                    source_path,
                    name=module_name or name,
                    activate=True,
                    embed=True,
                )
            except Exception:
                pass  # Module import failure is non-fatal for campaign creation
        return self.get(campaign_id)

    def _save_count(self, session: Any, campaign_id: str) -> int:
        from sqlalchemy import func as _func

        return (
            session.scalar(
                select(_func.count()).where(CampaignSave.campaign_id == campaign_id)
            )
            or 0
        )

    def _info(self, campaign: Campaign, save_count: int | None = None) -> CampaignInfo:
        return CampaignInfo(
            id=campaign.id,
            name=campaign.name,
            status=campaign.status,
            module_name=campaign.module_name,
            system_version=campaign.system_version,
            description=campaign.description,
            save_count=save_count if save_count is not None else 0,
        )
