# SwitchBot API Examples

## List Devices

```bash
node scripts/switchbot_cli.js list
```

## Get Device Status

```bash
node scripts/switchbot_cli.js status E1AA22334455
```

## Basic On/Off/Toggle

```bash
# Turn on a Plug Mini
node scripts/switchbot_cli.js cmd 3C8427B2118A turnOn

# Toggle
node scripts/switchbot_cli.js cmd 3C8427B2118A toggle
```

## Bot

```bash
node scripts/switchbot_cli.js cmd DFC21012C18F press
```

## Curtain / Curtain 3

```bash
# Open to 50%
node scripts/switchbot_cli.js cmd AABBCCDD setPosition --pos=50

# Pause
node scripts/switchbot_cli.js cmd AABBCCDD pause
```

## Lock / Lock Pro / Lock Ultra

```bash
node scripts/switchbot_cli.js cmd FB3A29024E71 lock
node scripts/switchbot_cli.js cmd FB3A29024E71 unlock
node scripts/switchbot_cli.js cmd FB3A29024E71 deadbolt
```

## Lights (Color Bulb / Strip Light / Floor Lamp / Strip Light 3)

```bash
# Set RGB color
node scripts/switchbot_cli.js cmd DC0675A7675A setColor --param="255:100:0"

# Set brightness
node scripts/switchbot_cli.js cmd DC0675A7675A setBrightness --param=80

# Set color temperature
node scripts/switchbot_cli.js cmd DC0675A7675A setColorTemperature --param=4000
```

## Fans (Battery Circulator / Circulator / Standing Circulator)

```bash
node scripts/switchbot_cli.js cmd AABB turnOn
node scripts/switchbot_cli.js cmd AABB setWindMode --param=natural
node scripts/switchbot_cli.js cmd AABB setWindSpeed --param=50
node scripts/switchbot_cli.js cmd AABB setNightLightMode --param=1
node scripts/switchbot_cli.js cmd AABB closeDelay --param=3600
```

## Robot Vacuum S1 / S1 Plus / K10+ / K10+ Pro

```bash
node scripts/switchbot_cli.js cmd 360TY400103021683 start
node scripts/switchbot_cli.js cmd 360TY400103021683 stop
node scripts/switchbot_cli.js cmd 360TY400103021683 dock
node scripts/switchbot_cli.js cmd 360TY400103021683 PowLevel --param=2
```

## Robot Vacuum S10 / S20 / K10+ Pro Combo / K20+ Pro / K11+

```bash
# Start sweep + mop
node scripts/switchbot_cli.js cmd AABB startClean --param='{"action":"sweep_mop","param":{"fanLevel":2,"waterLevel":1,"times":1}}'

# Pause / Dock
node scripts/switchbot_cli.js cmd AABB pause
node scripts/switchbot_cli.js cmd AABB dock

# Set volume
node scripts/switchbot_cli.js cmd AABB setVolume --param=50

# Self clean (S10/S20 only)
node scripts/switchbot_cli.js cmd AABB selfClean --param=1
```

## Blind Tilt

```bash
node scripts/switchbot_cli.js cmd AABB setPosition --param="up;60"
node scripts/switchbot_cli.js cmd AABB fullyOpen
node scripts/switchbot_cli.js cmd AABB closeUp
```

## Roller Shade

```bash
node scripts/switchbot_cli.js cmd AABB setPosition --param=50
```

## Evaporative Humidifier

```bash
# Auto mode, target 60% humidity
node scripts/switchbot_cli.js cmd A0A3B32CAE62 setMode --param='{"mode":7,"targetHumidify":60}'

# Child lock
node scripts/switchbot_cli.js cmd A0A3B32CAE62 setChildLock --param=true
```

## Air Purifier

```bash
# Auto mode
node scripts/switchbot_cli.js cmd ACA704AF64FE setMode --param='{"mode":2,"fanGear":2}'

# Child lock
node scripts/switchbot_cli.js cmd ACA704AF64FE setChildLock --param=1
```

## Smart Radiator Thermostat

```bash
node scripts/switchbot_cli.js cmd AABB setMode --param=1
node scripts/switchbot_cli.js cmd AABB setManualModeTemperature --param=22
```

## Relay Switch 1PM / 1

```bash
node scripts/switchbot_cli.js cmd C04E30DFEE06 turnOn
node scripts/switchbot_cli.js cmd C04E30DFEE06 toggle
node scripts/switchbot_cli.js cmd C04E30DFEE06 setMode --param=0
```

## Relay Switch 2PM (dual channel)

```bash
# Turn on channel 1
node scripts/switchbot_cli.js cmd AABB turnOn --param="1"
# Set mode for channel 2
node scripts/switchbot_cli.js cmd AABB setMode --param="2;0"
```

## Garage Door Opener

```bash
node scripts/switchbot_cli.js cmd AABB turnOn
```

## Video Doorbell

```bash
node scripts/switchbot_cli.js cmd AABB enableMotionDetection
node scripts/switchbot_cli.js cmd AABB disableMotionDetection
```

## AI Art Frame

```bash
node scripts/switchbot_cli.js cmd B0E9FEB6F885 next
node scripts/switchbot_cli.js cmd B0E9FEB6F885 previous
```

## Keypad / Keypad Touch / Keypad Vision

```bash
# Create permanent passcode
node scripts/switchbot_cli.js cmd DE133622237A createKey --param='{"name":"Front Door","type":"permanent","password":"12345678"}'

# Create temporary passcode
node scripts/switchbot_cli.js cmd DE133622237A createKey --param='{"name":"Guest","type":"timeLimit","password":"998877","startTime":1664640056,"endTime":1665331432}'

# Delete passcode
node scripts/switchbot_cli.js cmd DE133622237A deleteKey --param='{"id":"11"}'
```

## IR Remote - Air Conditioner

```bash
# Cool mode, 26°C, auto fan, on
node scripts/switchbot_cli.js cmd 01-202503291504-68270897 setAll --param="26,2,1,on"

# Heat mode, 20°C, low fan, on
node scripts/switchbot_cli.js cmd 01-202503291504-68270897 setAll --param="20,5,2,on"

# Turn off
node scripts/switchbot_cli.js cmd 01-202503291504-68270897 turnOff
```

Parameter format: `{temperature},{mode},{fanSpeed},{powerState}`
- mode: 0/1=auto, 2=cool, 3=dry, 4=fan, 5=heat
- fan: 1=auto, 2=low, 3=medium, 4=high
- power: on/off

## IR Remote - TV

```bash
node scripts/switchbot_cli.js cmd 01-202504011717-10628124 SetChannel --param=5
node scripts/switchbot_cli.js cmd 01-202504011717-10628124 volumeAdd
node scripts/switchbot_cli.js cmd 01-202504011717-10628124 volumeSub
node scripts/switchbot_cli.js cmd 01-202504011717-10628124 channelAdd
```

## IR Remote - Others (DIY custom buttons)

```bash
# Must use --commandType=customize
node scripts/switchbot_cli.js cmd 01-XXXX myButtonName --commandType=customize
```

## Scenes

```bash
# List all scenes
node scripts/switchbot_cli.js scenes

# Execute a scene
node scripts/switchbot_cli.js scene T02-20230101-xxxxxxxx
```
