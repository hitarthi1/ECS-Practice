from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field, model_validator 
import uuid
import logging
import pdb
from app.utils.token_manager import get_current_user
from app.utils.token_manager import generate_token, decode_token
from functools import partial

router = APIRouter()
logger = logging.getLogger(__name__)
class AuthUser(BaseModel):
    email: str | None = None
    logintype: str = Field(..., pattern="^(guest|social)$")
    firstname: str | None = None
    lastname: str | None = None
    socialid: str | None = None
    
    @model_validator(mode="before")
    def validate_fields(cls, values):
        logintype = values.get("logintype")
        if logintype == "guest":
            # Return only logintype for guest users and ignore other fields
            return {"logintype": logintype}
        # If it's social login, other required fields
        required_fields = ["email", "firstname", "socialid"]
        missing_fields = [field for field in required_fields if not values.get(field)]

        if missing_fields:
            raise ValueError(f"Missing required fields for social login: {', '.join(missing_fields)}")

        return values
@router.post("/auth/login")
async def login(user: AuthUser):
    if user.logintype == 'guest' :
        user_data = {
            "session_id": str(uuid.uuid4()),
            "type": user.logintype
        }
    else:
        user_data = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "socialid": user.socialid,
            "type": user.logintype,
            "email": user.email
        }
    token = generate_token(user_data, None, 'User logged in successfully!!')
    return {"token": token}

@router.get('/auth/refresh_token')
async def refresh_token( current_user: dict = Depends(partial(get_current_user, "Refresh token"))):
    existing_session_id = current_user.get("session_id")
    token = generate_token(current_user, existing_session_id, "Refresh token has been generated successfully!")
    return {"token": token}