-- Wahoo Workout Database Schema
-- Location: ~/.openclaw/workspace/training/wahoo.db

CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY,             -- Wahoo workout ID
    name TEXT,                          -- workout title
    starts TEXT,                        -- ISO8601 (UTC) start time
    minutes INTEGER,                    -- duration (Wahoo's coarse "minutes" field)
    workout_type_id INTEGER,            -- 0=run, 40=indoor cycle, 41=outdoor cycle, 42=mtb, 60=swim, ...
    plan_id INTEGER,
    route_id INTEGER,
    workout_token TEXT,
    created_at TEXT,
    updated_at TEXT,

    -- workout_summary fields (cast to numeric on read)
    distance_m REAL,
    duration_active_s REAL,
    duration_paused_s REAL,
    duration_total_s REAL,
    ascent_m REAL,
    cadence_avg REAL,
    calories REAL,
    heart_rate_avg REAL,
    power_avg REAL,
    power_np REAL,                      -- power_bike_np_last
    power_tss REAL,                     -- power_bike_tss_last
    speed_avg_ms REAL,
    work_j REAL,
    time_zone TEXT,

    -- FIT artifact tracking
    fit_url TEXT,                       -- workout_summary.file.url (CDN)
    fit_path TEXT,                      -- local download path
    fit_parsed_at TEXT,                 -- when we last parsed it

    -- FIT-derived session summary (filled by fit_parser)
    fit_start_time TEXT,
    fit_total_distance_m REAL,
    fit_total_elapsed_s REAL,
    fit_total_timer_s REAL,
    fit_total_ascent_m REAL,
    fit_total_descent_m REAL,
    fit_avg_power_w REAL,
    fit_max_power_w REAL,
    fit_normalized_power_w REAL,
    fit_threshold_power_w REAL,         -- FTP as configured on device
    fit_avg_heart_rate REAL,
    fit_max_heart_rate REAL,
    fit_avg_cadence REAL,
    fit_max_cadence REAL,
    fit_avg_speed_ms REAL,
    fit_max_speed_ms REAL,
    fit_avg_altitude_m REAL,
    fit_max_altitude_m REAL,
    fit_min_altitude_m REAL,
    fit_avg_grade REAL,
    fit_max_pos_grade REAL,
    fit_max_neg_grade REAL,
    fit_avg_temperature REAL,
    fit_max_temperature REAL,
    fit_left_right_balance REAL,
    fit_calories REAL,
    fit_record_count INTEGER,
    fit_num_laps INTEGER,

    -- FIT session power zone distribution (seconds per zone)
    fit_session_time_in_zone1 REAL,     -- <55% FTP
    fit_session_time_in_zone2 REAL,     -- 55–75% FTP
    fit_session_time_in_zone3 REAL,     -- 75–85% FTP
    fit_session_time_in_zone4 REAL,     -- 85–95% FTP
    fit_session_time_in_zone5 REAL,     -- 95–110% FTP
    fit_session_time_in_zone6 REAL,     -- >110% FTP

    synced TEXT DEFAULT '0000-00-00',
    fetched_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_workouts_starts ON workouts(starts);
CREATE INDEX IF NOT EXISTS idx_workouts_type ON workouts(workout_type_id);
CREATE INDEX IF NOT EXISTS idx_workouts_synced ON workouts(synced);

CREATE TABLE IF NOT EXISTS sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    synced_at TEXT DEFAULT (datetime('now')),
    workouts_seen INTEGER,
    workouts_new INTEGER,
    fit_downloaded INTEGER,
    status TEXT DEFAULT 'OK'            -- OK, ERROR, PARTIAL
);

CREATE TABLE IF NOT EXISTS laps (
    workout_id INTEGER,
    lap_number INTEGER,                 -- 1-indexed, matches FIT order
    start_time TEXT,
    end_time TEXT,
    elapsed_s REAL,
    timer_s REAL,
    distance_m REAL,
    ascent_m REAL,
    descent_m REAL,
    calories REAL,
    work_j REAL,
    avg_power_w REAL,
    np_w REAL,                          -- normalized power
    max_power_w REAL,
    avg_heart_rate REAL,
    max_heart_rate REAL,
    avg_cadence REAL,
    max_cadence REAL,
    avg_speed_ms REAL,
    max_speed_ms REAL,
    avg_altitude REAL,
    enhanced_avg_altitude REAL,
    max_altitude REAL,
    min_altitude REAL,
    avg_grade REAL,
    max_pos_grade REAL,
    max_neg_grade REAL,
    avg_temperature REAL,
    max_temperature REAL,
    left_right_balance REAL,
    lap_trigger TEXT,                   -- MANUAL, DISTANCE, DURATION, FITNESS_EQUIPMENT
    time_in_zone1 REAL,                 -- seconds in power zone 1 (<55% FTP)
    time_in_zone2 REAL,                 -- 55–75% FTP
    time_in_zone3 REAL,                 -- 75–85% FTP
    time_in_zone4 REAL,                 -- 85–95% FTP
    time_in_zone5 REAL,                 -- 95–110% FTP
    time_in_zone6 REAL,                 -- >110% FTP
    FOREIGN KEY (workout_id) REFERENCES workouts(id)
);

CREATE INDEX IF NOT EXISTS idx_laps_workout ON laps(workout_id);

CREATE TABLE IF NOT EXISTS records (
    workout_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,            -- ISO8601, 1 Hz typical
    power_w REAL,
    heart_rate REAL,
    cadence REAL,
    speed_ms REAL,
    enhanced_speed_ms REAL,
    distance_m REAL,
    altitude_m REAL,
    enhanced_altitude_m REAL,
    position_lat_deg REAL,              -- converted from semicircles by parser
    position_long_deg REAL,
    grade REAL,
    temperature REAL,
    battery_soc REAL,
    gps_accuracy REAL,
    left_right_balance REAL,
    ascent_m REAL,
    descent_m REAL,
    calories REAL,
    FOREIGN KEY (workout_id) REFERENCES workouts(id)
);

CREATE INDEX IF NOT EXISTS idx_records_workout_ts ON records(workout_id, timestamp);

CREATE TABLE IF NOT EXISTS device_info (
    workout_id INTEGER NOT NULL,
    device_index INTEGER,               -- FIT device_info.device_index
    timestamp TEXT,
    manufacturer TEXT,
    product TEXT,                       -- stored as TEXT for forward compat
    product_name TEXT,
    serial_number TEXT,
    software_version TEXT,
    hardware_version TEXT,
    battery_status TEXT,
    battery_charge_pct REAL,
    device_type TEXT,
    source_type TEXT,
    ant_device_number INTEGER,
    descriptor TEXT,
    crank_length_mm REAL,
    FOREIGN KEY (workout_id) REFERENCES workouts(id)
);

CREATE INDEX IF NOT EXISTS idx_device_info_workout ON device_info(workout_id);

CREATE TABLE IF NOT EXISTS zones (
    workout_id INTEGER NOT NULL,
    zone_type TEXT NOT NULL,            -- 'hr' | 'power'
    zone_number INTEGER NOT NULL,       -- from FIT message_index
    high_value REAL,                    -- bpm for hr, watts for power
    FOREIGN KEY (workout_id) REFERENCES workouts(id)
);

CREATE INDEX IF NOT EXISTS idx_zones_workout ON zones(workout_id, zone_type);
