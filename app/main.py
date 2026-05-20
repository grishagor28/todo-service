import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routers import tasks
from app.stats import stats
from app.logger import logger

Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI(title="Todo Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def tracking_middleware(request: Request, call_next):
    response = await call_next(request)
    stats.record_request(response.status_code)

    extra = {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
    }
    record = logging.LogRecord(
        name=logger.name,
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="request",
        args=(),
        exc_info=None,
    )
    record.extra = extra
    logger.handle(record)

    return response


@app.get("/stats", tags=["service"])
def get_stats():
    return JSONResponse(content=stats.get_stats())


@app.get("/instance", tags=["service"])
def get_instance():
    return JSONResponse(content={
        "instance": os.environ.get("INSTANCE_NAME", "todo-service"),
        "service": "todo-service",
    })


app.include_router(tasks.router)
