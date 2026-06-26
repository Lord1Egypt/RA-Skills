/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from "react";
import { motion, useScroll, useTransform } from "motion/react";
import { 
  Download, 
  Github, 
  CheckCircle2, 
  XCircle, 
  Terminal as TerminalIcon, 
  Copy, 
  Check, 
  Globe, 
  Mic, 
  Zap, 
  Code, 
  Eye, 
  Box, 
  Cpu, 
  Languages, 
  DollarSign 
} from "lucide-react";

const Navbar = () => (
  <header className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
    <nav className="max-w-6xl mx-auto flex items-center justify-between bg-charcoal/95 backdrop-blur-sm px-6 py-3 sketchy-box">
      <div className="flex items-center gap-2">
        <span className="text-coral text-2xl font-bold font-serif">XiaBB</span>
      </div>
      <div className="hidden md:flex items-center gap-8 text-sm font-medium">
        <a className="hover:text-coral transition-colors" href="#how-it-works">How It Works</a>
        <a className="hover:text-coral transition-colors" href="#features">Features</a>
        <a className="hover:text-coral transition-colors" href="#compare">Compare</a>
        <a className="hover:text-coral transition-colors" href="#terminal">Terminal</a>
      </div>
      <div className="flex items-center gap-4">
        <a className="text-sm hover:text-coral transition-colors" href="https://github.com" target="_blank" rel="noreferrer">GitHub</a>
        <button className="bg-coral text-charcoal px-4 py-2 text-sm font-bold sketchy-button hover:bg-transparent hover:text-coral">
          Download
        </button>
      </div>
    </nav>
  </header>
);

const Hero = () => {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, 50]);
  const rotate = useTransform(scrollY, [0, 500], [2, 12]);

  return (
    <section className="max-w-6xl mx-auto px-6 pt-32 pb-24 flex flex-col md:flex-row items-center gap-12" id="hero">
      <motion.div 
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="flex-1 space-y-8"
      >
        <h1 className="text-6xl md:text-8xl font-serif font-bold leading-tight">
          Stop Typing.<br />
          Start <span className="text-coral">瞎BB</span>.
        </h1>
        <p className="text-xl text-cream/80 max-w-lg leading-relaxed">
          The free macOS voice-to-text tool built for Vibe Coding. 
          Powered by Google's best-in-class Gemini API. Keep your flow, ditch the keys.
        </p>
        <div className="flex flex-wrap gap-4">
          <button className="bg-coral text-charcoal px-8 py-4 text-lg font-bold sketchy-button flex items-center gap-2">
            <Download className="w-5 h-5" />
            Download for macOS
          </button>
          <button className="px-8 py-4 text-lg font-bold sketchy-button flex items-center gap-2">
            <Github className="w-5 h-5" />
            View on GitHub
          </button>
        </div>
        <div className="flex items-center gap-2 text-sm text-cream/60">
          <CheckCircle2 className="w-4 h-4 text-green-accent" />
          Apple Silicon (M1/M2/M3) & Intel Support
        </div>
      </motion.div>
      
      <motion.div 
        style={{ y, rotate }}
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="flex-1 relative"
      >
        <div className="relative z-10 p-4 sketchy-box bg-surface">
          <img 
            alt="XiaBB Fusion Mascot" 
            className="w-full h-auto rounded-lg grayscale hover:grayscale-0 transition-all duration-500" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuBp0Rjg5-jfyS3hoTZx-aM9ydZ0yQytUGTNI7Off4jsWszW-YuI7l5DCGxGLev56LYEZ5o_Yi53IHfDzqISqU8kne3q0-8sY6bSZ1h2CoAgkgn_Y2htvPjs-qoaNsT1j8VP4pQ5m1fSEfQSLgHKEmHyfg1vUPPIq6wBwdeEvwjJw0kU9RrudKgRZpkB5eZe7JI33IdS6O2Ck5fpncn5x4ZV43BytZKkIqP33mDiM7R6mGyOvK3RTpwSWMutc0P4nu9DQUqP8MkNj0w"
            referrerPolicy="no-referrer"
          />
          <div className="absolute -top-4 -right-4 bg-yellow-accent text-charcoal px-3 py-1 text-xs font-bold rotate-12 sketchy-box">
            *bzzt*
          </div>
        </div>
        <div className="absolute -top-10 -left-10 w-32 h-32 bg-coral/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-10 -right-10 w-48 h-48 bg-yellow-accent/5 rounded-full blur-3xl"></div>
      </motion.div>
    </section>
  );
};

const HowItWorks = () => (
  <section className="py-24 bg-surface/30" id="how-it-works">
    <div className="max-w-5xl mx-auto px-6 text-center mb-16">
      <h2 className="text-4xl font-serif font-bold mb-4">Zero config. Just talk.</h2>
      <p className="text-cream/60">Three steps from a thought in your head to markdown on your screen.</p>
    </div>
    <div className="max-w-6xl mx-auto px-6 relative">
      <div className="absolute left-1/2 top-0 bottom-0 timeline-line -translate-x-1/2 hidden md:block"></div>
      
      {/* Step 1 */}
      <div className="flex flex-col md:flex-row items-center gap-12 mb-24 relative">
        <div className="flex-1 text-right hidden md:block">
          <h3 className="text-2xl font-bold mb-2">Press and hold Globe key</h3>
          <p className="text-cream/60">Invoke BB instantly from anywhere. No need to click around or find the window.</p>
        </div>
        <div className="z-10 bg-coral text-charcoal w-10 h-10 rounded-full flex items-center justify-center font-bold border-2 border-cream">1</div>
        <div className="flex-1">
          <div className="sketchy-box p-2 bg-surface -rotate-1">
            <img 
              alt="Press Globe Key" 
              className="w-full h-48 object-cover rounded shadow-lg" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuCzjaCKn3neUF_bFSv4dtNDSOb_LBu1bEQ-v7sB9tzJiiig7lptCcslVN_FIkzQcKkCvmRbOfHbFQC3X-7zT6Mj-vxBAF-EFlssnWTDc2aZCGXbrp71U2nmqC20P6w9giRB1n1-HDLJsLi-1EMbMyqt8wxCgN95zn_AidZwUdF9mFubday6spjKilmrufHz5vWNeJuno9yQiDQnGvxZeUVBELKv9WD1JUTaRdO4j0nVOVYsuDdoLEJmVYwyV_HdQlXj8RQVP4SKrmU"
              referrerPolicy="no-referrer"
            />
          </div>
          <div className="md:hidden mt-4 text-center">
            <h3 className="text-xl font-bold mb-2">Press and hold Globe key</h3>
            <p className="text-cream/60 text-sm">Invoke BB instantly from anywhere.</p>
          </div>
        </div>
      </div>

      {/* Step 2 */}
      <div className="flex flex-col md:flex-row-reverse items-center gap-12 mb-24 relative">
        <div className="flex-1 text-left hidden md:block">
          <h3 className="text-2xl font-bold mb-2">Speak your mind</h3>
          <p className="text-cream/60">Rambling is encouraged. BB processes your voice locally first, understanding context and code naturally.</p>
        </div>
        <div className="z-10 bg-yellow-accent text-charcoal w-10 h-10 rounded-full flex items-center justify-center font-bold border-2 border-cream">2</div>
        <div className="flex-1">
          <div className="sketchy-box p-2 bg-surface rotate-1">
            <img 
              alt="Lobster Mascot Talking" 
              className="w-full h-48 object-cover rounded shadow-lg" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuDKNtzSwfHUamH71heg4okO3eNVbZbAkWbQYgu3FfcXTNLXNtNC70BSYEFGkCgWKs1SkH2V_i2fgN51wy8d5Z0qizo2tqXBXJcasuVnUGtdIOn02bMT96jkWubnAIAxIA3Vt2O3Ei9APQWm97PB_6KeYuhT8hlx9bvRyZ_F1T8g7IQm7nyJuZBLq6Vx_A4hROVpHXok8KfgseEmHlZrUVoa6gJwha8pqixEaJZfZUmPEZGnUiSa_Z6HREqI7j_q6IbAx317Q9XQ-N8"
              referrerPolicy="no-referrer"
            />
          </div>
          <div className="md:hidden mt-4 text-center">
            <h3 className="text-xl font-bold mb-2">Speak your mind</h3>
            <p className="text-cream/60 text-sm">BB processes your voice with context.</p>
          </div>
        </div>
      </div>

      {/* Step 3 */}
      <div className="flex flex-col md:flex-row items-center gap-12 relative">
        <div className="flex-1 text-right hidden md:block">
          <h3 className="text-2xl font-bold mb-2">Text appears instantly</h3>
          <p className="text-cream/60">Done talking? Your nonsense is already formatted as perfect markdown and copied to your clipboard.</p>
        </div>
        <div className="z-10 bg-green-accent text-charcoal w-10 h-10 rounded-full flex items-center justify-center font-bold border-2 border-cream">3</div>
        <div className="flex-1">
          <div className="sketchy-box p-4 bg-charcoal border-green-accent/50 -rotate-1">
            <div className="flex gap-1.5 mb-3">
              <div className="w-2.5 h-2.5 rounded-full bg-coral/50"></div>
              <div className="w-2.5 h-2.5 rounded-full bg-yellow-accent/50"></div>
              <div className="w-2.5 h-2.5 rounded-full bg-green-accent/50"></div>
            </div>
            <code className="text-sm font-mono block">
              <span className="text-coral"># Project Ideas</span><br />
              - Build a lo-fi dictation app<br />
              - Name the mascot <span className="text-yellow-accent">BB</span><br />
              - 搞一个中英混搭的 <span className="text-green-accent">Vibe Coding</span> 工具
            </code>
          </div>
          <div className="md:hidden mt-4 text-center">
            <h3 className="text-xl font-bold mb-2">Text appears instantly</h3>
            <p className="text-cream/60 text-sm">Formatted markdown ready to paste.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
);

const Features = () => {
  const features = [
    {
      icon: <DollarSign className="w-8 h-8" />,
      title: "永久免费 (Gemini API)",
      desc: "Powered by your own Gemini API key. Free tier is generous enough for 24/7 rambling."
    },
    {
      icon: <Languages className="w-8 h-8" />,
      title: "中英混搭",
      desc: "Perfectly understands \"Vibe coding is so cool 真的太顶了\" without missing a beat."
    },
    {
      icon: <Eye className="w-8 h-8" />,
      title: "实时预览",
      desc: "Watch your nonsense turn into structure in real-time as you speak."
    },
    {
      icon: <Box className="w-8 h-8" />,
      title: "280KB 极简",
      desc: "Lightweight binary. No Electron bloat. Just a clean Swift tool sitting in your menu bar."
    },
    {
      icon: <Code className="w-8 h-8" />,
      title: "开源 MIT",
      desc: "Hackable and transparent. Check the source, build your own version, keep it forever."
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "LLM 引擎",
      desc: "Not just STT. It's an intelligent layer that formats code, cleans up \"umms\", and adds markdown."
    }
  ];

  return (
    <section className="py-24 max-w-6xl mx-auto px-6" id="features">
      <div className="text-center mb-16">
        <h2 className="text-4xl font-serif font-bold mb-4 text-yellow-accent">Built for midnight coding sessions.</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {features.map((f, i) => (
          <motion.div 
            key={i}
            whileHover={{ y: -5, x: -2 }}
            className="bg-surface p-8 sketchy-box hover:shadow-[6px_6px_0_0_rgba(234,105,98,0.8)] transition-all"
          >
            <div className="text-coral mb-4">{f.icon}</div>
            <h3 className="text-xl font-bold mb-3">{f.title}</h3>
            <p className="text-cream/70 text-sm leading-relaxed">{f.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
};

const Comparison = () => (
  <section className="py-24 max-w-6xl mx-auto px-6" id="compare">
    <div className="text-center mb-16">
      <h2 className="text-4xl font-serif font-bold mb-4">Why choose XiaBB?</h2>
      <p className="text-cream/60">Ditch the subscriptions and cloud latency. Keep your thoughts local.</p>
    </div>
    <div className="grid md:grid-cols-2 gap-8 items-stretch">
      <div className="bg-surface/50 p-10 sketchy-box border-charcoal opacity-80">
        <div className="flex items-center gap-3 mb-8 text-cream/40">
          <XCircle className="w-6 h-6" />
          <span className="text-2xl font-bold">Them</span>
        </div>
        <ul className="space-y-6">
          <li className="flex items-center gap-3 text-cream/50">
            <span className="text-coral">✕</span> Requires proprietary API keys
          </li>
          <li className="flex items-center gap-3 text-cream/50">
            <span className="text-coral">✕</span> Monthly subscriptions
          </li>
          <li className="flex items-center gap-3 text-cream/50">
            <span className="text-coral">✕</span> Cloud latency issues
          </li>
          <li className="flex items-center gap-3 text-cream/50">
            <span className="text-coral">✕</span> Privacy concerns & data logging
          </li>
        </ul>
      </div>
      
      <div className="bg-surface p-10 sketchy-box border-coral relative">
        <div className="absolute -top-4 -right-4 bg-green-accent text-charcoal px-3 py-1 text-sm font-bold rotate-6 sketchy-box">
          Free Forever
        </div>
        <div className="flex items-center gap-3 mb-8 text-coral">
          <CheckCircle2 className="w-6 h-6" />
          <span className="text-2xl font-bold">XiaBB</span>
        </div>
        <ul className="space-y-6">
          <li className="flex items-center gap-3 font-medium">
            <span className="text-green-accent">✓</span> Zero config out of the box
          </li>
          <li className="flex items-center gap-3 font-medium">
            <span className="text-green-accent">✓</span> 100% Free & Open Source
          </li>
          <li className="flex items-center gap-3 font-medium">
            <span className="text-green-accent">✓</span> Instant local processing
          </li>
          <li className="flex items-center gap-3 font-medium">
            <span className="text-green-accent">✓</span> Total offline privacy
          </li>
        </ul>
      </div>
    </div>
  </section>
);

const Terminal = () => {
  const [copied, setCopied] = useState(false);
  const command = "brew install --cask xiabb";

  const copyCommand = () => {
    navigator.clipboard.writeText(command);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="py-24 max-w-4xl mx-auto px-6" id="terminal">
      <div className="sketchy-box bg-black/40 overflow-hidden">
        <div className="bg-surface px-4 py-2 flex items-center gap-2 border-b border-cream/20">
          <div className="w-3 h-3 rounded-full bg-coral"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-accent"></div>
          <div className="w-3 h-3 rounded-full bg-green-accent"></div>
          <span className="text-xs text-cream/40 font-mono ml-2">terminal — zsh</span>
        </div>
        <div className="p-8 font-mono text-lg flex flex-col md:flex-row items-start md:items-center gap-4">
          <div className="flex items-center gap-4 flex-1">
            <span className="text-green-accent">$</span>
            <code className="text-cream">{command}</code>
          </div>
          <button 
            onClick={copyCommand}
            className="text-cream/40 hover:text-coral transition-colors flex items-center gap-2"
            title="Copy command"
          >
            {copied ? <Check className="w-6 h-6 text-green-accent" /> : <Copy className="w-6 h-6" />}
            <span className="text-xs uppercase font-bold tracking-widest">{copied ? "Copied!" : "Copy"}</span>
          </button>
        </div>
      </div>
    </section>
  );
};

const Footer = () => (
  <footer className="py-12 border-t border-cream/10 mt-12">
    <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-8">
      <div className="text-center md:text-left">
        <h4 className="text-xl font-serif font-bold text-coral mb-2">XiaBB</h4>
        <p className="text-cream/40 text-sm">Built with ❤️ for the Vibe Coding community.</p>
      </div>
      <div className="flex gap-8 text-sm text-cream/60">
        <a className="hover:text-coral transition-colors" href="#">Documentation</a>
        <a className="hover:text-coral transition-colors" href="#">Privacy</a>
        <a className="hover:text-coral transition-colors" href="#">Twitter</a>
        <a className="hover:text-coral transition-colors" href="#">MIT License</a>
      </div>
      <div className="text-sm text-cream/40 italic">
        © 2024 XiaBB Studio. No lobsters were harmed.
      </div>
    </div>
  </footer>
);

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main>
        <Hero />
        <HowItWorks />
        <Features />
        <Comparison />
        <Terminal />
      </main>
      <Footer />
    </div>
  );
}
