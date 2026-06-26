#!/bin/sh
set -eu

DB_CONTAINER="supabase-db"
DB_USER="postgres"
DB_NAME="postgres"
AGENT_ID="c61b873f-354c-431f-9dd7-f627120d576c"

usage() {
  echo "Usage:"
  echo "  reaction-processor.sh record-duplicate-skipped"
  echo "  reaction-processor.sh record-proposal-created"
  exit 1
}

cmd="${1:-}"
[ -n "$cmd" ] || usage

case "$cmd" in
  record-duplicate-skipped)
    docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<SQL
DO \$\$
DECLARE
  v_trigger RECORD;
  v_event_id uuid;
  v_stale_count integer := 0;
  v_titles text := '';
BEGIN
  SELECT *
  INTO v_trigger
  FROM public.openclaw_trigger_rules
  WHERE name = 'stale_missions_alert'
    AND enabled = true
  LIMIT 1;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Trigger stale_missions_alert no encontrado o deshabilitado.';
  END IF;

  SELECT COUNT(*),
         COALESCE(string_agg(title, ' | ' ORDER BY created_at), '')
  INTO v_stale_count, v_titles
  FROM public.openclaw_missions
  WHERE status = 'running'
    AND started_at IS NOT NULL
    AND started_at < now() - make_interval(hours => COALESCE((v_trigger.conditions->>'threshold_hours')::int, 24));

  INSERT INTO public.openclaw_agent_events (
    agent_id,
    kind,
    title,
    summary,
    tags,
    metadata
  ) VALUES (
    '$AGENT_ID'::uuid,
    'duplicate_skipped',
    'stale_missions_alert',
    'Se detectó una propuesta pending equivalente y no se creó duplicado. Misiones: ' || v_titles,
    ARRAY['trigger','heartbeat','duplicate_skipped'],
    jsonb_build_object(
      'trigger_name', v_trigger.name,
      'stale_count', v_stale_count,
      'titles', v_titles
    )
  )
  RETURNING id INTO v_event_id;

  INSERT INTO public.openclaw_agent_reactions (
    source_event_id,
    source_agent_id,
    target_agent_id,
    reaction_type,
    context,
    status
  ) VALUES (
    v_event_id,
    '$AGENT_ID'::uuid,
    '$AGENT_ID'::uuid,
    'duplicate_skipped',
    jsonb_build_object(
      'trigger_name', v_trigger.name,
      'stale_count', v_stale_count,
      'titles', v_titles
    ),
    'skipped'
  );

  RAISE NOTICE 'Evento/reacción duplicate_skipped registrados.';
END \$\$;
SQL
    ;;
  record-proposal-created)
    docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<SQL
DO \$\$
DECLARE
  v_trigger RECORD;
  v_event_id uuid;
  v_stale_count integer := 0;
  v_titles text := '';
BEGIN
  SELECT *
  INTO v_trigger
  FROM public.openclaw_trigger_rules
  WHERE name = 'stale_missions_alert'
    AND enabled = true
  LIMIT 1;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Trigger stale_missions_alert no encontrado o deshabilitado.';
  END IF;

  SELECT COUNT(*),
         COALESCE(string_agg(title, ' | ' ORDER BY created_at), '')
  INTO v_stale_count, v_titles
  FROM public.openclaw_missions
  WHERE status = 'running'
    AND started_at IS NOT NULL
    AND started_at < now() - make_interval(hours => COALESCE((v_trigger.conditions->>'threshold_hours')::int, 24));

  INSERT INTO public.openclaw_agent_events (
    agent_id,
    kind,
    title,
    summary,
    tags,
    metadata
  ) VALUES (
    '$AGENT_ID'::uuid,
    'trigger_fired',
    'stale_missions_alert',
    'Se detectaron ' || v_stale_count || ' misión(es) stale. Misiones: ' || v_titles,
    ARRAY['trigger','heartbeat','missions_stale'],
    jsonb_build_object(
      'trigger_name', v_trigger.name,
      'stale_count', v_stale_count,
      'titles', v_titles
    )
  )
  RETURNING id INTO v_event_id;

  INSERT INTO public.openclaw_agent_reactions (
    source_event_id,
    source_agent_id,
    target_agent_id,
    reaction_type,
    context,
    status
  ) VALUES (
    v_event_id,
    '$AGENT_ID'::uuid,
    '$AGENT_ID'::uuid,
    'proposal_created',
    jsonb_build_object(
      'trigger_name', v_trigger.name,
      'stale_count', v_stale_count,
      'titles', v_titles
    ),
    'completed'
  );

  UPDATE public.openclaw_trigger_rules
  SET
    fire_count = COALESCE(fire_count, 0) + 1,
    last_fired_at = now()
  WHERE id = v_trigger.id;

  RAISE NOTICE 'Evento/reacción proposal_created y trigger actualizados.';
END \$\$;
SQL
    ;;
  *)
    usage
    ;;
esac
