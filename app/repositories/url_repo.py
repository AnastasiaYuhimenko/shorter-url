from sqlalchemy import select

from app.models.url import Url
from app.repositories.base_repo import BaseRepo


class UrlRepository(BaseRepo[Url]):
    async def get_by_short_url(self, short_url: str) -> Url | None:
        obj = await self.session.execute(select(self.model).where(self.model.short_url == short_url))
        return obj.scalar_one_or_none()

    async def get_by_url(self, url: str) -> Url | None:
        obj = await self.session.execute(select(self.model).where(self.model.url == url))
        return obj.scalar_one_or_none()
