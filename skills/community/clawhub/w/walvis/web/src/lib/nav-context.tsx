import { createContext, useContext, useState, type ReactNode } from 'react';

interface NavContextValue {
  centerLabel: string;
  setCenterLabel: (label: string) => void;
}

const NavContext = createContext<NavContextValue>({
  centerLabel: '',
  setCenterLabel: () => {},
});

export function NavProvider({ children }: { children: ReactNode }) {
  const [centerLabel, setCenterLabel] = useState('');
  return (
    <NavContext.Provider value={{ centerLabel, setCenterLabel }}>
      {children}
    </NavContext.Provider>
  );
}

export function useNavContext() {
  return useContext(NavContext);
}
