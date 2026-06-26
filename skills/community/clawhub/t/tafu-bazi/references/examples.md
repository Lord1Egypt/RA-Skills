# Tafu API Examples

Use `{baseDir}/scripts/tafu_api.sh` from the skill root.

## Check credits

```sh
{baseDir}/scripts/tafu_api.sh GET /credits
```

## Calculate BaZi chart

```json
{
  "gender": "male",
  "calendarType": "solar",
  "birthYear": 1990,
  "birthMonth": 6,
  "birthDay": 15,
  "birthHour": 14,
  "birthMinute": 30,
  "location": "北京"
}
```

```sh
cat >/tmp/tafu-bazi.json <<'EOF'
{
  "gender": "male",
  "calendarType": "solar",
  "birthYear": 1990,
  "birthMonth": 6,
  "birthDay": 15,
  "birthHour": 14,
  "birthMinute": 30,
  "location": "北京"
}
EOF
{baseDir}/scripts/tafu_api.sh POST /bazi/calculate @/tmp/tafu-bazi.json
```

## Create a thematic reading

```json
{
  "birthData": {
    "gender": "female",
    "calendarType": "solar",
    "birthYear": 1994,
    "birthMonth": 11,
    "birthDay": 2,
    "birthHour": 8,
    "birthMinute": 15,
    "location": "Shanghai"
  },
  "theme": "career_wealth"
}
```

```sh
cat >/tmp/tafu-reading.json <<'EOF'
{
  "birthData": {
    "gender": "female",
    "calendarType": "solar",
    "birthYear": 1994,
    "birthMonth": 11,
    "birthDay": 2,
    "birthHour": 8,
    "birthMinute": 15,
    "location": "Shanghai"
  },
  "theme": "career_wealth"
}
EOF
{baseDir}/scripts/tafu_api.sh POST /reading @/tmp/tafu-reading.json
```

## Create a soul song

```json
{
  "birthData": {
    "gender": "female",
    "calendarType": "solar",
    "birthYear": 1994,
    "birthMonth": 11,
    "birthDay": 2,
    "birthHour": 8,
    "birthMinute": 15,
    "location": "Shanghai"
  }
}
```

## Create synastry

```json
{
  "subjectA": {
    "gender": "male",
    "calendarType": "solar",
    "birthYear": 1990,
    "birthMonth": 6,
    "birthDay": 15,
    "birthHour": 14,
    "birthMinute": 30,
    "location": "北京"
  },
  "subjectB": {
    "gender": "female",
    "calendarType": "solar",
    "birthYear": 1994,
    "birthMonth": 11,
    "birthDay": 2,
    "birthHour": 8,
    "birthMinute": 15,
    "location": "Shanghai"
  }
}
```

## Poll a task

```sh
{baseDir}/scripts/tafu_api.sh GET /tasks/task_xxx
```
