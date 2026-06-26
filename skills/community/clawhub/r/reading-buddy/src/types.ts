// 数据类型定义

export interface Book {
  id: number;
  title: string;
  author: string;
  description: string;
  coverUrl?: string;
  tags: string[];
  category?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ReadingRoom {
  id: number;
  bookId: number;
  name: string;
  description?: string;
  hostId: string;
  maxMembers: number;
  startTime: string;
  endTime?: string;
  status: RoomStatus;
  createdAt: string;
}

export enum RoomStatus {
  PENDING = 'pending',
  ACTIVE = 'active',
  ENDED = 'ended'
}

export interface RoomMember {
  id: number;
  roomId: number;
  userId: string;
  userName: string;
  joinedAt: string;
}

export interface ChatMessage {
  id: number;
  roomId: number;
  userId: string;
  userName: string;
  content: string;
  messageType: MessageType;
  createdAt: string;
}

export enum MessageType {
  TEXT = 'text',
  INSIGHT = 'insight'
}

export interface User {
  id: string;
  name: string;
  avatar?: string;
  createdAt: string;
}
