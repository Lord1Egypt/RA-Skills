-- workout-track schema
-- Run this once on your PostgreSQL database to create the required tables.

CREATE SCHEMA IF NOT EXISTS sport;

CREATE TABLE sport.sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_date    DATE NOT NULL DEFAULT CURRENT_DATE,
    session_type    TEXT NOT NULL DEFAULT 'strength',
    duration_min    SMALLINT,
    feeling         SMALLINT CHECK (feeling BETWEEN 1 AND 10),
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sport.exercises (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id         UUID NOT NULL REFERENCES sport.sessions(id) ON DELETE CASCADE,
    exercise_name      TEXT NOT NULL,
    sets               SMALLINT,
    reps               SMALLINT,
    weight_kg          NUMERIC(5, 1),
    rpe                NUMERIC(3, 1) CHECK (rpe BETWEEN 1 AND 10),
    rest_sec           SMALLINT,
    order_in_session   SMALLINT NOT NULL DEFAULT 1,
    notes              TEXT
);

CREATE INDEX ON sport.exercises (session_id);
