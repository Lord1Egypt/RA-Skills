#!/bin/bash
# Sony Bravia TV Control Helper
# Usage: tv.sh {command} [args]
TV="192.168.50.120"
PSK="19890801"

ircc() {
  curl -s -X POST "http://$TV/sony/ircc" \
    -H "Content-Type: text/xml; charset=utf-8" \
    -H 'SOAPACTION: "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"' \
    -H "X-Auth-PSK: $PSK" \
    -d "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>$1</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>"
}

case "$1" in
  power-on)    ircc "AAAAAQAAAAEAAAAuAw==" ;;
  power-off)   ircc "AAAAAQAAAAEAAAAvAw==" ;;
  toggle)      ircc "AAAAAQAAAAEAAAAVAw==" ;;
  vol-up)      ircc "AAAAAQAAAAEAAAASAw==" ;;
  vol-down)    ircc "AAAAAQAAAAEAAAATAw==" ;;
  mute)        ircc "AAAAAQAAAAEAAAAUAw==" ;;
  ch-up)       ircc "AAAAAQAAAAEAAAAQAw==" ;;
  ch-down)     ircc "AAAAAQAAAAEAAAARAw==" ;;
  up)          ircc "AAAAAQAAAAEAAAB0Aw==" ;;
  down)        ircc "AAAAAQAAAAEAAAB1Aw==" ;;
  left)        ircc "AAAAAQAAAAEAAAA0Aw==" ;;
  right)       ircc "AAAAAQAAAAEAAAAzAw==" ;;
  confirm)     ircc "AAAAAQAAAAEAAABlAw==" ;;
  home)        ircc "AAAAAQAAAAEAAABgAw==" ;;
  exit)        ircc "AAAAAQAAAAEAAABjAw==" ;;
  options)     ircc "AAAAAgAAAJcAAAA2Aw==" ;;
  back)        ircc "AAAAAgAAAJcAAAAjAw==" ;;
  play)        ircc "AAAAAgAAAJcAAAAaAw==" ;;
  pause)       ircc "AAAAAgAAAJcAAAAZAw==" ;;
  stop)        ircc "AAAAAgAAAJcAAAAYAw==" ;;
  rewind)      ircc "AAAAAgAAAJcAAAAbAw==" ;;
  forward)     ircc "AAAAAgAAAJcAAAAcAw==" ;;
  hdmi1)       ircc "AAAAAgAAABoAAABaAw==" ;;
  hdmi2)       ircc "AAAAAgAAABoAAABbAw==" ;;
  hdmi3)       ircc "AAAAAgAAABoAAABcAw==" ;;
  hdmi4)       ircc "AAAAAgAAABoAAABdAw==" ;;
  open-url)
    if [ -z "$2" ]; then
      echo "Usage: tv.sh open-url <url>"
      exit 1
    fi
    curl -s -X POST "http://$TV/sony/appControl" \
      -H "Content-Type: application/json" \
      -H "X-Auth-PSK: $PSK" \
      -d "{\"method\":\"setActiveApp\",\"params\":[{\"uri\":\"localapp://webappruntime?url=$2\",\"data\":\"\"}],\"id\":1,\"version\":\"1.0\"}"
    ;;
  kill)
    curl -s -X POST "http://$TV/sony/appControl" \
      -H "Content-Type: application/json" \
      -H "X-Auth-PSK: $PSK" \
      -d '{"method":"terminateApps","params":[],"id":1,"version":"1.0"}'
    ;;
  volume)
    curl -s -X POST "http://$TV/sony/audio" \
      -H "Content-Type: application/json" \
      -H "X-Auth-PSK: $PSK" \
      -d '{"method":"getVolumeInformation","params":[{"target":"speaker"}],"id":1,"version":"1.0"}'
    ;;
  power)
    curl -s -X POST "http://$TV/sony/system" \
      -H "Content-Type: application/json" \
      -H "X-Auth-PSK: $PSK" \
      -d '{"method":"getPowerStatus","params":[],"id":1,"version":"1.0"}'
    ;;
  *)
    echo "Sony Bravia TV Control"
    echo ""
    echo "Usage: tv.sh {command} [args]"
    echo ""
    echo "Power:    power-on | power-off | toggle"
    echo "Volume:   vol-up | vol-down | mute | volume"
    echo "Channel:  ch-up | ch-down"
    echo "Nav:      up | down | left | right | confirm | home | exit | options | back"
    echo "Media:    play | pause | stop | rewind | forward"
    echo "Input:    hdmi1 | hdmi2 | hdmi3 | hdmi4"
    echo "Browser:  open-url <url> | kill"
    echo "Status:   power | volume"
    ;;
esac
