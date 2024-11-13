from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.statistics import PaymentList, StatisticsResponse
from service.database import get_db
from service.statistics import getpaymentlist, get_statistics

router = APIRouter()

# 결제내역 조회
@router.get('/paymentlist', response_model=list[PaymentList])
async def list_paymentlist(db: Session = Depends(get_db)):
    payments = getpaymentlist(db)
    return [PaymentList.model_validate(pay) for pay in payments]


# 통계 및 분석
@router.get("/statistics", response_model=StatisticsResponse)
async def read_statistics(db: Session = Depends(get_db)):
    try:
        stats = get_statistics(db)
        return stats
    except Exception as e:
        return {"error": str(e)}