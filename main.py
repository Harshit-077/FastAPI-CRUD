import os
import dotenv
from datetime import datetime, timezone
from random import randint
from typing import Any, Annotated
from contextlib import asynccontextmanager
from sqlmodel import create_engine, SQLModel, Session, Field, select
from fastapi import FastAPI, HTTPException, Response, Depends

dotenv.load_dotenv()

postgres_url = (
    f"postgresql://{os.environ['POSTGRES_USER']}:"
    f"{os.environ['POSTGRES_PASSWORD']}@"
    f"{os.environ['POSTGRES_HOST']}:"
    f"{os.environ['POSTGRES_PORT']}/"
    f"{os.environ['POSTGRES_DB']}"
)
"""
if password:
    postgres_url = (
        f"postgresql+psycopg://{user}:{password}"
        f"@{host}:{port}/{database}"
    )
else:
    postgres_url = (
        f"postgresql+psycopg://{user}"
        f"@{host}:{port}/{database}"
    )
"""
engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class Campaign(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default = None, index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(bind=engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="Summer Launch", due_date = datetime.now()),
                Campaign(name="Halloween", due_date = datetime.now())
            ])
            session.commit()
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

data : Any = [
    {
        "campaign_id" : 1,
        "campaign_name" : "Summer Launch",
        "due_date" : datetime.now(),
        "created_at" : datetime.now()
    },
    {
        "campaign_id" : 2,
        "campaign_name" : "Halloween",
        "due_date" : datetime.now(),
        "created_at" : datetime.now()
    },
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign["campaign_id"] == id:# if campaign.get("campaign_id") == id:
            return {"campaign": campaign}

    raise HTTPException(status_code=404, detail="Campaign not found")

@app.post("/campaigns", status_code = 201)
async def create_campaign(body: dict[str, Any]):
    new: Any = {
        "campaign_id": randint(100, 1000),
        "campaign_name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }
    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            updated: Any = {
                "campaign_id": id,
                "campaign_name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")
            }

            data[index] = updated
            return {"campaign": updated}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.put("/campaigns/{id}")
async def update_campaign(id: int):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Campaign not found")