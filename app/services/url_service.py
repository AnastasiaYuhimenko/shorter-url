import secrets
import string

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.unit_of_work import UnitOfWork
from app.models.url import Url
from app.schemas.urls import UrlCreateRequest, UrlCreateResponse


class UrlService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_short_url(self, request: UrlCreateRequest) -> UrlCreateResponse:
        short_code = self._generate_short_code()
        async with UnitOfWork(self.session) as uow:
            existing = await uow.url_repo.get_by_url(str(request.url))
            if existing:
                return UrlCreateResponse(short_url=existing.short_url, url=existing.url)

            existing = await uow.url_repo.get_by_short_url(short_code)
            if existing:
                return ValueError("Short code already exists")

            url_obj = Url(short_url=str(short_code), url=str(request.url))
            await uow.url_repo.add(url_obj)
            await uow.commit()

        return UrlCreateResponse(short_url=url_obj.short_url, url=url_obj.url)

    async def get_url_by_short_url(self, short_url: str) -> Url | None:
        async with UnitOfWork(self.session) as uow:
            return await uow.url_repo.get_by_short_url(short_url)

    def _generate_short_code(self, length: int = 7) -> str:
        chars = string.ascii_letters + string.digits
        return "".join(secrets.choice(chars) for _ in range(length))
