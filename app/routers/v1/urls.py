from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from app.db.base import SessionDep
from app.schemas.urls import UrlCreateRequest, UrlCreateResponse
from app.services.url_service import UrlService

router = APIRouter(prefix="/urls", tags=["urls"])


@router.post("/short", response_model=UrlCreateResponse)
async def create_url(request: UrlCreateRequest, session: SessionDep):
    try:
        response = await UrlService(session).create_short_url(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/{short_url}")
async def get_url(short_url: str, session: SessionDep):
    url = await UrlService(session).get_url_by_short_url(short_url)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    return RedirectResponse(
        url=url.url,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
