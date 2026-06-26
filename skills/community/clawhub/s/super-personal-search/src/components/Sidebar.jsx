import React from 'react';

const navItems = [
  { label: 'Dashboard', active: true },
  { label: 'Network map', active: false },
  { label: 'Contacts', active: false },
  { label: 'Activity feed', active: false },
  { label: 'AI assistant', active: false },
];

// Fixed left rail navigation with sync metadata.
export default function Sidebar() {
  return (
    <aside className="md:fixed md:left-0 md:top-[72px] md:h-[calc(100vh-72px)] md:w-[230px] border-r border-zinc-200 bg-[#efefec]">
      <div className="flex h-full flex-col px-5 py-6">
        <nav className="space-y-4">
          {navItems.map((item) => (
            <a
              key={item.label}
              href="#"
              className={`flex items-center gap-3 text-sm ${item.active ? 'font-medium text-zinc-900' : 'text-zinc-500'}`}
            >
              <span
                className={`h-2.5 w-2.5 rounded-full border border-zinc-400 ${
                  item.active ? 'border-zinc-900 bg-zinc-900' : 'bg-transparent'
                }`}
              />
              {item.label}
            </a>
          ))}
        </nav>

        <div className="mt-auto text-xs leading-relaxed text-zinc-500">
          <p>Last sync: 2 min ago</p>
          <p>via Apify</p>
        </div>
      </div>
    </aside>
  );
}
