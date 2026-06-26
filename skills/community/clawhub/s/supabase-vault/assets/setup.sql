-- =============================================================================
-- Supabase Vault Setup for OpenClaw
-- =============================================================================
-- Run this ONCE in your Supabase project's SQL Editor.
-- Creates the wrapper functions needed by OpenClaw to interact with Vault.
-- All functions are restricted to service_role — the anon/authenticated roles
-- cannot read or write secrets.
-- =============================================================================

-- Enable Vault extension (idempotent)
CREATE EXTENSION IF NOT EXISTS vault WITH SCHEMA vault;

-- =============================================================================
-- insert_secret(name, secret)
-- Creates or replaces a secret. Returns the secret UUID.
-- =============================================================================
CREATE OR REPLACE FUNCTION insert_secret(name text, secret text)
RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  existing_id uuid;
BEGIN
  -- Check if a secret with this name already exists
  SELECT id INTO existing_id FROM vault.secrets WHERE vault.secrets.name = insert_secret.name LIMIT 1;

  IF existing_id IS NOT NULL THEN
    -- Update existing secret
    PERFORM vault.update_secret(existing_id, secret, name);
    RETURN existing_id;
  ELSE
    -- Create new secret
    RETURN vault.create_secret(secret, name);
  END IF;
END;
$$;

REVOKE EXECUTE ON FUNCTION insert_secret(text, text) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION insert_secret(text, text) FROM anon;
REVOKE EXECUTE ON FUNCTION insert_secret(text, text) FROM authenticated;
GRANT  EXECUTE ON FUNCTION insert_secret(text, text) TO service_role;

-- =============================================================================
-- read_secret(secret_name)
-- Returns the decrypted secret value for a given name.
-- Returns NULL if not found.
-- =============================================================================
CREATE OR REPLACE FUNCTION read_secret(secret_name text)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  secret_value text;
BEGIN
  SELECT decrypted_secret
  INTO   secret_value
  FROM   vault.decrypted_secrets
  WHERE  name = secret_name
  LIMIT  1;

  RETURN secret_value;
END;
$$;

REVOKE EXECUTE ON FUNCTION read_secret(text) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION read_secret(text) FROM anon;
REVOKE EXECUTE ON FUNCTION read_secret(text) FROM authenticated;
GRANT  EXECUTE ON FUNCTION read_secret(text) TO service_role;

-- =============================================================================
-- delete_secret(secret_name)
-- Removes a secret by name. No-op if not found.
-- =============================================================================
CREATE OR REPLACE FUNCTION delete_secret(secret_name text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  DELETE FROM vault.secrets WHERE name = secret_name;
END;
$$;

REVOKE EXECUTE ON FUNCTION delete_secret(text) FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION delete_secret(text) FROM anon;
REVOKE EXECUTE ON FUNCTION delete_secret(text) FROM authenticated;
GRANT  EXECUTE ON FUNCTION delete_secret(text) TO service_role;

-- =============================================================================
-- list_secret_names()
-- Returns all secret names (no values). Safe to call — no decryption.
-- =============================================================================
CREATE OR REPLACE FUNCTION list_secret_names()
RETURNS TABLE(name text, id uuid, created_at timestamptz, updated_at timestamptz)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  RETURN QUERY
  SELECT
    s.name,
    s.id,
    s.created_at,
    s.updated_at
  FROM vault.secrets s
  WHERE s.name IS NOT NULL
  ORDER BY s.name;
END;
$$;

REVOKE EXECUTE ON FUNCTION list_secret_names() FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION list_secret_names() FROM anon;
REVOKE EXECUTE ON FUNCTION list_secret_names() FROM authenticated;
GRANT  EXECUTE ON FUNCTION list_secret_names() TO service_role;

-- =============================================================================
-- Done! Verify with:
--   SELECT proname FROM pg_proc
--   WHERE proname IN ('insert_secret','read_secret','delete_secret','list_secret_names');
-- =============================================================================
