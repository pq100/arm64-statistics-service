from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from models.statistics import Payment
from schema.statistics import StatisticsResponse

# 결제내역 조회
def getpaymentlist(db: Session):
    return db.query(Payment).all()

# 통계 및 분석
def get_monthly_payments(db: Session):
    monthly_payments = [0] * 12
    results = db.query(
        extract('month', Payment.paydate).label('month'),
        func.sum(Payment.payment).label('total_payment')
    ).group_by('month').all()

    for month, total_payment in results:
        monthly_payments[int(month) - 1] = total_payment

    return monthly_payments

def get_monthly_visitors(db: Session):
    monthly_visitors = [0] * 12

    # 월별 방문자 수 집계
    results = db.query(
        extract('month', Payment.paydate).label('month'),
        func.count(Payment.payid).label('count')
    ).group_by('month').all()

    # 결과를 monthly_visitors 리스트에 저장
    for month, count in results:
        monthly_visitors[int(month) - 1] = count  # month는 1부터 시작하므로 인덱스를 조정

    return monthly_visitors


def get_statistics(db: Session) -> StatisticsResponse:
    monthly_payments = get_monthly_payments(db)
    monthly_visitors = get_monthly_visitors(db)

    visitordata = [{"month": str(i + 1), "visitor_count": count} for i, count in enumerate(monthly_visitors)]
    paymentdata = [{"month": str(i + 1), "total_payment": total} for i, total in enumerate(monthly_payments)]

    return StatisticsResponse(visitordata=visitordata, paymentdata=paymentdata)