import React from 'react';

// Top app navigation with logo, connected platforms, and account controls.
export default function Navbar() {
  return (
    <header className="fixed inset-x-0 top-0 z-30 h-[72px] border-b border-zinc-200 bg-[#f5f5f3]/95 backdrop-blur">
      <div className="mx-auto flex h-full max-w-[1440px] items-center justify-between px-4 md:px-6">
        <div className="text-2xl font-semibold tracking-tight">
          <span className="text-violet-600">Connect</span>
          <span className="text-zinc-500">ify</span>
        </div>

        <p className="hidden text-sm text-zinc-500 md:block">Connected: LinkedIn · Instagram</p>

        <div className="flex items-center gap-3">
          <button
            type="button"
            className="rounded-full border border-emerald-500 px-3 py-1.5 text-sm font-medium text-emerald-600"
          >
            Civic verified
          </button>
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-zinc-900 text-sm font-semibold text-white">
            AJ
          </div>
        </div>
      </div>
    </header>
  );
}
