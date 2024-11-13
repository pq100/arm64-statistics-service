import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from routes import statistics
from service.database import SessionLocal, create_tables
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()

# 기본 매트릭 설정
Instrumentator().instrument(app).expose(app)

# CORS 설정
# origins = [
#     "http://localhost:3000",  # 허용할 프론트엔드 도메인
#     "http://127.0.0.1:3000"
# ]
origins = os.getenv('CORS_ORIGINS','http://localhost:3000').split(",")
print('CORS -> ',origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(statistics.router)

@app.get('/mariadb')
def mariadb():
    try:
        with SessionLocal() as conn:
            result = conn.execute(text('SELECT SYSDATE();')).scalar()
            return {'msg': 'Database Connection Successful!!', 'result': f'{result}'}
    except Exception as ex:
        logging.error(f"Database Connection Failed: {ex}")
        return {'msg': 'Database Connection Failed!!', 'error': str(ex)}

if __name__ == '__main__':
    create_tables()
    uvicorn.run('main:app', port=8003, reload=True)