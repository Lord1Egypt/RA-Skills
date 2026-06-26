# TeslaMate Database Schema

## Tables

### positions
Vehicle position data including battery state.

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| car_id | integer | Vehicle ID |
| date | timestamp | Record time |
| latitude | float | Latitude |
| longitude | float | Longitude |
| battery_level | integer | SOC 0-100% |
| ideal_battery_range_km | float | Ideal range (km) |
| rated_battery_range_km | float | Rated range (km) |
| outside_temp | float | Outside temperature (°C) |
| inside_temp | float | Inside temperature (°C) |
| odometer | numeric | Total km |
| speed | integer | Current speed (km/h) |
| power | integer | Power kW |
| state | string | driving/charging/idle |

### drives
Trip records.

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| car_id | integer | Vehicle ID |
| start_date | timestamp | Trip start |
| end_date | timestamp | Trip end |
| distance | float | Distance (km) |
| duration_min | integer | Duration (minutes) |
| start_km | numeric | Odometer start |
| end_km | numeric | Odometer end |
| start_ideal_range_km | float | Range at start |
| end_ideal_range_km | float | Range at end |
| speed_max | integer | Max speed |
| power_max | integer | Max power |
| outside_temp_avg | float | Avg outside temp |
| inside_temp_avg | float | Avg inside temp |

### charging_processes
Charging sessions.

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| car_id | integer | Vehicle ID |
| start_date | timestamp | Charge start |
| end_date | timestamp | Charge end (NULL if ongoing) |
| start_battery_level | integer | SOC at start |
| end_battery_level | integer | SOC at end |
| charge_energy_added | float | Energy added (kWh) |
| duration_min | integer | Duration |

### charges
Individual charge records (within a process).

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| charging_process_id | integer | Parent process |
| date | timestamp | Record time |
| battery_level | integer | SOC |
| charger_power | float | Power (kW) |
| charger_voltage | float | Voltage (V) |
| charger_actual_current | float | Current (A) |
| charge_energy_added | float | Energy added (kWh) |

### states
Vehicle state history.

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| car_id | integer | Vehicle ID |
| start_date | timestamp | State start |
| end_date | timestamp | State end |
| state | string | online/offline/driving/charging/asleep/updating |

### cars
Vehicle information.

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| name | string | Display name |
| vin | string | VIN |
| model | string | Model 3/Y/S/X |
| trim | string | Trim variant |
| exterior_color | string | Color |
| options | string | Option codes |

### settings
TeslaMate configuration.

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| base_url | string | Grafana URL |
| unit_of_length | string | km/mi |
| unit_of_temperature | C/F | Temperature unit |
| preferred_range | string | ideal/rated |
| currency | string | Currency symbol |

### geofences
Saved locations.

| Column | Type | Description |
|--------|------|-------------|
| id | integer | Primary key |
| name | string | Location name |
| latitude | float | Center lat |
| longitude | float | Center lon |
| radius | integer | Radius (m) |

## Common Queries

### Current Status
```sql
SELECT battery_level, ideal_battery_range_km, date 
FROM positions ORDER BY date DESC LIMIT 1
```

### Vehicle State
```sql
SELECT state, start_date FROM states 
ORDER BY start_date DESC LIMIT 1
```

### Today's Drives
```sql
SELECT SUM(distance), COUNT(*), SUM(duration_min) 
FROM drives WHERE start_date >= CURRENT_DATE
```

### Last 5 Drives
```sql
SELECT id, start_date, end_date, distance, duration_min 
FROM drives ORDER BY id DESC LIMIT 5
```

### Last Charge
```sql
SELECT start_date, end_date, start_battery_level, end_battery_level, 
       charge_energy_added, duration_min
FROM charging_processes ORDER BY start_date DESC LIMIT 1
```

### Current Charge (if charging)
```sql
SELECT c.battery_level, c.charger_power, c.charger_voltage, c.date
FROM charges c
JOIN charging_processes p ON c.charging_process_id = p.id
WHERE p.end_date IS NULL
ORDER BY c.date DESC LIMIT 1
```

### Battery Health
```sql
SELECT battery_level, ideal_battery_range_km, rated_battery_range_km, date
FROM positions ORDER BY date DESC LIMIT 1
```

### Odometer
```sql SELECT odometer FROM positions 
WHERE ideal_battery_range_km IS NOT NULL 
ORDER BY date DESC LIMIT 1
```

### All Vehicles
```sql
SELECT id, name, model, trim, vin FROM cars
```
