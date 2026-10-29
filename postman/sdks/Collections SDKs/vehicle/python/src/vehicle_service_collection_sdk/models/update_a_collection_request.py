from __future__ import annotations
from pydantic import Field
from typing import Optional
from typing import Any
from typing import Union
from .utils.base_model import BaseModel


class UpdateACollectionRequest(BaseModel):
    """UpdateACollectionRequest

    :param nick_name: nick_name, defaults to None
    :type nick_name: str, optional
    :param vin: vin, defaults to None
    :type vin: str, optional
    :param make: make, defaults to None
    :type make: str, optional
    :param model: model, defaults to None
    :type model: str, optional
    :param year: year, defaults to None
    :type year: str, optional
    :param miles: miles, defaults to None
    :type miles: float, optional
    """

    nick_name: Optional[str] = Field(
        alias="nickName", serialization_alias="nickName", default=None
    )
    vin: Optional[str] = Field(default=None)
    make: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)
    year: Optional[str] = Field(default=None)
    miles: Optional[float] = Field(default=None)
