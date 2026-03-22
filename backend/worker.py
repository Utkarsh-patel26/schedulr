import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

#celery 
celery_app = Celery(
    "task_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task(name="print_task_name")
def execute_periodic_task(name: str):
    print("\n" + "="*50)
    print(f" CELERY WORKER PICKED UP TASK: {name}")
    print("="*50 + "\n")
    return f"Processed {name}"