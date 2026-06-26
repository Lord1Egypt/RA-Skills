// Detect Hidden script example
// Uses the Detect Hidden skill, targets self, waits briefly, and branches on the system message.
// Adjust the system-message substring if your client build uses different wording.

skill 'detecthidden'
waitfortarget
target 'self'
wait 400

if insysmsg 'you can see nothing'
    overhead 'All clear'
else
    say 'I ban thee'
    waitfortarget
    target closest grey humanoid
endif
