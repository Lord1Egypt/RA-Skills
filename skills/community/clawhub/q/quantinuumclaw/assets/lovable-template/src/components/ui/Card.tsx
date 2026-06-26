import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
}

export function Card({ className = '', children }: CardProps) {
  return (
    <div className={`bg-gray-800 border border-gray-700 rounded-lg shadow-lg ${className}`}>
      {children}
    </div>
  )
}

export function CardHeader({ className = '', children }: CardProps) {
  return <div className={`p-4 border-b border-gray-700 ${className}`}>{children}</div>
}

export function CardTitle({ className = '', children }: CardProps) {
  return <h3 className={`text-lg font-semibold ${className}`}>{children}</h3>
}

export function CardContent({ className = '', children }: CardProps) {
  return <div className={`p-4 ${className}`}>{children}</div>
}
