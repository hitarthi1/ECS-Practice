from fastapi import APIRouter, Form
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
from app.utils.send_email import send_email

executor = ThreadPoolExecutor()
router = APIRouter(prefix="/email", tags=["Email"])

class EmailSchema(BaseModel):
    recipient: str
    subject: str
    body: str

@router.post("/send-email/")
def send_email_endpoint(email: str = Form(...)):
    return send_email(email)
