from pydantic import BaseModel, HttpUrl


class Url(BaseModel):
    url: str
    short_url: str


class UrlCreateRequest(BaseModel):
    url: HttpUrl


class UrlCreateResponse(BaseModel):
    url: str
    short_url: str
