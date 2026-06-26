from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Comment:
    user: str = ""
    text: str = ""
    likes: str = ""
    time: str = ""


@dataclass
class Note:
    id: str = ""
    title: str = ""
    content: str = ""
    url: str = ""
    author: str = ""
    author_id: str = ""
    likes: str = ""
    collects: str = ""
    comments_count: str = ""
    type: str = ""          # "video" | "normal"
    images: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "author": self.author,
            "author_id": self.author_id,
            "likes": self.likes,
            "collects": self.collects,
            "comments_count": self.comments_count,
            "type": self.type,
            "images": self.images,
            "tags": self.tags,
            "comments": [c.__dict__ for c in self.comments],
        }


@dataclass
class UserProfile:
    user_id: str = ""
    nickname: str = ""
    description: str = ""
    followers: str = ""
    following: str = ""
    likes_collected: str = ""
    notes_count: str = ""
    avatar: str = ""
