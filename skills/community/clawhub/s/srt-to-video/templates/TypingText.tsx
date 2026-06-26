import React from 'react';
import { useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';

interface TypingTextProps {
  text: string;
  startFrame: number;
  typingSpeed?: number; // frames per character
  fontSize?: number;
  color?: string;
  maxWidth?: number;
}

export const TypingText: React.FC<TypingTextProps> = ({
  text,
  startFrame,
  typingSpeed = 4,
  fontSize = 52,
  color = '#FFFFFF',
  maxWidth = 900,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const localFrame = frame - startFrame;
  if (localFrame < 0) return null;

  // Count only visible characters (not line breaks)
  const visibleText = text.replace(/\n/g, '');
  const totalChars = visibleText.length;
  const typingDuration = totalChars * typingSpeed;
  
  // Number of revealed characters
  const revealedCount = Math.min(
    Math.floor(localFrame / typingSpeed),
    totalChars
  );

  // Cursor blink — blinks during typing, solid for a moment, then blinks after
  const isTyping = revealedCount < totalChars;
  const cursorVisible = isTyping
    ? true // always show cursor while typing
    : Math.sin(localFrame * 0.15) > 0; // blink after done

  // Fade in the whole block
  const fadeIn = interpolate(localFrame, [0, 10], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // Split text into lines for display
  const lines = text.split('\n');
  let globalCharIdx = 0;

  return (
    <div
      style={{
        position: 'absolute',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
        opacity: fadeIn,
      }}
    >
      <div
        style={{
          maxWidth,
          textAlign: 'center',
          lineHeight: 1.9,
          position: 'relative',
        }}
      >
        {lines.map((line, lineIdx) => {
          const lineChars = line.split('');
          const lineStartIdx = globalCharIdx;

          const lineElements = lineChars.map((char, ci) => {
            const charGlobalIdx = lineStartIdx + ci;
            if (charGlobalIdx >= revealedCount) return null;

            const charFrame = localFrame - charGlobalIdx * typingSpeed;
            const scale = interpolate(charFrame, [0, 3], [1.15, 1], {
              extrapolateRight: 'clamp',
            });
            const charOpacity = interpolate(charFrame, [0, 2], [0.5, 1], {
              extrapolateRight: 'clamp',
            });

            return (
              <span
                key={ci}
                style={{
                  display: 'inline',
                  fontSize,
                  fontWeight: 600,
                  color,
                  transform: `scale(${scale})`,
                  opacity: charOpacity,
                  textShadow: `0 0 30px rgba(100, 200, 255, 0.3), 0 0 60px rgba(100, 200, 255, 0.1)`,
                  letterSpacing: '0.05em',
                }}
              >
                {char}
              </span>
            );
          });

          globalCharIdx += lineChars.length;

          // Only show line if any characters are revealed
          if (lineStartIdx >= revealedCount) return null;

          // Show cursor on the last revealed line
          const isLastRevealedLine = lineIdx === lines.length - 1 || 
            globalCharIdx >= revealedCount;
          const showCursor = isLastRevealedLine && localFrame < typingDuration + 90;

          return (
            <div key={lineIdx} style={{ minHeight: fontSize * 1.2 }}>
              {lineElements}
              {showCursor && (
                <span
                  style={{
                    display: 'inline-block',
                    width: 3,
                    height: fontSize * 0.8,
                    backgroundColor: cursorVisible ? 'rgba(100, 220, 255, 0.9)' : 'transparent',
                    marginLeft: 2,
                    verticalAlign: 'middle',
                    boxShadow: cursorVisible ? '0 0 10px rgba(100, 220, 255, 0.5)' : 'none',
                  }}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
