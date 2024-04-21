from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import subqueryload
from typing import List, Optional
from ..db import get_session
from ..models import Bourbon
from ..schemas.bourbon import BourbonCreate, BourbonUpdate, BourbonInDB
from ..auth_dependencies import get_admin_user

router = APIRouter()


@router.get("/bourbons/{bourbon_name}", tags=["Bourbons"])
async def get_bourbon(bourbon_name: str, session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = (
            select(Bourbon)
            .where(func.lower(Bourbon.name) == bourbon_name.lower())
        )
        result = await s.execute(stmt)
        bourbon = result.scalar()
        if bourbon is None:
            raise HTTPException(
                status_code=404, detail=f"Bourbon {bourbon_name} not found"
            )
        return bourbon


@router.get("/bourbons", tags=["Bourbons"])
async def get_bourbons(count: int = 20, session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = (
            select(Bourbon)
            .order_by(Bourbon.id)
            .limit(count)
        )
        result = await s.execute(stmt)
        bourbons = result.scalars().all()
        return bourbons


@router.post("/bourbons", response_model=List[BourbonInDB], tags=["Bourbons"])
async def create_bourbons(
    bourbons: List[BourbonCreate],
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    created_bourbons = []

    async with session as s:
        # Begin a transaction
        await s.begin()

        for bourbon in bourbons:
            # Create the new bourbon
            new_bourbon = Bourbon(
                **bourbon.dict()
            )

            s.add(new_bourbon)
            await s.flush()  # Ensure new_bourbon gets an ID
            created_bourbons.append(new_bourbon)

        try:
            await s.commit()
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Bourbon already exists")

    return created_bourbons


# Update an existing Bourbon
@router.put("/bourbons/{bourbon_id}", response_model=BourbonInDB, tags=["Bourbons"])
async def update_bourbon(
    bourbon_id: int,
    bourbon: BourbonUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_bourbon = await s.get(Bourbon, bourbon_id)
        if existing_bourbon is None:
            raise HTTPException(status_code=404, detail="Bourbon not found")
        for key, value in bourbon.dict(exclude_unset=True).items():
            setattr(existing_bourbon, key, value)
        try:
            await s.commit()
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Bourbon already exists...")
        return existing_bourbon


# Delete an existing Bourbon
@router.delete("/bourbons/{bourbon_id}", response_model=dict, tags=["Bourbons"])
async def delete_bourbon(
    bourbon_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_bourbon = await s.get(Bourbon, bourbon_id)
        if existing_bourbon is None:
            raise HTTPException(status_code=404, detail="Bourbon not found")
        await s.delete(existing_bourbon)
        await s.commit()
        return {"Bourbon deleted": existing_bourbon.name}