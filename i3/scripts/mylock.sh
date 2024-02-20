#!/bin/sh

B='#00000000'  # blank
C='#4c566a'  # clear ish
D='#88c0d0'  # default
T='#d8dee9'  # text
W='#bf616a'  # wrong
V='#ebcb8b'  # verifying
d='ebcb8b'   # date color

i3lock \
#--insidevercolor=$C   \
--ringvercolor=$V     \
\
--insidewrongcolor=$C \
--ringwrongcolor=$W   \
\
--insidecolor=$B      \
--ringcolor=$D        \
--linecolor=$B        \
--separatorcolor=$D   \
\
--verifcolor=$T        \
--wrongcolor=$T        \
--timecolor=$T        \
--datecolor=$T        \
--layoutcolor=$T      \
--keyhlcolor=$W       \
--bshlcolor=$W        \
\
--datecolor=$d        \
\
--screen 1            \
--blur 5              \
--clock               \
--indicator           \
--timestr="%H:%M:%S"  \
--datestr="%A, %m %Y" \
