import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Graph brand palette
        bg: "#0C0A20",
        panel: "#15122E",
        panelHover: "#1B1738",
        border: "#2A2451",
        ink: "#E8E4FF",
        muted: "#8D86B8",
        dim: "#5A5485",
        accent: "#6F4CFF",
        accentHover: "#8463FF",
        success: "#00FFB2",
        warn: "#FFB547",
        danger: "#FF6B8A",
      },
      fontFamily: {
        sans: ["var(--font-inter-tight)", "Inter", "ui-sans-serif", "system-ui"],
        mono: ["var(--font-jetbrains)", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      animation: {
        pulse_dot: "pulse_dot 1.8s ease-in-out infinite",
        row_in: "row_in 600ms ease-out",
        count_up: "count_up 800ms ease-out",
      },
      keyframes: {
        pulse_dot: {
          "0%,100%": { opacity: "1", boxShadow: "0 0 0 0 rgba(0,255,178,0.5)" },
          "50%": { opacity: "0.6", boxShadow: "0 0 0 8px rgba(0,255,178,0)" },
        },
        row_in: {
          "0%": { opacity: "0", transform: "translateY(-4px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        count_up: {
          "0%": { opacity: "0", transform: "translateY(6px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
