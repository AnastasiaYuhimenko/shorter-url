import uuid

from sqlalchemy import UUID, Column
from sqlalchemy.types import String

from app.db.base import Base


class Url(Base):
    __tablename__ = "urls"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    url = Column(String, nullable=False)
    short_url = Column(String, index=True, unique=True, nullable=False)
