#!/bin/bash
# simple script to set volume level and send message on desktop.
# dependencies: 
#   - pulseaudio
#   - jq
#   - dunst

# Check if the script has exactly one argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <0 or 1>"
    exit 1
fi

# Check if the argument is 0 or 1
if [ "$1" -eq 0 ]; then
    pactl set-sink-volume @DEFAULT_SINK@ +5%
else
    pactl set-sink-volume @DEFAULT_SINK@ -5%
fi


vol=`pactl --format=json list sinks | jq -r '.[] | select(.state == "RUNNING") | .volume.["front-left"].value_percent'`

dunstify -r 1 "Volume ${vol}"
