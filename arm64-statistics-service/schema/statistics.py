from datetime import datetime

from pydantic import BaseModel
from typing import List

# 결제내역
class PaymentList(BaseModel):
    payid: int
    payment: str
    paydate: datetime
    parkingtime: str
    carnum: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')  # 출력 시 포맷 지정
        }

# 통계 및 분석
class VisitorStatistics(BaseModel):
    month: str
    visitor_count: int

class PaymentStatistics(BaseModel):
    month: str
    total_payment: float

class StatisticsResponse(BaseModel):
    visitordata: List[VisitorStatistics]
    paymentdata: List[PaymentStatistics]
