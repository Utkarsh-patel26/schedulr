from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio
import redis.asyncio as redis
from croniter import croniter
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MONGO_DETAILS = os.getenv("MONGO_DETAILS")
REDIS_URL = os.getenv("REDIS_URL")

# MongoDB
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.task_scheduler_db
task_collection = database.get_collection("tasks")

# Redis
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class TaskModel(BaseModel):
    name: str
    cron: str
    nextRun: datetime
    startDate: datetime
    endDate: datetime

@app.post("/api/tasks")
async def create_task(task: TaskModel):
    result = await task_collection.insert_one(task.model_dump())
    return {"id": str(result.inserted_id)}

# Scheduler
async def check_and_queue_tasks():
    while True:
        now = datetime.now() 
        print(f"[{now.strftime('%H:%M:%S')}] Checking tasks...")

        query = {
            "startDate": {"$lte": now},
            "endDate": {"$gte": now},
            "nextRun": {"$lte": now}
        }

        async for task in task_collection.find(query):
            print(f" Sending to Redis: {task['name']}")

           
            await redis_client.lpush("celery_task_queue", task["name"])

            
            cron = croniter(task["cron"], now)
            next_run = cron.get_next(datetime)

            await task_collection.update_one(
                {"_id": task["_id"]},
                {"$set": {"nextRun": next_run}}
            )
            print(f" Updated next run time for: {task['name']}")

        await asyncio.sleep(60)

@app.on_event("startup")
async def start():
    asyncio.create_task(check_and_queue_tasks())