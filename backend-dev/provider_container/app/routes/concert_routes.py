import asyncio
from fastapi import APIRouter, HTTPException, Query, Depends
from app.utils.token_manager import get_current_user,verify_api_secret_key  # Secure routes
from app.utils.concert_service import get_future_concerts, create_multiple_concerts, get_concert
from app.models.concert_model import Concert
from app.database.database import concert_collection
from typing import List, Literal
from concurrent.futures import ThreadPoolExecutor
from functools import partial

executor = ThreadPoolExecutor()
router = APIRouter(prefix="/concerts", tags=["Concerts"])

@router.get("/", status_code=200)
async def list_future_concerts(
    status: Literal["available", "sold", "all"] = "all",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(partial(get_current_user, "Access token"))):
    """Return future concerts with optional status filtering & pagination."""
    concerts = get_future_concerts(status_filter=status, page=page, limit=limit)
    return {
        "page": page,
        "limit": limit,
        "concerts": concerts
    }

@router.get("/{concert_id}",status_code=200)
async def concert_details(concert_id: str,  current_user: dict = Depends(partial(get_current_user, "Access token"))):
    concert = get_concert(concert_id)
    return {
        "concerts": concert
    }

@router.post("/", status_code=201)
async def create_concerts(concerts: List[Concert],secret_key: str = Depends(verify_api_secret_key)):
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, create_multiple_concerts, concerts)
        return {"message": "Concerts added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))